import os
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GALLERY_FILE = os.path.join(ROOT_DIR, 'gallery.html')

def update_chapter_content(filepath, chapter_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Hide English Button
    # Look for .lang-switch container
    if 'class="lang-switch"' in content and 'style="display:none"' not in content:
        content = content.replace('class="lang-switch"', 'class="lang-switch" style="display:none"')

    # 2. Cleanup Footer Garbage
    # Remove "Texto explicativo adicional..."
    content = re.sub(r'<p>Texto explicativo adicional\.\.\.</p>', '', content)
    
    # Remove ALL existing "Ver Galería" buttons to avoid duplication, we will add ONE back.
    # Pattern for the button container
    gallery_btn_pattern = r'<div style="margin-top: 30px; text-align: center;">\s*<a href="gallery\.html#chapter\d+" class="btn">.*?</a>\s*</div>'
    content = re.sub(gallery_btn_pattern, '', content, flags=re.DOTALL)

    # 3. Inject Image Placeholders after Subpoints (</h3>)
    # Only if not already present immediately after?
    # We'll just replace </h3> with </h3> + placeholder
    # usage: </h3> -> </h3>\n<div...>...</div>
    
    placeholder_html = '\n            <div class="media-container">\n                [Espacio para Imagen/Video/Animación]\n            </div>'
    
    # Avoid double insertion if run multiple times?
    # We can check if the placeholder follows </h3>
    # But for a simple script, we might just assume we run it once or regex check.
    # Let's use a regex that asserts NOT followed by media-container
    
    # Simple approach: Find </h3>. Replace with </h3> + placeholder.
    # BUT we don't want to add it if it's already there.
    
    # Let's split by </h3>, and check the next part.
    parts = content.split('</h3>')
    new_parts = []
    for i, part in enumerate(parts):
        new_parts.append(part)
        if i < len(parts) - 1: # Don't add after the last part (file end)
            # Check if next part starts with placeholder (ignoring whitespace)
            next_part_preview = parts[i+1].strip()
            if not next_part_preview.startswith('<div class="media-container">'):
                 new_parts.append(placeholder_html)
            
    content = '</h3>'.join(new_parts)

    # 4. Add SINGLE Ver Gallery Button at the end of .card
    gallery_btn = f'''
            <div style="margin-top: 30px; text-align: center;">
                <a href="gallery.html#chapter{chapter_num}" class="btn">🖼️ Ver Galería del Capítulo {chapter_num}</a>
            </div>'''
    
    content = re.sub(r'(\s*)</div>\s*</main>', f'{gallery_btn}\\1</div>\\1</main>', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def update_gallery():
    with open(GALLERY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    
    # 1. Hide English Button
    if 'class="lang-switch"' in content and 'style="display:none"' not in content:
        content = content.replace('class="lang-switch"', 'class="lang-switch" style="display:none"')
        
    # 2. Add "Feria de Aeronáutica" Section at TOP of main
    feria_section = '''            <section id="feria" style="margin-bottom: 40px; background: #f9f9f9; padding: 20px; border-radius: 8px;">
                <h2 style="border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; color: #2c3e50;">Feria de Aeronáutica</h2>
                <div class="gallery-container">
                    <figure>
                        <img src="src/assets/images/placeholder-feria.png" alt="Feria de Aeronáutica"
                            style="background: #ddd; height: 200px; display: flex; align-items: center; justify-content: center;">
                        <figcaption>Fotos del evento Feria de Aeronáutica</figcaption>
                    </figure>
                </div>
            </section>
'''
    
    if 'id="feria"' not in content:
        # Insert after <h1>Galería Multimedia</h1>
        content = content.replace('<h1>Galería Multimedia</h1>', '<h1>Galería Multimedia</h1>\n' + feria_section)

    if content != original_content:
        with open(GALLERY_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated gallery.html")

def main():
    # Update Chapters 1-10
    for i in range(1, 11):
        filepath = os.path.join(ROOT_DIR, f'chapter{i}.html')
        if os.path.exists(filepath):
            update_chapter_content(filepath, i)
            
    # Update Gallery
    if os.path.exists(GALLERY_FILE):
        update_gallery()
        
    # Also hide English button in index.html, formulas.html, etc.
    other_files = ['index.html', 'about.html', 'contact.html', 'formulas.html', 'glossary.html']
    for filename in other_files:
        filepath = os.path.join(ROOT_DIR, filename)
        if os.path.exists(filepath):
             with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
             if 'class="lang-switch"' in content and 'style="display:none"' not in content:
                content = content.replace('class="lang-switch"', 'class="lang-switch" style="display:none"')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Hidden English button in {filename}")

if __name__ == "__main__":
    main()
