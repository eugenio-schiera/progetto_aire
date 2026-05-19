import tkinter as tk
from tkinter import messagebox
import database
import views

def test_connessione():
    """Testa se l'app riesce a comunicare con il database."""
    conn = database.get_connection()
    if conn:
        messagebox.showinfo("Successo", "Connessione al database aire_db stabilita correttamente!")
        conn.close()
    else:
        messagebox.showerror("Errore", "Impossibile connettersi al database. Verifica le credenziali.")

def apri_misurazioni():
     """Richiama la funzione dal modulo views.""" 
     views.mostra_misurazioni(root)

# Configurazione della finestra principale
root = tk.Tk()
root.title("AIRE - Qualità dell'Aria a Milano")
root.geometry("800x600")

# Titolo della Home
titolo = tk.Label(root, text="Benvenuto in AIRE", font=("Helvetica", 24, "bold"))
titolo.pack(pady=40)

# Pulsanti
btn_test = tk.Button(root, text="Testa Connessione DB", font=("Helvetica", 12), command=test_connessione)
btn_test.pack(pady=10)

btn_dati = tk.Button(root, text="Visualizza Misurazioni", font=("Helvetica", 12), command=apri_misurazioni)
btn_dati.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()