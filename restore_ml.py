import re
import os

demo_dir = 'c:/scratch/demo-ha-tinh-showcase/mountain-lodge-framer'
index_path = os.path.join(demo_dir, 'index.html')
orig_path = os.path.join(demo_dir, 'index_original.html')

# Get the broken demo's HTML to extract the image
with open(index_path, 'r', encoding='utf-8') as f:
    demo_html = f.read()

# Try to find the Ke Go image URL used in the broken demo
# It might be in src="..." or background-image: url(...)
images = re.findall(r'(assets/shared-images/[^"\']+)', demo_html)
kego_image = ''
for img in images:
    if 'hero' in img or 'lake' in img or 'lodge' in img or 'river' in img or 'kego' in img or '18_hero' in img or '19_hospitality' in img:
        kego_image = img
        break
if not kego_image and images:
    kego_image = images[0]
if not kego_image:
    kego_image = '../assets/shared-images/19_hospitality_forest_lake_lodge.png' # Fallback

print("Using Ke Go image:", kego_image)

# Now read the original HTML
with open(orig_path, 'r', encoding='utf-8') as f:
    orig_html = f.read()

# The original image might be a framerusercontent URL
# Let's find the largest image or the hero image in orig_html
orig_images = re.findall(r'https://framerusercontent\.com/images/[a-zA-Z0-9]+\.(?:jpg|png|webp)', orig_html)

# We will just replace ALL occurrences of 'Mountain Lodge' with 'Ke Go Eco Lodge'
# and '- YOUR PERFECT GETAWAY -' with 'Nghỉ dưỡng giữa rừng hồ Kẻ Gỗ'
new_html = orig_html.replace('Mountain Lodge', 'Ke Go Eco Lodge')
new_html = new_html.replace('- YOUR PERFECT GETAWAY -', 'Nghỉ dưỡng giữa rừng hồ Kẻ Gỗ')

# We need to replace the hero image. Let's replace the first or most prominent framer image with our kego_image.
# Actually, the background image of the clover is likely the one with the largest dimensions, or first one.
# Let's just replace all framer images that look like hero images, or just manually replace the one we know.
# In mountain lodge, the hero image is usually the first large image.
# We can replace all framerusercontent.com images with our kego_image to be safe, but that might overwrite other images.
# Let's find the specific image. The original template used a specific image for the clover.
# If we replace ALL of them, the whole page will have the same image, which is fine for a demo if we don't know which is which.
# But it's better to replace just the first few.
if len(orig_images) > 0:
    # Most likely the hero is the most frequently occurring image, or the first one.
    # Let's count frequencies
    from collections import Counter
    counts = Counter(orig_images)
    hero_image = counts.most_common(1)[0][0]
    print("Replacing hero image:", hero_image, "with", kego_image)
    new_html = new_html.replace(hero_image, kego_image)

# Also update the navigation links to Vietnamese
nav_replacements = {
    '>ABOUT<': '>Phòng<',
    '>ROOMS<': '>Giới thiệu<',
    '>AREA<': '>Liên hệ<',
    '>RESTAURANTS<': '>Nhà hàng<',
    '>EVENTS<': '>Sự kiện<',
    '>GALLERY<': '>Thư viện<',
    '>CONTACT<': '>Liên hệ<',
    '>BOOK<': '>Đặt phòng<'
}

for k, v in nav_replacements.items():
    new_html = new_html.replace(k, v)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Restoration complete!")
