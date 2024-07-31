# 作業一 (影像的讀寫與旋轉)
**目標:**  
**1.請撰寫一可讀寫影像檔案並旋轉影像之程式，程式執行檔名稱為“HW1學號.exe”。  
2.主視窗請命名為 “AIP+學號”。  
3.可讀入的影像檔格式至少需包含JPG檔、BMP檔，以及PPM檔，輸出的影像檔格式不拘。(需與PHOTOIMPACT軟體的檔案格式相容)  
4.程式語言限C、C++、C#、Python與JAVA系列(若用其他語言需事先告知並酌量扣分)，但作業繳交時必需編譯成可執行檔且在沒有COMPILER的情況下亦能執行。  
5.程式需可選擇要輸入的檔案名稱並自動利用附檔名判斷影像格式以及影像大小，界面設計需符合要求**  

**過程:**  
**在這份作業中，我使用Tkinter來建立GUI，  
並透過OpenCV--cv2來讀取/寫入照片以及影像旋轉，將影像存檔。    
最後用PyInstaller將程式碼轉換成執行檔。**  


### 建立GUI，新增[選擇照片][顯示影像][影像旋轉][存檔]之功能鍵
![GUI](https://github.com/ttcheng26/MyAIP/blob/main/HW1/image/gui.jpg)

### 讀取影像並旋轉
![Read_Image](https://github.com/ttcheng26/MyAIP/blob/main/HW1/image/image_read.jpg)










