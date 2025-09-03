import tkinter as tk

# 🔢 Calculate function
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except ZeroDivisionError:
        entry.delete(0, tk.END)
        entry.insert(0, "Cannot divide by 0")
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# 🧹 Clear function
def clear():
    entry.delete(0, tk.END)

# 🖊 Button click
def press(key):
    entry.insert(tk.END, key)

# 🪟 Window setup
window = tk.Tk()
window.title("Simple Calculator")

entry = tk.Entry(window, width=25, font=('Arial', 18), borderwidth=5, relief=tk.RIDGE, justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# 🧮 Buttons
buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
    ('0',4,0), ('.',4,1), ('+',4,2), ('=',4,3),
    ('C',5,0)
]

for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(window, text=text, width=5, height=2, command=calculate)
    elif text == 'C':
        btn = tk.Button(window, text=text, width=23, height=2, command=clear)
        btn.grid(row=row, column=col, columnspan=4, padx=5, pady=5)
        continue
    else:
        btn = tk.Button(window, text=text, width=5, height=2, command=lambda t=text: press(t))
    btn.grid(row=row, column=col, padx=5, pady=5)

window.mainloop()