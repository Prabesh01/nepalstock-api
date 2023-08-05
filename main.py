from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from requests.packages import urllib3
from urllib.parse import parse_qs
import os
import json

import pywasm

import datetime
import pytz
tz_NP = pytz.timezone('Asia/Kathmandu')
payld_id=0
payld_d=0

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TokenParser():
    def __init__(self):
        self.runtime = pywasm.load('css.wasm')

    def parse_token_response(self, token_response):
        n = self.runtime.exec('cdx', [token_response['salt1'], token_response['salt2'], token_response['salt3'], token_response['salt4'], token_response['salt5']]);
        l = self.runtime.exec('rdx', [token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);
        o = self.runtime.exec('bdx', [token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);
        p = self.runtime.exec('ndx', [token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);
        q = self.runtime.exec('mdx', [token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);


        a = self.runtime.exec('cdx', [token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt5'], token_response['salt4']]);
        b = self.runtime.exec('rdx', [token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt4'], token_response['salt5']]);
        c = self.runtime.exec('bdx', [token_response['salt2'], token_response['salt1'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);
        d = self.runtime.exec('ndx', [token_response['salt2'], token_response['salt1'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);
        e = self.runtime.exec('mdx', [token_response['salt2'], token_response['salt1'], token_response['salt4'], token_response['salt3'], token_response['salt5']]);


        access_token  = token_response['accessToken']
        refresh_token = token_response['refreshToken']
        
        parsed_access_token  = access_token[0:n] + access_token[n + 1: l] + access_token[l + 1: o] + access_token[o + 1: p] + access_token[p + 1:q] + access_token[q + 1:]
        parsed_refresh_token = refresh_token[0:a] + refresh_token[a + 1: b] + refresh_token[b + 1: c] + refresh_token[c + 1: d] + refresh_token[d + 1: e ] + refresh_token[e + 1: ]
    
        return (parsed_access_token, parsed_refresh_token)

class Nepse:
    def __init__(self):        
        self.token_parser     = TokenParser()
        self.base_url             = "https://www.nepalstock.com.np"
        
        self.token_url            = f"{self.base_url}/api/authenticate/prove"
        self.refresh_url          = f"{self.base_url}/api/authenticate/refresh-token"

        self.post_payload_id      = None

        self.api_end_point_access_token = (False, False)
        
        self.headers= {
                            'Host': self.base_url.replace('https://', ''),
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                            'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Referer': f'{self.base_url}',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'TE': 'Trailers',
                        }
    ###############################################PRIVATE METHODS###############################################
    
    def requestAPI(self, url,no=None):
        
        headers = self.headers
        if not no: # this is done so that get request to api/authenticate doesnt fail, since it doesnt require authorization headers
            access_token, request_token = self.getToken()
            headers = {'Authorization': f'Salter {access_token}', **self.headers}
        
        response = requests.get(url, headers=headers, verify=False)
        # if (response.status_code != 200):
            # self.refreshToken()
            # return self.requestAPI(url) 
        
        return (response.text,response.status_code)
    
    def requestPOSTAPI(self, url,post_data=None):
        
        access_token, request_token = self.getToken()
        
        headers = {'Content-Type':'application/json', 'Authorization': f'Salter {access_token}', **self.headers, }
        if post_data:
            response = requests.post(url, headers=headers, data=json.dumps(post_data), verify=False)        
        else:
            #response = requests.post(url, headers=headers, data=json.dumps({"id": self.getPOSTPayloadIDForNepseIndex() if '/graph/index/' in url else self.getPOSTPayloadID()}))
            response = requests.post(url, headers=headers, data=json.dumps({"id": self.getPOSTPayloadIDForNepseIndex() if '/graph/index/' in url else (self.getPOSTPayloadIDForFloorSheet() if '/nepse-data/floorsheet' or ' /nepse-data/today-price' in url else self.getPOSTPayloadID())}), verify=False)
        # if (response.status_code != 200):
            # self.refreshToken()
            # return self.requestPOSTAPI(url)
        return (response.text,response.status_code)
    
    #token is not unique for each url, when token is requested,
    def getToken(self):
        if self.api_end_point_access_token == (False, False):
            token_response = self.getValidToken()
            self.api_end_point_access_token = token_response
            
        
        return self.api_end_point_access_token
    
    def refreshToken(self):
        access_token, refresh_token = self.api_end_point_access_token
        if (access_token != False):# this is done to make first request to api/authenticate pass

            data=json.dumps({'refreshToken':refresh_token})

            headers= {**self.headers, 
                        "Content-Type": "application/json",
                        "Content-Length": str(len(data)),
                        "Authorization": f"Salter {access_token}"
                    }
            
            refresh_key = requests.post(self.refresh_url, 
                                        headers=headers, 
                                        data=data, verify=False)
            
            if refresh_key.status_code != 200:
                self.resetToken()
            else:
                self.api_end_point_access_token = self.getValidTokenFromJSON( refresh_key.json() )
        else:
            self.getToken()

        
    def resetToken(self):
        self.api_end_point_access_token = (False, False)
        
#         self.api_end_point_access_token[url] = False
    def getValidTokenFromJSON(self, token_response):
        self.salts = []
        for salt_index in range(1, 6):
            val = int(token_response[f'salt{salt_index}'])
            token_response[f'salt{salt_index}'] = val
            self.salts.append(val)
        
        #returns access_token only, refresh token is not used right now
        return self.token_parser.parse_token_response(token_response)
        
    def getValidToken(self):
        token_response = json.loads(self.requestAPI(url=self.token_url,no='no')[0])
        return self.getValidTokenFromJSON(token_response)
            
    ##################method to get post payload id#################################33
    def getDummyID(self):
        global payld_d, payld_id
        now = datetime.datetime.now(tz_NP)
        if payld_d== now.day:
            return payld_id
        payld_d = now.day
        payld_id=json.loads(self.requestAPI(url='https://www.nepalstock.com.np/api/nots/nepse-data/market-open')[0])['id']
        return payld_id
    
    def getDummyData(self):
        return [ 147, 117, 239, 143, 157, 312, 161, 612, 512, 804,
            411, 527, 170, 511, 421, 667, 764, 621, 301, 106, 133, 793,
            411, 511, 312, 423, 344, 346, 653, 758, 342, 222, 236, 811,
            711, 611, 122, 447, 128, 199, 183, 135, 489, 703, 800, 745,
            152, 863, 134, 211, 142, 564, 375, 793, 212, 153, 138, 153,
            648, 611, 151, 649, 318, 143, 117, 756, 119, 141, 717, 113,
            112, 146, 162, 660, 693, 261, 362, 354, 251, 641, 157, 178,
            631, 192, 734, 445, 192, 883, 187, 122, 591, 731, 852, 384,
            565, 596, 451, 772, 624, 691 ]
    
    def getPOSTPayloadIDForNepseIndex(self):
        dummy_id = self.getDummyID()
        now = datetime.datetime.now(tz_NP)
        e = self.getDummyData()[dummy_id] + dummy_id + 2*(now.day)
        n = e + self.salts[ 3 if e % 10 < 5 else 1] * now.day - self.salts[ (3 if e%10 < 5 else 1) - 1];
        self.post_payload_id = n 
        return self.post_payload_id

    def getPOSTPayloadIDForFloorSheet(self):
        dummy_id = self.getDummyID()
        now = datetime.datetime.now(tz_NP)
        e = self.getDummyData()[dummy_id] + dummy_id + 2*(now.day)
        n = e + self.salts[1  if e%10 < 4 else 3] * now.day - self.salts[(1 if e%10<4 else 3) - 1]
        self.post_payload_id = n 
        return self.post_payload_id    
    
    def getPOSTPayloadID(self):
        dummy_id = self.getDummyID()
        now = datetime.datetime.now(tz_NP)
        self.post_payload_id = self.getDummyData()[dummy_id] + dummy_id + 2*(now.day)
        return self.post_payload_id
    
class S(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if '.ico' in self.path: return
        if(self.path)=='/info':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('info.html', 'rb') as file: 
                self.wfile.write(file.read())            
            return
        nepse = Nepse()    
        url='https://nepalstock.com.np/api/nots'+str(self.path)
        res=nepse.requestAPI(url=url)
        self.write_response(res)
        

    def do_POST(self):
        try:
            nepse = Nepse()
            url='https://nepalstock.com.np/api/nots'+str(self.path)
            content_len = int(self.headers.get('Content-Length'))
            if content_len==0:
                res=nepse.requestPOSTAPI(url=url)
            else:
                post_body = self.rfile.read(content_len).decode("utf-8")
                if(post_body.strip()==''):
                    post_body='{}'
                if not '{' in  post_body:
                    post_body=dict(parse_qs(post_body))
                    post_body={k: v[0] for k, v in post_body.items()}
                print(post_body)
                res=nepse.requestPOSTAPI(url=url,post_data=json.loads(post_body))
            self.write_response(res)
        except Exception as e:
            print(e)
            self.send_error(500)

    def write_response(self, content):
        self.send_response(content[1])
        self.end_headers()
        self.wfile.write(str(content[0]).encode('utf-8'))
        self.rfile.close()
             

port = int(os.environ.get("PORT", 5000))
def run(server_class=HTTPServer, handler_class=S, addr="0.0.0.0", port=port):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting http server on http://localhost:{port}")
    httpd.serve_forever()
run()
