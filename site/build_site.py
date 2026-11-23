#!/usr/bin/env python3
"""สร้างเว็บใน docs/ จากแอปรายบทใน site/src/ และค่าแบรนด์ใน site/brand.json

ใช้: python3 site/build_site.py
เปลี่ยนโลโก้: แทนไฟล์ docs/brand/logo.png (ไม่ต้องรันใหม่)
เปลี่ยนชื่อแบรนด์หรือรหัส: แก้ site/brand.json แล้วรันใหม่
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE, DOCS = ROOT / "site", ROOT / "docs"
B = json.loads((SITE / "brand.json").read_text(encoding="utf-8"))

SRC_LOGO = '<img src="logo.png" alt="Dr VIT">'
SRC_ORG = '<span class="org">Siam edu.</span>'
SRC_SERIES = "Dr VIT · Siam edu."

NAV_CSS = ("<style>.atx-nav{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.9rem;margin:0 0 4px}"
           ".atx-nav a{color:var(--accent,#0d6466);font-weight:700;text-decoration:none}"
           ".atx-nav a:hover{text-decoration:underline}"
           "main>*{min-width:0}.tbl,table{max-width:100%}</style>")


def title_of(s):
    m = re.search(r"<h1>([^<]+)", s)
    t = html.unescape(m.group(1)).strip() if m else ""
    return re.sub(r"^แอปบทที่\s*\d+\s*", "", t)


def build():
    pages = sorted((SITE / "src").glob("ch*.html"))
    nums = [int(p.stem[2:]) for p in pages]
    chapters, errors = [], []
    for i, p in enumerate(pages):
        n = nums[i]
        s = p.read_text(encoding="utf-8")
        for needle, want in ((SRC_LOGO, 1), (SRC_ORG, 1), ("</head>", 1), ("<main>", 1)):
            if s.count(needle) != want:
                errors.append(f"{p.name}: '{needle}' พบ {s.count(needle)} ครั้ง")
        s = s.replace(SRC_LOGO, f'<img src="{B["logo"]}" alt="{B["logo_alt"]}" data-atx-logo>')
        s = s.replace(SRC_ORG, f'<span class="org">{B["org"]}</span>')
        s = s.replace(SRC_SERIES, B["series"])
        s = s.replace("</head>", f'{NAV_CSS}\n<script src="gate.js"></script>\n</head>', 1)
        links = ['<a href="./">สารบัญแอปประจำเล่ม</a>']
        if i > 0:
            links.append(f'<a href="ch{nums[i-1]:02d}.html">บทที่ {nums[i-1]}</a>')
        if i < len(pages) - 1:
            links.append(f'<a href="ch{nums[i+1]:02d}.html">บทที่ {nums[i+1]}</a>')
        s = s.replace("<main>", '<main>\n<nav class="atx-nav" aria-label="นำทาง">' + " · ".join(links) + "</nav>", 1)
        (DOCS / f"ch{n:02d}.html").write_text(s, encoding="utf-8")
        chapters.append((n, title_of(s)))
    if errors:
        print("\n".join(errors)); sys.exit(1)

    gate = (SITE / "gate.template.js").read_text(encoding="utf-8")
    gate = gate.replace("__GATE_HASH__", B["gate_hash"]).replace("__BOOK__", B["book"]).replace("__ORG__", B["org"])
    (DOCS / "gate.js").write_text(gate, encoding="utf-8")

    rows = "\n".join(
        f'<li><a href="ch{n:02d}.html"><span class="no">บทที่ {n}</span><span class="t">{html.escape(t)}</span></a></li>'
        for n, t in chapters)
    idx = (SITE / "index.template.html").read_text(encoding="utf-8")
    idx = (idx.replace("__ROWS__", rows).replace("__LOGO__", B["logo"]).replace("__ALT__", B["logo_alt"])
              .replace("__ORG__", B["org"]).replace("__SERIES__", B["series"]).replace("__BOOK__", B["book"])
              .replace("__AUTHOR__", B["author"]))
    (DOCS / "index.html").write_text(idx, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    try:
        import qrcode
        (DOCS / "qr").mkdir(exist_ok=True)
        for n, _ in chapters:
            qrcode.make(f'{B["site_url"]}ch{n:02d}.html', border=1).save(DOCS / "qr" / f"ch{n:02d}.png")
        qrcode.make(B["site_url"], border=1).save(DOCS / "qr" / "index.png")
    except ImportError:
        print("ข้าม QR: ยังไม่ได้ติดตั้ง qrcode")
    print("สร้างแล้ว", len(chapters), "บท:", ", ".join(str(n) for n, _ in chapters))


if __name__ == "__main__":
    build()
