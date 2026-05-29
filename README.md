# 🎯 M3 - Server Dati (Legacy Database)

Questo repository contiene la configurazione per la terza e ultima macchina del laboratorio di Penetration Testing/Red Teaming sviluppato per la tesi magistrale. 

Rappresenta il "cuore" dell'infrastruttura aziendale, un server database isolato dalla rete esterna, ma vulnerabile a causa di un *Insecure Design* e *Security Misconfigurations*.

## 🏗️ Architettura e Sicurezza
* **Ruolo:** Server Database Backend.
* **Isolamento Rete:** Non esposto a Internet. Raggiungibile esclusivamente dalla rete interna (`10.10.10.X`).
* **Regole di Accesso:** Il database accetta connessioni solo dall'IP specifico della Macchina 2 (`10.10.10.20`), simulando un approccio *Zero Trust* configurato parzialmente.

## ⚠️ Vulnerabilità Introdotte (OWASP)
1. **Insecure Design:** Mancanza di segmentazione rigorosa. L'abuso di un tunnel proxy dalla Macchina 2 permette di eludere il whitelisting IP.
2. **Security Misconfiguration:** * La variabile `secure_file_priv = ""` nel file `mysqld.cnf` permette letture/scritture arbitrarie su disco.
   * L'assegnazione del privilegio globale `FILE` all'utente applicativo.

## ⚙️ Setup dell'Ambiente
Per replicare questa macchina su un'installazione pulita di Ubuntu Server:

1. Installare MySQL: `sudo apt install mysql-server -y`
2. Modificare il file `/etc/mysql/mysql.conf.d/mysqld.cnf`:
   * Impostare `bind-address = 0.0.0.0`
   * Aggiungere alla fine del file: `secure_file_priv = ""`
3. Riavviare il servizio: `sudo systemctl restart mysql`
4. Caricare il database: `sudo mysql < init_db.sql`

## 🗡️ The Kill Chain (Ransomware Double Extortion)
Questa macchina è il bersaglio finale dell'attacco. L'attaccante, partendo da una shell di root sulla M2:
1. Effettua **Reverse Engineering** di un binario Python per estrarre le credenziali hardcoded.
2. Esegue un **Network Pivoting** tramite *Chisel* per superare l'isolamento di rete.
3. Conduce un'**Esfiltrazione Silenziosa** dei dati tramite tunnel SSH/Chisel.
4. Completa l'attacco con un **Ransomware Logico Fileless**, abusando delle funzioni di crittografia native di MySQL (`AES_ENCRYPT`) per bloccare i dati aziendali a scopo di estorsione.
