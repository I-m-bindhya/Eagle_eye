# module
from calendar import c
from fileinput import filename
import socket
from timeit import Timer
from tkinter import *
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import numpy as np
import mysql.connector
from datetime import date
import sys
import eagle
import select_roi



def main():
    # create window
    root = Tk()
    #root.geometry('1280x720')
    #root.attributes("-fullscreen", True)
    root.state("zoomed")
    root.title("Eagle Eye")
    # root.iconbitmap("eagle.ico")

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    label =Label(root)
    label.place(x=600,y=100)

    def changeCam(event=0, nextCam=-1):
        global camIndex, cap, fileName

        if nextCam == -1:
            camIndex += 1
        else:
            camIndex = nextCam
        
        cap = cv2.VideoCapture(camIndex)

        #try to get a frame, if it returns nothing
        success, frame = cap.read()
        if not success:
            camIndex = 0
            del(cap)
            cap = cv2.VideoCapture(camIndex)

        f = open(fileName, 'w')
        f.write(str(camIndex))
        f.close()

    try:
        f = open(filename, 'r')
        camIndex = int(f.readline())
    except:
        camIndex = 0

    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(camIndex)

    success, frame = cap.read()
    if not success:
        if camIndex == 0:
            print("Error, No webcam found!")

            
        else:
            changeCam(nextCam=0)
            success, frame = cap.read()
            if not success:
                print("Error, No webcam found!")
                sys.exit(1)
    changeCamera = StringVar(root)
    my_list = ["CAM 0", "CAM1"]
    changeCamera.set(my_list[0])
    OptionMenu(root, changeCamera, *my_list, command=changeCam).place(x=20,y=500)
    # Define camera brightness

    def changebrightness(val=255):
        #print("br",val)
        cap.set(10,int(val))
        
        # show_frames()
    # Define cmaera contrast 
    def changecontrast(val=128):
        #print("con",val)
        cap.set(11,int(val))
        
        # show_frames()

    # define camera  saturation 
    def changesaturation(val=128):
        #print("sat",val)
        cap.set(12,int(val))
    
    def changefocus(val=0):
        #print("foc",val)
        cap.set(28,int(val))

    def cameraResolution(choice):
        #print("choice",choice)
        cr = choice.split('x')
        #print(cr)
        cap.set(3,int(cr[0]))
        cap.set(4,int(cr[1]))
        return str(cap.get()),str(cap.get())

    def changewidth(val=640):
        #print("vallllll",val)
        cap.set(3,int(val))

    def changeheight(val=400):
        #print("vallllll",val)
        cap.set(4,int(val))
        camera_resolution = str(cameraRes.get())
        #print("camera_resolution",camera_resolution)


    def saveSettings():
        camera_resolution = str(cameraRes.get())
        #print("camera_resolution",camera_resolution)


        brightness = brightnessScale.get()
        #print("brightnessssss",brightness)
        # recipe = SNtext.get()
        #print("recipe",recipe)
        recipe_alt_name = snAltNo.get()
        #print("recipe_alt_name",recipe_alt_name)
        brightness = brightnessScale.get()    
        #print("brightnessssss",brightness)
        contrast= contrast_scale.get()
        #print("contrasttttt",contrast)
        saturation= saturation_scale.get()
        #print("saturationnnnn",saturation)
        focus= focus_scale.get()
        #print("focusssss",focus)
        window_width = windowWidth.get()
        #print("window_widthhh",window_width)
        window_height = windowHeight.get()
        #print("window_heighttt",window_height)
        save_selection =CheckVar1.get()
        #print("save_selection",save_selection)

        # cameraRes = str(var.get())
        # print("cameraResss",cameraRes)
        today = date.today()
        recipedate = today.strftime("%Y-%m-%d")
        #print("d1 =", recipedate)

        #print("recipe,recipe_alt_name,brightness,contrast,saturation,focus,window_width,window_height,camera_resolution,recipedate", recipe,recipe_alt_name,brightness,contrast,saturation,focus,window_width,window_height,camera_resolution,recipedate)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eagle_eye"
        )
        mycursor = mydb.cursor()
        query = "Insert into recipes(recipe_alt_name,brightness,contrast,saturation,focus,window_width,window_height,camera_resolution,save_selection,recipe_date,station_name,ip_address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (recipe_alt_name,brightness,contrast,saturation,focus,window_width,window_height,camera_resolution,save_selection,recipedate,hostname,ip_address)
        mycursor.execute(query, val)
        cv2.imwrite( str(mycursor.lastrowid)+".png", cap.read()[1])
        # recipe_results = mycursor.fetchall()
        # print("recipe_resultssss",mycursor.lastrowid)
        mydb.commit()
        callRoi()

        # saveRoi(mycursor.lastrowid)

    # def saveRoi(receipe_id):
    #     for data in selected_roi:
    #         mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="eagle_eye")
    #         mycursor=mysqldb.cursor()


    #         try:
    #             sql = "INSERT INTO  roi (roi_name, type, receipe_id, start_x,start_y,end_x,end_y) VALUES (%s, %s, %s, %s, %s, %s, %s )"
    #             val = (data['roi_name'], data['roi_type'], receipe_id, data['start_x'], data['start_y'], data['end_x'], data['end_y'])
    #             mycursor.execute(sql, val)
    #             mysqldb.commit()
    #             messagebox.showinfo("information", "inserted successfully...")
    #         except Exception as e:
    #             print(e)
    #             mysqldb.rollback()
    #             mysqldb.close()

    # camera resolution
    Label(root,text="CAMERA RESOLUTION: ").place(x=20,y=38)
    cameraRes = StringVar(root)
    my_list = ["1280 x 720","1920 x 1080"]
    cameraRes.set(my_list[0])
    OptionMenu(root, cameraRes, *my_list, command=cameraResolution).place(x=155,y=32)

    # sn alt name
    Label(root, text="RECIPE NAME:").place(x=20,y=80)
    snAltNo = Entry(root)
    snAltNo.place(x=155,y=80)

    # windowWidth
    Label(root, text="WINDOW WIDTH:").place(x=20,y=120)

    windowWidth=Entry(root)
    windowWidth.insert(END, 'default text')

    windowWidth.place(x=157, y=120, w=83, h=25)
    windowWidth.focus_set()
    windowWidth.delete(0, END)
    #print("windowWidth",windowWidth)

    # windowHeight
    Label(root, text="WINDOW HEIGHT:").place(x=300,y=120)
    windowHeight=Entry(root)
    windowHeight.insert(0,"720")
    windowHeight.place(x=438, y=120, w=83, h=25)
    windowHeight.focus_set()
    windowHeight.delete(0, END)
    #print("windowHeight",windowHeight)

    # brightness scale
    Label(root,text="BRIGHTNESS").place(x=20,y=160)
    brightnessScale = Scale(
        master = root,
        from_ = 0,
        to=255,
        length=500,
        tickinterval=25,
        orient=HORIZONTAL,
        command = changebrightness  
        
    )
    brightnessScale.place(x=20,y=175)
    brightnessScale.set(128)
    # contrast
    Label(root,text="CONTRAST").place(x=20,y=240)
    contrast_scale = Scale(
        master = root,
        from_ = 0,
        to=255,
        length=500,
        tickinterval=25,
        orient=HORIZONTAL,
        command = changecontrast
    )
    contrast_scale.place(x=20,y=255)
    contrast_scale.set(128)
    # saturationScale
    Label(root,text="SATURATION").place(x=20,y=320)
    saturation_scale = Scale(
        master = root,
        from_ = 0,
        to=255,
        length=500,
        tickinterval=25,
        orient=HORIZONTAL,
        command = changesaturation
    )
    saturation_scale.place(x=20,y=335)
    saturation_scale.set(128)
    # focusScale 
    Label(root,text="FOCUS").place(x=20,y=400)
    focus_scale = Scale(
        master = root,
        from_ = 0,
        to=100,
        length=500,
        tickinterval=10,
        orient=HORIZONTAL,
        command = changefocus
    )
    focus_scale.place(x=20,y=415)
    focus_scale.set(0)

    # variable with integer values only
    var = IntVar()

    # label widget to display selected number
    Label(
        root,
        textvariable=var,
        font=('Times New Roman', 16)
    ).pack(side=BOTTOM)

    # sn print value
    # Label(root, text="RESULT:").place(x=150,y=505)
    # SNtext=Entry(root)
    # SNtext.place(x=230,y=505)
    # SNtext.focus_set()
    # SNtext.delete(0, END)
    #print("SNtexttt",SNtext)

    # # Selected roi
    # Label(root,text="SELECTED ROI").place(x=20,y=540)
    # selected_roi = []


    # def show_roi():
    #     x,y=20, 570
    #     with open("data.json") as file:
    #         data = json.load(file)
    #         selected_roi.append(data)

    #     for data in selected_roi:
    #         Label(root, text="ROI name:").place(x=x,y=y)
    #         Label(root, textvariable=StringVar(value=data['roi_name']), font=('Times New Roman', 12)).place(x=x+80,y=y)

    #         Label(root, text="ROI name:").place(x=x+210,y=y)
    #         Label(root, textvariable=StringVar(value=data['roi_type']), font=('Times New Roman', 12)).place(x=x+300,y=y)

    #         y+=20

    # Button(root, text="REFRESH", command=show_roi).place(x=150, y=540)



    # save checkbox
    CheckVar1 = IntVar()
    saveselection = Checkbutton(root, text = "SAVE", variable = CheckVar1, \
                    onvalue = 1, offvalue = 0 \
                    ).place(x=400, y=505)

    # button reset to default 
    def refreshscale():
        cameraRes.set(["320x240"])
        brightnessScale.set(128)
        contrast_scale.set(128)
        saturation_scale.set(128)
        focus_scale.set(0)
        # SNtext.delete(0, END)
        snAltNo.delete(0, END)

    resetScale= Button(root, text="RESET TO DEFAULT SETTINGS", command=refreshscale).place(x=355, y=35)

    def callRoi():
        cap.release()
        root.destroy()
        select_roi.main()


    # button to save camera settings
    # saveButton= Button(root, text="SELECT ROI", command=callRoi).place(x=240, y=700)
    saveButton= Button(root, text="SAVE SETTINGS", command=saveSettings).place(x=440, y=700)
    def back():
        root.destroy()
        cap.release()
        eagle.main()
        
    backToHome = Button(root, text="BACK TO HOME ", command=back).place(x=20, y=700) 


    def show_frames():
        #print("sdfasdfasfasdfasdfasdfasd", cap.read())
        # Get the latest frame and convert into Image
        cv2image = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        # print("imggggggggggg",img)
        for code in decode(img):        
            decoded_data = code.data.decode('utf-8')
            #print("data", code.data)
            # SNtext.insert(0, code.data)
            # Timer(3.0, show_frames).start()
            # e.insert(0, code.data)
            rect_pts = code.rect
            
            # if decoded_data:            
            #     pts = np.array([code.polygon], np.int32)            
            #     cv2.polylines(img,[pts], True,(0,50,255),2)
            #     cv2.putText(img, str(decoded_data), (rect_pts[0],rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0),3)
                
        # # Convert image to PhotoImage
        
        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        # # Repeat after an interval to capture continiously
        label.after(20, show_frames)

    show_frames()

    # infinite loop
    root.mainloop()

if __name__ == "__main__":
    main()
