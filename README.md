# PDF to Markdown

Convierte PDFs a Markdown de forma local y privada, sin internet.

## ¿Qué hace?

Convierte cualquier PDF a un archivo `.md` usando [Docling](https://github.com/DS4SD/docling) de IBM. Todo corre en tu máquina, ningún dato sale a servidores externos.

## Requisitos

- Python 3.11+
- GPU NVIDIA recomendada (funciona también en CPU)

## Instalación

Se recomienda usar un entorno virtual para no mezclar las dependencias de este proyecto (Docling, PyTorch, etc.) con el resto de tu instalación de Python.

\`\`\`bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

En Linux/Mac, activar con: \`source .venv/bin/activate\`

### Primera vez (requiere internet)

La primera ejecución descarga los modelos de Docling (~600MB). Requiere correr como administrador en Windows para crear los archivos de caché correctamente.

Después de esa descarga, funciona completamente offline.

## Uso

\`\`\`bash
py convertir_a_md.py
\`\`\`

1. Seleccioná el PDF de origen
2. Elegí la carpeta destino del `.md`
3. Click en **Convertir**
4. Al terminar, abrí la carpeta con el botón 📂

## Tecnologías

- [Docling](https://github.com/DS4SD/docling) — conversión de documentos
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — interfaz gráfica

## Licencia

MIT