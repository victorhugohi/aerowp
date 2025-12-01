import os

chapters = [f"chapter{i}.html" for i in range(1, 15)]
base_dir = "d:\\hello\\aerowp"

new_nav_items = """                <li><a href="index.html">Inicio</a></li>
                <li><a href="#">Carrera</a></li>
                <li><a href="topics.html">Temas</a></li>
                <li><a href="gallery.html">Galería</a></li>
                <li>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                </li>"""

chapter_links = "\n".join([f'                <li><a href="chapter{i}.html">Capítulo {i}</a></li>' for i in range(1, 15)])

new_bottom_nav = """                <li><a href="#">Glosario</a></li>
                <li>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                </li>
                <li><a href="contact.html">Contacto</a></li>
                <li><a href="about.html">Acerca de</a></li>"""

new_footer = """    <footer>
        <p>&copy; 2025 VHHI</p>
    </footer>"""

for chapter in chapters:
    file_path = os.path.join(base_dir, chapter)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the entire nav block for simplicity and robustness
        # We find the content between <nav> and </nav>
        
        start_nav = content.find("<nav>")
        end_nav = content.find("</nav>")
        
        if start_nav != -1 and end_nav != -1:
            new_nav_content = f"""<nav>
            <ul>
{new_nav_items}
{chapter_links}
{new_bottom_nav}
            </ul>
        </nav>"""
            
            content = content[:start_nav] + new_nav_content + content[end_nav+6:]
            
        # Update Footer
        start_footer = content.find("<footer>")
        end_footer = content.find("</footer>")
        
        if start_footer != -1 and end_footer != -1:
            content = content[:start_footer] + new_footer + content[end_footer+9:]
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {chapter}")
