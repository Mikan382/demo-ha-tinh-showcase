import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "asatha-luxury-webflow"

# Words that indicate English but are not common brand names or codes
# Let's search for text nodes that contain English words and don't contain Vietnamese characters.
# Vietnamese characters: áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ
vietnamese_re = re.compile(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸÝĐ]')

en_words = ["the", "and", "with", "from", "for", "our", "your", "about", "contact", "news", "stories", "villas", "suites", "wellness", "dining", "packages", "latest", "recent", "tranquility", "essence", "designing", "nature", "rituals", "culinary", "chef", "sustainable", "luxury", "retreat", "sanctuary", "architecture", "embraces", "cliffs", "ancient", "healing", "practices", "authentic", "flavors", "commitment", "respecting", "hospitality", "read", "more", "utility", "changelog", "license", "styleguide"]

results = []

for fp in folder.glob("*.html"):
    # Skip template config pages if they are not part of the showcase website
    # actually let's scan all to be sure
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
        # Also ensure it has some length and contains some english keywords
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text)]
        if not words:
            continue
            
        is_vi = bool(vietnamese_re.search(text))
        if is_vi:
            # Maybe it is mixed?
            # If it contains "Read Khác" or "Liên hệ Us", we want to catch it!
            lower_text = text.lower()
            if "read" in lower_text or "us" in lower_text or "utility" in lower_text:
                results.append((fp.name, text))
            continue
            
        # If it doesn't contain Vietnamese, let's see if it has English common words
        has_en_keyword = any(w in words for w in en_words)
        if has_en_keyword:
            results.append((fp.name, text))

# Print grouped by file
grouped = {}
for fname, text in results:
    grouped.setdefault(fname, []).append(text)

# Write results to a file with UTF-8 encoding
out_path = ROOT / "tools" / "en_strings_audit.txt"
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

