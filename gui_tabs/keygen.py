import tkinter
from tkinter import ttk
import rsa.rsa as rsa
import rsa.common as common


def make_keygen_tab(tab_control):
    keygen = ttk.Frame(tab_control)
    tab_control.add(keygen, text='keygen')

    tkinter.Label(keygen, text="Public Key").grid(column=0, row=0)
    T = tkinter.Text(keygen, height=7, width=52)
    T.grid(column=0, row=1)

    tkinter.Label(keygen, text="Private Key").grid(column=0, row=2)
    T2 = tkinter.Text(keygen, height=7, width=52)
    T2.grid(column=0, row=3)

    def generate_action():
        new_keys = rsa.gen_keys(1024)
        T.insert(tkinter.INSERT, common.key_to_base64(new_keys['public']))
        T2.insert(tkinter.INSERT, common.key_to_base64(new_keys['private']))

    b1 = tkinter.Button(keygen, text="Generate key pair", command=generate_action)
    b1.grid(column=0, row=4)
