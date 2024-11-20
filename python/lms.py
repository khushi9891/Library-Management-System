import mysql.connector
from datetime import date

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="password",  # Replace with your MySQL password
    database="library_db"
)
cursor = db.cursor()

# Menu Functions
def add_author():
    name = input("Enter author's name: ")
    birth_year = int(input("Enter birth year: "))
    nationality = input("Enter nationality: ")
    books_written = int(input("Enter number of books written: "))
    query = "INSERT INTO Authors (name, birth_year, nationality, books_written) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, birth_year, nationality, books_written))
    db.commit()
    print("Author added successfully!")

def add_book():
    title = input("Enter book title: ")
    author_id = int(input("Enter author ID: "))
    genre = input("Enter genre: ")
    available_copies = int(input("Enter number of available copies: "))
    query = "INSERT INTO Books (title, author_id, genre, available_copies) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, author_id, genre, available_copies))
    db.commit()
    print("Book added successfully!")

def add_member():
    name = input("Enter member's name: ")
    membership_type = input("Enter membership type (Gold/Silver): ")
    email = input("Enter email: ")
    phone_number = input("Enter phone number: ")
    query = "INSERT INTO Members (name, membership_type, email, phone_number) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, membership_type, email, phone_number))
    db.commit()
    print("Member added successfully!")

def issue_book():
    book_id = int(input("Enter book ID: "))
    member_id = int(input("Enter member ID: "))
    issue_date = date.today()
    query = "INSERT INTO Transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_id, member_id, issue_date))
    db.commit()
    query_update = "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = %s"
    cursor.execute(query_update, (book_id,))
    db.commit()
    print("Book issued successfully!")

def return_book():
    transaction_id = int(input("Enter transaction ID: "))
    return_date = date.today()
    query = "UPDATE Transactions SET return_date = %s WHERE transaction_id = %s"
    cursor.execute(query, (return_date, transaction_id))
    db.commit()
    query_update = """
    UPDATE Books 
    SET available_copies = available_copies + 1 
    WHERE book_id = (SELECT book_id FROM Transactions WHERE transaction_id = %s)
    """
    cursor.execute(query_update, (transaction_id,))
    db.commit()
    print("Book returned successfully!")

def view_data(table_name):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    records = cursor.fetchall()
    print(f"\n--- {table_name.upper()} ---")
    for record in records:
        print(record)
    print("\n")

# CLI Menu
def menu():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Author")
        print("2. Add Book")
        print("3. Add Member")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Authors")
        print("7. View Books")
        print("8. View Members")
        print("9. View Transactions")
        print("10. View Staff")
        print("0. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_author()
        elif choice == "2":
            add_book()
        elif choice == "3":
            add_member()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            view_data("Authors")
        elif choice == "7":
            view_data("Books")
        elif choice == "8":
            view_data("Members")
        elif choice == "9":
            view_data("Transactions")
        elif choice == "10":
            view_data("Staff")
        elif choice == "0":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again!")

# Run the menu
menu()

# Close database connection
cursor.close()
db.close()

