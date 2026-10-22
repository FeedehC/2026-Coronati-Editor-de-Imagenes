# Editor de Imágenes

Aplicación de escritorio con interfaz gráfica para abrir una imagen, transformarla y guardarla. Es una versión simplificada de un editor tipo Photoshop, hecha en Python con Tkinter. Cada transformación muestra una **vista previa antes/después** que se puede **confirmar o cancelar** antes de aplicarse.

> **Estado del proyecto:** versión en desarrollo (TPL3). Las funciones marcadas con 🚧 todavía no están disponibles.

---

## 1. Instalación

### Ejecutable (.exe)

🚧 **En proceso.** Todavía no hay un ejecutable generado. Cuando esté listo, la instalación será descargar el `.exe` desde la sección *Releases* del repositorio y abrirlo, sin necesidad de instalar Python.

### Mientras tanto: ejecutar desde el código fuente

Requisitos: **Python 3.9 o superior** (Tkinter viene incluido con el instalador oficial de Python).

```bash
# 1. Clonar o descargar el repositorio
git clone <URL-DEL-REPOSITORIO>
cd <carpeta-del-proyecto>

# 2. Instalar las dependencias
pip install pillow playsound3

# 3. Ejecutar
python main.py
```

**Sonidos (opcional):** la aplicación busca los archivos `.wav` en la carpeta `sounds/`, al lado de `main.py`. Si la carpeta o el archivo no existen, la aplicación funciona igual, solo que sin sonido. Actualmente se usa `sounds/aplicar.wav`, que suena al confirmar una transformación.

---

## 2. Guía de uso rápida

1. **Abrí una imagen:** menú **Archivo → Abrir imagen...** y elegí un archivo `.jpg`, `.png` o `.bmp` de tu computadora.
2. **Elegí una transformación:** en el menú **Imagen** seleccioná la que quieras aplicar (por ejemplo, *Escala de grises*).
3. **Mirá la vista previa:** la ventana se divide en dos. A la izquierda queda la imagen original (*Antes*) y a la derecha el resultado (*Después*).
4. **Decidí:** presioná **Confirmar** para aplicar el cambio, o **Cancelar** para descartarlo y volver a la imagen original.
5. **Repetí** con tantas transformaciones como quieras. Con **Editar → Deshacer** y **Editar → Rehacer** podés moverte por el historial de cambios.
6. **Guardá el resultado:** **Archivo → Guardar como...** y elegí el formato (PNG, JPEG o BMP).

---

## 3. Características

### Archivo

| Opción | Descripción |
|---|---|
| Abrir imagen | Carga una imagen desde cualquier carpeta del sistema. Formatos: JPG, JPEG, PNG y BMP. Si el archivo está dañado o no es una imagen, muestra un mensaje de error en lugar de cerrarse. |
| Guardar como | Guarda la imagen actual en PNG, JPEG o BMP. Como JPEG y BMP no admiten transparencia, esta se elimina automáticamente al guardar en esos formatos. |
| Enviar por correo | 🚧 En desarrollo. |
| Salir | Cierra la aplicación. |

### Editar

| Opción | Descripción |
|---|---|
| Deshacer | Vuelve a la versión anterior de la imagen. Se deshabilita al llegar al estado original. |
| Rehacer | Recupera un cambio deshecho. Se deshabilita cuando no hay cambios para rehacer. Si aplicás una transformación nueva después de deshacer, los cambios que se podían rehacer se descartan. |

### Imagen: transformaciones

Todas pasan por la vista previa con confirmación.

| Transformación | Descripción |
|---|---|
| Voltear horizontal | Espeja la imagen de izquierda a derecha. |
| Voltear vertical | Espeja la imagen de arriba hacia abajo. |
| Rotar 90° izquierda | Gira la imagen un cuarto de vuelta en sentido antihorario. |
| Rotar 90° derecha | Gira la imagen un cuarto de vuelta en sentido horario. |
| Rotar 180° | Da vuelta la imagen por completo. |
| Escala de grises | Convierte la imagen a tonos de gris. |
| Binarizar (umbral) | 🚧 En desarrollo. |
| Recortar | 🚧 En desarrollo. |
| Brillo, contraste y saturación | 🚧 En desarrollo. |

### Filtros

🚧 **En desarrollo.** El menú ya existe, pero los filtros todavía no están implementados. Esta sección se completará con cada filtro y su descripción a medida que se sumen.

### Otras características

- **Tema oscuro** con un color de acento personalizable: los colores están en el diccionario `TEMA` al comienzo de la clase `EditorImagenes` en `main.py`.
- **Vista previa lado a lado** que se ajusta al tamaño de la ventana.
- **Sonidos** al confirmar una transformación, sin congelar la interfaz.
- **Historial de cambios** completo durante la sesión.

---

## 4. Referencias

### Tecnologías utilizadas

- [Python](https://www.python.org/): lenguaje de programación.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): interfaz gráfica.
- [Pillow](https://pillow.readthedocs.io/): carga, procesamiento y guardado de imágenes.
- [playsound3](https://pypi.org/project/playsound3/): reproducción de sonidos.
- [PyInstaller](https://pyinstaller.org/): generación del `.exe` (planificado).

### Links útiles

- [Documentación de Pillow: ImageOps](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html)
- [Documentación de Pillow: ImageEnhance](https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html)
- [Documentación de Pillow: ImageFilter](https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html)
- [Tkinter: filedialog](https://docs.python.org/3/library/dialog.html#native-file-dialogs)

---

**Autor:** (tu nombre) · **Materia:** (materia / curso) · **Año:** 2026
