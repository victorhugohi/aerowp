import os
import re

# Chapter Data
CHAPTERS_EN = [
    "Safety, Ground Operations, and Servicing",
    "Airport Operations",
    "Aeronautical Decision-Making",
    "Introduction to Flying",
    "Principles of Flight",
    "Human Factors",
    "Mathematics in Aviation Maintenance",
    "Physics for Aviation",
    "Regulations, Maintenance Forms, Records, and Publications",
    "Flight Manuals and Other Documents",
    "Aircraft Construction",
    "Aircraft Materials, Hardware, and Processes",
    "Flight Controls",
    "Flight Instruments",
    "Weight and Balance",
    "Aircraft Systems",
    "Aerodynamics of Flight",
    "Aircraft Performance",
    "Airspace",
    "Fundamentals of Electricity and Electronics"
]

CHAPTERS_ES = [
    "Seguridad, Operaciones en Tierra y Servicio",
    "Operaciones Aeroportuarias",
    "Toma de Decisiones Aeronáuticas",
    "Introducción al Vuelo",
    "Principios de Vuelo",
    "Factores Humanos",
    "Matemáticas en el Mantenimiento de Aviación",
    "Física para la Aviación",
    "Regulaciones, Formularios de Mantenimiento, Registros y Publicaciones",
    "Manuales de Vuelo y Otros Documentos",
    "Construcción de Aeronaves",
    "Materiales de Aeronaves, Hardware y Procesos",
    "Controles de Vuelo",
    "Instrumentos de Vuelo",
    "Peso y Balance",
    "Sistemas de Aeronaves",
    "Aerodinámica del Vuelo",
    "Rendimiento de la Aeronave",
    "Espacio Aéreo",
    "Fundamentos de Electricidad y Electrónica"
]

def get_sidebar_html(is_en):
    """Generates the sidebar HTML with 20 chapters."""
    base_link = "index.html" if not is_en else "index.html" # Relative to current dir if same level, but sidebar links are usually relative.
    # Actually, let's look at existing sidebar structure.
    # It uses relative links.
    
    items = []
    
    # Top items
    if is_en:
        items.append('<li><a href="index.html">Home</a></li>')
        items.append('<li><a href="carrera.html">Career</a></li>')
        items.append('<li><a href="topics.html">Topics</a></li>')
        items.append('<li><a href="gallery.html">Gallery</a></li>')
    else:
        items.append('<li><a href="index.html">Inicio</a></li>')
        items.append('<li><a href="carrera.html">Carrera</a></li>')
        items.append('<li><a href="topics.html">Temas</a></li>')
        items.append('<li><a href="gallery.html">Galería</a></li>')
        
    items.append('<li><hr style="border-color: rgba(255,255,255,0.1);"></li>')
    
    # Chapters
    for i in range(1, 21):
        label = f"Chapter {i}" if is_en else f"Capítulo {i}"
        items.append(f'<li><a href="chapter{i}.html">{label}</a></li>')
        
    # Bottom items
    items.append('<li><a href="glossary.html">Glossary' if is_en else '<li><a href="glossary.html">Glosario')
    items.append('</a></li>') # Closing tag for glossary
    items.append('<li><hr style="border-color: rgba(255,255,255,0.1);"></li>')
    
    if is_en:
        items.append('<li><a href="contact.html">Contact</a></li>')
        items.append('<li><a href="about.html">About</a></li>')
    else:
        items.append('<li><a href="contact.html">Contacto</a></li>')
        items.append('<li><a href="about.html">Acerca de</a></li>')
        
    return "\n                ".join(items)

def update_sidebar(content, is_en):
    """Updates the sidebar <ul> content."""
    pattern = r'(<nav>\s*<ul>)(.*?)(</ul>\s*</nav>)'
    
    # We need to be careful not to replace the whole nav if it has classes, but the pattern above captures the inner part.
    # Let's construct the new inner HTML.
    
    new_inner_html = "\n                " + get_sidebar_html(is_en) + "\n            "
    
    # Regex replacement
    # DOTALL is needed if .*? spans multiple lines (it does)
    return re.sub(pattern, fr'\1{new_inner_html}\3', content, flags=re.DOTALL)

def update_main_page_list(content, is_en):
    """Adds or updates the chapter list on the main page."""
    
    chapters = CHAPTERS_EN if is_en else CHAPTERS_ES
    title = "Chapter List" if is_en else "Lista de Capítulos"
    glossary_text = "Glossary" if is_en else "Glosario"
    
    list_html = f'<section id="chapter-list" class="chapter-list-section">\n'
    list_html += f'                <h2>{title}</h2>\n'
    list_html += '                <ul class="main-chapter-list">\n'
    
    for i, chap_name in enumerate(chapters, 1):
        list_html += f'                    <li><a href="chapter{i}.html"><strong>{i}.</strong> {chap_name}</a></li>\n'
    
    list_html += f'                    <li><a href="glossary.html" class="glossary-link">📖 {glossary_text}</a></li>\n'
    list_html += '                </ul>\n'
    list_html += '            </section>'
    
    # Insert before the closing </main> tag, or replace existing list if we had one (we don't yet).
    # But wait, we want to put it inside the .card if possible, or after the welcome message.
    # The current index.html has a .card inside <main>.
    
    if '<section id="chapter-list"' in content:
        # Replace existing
        pattern = r'<section id="chapter-list".*?</section>'
        content = re.sub(pattern, list_html, content, flags=re.DOTALL)
    else:
        # Insert after the "Select a chapter..." paragraph or at the end of .card
        # Looking at index.html: <p>Select a chapter from the menu to begin.</p>
        target = '<p>Select a chapter from the menu to begin.</p>' if is_en else '<p>Selecciona un capítulo del menú para comenzar.</p>'
        
        if target in content:
            content = content.replace(target, target + "\n\n            " + list_html)
        else:
            # Fallback: insert before closing div of card
            content = content.replace('</div>\n    </main>', '\n' + list_html + '\n        </div>\n    </main>')
            
    return content

def create_or_update_chapter_page(filepath, chapter_num, is_en):
    """Creates or updates a chapter page."""
    
    chapters = CHAPTERS_EN if is_en else CHAPTERS_ES
    chapter_title = chapters[chapter_num - 1]
    lang = "en" if is_en else "es"
    
    # Template for new files
    template = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{"Chapter" if is_en else "Capítulo"} {chapter_num} - {chapter_title}</title>
    <link rel="stylesheet" href="{'../' if is_en else ''}src/css/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Montserrat:wght@400;700&family=Oswald:wght@500&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <a href="{'../' if is_en else ''}index.html" class="logo-link" style="text-decoration: none; color: inherit;"><div class="logo-area">
            <span>✈️</span> AeroWP
        </div></a>
        <button class="menu-toggle">☰</button>
        <div class="lang-switch">
            <a href="{'../' if is_en else 'en/'}chapter{chapter_num}.html" class="btn" style="padding: 5px 10px; font-size: 0.8rem;">{'ES' if is_en else 'EN'}</a>
        </div>
    </header>

    <div class="sidebar">
        <nav>
            <ul>
                PLACEHOLDER_SIDEBAR
            </ul>
        </nav>
    </div>

    <main>
        <div class="card">
            <h1>{chapter_title}</h1>
            <p>{"Content pending for Chapter" if is_en else "Contenido pendiente para el Capítulo"} {chapter_num}.</p>
            
            <div class="media-container">
                [{"Placeholder for Image/Video" if is_en else "Espacio para Imagen/Video/Animación"}]
            </div>

            <p>{"Additional explanatory text..." if is_en else "Texto explicativo adicional..."}</p>
        </div>
    </main>

    <footer>
        <p>&copy; 2025 VHHI</p>
    </footer>

    <div id="chatbot-widget">
        <div class="fab">💬</div>
    </div>

    <script src="{'../' if is_en else ''}src/js/main.js"></script>
</body>
</html>
"""

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update Title in Head
        new_title_tag = f'<title>{"Chapter" if is_en else "Capítulo"} {chapter_num} - {chapter_title}</title>'
        content = re.sub(r'<title>.*?</title>', new_title_tag, content)
        
        # Update H1
        # Assuming H1 is inside .card
        new_h1 = f'<h1>{chapter_title}</h1>'
        content = re.sub(r'<h1>.*?</h1>', new_h1, content)
        
        # Update Sidebar (will be done by general update, but good to ensure structure)
        content = update_sidebar(content, is_en)
        
    else:
        content = template.replace('PLACEHOLDER_SIDEBAR', get_sidebar_html(is_en))
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filepath}")

def process_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                is_en = 'en' + os.sep in filepath or filepath.endswith(os.sep + 'en' + os.sep) or os.path.basename(dirpath) == 'en'
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update Sidebar
                new_content = update_sidebar(content, is_en)
                
                # Update Main Page List if index.html
                if filename == 'index.html':
                    new_content = update_main_page_list(new_content, is_en)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated sidebar/list in {filepath}")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Update existing files (sidebar + index list)
    process_directory(root_dir)
    
    # 2. Create/Update Chapter Pages
    for i in range(1, 21):
        # Spanish
        es_path = os.path.join(root_dir, f'chapter{i}.html')
        create_or_update_chapter_page(es_path, i, False)
        
        # English
        en_dir = os.path.join(root_dir, 'en')
        if not os.path.exists(en_dir):
            os.makedirs(en_dir)
        en_path = os.path.join(en_dir, f'chapter{i}.html')
        create_or_update_chapter_page(en_path, i, True)

if __name__ == "__main__":
    main()
