from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox
import psycopg2
from constants import *

class PayDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("600x600+40+10")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("Payment Dashboard")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable
        self.var_id = IntVar()
        self.var_name = StringVar()
        self.var_per = DoubleVar()

        # Prod List Dashboard Text 
        cus_list_text = Label(window, text='Payment List Dashboard',font=("Roboto Regular", 16), fg=self.main_white_color,bg=self.main_black_color)
        cus_list_text.place(x=0,y=0)

        # Frame 
        self.frame_for_tree = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_tree.place(x=10, y=40,relwidth=1, height=160)

        self.scrolly = Scrollbar(self.frame_for_tree, orient=VERTICAL)
        self.scrollx = Scrollbar(self.frame_for_tree, orient=HORIZONTAL)
        #Treeview
        self.cus_list_tree = ttk.Treeview(self.frame_for_tree,
                columns=("id", "name", "percentage"), show='headings', yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set )

        self.cus_list_tree['selectmode'] = 'browse'

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.scrolly.config(command=self.cus_list_tree.yview)
        self.scrollx.config(command=self.cus_list_tree.xview)

        self.cus_list_tree.heading('id', text="Id")
        self.cus_list_tree.heading('name', text="Payment Mode Name")
        self.cus_list_tree.heading('percentage', text="Percentage")
        
        self.cus_list_tree.pack(fill=BOTH, expand=1)

        self.cus_list_tree.column('id', width=20)
        self.cus_list_tree.column('name', width=100)
        self.cus_list_tree.column('percentage', width=200)
        

        self.cus_list_tree.bind("<ButtonRelease-1>", self.get_pay_mode_data)
        self.show_pay_mode_func()

        # Add Payment Mode List 
        self.frame_for_pay_mode = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_pay_mode.place(x=10, y=220,relwidth=1, height=360)

        # ============================Payment Mode Name====================================
        pay_name_label = Label(self.frame_for_pay_mode, text="Payment Mode Name: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        pay_name_label.grid(row=0,column=0,padx=40,pady=20)

        self.pay_name_entry = Entry(self.frame_for_pay_mode,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_name)
        self.pay_name_entry.grid(row=0,column=1,padx=0,pady=20)

        # ============================Payment Percentage====================================
        pay_percentage_label = Label(self.frame_for_pay_mode, text="Payment Percentage: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        pay_percentage_label.grid(row=1,column=0,padx=40,pady=20)

        self.pay_percentage_entry = Entry(self.frame_for_pay_mode,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_per)
        self.pay_percentage_entry.grid(row=1,column=1,padx=0,pady=20)

        # ============================Payment Mode Id====================================
        pay_id_label = Label(self.frame_for_pay_mode, text="Payment Mode Id: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        pay_id_label.grid(row=2,column=0,padx=40,pady=20)

        self.pay_id = Label(self.frame_for_pay_mode, text="{self.var_id}", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"),textvariable=self.var_id)
        self.pay_id.grid(row=2,column=1,padx=0,pady=20)

        # ============================Buttons Lot of Buttons ============================
        self.save_prod_btn = Button(self.frame_for_pay_mode, text='Save',
                            cursor='hand2',fg=self.main_white_color,
                            command=self.add_pay_mode_func,                   
                            bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.save_prod_btn.grid(row=3,column=0,padx=40,pady=20)

        self.update_prod_btn = Button(self.frame_for_pay_mode, text='Update',
                                cursor='hand2',fg=self.main_white_color,   
                                command=self.upd_pay_mode_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.update_prod_btn.grid(row=3,column=1,padx=40,pady=20)

        self.del_prod_btn = Button(self.frame_for_pay_mode, text='Delete',
                                cursor='hand2',fg=self.main_white_color,  
                                command=self.del_pay_mode_func,                 
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.del_prod_btn.grid(row=3,column=2,padx=40,pady=20)

        self.clear_prod_btn = Button(self.frame_for_pay_mode, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_pay_mode_func,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.clear_prod_btn.grid(row=4,column=0,padx=40,pady=20)

        self.dashboard_btn = Button(self.frame_for_pay_mode, text='Dashboard',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.go_to_dashboard_func,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.dashboard_btn.grid(row=4,column=1,padx=40,pady=20)

    def get_pay_mode_data(self, ev):
        f = self.cus_list_tree.focus()
        content = (self.cus_list_tree.item(f))
        row = content['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_per.set(row[2])

    def show_pay_mode_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM paymode')
            rows_db = cur.fetchall()
            self.cus_list_tree.delete(*self.cus_list_tree.get_children())
            for row in rows_db:
                self.cus_list_tree.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def add_pay_mode_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_name.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute("""
                INSERT INTO paymode (name,percentage)
                VALUES (%s,%s)
                """, (
                    self.var_name.get().capitalize(),
                    self.var_per.get()
                    )
                )
                con.commit()
            
            messagebox.showinfo('Success', f'{self.var_name.get().capitalize()} has been added', parent=self.window)
            self.clear_pay_mode_func()
            self.show_pay_mode_func()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def upd_pay_mode_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_id.get() =='0' or self.var_name.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute('SELECT * FROM paymode where id=%s', (self.var_id.get(),))
                row_db = cur.fetchone()
                if row_db == None:
                    messagebox.showerror('Error', f'Invalid Payment Mode ID.', parent=self.window)
                else:
                    cur.execute("""
                        UPDATE paymode SET 
                        name=%s, 
                        percentage=%s,
                        WHERE id=%s
                        """, (
                            self.var_name.get().capitalize(),
                            self.var_per.get(),
                            self.var_id.get()
                            )
                        )
                    con.commit()
                
                messagebox.showinfo('Success', f'Payment Mode has been updated.', parent=self.window)
                self.clear_pay_mode_func()
                self.show_pay_mode_func()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def del_pay_mode_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM paymode where id=%s', (self.var_id.get(),))
            row_db = cur.fetchone()
            if row_db == None:
                messagebox.showerror('Error', f'Invalid Payment Mode ID.', parent=self.window)
            else:
                yes_no = messagebox.askyesno('Are you Sure?', f'Sure to Delete {self.var_name.get().capitalize()} of Id {self.var_id.get()}?', parent=self.window)
                if yes_no:
                    cur.execute("DELETE FROM paymode where id=%s",(self.var_id.get(),))
                    con.commit()
                    self.clear_pay_mode_func()
                    self.show_pay_mode_func()
                else:
                    messagebox.showinfo('Not deleted', f'{self.var_name.get().capitalize()} is not deleted :)', parent=self.window)
                    self.show_pay_mode_func()
                
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)


    def clear_pay_mode_func(self):
        self.var_id.set(0),
        self.var_name.set(''),
        self.var_per.set(0.0)
        
        self.deselect_tree_item(self.cus_list_tree)

    def go_to_dashboard_func(self):
        self.window.destroy()

    def deselect_tree_item(self, tree_name):
        tree_name.selection_remove(tree_name.selection())
