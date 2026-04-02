"""
Vercel Serverless Function - HTML sahifalarni xizmat qilish
"""
import os
from http.server import BaseHTTPRequestHandler

BACKEND_URL = os.environ.get("BACKEND_URL", "https://your-backend.railway.app")

PAGES = {
    "/": "index",
    "/game": "lobby",
    "/game/aviator": "aviator",
    "/game/apple": "apple",
    "/game/mines": "mines",
    "/game/history": "history",
    "/game/profile": "profile",
    "/admin": "admin",
}

def get_template(name: str) -> str:
    """HTML shablonni o'qish"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if name == "admin":
        path = os.path.join(base_dir, "public", "admin.html")
    else:
        path = os.path.join(base_dir, "public", f"{name}.html")
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Backend URL ni dinamik almashtirish
    content = content.replace("__BACKEND_URL__", BACKEND_URL)
    return content


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        page_name = PAGES.get(path, "index")
        
        try:
            html = get_template(page_name)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
