import os
from PIL import Image

def convert_logo():
    base_dir = r"C:\Users\LENOVO\Desktop\Proyectos programacion\salon_unas"
    input_path = os.path.join(base_dir, "static", "img", "productos", "logo-marca.png")
    output_dir = os.path.join(base_dir, "static", "img", "productos")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} no existe.")
        return

    sizes = {
        "sm": 60,   # Para navbar
        "md": 150,  # Para footer
        "lg": 300   # Para general
    }

    try:
        with Image.open(input_path) as img:
            # Convertir a RGBA si no lo es para transparencia
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            
            for name, height in sizes.items():
                # Calcular ancho manteniendo aspectos
                aspect_ratio = img.width / img.height
                width = int(height * aspect_ratio)
                
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                output_path = os.path.join(output_dir, f"logo-{name}.webp")
                resized_img.save(output_path, "WEBP", quality=90)
                print(f"Generado: {output_path}")
                
    except Exception as e:
        print(f"Error durante la conversión: {e}")

if __name__ == "__main__":
    convert_logo()
