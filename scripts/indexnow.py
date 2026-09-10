#!/usr/bin/env python3
"""Notifica IndexNow (Bing, Yandex, Seznam, Naver) sobre todas as URLs do sitemap.

Pré-requisito: o site já publicado, com a key acessível em
https://vidracariabh.emp.br/<KEY>.txt  (arquivo em public/, deployado).

O Google NÃO usa IndexNow — para o Google, use o Search Console
(enviar sitemap + "Inspecionar URL" > "Solicitar indexação").

Uso: python scripts/indexnow.py
"""
import json
import pathlib
import urllib.request

HOST = "vidracariabh.emp.br"
BASE = f"https://{HOST}"
ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = (ROOT / ".indexnow-key").read_text(encoding="utf-8").strip()

sitemap = (ROOT / "public/sitemap.xml").read_text(encoding="utf-8")
import re
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"{BASE}/{KEY}.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode(),
    method="POST",
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: HTTP {r.status} — {len(urls)} URLs enviadas")
except urllib.error.HTTPError as e:
    print(f"IndexNow: HTTP {e.code} — {e.read().decode()[:300]}")
