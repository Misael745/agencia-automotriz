# ui/main.py
import tkinter as tk
from ui.login_ui import LoginUI
from ui.menu_ui import MenuUI

def iniciar_sistema():
    root = tk.Tk()
    MenuUI(root)
    root.mainloop()

def main():
    root = tk.Tk()
    LoginUI(root, lambda: cerrar_e_iniciar(root))

    root.mainloop()

def cerrar_e_iniciar(ventana_login):
    ventana_login.destroy()
    iniciar_sistema()

if __name__ == "__main__":
    main()
