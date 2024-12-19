# zosnel/main.py

from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

class zosnel:
    def __init__(self, port=8000):
        self.title = "Zosnel Project"
        self.body_content = []
        self.styles = []
        self.port = port

    def set_title(self, title):
        self.title = title

    def para(self, text, class_name=None):
        if class_name:
            self.body_content.append(f'<p class="{class_name}">{text}</p>')
        else:
            self.body_content.append(f"<p>{text}</p>")

    def heading(self, text, level=1, class_name=None):
        if 1 <= level <= 6:
            if class_name:
                self.body_content.append(f'<h{level} class="{class_name}">{text}</h{level}>')
            else:
                self.body_content.append(f"<h{level}>{text}</h{level}>")
        else:
            print("ZOSNEL ERROR: Heading level must be between 1 and 6.")

    def url(self, text, url):
        self.body_content.append(f'<a href="{url}">{text}</a>')

    def img(self, src, alt="", class_name=None):
        if class_name:
            self.body_content.append(f'<img src="{src}" alt="{alt}" class="{class_name}">')
        else:
            self.body_content.append(f'<img src="{src}" alt="{alt}">')

    def breakline(self, class_name=None):
        self.body_content.append(f'<hr class="{class_name}">')

    def sep(self, class_name=None):
        self.body_content.append(f'<br class="{class_name}">')

    def link(self, href, rel="stylesheet"):
        self.body_content.append(f'<link rel="{rel}" href="{href}"')
        print("ZOSNEL WARNING: CSS IS LINKED BY DEFAULT, LINKING IT AGAIN COULD CAUSE ERRORS, IGNORE THIS IF YOU ARE NOT USING IT FOR LINKING")

    def link_css(self, href):
        self.body_content.append(f'<link rel="stylesheet" href="{href}">')

    def link_js(self, src):
        self.body_content.append(f'<script src="{src}"></script>')

    def pass_k():
        pass

    def custom(self, custom):
        self.body_content.append(f'{custom}')
        print("ZOSNEL: Be careful while using custom as it could not work or cause errors on your website, this function does not get support.")
        print("Element", custom)

    def add_css(self, css):
        self.styles.append(css)

    def generate_html(self):
        html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{self.title}</title>\n"
        html += "<style>\n" + self.generate_css() + "\n</style>\n"
        html += "</head>\n<body>\n"
        html += "\n".join(self.body_content)
        html += "\n</body>\n</html>"
        return html

    def generate_css(self):
        return "\n".join(self.styles)

    def javascript(self, javascript):
        self.body_content.append(f'<script>{javascript}</script>')

    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, html_content=None, **kwargs):
            self.html_content = html_content
            super().__init__(*args, **kwargs)

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.html_content.encode())

    def serve(self):
        handler = lambda *args, **kwargs: self.CustomHandler(*args, html_content=self.generate_html(), **kwargs)
        server = HTTPServer(('localhost', self.port), handler)
        print(f"Server started at http://localhost:{self.port}")
        
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server.shutdown()
