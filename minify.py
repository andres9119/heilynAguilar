import os
import re

def minify(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'/\*.*?\*/', '', c, flags=re.DOTALL)
    c = re.sub(r'\s+', ' ', c)
    c = re.sub(r'\s*([:;{},])\s*', r'\1', c)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c.strip())

minify('static/css/estilos.css')
minify('static/css/tienda.css')
print("CSS minified successfully")
