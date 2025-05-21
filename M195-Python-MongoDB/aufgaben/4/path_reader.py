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