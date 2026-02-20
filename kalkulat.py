import tkinter as ttk

tlacidla = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("C", 4, 2), ("+", 4, 3),
    ("=", 5, 0, 2), ("**", 5, 3, 1), ("√", 5, 2, 1)
]

root = ttk.Tk()
root.title("Kalkulacka")
root.geometry("300x400")

entry_var = ttk.StringVar()
entry = ttk.Entry(root, textvariable=entry_var, font=("Arial", 20), justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

def sucet(a,b):
    return a+b
def rozdiel(a,b):
    return a-b
def sucin(a,b):
    return a*b
def mocnina(a,b):
    return a**b
def podiel(a,b):
    if b == 0:
        raise ValueError ("delenie 0")
    return a/b

def odmocnina(a):
    if a < 0:
        raise ValueError("odmocnina zo zaporneho cisla")
    return a ** 0.5

ops = {
    "**": mocnina,
    "*": sucin,
    "/": podiel,
    "+": sucet,
    "-": rozdiel
}

def key_pressed(event):
    entry_var.set(entry_var.get()+event.char)

root.bind("Key", key_pressed)

def pridaj_znak(znak):
    entry_var.set(entry_var.get() + str(znak))

def vycisti():
    entry_var.set("")

def pocitaj():
    data = []
    expr = entry_var.get()
    for op in ops:
        if op in expr:
            data = [ float (value) for value in expr.split(op)]
            try:
                entry_var.set(ops[op](data[0], data[1]))
            except ValueError as chyba:
                print(f"detekcia chyby: {chyba}")
            return
    if expr.startswith("√"):
        try:
            val = float(expr[1:])
            entry_var.set(odmocnina(val))
        except ValueError as chyba:
            print(f"detekcia chyby: {chyba}")
            
for btn in tlacidla:
    text = btn[0]
    row_id = btn[1]
    col_id = btn[2]
    if len(btn) == 4:
        col_span = btn[3]
    else:
        col_span = 1

    if text == "=":
        b = ttk.Button(root, text=text, font=("Arial", 18),bg="green", command=pocitaj)    
    elif text == "C":
        b = ttk.Button(root, text=text, font=("Arial", 18),bg="red", command=vycisti)    
    elif text == "√":
        b = ttk.Button(root, text=text, font=("Arial", 18), command=lambda: pridaj_znak("√"))
    else:
        b = ttk.Button(root, text=text, font=("Arial", 18), command=lambda t=text: pridaj_znak(t))
    b.grid(row=row_id, column=col_id, columnspan=col_span, sticky="NSEW", padx=5, pady=5)

for i in range(6):
    root.rowconfigure(i, weight=1)
for i in range(4):
    root.columnconfigure(i, weight=1)

root.mainloop()