# Alle anleitungen

Dies ist eine **klare Schritt-für-Schritt-Anleitung**, wie du an deinem Python-MongoDB-Projekt arbeitest – vom Start bis zum Ausführen. Ideal für Schulaufgaben oder eigenes Üben unter Windows mit VS Code und `venv`.

---

### ✅ **Einmalig: Projekt einrichten**

#### 🔹 1. **Projektordner erstellen**

Zum Beispiel auf dem Desktop:

```plaintext
C:\Users\gggig\Desktop\M195-Python-MongoDB
```

#### 🔹 2. **VS Code öffnen**

Öffne den **gesamten Ordner** in VS Code:

* Rechtsklick auf den Ordner → „Mit Code öffnen“
* Oder: `Datei > Ordner öffnen` in VS Code

#### 🔹 3. **Terminal öffnen**

In VS Code: `Strg + ö` oder `Terminal > Neues Terminal`

#### 🔹 4. **Virtuelle Umgebung erstellen**

Im Terminal:

```bash
python -m venv m195
```

#### 🔹 5. **venv aktivieren**

```bash
.\m195\Scripts\activate
```
oder wenn das venv venv heisst:

```bash
.\.venv\Scripts\Activate.ps1
```

→ Jetzt siehst du z. B. `(m195)` im Terminal

#### 🔹 6. **Pymongo installieren**

```bash
pip install pymongo
```

#### 🔹 7. **Test-Skript erstellen**

Erstelle eine Datei im Projektordner, z. B. `mongodb_test.py`. Inhalt:

```python
from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

print("Verfügbare Datenbanken:")
print(client.list_database_names())
```

---

### 🔁 **Jedes Mal, wenn du daran arbeiten willst:**

1. **Projektordner öffnen in VS Code**
   → Öffne wieder `M195-Python-MongoDB`

2. **Terminal öffnen (Strg + ö)**

3. **Virtuelle Umgebung aktivieren:**

   ```bash
   .\m195\Scripts\activate
   ```

4. **Python-Datei ausführen**

   ```bash
   python mongodb_test.py
   ```

---

### 🧼 Zum Beenden

Wenn du fertig bist:

```bash
deactivate
```

---

### 💡 Optional: Pakete sichern

Falls du mehrere Pakete installiert hast, kannst du eine `requirements.txt` erstellen:

```bash
pip freeze > requirements.txt
```

Dann kannst du später alles wieder installieren mit:

```bash
pip install -r requirements.txt
```
