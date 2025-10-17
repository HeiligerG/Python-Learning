# WOCHE 1: Bankkonto-Simulator - Side Effects verstehen
# =====================================================

print("BANKKONTO-SIMULATOR")
print("=" * 50)

# SCHLECHT: Wie es NICHT gemacht werden sollte
# (Das hier führt zu Bugs die schwer zu finden sind)

balance = 1000  # Globale Variable - GEFÄHRLICH!

def withdraw_bad(amount):
    """Diese Funktion hat Side Effects - problematisch!"""
    global balance
    if balance >= amount:
        balance -= amount
        print(f"Abgehoben: {amount}€, Kontostand: {balance}€")
    else:
        print("Nicht genug Geld!")

def deposit_bad(amount):
    """Auch diese Funktion verändert globalen State"""
    global balance
    balance += amount
    print(f"Eingezahlt: {amount}€, Kontostand: {balance}€")

print("\n--- SCHLECHTES BEISPIEL (mit Side Effects) ---")
withdraw_bad(200)  # balance wird heimlich verändert
deposit_bad(50)    # balance wird wieder verändert
withdraw_bad(100)  # Wer weiß noch was balance ist?

# GUT: Pure Functions - Wie Profis es machen
def withdraw_pure(balance, amount):
    """Pure Function: Input → Output, keine Überraschungen!"""
    if balance >= amount:
        new_balance = balance - amount
        return new_balance, f"Abgehoben: {amount}€"
    else:
        return balance, "Nicht genug Geld!"

def deposit_pure(balance, amount):
    """Pure Function: Berechenbar und testbar"""
    new_balance = balance + amount
    return new_balance, f"Eingezahlt: {amount}€"

def get_balance_info(balance):
    """Pure Function für Kontostand-Info"""
    if balance < 0:
        return f"Kontostand: {balance}€ (Überziehen!)"
    elif balance < 100:
        return f"Kontostand: {balance}€ (Wenig Geld)"
    else:
        return f"Kontostand: {balance}€"

print("\n--- GUTES BEISPIEL (Pure Functions) ---")
current_balance = 1000

# Jeder Schritt ist klar und nachvollziehbar
current_balance, message1 = withdraw_pure(current_balance, 200)
print(message1, "->", get_balance_info(current_balance))

current_balance, message2 = deposit_pure(current_balance, 50)
print(message2, "->", get_balance_info(current_balance))

current_balance, message3 = withdraw_pure(current_balance, 100)
print(message3, "->", get_balance_info(current_balance))

# DEINE AUFGABE: Erweitere das System!
print("\n" + "=" * 50)
print("DEINE HERAUSFORDERUNG:")
print("=" * 50)

def calculate_interest_pure(balance, rate=0.02):
    """
    TODO: Implementiere eine Pure Function für Zinsen
    - Input: balance (Kontostand), rate (Zinssatz, default 2%)
    - Output: (neuer_kontostand, nachricht)
    """
    

def transfer_pure(from_balance, to_balance, amount):
    """
    TODO: Implementiere Überweisung zwischen zwei Konten
    - Input: from_balance, to_balance, amount
    - Output: (neuer_from_balance, neuer_to_balance, nachricht)
    - Denk dran: Pure Function = keine Überraschungen!
    """
    # DEIN CODE HIER
    pass

def simulate_month_pure(balance, transactions):
    """
    TODO: Simuliere einen ganzen Monat mit mehreren Transaktionen
    - Input: balance, transactions (Liste von ("withdraw/deposit", betrag))
    - Output: (end_balance, transaction_log)
    
    Beispiel transactions: [("deposit", 500), ("withdraw", 200), ("withdraw", 100)]
    """
    # DEIN CODE HIER
    pass

# Test deine Funktionen hier:
if __name__ == "__main__":
    print("\n--- TESTE DEINE FUNKTIONEN ---")
    
    # Test 1: Zinsen
    # balance_with_interest, msg = calculate_interest_pure(1000)
    # print(f"Zinsen: {msg}")
    
    # Test 2: Überweisung  
    # alice_balance, bob_balance, msg = transfer_pure(1000, 500, 200)
    # print(f"Überweisung: {msg}")
    # print(f"Alice: {alice_balance}€, Bob: {bob_balance}€")
    
    # Test 3: Monatssimulation
    # transactions = [("deposit", 500), ("withdraw", 200), ("withdraw", 100)]
    # final_balance, log = simulate_month_pure(1000, transactions)
    # print(f"Monatsende: {final_balance}€")
    # for entry in log:
    #     print(f"  - {entry}")

print("\nWARUM PURE FUNCTIONS BESSER SIND:")
print("- Bugs sind leichter zu finden")
print("- Code ist testbar")  
print("- Parallel ausführbar")
print("- Vorhersagbares Verhalten")
print("- Weniger mysterische 'Warum funktioniert das nicht?'-Momente")

print("\nNÄCHSTE WOCHE: Todo-Liste die nicht explodiert!")
print("   (Mutable vs Immutable Data)")