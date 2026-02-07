"""
Script to replace <img src="assets/img/NAME.ext" ...> in HTML files with a <picture>
that serves WebP responsive images (if available) and falls back to original image.

Usage: python update_html_for_webp.py --site-root .

This script will:
 - Scan all .html files under the site root
 - For each <img> whose src starts with assets/img/ and ends with .jpg/.jpeg/.png
   it will replace it with a <picture> block referencing webp versions under
   assets/img/webp/ with the responsive widths: 400,800,1200 (if present).

Note: run this AFTER running the conversion script so webp files exist.
"""

import re
import argparse
from pathlib import Path

IMG_PATTERN = re.compile(r'<img\s+([^>]*?)src=["\'](assets/img/([^"\']+?\.(?:jpe?g|png)))["\']([^>]*?)>', re.IGNORECASE)

RESP_WIDTHS = [400,800,1200]

def make_picture_html(orig_src, rel_name, attrs_leading, attrs_trailing):
    name = Path(rel_name).stem
    dir_part = str(Path(rel_name).parent)
    webp_base = f"assets/img/webp/{dir_part}/{name}"
    # build srcset entries for webp if files exist (we don't check here; generate markup)
    srcset_webp = ", ".join([f"{webp_base}-{w}.webp {w}w" for w in RESP_WIDTHS])
    srcset_webp += f", {webp_base}.webp"  # full-size fallback in set
    # keep original attributes for img (merge leading+trailing)
    img_attrs = (attrs_leading + ' ' + attrs_trailing).strip()
    # ensure loading and decoding present
    if 'loading=' not in img_attrs:
        img_attrs += ' loading="lazy"'
    if 'decoding=' not in img_attrs:
        img_attrs += ' decoding="async"'
    picture = (
        f"<picture>\n"
        f"  <source type=\"image/webp\" srcset=\"{srcset_webp}\" sizes=\"100vw\">\n"
        f"  <img src=\"{orig_src}\" {img_attrs}>
"
        f"</picture>"
    )
    return picture


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    new_text, count = IMG_PATTERN.subn(lambda m: make_picture_html(m.group(1)+m.group(4), m.group(2), m.group(1), m.group(4)), text)
    if count > 0:
        backup = path.with_suffix(path.suffix + '.bak')
        path.rename(backup)
        path.write_text(new_text, encoding='utf-8')
        print(f"Updated {path} ({count} replacements). Backup at {backup}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-root', default='.', help='Root folder of site (default: .)')
    args = parser.parse_args()
    root = Path(args.site_root)
    html_files = list(root.rglob('*.html'))
    for h in html_files:
        process_file(h)

if __name__ == '__main__':
    main()
