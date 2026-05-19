import tkinter as tk
from tkinter import ttk, messagebox
import database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def crea_barra_navigazione(root, callback_cambio_schermata):
    """Crea un menu superiore fisso per spostarsi tra le sezioni del progetto."""
    frame_nav = tk.Frame(root, bg="#2c3e50", height=40)
    frame_nav.pack(side="top", fill="x")
    
    pulsanti = [
        ("Home", lambda: callback_cambio_schermata(schermata_home)),
        ("Misurazioni (CRUD)", lambda: callback_cambio_schermata(schermata_misurazioni)),
        ("Grafici Analisi", lambda: callback_cambio_schermata(schermata_grafici)),
        ("Superamenti UE", lambda: callback_cambio_schermata(schermata_superamenti)),
        ("Mappa Stazioni", lambda: callback_cambio_schermata(schermata_stazioni)),
        ("Pannello AI", lambda: callback_cambio_schermata(schermata_ai))
    ]
    
    for testo, comando in pulsanti:
        btn = tk.Button(frame_nav, text=testo, command=comando, bg="#34495e", fg="white", 
                        relief="flat", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        btn.pack(side="left", padx=2, pady=2)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1abc9c"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))

def pulisci_schermata(container):
    for widget in container.winfo_children():
        widget.destroy()

# ================= SCHERMATA: HOME =================
def schermata_home(container):
    pulisci_schermata(container)
    
    lbl_titolo = tk.Label(container, text="AIRE — Monitoraggio Aria Milano", font=("Helvetica", 22, "bold"), fg="#2c3e50")
    lbl_titolo.pack(pady=30)
    
    info_testo = (
        "Applicazione Desktop interna per l'analisi della qualità dell'aria.\n\n"
        "Utilizzare la barra di navigazione superiore per accedere alle funzionalità:\n"
        "• Consultare e modificare i record tramite il pannello CRUD.\n"
        "• Visualizzare grafici temporali sull'andamento degli inquinanti.\n"
        "• Verificare le anomalie e i superamenti delle soglie critiche UE.\n"
        "• Esaminare i dati di localizzazione delle stazioni di rilevamento."
    )
    lbl_info = tk.Label(container, text=info_testo, font=("Helvetica", 12), justify="left")
    lbl_info.pack(pady=20, padx=40)

# ================= SCHERMATA: CRUD MISURAZIONI =================
def schermata_misurazioni(container):
    pulisci_schermata(container)
    
    # Area Filtri
    frame_filtri = tk.LabelFrame(container, text=" Filtri di Ricerca ", font=("Helvetica", 10, "bold"))
    frame_filtri.pack(fill="x", padx=15, pady=5)
    
    tk.Label(frame_filtri, text="ID Stazione:").grid(row=0, column=0, padx=5, pady=5)
    entry_f_staz = tk.Entry(frame_filtri, width=8)
    entry_f_staz.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame_filtri, text="Inquinante:").grid(row=0, column=2, padx=5, pady=5)
    entry_f_inq = tk.Entry(frame_filtri, width=8)
    entry_f_inq.grid(row=0, column=3, padx=5, pady=5)
    
    btn_applica = tk.Button(frame_filtri, text="Filtra", bg="#3498db", fg="white",
                            command=lambda: applica_filtri())
    btn_applica.grid(row=0, column=4, padx=15, pady=5)

    # Tabella Dati (Treeview)
    colonne = ("ID", "Stazione", "Data", "Inquinante", "Valore")
    tabella = ttk.Treeview(container, columns=colonne, show="headings", height=12)
    for col in colonne:
        tabella.heading(col, text=col)
        tabella.column(col, width=120, anchor="center")
    tabella.pack(fill="both", expand=True, padx=15, pady=5)

    def applica_filtri():
        for item in tabella.get_children():
            tabella.delete(item)
        dati = database.get_misurazioni(entry_f_staz.get(), entry_f_inq.get())
        for riga in dati:
            tabella.insert("", tk.END, values=riga)
            
    applica_filtri()

    # Form Inserimento Nuovo Record
    frame_add = tk.LabelFrame(container, text=" Inserisci Nuova Misurazione ", font=("Helvetica", 10, "bold"))
    frame_add.pack(fill="x", padx=15, pady=5)
    
    tk.Label(frame_add, text="Stazione ID:").grid(row=0, column=0, padx=5, pady=5)
    entry_staz = tk.Entry(frame_add, width=10)
    entry_staz.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame_add, text="Data (AAAA-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
    entry_data = tk.Entry(frame_add, width=12)
    entry_data.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(frame_add, text="Inquinante:").grid(row=0, column=4, padx=5, pady=5)
    entry_inq = tk.Entry(frame_add, width=10)
    entry_inq.grid(row=0, column=5, padx=5, pady=5)
    
    tk.Label(frame_add, text="Valore:").grid(row=0, column=6, padx=5, pady=5)
    entry_val = tk.Entry(frame_add, width=10)
    entry_val.grid(row=0, column=7, padx=5, pady=5)
    
    def esegui_inserimento():
        if database.inserisci_misurazione(entry_staz.get(), entry_data.get(), entry_inq.get(), entry_val.get()):
            messagebox.showinfo("Successo", "Misurazione memorizzata!")
            applica_filtri()
        else:
            messagebox.showerror("Errore", "Parametri non validi o ID errato.")
            
    btn_add = tk.Button(frame_add, text="Salva", bg="#2ecc71", fg="white", command=esegui_inserimento)
    btn_add.grid(row=0, column=8, padx=10, pady=5)

    # Pulsanti di Azione Riga (Modifica / Elimina)
    frame_azioni = tk.Frame(container)
    frame_azioni.pack(pady=5)
    
    def apri_popup_modifica():
        selezione = tabella.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona prima una riga.")
            return
        valori = tabella.item(selezione[0])['values']
        
        popup = tk.Toplevel(container)
        popup.title("Modifica Record")
        popup.geometry("300x250")
        
        tk.Label(popup, text="Nuovo Valore Inquinante:").pack(pady=10)
        entry_nuovo_val = tk.Entry(popup)
        entry_nuovo_val.insert(0, valori[4])
        entry_nuovo_val.pack()
        
        def conferma_modifica():
            if database.modifica_misurazione(valori[0], valori[1], valori[2], valori[3], entry_nuovo_val.get()):
                messagebox.showinfo("Successo", "Record modificato.")
                popup.destroy()
                applica_filtri()
            else:
                messagebox.showerror("Errore", "Impossibile aggiornare.")
                
        tk.Button(popup, text="Aggiorna", bg="#f1c40f", command=conferma_modifica).pack(pady=15)

    def esegui_eliminazione():
        selezione = tabella.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona prima una riga.")
            return
        valori = tabella.item(selezione[0])['values']
        if messagebox.askyesno("Conferma", "Eliminare definitivamente questa misurazione?"):
            database.elimina_misurazione(valori[0])
            applica_filtri()

    tk.Button(frame_azioni, text="Modifica Riga Selezionata", bg="#f1c40f", command=apri_popup_modifica).pack(side="left", padx=10)
    tk.Button(frame_azioni, text="Elimina Riga Selezionata", bg="#e74c3c", fg="white", command=esegui_eliminazione).pack(side="left", padx=10)

# ================= SCHERMATA: GRAFICI INTEGRATI =================
def schermata_grafici(container):
    pulisci_schermata(container)
    
    lbl_info = tk.Label(container, text="Andamento Temporale Medio Inquinanti", font=("Helvetica", 14, "bold"))
    lbl_info.pack(pady=5)
    
    frame_canvas = tk.Frame(container)
    frame_canvas.pack(fill="both", expand=True)
    
    # Creazione del contenitore Matplotlib (2 grafici affiancati)
    fig = Figure(figsize=(8, 4), dpi=100)
    
    # Grafico 1: PM10
    ax1 = fig.add_subplot(121)
    date_pm10, valori_pm10 = database.get_dati_grafico("PM10")
    ax1.plot(date_pm10, valori_pm10, color="orange", label="PM10")
    ax1.set_title("Andamento PM10")
    ax1.set_ylabel("µg/m³")
    ax1.tick_params(axis='x', rotation=45, labelsize=7)
    
    # Grafico 2: NO2
    ax2 = fig.add_subplot(122)
    date_no2, valori_no2 = database.get_dati_grafico("NO2")
    ax2.plot(date_no2, valori_no2, color="red", label="NO2")
    ax2.set_title("Andamento NO2")
    ax2.tick_params(axis='x', rotation=45, labelsize=7)
    
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

# ================= SCHERMATA: SUPERAMENTI SOGLIE UE =================
def schermata_superamenti(container):
    pulisci_schermata(container)
    
    lbl_titolo = tk.Label(container, text="Giornate Critiche oltre i Limiti di Legge UE", font=("Helvetica", 14, "bold"), fg="#e74c3c")
    lbl_titolo.pack(pady=10)
    
    colonne = ("ID", "Stazione", "Data", "Inquinante", "Valore Registrato", "Limite UE")
    tabella = ttk.Treeview(container, columns=colonne, show="headings", height=15)
    for col in colonne:
        tabella.heading(col, text=col)
        tabella.column(col, width=120, anchor="center")
    tabella.pack(fill="both", expand=True, padx=15, pady=10)
    
    dati = database.get_superamenti_limiti()
    for riga in dati:
        tabella.insert("", tk.END, values=riga)

# ================= SCHERMATA: ANAGRAFICA STAZIONI =================
def schermata_stazioni(container):
    pulisci_schermata(container)
    
    lbl_titolo = tk.Label(container, text="Stazioni di Rilevamento Attive (Milano)", font=("Helvetica", 14, "bold"))
    lbl_titolo.pack(pady=10)
    
    colonne = ("ID AMAT", "Località / Nome Stazione", "Latitudine", "Longitudine")
    tabella = ttk.Treeview(container, columns=colonne, show="headings", height=15)
    for col in colonne:
        tabella.heading(col, text=col)
        tabella.column(col, width=150, anchor="center")
    tabella.pack(fill="both", expand=True, padx=15, pady=10)
    
    dati = database.get_stazioni()
    for riga in dati:
        tabella.insert("", tk.END, values=riga)

# ================= SCHERMATA: PANNELLO AI / PREVISIONI =================
def schermata_ai(container):
    pulisci_schermata(container)
    
    lbl_titolo = tk.Label(container, text="Pannello AI & Modelli Predittivi", font=("Helvetica", 14, "bold"), fg="#8e44ad")
    lbl_titolo.pack(pady=15)
    
    box_ai = tk.LabelFrame(container, text=" Stato Modelli di Machine Learning ", font=("Helvetica", 10, "bold"), padx=20, pady=20)
    box_ai.pack(fill="both", expand=True, padx=30, pady=20)
    
    testo_placeholder = (
        "Sezione predisposta per l'integrazione con la Fase 5 del modulo AI.\n\n"
        "Configurazioni future previste:\n"
        "1. Modello di Regressione: Previsione concentrazione PM2.5 per il giorno successivo.\n"
        "2. Modello di Classificazione: Valutazione indice qualità aria (Buona / Media / Critica).\n\n"
        "I grafici di performance (curve di loss, accuratezza) verranno iniettati in questo spazio."
    )
    
    lbl_placeholder = tk.Label(box_ai, text=testo_placeholder, font=("Helvetica", 11, "italic"), justify="left", fg="#7f8c8d")
    lbl_placeholder.pack(anchor="w")