import tkinter as tk

def main():
    frame = tk.Tk()
    frame.title("teste")
    label1 = tk.Label(frame, text="Insira o arquivo com código assembly.")
    label1.pack()
    teste_input = tk.Entry(frame)
    teste_input.pack()
    frame.mainloop()
main()