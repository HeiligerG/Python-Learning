# 🛠️ Arbeitsweise bei der Bearbeitung von M195-Aufgaben

Dies ist ein **zusätzliches `arbeitsweise.md`**, das klar vorgibt, **wie beim Bearbeiten der Aufgaben vorgegangen werden soll**, inklusive **Schritt-für-Schritt-Vorgehen**, **Umgang mit Git** und **wann man was machen muss**. Ideal für strukturierte, professionelle Arbeit.

---

## 📂 Projektstruktur

```

M195-Python-MongoDB/
├── admin/                   # markdown
├── m195/                    # venv
├── aufgaben/                # einzelne Aufgaben als Dateien oder Ordner
│   ├── 2\_1\_db\_explorer.py
│   ├── 3\_1\_bezirke.py
│   └── ...
├── README.md                # Aufgabenplan
├── arbeitsweise.md          # Diese Datei
└── requirements.txt         # Abhängigkeiten

````

---

## 🚀 Vorgehen bei jeder Aufgabe

### 🔄 Vorbereitung (einmal pro Session)

1. Projektordner in VS Code öffnen
2. Terminal öffnen (`Strg + ö`)
3. Virtuelle Umgebung aktivieren:
   ```bash
   .\m195\Scripts\activate


4. Neues Git-Branch erstellen für die Aufgabe:

   ```bash
   git checkout -b aufgabe-3_1
   ```

---

### 🧩 Wenn du eine Aufgabe startest

* Erstelle eine neue Datei z. B. `3_1_bezirke.py`
* Schreibe einen Kommentar mit:

  ```python
  # Aufgabe 3.1: Alle Stadtbezirke ausgeben (ohne Duplikate)
  # Start: 2025-05-09
  ```
* Falls nötig, teste MongoDB-Verbindung
* Baue Lösung schrittweise auf
* Teste regelmäßig und logge eventuelle Fehler

---

### ✅ Wenn eine Aufgabe abgeschlossen ist

1. Funktionalität durchtesten
2. Optional: Ergebnis im Terminal screenshotten oder als Kommentar speichern
3. Änderungen committen:

   ```bash
   git add .
   git commit -m "🔧 Aufgabe 3.1 abgeschlossen: Bezirke ohne Duplikate"
   ```
4. Git-Branch ggf. pushen (z. B. bei Teamarbeit):

   ```bash
   git push origin aufgabe-3_1
   ```
5. Merge Request / Pull Request erstellen oder mit `main`/`master` mergen

---

## 🧠 Git-Kommandos – Reminder

```bash
# Neues Branch für Aufgabe starten
git checkout -b aufgabe-4_1

# Änderungen ansehen
git status

# Änderungen vorbereiten & committen
git add .
git commit -m "✅ Aufgabe 4.1: Umgebungsvariable auslesen"

# Zu GitHub pushen (wenn Remote eingerichtet)
git push origin aufgabe-4_1

# Zu anderem Branch wechseln
git checkout main

# Branch mergen (lokal)
git merge aufgabe-4_1
```

---

## 🗂️ Tipps für Struktur

* Benenne Dateien klar nach Aufgabe: `3_2_top_restaurants.py`
* Nutze `.gitignore` um `venv/` auszuschließen
* Speichere temporäre Dateien nicht mit (z. B. Dumps, Cache, Output)

---

📌 **Ziel:** Sauber, nachvollziehbar und git-sicher arbeiten – wie in echten Projekten!

```