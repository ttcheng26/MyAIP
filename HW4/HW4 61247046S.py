import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Tk, Label, StringVar, Button, Entry, filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


win = tk.Tk()
win.title("AIP 61247046S") # Title
win.geometry("1150x600+300+20") # screen size
win.config(bg="#323232") # background color

def cv_imread(filePath): # 避免檔名中文發生錯誤
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8), -1)
    return cv_img

def show(): # 顯示照片
    global img_path
    img_path = filedialog.askopenfilename(title="選擇", filetypes=[('png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm')])
    while img_path != '':
        img = cv_imread(img_path)
        global cv_img
        cv_img = cv2.cvtColor(cv2.resize(img, (512, 512)), cv2.COLOR_BGR2GRAY)
        tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
        canvas1.delete('all')
        canvas1.create_image(0,0, anchor='nw', image=tk_img)
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
    canvas2.create_image(0,0, anchor='nw', image=tk_img)
    canvas2.tk_img = tk_img

def smoothing():
    global cv_img
    NewWindow = tk.Toplevel(win)
    NewWindow.geometry('250x250+700+200')
    NewWindow.config(bg='bisque2')
    label = tk.Label(NewWindow, text="Enter convolution masks"+"\n"+"(5X5 Matrix)")
    label.config(font=("微軟正黑體", 13, "bold"), bg='bisque2')

    # empty arrays for your Entrys and StringVars
    text_var = []
    entries = []
    x2 = 0
    y2 = 0
    rows, cols = (5, 5)
    for i in range(rows):
        # append an empty list to your two arrays
        # so you can append to those later
        text_var.append([])
        entries.append([])
        for j in range(cols):
            # append your StringVar and Entry
            text_var[i].append(StringVar())
            entries[i].append(Entry(NewWindow, textvariable=text_var[i][j], width=4))
            entries[i][j].place(x=30 + x2, y=50 + y2)
            x2 += 40

        y2 += 30
        x2 = 0

        def get_mat():
            matrix = []
            for i in range(rows):
                matrix.append([])
                for j in range(cols):
                    if text_var[i][j].get() == '':
                        matrix[i].append(0)
                    else:
                        matrix[i].append(int(text_var[i][j].get()))
            matrix = np.array(matrix)
            sum = np.sum(matrix, dtype=np.int32)
            if sum == 0:
                sum = 1

            matrix = matrix / sum

            # kernel size
            kernel_size = 5

            # zero padding
            padding_size = kernel_size // 2
            input_image_padded = cv2.copyMakeBorder(cv_img, padding_size, padding_size, padding_size, padding_size,
                                                    cv2.BORDER_CONSTANT, value=0)

            # get image and kernel width&height
            image_height, image_width = input_image_padded.shape
            kernel_height, kernel_width = matrix.shape

            # calculate output image width and height
            output_height = image_height - kernel_height + 1
            output_width = image_width - kernel_width + 1

            # initial output image
            output_image = np.zeros((output_height, output_width))

            # execute convolution
            for i in range(output_height):
                for j in range(output_width):
                    # get matrix which match the kernel
                    input_region = input_image_padded[i:i + kernel_height, j:j + kernel_width]

                    # check region is match with kernel or not
                    if input_region.shape == matrix.shape:
                        output_image[i, j] = np.sum(input_region * matrix)

            global img2
            img2 = output_image
            tk_img = ImageTk.PhotoImage(image=Image.fromarray(img2))
            canvas2.delete('all')
            canvas2.create_image(0, 0, anchor='nw', image=tk_img)
            canvas2.tk_img = tk_img

            NewWindow.destroy()

        btn = tk.Button(NewWindow, text="Create Image", command=get_mat)
        btn.place(x=77, y=200)
        label.pack()

def edge_detection():
    NewWindow = tk.Toplevel(win)
    NewWindow.geometry('250x250+700+200')
    NewWindow.config(bg='bisque2')
    label = tk.Label(NewWindow, text="Enter convolution masks" + "\n" + "(5X5 Matrix)")
    label.config(font=("微軟正黑體", 13, "bold"), bg='bisque2')

    # empty arrays for your Entrys and StringVars
    text_var = []
    entries = []

    x2 = 0
    y2 = 0
    rows, cols = (5, 5)
    for i in range(rows):
        # append an empty list to your two arrays
        # so you can append to those later
        text_var.append([])
        entries.append([])
        for j in range(cols):
            # append your StringVar and Entry
            text_var[i].append(StringVar())
            entries[i].append(Entry(NewWindow, textvariable=text_var[i][j], width=4))
            entries[i][j].place(x=30 + x2, y=50 + y2)
            x2 += 40

        y2 += 30
        x2 = 0

    def get_mat():
            matrix = []
            for i in range(rows):
                matrix.append([])
                for j in range(cols):
                    if text_var[i][j].get() == '':
                        matrix[i].append(0)
                    else:
                        matrix[i].append(int(text_var[i][j].get()))
            matrix = np.array(matrix)

            # kernel size
            kernel_size = 5

            # zero padding
            padding_size = kernel_size // 2
            input_image_padded = cv2.copyMakeBorder(cv_img, padding_size, padding_size, padding_size, padding_size,
                                                    cv2.BORDER_CONSTANT, value=0)

            # get image and kernel width&height
            image_height, image_width = input_image_padded.shape
            kernel_height, kernel_width = matrix.shape

            # calculate output image width and height
            output_height = image_height - kernel_height + 1
            output_width = image_width - kernel_width + 1

            # initial output image
            output_image = np.zeros((output_height, output_width))

            # execute convolution
            for i in range(output_height):
                for j in range(output_width):
                    # get matrix which match the kernel
                    input_region = input_image_padded[i:i + kernel_height, j:j + kernel_width]

                    # check region is match with kernel or not
                    if input_region.shape == matrix.shape:
                        output_image[i, j] = np.sum(input_region * matrix)

            global img2
            img2 = output_image
            tk_img = ImageTk.PhotoImage(image=Image.fromarray(img2))
            canvas2.delete('all')
            canvas2.create_image(0, 0, anchor='nw', image=tk_img)
            canvas2.tk_img = tk_img

            NewWindow.destroy()

    btn = tk.Button(NewWindow, text="Create Image", command=get_mat)
    btn.place(x=77, y=200)
    label.pack()

def save(): # 存檔
    global img2
    img_path = filedialog.asksaveasfile(mode='w',defaultextension='.png', filetypes=[('png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm'), ('jpeg', '*.jpeg')]).name  # 指定儲存檔案格式
    cv2.imwrite(img_path, img2)

btn1 = tk.Button(text="選擇照片", bg="skyblue", command=show)
btn1.config(font="微軟正黑體 15")
btn1.pack()

btn2 = tk.Button(text="影像旋轉", bg="skyblue", command=flip)
btn2.config(font="微軟正黑體 15")
btn2.pack()

btn3 = tk.Button(text="平滑化", bg="skyblue", command=smoothing)
btn3.config(font="微軟正黑體 15")
btn3.pack()

btn4 = tk.Button(text="邊緣偵測", bg="skyblue", command=edge_detection)
btn4.config(font="微軟正黑體 15")
btn4.pack()

btn5 = tk.Button(text="存檔", bg="skyblue", command=save)
btn5.config(font="微軟正黑體 15")
btn5.pack()

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
btn1.place(x=0, y=0) # select image
btn2.place(x=100, y=0) # flip image
btn3.place(x=200, y=0) # smoothing
btn4.place(x=280, y=0) # edge dection
btn5.place(x=600, y=0) # save


win.mainloop()