import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
)
''')


# Function to add a new book record
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    try:
        year = int(entry_year.get())
        cursor.execute('''
        INSERT INTO books (title, author, year) VALUES (?, ?, ?)
        ''', (title, author, year))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        update_table()  # Refresh the table view
    except ValueError:
        messagebox.showerror("Invalid Input", "Year must be a number.")


# Function to view all book records in the table
def update_table():
    # Clear existing rows in the table
    for row in tree.get_children():
        tree.delete(row)

    # Fetch all books from the database
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    # Insert the book data into the table
    for book in books:
        tree.insert("", tk.END, values=book)


# Function to update a selected book record
def update_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a book to update.")
        return

    # Get the selected book's ID
    book_id = tree.item(selected_item)["values"][0]

    title = entry_title.get()
    author = entry_author.get()
    try:
        year = int(entry_year.get())
        cursor.execute('''
        UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?
        ''', (title, author, year, book_id))
        conn.commit()
        messagebox.showinfo("Success", "Book updated successfully!")
        update_table()  # Refresh the table view
    except ValueError:
        messagebox.showerror("Invalid Input", "Year must be a number.")


# Function to delete a selected book record
def delete_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a book to delete.")
        return

    # Get the selected book's ID
    book_id = tree.item(selected_item)["values"][0]
    cursor.execute('''
    DELETE FROM books WHERE id = ?
    ''', (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book deleted successfully!")
    update_table()  # Refresh the table view


# Function to populate the entry fields when a row is selected
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        # Get the selected row's data
        book_id, title, author, year = tree.item(selected_item)["values"]

        # Populate the entry fields with the selected row's data
        entry_book_id.delete(0, tk.END)
        entry_book_id.insert(0, book_id)
        entry_title.delete(0, tk.END)
        entry_title.insert(0, title)
        entry_author.delete(0, tk.END)
        entry_author.insert(0, author)
        entry_year.delete(0, tk.END)
        entry_year.insert(0, year)


# Function to display the About message
def show_about():
    messagebox.showinfo("About", "Book Records Application\nVersion 1.0\nDeveloped by Charlito C. Casalta\nSubject: FD IT 201 - Advance Programming 1 Graduate School (MIT/MSIT)\nInstructor: Edwin Murillo")


# Create the main window
window = tk.Tk()
window.title("Book Records Application")
window.configure(bg='#2e2e2e')

# Add custom styling for ttk widgets (Dark Mode)
style = ttk.Style(window)
style.configure("TButton",
                padding=6, relief="flat", background="#444444", foreground="black", font=("Segoe UI", 12, "bold"))
style.configure("TLabel",
                font=("Segoe UI", 10), background="#2e2e2e", foreground="white")
style.configure("TEntry",
                font=("Segoe UI", 10), padding=6, background="#444444", foreground="white")
style.configure("TTreeview",
                font=("Segoe UI", 10), rowheight=30, background="#333333", foreground="white")
style.configure("TScrollbar",
                background="#333333", troughcolor="#444444", width=10)

# Create a Menu bar
menu_bar = tk.Menu(window, bg="#333333", fg="white")
window.config(menu=menu_bar)

# Create 'Books' menu
books_menu = tk.Menu(menu_bar, tearoff=0, bg="#333333", fg="white")
menu_bar.add_cascade(label="Books", menu=books_menu)
books_menu.add_command(label="Add Book", command=lambda: window.deiconify())
books_menu.add_command(label="Exit", command=window.quit)

# Create 'About' menu
about_menu = tk.Menu(menu_bar, tearoff=0, bg="#333333", fg="white")
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=show_about)

# Create and place labels and entry fields
label_book_id = ttk.Label(window, text="Book ID (for update/delete):")
label_book_id.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_book_id = ttk.Entry(window)
entry_book_id.grid(row=0, column=1, padx=10, pady=5)

label_title = ttk.Label(window, text="Title:")
label_title.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_title = ttk.Entry(window)
entry_title.grid(row=1, column=1, padx=10, pady=5)

label_author = ttk.Label(window, text="Author:")
label_author.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_author = ttk.Entry(window)
entry_author.grid(row=2, column=1, padx=10, pady=5)

label_year = ttk.Label(window, text="Year:")
label_year.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_year = ttk.Entry(window)
entry_year.grid(row=3, column=1, padx=10, pady=5)

# Create and place buttons
button_add = ttk.Button(window, text="Add Book", command=add_book)
button_add.grid(row=4, column=0, padx=10, pady=10)

button_update = ttk.Button(window, text="Update Book", command=update_book)
button_update.grid(row=4, column=1, padx=10, pady=10)

button_delete = ttk.Button(window, text="Delete Book", command=delete_book)
button_delete.grid(row=5, column=0, padx=10, pady=10)

# Create Treeview to display books in a table format
tree = ttk.Treeview(window, columns=("ID", "Title", "Author", "Year"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Year", text="Year")

tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Add a scrollbar for the table
scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=6, column=2, sticky="ns")

# Bind the select event to populate the textboxes with the selected book's data
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Make the table row expand
window.grid_rowconfigure(6, weight=1)

# Start the application and populate the table with existing books
update_table()

# Dynamically set window size based on content
window.update_idletasks()  # Update the window's size before running
window.minsize(window.winfo_width(), window.winfo_height())  # Set the minimum size to be based on content

window.mainloop()

# Close the database connection when done
conn.close()
