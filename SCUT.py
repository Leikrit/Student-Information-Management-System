import tkinter as tk
from view import *  # 菜单栏对应的各个子页面


class MainPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小

        self.create_page()

    def create_page(self):
        menubar = tk.Menu(self.root)
        # menubar.add_command(label='录入')
        # menubar.add_command(label='查询')
        # menubar.add_command(label='删除')
        # menubar.add_command(label='修改')
        # menubar.add_command(label='关于')

        self.input_page = InputFrame(self.root)  # 创建不同 Frame
        self.query_page = QueryFrame(self.root)
        self.delete_page = DeleteFrame(self.root)
        self.change_page = ChangeFrame(self.root)
        self.about_page = AboutFrame(self.root)
        self.input_page.pack()  # 默认显示数据录入界面

        # 控件只是显示，如果需要实现切换的逻辑需要用代码实现
        menubar.add_command(label='录入', command=self.input_data)
        menubar.add_command(label='查询', command=self.query_data)
        menubar.add_command(label='删除', command=self.delete_data)
        menubar.add_command(label='修改', command=self.change_data)
        menubar.add_command(label='关于', command=self.about_disc)
        self.root['menu'] = menubar  # 设置菜单栏

    def input_data(self):
        self.input_page.pack()
        self.query_page.pack_forget()
        self.delete_page.pack_forget()
        self.change_page.pack_forget()
        self.about_page.pack_forget()

    def query_data(self):
        self.input_page.pack_forget()
        self.query_page.pack()
        self.delete_page.pack_forget()
        self.change_page.pack_forget()
        self.about_page.pack_forget()

    def delete_data(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.delete_page.pack()
        self.change_page.pack_forget()
        self.about_page.pack_forget()

    def change_data(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.delete_page.pack_forget()
        self.change_page.pack()
        self.about_page.pack_forget()

    def about_disc(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.delete_page.pack_forget()
        self.change_page.pack_forget()
        self.about_page.pack()

    def __del__(self):
        db.save_data()


if __name__ == '__main__':
    root = tk.Tk()
    MainPage(root)
    root.mainloop()