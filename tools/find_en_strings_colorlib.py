import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "colorlib-deluxe"

vietnamese_re = re.compile(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸÝĐ]')

en_words = [
    "the", "and", "with", "from", "for", "our", "your", "about", "contact", "news", "stories",
    "villas", "suites", "wellness", "dining", "packages", "latest", "recent", "tranquility",
    "essence", "designing", "nature", "rituals", "culinary", "chef", "sustainable", "luxury",
    "retreat", "sanctuary", "architecture", "embraces", "cliffs", "ancient", "healing",
    "practices", "authentic", "flavors", "commitment", "respecting", "hospitality", "read",
    "more", "utility", "changelog", "license", "styleguide", "hotel", "resort", "room",
    "rooms", "facility", "facilities", "service", "services", "event", "events", "activity",
    "activities", "blog", "gallery", "booking", "book", "now", "signin", "signup", "login",
    "register", "welcome", "experience", "comfort", "elegance", "style", "perfect", "fusion",
    "quick", "links", "guest", "adult", "child", "person", "team", "meet", "location", "address",
    "phone", "email", "subscribe", "newsletter", "similar", "view", "more", "learn", "special",
    "offers", "family", "fun", "romantic", "getaway", "spa", "play", "video", "watch", "show",
    "design", "by", "powered", "colorlib", "react", "template", "deluxe", "view", "details"
]

results = []

for fp in folder.glob("*.html"):
    html = fp.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for s in soup(["script", "style"]):
        s.decompose()
        
    text_nodes = soup.find_all(text=True)
    for node in text_nodes:
        text = node.strip()
        if not text:
            continue
        
        # Check if text looks like English and does not contain Vietnamese characters
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text)]
        if not words:
            continue
            
        is_vi = bool(vietnamese_re.search(text))
        if is_vi:
            # Check for mixed EN-VI cases
            lower_text = text.lower()
            # Catch known mixed phrases
            for word in ["read", "more", "us", "hotel", "room", "service", "event", "blog", "restaurant", "deluxe", "view", "details"]:
                if f" {word} " in f" {lower_text} ":
                    results.append((fp.name, text))
                    break
            continue
            
        # If it doesn't contain Vietnamese, check if it contains common English words
        # or if most of it is alphabetic characters (not just icons or numbers)
        has_en_keyword = any(w in words for w in en_words)
        # Also check if it's long enough to be an English sentence/phrase
        if has_en_keyword or len(words) > 1:
            results.append((fp.name, text))

# Print grouped by file
grouped = {}
for fname, text in results:
    grouped.setdefault(fname, []).append(text)

out_path = ROOT / "tools" / "en_strings_colorlib.txt"
with open(out_path, "w", encoding="utf-8") as out_f:
    for fname, texts in sorted(grouped.items()):
        out_f.write(f"=== {fname} ===\n")
        seen = set()
        for t in texts:
            t_clean = " ".join(t.split())
            if t_clean not in seen:
                out_f.write(f"  - {t_clean}\n")
                seen.add(t_clean)
print(f"Audit completed. Results saved to {out_path.name}")
