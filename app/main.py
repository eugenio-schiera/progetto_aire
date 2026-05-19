import tkinter as tk
import views

def cambia_schermata(funzione_schermata):
    """Svuota il pannello centrale e carica la nuova vista selezionata."""
    funzione_schermata(main_container)

# 1. Finestra Principale Root
root = tk.Tk()
root.title("AIRE - Qualità dell'Aria a Milano")
root.geometry("900x650")
root.minsize(850, 600)

# 2. Creazione della barra di navigazione fissa superiore
views.crea_barra_navigazione(root, cambia_schermata)

# 3. Contenitore dinamico centrale per le varie viste
main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True, padx=10, pady=10)

# 4. Avvio automatico dell'app sulla schermata Home
cambia_schermata(views.schermata_home)

if __name__ == "__main__":
    root.mainloop()