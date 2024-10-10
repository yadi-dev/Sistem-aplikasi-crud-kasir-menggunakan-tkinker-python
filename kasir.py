import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='kasir_db'
    )
    return connection

def add_item(name, price, stock):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Item added successfully!")
    refresh_items()

def delete_item(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    
    if cursor.rowcount == 0:
        messagebox.showerror("Hadeh", "ID mu nggk ada atau salah goblok, nggak bisa hapus data.")
    else:
        conn.commit()
        messagebox.showinfo("Success", "Item deleted successfully!")
    
    cursor.close()
    conn.close()
    refresh_items()

def update_item(item_id, name, price, stock):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = %s, price = %s, stock = %s WHERE id = %s", (name, price, stock, item_id))
    
    if cursor.rowcount == 0:
        messagebox.showerror("Hadeh", "ID item tidak ditemukan, nggak bisa update data.")
    else:
        conn.commit()
        messagebox.showinfo("Success", "selamat berhasil perbarui data!")
    
    cursor.close()
    conn.close()
    refresh_items()

def refresh_items():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        no_data_label = ttk.Label(scrollable_frame, text="No data available", padding=10)
        no_data_label.pack(fill=tk.X, padx=10, pady=5)
    else:
        for item in rows:
            item_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            item_label = ttk.Label(
                item_frame,
                text=f"ID: {item['id']}\nName: {item['name']}\nPrice: ${item['price']:.2f}\nStock: {item['stock']}",
                style="Card.TLabel",
                justify=tk.LEFT,
                padding=10
            )
            item_label.pack(fill=tk.X)

def submit_item():
    name = name_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()
    if name and price and stock:
        try:
            price = float(price)
            stock = int(stock)
            add_item(name, price, stock)
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hadeh", "kasih masuk harga dan stok yang masuk akal goblok!")

def remove_item():
    item_id = id_entry.get()
    if item_id.isdigit():
        delete_item(int(item_id))
        id_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Hadeh", "ID mu salah goblok.")

def update_item_ui():
    item_id = id_entry.get()
    name = name_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()
    if item_id.isdigit() and name and price and stock:
        try:
            price = float(price)
            stock = int(stock)
            update_item(int(item_id), name, price, stock)
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hadeh", "harga atau stok nggk masuk akal.")
    else:
        messagebox.showerror("Hadeh", "kasih masuk data barunya goblok")

app = tk.Tk()
app.title("Kasir CRUD")
app.geometry("500x700")
app.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")

# Configure styles for buttons and entry fields
style.configure("TButton", padding=10, font=("Helvetica", 12))
style.configure("TEntry", padding=5, font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")

main_frame = ttk.Frame(app, padding="20 20 20 0")
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10, fill=tk.X)

name_label = ttk.Label(input_frame, text="Item Name:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

price_label = ttk.Label(input_frame, text="Item Price:")
price_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
price_entry = ttk.Entry(input_frame)
price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

stock_label = ttk.Label(input_frame, text="Item Stock:")
stock_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
stock_entry = ttk.Entry(input_frame)
stock_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

submit_button = ttk.Button(input_frame, text="Add Item", command=submit_item)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

action_frame = ttk.Frame(main_frame)
action_frame.pack(pady=10, fill=tk.X)

id_label = ttk.Label(action_frame, text="Item ID:")
id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
id_entry = ttk.Entry(action_frame)
id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

button_frame = ttk.Frame(action_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=5)

remove_button = ttk.Button(button_frame, text="Remove Item", command=remove_item)
remove_button.pack(side=tk.LEFT, padx=5)

update_button = ttk.Button(button_frame, text="Update Item", command=update_item_ui)
update_button.pack(side=tk.LEFT, padx=5)

item_frame = ttk.Frame(main_frame)
item_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Create a canvas with a scrollbar for the item list
canvas = tk.Canvas(item_frame)
scrollbar = ttk.Scrollbar(item_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

refresh_items()

app.mainloop()
