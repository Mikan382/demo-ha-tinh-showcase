#!/usr/bin/env python3
"""
Fix LuxeStay Ha Tinh menu:
1. Strip old broken menu CSS/JS blocks (where class prefix was repeated).
2. Replace repeated brand prefix in class/id attrs & style/script blocks only.
3. Inject fresh menu CSS + JS (with actual UTF-8 labels via chr()) into all HTML files.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LUXESTAY_DIR = ROOT / "luxestay-framer"

# ─── Repeated prefix pattern ────────────────────────────────────────────────
# Only matches when 'Ha Tinh' appears 2+ times consecutively (true corruption).
# Single 'LuxeStay Ha Tinh' = brand name -> leave alone.
OLD_PREFIX_PAT = re.compile(r'LuxeStay(?:\s+Ha\s+Tinh){2,}')
NEW_PREFIX = "lxs"


# ─── Build Vietnamese labels using chr() to avoid encoding issues ────────────
def _l(href, label):
    return {"href": href, "label": label}


_ch = chr   # alias

MENU_LABELS = [
    _l("index.html",      "Trang ch" + _ch(7911)),       # Trang chu
    _l("rooms.html",      "Ph" + _ch(242) + "ng"),        # Phong
    _l("restaurant.html", _ch(7848) + "m th" + _ch(7921) + "c"),  # Am thuc
    _l("wellness.html",   "Spa"),
    _l("wedding.html",    "Ti" + _ch(7879) + "c c" + _ch(432) + _ch(7901) + "i"),  # Tiec cuoi
    _l("contact-us.html", "Li" + _ch(234) + "n h" + _ch(7879)),   # Lien he
]

# Build JS menuItems array with actual UTF-8 strings
_items_js = "  const menuItems = [\n"
for item in MENU_LABELS:
    _items_js += '    {{ href: "{href}", label: "{label}" }},\n'.format(**item)
_items_js += "  ];\n"

# Kicker and foot strings
_kicker = "LuxeStay H" + _ch(224) + " T" + _ch(297) + "nh"  # LuxeStay Ha Tinh (with diacritics)
_book   = "Xem ph" + _ch(242) + "ng"                          # Xem phong
_close_lbl = _ch(272) + _ch(243) + "ng menu"                  # Dong menu
_foot1  = ("Khu ngh" + _ch(7881) + " d" + _ch(432) + _ch(7905)
           + "ng ven h" + _ch(7891) + " v" + _ch(224) + " bi" + _ch(7875) + "n")
_foot2  = "H" + _ch(224) + " T" + _ch(297) + "nh"

# ─── Menu CSS ────────────────────────────────────────────────────────────────
MENU_CSS = """\
<style id="lxs-demo-overrides">
:root{
  --lxs-intro-top:#2b5e60;
  --lxs-intro-bottom:#18383c;
}
body .framer-Dh4vv .framer-1vyj1i7{
  background:
    radial-gradient(circle at top center, rgba(255,255,255,.08), transparent 42%),
    linear-gradient(180deg, var(--lxs-intro-top) 0%, var(--lxs-intro-bottom) 100%) !important;
}
body .framer-Dh4vv .framer-1vyj1i7 .framer-1xiel0e p{
  max-width:580px;
}
body.lxs-menu-open{
  overflow:hidden;
}
#lxs-site-menu{
  position:fixed;
  inset:0;
  z-index:9999;
  display:flex;
  justify-content:flex-end;
  background:rgba(37,43,21,.18);
  opacity:0;
  pointer-events:none;
  transition:opacity .22s ease;
  backdrop-filter:blur(1.5px);
}
#lxs-site-menu.is-open{
  opacity:1;
  pointer-events:auto;
}
#lxs-site-menu .lxs-menu-panel{
  width:min(420px,100vw);
  min-height:100vh;
  background:#f1ebe3;
  display:flex;
  flex-direction:column;
  padding:32px 36px 48px;
  box-sizing:border-box;
  transform:translateX(100%);
  transition:transform .32s cubic-bezier(.4,0,.2,1);
  overflow-y:auto;
  justify-content:space-between;
  gap:24px;
}
#lxs-site-menu.is-open .lxs-menu-panel{
  transform:translateX(0);
}
#lxs-site-menu .lxs-menu-head{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:16px;
}
#lxs-site-menu .lxs-menu-brand{
  display:flex;
  flex-direction:column;
  gap:8px;
}
#lxs-site-menu .lxs-menu-kicker{
  font-family:Arial,sans-serif;
  font-size:11px;
  font-weight:700;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:#90320a;
}
#lxs-site-menu .lxs-menu-book{
  display:inline-block;
  font-family:Arial,sans-serif;
  font-size:13px;
  color:#332015;
  text-decoration:none;
  border:1px solid rgba(51,32,21,.3);
  border-radius:2px;
  padding:8px 16px;
  margin-top:4px;
  transition:background .18s,color .18s;
}
#lxs-site-menu .lxs-menu-book:hover{
  background:#332015;
  color:#f1ebe3;
}
#lxs-site-menu .lxs-menu-close{
  background:none;
  border:none;
  cursor:pointer;
  font-size:22px;
  color:#332015;
  padding:4px;
  line-height:1;
  flex-shrink:0;
}
#lxs-site-menu .lxs-menu-links{
  display:flex;
  flex-direction:column;
  gap:0;
  flex:1;
  margin-top:32px;
}
#lxs-site-menu .lxs-menu-link{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:18px 0;
  border-bottom:1px solid rgba(51,32,21,.12);
  text-decoration:none;
  color:#332015;
  font-family:Georgia,serif;
  font-size:22px;
  transition:color .18s;
}
#lxs-site-menu .lxs-menu-link:hover{
  color:#90320a;
}
#lxs-site-menu .lxs-menu-label{
  flex:1;
}
#lxs-site-menu .lxs-menu-arrow{
  font-size:18px;
  opacity:.45;
}
#lxs-site-menu .lxs-menu-foot{
  display:flex;
  flex-direction:column;
  gap:4px;
  font-family:Arial,sans-serif;
  font-size:12px;
  color:rgba(51,32,21,.55);
  letter-spacing:.06em;
  margin-top:32px;
}
@media(max-width:580px){
  #lxs-site-menu .lxs-menu-panel{padding:24px 24px 36px;}
  #lxs-site-menu .lxs-menu-link{font-size:18px;}
  #lxs-site-menu .lxs-menu-foot{font-size:11px;}
}
</style>"""

# ─── Menu JS template (no Vietnamese inline - all built at runtime) ───────────
MENU_JS_TEMPLATE = """\
<script id="lxs-demo-nav">
(()=>{{
  const MENU_ID = "lxs-site-menu";
{menu_items}
  const kicker  = {kicker_json};
  const bookTxt = {book_json};
  const closeLbl = {close_json};
  const foot1   = {foot1_json};
  const foot2   = {foot2_json};

  function ensureMenu(){{
    let menu = document.getElementById(MENU_ID);
    if(menu) return menu;
    menu = document.createElement("aside");
    menu.id = MENU_ID;
    menu.setAttribute("aria-hidden", "true");
    menu.innerHTML = [
      '<div class="lxs-menu-panel" role="dialog" aria-modal="true">',
        '<div class="lxs-menu-head">',
          '<div class="lxs-menu-brand">',
            '<div class="lxs-menu-kicker">' + kicker + '</div>',
            '<a class="lxs-menu-book" href="rooms.html">' + bookTxt + '</a>',
          '</div>',
          '<button class="lxs-menu-close" type="button" aria-label="' + closeLbl + '">&times;</button>',
        '</div>',
        '<nav class="lxs-menu-links"></nav>',
        '<div class="lxs-menu-foot">',
          '<span>' + foot1 + '</span>',
          '<span>' + foot2 + '</span>',
        '</div>',
      '</div>'
    ].join('');
    const links = menu.querySelector(".lxs-menu-links");
    menuItems.forEach((item)=>{{
      const a = document.createElement("a");
      a.className = "lxs-menu-link";
      a.href = item.href;
      a.innerHTML = '<span class="lxs-menu-label">' + item.label + '</span>'
                  + '<span class="lxs-menu-arrow">&rarr;</span>';
      links.appendChild(a);
    }});
    document.body.appendChild(menu);
    return menu;
  }}

  function init(){{
    const burger = document.querySelector('.framer-1ipfx6b-container [data-framer-name="Start"]');
    const cta    = document.querySelector('.framer-krc2jy-container a');
    if(!burger || !cta) return false;

    const menu    = ensureMenu();
    const panel   = menu.querySelector('.lxs-menu-panel');
    const closeBtn = menu.querySelector('.lxs-menu-close');

    cta.href   = 'rooms.html';
    cta.target = '';
    cta.rel    = '';

    if(!burger.dataset.lxsBound){{
      burger.dataset.lxsBound = '1';
      burger.setAttribute('role', 'button');
      burger.style.cursor = 'pointer';

      const openMenu  = ()=>{{ menu.classList.add('is-open');    menu.setAttribute('aria-hidden','false'); document.body.classList.add('lxs-menu-open'); }};
      const closeMenu = ()=>{{ menu.classList.remove('is-open'); menu.setAttribute('aria-hidden','true');  document.body.classList.remove('lxs-menu-open'); }};

      burger.addEventListener('click', openMenu);
      closeBtn.addEventListener('click', closeMenu);
      menu.addEventListener('click', (e)=>{{ if(e.target===menu) closeMenu(); }});
      panel.addEventListener('click', (e)=>e.stopPropagation());
      document.addEventListener('keydown', (e)=>{{ if(e.key==='Escape') closeMenu(); }});
      menu.querySelectorAll('a').forEach((l)=>l.addEventListener('click', closeMenu));
      if(window.location.search.includes('menu=open')) openMenu();
    }}
    return true;
  }}

  let attempts = 0;
  const timer = setInterval(()=>{{
    attempts++;
    if(init() || attempts > 40) clearInterval(timer);
  }}, 250);
}})();
</script>"""


def _js_str(s: str) -> str:
    """Return a JS string literal (double-quoted) with the text encoded as JS \\uXXXX escapes."""
    parts = ['"']
    for ch in s:
        cp = ord(ch)
        if cp > 127:
            parts.append(f"\\u{cp:04x}")
        elif ch in ('"', "\\"):
            parts.append("\\" + ch)
        else:
            parts.append(ch)
    parts.append('"')
    return "".join(parts)


def build_menu_js() -> str:
    items_js = "  const menuItems = [\n"
    for item in MENU_LABELS:
        items_js += f'    {{ href: "{item["href"]}", label: {_js_str(item["label"])} }},\n'
    items_js += "  ];"
    return MENU_JS_TEMPLATE.format(
        menu_items=items_js,
        kicker_json=_js_str(_kicker),
        book_json=_js_str(_book),
        close_json=_js_str(_close_lbl),
        foot1_json=_js_str(_foot1),
        foot2_json=_js_str(_foot2),
    )


MENU_BLOCK = MENU_CSS + "\n" + build_menu_js()


# ─── Strip old (broken) menu blocks ─────────────────────────────────────────
def strip_old_menu(html: str) -> str:
    html = re.sub(
        r'<style\s+id="[^"]*(?:lxs|LuxeStay)[^"]*demo-overrides"[\s\S]*?</style>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script\s+id="[^"]*(?:lxs|LuxeStay)[^"]*demo-nav"[\s\S]*?</script>',
        "",
        html,
        flags=re.I,
    )
    return html


# ─── Fix repeated brand prefix (only in attrs / style / script) ──────────────
def fix_old_class_prefix(html: str) -> str:
    def repl(m: re.Match) -> str:
        return OLD_PREFIX_PAT.sub(NEW_PREFIX, m.group(0))

    # class="..." and id="..." attributes
    html = re.sub(r'(?:class|id)="[^"]*"', repl, html)
    # <style> blocks (CSS selectors)
    html = re.sub(r'<style[^>]*>[\s\S]*?</style>', repl, html, flags=re.I)
    # <script> blocks (JS class/id references)
    html = re.sub(r'<script[^>]*>[\s\S]*?</script>', repl, html, flags=re.I)
    return html


# ─── Inject menu ────────────────────────────────────────────────────────────
def inject_menu(html: str) -> str:
    if 'id="lxs-demo-nav"' in html:
        return html
    return html.replace("</body>", MENU_BLOCK + "\n</body>", 1)


# ─── Process one file ────────────────────────────────────────────────────────
def process_file(fp: Path) -> bool:
    html = fp.read_text(encoding="utf-8-sig", errors="replace")
    original = html
    html = strip_old_menu(html)
    html = fix_old_class_prefix(html)
    html = inject_menu(html)
    if html != original:
        fp.write_text(html, encoding="utf-8-sig")
        return True
    return False


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    if not LUXESTAY_DIR.exists():
        print(f"ERROR: {LUXESTAY_DIR} not found")
        return
    updated = []
    for fp in sorted(LUXESTAY_DIR.glob("*.html")):
        if process_file(fp):
            updated.append(fp.name)
            print(f"  UPDATED: {fp.name}")
        else:
            print(f"  skip   : {fp.name}")
    print(f"\nDone. Updated {len(updated)} files.")


if __name__ == "__main__":
    main()
