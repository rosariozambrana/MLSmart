# -*- coding: utf-8 -*-
"""
Script para quitar emojis de archivos Python (Windows compatibility)
"""
import os
import re

# Mapeo de emojis a texto
EMOJI_MAP = {
    '📊': '[Dataset]',
    '💰': '[Precio]',
    '🏠': '[Metros]',
    '🛏️': '[Habitaciones]',
    '✅': '[OK]',
    '🔧': '[Info]',
    '📈': '[Metricas]',
    '🔍': '[Feature]',
    '💾': '[Guardado]',
    '📂': '[Cargado]',
    '⚠️': '[Advertencia]',
    '🤖': '',
    '🚀': '',
    '📉': '[RMSE]',
    '⭐': '',
}

def remove_emojis(text):
    """Remueve emojis y los reemplaza con texto"""
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)

    # Remover cualquier emoji restante
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def fix_file(filepath):
    """Fix encoding de un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Quitar emojis
        new_content = remove_emojis(content)

        # Agregar encoding declaration si no existe
        if not new_content.startswith('# -*- coding:'):
            new_content = '# -*- coding: utf-8 -*-\n' + new_content

        # Guardar
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Fixed: {filepath}")
        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

# Fix todos los archivos .py en app/
for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_file(filepath)

print("\nEncoding fixed in all Python files!")
