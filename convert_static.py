"""
Utility script to convert static file references in HTML templates.

This script walks through a folder of HTML templates and converts static file
references (CSS, JS, images) to use Django's {% static %} template tag.
It also adds the {% load static %} tag if not present.
"""

import re
import os


def convert_all_templates(folder):
    """
    Convert static file references in all HTML templates within a folder.

    Args:
        folder (str): The root folder to search for HTML files.
    """
    for root, _, files in os.walk(folder):  # Walk through all directories
        for f in files:
            if f.endswith(".html"):  # Process only HTML files
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Convert href attributes for CSS, JS, HTML files
                content = re.sub(
                    r'href="([^"]+\.(css|js|html))"',
                    lambda m: f'href="{{% static \'{m.group(1)}\' %}}"',
                    content
                )
                # Convert src attributes for JS, CSS, images
                content = re.sub(
                    r'src="([^"]+\.(js|css|png|jpg|jpeg|gif|svg|webp))"',
                    lambda m: f'src="{{% static \'{m.group(1)}\' %}}"',
                    content
                )

                # Add {% load static %} tag if not present
                if "{% load static %}" not in content:
                    content = "{% load static %}\n" + content

                # Write the modified content back
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)
                print(f"✅ fixed: {path}")

# Usage: Convert templates in the 'templates' folder
convert_all_templates("templates")
