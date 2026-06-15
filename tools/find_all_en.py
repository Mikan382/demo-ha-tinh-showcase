import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "colorlib-deluxe"

# Look for text nodes that contain English text.
# We want to find anything that looks like English, even if the file is partially translated.
# We will filter out script, style, and purely numeric/punctuation nodes.

# Let's list some common Vietnamese words/characters to help identify mixed text.
vietnamese_re = re.compile(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸÝĐ]')

en_words_list = [
    "the", "and", "with", "from", "for", "our", "your", "about", "contact", "news",
    "villas", "suites", "wellness", "dining", "packages", "latest", "recent",
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "hotel", "resort", "room", "rooms", "service", "services", "event", "events",
    "activity", "activities", "blog", "gallery", "booking", "book", "now", "signin",
    "signup", "login", "register", "welcome", "experience", "comfort", "elegance",
    "view", "details", "tour", "review", "rating", "ratings", "take", "leave", "comment",
    "name", "email", "message", "subject", "send", "phone", "address", "website",
    "adult", "adults", "child", "children", "person", "people", "guest", "guests",
    "beef", "potatoes", "duden", "flows", "pineapple", "ham", "ultimate", "overload",
    "creative", "designer", "wordpress", "theme", "themes", "smith", "doe", "december"
]

results = []

for fp in folder.glob("*.html"):
    html = fp.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script, style, head, and meta elements
    for s in soup(["script", "style", "meta", "link", "noscript"]):
        s.decompose()
        
    text_nodes = soup.find_all(text=True)
    for node in text_nodes:
        text = node.strip()
        if not text:
            continue
            
        # Ignore comments
        if text.startswith("<!--") or text.endswith("-->"):
            continue
            
        # Ignore text that is purely numbers, symbols or whitespace
        if not re.search(r'[a-zA-Z]', text):
            continue
            
        # If the text has Vietnamese characters, it is likely mostly translated,
        # but let's check if it contains mixed English words we want to translate.
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text)]
        if not words:
            continue
            
        is_vi = bool(vietnamese_re.search(text))
        
        # If it has no Vietnamese, or if it is mixed and contains some english keywords:
        has_en = any(w in en_words_list for w in words)
        # Also include if it has no Vietnamese and has more than 1 word (since it's English text)
        if (not is_vi and (has_en or len(words) > 1)) or (is_vi and has_en and any(word in ["read", "more", "us", "hotel", "room", "service", "event", "blog", "restaurant", "view", "details", "adult", "child", "children", "person", "people"] for word in words)):
            results.append((fp.name, text))

# Print grouped by file
grouped = {}
for fname, text in results:
    grouped.setdefault(fname, []).append(text)

out_path = ROOT / "tools" / "en_all_colorlib.txt"
with open(out_path, "w", encoding="utf-8") as out_f:
    for fname, texts in sorted(grouped.items()):
        out_f.write(f"=== {fname} ===\n")
        seen = set()
        for t in texts:
            t_clean = " ".join(t.split())
            if t_clean not in seen:
                out_f.write(f"  - {t_clean}\n")
                seen.add(t_clean)
print(f"Extraction completed. Results saved to {out_path.name}")
