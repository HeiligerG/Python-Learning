# Aufgabe 1.1-1.2:

## Setup

>Erkläre die Abkürzung ODM und welche Funktion ODM wahrnimmt.

ODM ist eine Programmbibliothek der Datenbanken, die es ermöglicht, Datenbank-Objekte in Python zu definieren, die dann in der Datenbank gespeichert werden können.

### **Zusatz mit KI:**

**Funktion von ODMs – konkret**

>Ein ODM übernimmt diese Aufgaben:

| Funktion                        | Erklärung                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| 🧾 Modellierung                 | Du definierst Klassen wie `User`, `Book`, `Product` – mit Feldern und Typen         |
| 🔄 Mapping                      | Konvertiert Python-Objekte automatisch in MongoDB-Dokumente (und zurück)            |
| ✅ Validierung                   | Überprüft z. B. ob ein Feld `email` wirklich eine E-Mail ist                        |
| 🧮 Abfragen                     | Du kannst bequem mit `.find()` oder `.filter()` wie bei Objekten arbeiten           |
| 📝 Änderungen speichern/löschen | Statt `insert_one` usw. kannst du einfach `user.save()` oder `book.delete()` machen |


>Richte dein System so ein, dass du über Python eine Verbindung zur Datenbank herstellen kannst.
Erstelle dazu ein kleines Testprogramm.

#### Erledigt und abgelegt unter [Setup-Anleitung](C:\Users\gggig\Desktop\Python-Learning\README.md)

#### Arbeitsweise & Arbeitsplan abgelegt unter [Admin](C:\Users\gggig\Desktop\Python-Learning\M195-Python-MongoDB\admin)

