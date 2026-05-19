import mysql.connector
from mysql.connector import Error

def get_connection():
    """Crea e restituisce la connessione al database aire_db."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root', # Cambia se il tuo utente MySQL è diverso
            password='LA_TUA_PASSWORD_QUI', # Inserisci la tua password di MySQL
            database='aire_db'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Errore di connessione a MySQL: {e}")
        return None
import mysql.connector
from mysql.connector import Error

def get_connection():
    """Crea e restituisce la connessione al database aire_db."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root', # Cambia se il tuo utente MySQL è diverso
            password='LA_TUA_PASSWORD_QUI', # Inserisci la tua password di MySQL
            database='aire_db'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Errore di connessione a MySQL: {e}")
        return None
    
def get_misurazioni():
    """Recupera le misurazioni dal database."""
    conn = get_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    query = """
    SELECT m.id, s.nome, m.data, m.inquinante_codice, m.valore 
    FROM misurazione_giornaliera m 
    JOIN stazione s ON m.stazione_id = s.id_amat 
    LIMIT 100
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    conn.close()
    return risultati