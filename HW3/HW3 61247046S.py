import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, Variable
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


win = tk.Tk()
win.title("AIP 61247046S") # Title
win.geometry("1150x800+300+20") # screen size
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
        cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(cv_img, (320, 320))))
        canvas1.delete('all')
        canvas1.create_image(0,0, anchor='nw', image=tk_img)
        canvas1.tk_img = tk_img
        break

def show_gray(): # 顯示灰階
    global img_path
    # img_path = filedialog.askopenfilename(title="選擇",filetypes=[('png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm')])
    img = cv_imread(img_path)
    global cv_img
    cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(cv_img, (320, 320))))
    canvas1.delete('all')
    canvas1.create_image(0,0, anchor='nw', image=tk_img)
    canvas1.tk_img = tk_img

def flip():  # 影像翻轉
    # global img_path
    # img = cv_imread(img_path)
    # cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    global cv_img
    global img2
    img2 = cv2.flip(cv2.resize(cv_img, (320, 320)), -1)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(img2))
    canvas1.delete('all')
    canvas1.create_image(0,0, anchor='nw', image=tk_img)
    canvas1.tk_img = tk_img


def gaussian():
    newWindow = tk.Toplevel(win)
    newWindow.geometry("200x130+800+300")
    labelExample = tk.Label(newWindow, text="請輸入標準差")
    labelExample.config(font=("微軟正黑體", 13, "bold"))
    num = tk.Entry(newWindow, width=15)
    def execute_and_quit():
        global cv_img
        G = 256
        height, width = cv_img.shape
        sigma = int(num.get())
        global noisy_image
        noisy_image = cv_img.copy()

        # blank image
        global blank_image
        blank_image = np.full((height, width), 255, dtype=np.uint8)

        for _ in range(50):
            # Step 3: Calculate z1 and z2 using Box-Muller transform
            r1 = np.random.rand(height, width)
            r2 = np.random.rand(height, width)
            z1 = sigma * np.cos(2 * np.pi * r2) * np.sqrt(-2 * np.log(r1))
            z2 = sigma * np.sin(2 * np.pi * r2) * np.sqrt(-2 * np.log(r1))

            # Step 4: Calculate noisy pixel values
            f_prime = noisy_image + z1
            f_prime_neighbor = np.roll(noisy_image, shift=(0, 1)) + z2

            f_prime2 = blank_image + z1
            f_prime_neighbor2 = np.roll(blank_image, shift=(0, 1)) + z2

            # Step 5: Apply thresholding
            noisy_image = np.clip(f_prime, 0, G - 1)
            noisy_image_neighbor = np.clip(f_prime_neighbor, 0, G - 1)

            blank_image = np.clip(f_prime2, 0, G - 1)
            blank_image_neighbor = np.clip(f_prime_neighbor2, 0, G - 1)

            # Check for convergence
            if np.all(np.abs(noisy_image - f_prime) < 1e-5) and np.all(
                   np.abs(noisy_image_neighbor - f_prime_neighbor) < 1e-5):
                break

            if np.all(np.abs(blank_image - f_prime2) < 1e-5) and np.all(
                     np.abs(blank_image_neighbor - f_prime_neighbor2) < 1e-5):
                break

        tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(noisy_image, (320, 320))))
        tk_img2 = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(blank_image, (320, 320))))
        canvas2.delete('all')
        canvas3.delete('all')
        canvas2.create_image(0, 0, anchor='nw', image=tk_img2)
        canvas3.create_image(0, 0, anchor='nw', image=tk_img)
        canvas2.tk_img = tk_img2
        canvas3.tk_img = tk_img

        newWindow.destroy()

    buttonExample = tk.Button(newWindow, text="產生高斯雜訊", command=execute_and_quit)
    buttonExample.config(font=("微軟正黑體", 10, "bold"))

    labelExample.pack()
    num.pack()
    buttonExample.pack()


def salt_and_pepper():
    newWindow2 = tk.Toplevel(win)
    newWindow2.geometry("200x130+800+300")
    labelExample2 = tk.Label(newWindow2, text="請輸入百分比")
    labelExample2.config(font=("微軟正黑體", 13, "bold"))
    num2 = tk.Entry(newWindow2, width=15)
    def execute_and_quit2():
         global cv_img
         height, width = cv_img.shape
         global noisy_image
         noisy_image = cv_img.copy()
         # Create a blank image (black)
         global blank_image
         blank_image = np.full((height, width), 255, dtype=np.uint8)
         # blank_image = np.zeros((height, width), dtype=np.uint8)
         p = int(num2.get())

         num_pixels = int(height * width * p/100)

         # Generate random pixel coordinates to add impulse noise
         impulse_coordinates = [np.random.randint(0, height, num_pixels), np.random.randint(0, width, num_pixels)]

         # Set randomly selected pixels to either pure black (0) or pure white (255)
         for i in range(num_pixels):
             x, y = impulse_coordinates[0][i], impulse_coordinates[1][i]
             if np.random.random() < 0.5:
                 noisy_image[x, y], blank_image[x,y] = 0, 0  # Set to black
             else:
                 noisy_image[x, y], blank_image[x,y] = 255, 255  # Set to white

         tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(noisy_image, (320, 320))))
         tk_img2 = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(blank_image, (320, 320))))
         canvas2.delete('all')
         canvas3.delete('all')
         canvas2.create_image(0, 0, anchor='nw', image=tk_img2)
         canvas3.create_image(0, 0, anchor='nw', image=tk_img)
         canvas2.tk_img = tk_img2
         canvas3.tk_img = tk_img

         newWindow2.destroy()

    buttonExample2 = tk.Button(newWindow2, text="產生椒鹽雜訊", command=execute_and_quit2)
    buttonExample2.config(font=("微軟正黑體", 10, "bold"))

    labelExample2.pack()
    num2.pack()
    buttonExample2.pack()



def histogram(): # 顯示直方圖
    global cv_img
    img3 = cv2.equalizeHist(cv_img)
    plt.figure()
    plt.hist(img3.ravel(), 256, [0, 255], color="black")
    plt.savefig("hist1.png")
    plt.close()
    global hist1
    hist1 = cv_imread("hist1.png")
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(hist1, (320, 320))))
    canvas4.delete('all')
    canvas4.create_image(0,0, anchor='nw', image=tk_img)
    canvas4.tk_img = tk_img
    os.remove("hist1.png")

    global blank_image
    img4, bins = np.histogram(blank_image.flatten(), bins=256, range=[0,256])
    plt.figure()
    # plt.hist(img4.ravel(), 256, [0, 255], color="black")
    plt.plot(img4, color = 'black')
    plt.savefig("hist2.png")
    plt.close()
    global hist2
    hist2 = cv_imread("hist2.png")
    tk_img2 = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(hist2, (320, 320))))
    canvas5.delete('all')
    canvas5.create_image(0,0, anchor='nw', image=tk_img2)
    canvas5.tk_img = tk_img2
    os.remove("hist2.png")

    global noisy_image
    img5, bins = np.histogram(noisy_image.flatten(), bins=256, range=[0,256])
    # img5 = cv2.equalizeHist(noisy_image)
    plt.figure()
    plt.plot(img5, color = 'black')
    # plt.hist(img5.ravel(), 256, [0, 255], color="black")
    plt.savefig("hist3.png")
    plt.close()
    global hist3
    hist3 = cv_imread("hist3.png")
    tk_img3 = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(hist3, (320, 320))))
    canvas6.delete('all')
    canvas6.create_image(0,0, anchor='nw', image=tk_img3)
    canvas6.tk_img = tk_img3
    os.remove("hist3.png")
    # tk_img = tk.PhotoImage(file="hist.png")

# def save(): # 存檔
#     global img2
#     img_path = filedialog.asksaveasfile(mode='w',defaultextension='.png', filetypes=[('png', '*.png'), ('jpg', '*.jpg'), ('gif', '*.gif'), ('bmp', '*.bmp'), ('ppm', '*.ppm'), ('jpeg', '*.jpeg')]).name  # 指定儲存檔案格式
#     # img_type = img_path.split('.')[1]  # 取得檔案類型
#     img_save = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)
#     cv2.imwrite(img_path, img2)

btn1 = tk.Button(text="選擇照片", bg="skyblue", command=show)
btn1.config(font="微軟正黑體 15")
btn1.pack()

btn2 = tk.Button(text="影像旋轉", bg="skyblue", command=flip)
btn2.config(font="微軟正黑體 15")
btn2.pack()

# btn3 = tk.Button(text="存檔", bg="skyblue", command=save)
# btn3.config(font="微軟正黑體 15")
# btn3.pack()

btn4 = tk.Button(text="顯示灰階", bg="skyblue", command=show_gray)
btn4.config(font="微軟正黑體 15")
btn4.pack()

btn5 = tk.Button(text="直方圖", bg="skyblue", command=histogram)
btn5.config(font="微軟正黑體 15")
btn5.pack()

btn6 = tk.Button(text="雜訊產生(高斯)", bg="skyblue", command=gaussian)
btn6.config(font="微軟正黑體 15")
btn6.pack()

btn7 = tk.Button(text="雜訊產生(椒鹽)", bg="skyblue", command=salt_and_pepper)
btn7.config(font="微軟正黑體 15")
btn7.pack()

frame1 = tk.Frame(win, width=400, height=400)
frame1.pack()

frame2 = tk.Frame(win, width=400, height=400)
frame2.pack()

frame3 = tk.Frame(win, width=400, height=400)
frame3.pack()

frame4 = tk.Frame(win, width=400, height=400)
frame4.pack()

frame5 = tk.Frame(win, width=400, height=400)
frame5.pack()

frame6 = tk.Frame(win, width=400, height=400)
frame6.pack()


canvas1 = tk.Canvas(frame1, width=320, height=320)
canvas2 = tk.Canvas(frame2, width=320, height=320)
canvas3 = tk.Canvas(frame3, width=320, height=320)
canvas4 = tk.Canvas(frame4, width=320, height=320)
canvas5 = tk.Canvas(frame5, width=320, height=320)
canvas6 = tk.Canvas(frame6, width=320, height=320)

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

scroller3X = tk.Scrollbar(frame3, orient="horizontal")
scroller3X.pack(side="bottom", fill="x")
scroller3X.config(command=canvas3.xview)
scroller3Y = tk.Scrollbar(frame3, orient="vertical")
scroller3Y.pack(side="right", fill="y")
scroller3Y.config(command=canvas3.yview)

scroller4X = tk.Scrollbar(frame4, orient="horizontal")
scroller4X.pack(side="bottom", fill="x")
scroller4X.config(command=canvas4.xview)
scroller4Y = tk.Scrollbar(frame4, orient="vertical")
scroller4Y.pack(side="right", fill="y")
scroller4Y.config(command=canvas4.yview)

scroller5X = tk.Scrollbar(frame5, orient="horizontal")
scroller5X.pack(side="bottom", fill="x")
scroller5X.config(command=canvas5.xview)
scroller5Y = tk.Scrollbar(frame5, orient="vertical")
scroller5Y.pack(side="right", fill="y")
scroller5Y.config(command=canvas5.yview)

scroller6X = tk.Scrollbar(frame6, orient="horizontal")
scroller6X.pack(side="bottom", fill="x")
scroller6X.config(command=canvas6.xview)
scroller6Y = tk.Scrollbar(frame6, orient="vertical")
scroller6Y.pack(side="right", fill="y")
scroller6Y.config(command=canvas6.yview)

canvas1.config(xscrollcommand=scroller1X.set, yscrollcommand=scroller1Y.set)
canvas1.pack(side="left")

canvas2.config(xscrollcommand=scroller2X.set, yscrollcommand=scroller2Y.set)
canvas2.pack(side="left")

canvas3.config(xscrollcommand=scroller3X.set, yscrollcommand=scroller3Y.set)
canvas3.pack(side="left")

canvas4.config(xscrollcommand=scroller4X.set, yscrollcommand=scroller4Y.set)
canvas4.pack(side="left")

canvas5.config(xscrollcommand=scroller5X.set, yscrollcommand=scroller5Y.set)
canvas5.pack(side="left")

canvas6.config(xscrollcommand=scroller6X.set, yscrollcommand=scroller6Y.set)
canvas6.pack(side="left")

frame1.place(x=0, y=50)
frame2.place(x=400, y=50)
frame3.place(x=800, y=50)
frame4.place(x=0, y=450)
frame5.place(x=400, y=450)
frame6.place(x=800, y=450)

btn1.place(x=0, y=0) # select image
btn2.place(x=200, y=0) # flip image
# btn3.place(x=800, y=0) # save
btn4.place(x=100, y=0) # gray image
btn5.place(x=605, y=0) # histogram
btn6.place(x=300, y=0) # noise
btn7.place(x=452, y=0) # noise

win.mainloop()








