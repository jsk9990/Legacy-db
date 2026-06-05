# 🎯 M3 - Server Dati & Telemetria Enterprise (Legacy Database)

Questo repository contiene la configurazione di backend per la terza macchina (M3) del cyber range aziendale sviluppato per la tesi magistrale.

L'obiettivo di questo modulo è dimostrare come l'assunzione di una "rete interna intrinsecamente sicura" porti a gravi vulnerabilità di tipo applicativo e logico, consentendo il totale aggiramento dei meccanismi di segmentazione perimetrale.

## 🏗️ Architettura e Relazioni di Fiducia

* **Ruolo:** Database relazionale di produzione unito a un microservizio applicativo interno per la telemetria di rete.
* **Isolamento di Rete:** Il sistema è segregato e non possiede rotte verso Internet. Comunica esclusivamente nella subnet interna (`10.10.10.X`).
* **Meccanismi di Difesa Abusati:** Il database MySQL applica un whitelisting rigoroso, accettando connessioni unicamente dall'IP di M2 (`10.10.10.20`). Tuttavia, la presenza dell'API Flask sulla porta `5000` espone un perimetro applicativo interno attaccabile.

## ⚠️ Vulnerabilità Target (Mappatura OWASP Top 10)

Rispetto alle configurazioni tradizionali, l'ambiente è stato rifattorizzato per simulare uno scenario enterprise realistico:

1. **OWASP - Broken Access Control (Arbitrary File Read / Path Traversal):**
   L'endpoint dell'API `/api/v1/config?file=` non esegue la sanificazione dei parametri di input. Un utente malintenzionato in grado di parlare con l'API può risalire l'albero delle directory (`../`) per leggere file sensibili di sistema e applicativi.

2. **OWASP - Security Misconfiguration (Hardcoded Credentials):**
   Il codice sorgente del microservizio Flask (`app.py`) ospita in chiaro le credenziali di root del database MySQL (`db_admin`), violando le linee guida di gestione sicura dei segreti applicativi.

## ⚙️ Setup e Deployment dell'Ambiente

Per ripristinare la macchina allo stato iniziale ("Golden Image"):

1. **Installazione dipendenze e Database:**
```bash
   sudo apt update
   sudo apt install mysql-server python3-flask python3-pip python3-pymysql -y
```

2. **Configurazione di Rete di MySQL:**
   Modificare il file `/etc/mysql/mysql.conf.d/mysqld.cnf` impostando `bind-address = 0.0.0.0` per consentire l'instradamento del traffico proxy. Riavviare con `sudo systemctl restart mysql`.

3. **Inizializzazione dello Schema:**
```bash
   sudo mysql < init_db.sql
```

4. **Configurazione dell'API come Servizio Persistente:**
   Configurare l'applicazione Flask in `/app/app.py` e creare un'unità di servizio in `systemd` (`/etc/systemd/system/telemetry-api.service`) affinché il processo rimanga attivo in background e resista ai riavvii di sistema.

## 🗡️ La Kill Chain Operativa (Analisi End-to-End)

La catena d'attacco simulata si sviluppa attraverso i seguenti passaggi strategici condotti dall'attaccante:

1. **Reconnaissance Statica su M2:** Analisi in memoria delle stringhe del bytecode compilato (`.pyc`) per estrarre la topologia dei microservizi interni e mappare l'endpoint dell'API su M3.

2. **Sfruttamento Applicativo (Source Code Leak):** Esecuzione del Path Traversal sull'endpoint vulnerabile per esfiltrare il codice sorgente di `app.py` e recuperare le credenziali amministrative di MySQL.

3. **Multi-Hop Pivoting (Elusione del Firewall):** Distribuzione mimetizzata dello strumento *Chisel* (Masquerading in `/var/tmp/` sotto forma di file nascosto `.systemd-private-svc`) per incapsulare il traffico MySQL all'interno di un tunnel cifrato inverso non standard (Porte `58000` e `53306`).

4. **Credential Cracking Offline (Strada B):** Dump massivo del database da Kali Linux ed estrazione della tabella `staff_credentials`. Cracking offline degli hash MD5 tramite dizionario (`rockyou.txt`) per compromettere l'identità del personale IT e mappare potenziali riusi di password (*Password Reuse*) a livello infrastrutturale.

5. **Ransomware Logico Fileless:** Abuso intenzionale e autorizzato del motore crittografico nativo di MySQL (`AES_ENCRYPT`) per cifrare sul posto (*in-place*) i dati industriali sensibili, completando l'attacco di *Double Extortion* senza depositare payload eseguibili sul disco.
