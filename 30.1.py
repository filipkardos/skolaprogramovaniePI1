from cProfile import label
import tkinter as ttk # príkaz importuje knižnicu (vloží knižnicu do nášho skriptu pod skráteným názvom tk)
print(ttk.TkVersion) # vypíšeme do konzoly verziu knižnice
root = ttk.Tk() # vytvorenie novej inštancie (objektu, Tk() je konštruktor, teda funkcia pre inicializáciu objektu)
root.title("Main frame") # priradenie názvu(titulku) pre hlavný frame (metóda title berie ako parameter reťazec)
# reťazec je postupnosť znakov uzavretá v úvodzovkách (text)
root.geometry("1000x1000") # nastavenie veľkosti okna

entry = ttk.Entry(root)
entry.grid(pady=1000)

# funkcia, ktorá sa spustí po kliknutí.
def reakcia_tlacidla():
    text = entry.get()
    entry.config(text=f"Priklad: {text} , vysledok: {eval(text)}")

btn1 = ttk.Button(root, text="BT1", command=reakcia_tlacidla)
btn1.grid(row=5 ,column=5)

btn2 = ttk.Button(root, text="BT2", command=reakcia_tlacidla)
btn2.grid(row=10 ,column=10)

btn3 = ttk.Button(root, text="BT3", command=reakcia_tlacidla)
btn3.grid(row=20 ,column=15)

btn4 = ttk.Button(root, text="BT4", command=reakcia_tlacidla)
btn4.grid(row=30 ,column=20)

btn5 = ttk.Button(root, text="BT5", command=reakcia_tlacidla)
btn5.grid(row=40 ,column=25)

btn6 = ttk.Button(root, text="BT6", command=reakcia_tlacidla)
btn6.grid(row=50 ,column=30)

btn7 = ttk.Button(root, text="BT7", command=reakcia_tlacidla)
btn7.grid(row=60 ,column=35)

btn8 = ttk.Button(root, text="BT8", command=reakcia_tlacidla)
btn8.grid(row=70 ,column=40)

btn9 = ttk.Button(root, text="BT9", command=reakcia_tlacidla)
btn9.grid(row=80 ,column=45)

btn10 = ttk.Button(root, text="BT10", command=reakcia_tlacidla)
btn10.grid(row=90 ,column=50)

#label = ttk.Label(root, text="")
#label.pack(pady=10) # vykresli label s vertikálnou medzerou 10 pixelov
root.mainloop()
