"""Génère index.html (web app installable) à partir de app.html."""
import pathlib
here = pathlib.Path(__file__).parent
body = (here / "app.html").read_text(encoding="utf-8")
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
