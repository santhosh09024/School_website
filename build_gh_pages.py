import os
import shutil
import re
from app import create_app

def build_static_site():
    app = create_app('development')
    client = app.test_client()

    output_dir = os.path.abspath('_site')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 1. Copy static assets (CSS, JS, images, uploads)
    static_src = os.path.join(app.root_path, 'static')
    static_dest = os.path.join(output_dir, 'static')
    shutil.copytree(static_src, static_dest)

    # 2. Add .nojekyll so GitHub Pages doesn't ignore static folders
    with open(os.path.join(output_dir, '.nojekyll'), 'w', encoding='utf-8') as f:
        f.write('')

    # Public pages to freeze
    routes = [
        '/',
        '/about',
        '/academics',
        '/faculty',
        '/admissions',
        '/student-life',
        '/notices',
        '/events',
        '/gallery',
        '/downloads',
        '/results',
        '/contact',
        '/faq',
        '/privacy-policy',
        '/terms',
        '/auth/login'
    ]

    # Repository name for GitHub Pages path prefix
    repo_name = os.environ.get('GITHUB_REPOSITORY_NAME', 'School_website')
    base_prefix = f'/{repo_name}/'

    print(f"Building static site for GitHub Pages with prefix: {base_prefix}")

    for route in routes:
        response = client.get(route)
        if response.status_code != 200:
            print(f"Warning: route {route} returned status {response.status_code}")
            continue

        html = response.get_data(as_text=True)

        # Transform root-relative paths to repository-prefixed paths for GitHub Pages
        # Examples: href="/about" -> href="/School_website/about/"
        #           src="/static/css/style.css" -> src="/School_website/static/css/style.css"
        def rewrite_url(match):
            attr = match.group(1)
            path = match.group(2)
            # Don't touch external or protocol-relative URLs
            if path.startswith('//') or path.startswith('http'):
                return match.group(0)
            
            # Format route with trailing slash if not pointing to a file
            clean_path = path.lstrip('/')
            if '.' not in os.path.basename(clean_path) and clean_path and not clean_path.endswith('/'):
                clean_path += '/'
            
            return f'{attr}="{base_prefix}{clean_path}"'

        html = re.sub(r'(href|src|action)=["\']/([^"\']*)["\']', rewrite_url, html)

        if route == '/':
            dest_file = os.path.join(output_dir, 'index.html')
        else:
            route_name = route.strip('/')
            route_dir = os.path.join(output_dir, route_name)
            os.makedirs(route_dir, exist_ok=True)
            dest_file = os.path.join(route_dir, 'index.html')

        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated: {route} -> {os.path.relpath(dest_file, output_dir)}")

    # 3. Generate 404 error page for GitHub Pages
    resp_404 = client.get('/nonexistent-page-test-404')
    html_404 = resp_404.get_data(as_text=True)
    html_404 = re.sub(r'(href|src|action)=["\']/([^"\']*)["\']', rewrite_url, html_404)
    with open(os.path.join(output_dir, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html_404)
    print("Generated: 404.html")

    print(f"\n[SUCCESS] Successfully generated static pages in: {output_dir}")

if __name__ == '__main__':
    build_static_site()
