import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, Variable
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

win = tk.Tk()
win.title("AIP 61247046S") # Title
win.geometry("920x920+300+20") # screen size
win.config(bg="#323232") # background color
# win.iconbitmap("photo.ico") # icon

def cv_imread(filePath): # 避免檔名中文發生錯誤
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8), -1)
    return cv_img

def show(): # 顯示照片
    global img_path
    img_path = filedialog.askopenfilename(title="選擇", filetypes=[('png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm')])
    while img_path != '':
        img = cv_imread(img_path)
        global cv_img
        cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(cv_img, (400, 400))))
        canvas1.delete('all')
        canvas1.create_image(0,0, anchor='nw', image=tk_img)
        canvas1.tk_img = tk_img
        break


def flip():  # 影像翻轉
    global cv_img
    global img2
    img2 = cv2.flip(cv2.resize(cv_img, (400, 400)), -1)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(img2))
    canvas1.delete('all')
    canvas1.create_image(0,0, anchor='nw', image=tk_img)
    canvas1.tk_img = tk_img

def histogram(): # 顯示直方圖
    global cv_img
    # img3 = cv2.calcHist([cv_img], [0], None, [256], [0, 256])
    # img3 = cv2.equalizeHist(cv_img)
    plt.figure()
    plt.hist(cv_img.ravel(), 256, [0, 255], color="black")
    plt.savefig("hist.png")
    plt.close()
    global img2
    img2 = cv_imread("hist.png")
    # tk_img = tk.PhotoImage(file="hist.png")
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(img2, (400, 400))))
    canvas3.delete('all')
    canvas3.create_image(0,0, anchor='nw', image=tk_img)
    canvas3.tk_img = tk_img
    os.remove("hist.png")

def histogram_equalization(): # 顯示直方圖
    global cv_img
    # Compute the histogram
    hist, bins = np.histogram(cv_img.flatten(), 256, [0, 256])

    # Compute the cumulative distribution function (CDF)
    cdf = hist.cumsum()

    # Normalize the CDF to the range [0, 255]
    cdf_normalized = (cdf * 255) / cdf[-1]

    # Map the pixel values to their equalized values
    equalized_image = np.interp(cv_img.flatten(), bins[:-1], cdf_normalized)

    # Reshape the equalized image to its original shape

    equalized_image = equalized_image.reshape(cv_img.shape)
    equalized_image = equalized_image.astype(np.uint8)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(equalized_image, (400, 400))))
    canvas2.delete('all')
    canvas2.create_image(0, 0, anchor='nw', image=tk_img)
    canvas2.tk_img = tk_img


    plt.figure()
    plt.hist(equalized_image.ravel(), 256, [0, 255], color="black")
    plt.savefig("hist.png")
    plt.close()
    global img5
    img5 = cv_imread("hist.png")
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(img5, (400, 400))))
    canvas4.delete('all')
    canvas4.create_image(0,0, anchor='nw', image=tk_img)
    canvas4.tk_img = tk_img
    os.remove("hist.png")



btn1 = tk.Button(text="選擇照片", bg="skyblue", command=show)
btn1.config(font="微軟正黑體 15")
btn1.pack()

btn2 = tk.Button(text="影像旋轉", bg="skyblue", command=flip)
btn2.config(font="微軟正黑體 15")
btn2.pack()



btn5 = tk.Button(text="直方圖", bg="skyblue", command=histogram)
btn5.config(font="微軟正黑體 15")
btn5.pack()

btn4 = tk.Button(text="直方圖均化", bg="skyblue", command=histogram_equalization)
btn4.config(font="微軟正黑體 15")
btn4.pack()


frame1 = tk.Frame(win, width=400, height=400)
frame1.pack()

frame2 = tk.Frame(win, width=400, height=400)
frame2.pack()

frame3 = tk.Frame(win, width=400, height=400)
frame3.pack()

frame4 = tk.Frame(win, width=400, height=400)
frame4.pack()

canvas1 = tk.Canvas(frame1, width=400, height=400)
canvas2 = tk.Canvas(frame2, width=400, height=400)
canvas3 = tk.Canvas(frame3, width=400, height=400)
canvas4 = tk.Canvas(frame4, width=400, height=400)

canvas1.config()
canvas1.pack(side="left")

canvas2.config()
canvas2.pack(side="left")

canvas3.config()
canvas3.pack(side="left")

canvas4.config()
canvas4.pack(side="left")

frame1.place(x=0, y=50)
frame2.place(x=500, y=50)
frame3.place(x=0, y=500)
frame4.place(x=500, y=500)
btn1.place(x=0, y=0) # select image
btn2.place(x=100, y=0) # flip image
btn5.place(x=200, y=0) # histogram
btn4.place(x=280, y=0) # histogram equalization
win.mainloop()