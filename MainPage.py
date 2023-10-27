import time
import tkinter as tk
from tkinter.messagebox import showinfo
import tkinter.font as tkFont
from tkinter import ttk
import sqlite3
import dbOperations as op
from sqlite3 import Error

usr_type = 1


def set_usr_type(x):
    global usr_type
    usr_type = x

#%%
class EasyGridview(ttk.Treeview):
    def __init__(self, master=None,data=None, **kw):
        trv = self
        s = ttk.Style()
        s.configure('Treeview', rowheight=23)
        s.configure("Treeview.Heading", frowheight=20)

        self.dataFrame = ttk.Frame(master)
        self.dataFrame.pack(side=tk.TOP,fill=tk.X, expand=False)
        
        if not data or "columns" not in data.keys() :
            super().__init__(master=self.dataFrame, **kw)
        else:
            #表头及数据

            #表头定义
            gridCols = []
            for col in data['columns']:
                if "name" in col.keys():
                    name = col["name"]
                    gridCols.append(name)
                            
            super().__init__(master=self.dataFrame,columns=gridCols, **kw)

            for col in data['columns']:
                if "name" in col.keys():
                    name = col["name"]
                    title = name if "title" not in col.keys() else col["title"]
                    
                    del col['name']
                    if "title" in col:
                        del col['title']
                    
                    self.column(name,**col)
                    # self.heading(name, text=title)
                    self.heading(name, text=title,
                                 command=lambda _col=name: self.treeview_sort_column(trv, _col, reverse=False))

            if "data" in data.keys():
                #插入数据
                for dataRow in data["data"]:
                    self.insert('',1,values=dataRow)

        self.vbar = ttk.Scrollbar(self.dataFrame, orient=tk.VERTICAL, command=self.onScrollEvent)
        self.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side=tk.RIGHT,fill=tk.Y,expand=False)
        self.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

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

def showStudent(location):
    data = []
    con = sqlite3.connect("test.db")
    cursor = con.execute("SELECT * FROM Student;")
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
    con.close()
    tv = EasyGridview(location, height=20, data=dataShow, show="headings")
    return tv

def showTeacher(location):
    data = []
    con = sqlite3.connect("test.db")
    cursor = con.execute("SELECT * FROM Teacher;")
    for row in cursor:
        data.append((row[0], row[1]))

    dataShow = {
        'columns': [
            {"name": "Tid", "title": "Teacher ID", "width": 100, "anchor": "center"},
            {"name": "Tname", "title": "Name", "width": 50, "anchor": "center"},
        ],
        'data': data
    }
    cursor.close()
    con.close()
    tv = EasyGridview(location, height=20, data=dataShow, show="headings")
    return tv

def showCourse(location):
    data = []
    con = sqlite3.connect("test.db")
    cursor = con.execute("SELECT * FROM Course;")
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
    con.close()
    tv = EasyGridview(location, height=20, data=dataShow, show="headings")
    return tv

def showChoose(location):
    data = []
    con = sqlite3.connect("test.db")
    cursor = con.execute("SELECT * FROM Course_Choosing;")
    for row in cursor:
        data.append((row[1], row[2], row[0], row[3], row[4]))

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
    con.close()
    tv = EasyGridview(location, height=20, data=dataShow, show="headings")
    return tv

def mainPage():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql_init1 = '''
    CREATE TABLE if not exists Student
            (
            Sid MESSAGE_TEXT(10) PRIMARY KEY NOT NULL,
            Sname MESSAGE_TEXT NOT NULL,
            sex MESSAGE_TEXT NOT NULL CHECK(sex = 'male' OR sex = 'female'),
            age INTEGER NOT NULL CHECK(age > 9 AND age < 51),
            year NUMERIC,
            class MESSAGE_TEXT
            );
    '''
    c.execute(sql_init1)
    conn.commit()
    conn.close()
    print("Table Student OK")

    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql_init2 = '''
    CREATE TABLE IF NOT EXISTS Teacher
            (
            Tid MESSAGE_TEXT(5) PRIMARY KEY NOT NULL,
            Tname MESSAGE_TEXT NOT NULL
            );
    '''
    c.execute(sql_init2)
    conn.commit()
    conn.close()
    print("Table Teacher OK")

    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql_init3 = '''
    CREATE TABLE if not exists Course
            (
            Cid MESSAGE_TEXT(7) PRIMARY KEY NOT NULL,
            Tid MESSAGE_TEXT(5) NOT NULL,
            Cname MESSAGE_TEXT NOT NULL,
            credit NUMERIC NOT NULL,
            grade NUMERIC NOT NULL,
            cancel_year NUMERIC
            );
    '''
    c.execute(sql_init3)
    conn.commit()
    conn.close()
    print("Table Course OK")

    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql_init4 = '''
    CREATE TABLE  if not exists Course_Choosing
            (
            Sid MESSAGE_TEXT(10),

            Cid MESSAGE_TEXT(7),

            Tid MESSAGE_TEXT(5),
            
            Chosen_year NUMERIC,
            score NUMERIC NOT NULL,
            PRIMARY KEY(Sid, Cid, Tid)
            );
    '''
    c.execute(sql_init4)
    conn.commit()
    conn.close()
    print("Table Course_Choosing OK")

    # conn = sqlite3.connect("test.db")
    # c = conn.cursor()
    # sql_init5 = '''
    #     INSERT INTO Student(Sid, Sname, sex, age, year, class)
    #     values(
    #     '1234567890', 'Jack', 'male', 20, 2021, 'Innovation'
    #     )
    #     '''
    # c.execute(sql_init5)
    # conn.commit()
    # conn.close()
    # print("Insert Student OK")


    root = tk.Tk()
    root.title('MIS for SCUT')
    width, height = root.winfo_reqwidth() + 850, 650 #窗口大小
    x, y = (root.winfo_screenwidth()  - width )/2, (root.winfo_screenheight() - height)/2
    root.geometry('%dx%d+%d+%d' % (width, height, x, y )) #窗口位置居中

    style1 = ttk.Style()
    style1.configure('my.TNotebook')

    note1 = ttk.Notebook(root, style='my.TNotebook', cursor='hand2')
    note1.pack(fill=tk.BOTH, expand=True)

    fr1 = ttk.Frame(root, relief='ridge', borderwidth=1)
    fr2 = ttk.Frame(root, relief='ridge', borderwidth=1)
    fr3 = ttk.Frame(root, relief='ridge', borderwidth=1)
    fr4 = ttk.Frame(root,relief='ridge', borderwidth=1)
    fr_bt = ttk.Frame(root, relief='ridge', borderwidth=1)

    note1.add(fr1, text='Student Information')
    note1.add(fr2, text='Teacher Information')
    note1.add(fr3, text='Course Information')
    note1.add(fr4, text='Course Choosing Information')

    fr_bt.pack()

    #########################################
    # Student Information 窗口
    # 顶上的frame，用来放表格
    topFrm1 = ttk.LabelFrame(fr1,text="")
    topFrm1.pack(side=tk.TOP,fill=tk.X, expand=False)
    label = ttk.Label(topFrm1,text = "Help: Click on the records to select. Click on the title to sort.")
    label.pack(side=tk.TOP,fill=tk.BOTH)
    # 底下的frame，用来放按钮
    botFrm1 = ttk.LabelFrame(fr1, text="")
    botFrm1.pack(side=tk.BOTTOM,fill=tk.X, expand=False)

    def InsertStudent():
        op.InsertStudent(root=root)

    def DeleteStudent():
        selected = tv1.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv1.item(selected, 'values')
            sid = temp[0]
            try:
                con = sqlite3.connect("test.db")
                c1 = con.cursor()
                sql_delete = '''
                DELETE FROM Student WHERE Sid = \'''' + sid + '\'; '
                c1.execute(sql_delete)
                con.commit()
                con.close()
                print("Delete Student OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully deleted!')
            root.destroy()
            mainPage()

    def ModifyStudent():
        selected = tv1.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv1.item(selected, 'values')
            sid = temp[0]
            name = temp[1]
            sex = temp[2]
            age = temp[3]
            year = temp[4]
            clas = temp[5]
            op.ModifyStudent(root, sid, name, sex, age, year, clas)

    def QueryStudent():
        root.destroy()
        op.QueryStudent(root)

    insert = tk.Button(botFrm1, text="Insert", bg='lightblue', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=InsertStudent, cursor='hand2')
    insert.grid(row=0, column=0, padx=4)

    delete = tk.Button(botFrm1, text="Delete", bg='pink', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=DeleteStudent, cursor='hand2')
    delete.grid(row=0, column=1, padx=4)

    modify = tk.Button(botFrm1, text='Modify', bg='yellow', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=ModifyStudent, cursor='hand2')
    modify.grid(row=0, column=2, padx=4)

    query = tk.Button(botFrm1, text='Query', bg='lightgreen', width=20, font=("Bookman Old Style", 10, "bold"),
                      command=QueryStudent, cursor='hand2')
    query.grid(row=0, column=3, padx=4)

    if usr_type != 3:
        insert.configure(state='disabled')
        delete.configure(state='disabled')
        modify.configure(state='disabled')

    tv1 = showStudent(topFrm1)

    #########################################
    topFrm2 = ttk.LabelFrame(fr2, text="")
    topFrm2.pack(side=tk.TOP, fill=tk.X, expand=False)
    label = ttk.Label(topFrm2, text="Help: Click on the records to select. Click on the title to sort.")
    label.pack(side=tk.TOP, fill=tk.BOTH)
    # 底下的frame，用来放按钮
    botFrm2 = ttk.LabelFrame(fr2, text="")
    botFrm2.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    def InsertTeacher():
        op.InsertTeacher(root=root)

    def DeleteTeacher():
        selected = tv2.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv2.item(selected, 'values')
            tid = temp[0]
            try:
                con = sqlite3.connect("test.db")
                c1 = con.cursor()
                sql_delete = '''
                DELETE FROM Teacher WHERE Tid = \'''' + tid + '\'; '
                c1.execute(sql_delete)
                con.commit()
                con.close()
                print("Delete Teacher OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully deleted!')
            root.destroy()
            mainPage()

    def ModifyTeacher():
        selected = tv2.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv2.item(selected, 'values')
            sid = temp[0]
            name = temp[1]
            op.ModifyTeacher(root, sid, name)

    def QueryTeacher():
        root.destroy()
        op.QueryTeacher(root)

    insert = tk.Button(botFrm2, text="Insert", bg='lightblue', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=InsertTeacher, cursor='hand2')
    insert.grid(row=0, column=0, padx=5)

    delete = tk.Button(botFrm2, text="Delete", bg='pink', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=DeleteTeacher, cursor='hand2')
    delete.grid(row=0, column=1, padx=5)

    modify = tk.Button(botFrm2, text='Modify', bg='yellow', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=ModifyTeacher, cursor='hand2')
    modify.grid(row=0, column=2, padx=5)

    query = tk.Button(botFrm2, text='Query', bg='lightgreen', width=20, font=("Bookman Old Style", 10, "bold"),
                      command=QueryTeacher, cursor='hand2')
    query.grid(row=0, column=3, padx=5)

    if usr_type != 3:
        insert.configure(state='disabled')
        delete.configure(state='disabled')
        modify.configure(state='disabled')

    tv2 = showTeacher(topFrm2)

    ##########################################
    topFrm3 = ttk.LabelFrame(fr3, text="")
    topFrm3.pack(side=tk.TOP, fill=tk.X, expand=False)
    label = ttk.Label(topFrm3, text="Help: Click on the records to select. Click on the title to sort.")
    label.pack(side=tk.TOP, fill=tk.BOTH)
    # 底下的frame，用来放按钮
    botFrm3 = ttk.LabelFrame(fr3, text="")
    botFrm3.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    def InsertCourse():
        op.InsertCourse(root=root)

    def DeleteCourse():
        selected = tv3.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv3.item(selected, 'values')
            cid = temp[0]
            try:
                con = sqlite3.connect("test.db")
                c1 = con.cursor()
                sql_delete = '''
                DELETE FROM Course WHERE Cid = \'''' + cid + '\'; '
                c1.execute(sql_delete)
                con.commit()
                con.close()
                print("Delete Course OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully deleted!')
            root.destroy()
            mainPage()

    def ModifyCourse():
        selected = tv3.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv3.item(selected, 'values')
            cid = temp[0]
            tid = temp[1]
            cname = temp[2]
            cr = temp[3]
            gr = temp[4]
            ca = temp[5]
            op.ModifyCourse(root, cid, tid, cname, cr, gr, ca)

    def QueryCourse():
        root.destroy()
        op.QueryCourse(root)

    tv3 = showCourse(topFrm3)

    insert = tk.Button(botFrm3, text="Insert", bg='lightblue', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=InsertCourse, cursor='hand2')
    insert.grid(row=0, column=0, padx=5)

    delete = tk.Button(botFrm3, text="Delete", bg='pink', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=DeleteCourse, cursor='hand2')
    delete.grid(row=0, column=1, padx=5)

    modify = tk.Button(botFrm3, text='Modify', bg='yellow', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=ModifyCourse, cursor='hand2')
    modify.grid(row=0, column=2, padx=5)

    query = tk.Button(botFrm3, text='Query', bg='lightgreen', width=20, font=("Bookman Old Style", 10, "bold"),
                      command=QueryCourse, cursor='hand2')
    query.grid(row=0, column=3, padx=5)

    if usr_type != 3:
        insert.configure(state='disabled')
        delete.configure(state='disabled')
        modify.configure(state='disabled')
    ##########################################
    topFrm4 = ttk.LabelFrame(fr4, text="")
    topFrm4.pack(side=tk.TOP, fill=tk.X, expand=False)
    label = ttk.Label(topFrm4, text="Help: Click on the records to select. Click on the title to sort.")
    label.pack(side=tk.TOP, fill=tk.BOTH)
    # 底下的frame，用来放按钮
    botFrm4 = ttk.LabelFrame(fr4, text="")
    botFrm4.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    def InsertChoose():
        op.InsertChoose(root=root)

    def DeleteChoose():
        selected = tv4.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv4.item(selected, 'values')
            cid = temp[0]
            tid = temp[1]
            sid = temp[2]
            try:
                con = sqlite3.connect("test.db")
                c1 = con.cursor()
                sql_delete = '''
                DELETE FROM Course_Choosing WHERE Cid = \'''' + cid + '\' and Tid = \'' + tid + '\' and Sid = \'' + sid + '\'; '
                c1.execute(sql_delete)
                con.commit()
                con.close()
                print("Delete Course OK")
            except Error as e:
                tk.messagebox.showerror('Error', 'Fail to insert, please check if the data\'s type is correct!')
            tk.messagebox.showinfo('Completed', 'Successfully deleted!')
            root.destroy()
            mainPage()

    def ModifyChoose():
        selected = tv4.focus()
        if selected == "":
            tk.messagebox.showerror('Error', 'You did not select any record!')
        else:
            temp = tv4.item(selected, 'values')
            cid = temp[0]
            tid = temp[1]
            sid = temp[2]
            cy = temp[3]
            sc = temp[4]
            op.ModifyChoose(root, cid, tid, sid, cy, sc)

    def QueryChoose():
        root.destroy()
        op.QueryChoose(root)

    def AnalysisChoose():
        root.destroy()
        op.AnalysisChoose(root)

    tv4 = showChoose(topFrm4)

    insert = tk.Button(botFrm4, text="Insert", bg='lightblue', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=InsertChoose)
    insert.grid(row=0, column=0, padx=5)

    delete = tk.Button(botFrm4, text="Delete", bg='pink', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=DeleteChoose)
    delete.grid(row=0, column=1, padx=5)

    modify = tk.Button(botFrm4, text='Modify', bg='yellow', width=20, font=("Bookman Old Style", 10, "bold"),
                       command=ModifyChoose)
    modify.grid(row=0, column=2, padx=5)

    query = tk.Button(botFrm4, text='Query', bg='lightgreen', width=20, font=("Bookman Old Style", 10, "bold"),
                      command=QueryChoose)
    query.grid(row=0, column=3, padx=5)

    analysis = tk.Button(botFrm4, text='Analysis', bg='orange', width=20, font=("Bookman Old Style", 10, "bold"),
                         command=AnalysisChoose)
    analysis.grid(row=0, column=4, padx=5)

    if usr_type == 1:
        insert.configure(state='disabled')
        delete.configure(state='disabled')
        modify.configure(state='disabled')
    elif usr_type == 2:
        insert.configure(state='disabled')
        delete.configure(state='disabled')

    root.mainloop()
