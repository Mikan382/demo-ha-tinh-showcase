import os
import re

css_path = "assets/cdn.prod.website-files.com/68f0d3dd9d3c1fec17146b9f/css/asatha-luxury-webflow-template.webflow.shared.9a34a6ad6.css"

# 1. Clean up CSS file
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    
    # Remove everything after the comment "/* Fix Instagram Aspect Ratio */"
    if "/* Fix Instagram Aspect Ratio */" in css_content:
        print("Cleaning up CSS file...")
        css_content = css_content.split("/* Fix Instagram Aspect Ratio */")[0].rstrip() + "\n"
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        print("CSS file cleaned.")

# 2. Styles to inject
fix_styles = """
/* Instagram Layout Fix */
.insta-image-wrapper {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
  gap: 16px !important;
  align-items: start !important;
  position: relative !important;
}
.insta-image-div {
  height: auto !important;
  aspect-ratio: 1 / 1 !important;
  margin: 0 !important;
  overflow: hidden !important;
  position: relative !important;
}
.insta-image-div:nth-of-type(1) { flex: 1.2 1 0% !important; }
.insta-image-div:nth-of-type(2) { flex: 1.6 1 0% !important; }
.insta-image-div:nth-of-type(3) { flex: 1.0 1 0% !important; }
.insta-image-div:nth-of-type(4) { flex: 1.5 1 0% !important; }
.insta-image-div:nth-of-type(5) { flex: 1.1 1 0% !important; }

.insta-image-div.margin {
  margin-top: 32px !important;
}
.insta-post-image {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
}
.insta-post-button {
  position: absolute !important;
  top: calc(50% + 16px) !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  z-index: 10 !important;
}
"""

# 3. Inject into HTML files
html_count = 0
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find <style id="asatha-layout-fix">
            style_tag = '<style id="asatha-layout-fix">'
            if style_tag in content:
                # We will append the styles before the closing </style> of asatha-layout-fix
                pattern = r'(<style id="asatha-layout-fix">)(.*?)(</style>)'
                
                # Check if already injected
                if "/* Instagram Layout Fix */" in content:
                    # Replace the existing fix with the new one
                    content = re.sub(
                        r'/\* Instagram Layout Fix \*/.*?(?=\n</style>)',
                        fix_styles.strip(),
                        content,
                        flags=re.DOTALL
                    )
                else:
                    # Insert before </style>
                    def replacer(match):
                        return match.group(1) + match.group(2) + "\n" + fix_styles.strip() + "\n" + match.group(3)
                    content = re.sub(pattern, replacer, content, flags=re.DOTALL)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                html_count += 1

print(f"Successfully updated {html_count} HTML files with Instagram layout fixes!")
