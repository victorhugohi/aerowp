import os

# Spanish Chapters
base_dir_es = "d:\\hello\\aerowp"
chapters_es = [f"chapter{i}.html" for i in range(1, 15)]

for chapter in chapters_es:
    file_path = os.path.join(base_dir_es, chapter)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Fix Logo
        content = content.replace("<span>✈️</span> AeroIntro", "<span>✈️</span> AeroWP")
        
        # Fix Lang Switch (Ensure it points to en/chapterX.html)
        # We look for the lang-switch div and replace the link
        # This is a simple replacement assuming standard structure
        
        # Construct expected incorrect link pattern if any, or just force update
        # The current link is likely <a href="en/chapterX.html" ...>EN</a> which is correct for Spanish pages
        # But let's verify/enforce it.
        
        # Actually, let's just replace the Logo for now, as the Spanish Lang Switch seemed correct in inspection
        # "en/chapter1.html" is correct relative to "chapter1.html"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {chapter}")

# English Chapters
base_dir_en = "d:\\hello\\aerowp\\en"
chapters_en = [f"chapter{i}.html" for i in range(1, 15)]

for chapter in chapters_en:
    file_path = os.path.join(base_dir_en, chapter)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Fix Logo
        content = content.replace("<span>✈️</span> AeroIntro", "<span>✈️</span> AeroWP")
        
        # Fix Lang Switch
        # Current: <a href="../chapter1.html" ...>ES</a>
        # This is actually correct! "../chapter1.html" goes to Spanish chapter.
        # So mainly just the Logo needs fixing.
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated en/{chapter}")
