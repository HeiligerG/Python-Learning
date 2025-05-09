# Alle anleitungen

## M195-Python-MongoDB

Um unter **Windows** mit **VS Code** Python-Aufgaben in einer **virtuellen Umgebung (venv)** zu machen, kannst du folgende Schritte befolgen. Das ist ein bewährter Weg, um deine Abhängigkeiten für jede Aufgabe oder jedes Projekt sauber zu halten.

---

### ✅ Voraussetzungen:

* **Python** muss installiert sein ([Download von python.org](https://www.python.org/))
* **VS Code** muss installiert sein
* Die **Python-Erweiterung** in VS Code muss aktiviert sein

---

### 🔧 Schritte zur Nutzung von `venv` in VS Code:

1. **Projektordner anlegen**
   Erstelle einen neuen Ordner für deine Schulaufgabe, z. B. `schulaufgabe_01`.

2. **VS Code in diesem Ordner öffnen**

   * Öffne den Ordner direkt in VS Code (Rechtsklick → „Mit Code öffnen“ oder in VS Code: `Datei > Ordner öffnen...`).

3. **Terminal öffnen**
   In VS Code: `Strg + ö` oder `Terminal > Neues Terminal`.

4. **Virtuelle Umgebung erstellen**
   Im Terminal eingeben:

   ```bash
   python -m venv venv
   ```

   Dadurch wird ein Unterordner `venv` mit der virtuellen Umgebung erstellt.

5. **Virtuelle Umgebung aktivieren**
   Im Terminal eingeben:

   ```bash
   .\venv\Scripts\activate
   ```

   Danach siehst du im Terminal `(venv)` vor dem Pfad – das bedeutet, die Umgebung ist aktiv.

6. **Python-Interpreter auswählen (einmalig)**

   * `Strg + Shift + P` drücken → **„Python: Interpreter auswählen“** eingeben
   * Wähle den Eintrag mit dem Pfad `./venv/Scripts/python.exe` aus

7. **Jetzt kannst du loslegen**
   Erstelle eine `.py`-Datei (z. B. `aufgabe1.py`) und beginne zu programmieren.

8. **(Optional) Pakete installieren**
   Wenn du Pakete wie `numpy` oder `requests` brauchst:

   ```bash
   pip install numpy
   ```

---

### 🧹 Zum Beenden:

* Tippe `deactivate` im Terminal, um die virtuelle Umgebung zu verlassen.

---

Möchtest du ein kleines Beispielprojekt als Vorlage dazu haben?
