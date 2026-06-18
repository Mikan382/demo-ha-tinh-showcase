#!/usr/bin/env python3
"""
Tự động quét và sửa lỗi layout ảnh (khác aspect ratio) trong các template HTML.
Loại trừ các layout cố tình lộn xộn như masonry, isotope.
Bỏ qua logo, icon, ảnh chân dung.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("Vui lòng cài đặt beautifulsoup4: pip install beautifulsoup4")
    exit(1)

ROOT = Path(__file__).resolve().parents[1]

# Các thư mục chứa template cần quét
TARGET_DIRS = [
    "travol-duruthemes",
    "hotale-resort",
    "colorlib-deluxe",
    "moonlit-react",
    "asatha-luxury-webflow",
    "luxestay-framer",
    "mountain-lodge-framer",
    "wanderway-framer",
]

STYLE_INJECTION = """
<style id="auto-crop-image-style">
/* Tự động crop ảnh cho các grid/card để tránh vỡ layout do sai tỉ lệ */
.auto-crop-image {
    width: 100% !important;
    aspect-ratio: 4/3 !important;
    object-fit: cover !important;
}
</style>
"""

# Các từ khóa nhận diện layout lộn xộn có chủ đích
MASONRY_KEYWORDS = {"masonry", "isotope"}

# Các từ khóa nhận diện ảnh không nên ép tỉ lệ (logo, icon, avatar...)
EXCLUDE_IMG_KEYWORDS = {"logo", "icon", "avatar", "person", "author", "testimonial", "insta", "instagram"}

def has_class_keyword(element: Tag, keywords: set[str]) -> bool:
    """Kiểm tra xem element có chứa class nào nằm trong tập keywords hay không."""
    classes = element.get("class", [])
    if not classes:
        return False
    if isinstance(classes, str):
        classes = [classes]
    
    classes_lower = [c.lower() for c in classes]
    for c in classes_lower:
        for kw in keywords:
            if kw in c:
                return True
    return False

def is_in_masonry(img: Tag) -> bool:
    """Kiểm tra xem ảnh có nằm trong một khối masonry/isotope không."""
    parent = img.parent
    # Duyệt ngược lên 5 cấp cha để tìm masonry container
    depth = 0
    while parent and parent.name != "body" and depth < 5:
        if has_class_keyword(parent, MASONRY_KEYWORDS):
            return True
        parent = parent.parent
        depth += 1
    return False

def is_target_container(img: Tag) -> bool:
    """Kiểm tra xem ảnh có nằm trong grid/card/item hay không."""
    parent = img.parent
    depth = 0
    target_keywords = {"item", "card", "tour", "room", "post", "blog", "col-"}
    while parent and parent.name != "body" and depth < 5:
        if has_class_keyword(parent, target_keywords):
            return True
        parent = parent.parent
        depth += 1
    return False

def fix_html_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    
    # Dùng html.parser thay vì lxml để không bắt buộc cài thêm lxml
    soup = BeautifulSoup(content, "html.parser")
    
    modified = False
    
    images = soup.find_all("img")
    for img in images:
        skip = False
        
        # Bỏ qua nếu src là svg
        src = img.get("src", "").lower()
        if src.endswith(".svg"):
            skip = True
            
        # Bỏ qua các ảnh logo, icon, avatar dựa trên class của chính nó hoặc src
        if not skip and has_class_keyword(img, EXCLUDE_IMG_KEYWORDS):
            skip = True
        if not skip and any(kw in src for kw in EXCLUDE_IMG_KEYWORDS):
            skip = True
            
        # Kiểm tra thẻ cha xem có phải logo/avatar không
        if not skip:
            parent = img.parent
            depth = 0
            while parent and parent.name != "body" and depth < 2:
                if has_class_keyword(parent, EXCLUDE_IMG_KEYWORDS):
                    skip = True
                    break
                parent = parent.parent
                depth += 1
                
        # Bỏ qua nếu thuộc masonry
        if not skip and is_in_masonry(img):
            skip = True

        classes = img.get("class", [])
        if isinstance(classes, str):
            classes = [classes]
            
        if skip:
            # Nếu bị bỏ qua mà đang có auto-crop-image thì gỡ ra
            if "auto-crop-image" in classes:
                classes.remove("auto-crop-image")
                img["class"] = classes
                modified = True
            continue
            
        # Nếu nằm trong item/card/grid thông thường, ta sẽ thêm class
        if is_target_container(img):
            if "auto-crop-image" not in classes:
                classes.append("auto-crop-image")
                img["class"] = classes
                modified = True

    if modified:
        # Tiêm style vào head nếu chưa có
        head = soup.find("head")
        if head and not soup.find(id="auto-crop-image-style"):
            # Chuyển text thành BeautifulSoup tag
            style_soup = BeautifulSoup(STYLE_INJECTION, "html.parser")
            head.append(style_soup)
        
        # Ghi đè file
        file_path.write_text(str(soup), encoding="utf-8")
        print(f"Đã sửa (Fixed): {file_path.relative_to(ROOT)}")

def main():
    print(f"Bắt đầu quét thư mục gốc: {ROOT}")
    for d in TARGET_DIRS:
        folder = ROOT / d
        if not folder.exists() or not folder.is_dir():
            continue
            
        for file_path in folder.rglob("*.html"):
            fix_html_file(file_path)
            
    print("Hoàn tất sửa lỗi layout ảnh!")

if __name__ == "__main__":
    main()
