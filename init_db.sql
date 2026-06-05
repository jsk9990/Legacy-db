-- ==========================================
-- Configurazione Database Target - Macchina 3
-- ==========================================

CREATE DATABASE IF NOT EXISTS legacy_db;
USE legacy_db;

-- 1. Ripristino/Pulizia Tabelle
DROP TABLE IF EXISTS dati_aziendali_sensibili;
DROP TABLE IF EXISTS staff_credentials;

-- 2. Creazione Service Account vincolato all'IP di M2 (Trust Relationship)
-- Sostituisce il vecchio utente ad alti privilegi di sistema
CREATE USER IF NOT EXISTS 'db_admin'@'10.10.10.20' IDENTIFIED BY 'PasswordSicuraAziendale2026!';
GRANT ALL PRIVILEGES ON legacy_db.* TO 'db_admin'@'10.10.10.20';
FLUSH PRIVILEGES;

CREATE USER IF NOT EXISTS 'db_admin'@'localhost' IDENTIFIED BY 'PasswordSicuraAziendale2026!';
GRANT ALL PRIVILEGES ON legacy_db.* TO 'db_admin'@'localhost';
FLUSH PRIVILEGES;

-- 3. Tabella Target per Ransomware/Esfiltrazione (Dati Sensibili Aziendali in Chiaro)
CREATE TABLE dati_aziendali_sensibili (
    id INT AUTO_INCREMENT PRIMARY KEY,
    risorsa VARCHAR(100),
    valore_segreto VARCHAR(255)
);

INSERT INTO dati_aziendali_sensibili (risorsa, valore_segreto) VALUES 
('Conto_Corrente_Aziendale_IBAN', 'IT99C1234567890123456789012'),
('Chiave_Infrastruttura_Cloud_AWS', 'AKIAIOSFODNN7EXAMPLE:wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'),
('Brevetto_Algoritmo_Core', 'Progetto_Top_Secret_Industrial_Automation_v4.2.pdf'),
('Token_Integrazione_Stripe', 'sk_test_51Nx...[TOKEN_PRIVATO_AZIENDALE]...');

-- 4. Tabella Credenziali Staff per l'analisi del Password Cracking (Strada B - Teoria)
CREATE TABLE staff_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password_hash VARCHAR(32)
);

-- Le password reali corrispondenti sono 'shadow12' e 'password123' (presenti in rockyou.txt)
INSERT INTO staff_credentials (username, password_hash) VALUES 
('sysadmin_ops', MD5('shadow12')),
('finance_manager', MD5('password123'));
