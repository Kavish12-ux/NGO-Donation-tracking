import sqlite3
from datetime import datetime


DB_NAME = "donations.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            method TEXT,
            purpose TEXT,
            FOREIGN KEY(donor_id) REFERENCES donors(id)
        )
    """)

    conn.commit()
    conn.close()


def add_donor(name, email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO donors (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()


def add_donation(email, amount, method, purpose):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id FROM donors WHERE email=?", (email,))
    donor = cur.fetchone()

    if not donor:
        print("Donor not found. Add donor first.")
        conn.close()
        return

    donor_id = donor[0]
    cur.execute(
        "INSERT INTO donations (donor_id, amount, date, method, purpose) VALUES (?, ?, ?, ?, ?)",
        (donor_id, amount, datetime.now().strftime("%Y-%m-%d"), method, purpose)
    )

    conn.commit()
    conn.close()
    print("Donation recorded.")


def list_donations():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT donors.name, donations.amount, donations.date, donations.method, donations.purpose
        FROM donations
        JOIN donors ON donations.donor_id = donors.id
        ORDER BY donations.date DESC
    """)
    for row in cur.fetchall():
        print(row)
    conn.close()


def total_donations():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM donations")
    total = cur.fetchone()[0]
    conn.close()
    print("Total Donations:", total or 0)


def menu():
    init_db()
    while True:
        print("\nDonation Tracking System")
        print("1. Add Donor")
        print("2. Add Donation")
        print("3. View Donations")
        print("4. Total Amount Collected")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Donor Name: ")
            email = input("Donor Email: ")
            add_donor(name, email)

        elif choice == '2':
            email = input("Donor Email: ")
            amount = float(input("Amount: "))
            method = input("Method (Cash/UPI/Bank): ")
            purpose = input("Purpose: ")
            add_donation(email, amount, method, purpose)

        elif choice == '3':
            list_donations()

        elif choice == '4':
            total_donations()

        elif choice == '5':
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()