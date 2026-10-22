"""TPL3 - Editor de Imágenes (esqueleto).

Decisiones tomadas hasta ahora:
- Tema oscuro con un color de acento configurable.
- Una sola clase (EditorImagenes) que concentra la lógica.
- Sonidos con playsound3 (archivos .wav en la carpeta sounds/).
- Vista previa antes/después lado a lado, con Confirmar y Cancelar.
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

try:
    from playsound3 import playsound
except ImportError:  # la app sigue funcionando sin sonido
    playsound = None


# ---------------------------------------------------------------- utilidades
def ruta_recurso(relativa):
    """Devuelve la ruta de un recurso, tanto en el código fuente como en el .exe."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relativa)


# ------------------------------------------------------------------ la app
class EditorImagenes:
    # Paleta de colores: cambiá estos valores para personalizar tu editor.
    TEMA = {
        "fondo": "#1e1e24",
        "panel": "#2a2a33",
        "texto": "#e8e8ee",
        "acento": "#ff7a45",
    }
    FORMATOS_ABRIR = [("Imágenes", "*.jpg *.jpeg *.png *.bmp"), ("Todos", "*.*")]
    FORMATOS_GUARDAR = [("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]

    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        self.root.geometry("1000x650")
        self.root.configure(bg=self.TEMA["fondo"])

        # Estado de la aplicación (sin variables globales)
        self.historial = []          # lista de imágenes PIL
        self.indice = -1             # posición actual dentro del historial
        self.imagen_preview = None   # resultado pendiente de confirmar
        self._refs_tk = {}           # evita que Tkinter descarte las imágenes

        self._construir_menu()
        self._construir_interfaz()
        self._actualizar_estado_menu()

    # ------------------------------------------------------------ interfaz
    def _construir_menu(self):
        t = self.TEMA
        estilo = dict(bg=t["panel"], fg=t["texto"], activebackground=t["acento"],
                      activeforeground="black", tearoff=0)
        barra = tk.Menu(self.root, **estilo)

        m_archivo = tk.Menu(barra, **estilo)
        m_archivo.add_command(label="Abrir imagen...", command=self.abrir_imagen)
        m_archivo.add_command(label="Guardar como...", command=self.guardar_como)
        m_archivo.add_command(label="Enviar por correo...", command=self.enviar_correo)
        m_archivo.add_separator()
        m_archivo.add_command(label="Salir", command=self.root.destroy)
        barra.add_cascade(label="Archivo", menu=m_archivo)

        self.m_editar = tk.Menu(barra, **estilo)
        self.m_editar.add_command(label="Deshacer", command=self.deshacer)
        self.m_editar.add_command(label="Rehacer", command=self.rehacer)
        barra.add_cascade(label="Editar", menu=self.m_editar)

        m_imagen = tk.Menu(barra, **estilo)
        m_imagen.add_command(label="Voltear horizontal",
                             command=lambda: self.iniciar_vista_previa(
                                 ImageOps.mirror))
        m_imagen.add_command(label="Voltear vertical",
                             command=lambda: self.iniciar_vista_previa(
                                 ImageOps.flip))
        m_imagen.add_separator()
        m_imagen.add_command(label="Rotar 90° izquierda",
                             command=lambda: self.iniciar_vista_previa(
                                 lambda im: im.rotate(90, expand=True)))
        m_imagen.add_command(label="Rotar 90° derecha",
                             command=lambda: self.iniciar_vista_previa(
                                 lambda im: im.rotate(-90, expand=True)))
        m_imagen.add_command(label="Rotar 180°",
                             command=lambda: self.iniciar_vista_previa(
                                 lambda im: im.rotate(180)))
        m_imagen.add_separator()
        m_imagen.add_command(label="Escala de grises",
                             command=lambda: self.iniciar_vista_previa(
                                 lambda im: ImageOps.grayscale(im).convert("RGB")))
        # TODO: binarizar (umbral), recortar, brillo/contraste/saturación
        barra.add_cascade(label="Imagen", menu=m_imagen)

        m_filtros = tk.Menu(barra, **estilo)
        # TODO: elegir 3 filtros como mínimo (negativo, sepia, desenfoque...)
        m_filtros.add_command(label="(próximamente)", state="disabled")
        barra.add_cascade(label="Filtros", menu=m_filtros)

        m_ayuda = tk.Menu(barra, **estilo)
        m_ayuda.add_command(label="Acerca de", command=self.acerca_de)
        barra.add_cascade(label="Ayuda", menu=m_ayuda)

        self.root.config(menu=barra)

    def _construir_interfaz(self):
        t = self.TEMA
        # Zona donde se muestran las imágenes
        self.zona = tk.Frame(self.root, bg=t["fondo"])
        self.zona.pack(fill="both", expand=True, padx=10, pady=10)
        self.zona.columnconfigure(0, weight=1, uniform="col")
        self.zona.rowconfigure(1, weight=1)

        self.lbl_antes = tk.Label(self.zona, text="Imagen", bg=t["fondo"],
                                  fg=t["texto"])
        self.lbl_antes.grid(row=0, column=0)
        self.canvas_antes = tk.Canvas(self.zona, bg=t["panel"],
                                      highlightthickness=0)
        self.canvas_antes.grid(row=1, column=0, sticky="nsew", padx=5)

        # Estos dos solo aparecen durante la vista previa
        self.lbl_despues = tk.Label(self.zona, text="Después", bg=t["fondo"],
                                    fg=t["acento"])
        self.canvas_despues = tk.Canvas(self.zona, bg=t["panel"],
                                        highlightthickness=0)

        # Barra de confirmación (oculta hasta que haya una vista previa)
        self.barra_confirmar = tk.Frame(self.root, bg=t["fondo"])
        tk.Button(self.barra_confirmar, text="Confirmar", bg=t["acento"],
                  fg="black", command=self.confirmar).pack(side="left", padx=5)
        tk.Button(self.barra_confirmar, text="Cancelar", bg=t["panel"],
                  fg=t["texto"], command=self.cancelar).pack(side="left", padx=5)

        # Barra de estado
        self.estado = tk.Label(self.root, text="Abrí una imagen para empezar",
                               bg=t["panel"], fg=t["texto"], anchor="w")
        self.estado.pack(side="bottom", fill="x")

        # Redibujar al cambiar el tamaño de la ventana
        self.canvas_antes.bind("<Configure>", lambda e: self._redibujar())
        self.canvas_despues.bind("<Configure>", lambda e: self._redibujar())

    # ----------------------------------------------------- mostrar imágenes
    @property
    def imagen_actual(self):
        return self.historial[self.indice] if self.indice >= 0 else None

    def _dibujar(self, canvas, imagen, clave):
        """Dibuja 'imagen' dentro de 'canvas' ajustada al tamaño disponible."""
        canvas.delete("all")
        if imagen is None:
            return
        ancho, alto = max(canvas.winfo_width(), 1), max(canvas.winfo_height(), 1)
        copia = imagen.copy()
        copia.thumbnail((ancho, alto))
        self._refs_tk[clave] = ImageTk.PhotoImage(copia)
        canvas.create_image(ancho // 2, alto // 2, image=self._refs_tk[clave])

    def _redibujar(self):
        self._dibujar(self.canvas_antes, self.imagen_actual, "antes")
        if self.imagen_preview is not None:
            self._dibujar(self.canvas_despues, self.imagen_preview, "despues")

    # ------------------------------------------------------------ archivo
    def abrir_imagen(self):
        ruta = filedialog.askopenfilename(title="Abrir imagen",
                                          filetypes=self.FORMATOS_ABRIR)
        if not ruta:  # el usuario canceló el diálogo
            return
        try:
            with Image.open(ruta) as img:
                img.load()  # fuerza la lectura: detecta archivos corruptos
                imagen = img.convert("RGBA")
        except (UnidentifiedImageError, OSError):
            messagebox.showerror("Error", "El archivo no es una imagen válida "
                                          "o está dañado.")
            return
        self.cancelar()
        self.historial = [imagen]
        self.indice = 0
        self._redibujar()
        self._actualizar_estado_menu()
        self.estado.config(text=f"Cargada: {os.path.basename(ruta)}")

    def guardar_como(self):
        if not self._hay_imagen():
            return
        ruta = filedialog.asksaveasfilename(title="Guardar como",
                                            defaultextension=".png",
                                            filetypes=self.FORMATOS_GUARDAR)
        if not ruta:
            return
        imagen = self.imagen_actual
        try:
            # JPG y BMP no admiten transparencia: la quitamos para no fallar
            if ruta.lower().endswith((".jpg", ".jpeg", ".bmp")):
                imagen = imagen.convert("RGB")
            imagen.save(ruta)
            self.estado.config(text=f"Guardada en {ruta}")
        except (OSError, ValueError) as error:
            messagebox.showerror("Error", f"No se pudo guardar: {error}")

    def enviar_correo(self):
        # TODO: validar mail, comprimir si supera 25 MB (base64 pesa ~33% más),
        # leer credenciales de variables de entorno y manejar errores.
        messagebox.showinfo("Pendiente", "El envío por correo se arma en un paso próximo.")

    # ------------------------------------------- vista previa y confirmación
    def iniciar_vista_previa(self, funcion):
        """Calcula el resultado de 'funcion' y lo muestra al lado del original."""
        if not self._hay_imagen():
            return
        self.cancelar()
        self.imagen_preview = funcion(self.imagen_actual)
        self.lbl_antes.config(text="Antes")
        self.zona.columnconfigure(1, weight=1, uniform="col")
        self.lbl_despues.grid(row=0, column=1)
        self.canvas_despues.grid(row=1, column=1, sticky="nsew", padx=5)
        self.barra_confirmar.pack(before=self.estado, pady=5)
        self.root.update_idletasks()
        self._redibujar()

    def confirmar(self):
        if self.imagen_preview is None:
            return
        self._registrar(self.imagen_preview)
        self._cerrar_vista_previa()
        self.reproducir_sonido("aplicar.mp3")

    def cancelar(self):
        if self.imagen_preview is not None:
            self._cerrar_vista_previa()

    def _cerrar_vista_previa(self):
        self.imagen_preview = None
        self.lbl_despues.grid_remove()
        self.canvas_despues.grid_remove()
        self.barra_confirmar.pack_forget()
        self.lbl_antes.config(text="Imagen")
        self._redibujar()

    # ------------------------------------------------------------ historial
    def _registrar(self, imagen):
        """Agrega un cambio al historial (descarta los 'rehacer' pendientes)."""
        self.historial = self.historial[: self.indice + 1]
        self.historial.append(imagen)
        self.indice += 1
        self._actualizar_estado_menu()

    def deshacer(self):
        if self.indice > 0:
            self.cancelar()
            self.indice -= 1
            self._redibujar()
            self._actualizar_estado_menu()

    def rehacer(self):
        if self.indice < len(self.historial) - 1:
            self.cancelar()
            self.indice += 1
            self._redibujar()
            self._actualizar_estado_menu()

    def _actualizar_estado_menu(self):
        """Deshabilita Deshacer/Rehacer al llegar al principio o al final."""
        puede_deshacer = self.indice > 0
        puede_rehacer = self.indice < len(self.historial) - 1
        self.m_editar.entryconfig("Deshacer",
                                  state="normal" if puede_deshacer else "disabled")
        self.m_editar.entryconfig("Rehacer",
                                  state="normal" if puede_rehacer else "disabled")

    # --------------------------------------------------------------- sonido
    def reproducir_sonido(self, nombre):
        """Reproduce un .wav de sounds/ sin bloquear la interfaz."""
        ruta = ruta_recurso(os.path.join("sounds", nombre))
        if playsound is None or not os.path.exists(ruta):
            return
        try:
            playsound(ruta, block=False)
        except Exception:
            pass  # un problema de audio nunca debe cerrar la app

    # ------------------------------------------------------------- varios
    def _hay_imagen(self):
        if self.imagen_actual is None:
            messagebox.showwarning("Sin imagen", "Primero abrí una imagen "
                                                 "desde Archivo > Abrir.")
            return False
        return True

    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Editor de Imágenes - TPL3\nAutor: (tu nombre)")


def main():
    root = tk.Tk()
    EditorImagenes(root)
    root.mainloop()


if __name__ == "__main__":
    main()