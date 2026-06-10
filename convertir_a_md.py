import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

import customtkinter as ctk
from tkinter import filedialog
import threading
import subprocess

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF a Markdown")
        self.geometry("550x420")
        self.resizable(False, False)

        self.pdf_path = ""
        self.destino_path = ""

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="PDF → Markdown", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.pack(pady=(30, 20))

        # PDF origen
        self.frame_pdf = ctk.CTkFrame(self)
        self.frame_pdf.pack(fill="x", padx=30, pady=5)
        self.label_pdf = ctk.CTkLabel(self.frame_pdf, text="Sin PDF seleccionado", anchor="w")
        self.label_pdf.pack(side="left", padx=10, expand=True, fill="x")
        self.btn_pdf = ctk.CTkButton(self.frame_pdf, text="Seleccionar PDF", width=150, command=self.seleccionar_pdf)
        self.btn_pdf.pack(side="right", padx=10, pady=10)

        # Destino
        self.frame_destino = ctk.CTkFrame(self)
        self.frame_destino.pack(fill="x", padx=30, pady=5)
        self.label_destino = ctk.CTkLabel(self.frame_destino, text="Sin carpeta seleccionada", anchor="w")
        self.label_destino.pack(side="left", padx=10, expand=True, fill="x")
        self.btn_destino = ctk.CTkButton(self.frame_destino, text="Carpeta destino", width=150, command=self.seleccionar_destino)
        self.btn_destino.pack(side="right", padx=10, pady=10)

        # Botón convertir
        self.btn_convertir = ctk.CTkButton(self, text="Convertir", height=45, font=ctk.CTkFont(size=16, weight="bold"), command=self.convertir)
        self.btn_convertir.pack(padx=30, pady=20, fill="x")

        # Progreso
        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(padx=30, fill="x")
        self.progress.set(0)

        # Log
        self.log = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13))
        self.log.pack(pady=10)

        # Botón abrir carpeta (oculto al inicio)
        self.btn_abrir = ctk.CTkButton(self, text="📂 Abrir carpeta", command=self.abrir_carpeta)
        self.btn_abrir.pack(padx=30, fill="x")
        self.btn_abrir.pack_forget()

    def seleccionar_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path = path
            nombre = os.path.basename(path)
            self.label_pdf.configure(text=nombre)
            self.btn_abrir.pack_forget()
            self.progress.set(0)
            self.log.configure(text="")

    def seleccionar_destino(self):
        path = filedialog.askdirectory()
        if path:
            self.destino_path = path
            self.label_destino.configure(text=path)

    def convertir(self):
        if not self.pdf_path:
            self.log.configure(text="⚠️ Seleccioná un PDF primero.")
            return
        if not self.destino_path:
            self.log.configure(text="⚠️ Seleccioná una carpeta destino.")
            return

        self.btn_convertir.configure(state="disabled")
        self.btn_abrir.pack_forget()
        self.progress.set(0)
        self.log.configure(text="Convirtiendo...")
        threading.Thread(target=self._convertir_hilo, daemon=True).start()

    def _convertir_hilo(self):
        try:
            from docling.document_converter import DocumentConverter

            self.progress.start()
            converter = DocumentConverter()
            result = converter.convert(self.pdf_path)
            md = result.document.export_to_markdown()

            nombre = os.path.splitext(os.path.basename(self.pdf_path))[0] + ".md"
            salida = os.path.join(self.destino_path, nombre)
            with open(salida, "w", encoding="utf-8") as f:
                f.write(md)

            self.progress.stop()
            self.progress.set(1)
            self.log.configure(text="✅ Listo! Guardado en: " + nombre)
            self.btn_abrir.pack(padx=30, fill="x")

        except Exception as e:
            self.progress.stop()
            self.progress.set(0)
            self.log.configure(text=f"❌ Error: {str(e)[:60]}")
        finally:
            self.btn_convertir.configure(state="normal")

    def abrir_carpeta(self):
        subprocess.Popen(f'explorer "{self.destino_path}"')

if __name__ == "__main__":
    app = App()
    app.mainloop()