from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox
import psycopg2
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from constants import *

class BillCheckDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window['bg'] = self.main_black_color
        self.window.title("Bill List Dashboard")
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable 
        self.var_from_date = StringVar()
        self.var_to_date = StringVar()

        self.var_search_bill_by = StringVar()
        self.var_search_bill_text = StringVar()

        self.var_search_invoice_num = IntVar()
        
        self.var_tot_sale_am = IntVar()
        self.var_tot_sale_pr = IntVar()
        self.var_tot_loss_pur_mode = IntVar()

        # Cus List Dashboard Text 
        bill_list_text = Label(window, text='Bill List Dashboard',font=("Roboto Regular", 36), fg=self.main_white_color,bg=self.main_black_color)
        bill_list_text.place(x=0,y=0)

        # Dashboard Btn 
        main_win_btn = Button(self.window, text='Dashboard',
                                cursor='hand2',fg=self.main_black_color, 
                                command=self.go_to_dashboard_func,                  
                                bg='white', font=('Roboto Regular', 14, "bold"),width=14)
        main_win_btn.place(x=1170, y=10)

        # Frame 
        self.frame_for_tree = Frame(self.window, bd=2, relief=RIDGE)
        self.frame_for_tree.place(x=10, y=70,relwidth=1, height=260)

        self.scrolly = Scrollbar(self.frame_for_tree, orient=VERTICAL)
        self.scrollx = Scrollbar(self.frame_for_tree, orient=HORIZONTAL)
        #Treeview
        self.bill_list_tree = ttk.Treeview(self.frame_for_tree,
                columns=("id", "cus_id", "pr_id","pr_name", "paid", "date", "pur_mode","rate","quantity","t_amount","inv_id"), show='headings', yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set )

        self.bill_list_tree['selectmode'] = 'browse'

        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=X)

        self.scrolly.config(command=self.bill_list_tree.yview)
        self.scrollx.config(command=self.bill_list_tree.xview)

        self.bill_list_tree.heading('id', text="Id")
        self.bill_list_tree.heading('cus_id', text="Customer Name")
        self.bill_list_tree.heading('pr_id', text="IMEI")
        self.bill_list_tree.heading('pr_name', text="Product Name")
        self.bill_list_tree.heading('paid', text="Paid")
        self.bill_list_tree.heading('date', text="Date")
        self.bill_list_tree.heading('pur_mode', text="Pur Mode")
        self.bill_list_tree.heading('rate', text="Rate")
        self.bill_list_tree.heading('quantity', text="Quantity")
        self.bill_list_tree.heading('t_amount', text="T.Amount")
        self.bill_list_tree.heading('inv_id', text="Invoice No")
        
        
        self.bill_list_tree.pack(fill=BOTH, expand=1)

        self.bill_list_tree.column('id', width=20)
        self.bill_list_tree.column('cus_id', width=100)
        self.bill_list_tree.column('pr_id', width=100)
        self.bill_list_tree.column('pr_name', width=100)
        self.bill_list_tree.column('paid', width=50)
        self.bill_list_tree.column('date', width=50)
        self.bill_list_tree.column('pur_mode', width=100)
        self.bill_list_tree.column('rate', width=100)
        self.bill_list_tree.column('quantity', width=50)
        self.bill_list_tree.column('t_amount', width=100)
        self.bill_list_tree.column('inv_id', width=20)
        

        self.bill_list_tree.bind("<ButtonRelease-1>", self.get_bill_data)
        self.show_bill_func()

        # Invoice DETAILS FORM FRAME 
        self.bill_details_frame = LabelFrame(self.window,bd=2,text='Search Invoice Details', relief=FLAT)        
        self.bill_details_frame.place(x=40, y=340, width=580, height=90)

        search_txt_label = Label(self.bill_details_frame, text='Invoice No: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))

        search_txt_label.grid(row=0, column=0,padx=20,pady=10)

        self.search_txt_entry = Entry(self.bill_details_frame,relief=SUNKEN, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),
                                    textvariable=self.var_search_invoice_num
                                    )
        self.search_txt_entry.grid(row=0,column=1,padx=0,pady=10)

        self.search_cus_btn = Button(self.bill_details_frame, text='Search Bill',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.search_invoice_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "bold"))
        self.search_cus_btn.grid(row=0,column=2,padx=20,pady=10)

        self.search_cus_btn = Button(self.bill_details_frame, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_invoice_func,              
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.search_cus_btn.grid(row=0,column=3,padx=0,pady=10)

        # Bill Filters FORM FRAME 
        self.bill_filters_frame = LabelFrame(self.window,bd=2,text='Bill Filters', relief=FLAT)        
        self.bill_filters_frame.place(x=640, y=340, width=680, height=90)

        self.search_prod_select = ttk.Combobox(self.bill_filters_frame,
                                values=("Select By","Product Name", "IMEI","Cus Name","Purchase Mode"),
                                state='readonly', justify=CENTER,
                                font=('Roboto Regular', 14, "normal"),
                                textvariable=self.var_search_bill_by
                                )
        self.search_prod_select.grid(row=0, column=0,padx=20,pady=10)
        self.search_prod_select.current(0)

        self.search_prod_txt_entry = Entry(self.bill_filters_frame,relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),
                                    textvariable=self.var_search_bill_text
                                    )
        self.search_prod_txt_entry.grid(row=0,column=1,padx=0,pady=10)

        self.search_cus_btn = Button(self.bill_filters_frame, text='Search Bill',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.search_bill_filter_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "bold"))
        self.search_cus_btn.grid(row=0,column=2,padx=10,pady=10)

        self.search_cus_btn = Button(self.bill_filters_frame, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_bill_filter_func,              
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.search_cus_btn.grid(row=0,column=3,padx=0,pady=10)

        # Invoice DETAILS FORM FRAME 
        self.date_filter_frame = LabelFrame(self.window,bd=2,text='Filter Date in Bill Details', relief=FLAT)        
        self.date_filter_frame.place(x=40, y=440, width=780, height=90)

        from_date_label = Label(self.date_filter_frame, text='From: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))

        from_date_label.place(x=20, y=10,width=60, height=30)

        self.from_date_search = Entry(self.date_filter_frame,relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),
                                    textvariable=self.var_from_date
                                    )
        self.from_date_search.place(x=100, y=10,width=120, height=30)

        to_date_label = Label(self.date_filter_frame, text='To: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))

        to_date_label.place(x=240, y=10,width=60, height=30)

        self.to_date_search = Entry(self.date_filter_frame,relief=SUNKEN,
                                    bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12),
                                    textvariable=self.var_to_date
                                    )
        self.to_date_search.place(x=320, y=10,width=120, height=30)

        self.from_to_search_btn = Button(self.date_filter_frame, text='Search',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.search_from_to_bill,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "bold"))
        self.from_to_search_btn.place(x=460, y=5,width=120, height=40)

        self.clear_from_to_search_btn = Button(self.date_filter_frame, text='Clear',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.clear_search_from_to_bill,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.clear_from_to_search_btn.place(x=600, y=5,width=100, height=40)

        help_date_label = Label(self.date_filter_frame, text='Note:- Date format should be MM/DD/YYYY or YYYY-DD-MM ', fg="#4f4e4d",
                                    font=("yu gothic ui", 11, "bold"))

        help_date_label.place(x=0, y=50,relwidth=1, height=20)

        # Button Bill FRAME 
        self.button_bill_frame = LabelFrame(self.window,bd=2,text='Bill Buttons', relief=FLAT)        
        self.button_bill_frame.place(x=840, y=440, width=480, height=90)

        self.show_all_bill_btn = Button(self.button_bill_frame, text='Show All',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.show_bill_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.show_all_bill_btn.place(x=10, y=15,width=120, height=40)

        self.last_day_profit_btn = Button(self.button_bill_frame, text='Last Day Sale',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.last_day_sale_func,                
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.last_day_profit_btn.place(x=150, y=15,width=160, height=40)


        self.today_sale_btn = Button(self.button_bill_frame, text='Today Sale',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.today_sale_func,              
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"))
        self.today_sale_btn.place(x=330, y=15,width=120, height=40)

        # Profit and Loss FORM FRAME 
        self.profit_loss_frame = LabelFrame(self.window,bd=2,text='Profit Loss Frame', relief=FLAT)        
        self.profit_loss_frame.place(x=40, y=540, width=1280, height=140)

        total_sale_am_label = Label(self.profit_loss_frame, text='Total Sale Amount: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        total_sale_am_label.place(x=10, y=10)

        self.total_sale_am_entry = Label(self.profit_loss_frame,textvariable=self.var_tot_sale_am, fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        self.total_sale_am_entry.place(x=200, y=10)
        self.total_sale_amount_func()

        tot_pr_direct_label = Label(self.profit_loss_frame, text='Total Profit: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        tot_pr_direct_label.place(x=360, y=10)

        self.tot_pr_direct_entry = Label(self.profit_loss_frame,textvariable=self.var_tot_sale_pr, fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        self.tot_pr_direct_entry.place(x=500, y=10)

        loss_other_pur_mode_label = Label(self.profit_loss_frame, text='Loss in Other Purchase Mode: ',bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 14, "bold"))
        
        loss_other_pur_mode_label.place(x=660, y=10)

        self.loss_other_pur_mode_entry = Label(self.profit_loss_frame,textvariable=self.var_tot_loss_pur_mode, fg="#4f4e4d",
                                    font=("Roboto Regular", 14, "bold"))
        self.loss_other_pur_mode_entry.place(x=940, y=10)
        self.tot_loss_pur_mode_func()
        self.tot_sale_pr_am_func()

    def go_to_dashboard_func(self):
        self.window.destroy()

    def show_bill_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM bill')
            rows_db = cur.fetchall()
            self.bill_list_tree.delete(*self.bill_list_tree.get_children())
            # "id", "cus_id", "pr_id","pr_name", "paid", "date", "pur_mode","rate","quantity","t_amount"
            for row in rows_db:
                cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                cs_det_row = cur.fetchone()
                cur.execute('SELECT * FROM inventory WHERE id=%s',(row[2], )) 
                pr_det_row = cur.fetchone()
                cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                pay_det_row = cur.fetchone()
                self.bill_list_tree.insert('', END, values=(
                    row[0],
                    cs_det_row[1],
                    row[2],
                    pr_det_row[1],
                    row[3],
                    row[4],
                    pay_det_row[1],
                    pr_det_row[4],
                    row[5],
                    pr_det_row[4] * row[5],
                    row[7]
                    ))
            self.total_sale_amount_func()
            self.tot_sale_pr_am_func()
            self.tot_loss_pur_mode_func()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def search_from_to_bill(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_from_date.get()=='' and self.var_to_date.get()=='':
                messagebox.showerror("Field can't be empty", "Please input a date.", parent=self.window)
            elif self.var_from_date.get()=='':
                cur.execute('SELECT * FROM bill FETCH FIRST ROW ONLY;')
                first_row = cur.fetchone()
                cur.execute("""SELECT * FROM bill WHERE date BETWEEN %s AND %s""",(
                    first_row[4],
                    self.var_to_date.get()
                ))
                all_rows = cur.fetchall()
                if all_rows!=[]:
                    self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                    # Also Changing Profit Loss And Total Sale 
                    tot_sale_pr_am = 0
                    total_sale_amount = 0
                    loss_other_pur_mode = 0
                    for row in all_rows:
                        cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                        cs_det_row = cur.fetchone()
                        cur.execute('SELECT * FROM inventory WHERE id=%s',(row[2], )) 
                        pr_det_row = cur.fetchone()
                        cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                        pay_det_row = cur.fetchone()
                        self.bill_list_tree.insert('', END, values=(
                            row[0],
                            cs_det_row[1],
                            row[2],
                            pr_det_row[1],
                            row[3],
                            row[4],
                            pay_det_row[1],
                            pr_det_row[4],
                            row[5],
                            pr_det_row[4] * row[5],
                            row[7]
                            ))
                        # Total Sale Count 
                        total_sale = pr_det_row[4] * row[5]
                        total_sale_amount += total_sale
                        # Sale Profit Count 
                        prof_amount = pr_det_row[4] - pr_det_row[3]
                        sale_profit = row[5]*prof_amount
                        tot_sale_pr_am += sale_profit
                        # Loss Count 
                        loss_amount = float(pr_det_row[4]*(pay_det_row[2]/100))
                        tot_loss_amount=row[5]*loss_amount
                        loss_other_pur_mode += tot_loss_amount
                    round_up_two_tot_am = round(loss_other_pur_mode, 2)
                    self.var_tot_loss_pur_mode.set(round_up_two_tot_am)
                    self.var_tot_sale_pr.set((tot_sale_pr_am-self.var_tot_loss_pur_mode.get()))
                    self.var_tot_sale_am.set(total_sale_amount)
                
            elif self.var_to_date.get()=='':
                cur.execute('SELECT * FROM bill ORDER BY id DESC LIMIT 1;')
                last_row = cur.fetchone()
                cur.execute("""SELECT * FROM bill WHERE date BETWEEN %s AND %s""",(
                    self.var_from_date.get(),
                    last_row[4]
                ))
                all_rows = cur.fetchall()
                if all_rows!=[]:
                    # Also Changing Profit Loss And Total Sale 
                    tot_sale_pr_am = 0
                    total_sale_amount = 0
                    loss_other_pur_mode = 0
                    self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                    for row in all_rows:
                        cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                        cs_det_row = cur.fetchone()
                        cur.execute('SELECT * FROM inventory WHERE id=%s',(row[2], )) 
                        pr_det_row = cur.fetchone()
                        cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                        pay_det_row = cur.fetchone()
                        self.bill_list_tree.insert('', END, values=(
                            row[0],
                            cs_det_row[1],
                            row[2],
                            pr_det_row[1],
                            row[3],
                            row[4],
                            pay_det_row[1],
                            pr_det_row[4],
                            row[5],
                            pr_det_row[4] * row[5],
                            row[7]
                            ))
                        # Total Sale Count 
                        total_sale = pr_det_row[4] * row[5]
                        total_sale_amount += total_sale
                        # Sale Profit Count 
                        prof_amount = pr_det_row[4] - pr_det_row[3]
                        sale_profit = row[5]*prof_amount
                        tot_sale_pr_am += sale_profit
                        # Loss Count 
                        loss_amount = float(pr_det_row[4]*(pay_det_row[2]/100))
                        tot_loss_amount=row[5]*loss_amount
                        loss_other_pur_mode += tot_loss_amount
                    round_up_two_tot_am = round(loss_other_pur_mode, 2)
                    self.var_tot_loss_pur_mode.set(round_up_two_tot_am)
                    self.var_tot_sale_pr.set((tot_sale_pr_am-self.var_tot_loss_pur_mode.get()))
                    self.var_tot_sale_am.set(total_sale_amount)

                else:
                    messagebox.showerror('No Data Exist', f'No data in between {self.var_from_date.get()} till date', parent=self.window)
            else:
                cur.execute("""SELECT * FROM bill WHERE date BETWEEN %s AND %s""",(
                    self.var_from_date.get(),
                    self.var_to_date.get()
                ))
                all_rows = cur.fetchall()
                if all_rows!=[]:
                    # Also Changing Profit Loss And Total Sale 
                    tot_sale_pr_am = 0
                    total_sale_amount = 0
                    loss_other_pur_mode = 0
                    self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                    for row in all_rows:
                        cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                        cs_det_row = cur.fetchone()
                        cur.execute('SELECT * FROM inventory WHERE id=%s',(row[2], )) 
                        pr_det_row = cur.fetchone()
                        cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                        pay_det_row = cur.fetchone()
                        self.bill_list_tree.insert('', END, values=(
                            row[0],
                            cs_det_row[1],
                            row[2],
                            pr_det_row[1],
                            row[3],
                            row[4],
                            pay_det_row[1],
                            pr_det_row[4],
                            row[5],
                            pr_det_row[4] * row[5],
                            row[7]
                            ))
                        # Total Sale Count 
                        total_sale = pr_det_row[4] * row[5]
                        total_sale_amount += total_sale
                        # Sale Profit Count 
                        prof_amount = pr_det_row[4] - pr_det_row[3]
                        sale_profit = row[5]*prof_amount
                        tot_sale_pr_am += sale_profit
                        # Loss Count 
                        loss_amount = float(pr_det_row[4]*(pay_det_row[2]/100))
                        tot_loss_amount=row[5]*loss_amount
                        loss_other_pur_mode += tot_loss_amount
                    round_up_two_tot_am = round(loss_other_pur_mode, 2)
                    self.var_tot_loss_pur_mode.set(round_up_two_tot_am)
                    self.var_tot_sale_pr.set((tot_sale_pr_am-self.var_tot_loss_pur_mode.get()))
                    self.var_tot_sale_am.set(total_sale_amount)
                else:
                    messagebox.showerror('No Data Exist', f'No data in between starting date and {self.var_to_date.get()}', parent=self.window)
            
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def search_bill_filter_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            if self.var_search_bill_by.get()=='Select By':
                messagebox.showwarning('Please Select', "Select an option", parent=self.window)
            elif self.var_search_bill_by.get()=='Product Name':
                cur.execute('SELECT * FROM inventory WHERE pr_name=%s', (self.var_search_bill_text.get().capitalize(),))
                inven_row = cur.fetchone()
                if inven_row is not None:
                    cur.execute('SELECT * FROM bill WHERE pr_id=%s',(inven_row[0],))
                    rows_db=cur.fetchall()
                    if rows_db!=[]:
                        self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                        for row in rows_db:
                            cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                            cs_det_row = cur.fetchone()
                            cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                            pay_det_row = cur.fetchone()
                            self.bill_list_tree.insert('', END, values=(
                                row[0],
                                cs_det_row[1],
                                row[2],
                                inven_row[1],
                                row[3],
                                row[4],
                                pay_det_row[1],
                                inven_row[4],
                                row[5],
                                inven_row[4] * row[5],
                                row[7]
                                ))
                    else:
                        messagebox.showinfo('No Matching Results', f'Nothing Matched in Bill With Product Name: {self.var_search_bill_text.get()}.', parent=self.window)
                        self.show_bill_func()
                else:
                    messagebox.showinfo('No Matching Results', f'Not a Valid Product Name: {self.var_search_bill_text.get()}.', parent=self.window)

            elif self.var_search_bill_by.get()=='IMEI':
                cur.execute('SELECT * FROM inventory WHERE id=%s', (int(self.var_search_bill_text.get()),))
                inven_row = cur.fetchone()
                if inven_row is not None:
                    cur.execute('SELECT * FROM bill WHERE pr_id=%s',(inven_row[0],))
                    rows_db=cur.fetchall()
                    if rows_db!=[]:
                        self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                        for row in rows_db:
                            cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                            cs_det_row = cur.fetchone()
                            cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                            pay_det_row = cur.fetchone()
                            self.bill_list_tree.insert('', END, values=(
                                row[0],
                                cs_det_row[1],
                                row[2],
                                inven_row[1],
                                row[3],
                                row[4],
                                pay_det_row[1],
                                inven_row[4],
                                row[5],
                                inven_row[4] * row[5],
                                row[7]
                                ))
                    else:
                        messagebox.showinfo('No Matching Results', f'Nothing Matched With IMEI: {self.var_search_bill_text.get()}.', parent=self.window)
                        self.show_bill_func()
                else:
                    messagebox.showinfo('No Matching Results', f'Not a Valid Product Name: {self.var_search_bill_text.get()}.', parent=self.window)

            elif self.var_search_bill_by.get()=='Cus Name':
                cur.execute('SELECT * FROM customer WHERE name=%s', (self.var_search_bill_text.get().capitalize(),))
                cus_row = cur.fetchone()
                if cus_row is not None:
                    cur.execute('SELECT * FROM bill WHERE cus_id=%s',(cus_row[0],))
                    rows_db=cur.fetchall()
                    if rows_db!=[]:
                        self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                        for row in rows_db:
                            cur.execute('SELECT * FROM inventory WHERE id=%s',(row[2], )) 
                            pr_det_row = cur.fetchone()
                            cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                            pay_det_row = cur.fetchone()
                            self.bill_list_tree.insert('', END, values=(
                                row[0],
                                cus_row[1],
                                row[2],
                                pr_det_row[1],
                                row[3],
                                row[4],
                                pay_det_row[1],
                                pr_det_row[4],
                                row[5],
                                pr_det_row[4] * row[5],
                                row[7]
                                ))
                    else:
                        messagebox.showinfo('No Matching Results', f'Nothing Matched in Bill With Customer Name: {self.var_search_bill_text.get().capitalize()}.', parent=self.window)
                        self.show_bill_func()
                else:
                        messagebox.showinfo('No Matching Results', f'No Customer Name Exists: {self.var_search_bill_text.get().capitalize()}.', parent=self.window)

            elif self.var_search_bill_by.get()=='Purchase Mode':
                cur.execute('SELECT * FROM paymode WHERE name=%s', (self.var_search_bill_text.get().capitalize(),))
                pur_row = cur.fetchone()
                if pur_row is not None:
                    cur.execute('SELECT * FROM bill WHERE pur_mode=%s',(pur_row[0],))
                    rows_db=cur.fetchall()
                    if rows_db!=[]:
                        self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                        for row in rows_db:
                            cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                            cs_det_row = cur.fetchone()
                            cur.execute('SELECT * FROM inventory WHERE id=%s',(row[2], )) 
                            pr_det_row = cur.fetchone()
                            cur.execute('SELECT * FROM paymode WHERE id=%s',(row[6], )) 
                            pay_det_row = cur.fetchone()
                            self.bill_list_tree.insert('', END, values=(
                                row[0],
                                cs_det_row[1],
                                row[2],
                                pr_det_row[1],
                                row[3],
                                row[4],
                                pay_det_row[1],
                                pr_det_row[4],
                                row[5],
                                pr_det_row[4] * row[5],
                                row[7]
                                ))
                    else:
                        messagebox.showinfo('No Matching Results', f'Nothing Matched With Purchase Mode: {self.var_search_bill_text.get().capitalize()}.', parent=self.window)
                        self.show_bill_func()
                else:
                    messagebox.showinfo('No Matching Results', f'No such Purchase Mode Exists: {self.var_search_bill_text.get().capitalize()}.', parent=self.window)

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def clear_bill_filter_func(self):
        self.var_search_bill_by.set('Select By')
        self.var_search_bill_text.set('')
        self.show_bill_func()

    def total_sale_amount_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            total_sale_amount = 0
            cur.execute('SELECT * FROM billdetails')
            all_bill_row = cur.fetchall()
            for row in all_bill_row:
                total_sale_amount += row[3]
            self.var_tot_sale_am.set(total_sale_amount)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def tot_sale_pr_am_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            tot_sale_pr_am = 0
            cur.execute('SELECT * FROM bill WHERE paid=%s', ('yes',))
            all_paid_bill = cur.fetchall()
            for row in all_paid_bill:
                cur.execute('SELECT * FROM inventory WHERE id=%s', (row[2], ))
                prod_row = cur.fetchone()
                prof_amount = prod_row[4] - prod_row[3]
                sale_profit = row[5]*prof_amount
                tot_sale_pr_am += sale_profit
            self.var_tot_sale_pr.set((tot_sale_pr_am-self.var_tot_loss_pur_mode.get()))
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def tot_loss_pur_mode_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            loss_other_pur_mode = 0
            cur.execute('SELECT * FROM bill WHERE paid=%s', ('yes',))
            all_paid_bill = cur.fetchall()
            for row in all_paid_bill:
                cur.execute('SELECT * FROM paymode WHERE id=%s', (row[6], ))
                pur_mode_row=cur.fetchone()
                cur.execute('SELECT * FROM inventory WHERE id=%s', (row[2], ))
                prod_row = cur.fetchone()
                loss_amount = float(prod_row[4]*(pur_mode_row[2]/100))
                tot_loss_amount=row[5]*loss_amount
                loss_other_pur_mode += tot_loss_amount

            round_up_two_tot_am = round(loss_other_pur_mode, 2)
            self.var_tot_loss_pur_mode.set(round_up_two_tot_am)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)
    
    def last_day_sale_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            tot_sale_pr_am = 0
            total_sale_amount = 0
            loss_other_pur_mode = 0
            crnt_date = datetime.now()
            prev_date = crnt_date + relativedelta(days=-1)
            prev_date_date = prev_date.strftime('%x')
            cur.execute('SELECT * FROM bill WHERE paid=%s AND date=%s', ('yes',prev_date_date))
            all_paid_bill = cur.fetchall()
            if all_paid_bill!=[]:
                self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                for row in all_paid_bill:
                    cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                    cs_det_row = cur.fetchone()
                    cur.execute('SELECT * FROM paymode WHERE id=%s', (row[6], ))
                    pur_mode_row=cur.fetchone()
                    cur.execute('SELECT * FROM inventory WHERE id=%s', (row[2], ))
                    prod_row = cur.fetchone()
                    self.bill_list_tree.insert('', END, values=(
                        row[0],
                        cs_det_row[1],
                        row[2],
                        prod_row[1],
                        row[3],
                        row[4],
                        pur_mode_row[1],
                        prod_row[4],
                        row[5],
                        prod_row[4] * row[5],
                        row[7]
                        ))
                    # Total Sale Count 
                    total_sale = prod_row[4] * row[5]
                    total_sale_amount += total_sale
                    # Sale Profit Count 
                    prof_amount = prod_row[4] - prod_row[3]
                    sale_profit = row[5]*prof_amount
                    tot_sale_pr_am += sale_profit
                    # Loss Count 
                    loss_amount = float(prod_row[4]*(pur_mode_row[2]/100))
                    tot_loss_amount=row[5]*loss_amount
                    loss_other_pur_mode += tot_loss_amount
                round_up_two_tot_am = round(loss_other_pur_mode, 2)
                self.var_tot_loss_pur_mode.set(round_up_two_tot_am)
                self.var_tot_sale_pr.set((tot_sale_pr_am-self.var_tot_loss_pur_mode.get()))
                self.var_tot_sale_am.set(total_sale_amount)
            else:
                messagebox.showerror('No sale!', 'No sales yesterday.', parent=self.window)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

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

    def today_sale_func(self):
        con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()
        try:
            tot_sale_pr_am = 0
            total_sale_amount = 0
            loss_other_pur_mode = 0
            crnt_date = datetime.now().strftime('%x')
            cur.execute('SELECT * FROM bill WHERE paid=%s AND date=%s', ('yes',crnt_date))
            all_paid_bill = cur.fetchall()
            if all_paid_bill!=[]:
                self.bill_list_tree.delete(*self.bill_list_tree.get_children())
                for row in all_paid_bill:
                    cur.execute('SELECT * FROM customer WHERE id=%s',(row[1], )) 
                    cs_det_row = cur.fetchone()
                    cur.execute('SELECT * FROM paymode WHERE id=%s', (row[6], ))
                    pur_mode_row=cur.fetchone()
                    cur.execute('SELECT * FROM inventory WHERE id=%s', (row[2], ))
                    prod_row = cur.fetchone()
                    self.bill_list_tree.insert('', END, values=(
                        row[0],
                        cs_det_row[1],
                        row[2],
                        prod_row[1],
                        row[3],
                        row[4],
                        pur_mode_row[1],
                        prod_row[4],
                        row[5],
                        prod_row[4] * row[5],
                        row[7]
                        ))
                    # Total Sale Count 
                    total_sale = prod_row[4] * row[5]
                    total_sale_amount += total_sale
                    # Sale Profit Count 
                    prof_amount = prod_row[4] - prod_row[3]
                    sale_profit = row[5]*prof_amount
                    tot_sale_pr_am += sale_profit
                    # Loss Count 
                    loss_amount = float(prod_row[4]*(pur_mode_row[2]/100))
                    tot_loss_amount=row[5]*loss_amount
                    loss_other_pur_mode += tot_loss_amount
                round_up_two_tot_am = round(loss_other_pur_mode, 2)
                self.var_tot_loss_pur_mode.set(round_up_two_tot_am)
                self.var_tot_sale_pr.set((tot_sale_pr_am-self.var_tot_loss_pur_mode.get()))
                self.var_tot_sale_am.set(total_sale_amount)  
            else:
                messagebox.showerror('No sale!', 'No sales today.', parent=self.window)
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

    def get_bill_data(self, ev):
        f = self.bill_list_tree.focus()
        content = (self.bill_list_tree.item(f))
        row = content['values']
        self.var_search_invoice_num.set(row[10])

    def clear_invoice_func(self):
        self.var_search_invoice_num.set(0)

    def clear_search_from_to_bill(self):
        self.var_from_date.set('')
        self.var_to_date.set('')