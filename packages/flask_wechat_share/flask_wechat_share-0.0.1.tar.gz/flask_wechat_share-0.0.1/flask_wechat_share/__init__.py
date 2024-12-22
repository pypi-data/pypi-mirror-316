import hashlib
import random
import requests
import string
import time
from jinja2 import Environment, PackageLoader
from flask import current_app, request, url_for
from markupsafe import Markup


def timestamp():
    return int(time.time())


def token_lifetime(expires_in):
    return timestamp() + expires_in - current_app.config['WECHAT_TOKEN_EXPIRY_OFFSET']


class WeChatShare:
    ACCESS_TOKEN_CACHE = {'token': None, 'expires_at': 0}
    JSAPI_TICKET_CACHE = {'ticket': None, 'expires_at': 0}

    ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    JSAPI_TICKET_URL = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type=jsapi"

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        self.jinja2_env = Environment(loader=PackageLoader(__name__, 'templates'))

    def init_app(self, app):
        app.config.setdefault('WECHAT_APP_ID', '')
        app.config.setdefault('WECHAT_APP_SECRET', '')
        app.config.setdefault('WECHAT_TOKEN_EXPIRY_OFFSET', 300)

        app.config.setdefault(
            'WECHAT_SHARE_JS_API_LIST',
            [
                'updateAppMessageShareData',
                'updateTimelineShareData'
            ]
        )
        app.config.setdefault('WECHAT_SHARE_URL', '/js-sdk.php')
        app.config.setdefault('WECHAT_SHARE_ENDPOINT', '_wechat_share')
        app.config.setdefault('WECHAT_SHARE_DEBUG', False)

        app.jinja_env.globals['wechat_share'] = self.wechat_share
        app.jinja_env.globals['wechat_share_ajax'] = self.wechat_share_ajax

        app.add_url_rule(
            rule=app.config.get('WECHAT_SHARE_URL'),
            endpoint=app.config.get('WECHAT_SHARE_ENDPOINT'),
            view_func=self.as_view
        )

    def as_view(self):
        timestamp_str = str(timestamp())
        nonce_str = self.generate_nonce_str()
        signature_str = self.generate_signature(
            nonce_str,
            timestamp_str,
            request.args.get('url')
        )
        return {
            'appid': current_app.config.get('WECHAT_APP_ID'),
            'timestamp': timestamp_str,
            'nonce_str': nonce_str,
            'signature': signature_str,
        }

    @staticmethod
    def generate_nonce_str():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def generate_signature(self, nonce_str, timestamp_str, url) -> str:
        """
        签名算法
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        """
        ret = {
            'jsapi_ticket': self.get_jsapi_ticket(),
            'nonceStr': nonce_str,
            'timestamp': timestamp_str,
            'url': url
        }
        if current_app.config.get('WECHAT_SHARE_DEBUG'):
            print("jsapi_ticket:", ret['jsapi_ticket'])

        param_str = '&'.join([f"{key.lower()}={ret[key]}" for key in sorted(ret)])
        return hashlib.sha1(param_str.encode('utf-8')).hexdigest()

    def get_jsapi_ticket(self):
        if self.JSAPI_TICKET_CACHE['expires_at'] > timestamp():
            return self.JSAPI_TICKET_CACHE['ticket']

        try:
            resp = requests.get(
                self.JSAPI_TICKET_URL.format(access_token=self.get_access_token())
            )
            resp.raise_for_status()
            data = resp.json()
            if 'ticket' in data:
                self.JSAPI_TICKET_CACHE['ticket'] = data['ticket']
                self.JSAPI_TICKET_CACHE['expires_at'] = token_lifetime(data['expires_in'])
                return self.JSAPI_TICKET_CACHE['ticket']
            else:
                current_app.logger.error(f"Failed to get JSAPI ticket: {data}")
                return None
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching JSAPI ticket: {e}")
            return None

    def get_access_token(self):
        if self.ACCESS_TOKEN_CACHE['expires_at'] > timestamp():
            return self.ACCESS_TOKEN_CACHE['token']
        try:
            resp = requests.get(
                self.ACCESS_TOKEN_URL.format(
                    appid=current_app.config.get('WECHAT_APP_ID'),
                    secret=current_app.config.get('WECHAT_APP_SECRET')
                )
            )
            resp.raise_for_status()
            data = resp.json()
            if 'access_token' in data:
                self.ACCESS_TOKEN_CACHE['token'] = data['access_token']
                self.ACCESS_TOKEN_CACHE['expires_at'] = token_lifetime(data['expires_in'])
                return self.ACCESS_TOKEN_CACHE['token']
            else:
                current_app.logger.error(f"Failed to get access token: {data}")
                return ''
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching access token: {e}")
            return ''

    def wechat_share(self, title='', img='', desc='', link='', js_api_list=[]):
        timestamp_str = str(timestamp())
        nonce_str = self.generate_nonce_str()
        signature_str = self.generate_signature(nonce_str, timestamp_str, link or request.url)
        return Markup(
            self.render_template(
                '__wechat_share__.html',
                debug=current_app.config.get('WECHAT_SHARE_DEBUG'),
                appid=current_app.config.get('WECHAT_APP_ID'),
                timestamp=timestamp_str,
                nonce_str=nonce_str,
                signature=signature_str,
                js_api_list=js_api_list if len(js_api_list) > 0 else current_app.config.get('WECHAT_SHARE_JS_API_LIST'),
                title=title,
                desc=desc,
                link=link,
                img=img
            )
        )

    def wechat_share_ajax(self, title='', img='', desc='', link='', js_api_list=[]):
        return Markup(
            self.render_template(
                '__wechat_share_ajax__.html',
                debug=current_app.config.get('WECHAT_SHARE_DEBUG'),
                ajax_url=url_for(current_app.config["WECHAT_SHARE_ENDPOINT"], url=link or request.url),
                js_api_list=js_api_list if js_api_list else current_app.config.get('WECHAT_SHARE_JS_API_LIST'),
                title=title,
                desc=desc,
                link=link,
                img=img
            )
        )

    def render_template(self, template_name, **context):
        return self.jinja2_env.get_template(template_name).render(**context)
