from tkinter import *
from PIL import Image, ImageTk
from all_prod_list import AllProdDash
from all_bill_list import BillCheckDash
from bill_win import BillDash
from check_inv import CheckInvDash
from cus_list import CusDash
from pay_mode import PayDash
from user_list import UserListDash
from constants import *

class AdminDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#ffffff'
        self.window['bg'] = self.main_black_color
        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Login Dashboard Text 
        self.window.title("Main Dashboard")
        admin_dash_text = Label(window, text='Main Dashboard',font=("Roboto Regular", 36),
                            fg=self.main_white_color,bg=self.main_black_color)
        admin_dash_text.place(x=0,y=0)
        # # Main Window Btn 
        main_win_btn = Button(self.window, text='Main Window',
                                cursor='hand2',fg=self.main_black_color,
                                command=self.bill_win_fun,                   
                                bg='white', font=('Roboto Regular', 16, "bold"),width=16)
        main_win_btn.place(x=1040, y=16)

        # Inventory  BUTTON
        self.prod_image_open = Image.open('images/cartim.png')
        self.prod_image_open = self.prod_image_open.resize((300, 250), Image.ANTIALIAS)
        self.prod_cart_img = ImageTk.PhotoImage(self.prod_image_open)

        self.prod_cart_btn = Button(window, image=self.prod_cart_img,
                                            cursor='hand2',command=self.all_prod_list,
                                            borderwidth=0,border=0,bg=self.main_black_color)
        self.prod_cart_btn.image = self.prod_cart_img
        self.prod_cart_btn.place(x=80, y=80)
        prod_dash_text = Label(window, text='Product List',
                            font=("Roboto Regular", 28),
                            fg=self.main_black_color,bg=self.main_white_color)
        prod_dash_text.place(x=120,y=270)

        # Add Payment BUTTON
        self.payment_image_open = Image.open('images/paymode.png')
        self.payment_image_open = self.payment_image_open.resize((300, 250), Image.ANTIALIAS)
        self.payment_cart_img = ImageTk.PhotoImage(self.payment_image_open)

        self.payment_cart_btn = Button(window, image=self.payment_cart_img,
                                            cursor='hand2',command=self.all_pay_list,
                                            borderwidth=0,border=0,bg=self.main_black_color)
        self.payment_cart_btn.image = self.payment_cart_img
        self.payment_cart_btn.place(x=520, y=80)
        payment_dash_text = Label(window, text='Payment List',
                            font=("Roboto Regular", 28),
                            fg=self.main_black_color,bg=self.main_white_color)
        payment_dash_text.place(x=560,y=270)

        # Users aka Employee  BUTTON
        self.user_image_open = Image.open('images/customerbox.png')
        self.user_image_open = self.user_image_open.resize((300, 250), Image.ANTIALIAS)
        self.user_cart_img = ImageTk.PhotoImage(self.user_image_open)

        self.user_cart_btn = Button(window, image=self.user_cart_img,
                                            cursor='hand2',command=self.all_user_list,
                                            borderwidth=0,border=0,bg=self.main_black_color)
        self.user_cart_btn.image = self.user_cart_img
        self.user_cart_btn.place(x=960, y=80)
        user_dash_text = Label(window, text='User List',
                            font=("Roboto Regular", 28),
                            fg=self.main_black_color,bg=self.main_white_color)
        user_dash_text.place(x=1040,y=270)

        # Bill BUTTON
        self.bill_image_open = Image.open('images/trnsbox.jpg')
        self.bill_image_open = self.bill_image_open.resize((300, 250), Image.ANTIALIAS)
        self.bill_cart_img = ImageTk.PhotoImage(self.bill_image_open)

        self.bill_cart_btn = Button(window, image=self.bill_cart_img,
                                            cursor='hand2',command=self.all_bill_list,
                                            borderwidth=0,border=0,bg=self.main_black_color)
        self.bill_cart_btn.image = self.bill_cart_img
        self.bill_cart_btn.place(x=80, y=400)
        bill_dash_text = Label(window, text='Bill List',
                            font=("Roboto Regular", 28),
                            fg=self.main_black_color,bg=self.main_white_color)
        bill_dash_text.place(x=160,y=590)
        
        # Customer  BUTTON
        self.customer_image_open = Image.open('images/customerbox.png')
        self.customer_image_open = self.customer_image_open.resize((300, 250), Image.ANTIALIAS)
        self.customer_cart_img = ImageTk.PhotoImage(self.customer_image_open)

        self.customer_cart_btn = Button(window, image=self.customer_cart_img,
                                            cursor='hand2',command=self.all_cus_list,
                                            borderwidth=0,border=0,bg=self.main_black_color)
        self.customer_cart_btn.image = self.customer_cart_img
        self.customer_cart_btn.place(x=520, y=400)
        customer_text = Label(window, text='Customer List',
                            font=("Roboto Regular", 28),
                            fg=self.main_black_color,bg=self.main_white_color)
        customer_text.place(x=560,y=590)
        
        # Check Invoice BUTTON
        self.check_inv_image_open = Image.open('images/billicon.jpg')
        self.check_inv_image_open = self.check_inv_image_open.resize((300, 250), Image.ANTIALIAS)
        self.check_inv_cart_img = ImageTk.PhotoImage(self.check_inv_image_open)

        self.check_inv_cart_btn = Button(window, image=self.check_inv_cart_img,
                                            cursor='hand2',command=self.check_inv,
                                            borderwidth=0,border=0,bg=self.main_black_color)
        self.check_inv_cart_btn.image = self.check_inv_cart_img
        self.check_inv_cart_btn.place(x=960, y=400)
        check_inv_text = Label(window, text='Check Invoice',
                            font=("Roboto Regular", 28),
                            fg=self.main_black_color,bg=self.main_white_color)
        check_inv_text.place(x=1000,y=590)
             
    def bill_win_fun(self):
        self.newWindow = Toplevel(self.window)
        self.app = BillDash(self.newWindow)

    def all_prod_list(self):
        self.newWindow = Toplevel(self.window)
        self.app = AllProdDash(self.newWindow)

    def all_pay_list(self):
        self.newWindow = Toplevel(self.window)
        self.app = PayDash(self.newWindow)

    def all_user_list(self):
        self.newWindow = Toplevel(self.window)
        self.app = UserListDash(self.newWindow)

    def all_bill_list(self):
        self.newWindow = Toplevel(self.window)
        self.app = BillCheckDash(self.newWindow)

    def all_cus_list(self):
        self.newWindow = Toplevel(self.window)
        self.app = CusDash(self.newWindow)

    def check_inv(self):
        self.newWindow = Toplevel(self.window)
        self.app = CheckInvDash(self.newWindow)