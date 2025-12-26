import os
import re

# Configuration
directory = r'd:\\hello\\aerowp'
chapters_range = range(1, 21)

# New Sidebar Content (Collapsible)
# Inicio, Carrera, Materias, Galeria, Formulas, Capitulos, Glosario, Acerca de

new_sidebar_content = """                <li><a href="carrera.html">Carrera</a></li>
                <li><a href="materias.html">Materias</a></li>
                <li><a href="gallery.html">Galería</a></li>
                <li><a href="formulas.html">Fórmulas</a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li class="chapter-dropdown">
                    <details>
                        <summary>Capítulos ▾</summary>
                        <ul class="dropdown-list">
"""

# Only show chapters 1-10 in navigation
for i in range(1, 11):
    new_sidebar_content += f'                            <li><a href="chapter{i}.html">Capítulo {i}</a></li>\n'

new_sidebar_content += """                        </ul>
                    </details>
                </li>
                <li><a href="glossary.html">Glosario
                    </a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li><a href="about.html">Acerca de</a></li>"""

# Sidebar pattern to replace
# Matches from 'Carrera' link down to the end of the list (Acerca de)
# We need a robust regex to replace the entire old menu structure with the new one.
# Old structure starts after "Inicio".
sidebar_pattern = re.compile(
    r'(<li><a href="index\.html">Inicio</a></li>\s*)'
    r'(.*?)\s*'
    r'(</ul>)',
    re.DOTALL
)

def update_chapter_file(filepath, chapter_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Sidebar
    match = sidebar_pattern.search(content)
    if match:
        print(f"Updating sidebar in {filepath}")
        # match.group(1) is "Inicio" li, which we keep.
        # match.group(3) is "</ul>", which we keep.
        # We replace the middle part.
        new_content = match.group(1) + "\n" + new_sidebar_content + "\n            " + match.group(3)
        content = content.replace(match.group(0), new_content)
    else:
        print(f"Warning: Sidebar pattern not found in {filepath}")

    # 2. Add 'Go to Gallery' Button if missing
    if 'Ver Galería del Capítulo' not in content and 'class="card"' in content:
        # Only for chapters, which is checked by caller or implied by filenames
        if 'chapter' in os.path.basename(filepath):
             print(f"Adding Gallery button to {filepath}")
             gallery_btn = f'''
            <div style="margin-top: 30px; text-align: center;">
                <a href="gallery.html#chapter{chapter_num}" class="btn">🖼️ Ver Galería del Capítulo {chapter_num}</a>
            </div>
        '''
             content = re.sub(r'(\s*)</div>\s*</main>', f'{gallery_btn}\\1</div>\\1</main>', content)

    # 3. Add Image Placeholders if missing and 'media-container' invalid
    # (Existing logic seems fine, leaving as is or minor tweaks if needed)
    if 'media-container' not in content and 'chapter' in os.path.basename(filepath):
        placeholder = """
            <div class="media-container">
                [Espacio para Imagen/Video/Animación]
            </div>
            <p>Texto explicativo adicional...</p>
        """
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

# Apply to other main pages (carrera, materias, gallery, glossary, about, formulas)
# REMOVE topics.html, relations.html, contact.html from this list as they are being removed/hidden
other_pages = ['index.html', 'carrera.html', 'materias.html', 'gallery.html', 'glossary.html', 'about.html', 'formulas.html']

for page in other_pages:
    file = os.path.join(directory, page)
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Sidebar with new pattern
        match = sidebar_pattern.search(content)
        if match:
            print(f"Updating sidebar in {file}")
            new_nav_html = match.group(1) + "\n" + new_sidebar_content + "\n            " + match.group(3)
            content = content.replace(match.group(0), new_nav_html)
        else:
             print(f"Warning: Sidebar pattern not found in {file}")
             # Fallback if the pattern doesn't match exactly due to previous edits (like different indenting)
             # Try simpler replacement if needed, but the regex should cover standard layout.

        # Header code (same as before)
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
