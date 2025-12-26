import os
import re

# Configuration
directory = r'd:\\hello\\aerowp\\en'
chapters_range = range(1, 21)

# New Sidebar Content (English)
# Home, Career, Subjects, Gallery, Formulas, Chapters, Glossary, About
new_sidebar_content = """                <li><a href="carrera.html">Career</a></li>
                <li><a href="subjects.html">Subjects</a></li>
                <li><a href="gallery.html">Gallery</a></li>
                <li><a href="formulas.html">Formulas</a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li class="chapter-dropdown">
                    <details>
                        <summary>Chapters ▾</summary>
                        <ul class="dropdown-list">
"""

for i in range(1, 11):
    new_sidebar_content += f'                            <li><a href="chapter{i}.html">Chapter {i}</a></li>\n'

new_sidebar_content += """                        </ul>
                    </details>
                </li>
                <li><a href="glossary.html">Glossary
                    </a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li><a href="about.html">About</a></li>"""

# Sidebar pattern to replace
# Matches from 'Home' link down to the end of the list
# We assume the English pages have a similar structure but localized.
# We'll target the block inside <nav><ul> ... </ul></nav> more generically or use specific anchors.
# Let's anchor on "Home" link.
sidebar_pattern = re.compile(
    r'(<li><a href="index\.html">Home</a></li>\s*)'
    r'(.*?)\s*'
    r'(</ul>)',
    re.DOTALL
)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Sidebar
    match = sidebar_pattern.search(content)
    if match:
        print(f"Updating sidebar in {filepath}")
        new_nav_html = match.group(1) + "\n" + new_sidebar_content + "\n            " + match.group(3)
        content = content.replace(match.group(0), new_nav_html)
    else:
        print(f"Warning: Sidebar pattern not found in {filepath}")

    # 2. Update Header (Switch to ES)
    # Ensure link points to the Spanish counterpart
    filename = os.path.basename(filepath)
    es_target = filename # Default to same filename
    if filename == 'subjects.html':
        es_target = 'materias.html'
    
    # Check if header needs update or just link update
    # Note: English pages are in `en/` subdir, so link to ES is `../filename` or `../materias.html`
    
    if 'class="lang-switch"' in content:
        # Update ES link target
        content = re.sub(
            r'<a href="\.\./[^"]+" class="btn[^"]*"\s*[^>]*>\s*[^<]*ES\s*</a>',
            f'<a href="../{es_target}" class="btn lang-btn" style="padding: 5px 10px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px;">\n                    🇧🇴 ES\n                </a>',
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Apply to all English files
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        update_file(filepath)

print("English batch update completed.")
