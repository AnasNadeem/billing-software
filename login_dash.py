from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from admin_dash import AdminDash
import psycopg2
from constants import *

class LoginDash:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x720+0+0")
        self.main_black_color = '#0f0f0f'
        self.main_white_color = '#f8f8f8'
        self.window.title("Login Dashboard")
        self.login_frame = ImageTk.PhotoImage \
                (file='images\\login_frame_img.png')
        self.image_panel = Label(self.window, image=self.login_frame)

        self.image_panel.pack(fill='both')

        # self.window.iconbitmap("")
        self.window.resizable(False, False)

        # Defining Variable
        self.var_user_login = StringVar()
        self.var_user_pass = StringVar()
        # Login Dashboard Text 
        login_dash_text = Label(window, text='Login Dashboard', 
                                    font=("Roboto Regular", 36),
                                    fg=self.main_white_color, bg=self.main_black_color)
        login_dash_text.place(x=0,y=0)

        # ============================Username====================================
        username_label = Label(self.window, text="Username ", bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        username_label.place(x=495, y=220)

        self.username_entry = Entry(self.window, highlightthickness=0,
                                    textvariable=self.var_user_login,
                                    relief=FLAT, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12))
        self.username_entry.place(x=530, y=255, width=380)

        # User and Pass LOGO 
        self.user_image_open = Image.open('images/user.png')
        self.user_image_open = self.user_image_open.resize((20, 20), Image.ANTIALIAS)
        self.user_image = ImageTk.PhotoImage(self.user_image_open)

        self.user_image_label = Label(self.window, image=self.user_image,bg='white')
        self.user_image_label.image = self.user_image
        self.user_image_label.place(x=500, y=255)

        self.pass_image_open = Image.open('images/pass.png')
        self.pass_image_open = self.pass_image_open.resize((20, 20), Image.ANTIALIAS)
        self.pass_image = ImageTk.PhotoImage(self.pass_image_open)

        self.pass_image_label = Label(self.window, image=self.pass_image)
        self.pass_image_label.image = self.pass_image
        self.pass_image_label.place(x=500, y=370)
        
        # ============================Password====================================
        password_label = Label(self.window, text="Password ",
                                    bg="white", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        password_label.place(x=495, y=335)

        self.password_entry = Entry(self.window, highlightthickness=0, 
                                    textvariable=self.var_user_pass,
                                    relief=FLAT, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui semibold", 12), show="*")
        self.password_entry.place(x=530, y=370, width=355)

        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.window, image=self.show_image, relief=FLAT,
                                  activebackground="white", command=self.show
                                  ,borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=890, y=377)

        # ============================Login button================================
        self.login_button = Button(self.window, text='Login',
                                cursor='hand2',fg=self.main_white_color,
                                command=self.login_func,                   
                                bg=self.main_black_color, font=('Roboto Regular', 14, "normal"),width=16)
        self.login_button.place(x=620, y=450)

        # self.password_entry.bind('<Return>',self.login_func)
        # ============================Forgot password=============================
        # self.forgot_button = Button(self.window, text="Forgot Password?",
        #                             font=("yu gothic ui", 13, "bold underline"), fg="red", relief=FLAT,
        #                             activebackground="white"
        #                             , borderwidth=0, background="white", cursor="hand2")
        # self.forgot_button.place(x=767, y=410)

    # Command Function 
    def show(self):
        """allow user to show the password in password field"""
        self.hide_button = Button(self.window, image=self.hide_image, command=self.hide, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=890, y=377)
        self.password_entry.config(show='')

    def hide(self):
        """allow user to hide the password in password field"""
        self.show_button = Button(self.window, image=self.show_image, command=self.show, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=890, y=377)
        self.password_entry.config(show='*')

    def login_func(self):
        if self.var_user_login.get()=='' or self.var_user_pass.get()=='':
            messagebox.showerror("Error", "Field shouln't be empty", parent=self.window)
        else:
            con = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = con.cursor()
            try:
                cur.execute('SELECT * FROM users where username=%s and pass=%s', (self.var_user_login.get(),self.var_user_pass.get()))
                row_data = cur.fetchone()
                if row_data!=None:
                    self.newWindow = Toplevel(self.window)
                    self.app = AdminDash(self.newWindow)
                else:
                    messagebox.showerror('Invalid', f'Invalid Username or Password', parent=self.window)
                    
            except Exception as ex:
                messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.window)

def run_func():
    window = Tk()
    LoginDash(window)
    window.mainloop()
        
if __name__ == '__main__':
    run_func()