#!/usr/bin/env python3
"""Gera public/sitemap.xml e dist/sitemap.xml com <lastmod> REAL por página.

lastmod = data do último commit git que tocou o arquivo-fonte da página
(ou o mtime do arquivo, se git não souber). Estável entre builds — só muda
quando o conteúdo daquela página muda. Isso torna o lastmod um sinal
confiável para o Google priorizar o rastreamento.

Uso: python scripts/gen_sitemap.py   (rodar a partir da raiz do projeto Astro)
"""
import os
import subprocess
import datetime
import pathlib

BASE = "https://vidracariabh.emp.br"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def source_for(url_path: str) -> pathlib.Path | None:
    """Mapeia a URL para o arquivo-fonte que a gera."""
    if url_path == "/":
        return ROOT / "src/pages/index.astro"
    if url_path == "/blog/":
        return ROOT / "src/pages/blog/index.astro"
    if url_path.startswith("/blog/"):
        slug = url_path.strip("/").split("/", 1)[1]
        for ext in (".md", ".mdx"):
            p = ROOT / "src/content/blog" / (slug + ext)
            if p.exists():
                return p
        return ROOT / "src/pages/blog/[...slug].astro"
    p = ROOT / "src/pages" / (url_path.strip("/") + ".astro")
    return p if p.exists() else None


def last_commit_date(path: pathlib.Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        d = out.stdout.strip()
        return d or None
    except Exception:
        return None


def lastmod_for(url_path: str) -> str:
    src = source_for(url_path)
    if src and src.exists():
        d = last_commit_date(src)
        if d:
            return d
        return datetime.date.fromtimestamp(src.stat().st_mtime).isoformat()
    return datetime.date.today().isoformat()


def priority_for(url_path: str) -> str:
    if url_path == "/":
        return "1.0"
    if url_path == "/blog/":
        return "0.6"
    if url_path.startswith("/blog/"):
        return "0.6"
    return "0.8"


def changefreq_for(url_path: str) -> str:
    if url_path in ("/", "/blog/"):
        return "weekly"
    if url_path.startswith("/blog/"):
        return "yearly"
    return "monthly"


def main() -> None:
    urls: list[str] = []
    for root, _dirs, files in os.walk(DIST):
        if "index.html" in files:
            rel = os.path.relpath(root, DIST)
            u = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
            if "/404" in u:
                continue
            urls.append(u)
    urls.sort(key=lambda u: (u != "/", u))

    entries = "\n".join(
        "  <url>\n"
        f"    <loc>{BASE}{u}</loc>\n"
        f"    <lastmod>{lastmod_for(u)}</lastmod>\n"
        f"    <changefreq>{changefreq_for(u)}</changefreq>\n"
        f"    <priority>{priority_for(u)}</priority>\n"
        "  </url>"
        for u in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    (ROOT / "public/sitemap.xml").write_text(xml, encoding="utf-8")
    (DIST / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml — {len(urls)} URLs")
    for u in urls:
        print(f"  {lastmod_for(u)}  {u}")


if __name__ == "__main__":
    main()
