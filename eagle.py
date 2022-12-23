# module
from tkinter import *
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import mysql.connector
from threading import Timer
import socket
from time import strftime
from tkinter.font import Font
import OCR
import pytesseract
import numpy as np
import exe
import crud

def main():
    # function

    root=Tk()
    #root.geometry("1280x720")
    root.state("zoomed")
    root.title("Eagle Eye")
    # root.iconbitma'p(r"eagle.ico")

    COMPUTER_DETAILS = Frame(root, bd=2, relief=GROOVE)
    COMPUTER_DETAILS.place(x=10 , y=10, width=260, height=85)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    time_string = strftime(' %A %x')
    hostname = Label(root, text="Station Name:  " + hostname, font = "Calibri, 10 bold").place(x=20,y=20)
    ipaddress = Label(root, text="IP Address:  " + ip_address, font = "Calibri, 10 bold").place(x=20,y=40)
    dateDay = Label(root, text="Date:  " + time_string, font = "Calibri, 10 bold").place(x=20,y=60)


    Unit_count = Frame(root, bd=2, relief=GROOVE)
    Unit_count.place(x=1080, y=10, width=260, height=85)
    #Count Label and Textbox
    Label(root, text="Unit Tested: ", font = "Calibri, 10 bold").place(x=1085, y=20)
    countText = Entry(root)
    countText.configure(font=Font(size=12, weight="bold"))
    countText.place(x=1170, y=20,width=70,height=20)
    global captureCount
    captureCount = 0
    countText.insert(0,captureCount)


    unitpass = Label(text="Unit Pass: ", font = "Calibri, 10 bold").place(x=1085,y=40)
    unitpass = Entry(root,fg="green")
    unitpass.configure(font=Font(size=12, weight="bold"))
    unitpass.place(x=1170,y=40,width=70,height=20)
    unitpass.insert(0,0)


    unitfail = Label(text="Unit Fail: ", font = "Calibri, 10 bold").place(x=1085,y=60)
    unitfail = Entry(root,fg="red")
    unitfail.configure(font=Font(size=12, weight="bold"))
    unitfail.place(x=1170,y=60,width=70,height=20)
    unitfail.insert(0,0)




    #global snText
    # global snText
    # Label(root, text="SN").place(x=410, y=13)
    # snText = Entry(root)
    # snText.place(x=440, y=13,height=25)
    # snText.focus_set()
    # # snText.bind('<Return>', my_click)
    # snText.delete(0, END)

    #Select Models
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="eagle_eye")
    mycursor = mysqldb.cursor()
    sql= "SELECT * FROM recipes"
    mycursor.execute(sql)
    resRec = mycursor.fetchall()

    recipeid = 0
    recipeName = ''
        # choice = menu.get()
        # drop.config(bg=choice)

    my_list = []
    # c = 0
    for row in resRec:
        # my_list[c] = row[1]
        # if c == 0:
        #     recipeid = row[0]
        #     recipeName = row[2]
        my_list.append(row[2])
        # c = c+1
        
    def open():
        def login():
            mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="eagle_eye")
            mycursor = mysqldb.cursor()
            user = e3.get()
            password = e4.get()

            sql= "SELECT * from users where username=%s  and password=%s"
            mycursor.execute(sql,[(user),(password)])
            results = mycursor.fetchone()
            print("results", results)

            if results:
                cv2.destroyAllWindows()
                root.destroy()
                cap.release()            
                #cv2.destroyAllWindows()
                #messagebox.showinfo("","login successed")   
                if results[6]  == "Administrator"  :
                    crud.main() 
                else:  
                    exe.main()
                # root.destroy()
                return True
            else:
                messagebox.showinfo("","login error")
                return False
        global e3
        global e4
        
        top = Toplevel()
        top.geometry("400x300")
        top.title('LOGIN')
        top.config()
        Label(top, text="").pack(pady=10)
        Label(top,text="Username").place(x=80,y=50)
        Label(top,text="Password").place(x=80,y=90)
            
        e3 = Entry(top)
        e3.place(x=150, y=53)

        e4 =Entry(top)
        e4.place(x=150,y=93)
        e4.config(show="*")
        Button(top, text="LOGIN", command=login, height=1, width=5).place(x=150, y=150)       


    def recipeChangevent(choice):
        print("choice",choice)
        print('resRec',resRec)
        for row in resRec:
            if choice == row[2]:
                global recipeid, recipeName
                recipeid = row[0]
                recipeName = row[2]
                onResetValue()
                onReset()
                setCameraSettings(row)
                print('True')
            else:
                print('fase')

    def setCameraSettings(row):
        verifyCode = row[1]
        cap.set(10,row[3])
        cap.set(11,row[5])
        cap.set(12,row[6])
        # cap.set(28,row[8])

    def onResetValue():
        unitpass.delete(0,"end")
        unitpass.insert(0,0)
        unitfail.delete(0,"end")
        unitfail.insert(0,0)
        countText.delete(0,"end")
        countText.insert(0,0)

    loginButton = Button(root, text="LOGIN", height=1, width=7, command=open ).place(x=915, y=10)

    global label
    def update_text():
        # Configuring the text in Label widget
        label.configure(bg="#DDDDDD")
        #    label.configure(bg="red")


    # global e3
    # global e4
        
    # top = Toplevel()
    # top.geometry("400x300")
    # top.title('LOGIN')
    # top.config()
    # Label(top, text="").pack(pady=10)
    # Label(top,text="Username").place(x=80,y=50)
    # Label(top,text="Password").place(x=80,y=90)
            
    # e3 = Entry(top)
    # e3.place(x=150, y=53)

    # e4 =Entry(top)
    # e4.place(x=150,y=93)
    # e4.config(show="*")
    # Button(top, text="LOGIN", command=login, height=1, width=5).place(x=150, y=150)       
    # loginButton = Button(root, text="LOGIN", height=1, width=7, command=open ).place(x=915, y=10)

    # # Creating a photoimage object to use image
    # photo = PhotoImage(file = r"logo1.png") 

    # # Resizing image to fit on button
    # photoimage = photo.subsample(10, 10)
    # Button(root, image = photoimage,compound = LEFT).place(x=440,y=65)

    # def my_time():
    #     time_string = strftime(' %A %x') # time format 
    #     l1.config(text=time_string)
    #     l1.after(1000,my_time) # time delay of 1000 milliseconds 
        
    # my_font = "Calibri, 10 bold" # display size and style
    # datetime = Label(root,text="Date: ", font=my_font).place(x=20,y=60)
    # l1=Label(root,font=my_font)
    # l1.place(x=50,y=60)

    # camera frame border
    # Resultname=Label(root, text="PASS",fg="green",font=(20)).place(x=670, y=80)
    label =Label(root,bg="#DDDDDD",borderwidth = 40)
    label.grid(padx=320,pady=50)
    label.frame_num = 0
    cap = cv2.VideoCapture(0)

    capWidth = cap.get(640)
    capHeight = cap.get(480)
    ocrText = ''




    Label(root, text="SELECT MODEL").place(x=580, y=13)
    menu = StringVar(root)
    # menu.set(my_list[0])
    # recipeChangevent(my_list[0])
    drop = OptionMenu(root, menu, *my_list, command=recipeChangevent).place(x=670, y=10) 
    detect = 0

    def labelConfig(imgTemp):
        # Convert image to PhotoImage
        img = Image.fromarray(imgTemp)
        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.frame_num += 1
        label.configure(image=imgtk)

    def imgText(imgTemp, start: list[int, int], end: list[int, int], color, data, roi_name):
        imgTemp= cv2.rectangle(imgTemp, (start[0], start[1]), (end[0], end[1]), color , 2)
        cv2.putText(imgTemp, roi_name + ': ' + data, (start[0], start[1]-10), cv2.FONT_HERSHEY_DUPLEX, 0.6, color , 1)
        return imgTemp



    def show_frames():
        global imgTemp, detect, recipeid
        print("roi",recipeid)

        Resultname = Label(root, bg="#DDDDDD", text="                ", fg="green", font=('Helvatical bold',22), width=10, height=1).place(x=600, y=50)

        # Get the latest frame and convert into Image
        cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
        imgTemp = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="eagle_eye")
        mycursor = mysqldb.cursor()

        sql2= "SELECT * from roi where receipe_id=%s"
        mycursor.execute(sql2,[(recipeid)]) 
        roi_result = mycursor.fetchall()
        totalCount = 0
        passCount = 0
        for roi in roi_result:
            roi_name = roi[0]
            start_x = roi[1]
            start_y = roi[2]
            end_x = roi[3]
            end_y = roi[4]
            type = roi[7]
            data = roi[8]

            imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (0,0,255), " ", roi_name)
            # cv2.imwrite('temp.png',cv2image[roi[2]:roi[2]+roi[4],roi[1]:roi[1]+roi[3]])

            if detect:
                totalCount+=1
                if type == 'Logo':
                    # original = cv2image[start_y : start_y+end_y, start_x : start_x+end_x]
                    # duplicate_image = cv2.imread(str(recipeid)+".png")
                    # duplicate  = duplicate_image[start_y : start_y+end_y, start_x : start_x+end_x]
                    # difference = cv2.subtract(original, duplicate)
                    # b, g, r = cv2.split(difference)

                    # if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    #         imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (0,255,0), data, roi_name)
                    #         passCount+=1 
                    # else:
                    #     imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (255,0,0), " ", roi_name)

                    img_rgb = cv2image[start_y : end_y, start_x : end_x]
                    duplicate = cv2.imread(str(recipeid)+".png")
                    template = duplicate[start_y : end_y, start_x : end_x]

                    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                    print("res", res)
                    threshold = .6
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):  # Switch collumns and rows
                            imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (0,255,0), data, roi_name)
                            passCount+=1 
                    if len(loc[0]) == 0:
                        imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (255,0,0), " ", roi_name)
                elif type == 'OCR': 
                    OCR.tesseract_location('C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
                    imgTemp, text = ocr_stream(crop=[start_x, start_y], img_hi= end_y - start_y , img_wi = end_x - start_x)
                    # print("ocr text ", text) 
                    if text:
                        sql2= "SELECT * from roi where receipe_id=%s and data=%s"
                        mycursor.execute(sql2,[(recipeid), (text)])
                        results = mycursor.fetchall()

                        if results:
                            imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (0,255,0), data, roi_name)
                            passCount+=1 
                        else:
                            imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (255,0,0), " ", roi_name)
                    else:
                        imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (255,0,0), " ", roi_name)

                else:
                    imCrop = Image.fromarray(cv2image[start_y : start_y+end_y, start_x : start_x+end_x])
                    for code in decode(imCrop):        
                        decoded_data = code.data.decode('utf-8')
                        print("data", decoded_data)
                        print("receipe_id", recipeid)
                        
                        sql1= "SELECT * from roi where receipe_id=%s and data=%s"
                        mycursor.execute(sql1,[(recipeid), (decoded_data)])
                        recipe_results = mycursor.fetchall()

                        print("query", recipe_results) 

                        if recipe_results:
                            imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (0,255,0), data, roi_name)
                            passCount+=1
                        else:
                            imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (255,0,0), " ", roi_name)



                        # Timer(3.0, show_frames).start()
                        # time = datetime.today()
                        # capturedatetime = time.strftime('%Y-%m-%d %H:%M:%S')
                        # print("capturedatetimeeee",capturedatetime)
                    
                        # insert ="insert into capture(recipe_id,status,datetime) value(%s,%s,%s)"
                        # valuee = (recipeid,status,capturedatetime)
                        # mycursor.execute(insert,valuee)
                        # mysqldb.commit()           
                    if not decode(imCrop):                    
                        imgTemp = imgText(imgTemp, [start_x, start_y], [end_x, end_y], (255,0,0), " ", roi_name)


        labelConfig(imgTemp)
            
        if not detect: 
            label.after(100, show_frames)
            return label.configure(bg="#DDDDDD")

        elif roi_result and len(roi_result) == totalCount:
            cntp = countText.get()        
            captureCount = int(cntp)
            countText.delete(0,"end")
            countText.insert(0, captureCount+1)
            if totalCount == passCount:
                Resultname = Label(root, bg="#77dd77", text="   PASS   ",fg="white",font=('Helvatical bold',22), width=10, height=1).place(x=600, y=50)
                cntp = unitpass.get()
                capturepass=int(cntp)+1
                unitpass.delete(0,"end")
                unitpass.insert(0,capturepass )
                return label.configure(bg="#77dd77")

            else:
                Resultname = Label(root, bg="#EC2424", text="   FAIL   ",fg="white",font=('Helvatical bold',22), width=10, height=1).place(x=600, y=50)
                cntp = unitfail.get()
                capturefail=int(cntp)+1
                unitfail.delete(0,"end")
                unitfail.insert(0,capturefail)
                return label.configure(bg="#EC2424")


    def show_initial_frames():
        global imgTemp

        Resultname = Label(root, bg="#DDDDDD", text="                ", fg="green", font=('Helvatical bold',22), width=10, height=1).place(x=600, y=50)

        # Get the latest frame and convert into Image
        cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
        imgTemp = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)

        labelConfig(imgTemp)
        # Repeat 
        if not recipeid: 
            print("init", recipeid)
            label.after(100, show_initial_frames)
        return label.configure(bg="#DDDDDD")



    def key_pressed(event):
        take_pic()

    def take_pic():
        #file_name = f"{label.datetime.now()}.png"
        file_name = "images/"+"tesss.png"
        print(file_name)
        imagetk = label.imgtk
        print(imagetk)
        imgpil = ImageTk.getimage( imagetk )
        print(imgpil)
        # imgpil = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        imgpil.save(file_name,"PNG")
        imgpil.close()


    def ocr_stream(crop: list[int, int], source: int = 0, view_mode: int = 1, language=None, img_wi: int = 0, img_hi: int = 0):

        # Main display loop
        # print("\nPUSH c TO CAPTURE AN IMAGE. PUSH q TO VIEW VIDEO STREAM\n")

        frame = imgTemp # Grabs the most recent frame read by the VideoStream class

        frame1 = frame[crop[1]: crop[1]+img_hi, crop[0]: crop[0]+img_wi]

        boxes = pytesseract.image_to_data(frame1)

        ocrText = ''
        if boxes is not None:  # Defends against empty data from tesseract image_to_data
            for i, box in enumerate(boxes.splitlines()):  # Next three lines turn data into a list
                box = box.split()
                if i != 0:
                    if len(box) == 12:
                        x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                        conf = box[10]
                        word = box[11]
                        x += crop[0]  # If tesseract was performed on a cropped image we need to 'convert' to full frame
                        y += crop[1]
                        conf_thresh, color = OCR.views(view_mode, int(float(conf)))

                        if int(float(conf)) > conf_thresh:
                            cv2.rectangle(frame, (x, y), (w + x, h + y), color, thickness=1)
                            ocrText = ocrText + ' ' + word

            # if ocrText.isascii():  # CV2 is only able to display ascii chars at the moment
            #     cv2.putText(frame, ocrText, (5, img_hi - 5), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0))
        return frame, ocrText

    def detectChange():
        global detect
        detect = 1

    def onReset():
        global detect
        detect = 0
        show_frames()
        Timer(3.0, detectChange).start()



    resetCamera = Button(root, text="RESET", height=1, width=10, command=onReset).place(x=580, y=630)
    captureButton = Button(root, text="CAPTURE", height=1, width=10, command=take_pic).place(x=690, y=630)
    #my_time()
    show_initial_frames()
    mainloop()



if __name__ == "__main__":
    main()