import sqlite3


# 打开数据库
def opendb():
    conn = sqlite3.connect("testdb.db")
    cur = conn.execute(
        """create table if not exists student(usernum integer primary key,username varcher(128), sex varchar(20),age varchar(25), jiguan varchar(28),classroom varchar(30),score integer)""")
    return cur, conn


# 查询全部信息
def showalldb():
    print("--------------------处理后的数据--------------------")
    hel = opendb()
    cur = hel[1].cursor()
    cur.execute("select*from student")
    res = cur.fetchall()
    for line in res:
        for h in line:
            print(h),
        print
    cur.close()


# 输入信息
def into():
    usernum = input("请输入学号：")
    username1 = input("请输入姓名：")
    sex = input("请输入性别：")
    age = input("请输入年龄：")
    jiguan = input("请输入籍贯：")
    classroom = input("请输入班级：")
    score = int(input("请输入成绩："))
    return usernum, username1, sex, age, jiguan, classroom, score


# 网数据库中添加内容
def adddb():
    welcome = """----------欢迎使用数据库功能----------"""
    print(welcome)
    person = into()
    hel = opendb()
    hel[1].execute("insert into student(usernum,username, sex, age,jiguan,classroom,score)values (?,?,?,?,?,?,?)",
                   (person[0], person[1], person[2], person[3], person[4], person[5], person[6]))
    hel[1].commit()
    print("----------恭喜你，数据添加成功----------")
    showalldb()
    hel[1].close()


# 删除数据库中的内容
def deldb():
    welcome = "----------欢迎使用删除数据库功能-----------"
    print(welcome)
    delchoice = input("请输入要删除的学号：")
    hel = opendb()  # 返回游标conn
    hel[1].execute("delete from student where usernum=" + delchoice)
    hel[1].commit()
    print("----------恭喜你，数据删除成功----------")
    showalldb()
    hel[1].close()


# 修改数据库内容
def alter():
    welecome = "----------欢迎使用修改数据库功能----------"
    print(welcome)
    changechoice = input("请输入想要修改的学生的学号;")
    hel = opendb()
    person = into()
    hel[1].execute(
        "update  student set usernum=?,username=?, sex=?, age=?,jiguan=?,classroom=?,score=? where usernum=" + changechoice,
        (person[0], person[1],
         person[2], person[3], person[4], person[5], person[6]))
    hel[1].commit()
    showalldb()
    hel[1].close


# 查询数据
def searchdb():
    welcome = "----------欢迎使用数据库查询功能----------"
    print(welcome)
    choice = input("请输入类别查询的方式，如：（学号，姓名，性别，籍贯，班级）")
    searlist = ['', '']
    if choice == "学号":
        searlist[0] = "usernum"
        searlist[1] = input("请输入学号:")
    elif choice == "姓名":
        searlist[0] = "usrname"
        searlist[1] = input("请输入姓名:")
    elif choice == "性别":
        searlist[0] = "sex"
        searlist[1] = input("请输入性别:")
    elif choice == "籍贯":
        searlist[0] = "jiguan"
        searlist[1] = input("请输入籍贯:")
    elif choice == "班级":
        searlist[0] = "classroom"
        searlist[1] = input("请输入班级:")
    hel = opendb()
    cur = hel[1].cursor()
    cur.execute("select*from student where " + searlist[0] + "=" + searlist[1])
    hel[1].commit()
    print("-----------恭喜你，你要查询的数据如下-----------")
    for row in cur:
        print(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    cur.close()
    hel[1].close()


# 按类统计每个班级或性别的平均成绩
def searchClass():
    welcome = "----------欢迎使用数据库统计功能----------"
    print(welcome)
    choice = input("请输入你要按什么类型统计，如（班级，性别）")
    searList = ['', '']
    if choice == '班级':
        searList[0] = 'classroom'
        searList[1] = input("请输入你要统计的班级:")
    elif choice == '性别':
        searList[0] = 'sex'
        searList[1] = input("请输入你要统计的性别:")
    hel = opendb()
    cur = hel[1].cursor()
    cur.execute("select * from student where " + searList[0] + "=" + searList[1])
    hel[1].commit()
    print("-----------恭喜你，你要统计的数据如下-----------")
    result = [0, 0]
    for item in cur:
        result[0] += item[6]
        result[1] += 1
    print("按" + choice + "统计的平均成绩是：%.2lf" % (result[0] / result[1]))
    cur.close()
    hel[1].close()


# 按成绩排序并输出结果
def sortScore():
    welcome = "----------欢迎使用数据库统计功能----------"
    print(welcome)
    hel = opendb()
    cur = hel[1].cursor()
    cur.execute("select * from student ")
    sortList = []
    for item in cur:
        sortList.append(
            {"学号": item[0], "姓名": item[1], "性别": item[2], "年龄": item[3], "籍贯": item[4], "班级": item[5],
             "成绩": item[6]})
    sortList.sort(key=lambda x: x["成绩"])
    for item in sortList:
        print(item)
    cur.close()
    hel[1].close()


# 是否继续
def conti(a):
    choice = input("是否继续?(y or n):")
    if choice == 'y':
        a = 1
    else:
        a = 0
    return a


if __name__ == "__main__":
    flag = 1
    while flag:
        welcome = "---------欢迎使用数据库通讯功能----------"
        print(welcome)
        choiceshow = """
请选择你的进一步选择：
（添加）往数据库中添加内容
（删除）删除数据库中内容
（修改）修改数据库的内容
（查询）查询数据的内容
（统计）按类统计每个班级或性别的平均成绩
（排序）按成绩排序并输出结果
选择你想要进行的操作：
"""
        choice = input(choiceshow)
        if choice == "添加":
            adddb()
            conti(flag)
        elif choice == "删除":
            deldb()
            conti(flag)
        elif choice == "修改":
            alter()
            conti(flag)
        elif choice == "查询":
            searchdb()
            conti(flag)
        elif choice == '统计':
            searchClass()
            conti(flag)
        elif choice == '排序':
            sortScore()
            conti(flag)
        else:
            print("你输入错误，请重新输入")


