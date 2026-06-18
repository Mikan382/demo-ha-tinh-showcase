import os
from bs4 import BeautifulSoup

with open("index.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

wrapper = soup.find(class_="insta-image-wrapper")
if wrapper:
    path = []
    parent = wrapper
    while parent:
        path.append(f"{parent.name}.{'.'.join(parent.get('class', []))}")
        parent = parent.parent
    print("DOM Path:", " -> ".join(reversed(path)))
else:
    print("Wrapper not found")
