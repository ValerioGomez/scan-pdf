import tkinter as tk
from tkinter import filedialog, messagebox

import PyPDF2
import os

import subprocess

archivo_amberso = ""
archivo_reverso = ""

def seleccionar_archivo(tipo):
    global archivo_amberso, archivo_reverso
    archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if archivo:
        if tipo == "amberso":
            archivo_amberso = archivo
            label_amberso.config(text=f"Seleccionado: {os.path.basename(archivo)}")
        else:
            archivo_reverso = archivo
            label_reverso.config(text=f"Seleccionado: {os.path.basename(archivo)}")

def combinar_pdfs():
    global archivo_amberso, archivo_reverso

    if not archivo_amberso or not archivo_reverso:
        messagebox.showerror("Error", "Debes seleccionar ambos archivos PDF.")
        return

    try:
        pdf_amberso = PyPDF2.PdfReader(archivo_amberso)
        pdf_reverso = PyPDF2.PdfReader(archivo_reverso)
        pdf_salida = PyPDF2.PdfWriter()

        if len(pdf_amberso.pages) != len(pdf_reverso.pages):
            messagebox.showerror("Error", "Los PDFs tienen diferente número de páginas.")
            return

        for i in range(len(pdf_amberso.pages)):
            pdf_salida.add_page(pdf_amberso.pages[i])
            pdf_salida.add_page(pdf_reverso.pages[len(pdf_reverso.pages) - 1 - i]) 

        directorio = os.path.dirname(archivo_amberso)
        archivo_salida = os.path.join(directorio, "Folleto_Combinado.pdf")
        with open(archivo_salida, "wb") as salida:
            pdf_salida.write(salida)

        messagebox.showinfo("Éxito", f"PDF generado: {archivo_salida}")

        if os.name == "nt":  # Windows
            os.startfile(directorio)
        else:  # Linux/Mac
            subprocess.Popen(["xdg-open", directorio])

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema: {e}")

root = tk.Tk()
root.title("Fusionar Folleto PDF")
root.geometry("400x250")

label_amberso = tk.Label(root, text="No se ha seleccionado el anverso", wraplength=300)
label_amberso.pack(pady=5)
btn_amberso = tk.Button(root, text="Subir Anverso", command=lambda: seleccionar_archivo("amberso"))
btn_amberso.pack(pady=5)

label_reverso = tk.Label(root, text="No se ha seleccionado el reverso", wraplength=300)
label_reverso.pack(pady=5)
btn_reverso = tk.Button(root, text="Subir Reverso", command=lambda: seleccionar_archivo("reverso"))
btn_reverso.pack(pady=5)

btn_iniciar = tk.Button(root, text="Iniciar", command=combinar_pdfs, bg="green", fg="white")
btn_iniciar.pack(pady=10)

root.mainloop()
