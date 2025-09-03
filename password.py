import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate password
def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showwarning("Invalid Input", "Password length must be at least 4.")
            return

        # Character sets
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special = string.punctuation

        all_chars = lower + upper + digits + special

        # Ensure complexity
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(special)
        ]

        password += random.choices(all_chars, k=length - 4)
        random.shuffle(password)

        result_var.set(''.join(password))

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x250")
root.config(bg="#f0f0f0")

# Title Label
tk.Label(root, text="Password Generator", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Length Entry
tk.Label(root, text="Enter Password Length:", font=("Helvetica", 12), bg="#f0f0f0").pack()
length_entry = tk.Entry(root, font=("Helvetica", 12), justify='center')
length_entry.pack(pady=5)

# Generate Button
tk.Button(root, text="Generate Password", command=generate_password,
          font=("Helvetica", 12), bg="#007acc", fg="white").pack(pady=10)

# Result Display
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, font=("Helvetica", 12), justify='center', state='readonly', width=30).pack(pady=5)

# Start the GUI
root.mainloop()