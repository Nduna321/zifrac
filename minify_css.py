import re

# Read the full CSS file
with open('assets/css/main.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Minify CSS
# Remove comments
css_minified = re.sub(r'/\*[\s\S]*?\*/', '', css_content)

# Remove whitespace at beginning and end of lines
css_minified = re.sub(r'^\s+', '', css_minified, flags=re.MULTILINE)
css_minified = re.sub(r'\s+$', '', css_minified, flags=re.MULTILINE)

# Remove unnecessary spaces around special characters
css_minified = re.sub(r'\s*([{}:;,])\s*', r'\1', css_minified)

# Remove newlines while preserving where needed
css_minified = re.sub(r'\n+', '', css_minified)

# Remove spaces between selectors
css_minified = re.sub(r',\s*', ',', css_minified)

# Clean up any remaining tabs
css_minified = re.sub(r'\t', '', css_minified)

# Write minified CSS
with open('assets/css/main.min.css', 'w', encoding='utf-8') as f:
    f.write(css_minified)

print(f"Original size: {len(css_content):,} bytes")
print(f"Minified size: {len(css_minified):,} bytes")
print(f"Reduction: {((len(css_content) - len(css_minified)) / len(css_content) * 100):.1f}%")
print("\nMinified CSS file created: assets/css/main.min.css")
