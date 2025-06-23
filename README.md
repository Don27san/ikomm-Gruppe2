# Project Overview

## 🚀 Our Tasks

- [ ] **Implement default connection handling**
- [ ] **Feature:** Build User Interface
- [ ] **Feature:** Message delivery & reception
- [ ] **Feature:** Writing Indicators
- [ ] **Feature:** Live Location
- [ ] **Support:** Read Receipts

---

## 📝 Getting Started

Follow these steps to set up and run both the server and client:

### 1. Clone the Repository
```bash
git clone https://github.com/Don27san/ikomm-Gruppe2.git
cd ikomm-Gruppe2
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
python -m server.main
```

### 4. Start the Client (in a new terminal)

```bash
python -m client.main
```

---

## 💡 Important Commands

Its better to use `Pipenv`! Use the following scripts defined in your `Pipfile` for easier setup and management:

```bash
# Start the client on localhost
pipenv run client

# Start the server on localhost
pipenv run server

# Start the client on local network
pipenv run client-prod

# Start the server on local network
pipenv run server-prod

# Generate Python code from protobuf definitions
pipenv run pb-compile

# Update requirements.txt with current dependencies
pipenv run update-requirements
```

These scripts simplify running common tasks without typing full commands. :)





🖥️ GUI-Client – Anleitung zur Ausführung
Dieses Projekt enthält einen grafischen Chat-Client, der mit PyQt5 entwickelt wurde. Diese Anleitung erklärt, wie man den GUI-Client lokal ausführt und testet.

📦 Abhängigkeiten installieren
Stelle sicher, dass Python 3.10+ installiert ist, und installiere die benötigten Pakete mit:

bash

pip install -r requirements.txt
Alternativ (falls keine requirements.txt vorhanden ist):

bash

pip install PyQt5 protobuf geocoder netifaces pynput
📁 Projektstruktur
bash

ikomm-Gruppe2/
├── chatwindow.py           # GUI-Hauptfenster
├── main.py                 # Einstiegspunkt für den ersten Client
├── main2.py                # Zweiter Einstiegspunkt (für parallele Tests)
├── config.py               # Konfiguration für Client 1 (Ports, Adresse usw.)
├── config2.py              # Konfiguration für Client 2 (mit anderen Ports)
├── client/
│   ├── connection_service.py
│   ├── discovery_service.py
│   ├── typing_feature.py
│   └── location_feature.py
├── server/                 # Servermodule
├── locationviewer.py       # Popup zur Standortanzeige
└── chatwindow.ui           # UI-Datei für Qt Designer
🚀 GUI starten
✅ Haupt-Client starten:
bash

python main.py
✅ Zweiten Client starten (für Kommunikationstests):
Stelle sicher, dass config2.py andere Ports als config.py verwendet.

bash

python main2.py
Nun kannst du in zwei Fenstern chatten, Tipp-Anzeigen testen und Standorte teilen.
