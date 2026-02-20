import tkinter as ttk

tlacidla = [
    ("7",1,0,1), ("8",1,1,1), ("9",1,2,1), ("/",1,3,1),
    ("4",2,0,1), ("5",2,1,1), ("6",2,2,1), ("*",2,3,1),
    ("1",3,0,1), ("2",3,1,1), ("3",3,2,1), ("-",3,3,1),
    ("0",4,0,1), (".",4,1,1), ("C",4,2,1), ("+",4,3,1),
    ("=",5,0,4)
]



print(f"List of buttons: {tlacidla}")

root = ttk.Tk()
root.title("Kalkulacka")
root.geometry("300x400")

entry_var = ttk.StringVar()
entry = ttk.Entry(root, textvariable=entry_var, font=("Arial",20),justify="left")
entry.grid(row=0, column=0, columnspan=4,padx=5, pady=5)
def pridaj_znak(znak):
    entry_var.set(entry_var.get() + str(znak))
def pocitaj():
    try:
        result = eval(entry_var.get())
        entry_var.set(str(result))
    except:
        entry_var.set("Error")
def vycisti():
   
    entry_var.set("")
for btn in tlacidla:
    text = btn[0]
    row_id = btn[1]
    col_id = btn[2]
    col_span = btn[3]
    
    if text == "=":    
        b=ttk.Button(root, text=text, font=("Arial",18),background="lightgreen", command=pocitaj)
    elif text == "C":
        b=ttk.Button(root, text=text, font=("Arial",18), background="red", command=vycisti)
    else:   
        b=ttk.Button(root, text=text, font=("Arial",18), command=lambda t=text: pridaj_znak(t))
    b.grid(row=row_id, column=col_id, columnspan=col_span, sticky="NSEW", padx=5, pady=5)

for i in range(6):
    root.rowconfigure(i,weight=1)
for i in range(4):
    root.columnconfigure(i, weight=1)

root.rowconfigure(0, weight=1)
root.mainloop()