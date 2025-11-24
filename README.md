# DONATION-TRACKING-SYSTEM-FOR-NGO
A donation tracking system lets an NGO record and verify every contribution in one place—who gave, how much, when, and where it was used. It cuts out messy spreadsheets, prevents missing funds, and makes audits and reporting straightforward. Without it, an NGO is guessing and hoping; with it transparency and accountability are provable not assumed.

WHAT DOES THIS CODE ACTUALLY DOES

Creates a real database (SQLite) instead of throwing data into temporary lists.

Separates donors and donations, meaning you can track multiple donations per person.

Runs as a CLI menu app, so you interact through numbered options.


Core components

1. init_db()

Builds two tables if they don’t exist:

donors (name + unique email)

donations (amount, date, method, purpose)


Ensures data persists across runs.


2. add_donor(name, email)

Inserts a donor.

Uses INSERT OR IGNORE, so duplicate emails don’t break the app.


3. add_donation(email, amount, method, purpose)

Looks up donor by email.

Refuses to record donations for unknown donors (good data hygiene).

Stores timestamp automatically.


4. list_donations()

Joins donor + donation tables.

Displays all recorded donations sorted by date.


5. total_donations()

Calculates the sum of all donations in the database.


6. menu()

Provides the user interface loop.

Calls the correct functions based on input.
