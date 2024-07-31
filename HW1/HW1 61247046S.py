import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, Variable
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


win = tk.Tk()
win.title("AIP 61247046S")  # Title
win.geometry("1200x700+300+20")  # screen size
win.config(bg="#323232")  # background color
# win.iconbitmap("photo.ico") # icon


def cv_imread(filePath):  # 避免檔名中文發生錯誤
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img


def show():  # 顯示照片
    global img_path
    img_path = filedialog.askopenfilename(title="選擇", filetypes=[(
        'png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm')])
    while img_path != '':
        img = cv_imread(img_path)
        global cv_img
        cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        tk_img = ImageTk.PhotoImage(
            image=Image.fromarray(cv2.resize(cv_img, (512, 512))))
        canvas1.delete('all')
        canvas1.create_image(0, 0, anchor='nw', image=tk_img)
        canvas1.tk_img = tk_img
        break


def flip():  # 影像翻轉
    # global img_path
    # img = cv_imread(img_path)
    # cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    global cv_img
    global img2
    img2 = cv2.flip(cv2.resize(cv_img, (512, 512)), -1)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(img2))
    canvas2.delete('all')
    canvas2.create_image(0, 0, anchor='nw', image=tk_img)
    canvas2.tk_img = tk_img


def save():  # 存檔
    global img2
    img_path = filedialog.asksaveasfile(mode='w', defaultextension='.png', filetypes=[(
        'png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm'), ('jpeg', '*.jpeg')]).name  # 指定儲存檔案格式
    # img_type = img_path.split('.')[1]  # 取得檔案類型
    img_save = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)
    cv2.imwrite(img_path, img2)


btn1 = tk.Button(text="選擇照片", bg="skyblue", command=show)
btn1.config(font="微軟正黑體 15")
btn1.pack()

btn2 = tk.Button(text="影像旋轉", bg="skyblue", command=flip)
btn2.config(font="微軟正黑體 15")
btn2.pack()

btn3 = tk.Button(text="存檔", bg="skyblue", command=save)
btn3.config(font="微軟正黑體 15")
btn3.pack()

frame1 = tk.Frame(win, width=400, height=400)
frame1.pack()

frame2 = tk.Frame(win, width=400, height=400)
frame2.pack()

canvas1 = tk.Canvas(frame1, width=520, height=520)
canvas2 = tk.Canvas(frame2, width=520, height=520)


scroller1X = tk.Scrollbar(frame1, orient="horizontal")
scroller1X.pack(side="bottom", fill="x")
scroller1X.config(command=canvas1.xview)

scroller1Y = tk.Scrollbar(frame1, orient="vertical")
scroller1Y.pack(side="right", fill="y")
scroller1Y.config(command=canvas1.yview)

scroller2X = tk.Scrollbar(frame2, orient="horizontal")
scroller2X.pack(side="bottom", fill="x")
scroller2X.config(command=canvas2.xview)

scroller2Y = tk.Scrollbar(frame2, orient="vertical")
scroller2Y.pack(side="right", fill="y")
scroller2Y.config(command=canvas2.yview)

canvas1.config(xscrollcommand=scroller1X.set, yscrollcommand=scroller1Y.set)
canvas1.pack(side="left")

canvas2.config(xscrollcommand=scroller2X.set, yscrollcommand=scroller2Y.set)
canvas2.pack(side="left")

frame1.place(x=0, y=50)
frame2.place(x=600, y=50)
btn1.place(x=0, y=0)  # select image
btn2.place(x=600, y=0)  # flip image
btn3.place(x=800, y=0)  # save

win.mainloop()
