import unittest
import os
import re
from urllib.parse import unquote

class TestSiteIntegrity(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.en_dir = os.path.join(self.root_dir, 'en')

    def test_chapter_files_exist(self):
        """Verify that all 20 chapter files exist in both languages."""
        for i in range(1, 21):
            # Spanish
            es_path = os.path.join(self.root_dir, f'chapter{i}.html')
            self.assertTrue(os.path.exists(es_path), f"Missing Spanish chapter {i}: {es_path}")
            
            # English
            en_path = os.path.join(self.en_dir, f'chapter{i}.html')
            self.assertTrue(os.path.exists(en_path), f"Missing English chapter {i}: {en_path}")

    def test_essential_pages_exist(self):
        """Verify essential pages exist."""
        pages = ['index.html', 'about.html', 'contact.html', 'gallery.html', 'topics.html', 'carrera.html']
        for page in pages:
            es_path = os.path.join(self.root_dir, page)
            self.assertTrue(os.path.exists(es_path), f"Missing essential page: {es_path}")
            
            # English check (assuming strict mirroring)
            if page != 'index.html': # English index might be index.html or separate
                 en_path = os.path.join(self.en_dir, page)
                 self.assertTrue(os.path.exists(en_path), f"Missing English essential page: {en_path}")

    def test_links_validity(self):
        """
        Crawl all HTML files and verify that local hrefs point to existing files.
        """
        for dirpath, _, filenames in os.walk(self.root_dir):
            if '.git' in dirpath or '.vscode' in dirpath or '__pycache__' in dirpath:
                continue

            for filename in filenames:
                if not filename.endswith('.html'):
                    continue
                
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all hrefs
                # Simple regex, might miss some edge cases but good for static site
                links = re.findall(r'href=["\'](.*?)["\']', content)
                
                for link in links:
                    if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
                        continue
                    
                    # Resolve relative links
                    # If link starts with /, it's relative to root (rare in this static setup but possible)
                    # Otherwise relative to current file
                    
                    if link.startswith('/'):
                        # Assuming root is self.root_dir
                        target_path = os.path.join(self.root_dir, link.lstrip('/'))
                    else:
                        target_path = os.path.join(dirpath, link)
                    
                    # Remove anchor # if present
                    if '#' in target_path:
                        target_path = target_path.split('#')[0]
                        
                    # Handle URL decoding (e.g. %20 -> space) although unlikely in filenames here
                    target_path = unquote(target_path)

                    # Check existence
                    if not os.path.exists(target_path) and not os.path.isdir(target_path):
                         # Try simpler check for directory index? No, let's just fail.
                         self.fail(f"Broken link in {filepath}: {link} -> {target_path} does not exist")

    def test_title_tags_present(self):
        """Verify all HTML files have a non-empty title tag."""
        for dirpath, _, filenames in os.walk(self.root_dir):
            if '.git' in dirpath or 'node_modules' in dirpath:
                continue
            for filename in filenames:
                if filename.endswith('.html'):
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                    self.assertTrue(match, f"Missing <title> tag in {filepath}")
                    self.assertTrue(match.group(1).strip(), f"Empty <title> tag in {filepath}")

if __name__ == '__main__':
    unittest.main()
