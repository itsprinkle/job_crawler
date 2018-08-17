#importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication

import base64
import random

http_proxy=[
"http://42.96.209.47:2333",
"http://139.129.18.6:2333",
"http://42.96.209.61:2333",
"http://42.96.209.195:2333",
"http://120.27.34.93:2333",
"http://42.96.204.242:2333",
"http://114.215.154.49:2333",
"http://42.96.209.68:2333",
"http://42.96.207.88:2333",
"http://115.28.50.171:2333",
"http://42.96.209.57:2333",
"http://121.42.196.105:2333",
"http://115.28.0.191:2333",
"http://120.27.31.204:2333",
"http://115.28.146.148:2333",
"http://114.215.115.5:2333",
"http://114.215.136.188:2333",
"http://42.96.209.249:2333",
"http://42.96.209.69:2333",
"http://120.27.31.64:2333",
"http://42.96.207.206:2333",
"http://42.96.208.146:2333",
"http://114.215.153.81:2333",
"http://115.28.168.84:2333",
"http://115.28.50.46:2333",
"http://115.29.136.99:2333",
"http://121.42.137.150:2333",
"http://114.215.118.94:2333",
"http://139.129.128.108:2333",
"http://42.96.207.63:2333",
"http://114.215.140.98:2333",
"http://42.96.207.82:2333",
"http://42.96.207.204:2333",
"http://121.42.148.109:2333",
"http://42.96.207.100:2333",
"http://121.201.58.120:2333",
"http://121.201.58.139:2333",
"http://121.42.147.178:2333",
"http://42.96.195.96:2333",
"http://42.96.207.67:2333",
]
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = http_proxy[random.randint(0, len(http_proxy)-1)]
        # Use the following lines if your proxy requires authentication
        #proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
