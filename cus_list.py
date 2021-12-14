from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox
import psycopg2
from constants import *

class CusDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("Customer List Dashboard")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable
        self.var_id = IntVar()
        self.var_name = StringVar()
        self.var_num = StringVar()
        self.var_address = StringVar()

        # Cus List Dashboard Text 
        cus_list_text = Label(window, text='Customer List Dashboard',font=("Roboto Regular", 36), fg=self.main_white_color,bg=self.main_black_color)
        cus_list_text.place(x=0,y=0)

        # Frame 
        self.frame_for_tree = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_tree.place(x=10, y=70,relwidth=1, height=340)

        self.scrolly = Scrollbar(self.frame_for_tree, orient=VERTICAL)
        self.scrollx = Scrollbar(self.frame_for_tree, orient=HORIZONTAL)
        #Treeview
        self.cus_list_tree = ttk.Treeview(self.frame_for_tree,
                columns=("id", "name", "num", "address"), show='headings', yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set )

        self.cus_list_tree['selectmode'] = 'browse'

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.scrolly.config(command=self.cus_list_tree.yview)
        self.scrollx.config(command=self.cus_list_tree.xview)

        self.cus_list_tree.heading('id', text="Customer Id")
        self.cus_list_tree.heading('name', text="Customer Name")
        self.cus_list_tree.heading('num', text="Customer Number")
        self.cus_list_tree.heading('address', text="Address")
        
        
        self.cus_list_tree.pack(fill=BOTH, expand=1)

        self.cus_list_tree.column('id', width=20)
        self.cus_list_tree.column('name', width=100)
        self.cus_list_tree.column('num', width=100)
        self.cus_list_tree.column('address', width=200)
        

        self.cus_list_tree.bind("<ButtonRelease-1>", self.get_cus_data_fun)
        self.show_cus_fun()

        # Add Customer List 
        self.frame_for_cus = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_cus.place(x=10, y=420,relwidth=1, height=280)

        # ============================Customer Name====================================
        cus_name_label = Label(self.frame_for_cus, text="Customer Name: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        cus_name_label.grid(row=0,column=0,padx=40,pady=20)

        self.cus_name_entry = Entry(self.frame_for_cus,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_name)
        self.cus_name_entry.grid(row=0,column=1,padx=0,pady=20)

        # ============================Customer Number====================================
        cus_num_label = Label(self.frame_for_cus, text="Customer Number: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        cus_num_label.grid(row=0,column=2,padx=40,pady=20)

        self.cus_num_entry = Entry(self.frame_for_cus,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_num)
        self.cus_num_entry.grid(row=0,column=3,padx=0,pady=20)

        # ============================Customer Address====================================
        cus_add_label = Label(self.frame_for_cus, text="Customer Address: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        cus_add_label.grid(row=1,column=0,padx=40,pady=20)

        self.cus_add_entry = Entry(self.frame_for_cus,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),textvariable=self.var_address)
        self.cus_add_entry.grid(row=1,column=1,padx=0,pady=20)

        # ============================Customer Id====================================
        cus_id_label = Label(self.frame_for_cus, text="Customer Id: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        cus_id_label.grid(row=1,column=2,padx=40,pady=20)

        self.cus_id = Label(self.frame_for_cus, text="{self.var_id}", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"),textvariable=self.var_id)
        self.cus_id.grid(row=1,column=3,padx=0,pady=20)

        # ============================Buttons Lot of Buttons ============================
        self.save_prod_btn = Button(self.frame_for_cus, text='Save',
                            cursor='hand2',fg=self.main_white_color,
                            command=self.add_cus_func,                   
                            bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.save_prod_btn.place(x=450, y=220, width=120,height=40)

        self.update_prod_btn = Button(self.frame_for_cus, text='Update',
                                cursor='hand2',fg=self.main_white_color,   
                                command=self.upd_cus_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.update_prod_btn.place(x=600, y=220, width=120,height=40)

        self.del_prod_btn = Button(self.frame_for_cus, text='Delete',
                                cursor='hand2',fg=self.main_white_color,  
                                command=self.del_cus_func,                 
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.del_prod_btn.place(x=750, y=220, width=120,height=40)

        self.clear_prod_btn = Button(self.frame_for_cus, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_cus_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.clear_prod_btn.place(x=900, y=220, width=120,height=40)

        self.dashboard_btn = Button(self.frame_for_cus, text='Dashboard',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.go_to_dashboard_func,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.dashboard_btn.place(x=1050, y=220, width=120,height=40)

    def get_cus_data_fun(self, ev):
        f = self.cus_list_tree.focus()
        content = (self.cus_list_tree.item(f))
        row = content['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_num.set(row[2])
        self.var_address.set(row[3])

    def show_cus_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM customer')
            rows_db = cur.fetchall()
            self.cus_list_tree.delete(*self.cus_list_tree.get_children())
            for row in rows_db:
                self.cus_list_tree.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def add_cus_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_name.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute("""
                INSERT INTO customer (name,num,address)
                VALUES (%s,%s,%s)
                """, (
                    self.var_name.get().capitalize(),
                    self.var_num.get(),
                    self.var_address.get()
                    )
                )
                con.commit()
            
            messagebox.showinfo('Success', f'{self.var_name.get().capitalize()} has been added', parent=self.window)
            self.clear_cus_fun()
            self.show_cus_fun()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def upd_cus_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_id.get() =='0' or self.var_name.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute('SELECT * FROM customer where id=%s', (self.var_id.get(),))
                row_db = cur.fetchone()
                if row_db == None:
                    messagebox.showerror('Error', f'Invalid Customer ID.', parent=self.window)
                else:
                    cur.execute("""
                        UPDATE customer SET 
                        name=%s,
                        num=%s,
                        address=%s,
                        WHERE id = %s
                        """, (
                            self.var_name.get().capitalize(),
                            self.var_num.get(),
                            self.var_address.get(),
                            self.var_id.get(),
                            )
                        )
                    con.commit()
                
                messagebox.showinfo('Success', f'Customer has been updated.', parent=self.window)
                self.clear_cus_fun()
                self.show_cus_fun()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def del_cus_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM customer where id=%s', (self.var_id.get(),))
            row_db = cur.fetchone()
            if row_db == None:
                messagebox.showerror('Error', f'Invalid Customer ID.', parent=self.window)
            else:
                yes_no = messagebox.askyesno('Are you Sure?', f'Sure to Delete {self.var_name.get().capitalize()} of Id {self.var_id.get()}?', parent=self.window)
                if yes_no:
                    cur.execute("DELETE FROM customer where id=%s",(self.var_id.get(),))
                    con.commit()
                    self.clear_cus_fun()
                    self.show_cus_fun()
                else:
                    messagebox.showinfo('Not deleted', f'{self.var_name.get().capitalize()} is not deleted :)', parent=self.window)
                    self.show_cus_fun()
                
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)


    def clear_cus_fun(self):
        self.var_id.set(0),
        self.var_name.set(''),
        self.var_num.set(''),
        self.var_address.set(''),
        
        self.deselect_tree_item(self.cus_list_tree)

    def go_to_dashboard_func(self):
        self.window.destroy()

    def deselect_tree_item(self, tree_name):
        tree_name.selection_remove(tree_name.selection())
