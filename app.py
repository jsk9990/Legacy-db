# ==========================================================
# Microservizio Interno REST API di Telemetria e Policy (M3)
# ==========================================================

from flask import Flask, request, jsonify, send_file
import os
import pymysql  # Ricordati di eseguire 'pip install pymysql' su M3

app = Flask(__name__)

# Credenziali amministrative hardcoded (Target dell'attacco applicativo)
# L'attaccante sfrutta il Path Traversal per leggere queste righe
DB_HOST = "localhost"
DB_USER = "db_admin"
DB_PASS = "PasswordSicuraAziendale2026!"
DB_NAME = "legacy_db"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/v1/telemetry', methods=['POST'])
def telemetry():
    """
    Endpoint legittimo per la ricezione dello stato di salute dei nodi interni.
    Questo endpoint viene richiamato dal tuo file offuscato 'db_health_check.pyc' su M2.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing payload"}), 400
    
    with open("/var/log/telemetry_received.log", "a") as f:
        f.write(f"Node: {data.get('node')} - Status: {data.get('status')} - Storage: {data.get('disk_usage')}\n")
    
    return jsonify({"status": "success", "message": "Telemetry processed"}), 200


@app.route('/api/v1/reports', methods=['POST'])
def save_report():
    
    # NUOVO ENDPOINT: Riceve i dati dei report inviati periodicamente dallo script archive_reports.py di M2 e li scrive nel DB.
    
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing payload"}), 400

    title = data.get('title', '(senza titolo)')
    author = data.get('author', 'N/D')
    date = data.get('date', '')
    body = data.get('body', '')

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Crea la tabella di storicizzazione se non esiste nel database relazionale
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports_storicizzati (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    titolo VARCHAR(255),
                    autore VARCHAR(100),
                    data_report VARCHAR(50),
                    corpo TEXT,
                    archiviato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Query di inserimento reale dei dati nel DB
            sql = """INSERT INTO reports_storicizzati (titolo, autore, data_report, corpo) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (title, author, date, body))
        
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Report scritto correttamente nel database"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"DB Error: {str(e)}"}), 500


@app.route('/api/v1/config', methods=['GET'])
def get_config():
    """
    Endpoint per la distribuzione centralizzata delle configurazioni di policy.
    VULNERABILITÀ INDIVIDUATA: Broken Access Control (Path Traversal).
    La concatenazione diretta dell'input permette la lettura di file arbitrari su disco.
    """
    filename = request.args.get('file')
    if not filename:
        return jsonify({"status": "error", "message": "Missing file parameter"}), 400
    
    base_dir = "/app/config_files/"
    # Mancanza di controllo e sanificazione del percorso (es. utilizzo di ../../)
    target_path = base_dir + filename
    
    if os.path.exists(target_path):
        return send_file(target_path)
    else:
        return jsonify({"status": "error", "message": f"File {filename} not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
