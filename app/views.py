import tkinter as tk
from tkinter import ttk
import database

def mostra_misurazioni(root):
    # 1. Pulisce la schermata corrente (rimuove i bottoni della Home)
    for widget in root.winfo_children():
        widget.destroy()
        
    titolo = tk.Label(root, text="Dati delle Misurazioni", font=("Helvetica", 18, "bold"))
    titolo.pack(pady=20)

    # 2. Creazione del widget Treeview richiesto dalla consegna
    colonne = ("ID", "Stazione", "Data", "Inquinante", "Valore")
    tabella = ttk.Treeview(root, columns=colonne, show="headings")
    
    # 3. Imposta le intestazioni delle colonne
    for col in colonne:
        tabella.heading(col, text=col)
        tabella.column(col, width=140)
        
    tabella.pack(pady=10, padx=20, fill="both", expand=True)

    # 4. Recupero e inserimento dati dal database
    dati = database.get_misurazioni()
    for riga in dati:
        tabella.insert("", tk.END, values=riga)