import os
import tkinter
import cv2
from threading import Thread
from tkinter import messagebox
from fileinput import filename
from tkinter import *
# module
from calendar import c
from fileinput import filename
from tkinter import *
import cv2
from pyzbar.pyzbar import decode
import mysql.connector
from PIL import Image, ImageTk
import OCR

root = Tk()
root.state("zoomed")
root.title("Eagle Eye")
# root.iconbitmap("eagle.ico")

mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="eagle_eye")
mycursor=mysqldb.cursor()
sqlReceipe = "SELECT * FROM recipes ORDER BY ID DESC LIMIT 1"
mycursor.execute(sqlReceipe)
lastRow = mycursor.fetchone()



# selected_roi_new = []

def display_roi(event):
    global tkimg

    # if image:
    #     tkimg = ImageTk.PhotoImage(image)
    #     print("tkimggg",tkimg)
    #     cropped_lbl.config(image=tkimg)


def __select_roi():
    global roi, img_crop, x1, x2, y1, y2, barcodeData
    # cap = cv2.VideoCapture(0)
    # ret, frame1 = cap.read()

    image = cv2.imread(str(lastRow[0]) + '.png')

    roi = cv2.selectROI("Select Rois",image, True)
    print("roi",roi)
    # for rect in roi:
    x1=roi[0]
    y1=roi[1]
    x2=roi[2]
    y2=roi[3]

    #crop roi from original image
    img_crop=image[y1:y1+y2,x1:x1+x2]

    cv2.imwrite("crop.jpg", img_crop)
    opencv_image=cv2.imread("crop.jpg")

    if e4.get() =='Logo':
        barcodeData = ""
        save()
        return

    elif e4.get() =='OCR':
        OCR.tesseract_location('C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
        barcodeData = OCR.ocr_stream(crop=[x1, y1], img_wi = x2, img_hi=y2)
        if barcodeData: 
            save()
        return

    color_converted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image=Image.fromarray(color_converted)
    for code in decode(pil_image):        
        barcodeData = code.data.decode('utf-8')
        print("data", code.data)
        save()

def details_popup():
    global e3
    global e4    
    global top 
    my_list = ['Barcode', 'QRcode', 'OCR', 'Logo']

    top = Toplevel()
    top.geometry("400x300")
    top.title('ROI Details')
    top.config()
    Label(top, text="").pack(pady=10)
    Label(top,text="ROI name").place(x=80,y=50)
    Label(top,text="ROI type").place(x=80,y=90)
    e4 = StringVar(top)
    e4.set(my_list[0])
    drop = OptionMenu(top, e4, *my_list).place(x=150,y=93) 
    e3 = Entry(top)
    e3.place(x=150, y=53)

    # e4 =Entry(top)
    # e4.place(x=150,y=93)
    Button(top, text="SAVE", command=lambda:(__select_roi()), height=1, width=5).place(x=150, y=150)

def save():
    if len(img_crop)>0:        
        try:
            sql = "INSERT INTO  roi (roi_name, type, receipe_id, start_x,start_y,end_x,end_y,data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )"
            val = (e3.get(), e4.get(), lastRow[0] ,int(x1),int(y1),int(x1+x2),int(y1+y2),barcodeData)
            mycursor.execute(sql, val)
            mysqldb.commit()
            top.destroy()
            cv2.destroyAllWindows()
            messagebox.showinfo("information", "inserted successfully...")
        except Exception as e:
            print(e)
            mysqldb.rollback()
            mysqldb.close()
    else:
        messagebox.showinfo("error", "invalid data... ")

def __start_thread():
    thread = Thread(target=details_popup, daemon=True)
    thread.start()

def gotoHome():
    root.destroy()
    os.system("python eagle.py")



# cropped_lbl = tk.Label(root)
# cropped_lbl.pack(expand=True, fill="both")

Button(root, text="Select ROI", command=__start_thread).place(x=600, y=53)
Button(root, text="Go to home", command=gotoHome).place(x=700, y=53)

# root.bind("<<ROISELECTED>>", display_roi)
root.mainloop()