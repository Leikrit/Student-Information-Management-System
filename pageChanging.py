import tkinter as tk


# 按钮对应的功能
def create_frame1():
    global frame3, frame2, frame1
    try:
        frame1.destroy()
    except:
        pass
    finally:
        try:
            frame2.destroy()
        except:
            pass
        finally:
            try:
                frame3.destroy()
            except:
                pass
            finally:
                frame1 = tk.Frame(window, height=600, width=1080, bg='pink')
                frame1.pack(side='bottom', fill='both', expand=1)
                frame1.pack_propagate(0)
                label = tk.Label(frame1,
                                 text='界面一',
                                 font=('微软雅黑',18),
                                 bg='pink')
                label.pack()

def create_frame2():
    global frame3, frame2, frame1
    try:
        frame1.destroy()
    except:
        pass
    finally:
        try:
            frame3.destroy()
        except:
            pass
        finally:
            frame2 = tk.Frame(window, height=600, width=1080, bg='blue')
            frame2.pack(side='bottom', fill='both', expand=1)
            frame2.pack_propagate(0)
            label = tk.Label(frame2,
                             text='界面二',
                             font=('微软雅黑',18),
                             bg='blue')
            label.pack()

def create_frame3():
    global frame3, frame2, frame1
    try:
        frame1.destroy()
    except:
        pass
    finally:
        try:
            frame2.destroy()
        except:
            pass
        finally:
            frame3 = tk.Frame(window, height=600, width=1080, bg='green')
            frame3.pack(side='bottom', fill='both', expand=1)
            frame3.pack_propagate(0)
            label = tk.Label(frame3,
                             text='界面三',
                             font=('微软雅黑',18),
                             bg='green')
            label.pack()

#创建窗口
window = tk.Tk()
window.geometry('1080x720')
window.title("多窗口切换")

# 按钮框架
frame0 = tk.Frame(window, height=120, width=1080, bg='pink')
frame0.pack(side='top', fill='both', expand=1)

# 界面切换按钮
btn1 = tk.Button(frame0, text='界面一', command=create_frame1)
btn1.place(relx=0, rely=0, relwidth=0.3, relheight=1)

btn2 = tk.Button(frame0, text='界面二', command=create_frame2)
btn2.place(relx=0.3, rely=0, relwidth=0.3, relheight=1)

btn3 = tk.Button(frame0, text='界面三', command=create_frame3)
btn3.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

# 首先打开主界面
create_frame1()

window.mainloop()  # 进入消息循环
