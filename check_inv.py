from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox
import psycopg2
from constants import *

class CheckInvDash:
    def __init__(self, window):
        self.window = window
        # self.username = username
        self.window.geometry("400x360+20+10")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("Check Invoice Dashboard")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable 
        self.var_search_invoice_num = IntVar()
        # Check Invoice Dashboard Text 
        cus_list_text = Label(self.window, text='Check Invoice Dashboard',font=("Roboto Regular", 16), fg=self.main_white_color,bg=self.main_black_color)
        cus_list_text.place(x=0,y=0)

        self.frame_for_inv = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_inv.place(x=10, y=40,relwidth=1, height=290)

        search_txt_label = Label(self.frame_for_inv, text='Invoice Number:',font=("Roboto Regular", 16), fg=self.main_white_color,bg=self.main_black_color)
        search_txt_label.place(x=60,y=20)

        self.search_txt_entry = Entry(self.frame_for_inv, relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 14),
                                    textvariable=self.var_search_invoice_num
                                    )
        self.search_txt_entry.place(x=60,y=60, width=280, height=40)

        self.search_cus_btn = Button(self.frame_for_inv, text='Search Bill',
                                cursor='hand2',
                                command=self.search_invoice_func,
                                fg=self.main_white_color,              
                                bg=self.main_black_color,                
                                font=('Roboto Regular', 14, "bold"))
        self.search_cus_btn.place(x=60,y=120, width=280 ,height=40)

        self.search_cus_btn = Button(self.frame_for_inv, text='Clear',
                                cursor='hand2',
                                command=self.clear_invoice_func,
                                fg=self.main_white_color,              
                                bg=self.main_black_color,
                                font=('Roboto Regular', 14, "normal"))
        self.search_cus_btn.place(x=60,y=180, width=280, height=40)

        self.dash_btn = Button(self.frame_for_inv, text='Dashboard',
                                cursor='hand2',
                                command=self.go_to_dashboard_func,
                                fg=self.main_white_color,              
                                bg=self.main_black_color,
                                font=('Roboto Regular', 14, "normal"))
        self.dash_btn.place(x=60,y=240, width=280, height=40)
        
    def search_invoice_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_search_invoice_num.get()=='' or self.var_search_invoice_num.get()=='0':
                messagebox.showerror('Enter Data', f'Please Enter Data', parent=self.window)
            else:
                cur.execute('SELECT * FROM billdetails WHERE id=%s',(self.var_search_invoice_num.get(), ))
                billdet_row = cur.fetchone()
                if billdet_row!=None:
                    import os
                    import webbrowser
                    cwd = f'{os.getcwd()}'
                    pdf = f'{billdet_row[4]}.pdf'
                    full_path = os.path.join(cwd, pdf)
                    webbrowser.open_new(f'file://{full_path}')
                else:
                    messagebox.showerror('No Data Found', f'No bill with {self.var_search_invoice_num.get()}', parent=self.window)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def clear_invoice_func(self):
        self.var_search_invoice_num.set(0)

    def go_to_dashboard_func(self):
        self.window.destroy()