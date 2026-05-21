import mysql.connector
from mysql.connector import Error

def get_connection():
    """Crea e restituisce la connessione al database aire_db."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='astro97T',  # Cambia con la tua password se diversa
            database='aire_db'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Errore di connessione a MySQL: {e}")
        return None

def get_misurazioni(stazione_id=None, inquinante=None, data_inizio=None, data_fine=None):
    """Recupera le misurazioni applicando eventuali filtri."""
    conn = get_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    query = """
    SELECT m.id, s.nome, m.data, m.inquinante_codice, m.valore 
    FROM misurazione_giornaliera m 
    JOIN stazione s ON m.stazione_id = s.id_amat 
    WHERE 1=1
    """
    parametri = []
    
    if stazione_id:
        query += " AND m.stazione_id = %s"
        parametri.append(stazione_id)
    if inquinante:
        query += " AND m.inquinante_codice = %s"
        parametri.append(inquinante)
    if data_inizio:
        query += " AND m.data >= %s"
        parametri.append(data_inizio)
    if data_fine:
        query += " AND m.data <= %s"
        parametri.append(data_fine)
        
    query += " ORDER BY m.data DESC LIMIT 200"
    
    cursor.execute(query, tuple(parametri))
    risultati = cursor.fetchall()
    conn.close()
    return risultati

def inserisci_misurazione(stazione_id, data, inquinante, valore):
    """Inserisce una nuova misurazione."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO misurazione_giornaliera (stazione_id, data, inquinante_codice, valore)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (stazione_id, data, inquinante, valore))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Errore inserimento: {e}")
        return False

def modifica_misurazione(id_misurazione, stazione_id, data, inquinante, valore):
    """Modifica una misurazione esistente."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = """
        UPDATE misurazione_giornaliera 
        SET stazione_id = %s, data = %s, inquinante_codice = %s, valore = %s
        WHERE id = %s
        """
        cursor.execute(query, (stazione_id, data, inquinante, valore, id_misurazione))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Errore modifica: {e}")
        return False

def elimina_misurazione(id_misurazione):
    """Elimina una misurazione dal database."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM misurazione_giornaliera WHERE id = %s"
        cursor.execute(query, (id_misurazione,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Errore eliminazione: {e}")
        return False

def get_stazioni():
    """Recupera l'anagrafica delle stazioni."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT id_amat, nome, latitudine, longitudine FROM stazione")
    risultati = cursor.fetchall()
    conn.close()
    return risultati

def get_superamenti_limiti():
    """Recupera i giorni in cui i valori superano i limiti normativi UE."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    # Limiti indicativi UE: PM10 > 50, PM25 > 25, NO2 > 40
    query = """
    SELECT m.id, s.nome, m.data, m.inquinante_codice, m.valore,
           CASE 
               WHEN m.inquinante_codice = 'PM10' THEN 50
               WHEN m.inquinante_codice = 'PM25' THEN 25
               WHEN m.inquinante_codice = 'NO2' THEN 40
               ELSE 40
           END AS limite
    FROM misurazione_giornaliera m
    JOIN stazione s ON m.stazione_id = s.id_amat
    WHERE (m.inquinante_codice = 'PM10' AND m.valore > 50)
       OR (m.inquinante_codice = 'PM25' AND m.valore > 25)
       OR (m.inquinante_codice = 'NO2' AND m.valore > 40)
    ORDER BY m.data DESC
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    conn.close()
    return risultati

def get_dati_grafico(inquinante):
    """Recupera l'andamento temporale medio di un inquinante."""
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    query = """
    SELECT data, AVG(valore) 
    FROM misurazione_giornaliera 
    WHERE inquinante_codice = %s 
    GROUP BY data 
    ORDER BY data ASC
    """
    cursor.execute(query, (inquinante,))
    risultati = cursor.fetchall()
    conn.close()
    
    date = [rigo[0].strftime('%m-%d') if hasattr(rigo[0], 'strftime') else str(rigo[0]) for rigo in risultati]
    valori = [float(rigo[1]) for rigo in risultati if rigo[1] is not None]
    return date, valori