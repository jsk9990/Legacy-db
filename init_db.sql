-- Creazione Database
CREATE DATABASE IF NOT EXISTS legacy_db;

-- Creazione Service Account vincolato all'IP della Macchina 2 (Whitelisting)
CREATE USER 'legacy_db_user'@'10.10.10.20' IDENTIFIED BY 'Password123!';

-- Assegnazione privilegi operativi e vulnerabilità (Privilegio FILE)
GRANT ALL PRIVILEGES ON legacy_db.* TO 'legacy_db_user'@'10.10.10.20';
GRANT FILE ON *.* TO 'legacy_db_user'@'10.10.10.20';
FLUSH PRIVILEGES;

-- Creazione tabella target per Ransomware/Esfiltrazione
USE legacy_db;
CREATE TABLE IF NOT EXISTS dati_aziendali_sensibili (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descrizione VARCHAR(100),
    valore_segreto VARCHAR(255)
);

-- Popolamento dati sensibili in chiaro
INSERT INTO dati_aziendali_sensibili (descrizione, valore_segreto) VALUES 
('Credenziali_Amministratore_Dominio', 'admin:SuperS3cr3t2026!'),
('Conto_Corrente_Aziendale', 'IT99C1234567890123456789012'),
('Token_Accesso_API_Esterna', 'ey...[TOKEN_FITTIZIO_MOLTO_LUNGO]...'),
('Progetto_Brevetti', 'Dettagli architettura nuovo prodotto confidenziale');
