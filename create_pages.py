import os

# Content for Sidebar (Updated)
sidebar_content = """    <div class="sidebar">
        <nav>
            <ul>
                <li><a href="index.html">Inicio</a></li>
                <li><a href="carrera.html">Carrera</a></li>
                <li><a href="topics.html">Temas</a></li>
                <li><a href="gallery.html">Galería</a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li class="chapter-dropdown">
                    <details>
                        <summary>Capítulos ▾</summary>
                        <ul class="dropdown-list">
                            <li><a href="chapter1.html">Capítulo 1</a></li>
                            <li><a href="chapter2.html">Capítulo 2</a></li>
                            <li><a href="chapter3.html">Capítulo 3</a></li>
                            <li><a href="chapter4.html">Capítulo 4</a></li>
                            <li><a href="chapter5.html">Capítulo 5</a></li>
                            <li><a href="chapter6.html">Capítulo 6</a></li>
                            <li><a href="chapter7.html">Capítulo 7</a></li>
                            <li><a href="chapter8.html">Capítulo 8</a></li>
                            <li><a href="chapter9.html">Capítulo 9</a></li>
                            <li><a href="chapter10.html">Capítulo 10</a></li>
                            <li><a href="chapter11.html">Capítulo 11</a></li>
                            <li><a href="chapter12.html">Capítulo 12</a></li>
                            <li><a href="chapter13.html">Capítulo 13</a></li>
                            <li><a href="chapter14.html">Capítulo 14</a></li>
                            <li><a href="chapter15.html">Capítulo 15</a></li>
                            <li><a href="chapter16.html">Capítulo 16</a></li>
                            <li><a href="chapter17.html">Capítulo 17</a></li>
                            <li><a href="chapter18.html">Capítulo 18</a></li>
                            <li><a href="chapter19.html">Capítulo 19</a></li>
                            <li><a href="chapter20.html">Capítulo 20</a></li>
                        </ul>
                    </details>
                </li>
                <li><a href="glossary.html">Glosario</a></li>
                <li><hr style="border-color: rgba(255,255,255,0.1);"></li>
                <li><a href="contact.html">Contacto</a></li>
                <li><a href="about.html">Acerca de</a></li>
            </ul>
        </nav>
    </div>"""

# Header Content (Updated)
def get_header(page_type="generic"):
    # page_type could be used for english link logic
    en_link = f"en/{page_type}.html"
    return f"""    <header>
        <a href="index.html" class="logo-link" style="text-decoration: none; color: inherit;">
            <div class="logo-area">
                <span>✈️</span> AeroWP
            </div>
        </a>
        <button class="menu-toggle">☰</button>
        <div class="header-controls" style="display: flex; gap: 10px; align-items: center;">
            <button class="search-btn" style="background:none; border:none; font-size: 1.2rem; cursor: pointer;">🔍</button>
            <div class="lang-switch">
                <a href="{en_link}" class="btn lang-btn" style="padding: 5px 10px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px;">
                    🇺🇸 EN
                </a>
            </div>
        </div>
    </header>"""

# HTML Template
def create_html(title, content, filename):
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="src/css/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Montserrat:wght@400;700&family=Oswald:wght@500&display=swap" rel="stylesheet">
</head>
<body>
{get_header(filename.replace('.html', ''))}

{sidebar_content}

    <main>
        <div class="card">
            <h1>{title.split(' - ')[-1] if '-' in title else title}</h1>
            {content}
        </div>
    </main>

    <footer>
        <p>&copy; 2025 VHHI</p>
    </footer>

    <div id="chatbot-widget">
        <div class="fab">💬</div>
    </div>

    <script src="src/js/main.js"></script>
</body>
</html>"""
    with open(rf'd:\hello\aerowp\{filename}', 'w', encoding='utf-8') as f:
        f.write(html)

# 1. Update Gallery
gallery_content = ""
for i in range(1, 21):
    gallery_content += f"""
            <section id="chapter{i}" style="margin-bottom: 40px;">
                <h2 style="border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px;">Capítulo {i}</h2>
                <div class="gallery-container">
                    <figure>
                        <img src="src/assets/images/placeholder-gallery.png" alt="Imagen Capítulo {i}" style="background: #ddd; height: 150px; display: flex; align-items: center; justify-content: center;">
                        <figcaption>Imagen representativa del Capítulo {i}</figcaption>
                    </figure>
                </div>
            </section>
"""
create_html("Galería Multimedia", gallery_content, "gallery.html")

# 2. Formulas Page
formulas_content = """
            <p>Aquí encontrarás las fórmulas matemáticas y físicas fundamentales utilizadas en aeronáutica.</p>
            
            <h2>Matemáticas</h2>
            <div class="media-container">
                [Espacio para Fórmulas Matemáticas]
            </div>

            <h2>Física</h2>
            <div class="media-container">
                [Espacio para Fórmulas Físicas]
            </div>
"""
create_html("Fórmulas - Matemáticas y Física", formulas_content, "formulas.html")

# 3. Relations Page
relations_content = """
            <p>Explicación de la relación entre la materia aeronáutica y las materias fundamentales.</p>
            
            <div class="relation-grid" style="display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); margin-top: 20px;">
                <div class="relation-card" style="border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                    <h3>Lenguaje y Redacción</h3>
                    <p>Importancia de la comunicación técnica y manuales.</p>
                </div>
                <div class="relation-card" style="border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                    <h3>Matemáticas</h3>
                    <p>Cálculos de peso, balance, navegación y aerodinámica.</p>
                </div>
                <div class="relation-card" style="border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                    <h3>Física</h3>
                    <p>Principios de vuelo, fuerzas, electricidad y mecánica.</p>
                </div>
                <div class="relation-card" style="border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                    <h3>Inglés</h3>
                    <p>El idioma universal de la aviación. Manuales y comunicaciones.</p>
                </div>
            </div>
"""
create_html("Relación de Materias", relations_content, "relations.html")

print("Gallery, Formulas, and Relations pages created.")
