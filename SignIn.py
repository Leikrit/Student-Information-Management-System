import tkinter as tk
import tkinter.messagebox
from SCUT import *

"""
"""
# 一张画纸
class LoginPage(object):
    def __init__(self, master=None):
        # master 画板对象，往画板上作画
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (400, 280))  # 设置窗口大小
        root.title('登陆页面')
        # 定义可以在页面更新数据的变量 普通字符串改变之后无法及时在页面中刷新
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # 画 内容 需要画在纸上面
        # 创建新的 布局控件 找一张新的纸作画
        self.page = tk.Frame(self.root)  # 创建Frame
        # 将控件布局到 root 对象 （GUI 程序对象）
        self.page.pack()

        self.create_page()

    def create_page(self):
        """
            使用表格布局绘制内容

        """
        #
        # tk.Label 文本框 显示文字内容
        # stick 控件对象方向 tk.W 西方位
        # pady padding y 上下的宽度
        # row 行 表格布局
        tk.Label(self.page).grid(row=0, stick=tk.W)
        tk.Label(self.page, text='账户: ').grid(row=1, stick=tk.W, pady=10)
        # tk.Label 输入框 显示输入内容
        # 输入框的文字等内容需要更新
        tk.Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=tk.E)
        tk.Label(self.page, text='密码: ').grid(row=2, stick=tk.W, pady=10)
        tk.Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=tk.E)
        tk.Button(self.page, text='登陆', command=self.login_check).grid(row=3, stick=tk.W, pady=10)
        tk.Button(self.page, text='注册', command=self.page.quit).grid(row=3, column=1, stick=tk.E)

    def login_check(self):
        """登录检测"""
        name = self.username.get()
        secret = self.password.get()
        if name == 'admin' and secret == '123456':
            self.page.destroy()
            MainPage(self.root)
        else:
            tkinter.messagebox.showinfo(title='错误', message='账号或密码错误！')


if __name__ == '__main__':
    # root 对象 画板
    root = tk.Tk()
    # LoginPage 画纸
    LoginPage(root)
    root.mainloop()