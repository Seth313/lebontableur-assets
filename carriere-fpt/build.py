"""Génère index.html (web app installable) à partir de app.html."""
import pathlib
here = pathlib.Path(__file__).parent
import json, sys
body = (here / "app.html").read_text(encoding="utf-8")
ref = json.dumps(json.loads((here / "data" / "grilles.json").read_text(encoding="utf-8")), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
body = body.replace("<script>", '<script type="application/json" id="ref-grilles">' + ref + "</script>\n<script>", 1)
if len(sys.argv) > 1:  # copie pour publication claude.ai
    pathlib.Path(sys.argv[1]).write_text(body, encoding="utf-8")
head = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Carrière">
<meta name="theme-color" content="#f2f3f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0e16" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-512.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
tail = """
<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js").catch(function(){})}</script>
</body>
</html>
"""
(here / "index.html").write_text(head + body + tail, encoding="utf-8")
print("index.html généré")

# Version autonome pour ordinateur : un seul fichier, sans manifeste ni service worker.
import base64
icon = base64.b64encode((here / "icon-180.png").read_bytes()).decode()
solo = (head
        .replace('<link rel="manifest" href="manifest.webmanifest">\n', "")
        .replace('href="icon-180.png"', f'href="data:image/png;base64,{icon}"')
        .replace('<link rel="icon" href="icon-512.png">', f'<link rel="icon" type="image/png" href="data:image/png;base64,{icon}">'))
(here / "Carriere-Territoriale.html").write_text(solo + body + "\n</body>\n</html>\n", encoding="utf-8")
print("Carriere-Territoriale.html généré")
