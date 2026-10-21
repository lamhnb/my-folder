"""Volatile localhost byte-range bridge for ffmpeg public media transport.

No access-control bypass: forwards only an already public, non-DRM HTTPS URL.
No disk cache, auth, cookies, background daemon, or URL logging. Bound to loopback.
"""
import contextlib,http.server,threading,urllib.request,urllib.parse,urllib.error

class Bridge:
    def __init__(self,url):self.remote=url;self.errors=[];self.bytes_sent=0
    def __enter__(self):
        owner=self
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_HEAD(self):self.serve(False)
            def do_GET(self):self.serve(True)
            def serve(self,body):
                headers={'User-Agent':'Mozilla/5.0'}
                if self.headers.get('Range'):headers['Range']=self.headers['Range']
                req=urllib.request.Request(owner.remote,headers=headers,method='GET')
                try:
                    with urllib.request.urlopen(req,timeout=20) as response:
                        self.send_response(response.status)
                        for k in ['Content-Type','Content-Length','Content-Range','Accept-Ranges']:
                            if response.headers.get(k):self.send_header(k,response.headers[k])
                        self.end_headers()
                        if body:
                            while True:
                                b=response.read(256*1024)
                                if not b:break
                                self.wfile.write(b);owner.bytes_sent+=len(b)
                except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
                except Exception as e:
                    owner.errors.append(type(e).__name__)
                    with contextlib.suppress(Exception):self.send_error(502,'Public upstream transport failed')
        self.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        self.server.daemon_threads=True
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.url=f'http://127.0.0.1:{self.server.server_port}/video'
        return self
    def __exit__(self,*args):self.server.shutdown();self.server.server_close()
