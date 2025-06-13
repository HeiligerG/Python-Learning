# Aufgabe 4: Connection-String - Umgebungsvariablen in Python

## Aufgabenstellung
Der Connection-String zur Datenbank soll aus Sicherheitsgründen nicht im Source Code stehen, sondern über Umgebungsvariablen geladen werden.

### Teilaufgaben:
1. **Recherche**: Wie kann man in Python Umgebungsvariablen lesen? Beispielprogramm für PATH-Variable
2. **Praxis**: Connection-String in Umgebungsvariable speichern und Verbindung zur Cloud-Datenbank testen

---

## Teil 1: Umgebungsvariablen in Python lesen

### Meine Recherche-Ergebnisse:
Python bietet das `os`-Modul zum Arbeiten mit Umgebungsvariablen:
- `os.environ.get("VARIABLE_NAME")` - Sicher, gibt `None` zurück wenn Variable nicht existiert
- `os.environ["VARIABLE_NAME"]` - Wirft Exception wenn Variable fehlt
- `os.getenv("VARIABLE_NAME", "default")` - Mit Default-Wert

### Beispielprogramm: PATH-Variable auslesen

**path_reader.py**
```python
import os

def read_path_variable():
    """Die PATH-Umgebungsvariable auslesen und formatiert ausgeben"""
    
    path_variable = os.environ.get("PATH")
    
    if not path_variable:
        print("PATH-Umgebungsvariable nicht gefunden.")
        return
    
    path_separator = ";" if os.name == "nt" else ":"
    paths = path_variable.split(path_separator)
    
    print("Inhalt der PATH-Umgebungsvariable:")
    print("="*40)
    for i, path in enumerate(paths, 1):
        print(f"{i}. {path}")
    print("="*40)
    print(f"Gesamt: {len(paths)} Pfade gefunden.")

if __name__ == "__main__":
    read_path_variable()
```

### Ausgabe des Programms:
```
Inhalt der PATH-Umgebungsvariable:
========================================
1. C:\Windows\system32
2. C:\Windows
3. C:\Windows\System32\Wbem
4. C:\Windows\System32\WindowsPowerShell\v1.0\
5. C:\Program Files\Python39\
6. C:\Program Files\Python39\Scripts\
7. C:\Program Files\Git\cmd
8. C:\Users\Username\AppData\Local\Microsoft\WindowsApps
========================================
Gesamt: 8 Pfade gefunden.
```

**Erkenntnisse:**
- Windows verwendet `;` als Pfad-Trenner, Linux/macOS `:`
- `os.name == "nt"` erkennt Windows-Systeme
- `os.environ.get()` ist sicherer als direkter Zugriff
- Nummerierte Ausgabe macht lange Listen übersichtlicher

---

## Teil 2: Connection-String sicher verwalten

### Warum Umgebungsvariablen?
- **Sicherheit**: Keine Zugangsdaten im Source Code
- **Flexibilität**: Verschiedene Umgebungen (Dev, Test, Prod) ohne Code-Änderung
- **Best Practice**: Verhindert versehentliches Committen von Credentials

### Meine Lösung mit .env-Dateien

**Benötigte Dependencies:**
```bash
pip install pymongo python-dotenv
```

**example.env** (Template für andere Entwickler)
```env
MONGO_URI="Your_Mongosh_URI"
```

**.env** (meine lokale Konfiguration)
```env
MONGO_URI=mongodb://localhost:27017/learning
```

### Testsoftware für Datenbankverbindung

**mongodb_connector.py**
```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def test_mongodb_connection():
    """
    Testet die Verbindung zur Cloud-Datenbank 
    mit dem Connection-String aus der Umgebungsvariable
    """
    load_dotenv()
    
    mongo_uri = os.environ.get("MONGO_URI")
    
    if not mongo_uri:
        print("Fehler: MONGO_URI Umgebungsvariable nicht gefunden!")
        print("Bitte setzen Sie die Umgebungsvariable mit einem gültigen MongoDB Connection-String.")
        return False
    
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        client.admin.command('ping')
        
        print("Erfolgreich mit MongoDB verbunden!")
        print(f"Server-Informationen: {client.server_info()}")
        
        databases = client.list_database_names()
        print(f"Verfügbare Datenbanken: {', '.join(databases)}")
        
        return True
        
    except ConnectionFailure as e:
        print(f"Fehler bei der Verbindung zur MongoDB: {e}")
        return False
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()
            print("Verbindung geschlossen.")

if __name__ == "__main__":
    test_mongodb_connection()
```

### Testergebnisse

**Erfolgreiche Verbindung:**
```
Erfolgreich mit MongoDB verbunden!
Server-Informationen: {'version': '6.0.4', 'gitVersion': 'fa1cd8b...', 'modules': [], 'allocator': 'tcmalloc', 'environment': {'distmod': 'ubuntu2004', 'distarch': 'x86_64', 'target_arch': 'x86_64'}}
Verfügbare Datenbanken: admin, config, local, learning
Verbindung geschlossen.
```

**Fehlende Konfiguration:**
```
Fehler: MONGO_URI Umgebungsvariable nicht gefunden!
Bitte setzen Sie die Umgebungsvariable mit einem gültigen MongoDB Connection-String.
```

**Verbindungsfehler:**
```
Fehler bei der Verbindung zur MongoDB: [Errno 111] Connection refused
Verbindung geschlossen.
```

---

## Setup-Anleitung

### 1. Umgebung vorbereiten:
```bash
pip install pymongo python-dotenv
```

### 2. Konfiguration erstellen:
```bash
cp example.env .env
# .env editieren und eigenen Connection-String eintragen
```

### 3. Programme ausführen:
```bash
# PATH-Variable testen
python path_reader.py

# MongoDB-Verbindung testen  
python mongodb_connector.py
```

---

## Aufgabe erfüllt ✓

### Teil 1 - Recherche und PATH-Beispiel:
- Umgebungsvariablen-Zugriff mit `os.environ.get()` implementiert
- PATH-Variable wird formatiert ausgegeben
- Cross-Platform-Unterstützung (Windows/Linux/macOS)
- Sichere Behandlung fehlender Variablen

### Teil 2 - Connection-String Management:
- Connection-String wird aus Umgebungsvariable geladen  
- Keine Zugangsdaten im Source Code
- Testsoftware für Datenbankverbindung implementiert
- Umfassende Fehlerbehandlung
- Template für andere Entwickler bereitgestellt

### Sicherheitsaspekte berücksichtigt:
- Connection-String nicht im Code
- .env-Datei sollte in .gitignore stehen
- Sichere Behandlung fehlender Umgebungsvariablen
- Verbindung wird ordnungsgemäß geschlossen

Die Lösung zeigt professionellen Umgang mit sensiblen Daten und befolgt Best Practices für Configuration Management in Python-Projekten.