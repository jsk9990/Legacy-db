# ==========================================================
# Microservizio Interno REST API di Telemetria e Policy (M3)
# ==========================================================

from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Credenziali amministrative hardcoded (Target dell'attacco applicativo)
DB_HOST = "localhost"
DB_USER = "db_admin"
DB_PASS = "PasswordSicuraAziendale2026!"
DB_NAME = "legacy_db"

@app.route('/api/v1/telemetry', methods=['POST'])
def telemetry():
    """Endpoint legittimo per la ricezione dello stato di salute dei nodi interni"""
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing payload"}), 400
    
    with open("/var/log/telemetry_received.log", "a") as f:
        f.write(f"Node: {data.get('node')} - Status: {data.get('status')} - Storage: {data.get('disk_usage')}\n")
    
    return jsonify({"status": "success", "message": "Telemetry processed"}), 200

@app.route('/api/v1/config', methods=['GET'])
def get_config():
    """
    Endpoint per la distribuzione centralizzata delle configurazioni di policy.
    VULNERABILITÀ INDIVIDUATA: OWASP A01:2021 - Broken Access Control (Path Traversal).
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
