import tkinter as tk
from tkinter.filedialog import askdirectory, asksaveasfile
import os
from PIL import ImageTk, Image
from tkinter import ttk, simpledialog, messagebox
import pandas as pd
import numpy as np


class MainWindow:
    def __init__(self, window) -> None:

        self.label = {}

        self.window = window

        self.frameTop = tk.Frame(window)

        # top left
        frameLeft = tk.Frame(self.frameTop)
        self.btnOpen = tk.Button(
            frameLeft, text='Open Folder', command=self.openFolder)
        self.btnSave = tk.Button(frameLeft, text='Save', command=self.save)
        self.btnOpen.grid(row=0, column=0, ipadx=10)
        self.btnSave.grid(row=1, column=0, ipadx=30, pady=10)
        frameLeft.grid(row=0, column=0, sticky="ew", padx=(10, 30), pady=10)

        # top right
        frameRight = tk.Frame(self.frameTop)
        frameRTop = tk.Frame(frameRight)
        self.combobox = ttk.Combobox(
            frameRTop, width=50, state="readonly")
        value_label = ()
        self.combobox['values'] = value_label
        self.btnAddLabel = tk.Button(
            frameRTop, text='Add label', command=self.addLabel)
        self.combobox.grid(row=0, column=0)
        self.btnAddLabel.grid(row=0, column=1, ipadx=10, padx=(10, 0))
        frameRTop.grid(row=0, column=0,  pady=(20, 10))

        frameRButtom = tk.Frame(frameRight)
        self.btnBack = tk.Button(frameRButtom, text='Back', command=self.back)
        self.btnNext = tk.Button(
            frameRButtom, text='Next', command=self.next)

        self.btnBack.grid(row=1, column=0, ipadx=10, padx=(10, 50))
        self.btnNext.grid(row=1, column=1, ipadx=10)
        frameRButtom.grid(row=1, column=0, sticky='W')

        frameRight.grid(row=0, column=1, sticky='N', ipady=15)

        self.frameTop.grid(row=0, column=0, pady=10)

        self.canvas = tk.Canvas(window, width=550, height=350,)
        self.canvas.grid(row=1, column=0)

    def resize_image(self, img):
        while img.size[0] > 550 or img.size[0] > 350:
            img = img.resize((round(img.size[0]*0.9), round(img.size[1]*0.9)))
        return img

    def setImageCanvas(self, image_name):

        if image_name in self.label.keys():
            label = self.label[image_name]
            self.combobox.set(label)

        image_name = os.path.join(self.folder, image_name)
        img = Image.open(image_name)
        img = self.resize_image(img)
        img = ImageTk.PhotoImage(img)

        self.canvas.delete('all')
        self.canvas.background = img
        self.canvas_img = self.canvas.create_image(
            300, self.frameTop.winfo_height()+50, anchor=tk.CENTER, image=self.canvas.background)

    def openFolder(self):
        self.path_images = []
        self.folder = None
        self.current_image_index = 0
        self.folder = askdirectory()
        if self.folder == '':
            return
        for i in os.listdir(self.folder):
            if i.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'tiff']:
                self.path_images.append(i)
        fileName = self.path_images[self.current_image_index]
        self.setImageCanvas(fileName)

    def addLabel(self):
        label = simpledialog.askstring(title='Lable', prompt='Nhap label: ')
        if label is None:
            return
        if label not in self.combobox['values']:
            self.combobox['values'] += (label,)

    def getLabelValue(self):
        label = self.combobox.get()
        self.label[self.path_images[self.current_image_index]] = label

    def next(self):
        if len(self.path_images) == 0:
            return
        self.getLabelValue()
        self.current_image_index += 1
        if self.current_image_index == len(self.path_images):
            self.current_image_index = 0
        self.setImageCanvas(self.path_images[self.current_image_index])

    def back(self):
        if len(self.path_images) == 0:
            return
        self.getLabelValue()
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.path_images)-1

        self.setImageCanvas(self.path_images[self.current_image_index])

    def save(self):
        files = [
            ('CSV file', '*.csv'), ]
        file = asksaveasfile(filetypes=files, defaultextension=files)
        if file is None:
            return
        data = []
        for k, v in self.label.items():
            data.append([k, v])
        data = np.array(data)
        df = pd.DataFrame(data)
        df.to_csv(file.name, index=None, header=None)
        messagebox.showinfo("Info", "Lưu thành công")


window = tk.Tk()
window.title("Tool label for object classification")
window.geometry('600x500')
window.resizable(False, False)
MainWindow(window)
window.mainloop()
