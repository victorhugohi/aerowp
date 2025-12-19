import os
import re

# Configuration
directory = r'd:\\hello\\aerowp'
chapters_range = range(1, 21)

# New Sidebar Content (Collapsible)
new_sidebar_content = """                <li><a href="gallery.html">Galería</a></li>
                <li><a href="formulas.html">Fórmulas</a></li>
                <li><a href="relations.html">Relación de Materias</a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li class="chapter-dropdown">
                    <details>
                        <summary>Capítulos ▾</summary>
                        <ul class="dropdown-list">
"""
for i in range(1, 21):
    new_sidebar_content += f'                            <li><a href="chapter{i}.html">Capítulo {i}</a></li>\n'

new_sidebar_content += """                        </ul>
                    </details>
                </li>
                <li><a href="glossary.html">Glosario
                    </a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>"""

# Sidebar pattern to replace
# Matches from 'Galería' link down to the separator after Glossary
sidebar_pattern = re.compile(
    r'<li><a href="gallery\.html">Galería</a></li>.*?'
    r'<li><a href="glossary\.html">Glosario\s*</a></li>\s*'
    r'<li>\s*<hr[^>]*>\s*</li>',
    re.DOTALL
)

def update_chapter_file(filepath, chapter_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Sidebar
    if 'class="chapter-dropdown"' not in content or 'formulas.html' not in content:
        # Try finding the block to replace
        match = sidebar_pattern.search(content)
        if match:
            print(f"Updating sidebar in {filepath}")
            content = content.replace(match.group(0), new_sidebar_content)
        else:
            print(f"Warning: Sidebar pattern not found in {filepath}")

    # 2. Add 'Go to Gallery' Button if missing
    if 'Ver Galería del Capítulo' not in content and 'class="card"' in content:
        print(f"Adding Gallery button to {filepath}")
        gallery_btn = f'''
            <div style="margin-top: 30px; text-align: center;">
                <a href="gallery.html#chapter{chapter_num}" class="btn">🖼️ Ver Galería del Capítulo {chapter_num}</a>
            </div>
        '''
        # Insert before the closing </div> of .card
        # We look for the last </div> inside <main> or generally the last </div> before </main>
        content = re.sub(r'(\s*)</div>\s*</main>', f'{gallery_btn}\\1</div>\\1</main>', content)

    # 3. Add Image Placeholders if missing and 'media-container' invalid
    if 'media-container' not in content:
        placeholder = """
            <div class="media-container">
                [Espacio para Imagen/Video/Animación]
            </div>
            <p>Texto explicativo adicional...</p>
        """
        # Insert after h1 or the first paragraph
        content = re.sub(r'(</h1>)', f'\\1\n{placeholder}', content)

    # 4. Update Header Search/Flags
    if 'class="lang-switch"' in content and 'class="header-controls"' not in content:
         print(f"Updating header in {filepath}")
         header_regex = re.compile(
             r'<button class="menu-toggle">☰</button>\s*'
             r'<div class="lang-switch">\s*'
             r'<a href="[^"]+" class="btn"[^>]*>EN</a>\s*'
             r'</div>',
             re.DOTALL
         )
         
         header_replacement = f"""<button class="menu-toggle">☰</button>
        <div class="header-controls" style="display: flex; gap: 10px; align-items: center;">
            <button class="search-btn" style="background:none; border:none; font-size: 1.2rem; cursor: pointer;">🔍</button>
            <div class="lang-switch">
                <a href="en/chapter{chapter_num}.html" class="btn lang-btn" style="padding: 5px 10px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px;">
                    🇺🇸 EN
                </a>
            </div>
        </div>"""
         content = header_regex.sub(header_replacement, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Apply to all chapters
for i in chapters_range:
    file = os.path.join(directory, f'chapter{i}.html')
    if os.path.exists(file):
        update_chapter_file(file, i)

# Apply to other main pages (carrera, topics, gallery, glossary, contact, about) as well?
other_pages = ['index.html', 'carrera.html', 'topics.html', 'gallery.html', 'glossary.html', 'contact.html', 'about.html', 'formulas.html', 'relations.html']
for page in other_pages:
    file = os.path.join(directory, page)
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Sidebar
        if 'class="chapter-dropdown"' not in content or 'formulas.html' not in content:
            match = sidebar_pattern.search(content)
            if match:
                print(f"Updating sidebar in {file}")
                content = content.replace(match.group(0), new_sidebar_content)

        # Header
        if 'class="header-controls"' not in content:
            print(f"Updating header in {file}")
            # Identify EN link target
            en_link_match = re.search(r'<a href="en/([^"]+)" class="btn"', content)
            en_target = en_link_match.group(1) if en_link_match else f'{page}'
            
            header_regex = re.compile(
                 r'<button class="menu-toggle">☰</button>\s*'
                 r'<div class="lang-switch">\s*'
                 r'<a href="[^"]+" class="btn"[^>]*>EN</a>\s*'
                 r'</div>',
                 re.DOTALL
             )
            header_replacement = f"""<button class="menu-toggle">☰</button>
        <div class="header-controls" style="display: flex; gap: 10px; align-items: center;">
            <button class="search-btn" style="background:none; border:none; font-size: 1.2rem; cursor: pointer;">🔍</button>
            <div class="lang-switch">
                <a href="en/{en_target}" class="btn lang-btn" style="padding: 5px 10px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px;">
                    🇺🇸 EN
                </a>
            </div>
        </div>"""
            content = header_regex.sub(header_replacement, content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Batch update completed.")
