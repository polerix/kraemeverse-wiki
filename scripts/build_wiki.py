import os
import re
import markdown

# Directory containing the markdown files
md_dir = 'The Hoag/files'

# HTML template string
TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Kraemerverse Wiki</title>
    <link rel="stylesheet" href="../../styles.css">
</head>

<body>
    <div class="wiki-container">

        <!-- Sidebar Navigation -->
        <nav class="sidebar">
            <div class="sidebar-logo">Kraemerverse Wiki</div>
            <ul class="sidebar-nav">
                <li><a href="../../index.html#main">Main Page</a></li>
                <li><a href="../../index.html#about-author">About the Author</a></li>
                <li><a href="../../index.html#bibliography">Bibliography</a></li>
                <li><a href="../../index.html#hoag-universe">The HOAG Universe</a></li>
            </ul>

            <div class="sidebar-section">
                <h3>Directory</h3>
                <ul class="sidebar-nav">
                    <li><a href="Home.html">The Hoag Index</a></li>
                    <li><a href="../../Dark Deep/">Dark Deep Logs</a></li>
                    <li><a href="Characters-Humans-GO.html">Characters (GO)</a></li>
                    <li><a href="Ships-and-Vehicles.html">Technology</a></li>
                </ul>
            </div>
        </nav>

        <!-- Main Content Area -->
        <main class="content">
            {content}
        </main>
    </div>
</body>

</html>"""

def fix_links(match):
    text = match.group(1)
    link = match.group(2)
    
    # Ignore absolute URLs (http://, https://, mailto:, etc.)
    if re.match(r'^[a-zA-Z]+:', link):
        return f"[{text}]({link})"
        
    # Ignore simple anchor links in the same page
    if link.startswith('#'):
        return f"[{text}]({link})"
        
    # For relative links, append .html
    # Handle Links like 'Concepts#sixthsense'
    if '#' in link:
        base, hash_part = link.split('#', 1)
        return f"[{text}]({base}.html#{hash_part})"
    
    return f"[{text}]({link}.html)"

def main():
    md = markdown.Markdown(extensions=['meta', 'tables', 'fenced_code'])
    
    # Process all markdown files
    for filename in os.listdir(md_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(md_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
                
            # Replace links `[text](link)` to point to `.html` instead of `.md`
            # Note: This simple regex assumes no nested parentheses in labels/links.
            md_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', fix_links, md_content)
            
            # Convert to HTML
            html_content = md.convert(md_content)
            
            # Extract title (either from metadata or filename)
            title = filename[:-3] # Default to filename without .md
            # Simple heuristic for Title: grab the first h1
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content)
            if title_match:
                title = title_match.group(1)
                
            # Create final HTML
            final_html = TEMPLATE.format(title=title, content=html_content)
            
            out_filename = filename[:-3] + '.html'
            out_filepath = os.path.join(md_dir, out_filename)
            
            with open(out_filepath, 'w', encoding='utf-8') as f:
                f.write(final_html)
                
            print(f"Generated {out_filepath}")

if __name__ == '__main__':
    main()
