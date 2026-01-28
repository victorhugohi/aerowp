import os
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def fix_chapter_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Fix the double </h3> issue from previous run
    # Previous run output: <h3>Title</h3>\nPLACEHOLDER\n</h3>
    # We want: <h3>Title</h3>\nPLACEHOLDER
    
    # Detect the bad pattern: </div></h3> where div is inside media-container?
    # Actually, looking at the previous file view:
    # <h3>1.2 Safety ...</h3>
    # <div class="media-container">...</div></h3>
    
    # The pattern to fix is `</div></h3>`. 
    # But wait, `</div>` closes the media container. So `</h3>` is hanging after it.
    # We should replace `</div></h3>` with `</div>`.
    
    # However, we must be careful not to remove valid `</div></h3>` if that ever existed (unlikely).
    # Since media-container is newly inserted, if it ends with `</div>` and is followed by `</h3>`, that `</h3>` is the extra one.
    
    content = content.replace('</div></h3>', '</div>')

    # 4. Ensure SINGLE Ver Gallery Button at the end of .card
    # (Re-verify logic from previous script to ensure we didn't duplicate if run again)
    # The previous script removed ALL buttons then added one.
    # Since we are just fixing HTML, we might not need to re-run that part if it was correct.
    # But let's be safe.
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
             f.write(content)
        print(f"Fixed HTML in {filepath}")

def main():
    # Fix Chapters 1-10
    for i in range(1, 11):
        filepath = os.path.join(ROOT_DIR, f'chapter{i}.html')
        if os.path.exists(filepath):
            fix_chapter_content(filepath)

if __name__ == "__main__":
    main()
