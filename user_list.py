from tkinter import *
import tkinter.ttk as ttk
# from PIL import Image, ImageTk
from tkinter import messagebox
import psycopg2
from constants import *

class UserListDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("User List Dashboard")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable
        self.var_search_by = StringVar()
        self.var_search_by_val = StringVar()

        self.var_username = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_pass = StringVar()

        # Login Dashboard Text 
        admin_dash_text = Label(window, text='User List Dashboard',font=("Roboto Regular", 36), fg=self.main_white_color,bg=self.main_black_color)
        admin_dash_text.place(x=0,y=0)

        # Main Window Btn 
        main_win_btn = Button(self.window, text='Dashboard',
                                cursor='hand2',fg=self.main_black_color,
                                command=self.go_to_dashboard_func,                   
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        main_win_btn.place(x=1160, y=16)

        # Frame Search 
        self.search_frame = Frame(self.window, bd=2, relief=RIDGE)
        self.search_frame.place(x=10, y=80,relwidth=1,height=120)

        self.search_combo_select = ttk.Combobox(self.search_frame,
                                values=("Select By","Username","Email Id","Phone Number"),
                                state='readonly', justify=CENTER,
                                textvariable=self.var_search_by,
                                font=('Roboto Regular', 14, "normal")
                                )
        # self.search_combo_select.place(x=10, y=10, width=180)
        self.search_combo_select.grid(row=0, column=0,padx=40,pady=30)
        self.search_combo_select.current(0)

        self.search_txt_entry = Entry(self.search_frame,relief=SUNKEN,
                                            bg="white", fg="#6b6a69",
                                            textvariable=self.var_search_by_val,
                                            font=("yu gothic ui semibold", 12))
        self.search_txt_entry.grid(row=0,column=1,padx=0,pady=30)

        self.search_btn_search =Button(self.search_frame, text='Search',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.search_user_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=16)
        self.search_btn_search.grid(row=0, column=2,padx=40, pady=30)

        self.show_all_btn_search =Button(self.search_frame, text='Show All',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.show_user_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=16)
        self.show_all_btn_search.grid(row=0, column=3,padx=0,pady=30)

        # Frame 
        self.frame_for_tree = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_tree.place(x=10, y=220,relwidth=1, height=240)

        self.scrolly = Scrollbar(self.frame_for_tree, orient=VERTICAL)
        self.scrollx = Scrollbar(self.frame_for_tree, orient=HORIZONTAL)
        #Treeview
        self.main_list_tree = ttk.Treeview(self.frame_for_tree,
                columns=("username","email","phone","pass"), show='headings', yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)

        self.main_list_tree['selectmode'] = 'browse'

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.scrolly.config(command=self.main_list_tree.yview)
        self.scrollx.config(command=self.main_list_tree.xview)

        self.main_list_tree.heading('username', text="Username")
        self.main_list_tree.heading('email', text="Email Id")
        self.main_list_tree.heading('phone', text="Phone No")
        self.main_list_tree.heading('pass', text="Password")
        self.main_list_tree.pack(fill=BOTH, expand=1)

        self.main_list_tree.column('username', width=100)
        self.main_list_tree.column('email', width=100)
        self.main_list_tree.column('phone',width=100)
        self.main_list_tree.column('pass', width=100)

        self.main_list_tree.bind("<ButtonRelease-1>", self.get_user_data_fun)
        self.show_user_fun()

        self.frame_for_update = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_update.place(x=10, y=480,relwidth=1, height=220)

        # ============================Username====================================

        username_label = Label(self.frame_for_update, text="Username: ",
                                    bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        username_label.grid(row=0,column=0,padx=40,pady=20)

        self.username_entry = Entry(self.frame_for_update,relief=SUNKEN,
                                    textvariable=self.var_username,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12))
        self.username_entry.grid(row=0,column=1,padx=0,pady=20)
        # ============================Email====================================
        email_label = Label(self.frame_for_update, text="Email Id: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        email_label.grid(row=0,column=2,padx=40,pady=20)

        self.email_entry = Entry(self.frame_for_update, relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    textvariable=self.var_email,
                                    font=("yu gothic ui semibold", 12))
        self.email_entry.grid(row=0,column=3,padx=0,pady=20)
        # ============================Phone Num====================================
        phone_num_label = Label(self.frame_for_update, text="Phone Num: ",
                                    bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        phone_num_label.grid(row=1,column=0,padx=40,pady=20)

        self.phone_num_entry = Entry(self.frame_for_update, relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    textvariable=self.var_phone,
                                    font=("yu gothic ui semibold", 12))
        # self.cost_price_entry.place(x=1000, y=10, width=180)
        self.phone_num_entry.grid(row=1,column=1,padx=0,pady=20)

        # ============================Password====================================

        pass_label = Label(self.frame_for_update, text="Password: ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        # sell_price_label.place(x=730, y=260)
        pass_label.grid(row=1,column=2,padx=40,pady=20)

        self.pass_entry = Entry(self.frame_for_update, relief=SUNKEN,
                                bg="white", fg="#6b6a69",
                                textvariable=self.var_pass,
                                font=("yu gothic ui semibold", 12))
        # self.sell_price_entry.place(x=750, y=303, width=150)
        self.pass_entry.grid(row=1,column=3,padx=0,pady=20)

        # ============================Buttons====================================
        self.save_user_btn = Button(self.frame_for_update, text='Save',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.save_user_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.save_user_btn.place(x=840, y=150, width=90,height=40)

        self.update_user_btn = Button(self.frame_for_update, text='Update',
                                cursor='hand2',fg=self.main_white_color,    
                                command=self.update_user_fun,               
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.update_user_btn.place(x=940, y=150, width=90,height=40)

        self.del_user_btn = Button(self.frame_for_update, text='Delete',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.del_user_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.del_user_btn.place(x=1040, y=150, width=90,height=40)

        self.clear_user_btn = Button(self.frame_for_update, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_user_fun,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.clear_user_btn.place(x=1140, y=150, width=90,height=40)

    def save_user_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_username.get() == '' or self.var_pass.get() == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute('SELECT * FROM users where username=%s', (self.var_username.get(),))
                row_db = cur.fetchone()
                if row_db != None:
                    messagebox.showerror('Error', f'Username is already in use.', parent=self.window)
                else:
                    cur.execute("""
                    INSERT INTO users (username,email, phone, pass)
                    VALUES (%s,%s,%s,%s)
                    """, (
                        self.var_username.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_pass.get()
                        )
                    )
                    con.commit()
                    messagebox.showinfo('Success', f'{self.var_username.get()} has been added', parent=self.window)
                    self.show_user_fun()
                    self.clear_user_fun()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)


    def show_user_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM users')
            rows_db = cur.fetchall()
            self.main_list_tree.delete(*self.main_list_tree.get_children())
            for row in rows_db:
                self.main_list_tree.insert('', END, values=row[1:])

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)


    def get_user_data_fun(self, ev):
        f = self.main_list_tree.focus()
        content = (self.main_list_tree.item(f))
        row = content['values']
        self.var_username.set(row[0]),
        self.var_email.set(row[1]),
        self.var_phone.set(row[2]),
        self.var_pass.set(row[3]),

    def update_user_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_username == '' or self.var_location == '':
                messagebox.showerror('Empty Value', "Value could not be empty", parent=self.window)
            else:
                cur.execute('SELECT * FROM users where username=%s', (self.var_username.get(),))
                row_db = cur.fetchone()
                if row_db == None:
                    messagebox.showerror('Error', f'Invalid Username.', parent=self.window)
                else:
                    cur.execute("""
                    UPDATE users SET 
                    email=%s,
                    phone=%s,
                    pass=%s
                    WHERE username=%s
                    """, (
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_pass.get(),
                        self.var_username.get(),
                        )
                    )
                    con.commit()
                    messagebox.showinfo('Success', f'User {self.var_username.get()} has been updated.', parent=self.window)
                    self.show_user_fun()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)


    def del_user_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM users where username=%s', (self.var_username.get(),))
            row_db = cur.fetchone()
            if row_db == None:
                messagebox.showerror('Error', f'Invalid Username.', parent=self.window)
            else:
                yes_no = messagebox.askyesno('Are you Sure?', f'Sure to Delete {self.var_username.get()} ?', parent=self.window)
                if yes_no:
                    cur.execute("DELETE FROM users where username=%s",(self.var_username.get(),))
                    con.commit()
                    self.show_user_fun()
                else:
                    messagebox.showinfo('Not deleted', f'{self.var_username.get()} is not deleted :)', parent=self.window)
                    self.show_user_fun()
                
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def clear_user_fun(self):
        self.var_username.set(''),
        self.var_email.set(''),
        self.var_phone.set(''),
        self.var_pass.set(''),

    def search_user_fun(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_search_by.get()=='Select By':
                messagebox.showwarning('Please Select', "Select an option", parent=self.window)
            elif self.var_search_by.get()=='Username':
                cur.execute('SELECT * FROM users WHERE username=%s', (self.var_search_by_val.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row[1:])
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Username: {self.var_search_by_val.get()}.', parent=self.window)
            elif self.var_search_by.get()=='Email Id':
                cur.execute('SELECT * FROM users WHERE email=%s', (self.var_search_by_val.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row[1:])
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Email Id: {self.var_search_by_val.get()}.', parent=self.window)
            elif self.var_search_by.get()=='Phone Number':
                cur.execute('SELECT * FROM users WHERE phone=%s', (self.var_search_by_val.get(),))
                rows_db = cur.fetchall()
                if rows_db!=[]:
                    self.main_list_tree.delete(*self.main_list_tree.get_children())
                    for row in rows_db:
                        self.main_list_tree.insert('', END, values=row[1:])
                else:
                    messagebox.showinfo('No Matching Results', f'Nothing Matched With Phone Number: {self.var_search_by_val.get()}.', parent=self.window)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}',parent=self.window)
 
    def go_to_dashboard_func(self):
        self.window.destroy()