from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import time
import json
from requests.packages import urllib3
from urllib.parse import parse_qs
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TokenParser():
    def __init__(self):
        ###############################################MAGIC ARRAY###############################################
        self.data_segment_data_0 = [
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x07, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x06, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x04, 
                                    ]
        
    def rdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):

        w2c_i0 = w2c_p1
        w2c_i1 = 100
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_p0 = w2c_i1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_p2 = w2c_i0
        w2c_i1 = w2c_p2
        w2c_i2 = w2c_p1
        w2c_i3 = w2c_p0
        w2c_i4 = 10
        w2c_i3 *= w2c_i4
        w2c_i2 -= w2c_i3
        w2c_i1 += w2c_i2
        w2c_i2 = 2
        w2c_i1 <<= (w2c_i2 & 31)

        w2c_i1 = self.data_segment_data_0[w2c_i1]
        w2c_i0 += w2c_i1
        w2c_i1 = 22
        w2c_i0 += w2c_i1
        return w2c_i0


    def cdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):
        w2c_i0 = w2c_p1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_p0 = w2c_i0
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = w2c_p0
        w2c_i3 = 10
        w2c_i2 *= w2c_i3
        w2c_i1 -= w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 100
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = 2
        w2c_i0 <<= (w2c_i1 & 31)

        w2c_i0 = self.data_segment_data_0[w2c_i0]
        w2c_i1 = 22
        w2c_i0 += w2c_i1

        return w2c_i0

    def parse_token_response(self, token_response):
        n = self.cdx(token_response['salt1'], token_response['salt2'], token_response['salt3'], token_response['salt4'], token_response['salt5']);
        l = self.rdx(token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']);
        
        i = self.cdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt5'], token_response['salt4']);
        r = self.rdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt4'], token_response['salt5']);

        access_token  = token_response['accessToken']
        refresh_token = token_response['refreshToken']
        
        parsed_access_token  = access_token[0:n] + access_token[n + 1: l] + access_token[l + 1:]
        parsed_refresh_token = refresh_token[0:i] + refresh_token[i + 1: r] + refresh_token[r + 1:]
    
        #returns both access_token and refresh_token
        #Right now new access_token can be used for every new api request
        return (parsed_access_token, parsed_refresh_token)

class Nepse:
    def __init__(self):
        self.token_parser     = TokenParser()
        
        self.token_url            = "https://nepalstock.com/api/authenticate/prove"
                
        self.headers= {
                            'Host': 'nepalstock.com',
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                            'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/json',
                            'Referer': 'https://nepalstock.com/',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'TE': 'Trailers',
                        }
    ###############################################PRIVATE METHODS###############################################
    
    def requestAPI(self, url, access_token=None,post_body=None):
        if access_token is not None:
            headers = {'Authorization': f'Salter {access_token}', **self.headers}
        else:
            headers = self.headers
        if post_body:
            r=requests.post(url, headers=headers, data=post_body, verify=False)
            return (r.text,r.status_code)
        else:
            r=requests.get(url, headers=headers, verify=False)
            try:
                return (r.json(),r.status_code)
            except:
                try:
                    return (r.text,r.status_code)
                except:
                    return({"error": "invalid"}, 403)
        
    def getValidToken(self):
        token_response = self.requestAPI(url=self.token_url)[0]
        
        for salt_index in range(1, 6):
            token_response[f'salt{salt_index}'] = int(token_response[f'salt{salt_index}'])
        
        #returns access_token only, refresh token is not used right now
        return self.token_parser.parse_token_response(token_response)[0]
    
    ###############################################PUBLIC METHODS###############################################
        
    def get(self,url):
        access_token = self.getValidToken()
        return self.requestAPI(url=url, access_token=access_token)

    def post(self,url,post_body):
        access_token = self.getValidToken()
        return self.requestAPI(url=url, access_token=access_token,post_body=post_body)

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if(self.path)=='/info':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('info.html', 'rb') as file: 
                self.wfile.write(file.read())            
            return
        nepse = Nepse()    
        url='https://nepalstock.com/api/nots'+str(self.path)
        res=nepse.get(url)
        self.write_response(res)
        

    def do_POST(self):
        try:
            nepse = Nepse()
            url='https://nepalstock.com/api/nots'+str(self.path)
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len).decode("utf-8")
            if(post_body.strip()==''):
                post_body='{}'
            if not '{' in  post_body:
                post_body=dict(parse_qs(post_body))
                post_body={k: v[0] for k, v in post_body.items()}
            print(post_body)
            res=nepse.post(url,post_body)
            self.write_response(res)
        except Exception as e:
            print(e)
            self.send_error(500)


    def write_response(self, content):
        self.send_response(content[1])
        # self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(content[0]).encode('utf-8'))
        # try:
            # if not self.wfile.closed:
                # self.wfile.flush()
                # self.wfile.close()
        # except:
            # pass
        self.rfile.close()
             

port = int(os.environ.get("PORT", 5000))
def run(server_class=HTTPServer, handler_class=S, addr="0.0.0.0", port=port):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()
run()
