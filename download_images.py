"""Download all lab images from Wikimedia Commons (free licenses).

Usage: python download_images.py
Creates image.jpg, eval_images/, images/, vqa_images/ and CREDITS.md.
"""
import json
import os
import time
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "CLIP-LLaVA-Lab/1.0 (https://github.com/yassirtl/CLIP-LLaVA-Lab)"}
WIDTH = 640

# (output folder, file prefix, search query, number of images)
PLAN = [
    (".", "image", "cat portrait", 1),
    # Exercise 5 - labeled evaluation set (label = file prefix)
    ("eval_images", "cat", "domestic cat sitting", 2),
    ("eval_images", "dog", "dog portrait", 2),
    ("eval_images", "car", "hatchback car", 2),
    ("eval_images", "airplane", "airliner in flight", 2),
    ("eval_images", "horse", "horse in field", 2),
    ("eval_images", "bird", "bird perched on branch", 2),
    # Exercises 7-8 - retrieval database
    ("images", "football", "soccer player dribbling ball", 4),
    ("images", "basketball", "basketball game players", 2),
    ("images", "tennis", "tennis player match", 2),
    ("images", "dog", "dog running grass", 2),
    ("images", "cat", "cat sleeping", 2),
    ("images", "car", "sports car", 2),
    ("images", "bus", "city bus", 2),
    ("images", "building", "skyscraper building", 2),
    ("images", "landscape", "mountain landscape lake", 2),
    ("images", "food", "pizza on plate", 2),
    ("images", "beach", "beach sea sand", 2),
    # Exercises 10-12 - LLaVA VQA and hallucination test
    ("vqa_images", "classroom", "classroom whiteboard", 1),
    ("vqa_images", "street", "people walking street market", 1),
    ("vqa_images", "dinner", "family dinner table", 1),
    ("vqa_images", "office", "people working office meeting", 1),
    ("vqa_images", "kitchen", "modern kitchen", 1),
]


def search(query, limit=30):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrnamespace": 6, "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": WIDTH,
    }
    req = urllib.request.Request(f"{API}?{urllib.parse.urlencode(params)}", headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        pages = json.load(r).get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("index", 0))


def download(url, path):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r, open(path, "wb") as f:
        f.write(r.read())


def main():
    used, credits = set(), []
    for folder, prefix, query, n in PLAN:
        os.makedirs(folder, exist_ok=True)
        count = 0
        for page in search(query):
            info = page["imageinfo"][0]
            if count == n:
                break
            if info["mime"] != "image/jpeg" or page["title"] in used:
                continue
            name = f"{prefix}.jpg" if prefix == "image" else f"{prefix}{count + 1}.jpg"
            path = os.path.join(folder, name)
            download(info["thumburl"], path)
            used.add(page["title"])
            meta = info.get("extmetadata", {})
            license_ = meta.get("LicenseShortName", {}).get("value", "see source")
            credits.append((path, page["title"], info["descriptionurl"], license_))
            count += 1
            print(f"{path:30s} <- {page['title']}")
            time.sleep(0.3)

    with open("CREDITS.md", "w") as f:
        f.write("# Image credits\n\nAll images are from Wikimedia Commons under free licenses.\n\n")
        f.write("| File | Source | License |\n|---|---|---|\n")
        for path, title, url, license_ in credits:
            f.write(f"| `{path.lstrip('./')}` | [{title}]({url}) | {license_} |\n")


if __name__ == "__main__":
    main()
