Conversion to WebP and responsive srcset — instructions

What I created
- `scripts/convert_images.ps1` — PowerShell script to convert `assets/img/**/*.(jpg|jpeg|png)` to WebP responsive versions under `assets/img/webp/...` (widths: 400,800,1200 + full-size).
- `scripts/update_html_for_webp.py` — Python script to scan HTML files and replace `<img src="assets/img/...">` with a `<picture>` block that prefers WebP `srcset` and falls back to the original image.

Why this approach
- WebP reduces image payload significantly.
- Responsive `srcset` serves smaller images to small viewports.
- Using a `<picture>` element keeps fallback compatibility.

Prerequisites (install one of these):
- ImageMagick (recommended): https://imagemagick.org (adds `magick` to PATH)
  or
- Google `cwebp` (https://developers.google.com/speed/webp/docs/cwebp)

Also install Python if you want to run the HTML update script.

Usage
1. From repository root, run the PowerShell conversion (requires `magick` or `cwebp`):

```powershell
# PowerShell (run in repo root)
# Optionally run PowerShell as Administrator
powershell -ExecutionPolicy Bypass -File .\scripts\convert_images.ps1 -SrcDir "assets/img" -OutDir "assets/img/webp" -Widths 400,800,1200 -Quality 80
```

2. After conversion completes, run the Python updater to modify HTML files (it makes .bak backups):

```bash
# If you have Python
python scripts/update_html_for_webp.py --site-root .
```

3. Verify the `assets/img/webp` folder contains `.webp` files and open your pages locally. If everything looks fine, remove `.bak` files.

Notes & next steps
- The script generates `name-400.webp`, `name-800.webp`, `name-1200.webp`, and `name.webp` (full-size) under `assets/img/webp/<original-subdir>`.
- I didn't modify HTML automatically because image tools aren't installed in the environment; the scripts will modify HTML when you run them locally.
- After you run them, I can finish updating references to `assets/css/main.min.css` across HTML and mark the task complete.

Would you like me to:
- attempt conversions here (I checked and `magick`/`cwebp` are not installed), or
- update HTML now to reference `main.min.css` and leave image conversion to you to run locally?