import numpy as np
from PIL import Image as Iimage
import os
from tkinter import *
import keyboard as kb
import time as t

def sigmoid(x): return 1 / (1 + np.exp(-x))

def pretty_bytes(fpath, delim=''):
    arr = []

    ff = ''
    img = Iimage.open(fpath)

    w, h = img.size

    obj = img.load()

    for k in range(w):
        for i in range(h):
            if obj[k, i][0] == 0:
                arr.append(0)
            else: arr.append(1)

    return arr

def new_data(num = 0):
    return pretty_bytes("all/o_{}.png".format(num))

arr = []
out_arr = []

arr2 = os.listdir("C:\\Users\\Igrok\\Desktop\\New\\all")
for k in range(101, 200):
    if ("o_" + str(k) + ".png") not in arr2:
        break
    else: arr.append(new_data(k)); out_arr.append(1)

for k in range(201, 300):
    if ("o_" + str(k) + ".png") not in arr2:
        break
    else: arr.append(new_data(k)); out_arr.append(0)

train_inp = np.array( arr )

train_outputs = np.array([out_arr]).T

synaptic_weight = 2 * np.random.random((len(new_data(101)), 1)) - 1

np.set_printoptions(formatter={'float': '{: 0.10f}'.format})


def load_weights():
    with open("all/h.txt", "r") as f:
        text = f.read()
    text = text.replace("[", "")
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    arr = text.split("]")
    while "" in arr: arr.remove("")
    arr = np.array(arr)
    arr = arr.astype("float")
    arr = np.array(arr)

    print("\nYour weights succesfully loaded\n")
    t.sleep(0.3)

    return arr

import time
import os
def getdot(val):
    a=["",".","..","..."]
    return a[val]

epohs = 1000000

if (input("Wonna u to load your weights? (y/n) - ").lower() != "y"):
    os.system("cls")
    print("\tERROR\t\t\tPROGRESS")
    for i in range(epohs):
        input_layer = train_inp
        outputs = sigmoid( np.dot(input_layer, synaptic_weight) )

        err = train_outputs - outputs
        adj = np.dot( input_layer.T, err * (outputs * (1 - outputs)) )

        synaptic_weight += adj * 0.6

        if (i % 5000 == 0 or i == 10):
            line = "|" + "=" * (int(i / epohs * 100) // 5) + " " * (19 - (int(i / epohs * 100) // 5)) + "|"

            sys.stdout.write("\r" + str((np.sum(err) / len(err)).round(50) ) + "\t" + line + "\t" + str(int(i / epohs * 101)) + "% / " + str(i) +  "e")
            if kb.is_pressed('enter'): break
else: synaptic_weight = load_weights()

inp = np.array([pretty_bytes("all/o_502.png"), pretty_bytes("all/o_501.png")])
outputs = sigmoid( np.dot( inp, synaptic_weight))


print("\n\n\t----")
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

out = []

if "[" in str(outputs[0]):
    for k in range(outputs.size): out.append(outputs[k][0])
else: out = outputs
print("\t{}\n\t{}".format(out[0].round(3), out[1].round(3)))
print("\t----\n\n")

class Paint(Frame):
    def __init__(self, parent, Image):
        Frame.__init__(self, parent)

        self.parent = parent

        self.setUI()

        self.brush_size =  40
        self.brush_color = "black"

        self.canv.bind("<B1-Motion>", self.draw)
        self.canv.bind("<Button-3>", self.get_res)
        self.canv.bind("<MouseWheel>", self.add_examples_2)
        self.canv.bind("<Button-2>", self.save_weights)
        self.canv.bind_all("<KeyPress>", self.get_shit)

    def get_shit(self, event):
        key = event.char

        arr = os.listdir("C:/Users/Igrok/Desktop/new/all")
        for k in range(1, 200):
            if ("o_{}_{}.png".format(key, k)) not in arr:
                print("\nimage saved by the number {}_{}".format(key, k))
                break
        self.save_photo("{}_{}".format(key, k))


    def add_examples_2(self, event):
        if event.delta == 120:
            if self.canv.find_all():
                arr = os.listdir("C:/Users/Igrok/Desktop/new/all")
                for k in range(101, 200):
                    if ("o_" + str(k) + ".png") not in arr:
                        print("\nimage saved byu the number {}".format(k))
                        break
                self.save_photo(k)



        if event.delta == -120:

            if self.canv.find_all():
                arr = os.listdir("C:/Users/Igrok/Desktop/new/all")
                for k in range(201, 300):
                    if ("o_" + str(k) + ".png") not in arr:
                        print("\nimage saved by the number {}".format(k))
                        break
                self.save_photo(k)


    def save_weights(self, event):
        np.set_printoptions(formatter={'float': '{: 0.100f}'.format})
        with open("all/h.txt", "w") as f:
            f.write(str(synaptic_weight))
        print("\nYour weights succesfully saved\n")
        np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

    def save_photo(self, val):
        self.canv.postscript(file="img.eps", colormode='color')
        filename = "img"

        img = Iimage.open(filename + ".eps")

        i2 = Iimage.open("all/o_501.png")

        resized_image = img.resize(i2.size)

        resized_image.save("all/o_" + str(val) + ".png")

        self.canv.delete("all")

        img.close()

        os.remove(filename + ".eps")

    def get_res(self, event):
        self.canv.postscript(file="all/imgg.eps", colormode='color')
        filename = "all/imgg"

        img = Iimage.open(filename + ".eps")

        i2 = Iimage.open("all/o_501.png")

        resized_image = img.resize(i2.size)

        resized_image.save(filename + ".png")

        self.canv.delete("all")

        inp = np.array([pretty_bytes(filename + ".png")])
        outputs = sigmoid( np.dot( inp, synaptic_weight))

        if "[" in str(outputs[0]):
            out = str(outputs[0])
        else: out = str(outputs)

        sys.stdout.write("\rRESULT:\t{} ".format(out))

        img.close()

        os.remove(filename + ".eps")
        os.remove(filename + ".png")

    def setUI(self):

        self.parent.title("Pythonicway PyPaint")  # Устанавливаем название окна
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        self.columnconfigure(6, weight=1) # Даем седьмому столбцу возможность растягиваться, благодаря чему кнопки не будут разъезжаться при ресайзе
        self.rowconfigure(2, weight=1) # То же самое для третьего ряда

        self.canv = Canvas(self, bg="white")  # Создаем поле для рисования, устанавливаем белый фон
        self.canv.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E+W+S+N)

    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                          event.y - self.brush_size,
                          event.x + self.brush_size,
                          event.y + self.brush_size,
                          fill=self.brush_color, outline=self.brush_color)


def main():
    root = Tk()
    root.geometry("500x500")
    app = Paint(root, Image)
    root.mainloop()

if __name__ == "__main__":
    main()
