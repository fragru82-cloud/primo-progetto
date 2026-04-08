# Guida Connessione VPS

## Dettagli Server

| Campo          | Valore               |
|----------------|----------------------|
| Provider       | Xpress VPS (CheapVPS)|
| Tipo           | Windows VPS          |
| IP Address     | 154.61.189.57        |
| Porta RDP      | 8467                 |
| Username       | Administrator        |
| Password       | *(vedi email)*       |

> **Nota sicurezza**: Non salvare mai la password in file versionati. Cambiala periodicamente.

---

## Connessione da Windows

### Metodo 1: Remote Desktop (mstsc)
1. Premi `Win + R`, digita `mstsc` e premi Invio
2. Nel campo "Computer" inserisci: `154.61.189.57:8467`
3. Clicca "Mostra opzioni" e inserisci il nome utente: `Administrator`
4. Clicca "Connetti"
5. Inserisci la password quando richiesto
6. Se appare un avviso certificato, clicca "Si" per procedere

### Metodo 2: File .rdp (connessione rapida)
Crea un file `vps.rdp` con questo contenuto:
```
full address:s:154.61.189.57:8467
username:s:Administrator
prompt for credentials:i:1
screen mode id:i:2
desktopwidth:i:1920
desktopheight:i:1080
```
Doppio click sul file per connetterti.

---

## Connessione da macOS

### Metodo 1: Microsoft Remote Desktop (consigliato)
1. Scarica "Microsoft Remote Desktop" dall'App Store
2. Clicca "+" > "Add PC"
3. PC Name: `154.61.189.57:8467`
4. User account: aggiungi account con `Administrator` e la password
5. Clicca "Add" e poi doppio click per connetterti

### Metodo 2: Da Terminale (con Homebrew)
```bash
brew install freerdp
xfreerdp /v:154.61.189.57:8467 /u:Administrator /p:'TUA_PASSWORD' /f
```

---

## Connessione da Linux

### Con xfreerdp (consigliato)
```bash
# Installazione
sudo apt install freerdp2-x11    # Debian/Ubuntu
sudo dnf install freerdp          # Fedora
sudo pacman -S freerdp            # Arch

# Connessione
xfreerdp /v:154.61.189.57:8467 /u:Administrator /p:'TUA_PASSWORD' /f /cert:ignore
```

### Con Remmina (GUI)
1. Installa Remmina: `sudo apt install remmina remmina-plugin-rdp`
2. Apri Remmina
3. Crea nuova connessione:
   - Protocollo: RDP
   - Server: `154.61.189.57:8467`
   - Username: `Administrator`
   - Password: *(inserisci manualmente)*
4. Clicca "Connetti"

---

## Connessione da Mobile

### Android
1. Scarica "RD Client" (Microsoft) dal Play Store
2. Aggiungi PC con indirizzo `154.61.189.57:8467`
3. Inserisci le credenziali

### iOS/iPadOS
1. Scarica "Remote Desktop" (Microsoft) dall'App Store
2. Aggiungi PC con indirizzo `154.61.189.57:8467`
3. Inserisci le credenziali

---

## Risoluzione Problemi

| Problema | Soluzione |
|----------|-----------|
| Connessione rifiutata | Verifica che la VPS sia attiva nel pannello del provider |
| Timeout connessione | Controlla il firewall; la porta 8467 deve essere aperta |
| Credenziali errate | Verifica maiuscole/minuscole nella password |
| Schermo nero dopo login | Attendi qualche secondo; se persiste, riconnettiti |
| Lag/lentezza | Riduci risoluzione e disabilita effetti visivi |

## Primi Passi dopo la Connessione

1. **Cambia la password** di Administrator
2. **Aggiorna Windows** (Windows Update)
3. **Configura il firewall** per le porte necessarie
4. **Installa** il software necessario per il tuo progetto
