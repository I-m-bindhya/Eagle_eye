import tkinter as tk
from tkinter import Button, mainloop, ttk
from tkinter import messagebox
import pymysql
import cv2
import mysql.connector
import xlwt

def main(window):

    #ProjectGurukul- Initializing window frame
    # window = tk.Tk()
    # # window.geometry("1350x700")
    # window.title("eagle eye")

    # database
    con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
    cur = con.cursor()
    
    Label_Heading = tk.Label(window, text="COMMON REPORT", font=(22))
    Label_Heading.pack(side=tk.TOP, fill=tk.X)

    # Frame_Details = tk.LabelFrame(window, text="RECIPE DETAILS", font=(12), bd=2, relief=tk.GROOVE)
    # Frame_Details.place(x=20, y=40, width=400, height=575)
    
    Frame_Data = tk.LabelFrame(window, text="", font=(12), bd=2, relief=tk.GROOVE)
    Frame_Data.pack(side=tk.TOP, fill=tk.X)

    recipename = tk.StringVar()
    # lastname = tk.StringVar()
    # username = tk.StringVar()
    # password = tk.StringVar()
    search_box = tk.StringVar()
    searchEntry = tk.StringVar()
    status = tk.StringVar(value="0")
    id = tk.IntVar()

    
    # Label_recipename = tk.Label(Frame_Details, text="RECIPE NAME: ")
    # Label_recipename.place(x=30, y=50)
    # Entry_recipename = tk.Entry(Frame_Details, bd=2, textvariable=recipename)
    # Entry_recipename.place(x=130, y=50, height=28, width=220)

    # Label_lastname = tk.Label(Frame_Details, text="LASTNAME: ")
    # Label_lastname.place(x=30,y=100)
    # Entry_lastname = tk.Entry(Frame_Details, bd=2, textvariable=lastname)
    # Entry_lastname.place(x=130, y=100, height=28, width=220)
    
    # Label_username = tk.Label(Frame_Details, text="USERNAME: ")
    # Label_username.place(x=30, y=150)
    # Entry_username = tk.Entry(Frame_Details, bd=2, textvariable=username)
    # Entry_username.place(x=130, y=150, height=28, width=220)
    
    # Label_password = tk.Label(Frame_Details, text="PASSWORD: ")
    # Label_password.place(x=30, y=200)
    # Entry_password = tk.Entry(Frame_Details, bd=2, textvariable=password)
    # Entry_password.place(x=130, y=200, height=28, width=220)
    # Entry_password.config(show="*")
    
    # Label_active = tk.Label(Frame_Details, text="STATUS:")
    # Label_active.place(x=30,y=100)
    # saveselection = tk.Checkbutton(Frame_Details, variable = status, onvalue = "1", offvalue = "0", width=0, height=1)
    # saveselection.place(x=130, y=100)


    def EXPORT_TO_EXCEL():

        # database
        con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
        curr = con.cursor()    

        # cur.execute('SELECT r.id, r.recipe_alt_name, r.save_selection, u.username, r.ip_address, r.station_name, r.recipe_date FROM recipes as r LEFT JOIN Users as u ON r.user_id=u.id')
        curr.execute('SELECT * FROM recipes')
        rows=curr.fetchall()
        print("rows", rows)

        workbook = xlwt.Workbook()
        #Naming the sheet in the excel
        sheet = workbook.add_sheet("Common Report")

        sheet.write(0, 0, 'Receipe name')
        sheet.write(0, 1, 'ROI Name')    
        sheet.write(0, 2, 'Test Result')
        sheet.write(0, 3, 'Tested On')
        sheet.write(0, 4, 'Tested Machine')

        if len(rows)!=0:
            # Recipes_table.delete(*Recipes_table.get_children())        
            for count, row in enumerate(rows):
                #suser = list(row)
                
                receipeName = row[1]
                roiName = row[2]
                testResult = row[3]
                testedOn = row[4]
                testedMachine = row[5]
                print("xxxxxxx", count+1)
                # if suser[2] == 1:
                #     suser[2] = "Yes"
                # else:
                #     suser[2] = "No"

                sheet.write(count+1, 1, receipeName)
                sheet.write(count+1, 2, roiName)            
                sheet.write(count+1, 3, testResult)
                sheet.write(count+1, 4, testedOn)
                sheet.write(count+1, 5, testedMachine)
                
                # row = tuple(suser)
                #Recipes_table.insert('',tk.END,values=row)            

            print("workbook", workbook)    

            #saving the data to excel
            workbook.save("CommonReport.xls")
            con.commit()
            con.close()  


    def VIEW():
        cursor=Recipes_table.focus()
        if cursor:
            print("cursor", cursor)
            content=Recipes_table.item(cursor)
            print("content", content)
            row=content['values']
            print("row", row)
            id.set(row[0])
            recipename.set(row[1])
            print("row[1]", row[1])
            # lastname.set(row[2])
            # username.set(row[3])
            # password.set(row[4])
            if row[2] == "Yes":
                status.set("1")
            else:
                status.set("0")
            SHOW_ROI()

        else:
            messagebox.showerror('Error','Select data row to edit')

    def GET_DATA():
        cur.execute('SELECT r.id, r.recipe_alt_name, r.save_selection, u.username, r.ip_address, r.station_name, r.recipe_date FROM  recipes as r LEFT JOIN Users as u ON r.user_id=u.id')
        rows=cur.fetchall()
            
        if len(rows)!=0:
            Recipes_table.delete(*Recipes_table.get_children())
            for row in rows:
                suser = list(row)
                print("row", row)
                if suser[2] == 1:
                    suser[2] = "Yes"
                else:
                    suser[2] = "No"

                row = tuple(suser)
                Recipes_table.insert('',tk.END,values=row)
            con.commit()
            con.close()        

    def GET_DATA_SEARCH():
        print("search_box.get().lower()", search_box.get().lower())
        print("search_box.get().lower()", searchEntry.get())
        searchField = tk.StringVar()
        searchField = search_box.get().lower()
        searchValue = tk.StringVar()
        searchValue = searchEntry.get()    
        cur.execute("SELECT r.id, r.recipe, r.save_selection, u.username, r.ip_address, r.station_name, r.recipe_date FROM recipes as r LEFT JOIN Users as u ON r.user_id=u.id where r.recipe='" + searchValue + "'")

        print("cur", cur)
        rows=cur.fetchall()
        
        print(rows)
        if len(rows)!=0:
            Recipes_table.delete(*Recipes_table.get_children())
            for row in rows:
                suser = list(row)
                print("row", row)
                if suser[2] == 1:
                    suser[2] = "Yes"
                else:
                    suser[2] = "No"

                row = tuple(suser)
                Recipes_table.insert('',tk.END,values=row)
            con.commit()
            con.close()
        else:
            Recipes_table.delete(*Recipes_table.get_children())

    # def ADD_DATA():
    #     if firstname.get() == "" or lastname.get() == "" or username.get() == "" or password.get() == "":
    #         messagebox.showerror('Error','All Fields required')
    #     else:
    #         con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
    #         cur = con.cursor()
    #         query ="insert into users (firstname, lastname, username, password, status) values(%s,%s,%s,%s,%s)"
    #         val =(firstname.get(), lastname.get(), username.get(), password.get(), status.get())
    #         cur.execute(query,val)
    #         con.commit()
    #         con.close()
    #         GET_DATA()
    #         CLEAR()
    #         messagebox.showinfo('Success',"User has been created successfully")

    def UPDATE_DATA():
        print("id.get()", id.get())
        cur.execute("Update recipes SET recipe=%s, save_selection=%s where id=%s", (recipename.get(), status.get(), id.get()))
        print("cur", cur)
        con.commit()
        GET_DATA()
        con.close()
        CLEAR()
        messagebox.showinfo('Success',"Recipe has been updated successfully")

    def CLEAR():
        recipename.set("")
        # lastname.set("")
        # username.set("")
        # password.set("")
        status.set("0")
        id.set("")
        search_box.set("RECIPE NAME")
        searchEntry.set("")

    def DELETE():
        cur.execute("delete from recipes where id=%s", id.get())
        con.commit()
        con.close()
        GET_DATA()
        CLEAR()
        messagebox.showinfo('Success','Recipe has been deleted successfully')    

    def FOCUS():
        cursor=Recipes_table.focus()
        if cursor:
            print("cursor", cursor)
            content=Recipes_table.item(cursor)
            print("content", content)
            row=content['values']
            print("row", row)
            id.set(row[0])
            recipename.set(row[1])
            print("row[1]", row[1])
            # lastname.set(row[2])
            # username.set(row[3])
            # password.set(row[4])
            if row[2] == "Yes":
                status.set("1")
            else:
                status.set("0")

        else:
            messagebox.showerror('Error','Select data row to edit')

    def SHOW_ROI():
        cv2.destroyAllWindows()
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="eagle_eye")
        mycursor = mysqldb.cursor()
        sql= "SELECT * from roi where receipe_id=%s"
        mycursor.execute(sql,[id.get()]) 
        roi_result = mycursor.fetchall()
        img = cv2.imread("reports/recipes/" + str(id.get())+'.png')
        for roi in roi_result:
            roi_name = roi[0]
            start_x = roi[1]
            start_y = roi[2]
            end_x = roi[3]
            end_y = roi[4]
            data = roi[8]

            img= cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (57,255,20) , 2)
            cv2.putText(img, roi_name + ': ' + data, (start_x, start_y-10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (57,255,20) , 1)
        cv2.imshow(recipename.get() , img)


    #buttons
    # Frame_Btn = tk.Frame(Frame_Details,  bd=2, relief=tk.GROOVE)
    # Frame_Btn.place(x=15, y=200, width=365, height=50)

    # Edit_Button = tk.Button(Frame_Btn, text="Edit", bd=2, font=(15), width=6, command=FOCUS)
    # Edit_Button.grid(row=0, column=4, padx=4, pady=5)

    # View_Button = tk.Button(Frame_Btn, text="View", bd=2, font=(15), width=6, command=VIEW)
    # View_Button.grid(row=0, column=0, padx=4, pady=1)
    
    # Delete_Button = tk.Button(Frame_Btn, text="Update", bd=2, font=(15), width=6, command=UPDATE_DATA)
    # Delete_Button.grid(row=0, column=1, padx=4, pady=1)

    # Update_Button = tk.Button(Frame_Btn,  text="Delete", bd=2, font=(15), width=6, command=DELETE)
    # Update_Button.grid(row=0, column=2, padx=4, pady=1)
    
    # Clear_Button = tk.Button(Frame_Btn, text="Clear", bd=2, font=(15), width=6, command=CLEAR)
    # Clear_Button.grid(row=0, column=3, padx=4, pady=1)


    # Search Frame
    Frame_Search = tk.Frame(Frame_Data , bd=2, relief=tk.GROOVE)
    Frame_Search.pack(side=tk.TOP, fill=tk.X)
    
    Label_Search = tk.Label(Frame_Search, text="SEARCH BY",  font=(16))
    Label_Search.grid(row=0, column=0, padx=12, pady=2)
    
    Search_Box = ttk.Combobox(Frame_Search, font=(6), state="readonly", textvariable=search_box)
    Search_Box['values'] = ("RECIPE NAME","AUTO SAVE", "USERNAME", "IP ADDRESS", "STATION NAME", "CREATED DATE")
    Search_Box.current(0)
    Search_Box.grid(row=0, column=1, padx=12, pady=2)

    Entry_Search = tk.Entry(Frame_Search, bd=2, font=(12), width=20, textvariable=searchEntry)
    Entry_Search.grid(row=0, column=2, padx=12, pady=2)

    Search_Button = tk.Button(Frame_Search, text="SEARCH", bd=2, font=(15), width=10, command=GET_DATA_SEARCH)
    Search_Button.grid(row=0, column=3, padx=4, pady=1)
    
    Show_Button = tk.Button(Frame_Search, text="SHOW ALL", bd=2, font=(15), width=10, command=GET_DATA)
    Show_Button.grid(row=0, column=4, padx=4, pady=1)

    EXPORT_TO_EXCEL_Button = tk.Button(Frame_Search, text="EXPORT TO EXCEL", bd=2, font=(15), width=20, command=EXPORT_TO_EXCEL)
    EXPORT_TO_EXCEL_Button.grid(row=0, column=5, padx=4, pady=1)



    # Database Frame
    Frame_Database = tk.Frame(Frame_Data, bd=2, relief=tk.GROOVE)
    Frame_Database.pack(fill=tk.BOTH, expand=True)
    
    Scroll_X = tk.Scrollbar(Frame_Database, orient=tk.HORIZONTAL)
    Scroll_Y = tk.Scrollbar(Frame_Database, orient=tk.VERTICAL)
    
    Recipes_table = ttk.Treeview(Frame_Database, columns=("ID","RECIPE NAME","AUTO SAVE", "USERNAME", "IP ADDRESS", "STATION NAME", "CREATED DATE"), yscrollcommand= Scroll_Y.set,xscrollcommand= Scroll_X.set)
    
    Scroll_X.config(command=Recipes_table.xview)
    Scroll_X.pack(side=tk.BOTTOM, fill=tk.X)
    Scroll_Y.config(command=Recipes_table.yview)
    Scroll_Y.pack(side=tk.RIGHT, fill=tk.Y)

    Recipes_table.heading("ID", text="ID") 
    Recipes_table.heading("RECIPE NAME", text="RECIPE NAME")
    Recipes_table.heading("AUTO SAVE", text="AUTO SAVE")
    Recipes_table.heading("USERNAME", text="USERNAME")
    Recipes_table.heading("IP ADDRESS", text="IP ADDRESS")
    Recipes_table.heading("STATION NAME", text="STATION NAME")
    Recipes_table.heading("CREATED DATE", text="CREATED DATE")

    Recipes_table['show']='headings'
    Recipes_table.column("ID")
    Recipes_table.column("RECIPE NAME")
    Recipes_table.column("AUTO SAVE")
    Recipes_table.column("USERNAME")
    Recipes_table.column("IP ADDRESS")
    Recipes_table.column("STATION NAME")
    Recipes_table.column("CREATED DATE")

    
    Recipes_table.pack(fill=tk.BOTH, expand=True)

    GET_DATA()

    mainloop()

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Eagle Eye")

    main(root)