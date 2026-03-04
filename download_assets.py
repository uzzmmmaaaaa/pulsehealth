import os
import re
import urllib.request
from urllib.parse import urlparse
import glob

html_files = glob.glob('*.html')
css_files = glob.glob('css/*.css')

# Target directories
BASE_IMG_DIR = 'assets/images'
DOCTORS_DIR = os.path.join(BASE_IMG_DIR, 'doctors')
ICONS_DIR = os.path.join(BASE_IMG_DIR, 'icons')
BANNERS_DIR = os.path.join(BASE_IMG_DIR, 'banners')

for d in [DOCTORS_DIR, ICONS_DIR, BANNERS_DIR]:
    os.makedirs(d, exist_ok=True)

# Regex to find Unsplash and other external images
img_pattern = re.compile(r'(https://images\.unsplash\.com/[^\s"\',\)]+)')

downloaded = {}
doc_counter = 1
banner_counter = 1
icon_counter = 1

def download_and_get_local_path(url, context_hint=''):
    global doc_counter, banner_counter, icon_counter
    
    if url in downloaded:
        return downloaded[url]
        
    print(f"Downloading {url} ...")
    try:
        # Determine path based on hint
        if 'doctor' in context_hint.lower() or 'avatar' in context_hint.lower() or ('w=300' in url or 'w=150' in url):
            filename = f"doctor_{doc_counter}.jpg"
            local_path = os.path.join(DOCTORS_DIR, filename)
            url_path = f"assets/images/doctors/{filename}"
            doc_counter += 1
        elif 'banner' in context_hint.lower() or 'hero' in context_hint.lower() or 'w=1200' in url or 'w=800' in url:
            filename = f"banner_{banner_counter}.jpg"
            local_path = os.path.join(BANNERS_DIR, filename)
            url_path = f"assets/images/banners/{filename}"
            banner_counter += 1
        else:
            # Default to icons/general
            filename = f"icon_{icon_counter}.jpg"
            local_path = os.path.join(ICONS_DIR, filename)
            url_path = f"assets/images/icons/{filename}"
            icon_counter += 1
            
        urllib.request.urlretrieve(url, local_path)
        downloaded[url] = url_path
        return url_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return url

# Process HTML files
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will replace URLs iteratively to have some context
    updated_content = content
    # Find all image tags to guess context
    img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', content)
    for src in img_tags:
        if src.startswith('http'):
            # Basic context hint
            context = 'doctor' if 'avatar' in content else ''
            # To be more precise, let's just use the URL params
            local_url = download_and_get_local_path(src, context_hint='doctor' if 'w=300' in src or 'w=150' in src else 'banner')
            updated_content = updated_content.replace(src, local_url)
            
    # Also find CSS background URLs in inline styles or other matches
    other_urls = img_pattern.findall(updated_content)
    for url in set(other_urls):
        local_url = download_and_get_local_path(url, context_hint='banner' if 'w=1200' in url else '')
        updated_content = updated_content.replace(url, local_url)
        
    if updated_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Updated {file}")

# Process CSS files
for file in css_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    other_urls = img_pattern.findall(content)
    updated_content = content
    for url in set(other_urls):
        local_url = download_and_get_local_path(url, context_hint='banner')
        updated_content = updated_content.replace(url, local_url)
        
    if updated_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Updated {file}")

print("Asset replacement complete.")
