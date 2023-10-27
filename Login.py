import tkinter as tk
import tkinter.messagebox
import pickle
import MainPage
import dbOperations as db

usr_type = 0

# 登录函数
def usr_log_in():
    # 输入框获取用户名密码
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    # 从本地字典获取用户信息，如果没有则新建本地数据库
    try:
        with open('usr_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usr_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
    # 判断用户名和密码是否匹配
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name][0]:
            tk.messagebox.showinfo(title='welcome',
                                   message='Welcome: ' + usr_name)
            MainPage.set_usr_type(usrs_info[usr_name][1])
            db.set_usr_type(usrs_info[usr_name][1])
            window.destroy()
            MainPage.mainPage()
        else:
            tk.messagebox.showerror(message='Wrong password!')
    # 用户名密码不能为空
    elif usr_name == '' or usr_pwd == '':
        tk.messagebox.showerror(message='Username or password is empty.')
    # 不在数据库中弹出是否注册的框
    else:
        is_signup = tk.messagebox.askyesno('Welcome', 'You have not register yet, register now?')
        if is_signup:
            usr_sign_up()  # 打开注册界面


# 注册函数
def usr_sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nn = new_name.get()
        nt = new_type.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()

        # 本地加载已有用户信息,如果没有则已有用户信息为空
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}

            # 检查用户名存在、密码为空、密码前后不一致
        if nn in exist_usr_info:
            tk.messagebox.showerror('Error', 'Existing username.')
        elif np == '' or nn == '':
            tk.messagebox.showerror('Error', 'Username or password is empty.')
        elif np != npf:
            tk.messagebox.showerror('Error', 'Different password in repeating')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            exist_usr_info[nn] = [np, nt]
            with open('usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', 'Successfully registered')
            # 注册成功关闭注册框
            window_sign_up.destroy()


# 新建注册界面
    window_sign_up = tk.Toplevel(window)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Register')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中
    # 用户名变量及标签、输入框
    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='Username').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)
   # 用户类别：学生、老师、管理员
    new_type = tk.IntVar()
    # 设置默认选项为1， 在此相当于默认是学生
    new_type.set(1)
    tk.Label(window_sign_up, text='User Type：').place(x=10, y=50)
    # 学生
    tk.Radiobutton(window_sign_up, text="Student", variable=new_type, value=1).place(x=150, y=50)
    # 老师
    tk.Radiobutton(window_sign_up, text="Teacher", variable=new_type, value=2).place(x=150, y=75)
    # 管理员
    tk.Radiobutton(window_sign_up, text="Administer", variable=new_type, value=3).place(x=150, y=100)

    # 密码变量及标签、输入框
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password').place(x=10, y=150)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=150)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Repeat the password').place(x=10, y=190)
    tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=190)
    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm register',
                                   command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=230)


def usr_sign_quit():
    window.quit()

# 窗口
window = tk.Tk()
window.title('MIS for SCUT')
window.geometry('400x500')
width, height = 400, 500  # 窗口大小
x, y = (window.winfo_screenwidth() - width) / 2, (window.winfo_screenheight() - height) / 2
window.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中
# 画布放置图片
canvas = tk.Canvas(window, height=150, width=400)
imagefile = tk.PhotoImage(file='scut.png')
image = canvas.create_image(200, 100, anchor='center', image=imagefile)
canvas.pack(side='top')
# 标题文字
tk.Label(window, text='Welcome to \n MIS for SCUT', font=("Bookman Old Style", 30, "bold")).place(x=200, y=225,anchor='center')
# 标签 用户名密码
tk.Label(window, text='Username:').place(x=50, y=320)
tk.Label(window, text='Password:').place(x=50, y=360)
# 用户名输入框
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=150, y=320)
# 密码输入框
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=150, y=360)
# 登录 注册按钮
bt_login = tk.Button(window, text='Log in', command=usr_log_in, bg='lightgreen')
bt_login.place(x=50, y=400)
bt_logup = tk.Button(window, text='Register', command=usr_sign_up, bg='lightblue')
bt_logup.place(x=150, y=400)
bt_logquit = tk.Button(window, text='Quit', command=usr_sign_quit, bg='pink')
bt_logquit.place(x=300, y=400)

window.mainloop()
