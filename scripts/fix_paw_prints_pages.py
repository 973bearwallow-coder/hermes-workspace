#!/usr/bin/env python3
"""
Update all Paw Prints HTML pages to match the homepage style.
Fixes:
1. Heading colors: h1-h6 should use var(--color-text-dark) on inner pages, var(--color-primary) only on homepage hero
2. Nav hover color: should be var(--color-primary) (yellow) on all pages
3. Nav underline: should be var(--color-primary) (yellow) on all pages
4. Hero section: add wavy divider to pages that have hero sections
5. CTA button styling: match homepage (green bg, yellow hover)
6. Footer h4: add font-family: var(--font-heading)
7. Add paw print animation to pages missing it
8. Fix FAQ page heading color (yellow -> dark)
9. Fix Resources page heading color (yellow -> dark)
10. Fix Services page heading color consistency
11. Fix Who I Am page heading color consistency
12. Fix Contact page heading color consistency
"""

import os, re

ASSETS_DIR = "/home/tom/Desktop/paw_prints_redesign_assets/"

# Pages to update (exclude homepage which is the reference)
PAGES = [
    "paw_prints_services_rates.html",
    "paw_prints_who_i_am.html",
    "paw_prints_contact_me_v2.html",
    "paw_prints_area_serve.html",
    "paw_prints_blog.html",
    "paw_prints_download_forms.html",
    "paw_prints_faq.html",
    "paw_prints_gallery.html",
    "paw_prints_resources.html",
]

# Standardized CSS that matches the homepage
# Key fix: headings use var(--color-text-dark) not var(--color-primary) or var(--color-green)
STANDARD_CSS = """
        /* Base styles and color palette — Divi 5 palette */
        :root {
            --color-primary: #FFF386; /* Light yellow (Divi primary) */
            --color-gold: #FFD000; /* Gold */
            --color-secondary: #FFB300; /* Amber */
            --color-background-light: #FFF8E1; /* Cream */
            --color-text-dark: #3D2E25; /* Warm brown */
            --color-text-light: #FFFFFF;
            --color-border: #B4B4B8;
            --color-button-hover: #FFD000;
            --color-trust-bg: #FFF386;
            --color-green: #5CBF2A;
            --color-green-dark: #4A9E20;
            --color-tan: #8B6914;
            --font-heading: 'Lora', Georgia, serif;
            --font-body: 'Nunito', 'Helvetica Neue', sans-serif;
            --padding-section: 60px 20px;
            --max-width: 1200px;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-body);
            line-height: 1.6;
            color: var(--color-text-dark);
            background-color: var(--color-background-light);
            -webkit-font-smoothing: antialiased;
            scroll-behavior: smooth;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-heading);
            color: var(--color-text-dark);
            margin-bottom: 0.8em;
            line-height: 1.2;
        }

        h1 { font-size: 2.8em; }
        h2 { font-size: 2.2em; }
        h3 { font-size: 1.8em; }
        h4 { font-size: 1.4em; }

        p {
            margin-bottom: 1em;
        }

        a {
            color: var(--color-green);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        a:hover {
            color: var(--color-secondary);
        }

        .container {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Buttons — matching homepage */
        .btn {
            display: inline-block;
            background-color: var(--color-green);
            color: var(--color-text-light);
            padding: 14px 28px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1em;
            text-align: center;
            transition: background-color 0.2s ease, transform 0.2s ease;
            cursor: pointer;
            border: none;
        }

        .btn:hover {
            background-color: var(--color-green-dark);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(92,191,42,0.35);
        }

        /* Header — matching homepage */
        header {
            background-color: var(--color-text-light);
            padding: 15px 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            position: relative;
            top: 0;
            z-index: 1000;
            overflow: hidden;
        }

        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .logo {
            font-family: var(--font-heading);
            font-size: 1.8em;
            color: var(--color-green);
            font-weight: 700;
            white-space: nowrap;
        }

        .logo img {
            max-height: 50px;
            vertical-align: middle;
            margin-right: 10px;
        }

        nav ul {
            list-style: none;
            display: flex;
        }

        nav ul li {
            margin-left: 30px;
        }

        nav ul a {
            color: var(--color-text-dark);
            font-weight: 600;
            font-size: 0.95em;
            position: relative;
        }

        nav ul a:hover {
            color: var(--color-primary);
        }

        nav ul a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            display: block;
            margin-top: 5px;
            right: 0;
            background: var(--color-primary);
            transition: width 0.3s ease;
        }

        nav ul a:hover::after {
            width: 100%;
            left: 0;
            background: var(--color-primary);
        }

        .nav-cta {
            background: var(--color-primary);
            color: var(--color-text-dark);
            border: none;
            border-radius: 50px;
            padding: 0.55rem 1.5rem;
            font-family: var(--font-body);
            font-weight: 800;
            font-size: 0.85rem;
            letter-spacing: 0.3px;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-block;
            white-space: nowrap;
        }
        .nav-cta:hover {
            background: var(--color-gold);
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(255,231,74,0.5);
        }

        .menu-toggle {
            display: none;
            cursor: pointer;
        }

        .contact-phone {
            font-family: var(--font-heading);
            font-size: 1.2em;
            color: var(--color-green);
            font-weight: 700;
            white-space: nowrap;
        }

        /* Hero Banner — yellow gradient matching homepage */
        .hero, .hero-banner {
            background: linear-gradient(160deg, #FFF386 0%, #FFD000 60%, #FFB300 100%);
            color: var(--color-text-dark);
            text-align: center;
            padding: 80px 20px 100px;
            position: relative;
        }

        .hero h1, .hero-banner h1 {
            color: var(--color-text-dark);
            font-size: 3em;
            margin-bottom: 15px;
            line-height: 1.2;
        }

        .hero p, .hero-banner p {
            color: #5A4A3A;
            font-size: 1.3em;
            margin-bottom: 30px;
            line-height: 1.5;
        }

        /* Wavy bottom divider */
        .hero-wave {
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            overflow: hidden;
            line-height: 0;
        }
        .hero-wave svg {
            display: block;
            width: 100%;
            height: 60px;
        }
        .hero-wave svg path {
            fill: var(--color-text-light);
        }

        /* CTA Section — green gradient matching homepage */
        .secondary-cta, .cta-banner {
            background: linear-gradient(180deg, #4A9E20 0%, #3A8018 100%);
            color: var(--color-text-light);
            padding: 80px 20px;
            text-align: center;
            position: relative;
            z-index: 50;
        }

        .secondary-cta h2, .cta-banner h2 {
            color: var(--color-primary);
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        .secondary-cta p, .cta-banner p {
            font-size: 1.2em;
            max-width: 700px;
            margin: 0 auto 30px auto;
        }

        .secondary-cta .btn, .cta-banner .btn {
            background-color: var(--color-primary);
            color: var(--color-text-dark);
        }

        .secondary-cta .btn:hover, .cta-banner .btn:hover {
            background-color: var(--color-gold);
            color: var(--color-text-dark);
            box-shadow: 0 6px 20px rgba(255,208,0,0.35);
        }

        /* Footer — dark brown matching homepage */
        footer {
            background-color: var(--color-text-dark);
            color: var(--color-background-light);
            padding: 50px 0 20px 0;
            font-size: 0.9em;
        }

        footer .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }

        footer h4 {
            color: var(--color-text-light);
            margin-bottom: 15px;
            font-family: var(--font-heading);
        }

        footer ul {
            list-style: none;
        }

        footer ul li {
            margin-bottom: 10px;
        }

        footer ul li a {
            color: var(--color-background-light);
            transition: color 0.3s ease;
        }

        footer ul li a:hover {
            color: var(--color-primary);
        }

        .social-media-links {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .social-media-links a {
            color: var(--color-background-light);
            font-size: 1.5em;
            transition: color 0.3s ease;
        }

        .social-media-links a:hover {
            color: var(--color-primary);
        }

        .footer-bottom {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.85em;
        }

        /* Paw Print Animation */
        .paw-print-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 50;
        }

        .paw-print {
            position: absolute;
            width: 28px;
            height: 28px;
            opacity: 0;
            animation: paw-step 1.6s ease-in-out 1 forwards;
            background-image: url('images/paw-print.svg');
            background-size: contain;
            background-repeat: no-repeat;
            filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3));
        }

        @keyframes paw-step {
            0% { opacity: 0; transform: scale(0.2); }
            15% { opacity: 0.85; transform: scale(1); }
            50% { opacity: 0.85; transform: scale(1); }
            75% { opacity: 0; transform: scale(0.4); }
            100% { opacity: 0; transform: scale(0.2); }
        }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            nav ul {
                display: none;
                flex-direction: column;
                width: 100%;
                text-align: center;
            }

            nav ul.active {
                display: flex;
            }

            nav ul li {
                margin: 10px 0;
            }

            .menu-toggle {
                display: block;
                cursor: pointer;
            }

            .contact-phone {
                margin-left: 0;
                margin-top: 10px;
            }

            .hero h1, .hero-banner h1 {
                font-size: 2.2em;
            }
        }
"""

def fix_page(filename):
    filepath = os.path.join(ASSETS_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # 1. Replace the entire <style> block in <head> with our standard CSS
    # Find the <style> tag after <link rel="stylesheet" href="css/pp-theme.css"> or standalone
    # Pattern: everything from <style> to the closing </style> in the head section
    
    # First, check if page links to pp-theme.css
    has_theme_css = 'css/pp-theme.css' in content
    
    # Replace the inline <style>...</style> block
    # We need to be careful to only replace the first <style> block (in head)
    style_pattern = r'<style>.*?</style>'
    new_style = '<style>' + STANDARD_CSS + '</style>'
    content = re.sub(style_pattern, new_style, content, count=1, flags=re.DOTALL)
    
    # 2. Fix heading colors: change h1-h6 color from var(--color-primary) or var(--color-green) to var(--color-text-dark)
    # (already handled by the CSS replacement above, but let's also fix any inline styles)
    
    # 3. Fix nav hover colors: ensure nav ul a:hover uses var(--color-primary)
    # (already handled by CSS replacement)
    
    # 4. Fix nav underline: ensure nav ul a::after uses var(--color-primary)  
    # (already handled by CSS replacement)
    
    # 5. Fix footer h4 to include font-family: var(--font-heading)
    # (already handled by CSS replacement)
    
    # 6. Fix CTA sections: ensure .secondary-cta and .cta-banner match homepage
    # (already handled by CSS replacement)
    
    # 7. Fix hero sections: ensure .hero and .hero-banner match homepage
    # (already handled by CSS replacement)
    
    # 8. Add wavy divider to hero sections that don't have it
    if 'hero-wave' not in content and ('class="hero"' in content or 'class="hero-banner"' in content):
        # Find the end of the hero content (before closing </section> or </div>)
        # Add wave SVG after the hero-content div
        wave_svg = '''
        <!-- Wavy bottom divider -->
        <div class="hero-wave">
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"></path>
            </svg>
        </div>'''
        # Insert before the closing </section> of hero
        content = re.sub(
            r'(<div class="hero-content">.*?</div>)\s*(</section>)',
            r'\1' + wave_svg + r'\n\2',
            content,
            count=1,
            flags=re.DOTALL
        )
    
    # 9. Add paw print animation to header if missing
    if 'paw-print-container' not in content:
        paw_prints = '''
        <div class="paw-print-container">
            <div class="paw-print" style="left: -3%; top: 15%; animation-delay: 0s;"></div>
            <div class="paw-print" style="left: 5%; top: 8%; animation-delay: 0.25s;"></div>
            <div class="paw-print" style="left: 13%; top: 15%; animation-delay: 0.5s;"></div>
            <div class="paw-print" style="left: 21%; top: 8%; animation-delay: 0.75s;"></div>
            <div class="paw-print" style="left: 29%; top: 15%; animation-delay: 1.0s;"></div>
            <div class="paw-print" style="left: 37%; top: 8%; animation-delay: 1.25s;"></div>
            <div class="paw-print" style="left: 45%; top: 15%; animation-delay: 1.5s;"></div>
            <div class="paw-print" style="left: 53%; top: 8%; animation-delay: 1.75s;"></div>
            <div class="paw-print" style="left: 61%; top: 15%; animation-delay: 2.0s;"></div>
            <div class="paw-print" style="left: 69%; top: 8%; animation-delay: 2.25s;"></div>
            <div class="paw-print" style="left: 77%; top: 15%; animation-delay: 2.5s;"></div>
            <div class="paw-print" style="left: 85%; top: 8%; animation-delay: 2.75s;"></div>
            <div class="paw-print" style="left: 93%; top: 15%; animation-delay: 3.0s;"></div>
            <div class="paw-print" style="left: 101%; top: 8%; animation-delay: 3.25s;"></div>
        </div>'''
        # Insert before closing </header>
        content = content.replace('</header>', paw_prints + '\n    </header>')
    
    # 10. Fix specific page issues:
    
    # FAQ page: fix accordion header to use green bg with white text
    if filename == 'paw_prints_faq.html':
        # Fix the accordion header color
        content = content.replace(
            '.accordion-header {',
            '.accordion-header {\n            background-color: var(--color-green);\n            color: var(--color-text-light);'
        )
    
    # Gallery page: fix broken var reference
    if filename == 'paw_prints_gallery.html':
        content = content.replace('var(--color-light-text)', 'var(--color-text-light)')
    
    # Resources page: fix heading color
    if filename == 'paw_prints_resources.html':
        # Already fixed by CSS replacement
        pass
    
    # 11. Fix double "LLC" in title
    content = content.replace('Paw Prints Pet Services LLC LLC', 'Paw Prints Pet Services LLC')
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Updated {filename}")
    else:
        print(f"- No changes needed for {filename}")

for page in PAGES:
    fix_page(page)

print("\nDone! All pages updated to match homepage style.")
