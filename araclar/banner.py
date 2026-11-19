"""Profil başlığını (animasyonlu pixel SVG) üretir.

Sahne: gece pazarı. Kara kedi sinsice gelir, kasanın üstündeki balığı kapar, kaçar.
Çalıştır:  python3 araclar/banner.py   →  assets/banner-en.svg, assets/banner-tr.svg
"""
from html import escape
from pathlib import Path

W, H = 1000, 280
P = 6          # bir pixel kaç piksel
ZEMIN = 232    # sokak çizgisi (y)
SURE = 12      # animasyon döngüsü (sn)

# ---- Sprite'lar (harf = renk) ----
KEDI = [
    "..........L...L.",
    "..........KL.LK.",
    "..........LLLLL.",
    "..........KOKOKK",
    "L.........KKKKK.",
    ".L..LLLLLLLKKK..",
    ".KKKKKKKKKKKKK..",
    "..KKKKKKKKKKKK..",
]
BACAK_A = "...K.K....K.K..."
BACAK_B = "....K.K..K.K...."
BALIK = [
    ".FFFF.F",
    "FEFFFFF",
    ".FFFF.F",
]
AY = [
    "..MMMM..",
    ".MMMMMM.",
    "MMMMMMMM",
    "MMMMMMMM",
    "MMMMMMMM",
    "MMMMMMMM",
    ".MMMMMM.",
    "..MMMM..",
]
RENK = {
    "K": "#0d0d14", "L": "#4b4f80", "O": "#ff9a1f", "F": "#8fd3f0", "E": "#1b2238", "M": "#f6edc8",
}

METIN = {
    "en": ("MUHAMMED YAŞAR ÖZKUL", "software developer · I build games & web apps"),
    "tr": ("MUHAMMED YAŞAR ÖZKUL", "yazılım geliştirici · oyunlar ve web uygulamaları"),
}


def sprite(rows, x0=0, y0=0, renk=RENK, p=P):
    out = []
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != ".":
                out.append(f'<rect x="{x0 + x * p}" y="{y0 + y * p}" width="{p}" height="{p}" fill="{renk[c]}"/>')
    return "".join(out)


def yildizlar():
    # sabit tohumla (tekrarlanabilir) dağıtılmış yıldızlar
    out, s = [], 7
    for i in range(46):
        s = (s * 1103515245 + 12345) % 2**31
        x = s % W
        s = (s * 1103515245 + 12345) % 2**31
        y = 8 + s % 120
        if 20 < x < 640 and 40 < y < 130:   # yazının arkasını boş bırak
            continue
        boy = 2 if i % 5 else 4
        gecikme = (i * 0.37) % 3
        out.append(f'<rect class="yildiz" x="{x}" y="{y}" width="{boy}" height="{boy}" '
                   f'fill="#fff6d8" style="animation-delay:{gecikme:.2f}s"/>')
    return "".join(out)


def tezgah():
    x0, ust = 700, 150
    out = []
    # direkler
    out.append(f'<rect x="{x0}" y="{ust}" width="6" height="{ZEMIN - ust}" fill="#5a3a22"/>')
    out.append(f'<rect x="{x0 + 204}" y="{ust}" width="6" height="{ZEMIN - ust}" fill="#5a3a22"/>')
    # çizgili tente
    for i in range(18):
        renk = "#d94f4f" if i % 2 == 0 else "#f2e6d0"
        out.append(f'<rect x="{x0 - 12 + i * 13}" y="{ust - 30}" width="13" height="24" fill="{renk}"/>')
        out.append(f'<rect x="{x0 - 12 + i * 13}" y="{ust - 6}" width="13" height="6" fill="{renk}" '
                   f'rx="0" opacity="{1 if i % 2 == 0 else .85}"/>')
    # fener (parlıyor)
    out.append(f'<circle class="isik" cx="{x0 + 105}" cy="{ust + 14}" r="34" fill="#ffcc66" opacity=".18"/>')
    out.append(f'<rect x="{x0 + 102}" y="{ust}" width="6" height="6" fill="#3a2a1a"/>')
    out.append(f'<rect x="{x0 + 98}" y="{ust + 6}" width="14" height="16" fill="#ffcc66"/>')
    # tezgâh masası ve üstündeki balıklar (dekor)
    out.append(f'<rect x="{x0 + 6}" y="{ZEMIN - 52}" width="198" height="10" fill="#8a5a34"/>')
    out.append(f'<rect x="{x0 + 6}" y="{ZEMIN - 42}" width="198" height="42" fill="#6b4428"/>')
    for i in range(4):
        out.append(sprite(BALIK, x0 + 30 + i * 42, ZEMIN - 52 - 3 * 4, p=4))
    return "".join(out)


def kasa():
    # tezgâhın önündeki alçak kasa + çalınacak balık
    x0, ust = 640, ZEMIN - 30
    out = [f'<rect x="{x0}" y="{ust}" width="48" height="30" fill="#9b6a3c"/>',
           f'<rect x="{x0}" y="{ust + 9}" width="48" height="3" fill="#7a5230"/>',
           f'<rect x="{x0}" y="{ust + 20}" width="48" height="3" fill="#7a5230"/>',
           f'<g class="kasa-balik">{sprite(BALIK, x0 + 3, ust - 18)}</g>']
    return "".join(out)


def kedi():
    govde = sprite(KEDI)
    a = sprite([BACAK_A], 0, len(KEDI) * P)
    b = sprite([BACAK_B], 0, len(KEDI) * P)
    agiz_balik = sprite(BALIK, 15 * P - 6, 4 * P - 4)
    unlem = (f'<g class="unlem"><rect x="{12 * P}" y="-34" width="6" height="16" fill="#ffd34d"/>'
             f'<rect x="{12 * P}" y="-14" width="6" height="6" fill="#ffd34d"/></g>')
    kedi_y = ZEMIN - (len(KEDI) + 1) * P
    return (f'<g transform="translate(0 {kedi_y})"><g class="kedi">'
            f'{govde}<g class="bacak-a">{a}</g><g class="bacak-b">{b}</g>'
            f'<g class="agiz-balik">{agiz_balik}</g>{unlem}</g></g>')


def css():
    # kedi 0–38%: sinsice gelir · 38–48%: kasada durur, balığı kapar · 48–78%: koşarak kaçar
    return f"""
.yildiz{{animation:parla 3s ease-in-out infinite}}
@keyframes parla{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.isik{{animation:fener 2.4s ease-in-out infinite}}
@keyframes fener{{0%,100%{{opacity:.12}}50%{{opacity:.24}}}}
.kedi{{animation:yuru {SURE}s linear infinite}}
@keyframes yuru{{
 0%{{transform:translateX(-130px)}}
 38%{{transform:translateX(552px)}}
 48%{{transform:translateX(552px)}}
 78%{{transform:translateX(1060px);animation-timing-function:step-end}}
 100%{{transform:translateX(-130px)}}}}
.bacak-a{{animation:adimA .36s steps(1) infinite}}
.bacak-b{{animation:adimB .36s steps(1) infinite}}
@keyframes adimA{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes adimB{{0%{{opacity:0}}50%{{opacity:1}}}}
.agiz-balik{{animation:agiz {SURE}s steps(1) infinite}}
@keyframes agiz{{0%{{opacity:0}}44%{{opacity:1}}80%{{opacity:0}}}}
.kasa-balik{{animation:kasa {SURE}s steps(1) infinite}}
@keyframes kasa{{0%{{opacity:1}}44%{{opacity:0}}92%{{opacity:1}}}}
.unlem{{animation:unlem {SURE}s steps(1) infinite}}
@keyframes unlem{{0%{{opacity:0}}44%{{opacity:1}}56%{{opacity:0}}}}
.imlec{{animation:imlec 1s steps(1) infinite}}
@keyframes imlec{{0%{{opacity:1}}50%{{opacity:0}}}}
"""


def banner(dil):
    baslik, alt = METIN[dil]
    yazi = "font-family:ui-monospace,'SFMono-Regular',Menlo,Consolas,'Courier New',monospace"
    alt_genislik = len(alt) * 9.6
    baslik, alt = escape(baslik), escape(alt)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges" role="img" aria-label="{baslik} — {alt}">
<title>{baslik} — {alt}</title>
<style>{css()}</style>
<defs><linearGradient id="gok" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#11142b"/><stop offset="1" stop-color="#2b2350"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#gok)"/>
{yildizlar()}
{sprite(AY, 900, 30)}
<text x="40" y="92" style="{yazi};font-weight:800;font-size:38px;letter-spacing:2px" fill="#f6edc8">{baslik}</text>
<text x="42" y="128" style="{yazi};font-size:16px" fill="#ff9a1f">{alt}</text>
<rect class="imlec" x="{42 + alt_genislik + 4}" y="115" width="9" height="16" fill="#ff9a1f"/>
{tezgah()}
<rect x="0" y="{ZEMIN}" width="{W}" height="{H - ZEMIN}" fill="#24243a"/>
<rect x="0" y="{ZEMIN}" width="{W}" height="4" fill="#3a3a58"/>
{''.join(f'<rect x="{x}" y="{ZEMIN + 22}" width="30" height="4" fill="#30304b"/>' for x in range(20, W, 70))}
{kasa()}
{kedi()}
</svg>
"""


if __name__ == "__main__":
    kok = Path(__file__).resolve().parent.parent / "assets"
    kok.mkdir(exist_ok=True)
    for dil in METIN:
        (kok / f"banner-{dil}.svg").write_text(banner(dil), encoding="utf-8")
        print("yazıldı:", kok / f"banner-{dil}.svg")
