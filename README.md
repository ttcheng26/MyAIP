# NTNU Course -- AIP
The project was learned and created as part of AIP course at school.
This utilizes Python for its programming language, and the GUI is created using Tkinter.

## 1. Image Gray scale & GUI created
首先安裝需要的Package, GUI我所使用的是Tkinter, 原因在於介面簡單、清楚。

    import tkinter as tk
    from PIL import Image, ImageTk
    from tkinter import filedialog, Variable
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import os