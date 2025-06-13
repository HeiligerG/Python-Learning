from book import Buch

def main():
    buecher_liste = [
    Buch("Der Herr der Ringe", "J.R.R. Tolkien", "978-3-608-93830-2", 15.99),
    Buch("Harry Potter und der Stein der Weisen", "J.K. Rowling", "978-3-551-35401-4", 12.50),
    Buch("1984", "George Orwell", "978-3-548-23410-8", 9.99),
    Buch("Python Programming", "Mark Lutz", "978-1-449-35573-9", 45.00),
    ]
    
    print("=== Bücherliste ===")
    for i, buch in enumerate(buecher_liste, 1):
        print(f"{i}. {buch}")


if __name__ == "__main__":
    main()