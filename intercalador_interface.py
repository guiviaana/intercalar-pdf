import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox, Listbox, SINGLE, END, Button
from PyPDF2 import PdfReader, PdfWriter
import ctypes

arquivos_pdf = []

def atualizar_lista():
    listbox.delete(0, END)
    for caminho in arquivos_pdf:
        listbox.insert(END, os.path.basename(caminho))

def drop(event):
    novos_arquivos = root.tk.splitlist(event.data)
    pdfs = [f for f in novos_arquivos if f.lower().endswith(".pdf")]
    
    if len(arquivos_pdf) + len(pdfs) > 2:
        messagebox.showwarning("Atenção", "Você pode adicionar no máximo 2 arquivos PDF.")
        return

    arquivos_pdf.extend(pdfs)
    atualizar_lista()

def remover_arquivo():
    selecionado = listbox.curselection()
    if selecionado:
        del arquivos_pdf[selecionado[0]]
        atualizar_lista()

def mover_para_cima():
    selecionado = listbox.curselection()
    if selecionado and selecionado[0] > 0:
        i = selecionado[0]
        arquivos_pdf[i - 1], arquivos_pdf[i] = arquivos_pdf[i], arquivos_pdf[i - 1]
        atualizar_lista()
        listbox.select_set(i - 1)

def mover_para_baixo():
    selecionado = listbox.curselection()
    if selecionado and selecionado[0] < len(arquivos_pdf) - 1:
        i = selecionado[0]
        arquivos_pdf[i + 1], arquivos_pdf[i] = arquivos_pdf[i], arquivos_pdf[i + 1]
        atualizar_lista()
        listbox.select_set(i + 1)

def intercalar_pdfs():
    if len(arquivos_pdf) != 2:
        messagebox.showwarning("Atenção", "Adicione exatamente 2 arquivos PDF.")
        return
    try:
        etiquetas = PdfReader(arquivos_pdf[0])
        declaracoes = PdfReader(arquivos_pdf[1])
        output = PdfWriter()

        num_paginas = min(len(etiquetas.pages), len(declaracoes.pages))

        for i in range(num_paginas):
            output.add_page(etiquetas.pages[i])
            output.add_page(declaracoes.pages[i])

        for i in range(num_paginas, len(etiquetas.pages)):
            output.add_page(etiquetas.pages[i])
        for i in range(num_paginas, len(declaracoes.pages)):
            output.add_page(declaracoes.pages[i])

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        saida_path = os.path.join(downloads_path, "intercalado.pdf")

        with open(saida_path, "wb") as f:
            output.write(f)

        messagebox.showinfo("Sucesso", f"PDF intercalado salvo com sucesso em:\n{saida_path}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface com tema escuro e transparência
root = TkinterDnD.Tk()
root.title("Intercalar PDFs - Drag & Drop")
root.geometry("520x430")
root.configure(bg="#1e1e1e")

# Transparência (somente Windows)
try:
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(ctypes.c_int(-1)))
    root.attributes("-alpha", 0.94)
except:
    pass

instrucoes = tk.Label(root, text="📝 Arraste até 2 arquivos PDF para intercalar (etiquetas e declarações)", bg="#1e1e1e", fg="white", wraplength=480)
instrucoes.pack(pady=15)

drop_area = tk.Label(root, text="🔽 Solte os arquivos aqui", bg="#2e2e2e", fg="white", relief="ridge", width=50, height=4)
drop_area.pack(pady=10)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)

listbox = Listbox(root, selectmode=SINGLE, width=55, height=5, bg="#121212", fg="white", highlightbackground="#444", selectbackground="#444")
listbox.pack(pady=10)

frame_botoes = tk.Frame(root, bg="#1e1e1e")
frame_botoes.pack(pady=5)

btn_remover = Button(frame_botoes, text="Remover", command=remover_arquivo, bg="#444", fg="white", width=10)
btn_remover.grid(row=0, column=0, padx=5)

btn_cima = Button(frame_botoes, text="⬆ Subir", command=mover_para_cima, bg="#444", fg="white", width=10)
btn_cima.grid(row=0, column=1, padx=5)

btn_baixo = Button(frame_botoes, text="⬇ Descer", command=mover_para_baixo, bg="#444", fg="white", width=10)
btn_baixo.grid(row=0, column=2, padx=5)

btn_intercalar = Button(root, text="💾 Intercalar e Salvar em Downloads", command=intercalar_pdfs, bg="#007acc", fg="white", height=2, width=40)
btn_intercalar.pack(pady=20)

root.mainloop()
