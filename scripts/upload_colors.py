import os
import sys
import django

# Configuramos el entorno de Django para poder usar los modelos
sys.path.append(r"c:\Users\LENOVO\Desktop\Proyectos programacion\salon_unas")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salonweb.settings')
django.setup()

from inventario.models import Color

colors_data = [
    ("#000000", "Negro"),
    ("#FFFFFF", "Blanco"),
    ("#FF0000", "Rojo"),
    ("#00FF00", "Verde"),
    ("#0000FF", "Azul"),
    ("#FFFF00", "Amarillo"),
    ("#FFA500", "Naranja"),
    ("#800080", "Morado"),
    ("#FFC0CB", "Rosado"),
    ("#A52A2A", "Marrón"),
    ("#808080", "Gris"),
    ("#C0C0C0", "Plata"),
    ("#FFD700", "Dorado"),
    ("#00FFFF", "Cian"),
    ("#008080", "Verde azulado"),
    ("#000080", "Azul marino"),
    ("#F5F5F5", "Blanco humo"),
    ("#D3D3D3", "Gris claro"),
    ("#A9A9A9", "Gris oscuro"),
    ("#2F4F4F", "Gris pizarra oscuro"),
    ("#708090", "Gris pizarra"),
    ("#B0C4DE", "Azul acero claro"),
    ("#4682B4", "Azul acero"),
    ("#5F9EA0", "Azul cadete"),
    ("#6495ED", "Azul maíz"),
    ("#1E90FF", "Azul dodger"),
    ("#ADD8E6", "Azul claro"),
    ("#87CEEB", "Azul cielo"),
    ("#87CEFA", "Azul cielo claro"),
    ("#191970", "Azul medianoche"),
    ("#7B68EE", "Azul pizarra medio"),
    ("#6A5ACD", "Azul pizarra"),
    ("#483D8B", "Azul pizarra oscuro"),
    ("#4169E1", "Azul real"),
    ("#8A2BE2", "Azul violeta"),
    ("#9932CC", "Orquídea oscura"),
    ("#BA55D3", "Orquídea media"),
    ("#DA70D6", "Orquídea"),
    ("#EE82EE", "Violeta"),
    ("#FF00FF", "Magenta"),
    ("#C71585", "Rojo violeta medio"),
    ("#DB7093", "Rojo violeta pálido"),
    ("#FF1493", "Rosa profundo"),
    ("#FF69B4", "Rosa fuerte"),
    ("#FFB6C1", "Rosa claro"),
    ("#FA8072", "Salmón"),
    ("#E9967A", "Salmón oscuro"),
    ("#F08080", "Coral claro"),
    ("#CD5C5C", "Rojo indio"),
    ("#DC143C", "Carmesí"),
    ("#B22222", "Rojo fuego"),
    ("#8B0000", "Rojo oscuro"),
    ("#FF6347", "Tomate"),
    ("#FF4500", "Naranja rojo"),
    ("#FF8C00", "Naranja oscuro"),
    ("#FFDAB9", "Durazno"),
    ("#FFE4B5", "Mocasín"),
    ("#FFEFD5", "Papaya whip"),
    ("#FFF8DC", "Maíz"),
    ("#FFFACD", "Limón claro"),
    ("#FAFAD2", "Amarillo claro"),
    ("#FFFFE0", "Amarillo pálido"),
    ("#BDB76B", "Caqui oscuro"),
    ("#EEE8AA", "Caqui pálido"),
    ("#F0E68C", "Caqui"),
    ("#DAA520", "Vara de oro"),
    ("#B8860B", "Dorado oscuro"),
    ("#CD853F", "Perú"),
    ("#D2691E", "Chocolate"),
    ("#8B4513", "Marrón silla"),
    ("#A0522D", "Siena"),
    ("#DEB887", "Madera clara"),
    ("#F5DEB3", "Trigo"),
    ("#FFF5EE", "Concha de mar"),
    ("#FDF5E6", "Lino viejo"),
    ("#FAF0E6", "Lino"),
    ("#FAEBD7", "Blanco antiguo"),
    ("#FFE4C4", "Bisque"),
    ("#FFEBCD", "Almendra blanqueada"),
    ("#FFE4E1", "Rosa niebla"),
    ("#FFF0F5", "Lavanda rubor"),
    ("#E6E6FA", "Lavanda"),
    ("#D8BFD8", "Cardo"),
    ("#DDA0DD", "Ciruela"),
    ("#98FB98", "Verde pálido"),
    ("#90EE90", "Verde claro"),
    ("#00FA9A", "Verde primavera medio"),
    ("#00FF7F", "Verde primavera"),
    ("#3CB371", "Verde mar medio"),
    ("#2E8B57", "Verde mar"),
    ("#228B22", "Verde bosque"),
    ("#006400", "Verde oscuro"),
    ("#7FFF00", "Chartreuse"),
    ("#7CFC00", "Verde césped"),
    ("#ADFF2F", "Verde amarillo"),
    ("#556B2F", "Oliva oscuro"),
    ("#6B8E23", "Oliva"),
    ("#808000", "Oliva puro"),
    ("#9ACD32", "Verde amarillo medio"),
    ("#32CD32", "Verde lima"),
    ("#00FF00", "Lima"),
    ("#008000", "Verde oscuro 2"), # Cambié un Verde duplicado para que no colisionara
]

def load():
    created_count = 0
    updated_count = 0
    
    for hex_code, name in colors_data:
        # Usamos el nombre como identificador único
        color, created = Color.objects.get_or_create(
            nombre__iexact=name,
            defaults={'nombre': name.strip(), 'codigo_hex': hex_code.strip()}
        )
        if not created and color.codigo_hex != hex_code.strip():
            color.codigo_hex = hex_code.strip()
            color.save()
            updated_count += 1
            print(f"✔️ Actualizado: {name}")
        elif created:
            created_count += 1
            print(f"✨ Creado: {name}")

    print(f"\n¡Listo! {created_count} colores creados y {updated_count} actualizados correctamente en la base de datos.")

if __name__ == '__main__':
    load()
