import os

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    is_en = 'en' + os.sep in filepath or filepath.endswith(os.sep + 'en' + os.sep)
    index_link = "../index.html" if is_en else "index.html"
    
    # 1. Wrap Logo in Link
    if '<div class="logo-area">' in content and '<a href="' + index_link + '" class="logo-link">' not in content:
        # Check if already wrapped (simple check)
        if 'class="logo-link"' not in content:
             content = content.replace(
                '<div class="logo-area">',
                f'<a href="{index_link}" class="logo-link" style="text-decoration: none; color: inherit;"><div class="logo-area">'
            ).replace(
                '<span>✈️</span> AeroWP\n        </div>',
                '<span>✈️</span> AeroWP\n        </div></a>'
            )

    # 2. Update Glossary Link
    # Spanish
    content = content.replace('href="#">Glosario</a>', 'href="glossary.html">Glosario</a>')
    # English
    content = content.replace('href="#">Glossary</a>', 'href="glossary.html">Glossary</a>')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    root_dir = '.'
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                update_file(filepath)

if __name__ == "__main__":
    main()
