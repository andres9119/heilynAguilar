import os
from PIL import Image
import re

def convert_to_webp(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                name, ext = os.path.splitext(file_path)
                webp_path = name + '.webp'
                
                try:
                    img = Image.open(file_path)
                    img.save(webp_path, 'WebP', quality=85)
                    print(f"Converted: {file_path} -> {webp_path}")
                except Exception as e:
                    print(f"Error converting {file_path}: {e}")

def update_templates(directory):
    # Regex to find image references in templates
    # This is a bit risky but we can target common static patterns
    # e.g. {% static 'img/logo.png' %}
    pattern = re.compile(r"static\s+['\"]([^'\"]+\.(?:png|jpg|jpeg))['\"]")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = pattern.sub(lambda m: "static '" + os.path.splitext(m.group(1))[0] + ".webp'", content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated templates in: {file_path}")

if __name__ == "__main__":
    static_dir = r"c:\Users\LENOVO\Desktop\Proyectos programacion\salon_unas\static"
    templates_dir = r"c:\Users\LENOVO\Desktop\Proyectos programacion\salon_unas\templates"
    core_templates_dir = r"c:\Users\LENOVO\Desktop\Proyectos programacion\salon_unas\core\templates"
    
    print("Converting static images...")
    convert_to_webp(static_dir)
    
    print("\nUpdating templates...")
    update_templates(templates_dir)
    update_templates(core_templates_dir)
    print("\nDone!")
