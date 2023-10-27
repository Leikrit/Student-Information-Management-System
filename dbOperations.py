import tkinter as tk
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import tkinter.messagebox
import MainPage
import datetime

usr_type = 1
def set_usr_type(x):
    global  usr_type
    usr_type = x

class EasyGridview(ttk.Treeview):
    def __init__(self, master=None, data=None, **kw):
        trv = self
        s = ttk.Style()
        s.configure('Treeview', rowheight=23)
        s.configure("Treeview.Heading", frowheight=20)

        self.dataFrame = ttk.Frame(master)
        self.dataFrame.pack(side=tk.TOP, fill=tk.X, expand=False)

        if not data or "columns" not in data.keys():
            super().__init__(master=self.dataFrame, **kw)
        else:
            # 表头及数据

            # 表头定义
            gridCols = []
            for col in data['columns']:
                if "name" in col.keys():
                    name = col["name"]
                    gridCols.append(name)

            super().__init__(master=self.dataFrame, columns=gridCols, **kw)

            for col in data['columns']:
                if "name" in col.keys():
                    name = col["name"]
                    title = name if "title" not in col.keys() else col["title"]

                    del col['name']
                    if "title" in col:
                        del col['title']

                    self.column(name, **col)
                    # self.heading(name, text=title)
                    self.heading(name, text=title,
                                 command=lambda _col=name: self.treeview_sort_column(trv, _col, reverse=False))

            if "data" in data.keys():
                # 插入数据
                for dataRow in data["data"]:
                    self.insert('', 1, values=dataRow)

        self.vbar = ttk.Scrollbar(self.dataFrame, orient=tk.VERTICAL, command=self.onScrollEvent)
        self.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def onScrollEvent(self, *event):
        self.yview(*event)

    def treeview_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        # print(tv.get_children(''))
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
            # print(k)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def Insertion(self, data=None):
        if "data" in data.keys():
            # 插入数据
            for dataRow in data["data"]:
                self.insert('', 'end', values=dataRow)
        self.update()

    def getTree(self):
        return self


def InsertStudent(root):
    window = root
    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Insert Student Information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        si = student_id.get()
        sn = student_name.get()
        ss = student_sex.get()
        sa = student_age.get()
        sy = student_year.get()
        sc = student_class.get()

        # 检查信息
        if len(si) != 10:
            tk.messagebox.showerror('Error', 'Illegal student ID!')
        elif sn == '' or ss == '' or sa == 0 or sy == 0 or sc == '':
            tk.messagebox.showerror('Error', 'Some information is empty!')
        elif sa < 10 or sa > 50:
            tk.messagebox.showerror('Error', 'Illegal entrance age!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                sex = ['male', 'female']
                sql_insert = '''
                INSERT INTO Student(Sid, Sname, sex, age, year, class)
                    values(''' + '\'' + si + '\'' + ',' + '\'' + sn + '\'' + ',' + '\'' + sex[ss] + '\'' + ',' + '\'' \
                    + str(sa) + '\'' + ',' + '\'' + str(sy) + '\'' + ',' + '\'' + sc + '\'' + ')'
                c.execute(sql_insert)
                conn.commit()
                conn.close()
                print("Insert Student OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully inserted!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()



    # 用户名变量及标签、输入框
    student_id = tk.StringVar()
    tk.Label(window_sign_up, text='Student ID (10 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=student_id, cursor='xterm').place(x=150, y=10)
    student_name = tk.StringVar()
    tk.Label(window_sign_up, text='Student name').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=student_name, cursor='xterm').place(x=150, y=40)

    # 学生性别：male, female
    student_sex = tk.IntVar()
    # 设置默认选项为1， 在次相当于默认是男生
    student_sex.set(0)
    tk.Label(window_sign_up, text='Sex').place(x=10, y=60)
    # male
    tk.Radiobutton(window_sign_up, text="Male", variable=student_sex, value=0).place(x=150, y=60)
    # female
    tk.Radiobutton(window_sign_up, text="Female", variable=student_sex, value=1).place(x=150, y=90)

    # 年龄
    student_age = tk.IntVar()
    student_age.set(20)
    tk.Label(window_sign_up, text='Entrance Age').place(x=10, y=120)
    tk.Entry(window_sign_up, textvariable=student_age, cursor='xterm').place(x=150, y=120)

    # 年份
    student_year = tk.IntVar()
    student_year.set(2021)
    tk.Label(window_sign_up, text='Entrance Year').place(x=10, y=150)
    tk.Entry(window_sign_up, textvariable=student_year, cursor='xterm').place(x=150, y=150)

    # 班级
    student_class = tk.StringVar()
    tk.Label(window_sign_up, text='Class').place(x=10, y=180)
    tk.Entry(window_sign_up, textvariable=student_class, cursor='xterm').place(x=150, y=180)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)

def ModifyStudent(root, id, name, sex, age, year, clas):
    window = root
    orid = id
    orname = name
    orsex = sex
    orage = age
    oryear = year
    orclas = clas
    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Modify Student Information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        si = student_id.get()
        sn = student_name.get()
        ss = student_sex.get()
        sa = student_age.get()
        sy = student_year.get()
        sc = student_class.get()

        # 检查信息
        if len(si) != 10:
            tk.messagebox.showerror('Error', 'Illegal student ID!')
        elif sn == '' or ss == '' or sa == 0 or sy == 0 or sc == '':
            tk.messagebox.showerror('Error', 'Some information is empty!')
        elif sa < 10 or sa > 50:
            tk.messagebox.showerror('Error', 'Illegal entrance age!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                ssex = ['male', 'female']
                sql_modify1 = '''
                UPDATE Student SET Sname = 
                ''' + '\'' + sn + '\' where Sid = ' + '\'' + si + '\''
                c.execute(sql_modify1)
                sql_modify2 = '''
                                UPDATE Student SET sex = 
                                ''' + '\'' + ssex[ss] + '\' where Sid = ' + '\'' + si + '\''
                c.execute(sql_modify2)
                sql_modify3 = '''
                                UPDATE Student SET age = 
                                ''' + str(sa) + ' where Sid = ' + '\'' + si + '\''
                c.execute(sql_modify3)
                sql_modify4 = '''
                                UPDATE Student SET year = 
                                ''' + str(sy) + ' where Sid = ' + '\'' + si + '\''
                c.execute(sql_modify4)
                sql_modify5 = '''
                                UPDATE Student SET class = 
                                ''' + '\'' + sc + '\' where Sid = ' + '\'' + si + '\''
                c.execute(sql_modify5)
                conn.commit()
                conn.close()
                print("Modify Student OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to modify, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully modified!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 用户名变量及标签、输入框
    student_id = tk.StringVar()
    student_id.set(orid)
    tk.Label(window_sign_up, text='Student ID (10 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=student_id, state="disabled").place(x=150, y=10)

    student_name = tk.StringVar()
    student_name.set(orname)
    tk.Label(window_sign_up, text='Student name').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=student_name, cursor='xterm').place(x=150, y=40)

    # 学生性别：male, female
    student_sex = tk.IntVar()
    # 设置默认选项为1， 在次相当于默认是男生
    student_sex.set(orsex == 'female')
    tk.Label(window_sign_up, text='Sex').place(x=10, y=60)
    # male
    tk.Radiobutton(window_sign_up, text="Male", variable=student_sex, value=0).place(x=150, y=60)
    # female
    tk.Radiobutton(window_sign_up, text="Female", variable=student_sex, value=1).place(x=150, y=90)

    # 年龄
    student_age = tk.IntVar()
    student_age.set(orage)
    tk.Label(window_sign_up, text='Entrance Age').place(x=10, y=120)
    tk.Entry(window_sign_up, textvariable=student_age, cursor='xterm').place(x=150, y=120)

    # 年份
    student_year = tk.IntVar()
    student_year.set(oryear)
    tk.Label(window_sign_up, text='Entrance Year').place(x=10, y=150)
    tk.Entry(window_sign_up, textvariable=student_year, cursor='xterm').place(x=150, y=150)

    # 班级
    student_class = tk.StringVar()
    student_class.set(orclas)
    tk.Label(window_sign_up, text='Class').place(x=10, y=180)
    tk.Entry(window_sign_up, textvariable=student_class, cursor='xterm').place(x=150, y=180)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)

def QueryStudent(root):
    counter = 1
    window = root
    window_sign_up = tk.Tk()
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Query Student Information')
    width, height = 600, 400  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()
        MainPage.mainPage()

    def tryQuery():
        # 获取输入框内的内容
        mode = comvalue.get()
        target = content.get()
        trv = EasyGridview(window_sign_up, height=20, show="headings")
        # 检查信息
        if mode == "Student ID" and len(target) != 10:
            tk.messagebox.showerror('Error', 'Illegal student ID!')
        elif target == "":
            tk.messagebox.showerror('Error', 'No content!')
        elif mode == "Student ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q1 = "SELECT * FROM Student WHERE Sid = '" + target + "';"
                print(sql_q1)
                # sql_test = "SELECT * FROM Student WHERE Sid = '1234567890';"
                cursor = conn.execute(sql_q1)
                data = []
                for row in cursor:
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5]))
                print(data)
                dataShow = {
                    'columns': [
                        {"name": "Sid", "title": "Student ID", "width": 100, "anchor": "center"},
                        {"name": "Sname", "title": "Name", "width": 50, "anchor": "center"},
                        {"name": "sex", "title": "Sex", "width": 50, "anchor": "center"},
                        {"name": "age", "title": "Entrance Age", "width": 30, "anchor": "center"},
                        {"name": "year", "title": "Entrance Year", "width": 50, "anchor": "center"},
                        {"name": "class", "title": "Class", "width": 100, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Student OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20,data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            tk.messagebox.showinfo('Completed', 'Successfully queried!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT * FROM Student WHERE Sname = '" + target + "';"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5]))
                dataShow = {
                    'columns': [
                        {"name": "Sid", "title": "Student ID", "width": 100, "anchor": "center"},
                        {"name": "Sname", "title": "Name", "width": 50, "anchor": "center"},
                        {"name": "sex", "title": "Sex", "width": 50, "anchor": "center"},
                        {"name": "age", "title": "Entrance Age", "width": 30, "anchor": "center"},
                        {"name": "year", "title": "Entrance Year", "width": 50, "anchor": "center"},
                        {"name": "class", "title": "Class", "width": 100, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Student OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            tk.messagebox.showinfo('Completed', 'Successfully queried!')
            #
            #
            # # 插入成功关闭窗口
            # window_sign_up.destroy()
            # window.destroy()
            # MainPage.mainPage()

    topFrm = ttk.LabelFrame(window_sign_up, text="")
    botFrm = ttk.LabelFrame(window_sign_up, text="")
    # 用户名变量及标签、输入框
    comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = ttk.Combobox(topFrm, textvariable=comvalue)  # 初始化
    comboxlist["values"] = ("Student ID", "Student Name")
    comboxlist.current(0)  # 选择第一个
    tk.Label(topFrm, text='Select query mode: ').grid(row=0, column=0, padx=50, pady=20)
    comboxlist.grid(row=0, column=1, padx=50, pady=20)

    content = tk.StringVar()
    tk.Label(topFrm, text='Enter the content: ').grid(row=1, column=0, padx=50, pady=20)
    tk.Entry(topFrm, textvariable=content, cursor='xterm').grid(row=1, column=1, padx=50, pady=20)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(topFrm, text='Confirm', bg='lightgreen', command=tryQuery)
    bt_confirm_sign_up.grid(row=2, column=0, padx=50, pady=20)
    cancel = tk.Button(topFrm, text='Back', bg='pink', command=destroy)
    cancel.grid(row=2, column=1, padx=50, pady=20)

    topFrm.pack(side=tk.TOP,fill=tk.X, expand=False)
    botFrm.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    dataShow = {
        'columns': [
            {"name": "Sid", "title": "Student ID", "width": 100, "anchor": "center"},
            {"name": "Sname", "title": "Name", "width": 50, "anchor": "center"},
            {"name": "sex", "title": "Sex", "width": 50, "anchor": "center"},
            {"name": "age", "title": "Entrance Age", "width": 30, "anchor": "center"},
            {"name": "year", "title": "Entrance Year", "width": 50, "anchor": "center"},
            {"name": "class", "title": "Class", "width": 100, "anchor": "center"},
        ]
    }
    trv = EasyGridview(botFrm, height=20,data=dataShow, show="headings")


################################################################
def InsertTeacher(root):
    window = root
    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Insert Teacher Information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        ti = teacher_id.get()
        tn = teacher_name.get()

        # 检查信息
        if len(ti) != 5:
            tk.messagebox.showerror('Error', 'Illegal teacher ID!')
        elif tn == '':
            tk.messagebox.showerror('Error', 'Some information is empty!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                sql_insert = '''
                INSERT INTO Teacher(Tid, Tname)
                    values(''' + '\'' + ti + '\'' + ',' + '\'' + tn + '\''  + ')'
                c.execute(sql_insert)
                conn.commit()
                conn.close()
                print("Insert Teacher OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully inserted!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 老师信息只有ID和名字，课程相关信息在Course Information里修改
    teacher_id = tk.StringVar()
    tk.Label(window_sign_up, text='Teacher ID (5 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=teacher_id, cursor='xterm').place(x=150, y=10)
    teacher_name = tk.StringVar()
    tk.Label(window_sign_up, text='Teacher name').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=teacher_name, cursor='xterm').place(x=150, y=40)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)


def ModifyTeacher(root, id, name):
    window = root
    orid = id
    orname = name
    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Modify Teacher information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        ti = teacher_id.get()
        tn = teacher_name.get()

        # 检查信息
        if len(ti) != 5:
            tk.messagebox.showerror('Error', 'Illegal student ID!')
        elif tn == '' :
            tk.messagebox.showerror('Error', 'Some information is empty!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                sql_modify1 = '''
                UPDATE Teacher SET Tname = 
                ''' + '\'' + tn + '\' where Tid = ' + '\'' + ti + '\''
                c.execute(sql_modify1)
                conn.commit()
                conn.close()
                print("Modify Teacher OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to modify, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully modified!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 用户名变量及标签、输入框
    teacher_id = tk.StringVar()
    teacher_id.set(orid)
    tk.Label(window_sign_up, text='Student ID (10 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=teacher_id, state="disabled").place(x=150, y=10)

    teacher_name = tk.StringVar()
    teacher_name.set(orname)
    tk.Label(window_sign_up, text='Student name').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=teacher_name, cursor='xterm').place(x=150, y=40)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)

def QueryTeacher(root):
    counter = 1
    window = root
    window_sign_up = tk.Tk()
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Query Teacher Information')
    width, height = 600, 400  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()
        MainPage.mainPage()

    def tryQuery():
        # 获取输入框内的内容
        mode = comvalue.get()
        target = content.get()
        trv = EasyGridview(window_sign_up, height=20, show="headings")
        # 检查信息
        if mode == "Teacher ID" and len(target) != 5:
            tk.messagebox.showerror('Error', 'Illegal student ID!')
        elif target == "":
            tk.messagebox.showerror('Error', 'No content!')
        elif mode == "Teacher ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q1 = "SELECT T.Tid, T.Tname, C.Cname FROM Teacher as T, Course as C WHERE T.Tid = '" + target + "' and T.Tid = C.Tid"
                print(sql_q1)
                # sql_test = "SELECT * FROM Student WHERE Sid = '1234567890';"
                cursor = conn.execute(sql_q1)
                data = []
                for row in cursor:
                    data.append((row[0], row[1], row[2]))
                print(data)
                dataShow = {
                    'columns': [
                        {"name": "Tid", "title": "Teacher ID", "width": 75, "anchor": "center"},
                        {"name": "Tname", "title": "Name", "width": 50, "anchor": "center"},
                        {"name": "course", "title": "Course", "width": 200, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Teacher OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20,data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            tk.messagebox.showinfo('Completed', 'Successfully queried!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT T.Tid, T.Tname, C.Cname FROM Teacher as T, Course as C WHERE T.Tname = '" + target + "' and T.Tid = C.Tid;"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[0], row[1], row[2]))
                dataShow = {
                    'columns': [
                        {"name": "Tid", "title": "Teacher ID", "width": 75, "anchor": "center"},
                        {"name": "Tname", "title": "Name", "width": 50, "anchor": "center"},
                        {"name": "course", "title": "Course", "width": 200, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Teacher OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            tk.messagebox.showinfo('Completed', 'Successfully queried!')
            #
            #
            # # 插入成功关闭窗口
            # window_sign_up.destroy()
            # window.destroy()
            # MainPage.mainPage()

    topFrm = ttk.LabelFrame(window_sign_up, text="")
    botFrm = ttk.LabelFrame(window_sign_up, text="")
    # 用户名变量及标签、输入框
    comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = ttk.Combobox(topFrm, textvariable=comvalue)  # 初始化
    comboxlist["values"] = ("Teacher ID", "Teacher Name")
    comboxlist.current(0)  # 选择第一个
    tk.Label(topFrm, text='Select query mode: ').grid(row=0, column=0, padx=50, pady=20)
    comboxlist.grid(row=0, column=1, padx=50, pady=20)

    content = tk.StringVar()
    tk.Label(topFrm, text='Enter the content: ').grid(row=1, column=0, padx=50, pady=20)
    tk.Entry(topFrm, textvariable=content, cursor='xterm').grid(row=1, column=1, padx=50, pady=20)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(topFrm, text='Confirm', bg='lightgreen', command=tryQuery)
    bt_confirm_sign_up.grid(row=2, column=0, padx=50, pady=20)
    cancel = tk.Button(topFrm, text='Back', bg='pink', command=destroy)
    cancel.grid(row=2, column=1, padx=50, pady=20)

    topFrm.pack(side=tk.TOP,fill=tk.X, expand=False)
    botFrm.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    dataShow = {
        'columns': [
            {"name": "Tid", "title": "Teacher ID", "width": 75, "anchor": "center"},
            {"name": "Tname", "title": "Name", "width": 50, "anchor": "center"},
            {"name": "course", "title": "Course", "width": 50, "anchor": "center"},
        ]
    }
    trv = EasyGridview(botFrm, height=20,data=dataShow, show="headings")

########################################################
def InsertCourse(root):
    window = root
    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Insert Course Information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        ci = course_id.get()
        ti = teacher_id.get()
        cn = course_name.get()
        cr = credit.get()
        gr = grade.get()
        ca = cancel_year.get()

        # 检查信息
        if len(ci) != 7 or len(ti) != 5:
            tk.messagebox.showerror('Error', 'Illegal ID!')
        elif cn == '' or cr == 0 or gr == 0 or ca == 0:
            tk.messagebox.showerror('Error', 'Some information is empty!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                sql_insert = '''
                INSERT INTO Course(Cid, Tid, Cname, credit, grade, cancel_year)
                    values(''' + '\'' + ci + '\'' + ',' + '\'' + ti + '\',' + '\'' + cn + '\',' + str(cr) + ',' + str(gr) + ',' + str(ca) + ')'
                c.execute(sql_insert)
                conn.commit()
                conn.close()
                print("Insert Course OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully inserted!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 老师信息只有ID和名字，课程相关信息在Course Information里修改
    course_id = tk.StringVar()
    tk.Label(window_sign_up, text='Course ID (7 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=course_id, cursor='xterm').place(x=150, y=10)
    teacher_id = tk.StringVar()
    tk.Label(window_sign_up, text='Teacher ID').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=teacher_id, cursor='xterm').place(x=150, y=40)
    course_name = tk.StringVar()
    tk.Label(window_sign_up, text='Course Name').place(x=10, y=70)
    tk.Entry(window_sign_up, textvariable=course_name, cursor='xterm').place(x=150, y=70)
    credit = tk.DoubleVar()
    credit.set(0.0)
    tk.Label(window_sign_up, text='Credit').place(x=10, y=110)
    tk.Entry(window_sign_up, textvariable=credit, cursor='xterm').place(x=150, y=110)
    grade = tk.IntVar()
    grade.set(0)
    tk.Label(window_sign_up, text='Grade').place(x=10, y=140)
    tk.Entry(window_sign_up, textvariable=grade, cursor='xterm').place(x=150, y=140)
    cancel_year = tk.IntVar()
    cancel_year.set(2023)
    tk.Label(window_sign_up, text='Cancel year').place(x=10, y=170)
    tk.Entry(window_sign_up, textvariable=cancel_year, cursor='xterm').place(x=150, y=170)
    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)


def ModifyCourse(root, cid,tid, name, credit, grade, year):
    window = root
    orcid = cid
    ortid = tid
    orname = name
    orcredit = credit
    orgrade = grade
    oryear = year

    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Modify Course information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        ci = course_id.get()
        ti = teacher_id.get()
        cn = course_name.get()
        cr = credit.get()
        gr = grade.get()
        ca = cancel_year.get()

        # 检查信息
        if len(ti) != 5 or len(ci) != 7:
            tk.messagebox.showerror('Error', 'Illegal ID!')
        elif cn == '' or cr == 0 or gr == 0 or ca == '' :
            tk.messagebox.showerror('Error', 'Some information is empty!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                sql_modify1 = '''
                UPDATE Course SET Tid = 
                ''' + '\'' + ti + '\' where Cid = ' + '\'' + ci + '\''
                c.execute(sql_modify1)

                sql_modify2 = '''
                               UPDATE Course SET Cname = 
                               ''' + '\'' + cn + '\' where Cid = ' + '\'' + ci + '\''
                c.execute(sql_modify2)

                sql_modify3 = '''
                               UPDATE Course SET credit = 
                               ''' + str(cr) + ' where Cid = ' + '\'' + ci + '\''
                c.execute(sql_modify3)

                sql_modify4 = '''
                               UPDATE Course SET grade = 
                               ''' + str(gr) + ' where Cid = ' + '\'' + ci + '\''
                c.execute(sql_modify4)

                sql_modify5 = '''
                               UPDATE Course SET cancel_year = 
                               ''' + str(ca) + ' where Cid = ' + '\'' + ci + '\''
                c.execute(sql_modify5)

                conn.commit()
                conn.close()
                print("Modify Course OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to modify, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully modified!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 用户名变量及标签、输入框
    course_id = tk.StringVar()
    course_id.set(orcid)
    tk.Label(window_sign_up, text='Course ID (7 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=course_id, state='disabled').place(x=150, y=10)
    teacher_id = tk.StringVar()
    teacher_id.set(ortid)
    tk.Label(window_sign_up, text='Teacher ID').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=teacher_id, cursor='xterm').place(x=150, y=40)
    course_name = tk.StringVar()
    course_name.set(orname)
    tk.Label(window_sign_up, text='Course Name').place(x=10, y=70)
    tk.Entry(window_sign_up, textvariable=course_name, cursor='xterm').place(x=150, y=70)
    credit = tk.DoubleVar()
    credit.set(orcredit)
    tk.Label(window_sign_up, text='Credit').place(x=10, y=110)
    tk.Entry(window_sign_up, textvariable=credit, cursor='xterm').place(x=150, y=110)
    grade = tk.IntVar()
    grade.set(orgrade)
    tk.Label(window_sign_up, text='Grade').place(x=10, y=140)
    tk.Entry(window_sign_up, textvariable=grade, cursor='xterm').place(x=150, y=140)
    cancel_year = tk.IntVar()
    cancel_year.set(oryear)
    tk.Label(window_sign_up, text='Cancel year').place(x=10, y=170)
    tk.Entry(window_sign_up, textvariable=cancel_year, cursor='xterm').place(x=150, y=170)
    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)

def QueryCourse(root):
    counter = 1
    window = root
    window_sign_up = tk.Tk()
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Query Course Information')
    width, height = 600, 400  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()
        MainPage.mainPage()

    def tryQuery():
        # 获取输入框内的内容
        mode = comvalue.get()
        target = content.get()
        trv = EasyGridview(window_sign_up, height=20, show="headings")
        # 检查信息
        if mode == "Course ID" and len(target) != 7:
            tk.messagebox.showerror('Error', 'Illegal Course ID!')
        elif target == "":
            tk.messagebox.showerror('Error', 'No content!')
        elif mode == "Course ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q1 = "SELECT * FROM Course WHERE Cid = '" + target + "';"
                print(sql_q1)
                # sql_test = "SELECT * FROM Student WHERE Sid = '1234567890';"
                cursor = conn.execute(sql_q1)
                data = []
                for row in cursor:
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5]))
                print(data)
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Cname", "title": "Course Name", "width": 50, "anchor": "center"},
                        {"name": "credit", "title": "Credit", "width": 30, "anchor": "center"},
                        {"name": "grade", "title": "Grade", "width": 50, "anchor": "center"},
                        {"name": "cancel_year", "title": "Year", "width": 100, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20,data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            tk.messagebox.showinfo('Completed', 'Successfully queried!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT * FROM Course WHERE Cname = '" + target + "';"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[0], row[1], row[2], row[3], row[4], row[5]))
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Cname", "title": "Course Name", "width": 50, "anchor": "center"},
                        {"name": "credit", "title": "Credit", "width": 30, "anchor": "center"},
                        {"name": "grade", "title": "Grade", "width": 50, "anchor": "center"},
                        {"name": "cancel_year", "title": "Year", "width": 100, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            tk.messagebox.showinfo('Completed', 'Successfully queried!')
            #
            #
            # # 插入成功关闭窗口
            # window_sign_up.destroy()
            # window.destroy()
            # MainPage.mainPage()

    topFrm = ttk.LabelFrame(window_sign_up, text="")
    botFrm = ttk.LabelFrame(window_sign_up, text="")
    # 用户名变量及标签、输入框
    comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = ttk.Combobox(topFrm, textvariable=comvalue)  # 初始化
    comboxlist["values"] = ("Course ID", "Course Name")
    comboxlist.current(0)  # 选择第一个
    tk.Label(topFrm, text='Select query mode: ').grid(row=0, column=0, padx=50, pady=20)
    comboxlist.grid(row=0, column=1, padx=50, pady=20)

    content = tk.StringVar()
    tk.Label(topFrm, text='Enter the content: ').grid(row=1, column=0, padx=50, pady=20)
    tk.Entry(topFrm, textvariable=content, cursor='xterm').grid(row=1, column=1, padx=50, pady=20)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(topFrm, text='Confirm', bg='lightgreen', command=tryQuery)
    bt_confirm_sign_up.grid(row=2, column=0, padx=50, pady=20)
    cancel = tk.Button(topFrm, text='Back', bg='pink', command=destroy)
    cancel.grid(row=2, column=1, padx=50, pady=20)

    topFrm.pack(side=tk.TOP,fill=tk.X, expand=False)
    botFrm.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    dataShow = {
        'columns': [
            {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
            {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
            {"name": "Cname", "title": "Course Name", "width": 50, "anchor": "center"},
            {"name": "credit", "title": "Credit", "width": 30, "anchor": "center"},
            {"name": "grade", "title": "Grade", "width": 50, "anchor": "center"},
            {"name": "cancel_year", "title": "Year", "width": 100, "anchor": "center"},
        ]
    }
    trv = EasyGridview(botFrm, height=20,data=dataShow, show="headings")

####################################################################
def InsertChoose(root):
    window = root
    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Insert Course Choosing Information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        ci = course_id.get()
        ti = teacher_id.get()
        si = student_id.get()
        cy = chooseyear.get()
        sc = score.get()

        conn = sqlite3.connect("test.db")
        sql_q1 = "SELECT year FROM Student WHERE Sid = \'" + si + "\';"
        cursor = conn.execute(sql_q1)
        eyear = 2023
        for row in cursor:
            eyear = row[0]
        cursor.close()
        conn.close()

        conn = sqlite3.connect("test.db")
        sql_q2 = "SELECT grade, cancel_year  FROM Course WHERE Cid = \'" + ci + "\';"
        cursor = conn.execute(sql_q2)
        cyear = 3000
        gr = 1
        for row in cursor:
            gr = row[0]
            cyear = row[1]
        cursor.close()
        conn.close()

        now = datetime.datetime.now()
        current_year = now.year
        # 检查信息
        if len(ci) != 7 or len(ti) != 5 or len(si) != 10:
            tk.messagebox.showerror('Error', 'Illegal ID!')
        elif cy == 0 or sc == 0:
            tk.messagebox.showerror('Error', 'Some information is empty!')
        elif cy > cyear or (current_year - eyear) < gr:
            tk.messagebox.showerror('Rejected!', 'Student \'s grade is not suitable for this course or the course is already canceled!')
        elif sc < 60:
            tk.messagebox.showinfo('Drop out!', 'The student drops out this course, record automatically removed!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                sql_insert = '''
                INSERT INTO Course_Choosing(Sid, Cid, Tid, Chosen_year, score)
                    values(''' + '\'' + si + '\'' + ',' + '\'' + ci + '\',' + '\'' + ti + '\',' + str(cy) + ',' + str(sc) + ')'
                c.execute(sql_insert)
                conn.commit()
                conn.close()
                print("Insert Course Choosing OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully inserted!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 老师信息只有ID和名字，课程相关信息在Course Information里修改
    course_id = tk.StringVar()
    tk.Label(window_sign_up, text='Course ID (7 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=course_id, cursor='xterm').place(x=150, y=10)
    teacher_id = tk.StringVar()
    tk.Label(window_sign_up, text='Teacher ID (5 digits)').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=teacher_id, cursor='xterm').place(x=150, y=40)
    student_id = tk.StringVar()
    tk.Label(window_sign_up, text='Student ID (10 digits)').place(x=10, y=70)
    tk.Entry(window_sign_up, textvariable=student_id, cursor='xterm').place(x=150, y=70)
    chooseyear = tk.IntVar()
    chooseyear.set(0)
    tk.Label(window_sign_up, text='Chosen Year').place(x=10, y=110)
    tk.Entry(window_sign_up, textvariable=chooseyear, cursor='xterm').place(x=150, y=110)
    score = tk.DoubleVar()
    score.set(0.0)
    tk.Label(window_sign_up, text='Score').place(x=10, y=140)
    tk.Entry(window_sign_up, textvariable=score, cursor='xterm').place(x=150, y=140)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)


def ModifyChoose(root, cid,tid, sid, chosenyear, score):
    window = root
    orcid = cid
    ortid = tid
    orsid = sid
    orchosenyear = chosenyear
    orscore = score

    window_sign_up = tk.Toplevel(root)
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Modify Course information')
    width, height = 300, 300  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()

    def tryInsert():
        # 获取输入框内的内容
        ci = course_id.get()
        ti = teacher_id.get()
        si = student_id.get()
        cy= chosenyear.get()
        sc = score.get()

        # 检查信息
        if len(ti) != 5 or len(ci) != 7 or len(si) != 10:
            tk.messagebox.showerror('Error', 'Illegal ID!')
        elif cy == 0:
            tk.messagebox.showerror('Error', 'Some information is empty!')
        else:
            try:
                conn = sqlite3.connect("test.db")
                c = conn.cursor()
                # sql_modify1 = '''
                # UPDATE Course_Choosing SET Tid =
                # ''' + '\'' + ti + '\' where Cid = ' + '\'' + ci + '\''
                # c.execute(sql_modify1)
                #
                # sql_modify2 = '''
                #                UPDATE Course_Choosing SET Sid =
                #                ''' + '\'' + si + '\' where Cid = ' + '\'' + ci + '\''
                # c.execute(sql_modify2)

                sql_modify3 = '''
                               UPDATE Course_Choosing SET Chosen_year = 
                               ''' + str(cy) + ' where Cid = ' + '\'' + ci + '\'' + ' and Tid = \'' + ti + '\' and Sid = \'' + si + '\''
                c.execute(sql_modify3)

                sql_modify4 = '''
                               UPDATE Course_Choosing SET score = 
                               ''' + str(sc) + ' where Cid = ' + '\'' + ci + '\'' + ' and Tid = \'' + ti + '\' and Sid = \'' + si + '\''
                c.execute(sql_modify4)

                conn.commit()
                conn.close()
                print("Modify Course Choosing OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to modify, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully modified!')
            # 插入成功关闭窗口
            window_sign_up.destroy()
            window.destroy()
            MainPage.mainPage()

    # 用户名变量及标签、输入框
    course_id = tk.StringVar()
    course_id.set(orcid)
    tk.Label(window_sign_up, text='Course ID (7 digits)').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=course_id, state='disabled').place(x=150, y=10)
    teacher_id = tk.StringVar()
    teacher_id.set(ortid)
    tk.Label(window_sign_up, text='Teacher ID (5 digits)').place(x=10, y=40)
    tk.Entry(window_sign_up, textvariable=teacher_id, state='disabled').place(x=150, y=40)
    student_id = tk.StringVar()
    student_id.set(orsid)
    tk.Label(window_sign_up, text='Course Name').place(x=10, y=70)
    tk.Entry(window_sign_up, textvariable=student_id, state='disabled').place(x=150, y=70)
    chosenyear = tk.IntVar()
    chosenyear.set(orchosenyear)
    tk.Label(window_sign_up, text='Chosen Year').place(x=10, y=110)
    chosen = tk.Entry(window_sign_up, textvariable=chosenyear, cursor='xterm')
    chosen.place(x=150, y=110)
    score = tk.DoubleVar()
    score.set(orscore)
    tk.Label(window_sign_up, text='Score').place(x=10, y=140)
    scr = tk.Entry(window_sign_up, textvariable=score, cursor='xterm')
    scr.place(x=150, y=140)

    if usr_type == 2:
        chosen.configure(state='disabled')
    elif usr_type == 3:
        scr.configure(state='disabled')

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='Confirm', command=tryInsert)
    bt_confirm_sign_up.place(x=150, y=250)
    cancel = tk.Button(window_sign_up, text='Cancel', command=destroy)
    cancel.place(x=225, y=250)

def QueryChoose(root):
    counter = 1
    window = root
    window_sign_up = tk.Tk()
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Query Course Choosing Information')
    width, height = 800, 400  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()
        MainPage.mainPage()

    def tryQuery():
        # 获取输入框内的内容
        mode = comvalue.get()
        target = content.get()
        trv = EasyGridview(window_sign_up, height=20, show="headings")
        # 检查信息
        if mode == "Course ID" and len(target) != 7:
            tk.messagebox.showerror('Error', 'Illegal Course ID!')
        elif target == "":
            tk.messagebox.showerror('Error', 'No content!')
        elif mode == "Course ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q1 = "SELECT * FROM Course_Choosing WHERE Cid = '" + target + "';"
                print(sql_q1)
                # sql_test = "SELECT * FROM Student WHERE Sid = '1234567890';"
                cursor = conn.execute(sql_q1)
                data = []
                for row in cursor:
                    data.append((row[1], row[2], row[0], row[3], row[4]))
                print(data)
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
                        {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
                        {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course Choosing OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20,data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Course Name":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT Course_Choosing.* FROM Course_Choosing, Course WHERE Course.Cname = '" + target + "' and Course_Choosing.Cid = Course.Cid;"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[1], target, row[2], row[0], row[3], row[4]))
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Cname", "title": "Course Name", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
                        {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
                        {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course Choosing OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Student ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT Course_Choosing.*, Student.Sname FROM Course_Choosing, Student WHERE Student.Sid = '" + target + "' and Course_Choosing.Sid = Student.Sid;"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[1], row[2], row[0], row[5], row[3], row[4]))
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
                        {"name": "Sname", "title": "Student Name", "width": 50, "anchor": "center"},
                        {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
                        {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course Choosing OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Student Name":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT Course_Choosing.*, Student.Sname FROM Course_Choosing, Student WHERE Student.Sname = '" + target + "' and Course_Choosing.Sid = Student.Sid;"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[1], row[2], row[0], row[5], row[3], row[4]))
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
                        {"name": "Sname", "title": "Student Name", "width": 50, "anchor": "center"},
                        {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
                        {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course Choosing OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Teacher ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT Course_Choosing.*, Teacher.Tname FROM Course_Choosing, Teacher WHERE Teacher.Tid = '" + target + "' and Course_Choosing.Tid = Teacher.Tid;"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[1], row[2], row[5], row[0], row[3], row[4]))
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Tname", "title": "Teacher Name", "width": 50, "anchor": "center"},
                        {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
                        {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
                        {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course Choosing OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Teacher Name":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT Course_Choosing.*, Teacher.Tname FROM Course_Choosing, Teacher WHERE Teacher.Tname = '" + target + "' and Course_Choosing.Tid = Teacher.Tid;"
                cursor = conn.execute(sql_q2)
                data = []
                for row in cursor:
                    data.append((row[1], row[2], row[5], row[0], row[3], row[4]))
                dataShow = {
                    'columns': [
                        {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
                        {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
                        {"name": "Tname", "title": "Teacher Name", "width": 50, "anchor": "center"},
                        {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
                        {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
                        {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
                    ],
                    'data': data
                }
                cursor.close()
                conn.close()
                print("Query Course Choosing OK")
                for widget in botFrm.winfo_children():
                    widget.destroy()
                EasyGridview(botFrm, height=20, data=dataShow, show="headings")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
            #
            #
            # # 插入成功关闭窗口
            # window_sign_up.destroy()
            # window.destroy()
            # MainPage.mainPage()

    topFrm = ttk.LabelFrame(window_sign_up, text="")
    botFrm = ttk.LabelFrame(window_sign_up, text="")
    # 用户名变量及标签、输入框
    comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = ttk.Combobox(topFrm, textvariable=comvalue)  # 初始化
    comboxlist["values"] = ("Course ID", "Course Name", "Student ID", "Student Name", "Teacher ID", "Teacher Name")
    comboxlist.current(0)  # 选择第一个
    tk.Label(topFrm, text='Select query mode: ').grid(row=0, column=0, padx=50, pady=20)
    comboxlist.grid(row=0, column=1, padx=50, pady=20)

    content = tk.StringVar()
    tk.Label(topFrm, text='Enter the content: ').grid(row=1, column=0, padx=50, pady=20)
    tk.Entry(topFrm, textvariable=content, cursor='xterm').grid(row=1, column=1, padx=50, pady=20)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(topFrm, text='Confirm', bg='lightgreen', command=tryQuery)
    bt_confirm_sign_up.grid(row=2, column=0, padx=50, pady=20)
    cancel = tk.Button(topFrm, text='Back', bg='pink', command=destroy)
    cancel.grid(row=2, column=1, padx=50, pady=20)

    topFrm.pack(side=tk.TOP,fill=tk.X, expand=False)
    botFrm.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    dataShow = {
        'columns': [
            {"name": "Cid", "title": "Course ID", "width": 100, "anchor": "center"},
            {"name": "Tid", "title": "Teacher ID", "width": 50, "anchor": "center"},
            {"name": "Sid", "title": "Student ID", "width": 50, "anchor": "center"},
            {"name": "Chosen_year", "title": "Chosen year", "width": 30, "anchor": "center"},
            {"name": "score", "title": "Score", "width": 50, "anchor": "center"},
        ]
    }
    trv = EasyGridview(botFrm, height=20,data=dataShow, show="headings")

def AnalysisChoose(root):
    counter = 1
    window = root
    window_sign_up = tk.Tk()
    # window_sign_up.geometry('300x300')
    window_sign_up.title('Analysis Course Choosing Information')
    width, height = 500, 400  # 窗口大小
    x, y = (window_sign_up.winfo_screenwidth() - width) / 2, (window_sign_up.winfo_screenheight() - height) / 2
    window_sign_up.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    def destroy():
        window_sign_up.destroy()
        MainPage.mainPage()

    def tryQuery():
        # 获取输入框内的内容
        mode = comvalue.get()
        target = content.get()
        # trv = EasyGridview(window_sign_up, height=20, show="headings")
        # 检查信息
        if mode == "Student ID" and len(target) != 10:
            tk.messagebox.showerror('Error', 'Illegal Student ID!')
        elif mode == "Course ID" and len(target) != 7:
            tk.messagebox.showerror('Error', "Illegal Course ID!")
        elif target == "":
            tk.messagebox.showerror('Error', 'No content!')
        elif mode == "Student ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q1 = "SELECT AVG(score) FROM Course_Choosing WHERE Sid = \'" + target + "\';"
                print(sql_q1)
                # sql_test = "SELECT * FROM Student WHERE Sid = '1234567890';"
                cursor = conn.execute(sql_q1)
                data = 0
                for row in cursor:
                    data = row[0]
                print(data)
                result.configure(text=str(data))
                cursor.close()
                conn.close()
                print("Analysis Course Choosing OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Course ID":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT AVG(score) FROM Course_Choosing WHERE Cid = \'" + target + "\' ;"
                cursor = conn.execute(sql_q2)
                data = 0
                for row in cursor:
                    data = row[0]
                result.configure(text=str(data))
                cursor.close()
                conn.close()
                print("Analysis Course Choosing OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "All Students":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT AVG(score) FROM Course_Choosing "
                cursor = conn.execute(sql_q2)
                data = 0
                for row in cursor:
                    data = row[0]
                result.configure(text=str(data))
                cursor.close()
                conn.close()
                print("Analysis Course Choosing OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')
        elif mode == "Class":
            try:
                conn = sqlite3.connect("test.db")
                sql_q2 = "SELECT AVG(score) FROM Course_Choosing, Student WHERE Student.class = '" + target + "' and Course_Choosing.Sid = Student.Sid;"
                cursor = conn.execute(sql_q2)
                data = 0
                for row in cursor:
                    data = row[0]
                result.configure(text=str(data))
                cursor.close()
                conn.close()
                print("Analysis Course Choosing OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'No such record!')

    topFrm = ttk.LabelFrame(window_sign_up, text="")
    # 用户名变量及标签、输入框
    comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = ttk.Combobox(topFrm, textvariable=comvalue)  # 初始化
    comboxlist["values"] = ("Student ID", "All Students", "Class", "Course ID")
    comboxlist.current(0)  # 选择第一个
    tk.Label(topFrm, text='Select query mode: ').grid(row=0, column=0, padx=50, pady=20)
    comboxlist.grid(row=0, column=1, padx=50, pady=20)

    content = tk.StringVar()
    tk.Label(topFrm, text='Enter the content: ').grid(row=1, column=0, padx=50, pady=20)
    tk.Entry(topFrm, textvariable=content, cursor='xterm').grid(row=1, column=1, padx=50, pady=20)

    # 确认及取消按钮及位置
    bt_confirm_sign_up = tk.Button(topFrm, text='Confirm', bg='lightgreen', command=tryQuery)
    bt_confirm_sign_up.grid(row=2, column=0, padx=50, pady=20)
    cancel = tk.Button(topFrm, text='Back', bg='pink', command=destroy)
    cancel.grid(row=2, column=1, padx=50, pady=20)
    result = tk.Label(topFrm, text='', bg='grey')
    result.grid(row=3, column=0,columnspan=2, padx=50, pady=20)

    topFrm.pack(side=tk.TOP,fill=tk.X, expand=False)
