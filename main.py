# main.py

import tkinter as tk
from app.ui import MainApplicationWindow

def main():
    """
    Inicializa e executa a aplicação de interface gráfica.
    """
    root = tk.Tk()
    app = MainApplicationWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()