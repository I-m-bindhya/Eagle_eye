import tkinter as tk
from tkinter import mainloop, ttk
from tkinter import messagebox
import pymysql
import eagle

def main():

    #ProjectGurukul- Initializing window frame
    window = tk.Tk()
    window.state("zoomed")
    #window.geometry("1350x700")
    window.title("eagle eye")
    
    Label_Heading = tk.Label(window, text="USER MANAGEMENT", font=(22))
    Label_Heading.pack(side=tk.TOP, fill=tk.X)
    
    Frame_Details = tk.LabelFrame(window, text="ENTER USER DETAILS", font=(12), bd=2, relief=tk.GROOVE)
    Frame_Details.place(x=20, y=40, width=400, height=575)
    
    Frame_Data = tk.LabelFrame(window, text="USER LIST", font=(12), bd=2, relief=tk.GROOVE)
    Frame_Data.place(x=440 , y=40, height=575)

    firstname = tk.StringVar()
    lastname = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()
    search_box = tk.StringVar()
    searchEntry = tk.StringVar()
    status = tk.StringVar(value="Active")
    id = tk.IntVar()

    
    Label_firstname = tk.Label(Frame_Details, text="FIRSTNAME: ")
    Label_firstname.place(x=30, y=50)
    Entry_firstname = tk.Entry(Frame_Details, bd=2, textvariable=firstname)
    Entry_firstname.place(x=130, y=50, height=28, width=220)

    Label_lastname = tk.Label(Frame_Details, text="LASTNAME: ")
    Label_lastname.place(x=30,y=100)
    Entry_lastname = tk.Entry(Frame_Details, bd=2, textvariable=lastname)
    Entry_lastname.place(x=130, y=100, height=28, width=220)
    
    Label_username = tk.Label(Frame_Details, text="USERNAME: ")
    Label_username.place(x=30, y=150)
    Entry_username = tk.Entry(Frame_Details, bd=2, textvariable=username)
    Entry_username.place(x=130, y=150, height=28, width=220)
    
    Label_password = tk.Label(Frame_Details, text="PASSWORD: ")
    Label_password.place(x=30, y=200)
    Entry_password = tk.Entry(Frame_Details, bd=2, textvariable=password)
    Entry_password.place(x=130, y=200, height=28, width=220)
    Entry_password.config(show="*")
    
    Label_active = tk.Label(Frame_Details, text="STATUS:")
    Label_active.place(x=30,y=250)
    saveselection = tk.Checkbutton(Frame_Details, variable = status, onvalue = "Active", offvalue = "Inactive", width=0, height=1)
    saveselection.place(x=130, y=250)

    def GET_DATA():
        con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
        cur=con.cursor()
        cur.execute('SELECT * FROM users where id<>10')
        rows=cur.fetchall()
            
        if len(rows)!=0:
            User_table.delete(*User_table.get_children())
            for row in rows:
                User_table.insert('',tk.END,values=row)
            con.commit()
            con.close()    

    def LOG_OUT():
        window.destroy()
        eagle.main()   

    def GET_DATA_SEARCH():
        con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
        cur=con.cursor()
        print("search_box.get().lower()", search_box.get().lower())
        print("search_box.get().lower()", searchEntry.get())
        searchField = tk.StringVar()
        searchField = search_box.get().lower()
        searchValue = tk.StringVar()
        searchValue = searchEntry.get()
        cur.execute("SELECT * FROM users where id<>10 AND " + searchField + "='" + searchValue + "'")

        print("cur", cur)
        rows=cur.fetchall()
        
        print(rows)
        if len(rows)!=0:
            User_table.delete(*User_table.get_children())
            for row in rows:
                User_table.insert('',tk.END,values=row)
            con.commit()
            con.close()
        else:
            User_table.delete(*User_table.get_children())

    def ADD_DATA():
        if firstname.get() == "" or lastname.get() == "" or username.get() == "" or password.get() == "":
            messagebox.showerror('Error','All Fields required')
        else:
            con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
            cur = con.cursor()
            query ="insert into users (firstname, lastname, username, password, status) values(%s,%s,%s,%s,%s)"
            val =(firstname.get(), lastname.get(), username.get(), password.get(), status.get())
            cur.execute(query,val)
            con.commit()
            con.close()
            GET_DATA()
            CLEAR()
            messagebox.showinfo('Success',"User has been created successfully")

    def UPDATE_DATA():
        print("id.get()", id.get())
        con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
        cur = con.cursor()
        cur.execute("Update users SET firstname=%s, lastname=%s, username=%s, password=%s, status=%s where id=%s", (firstname.get(), lastname.get(), username.get(), password.get(), status.get(), id.get()))
        print("cur", cur)
        con.commit()
        GET_DATA()
        con.close()
        CLEAR()
        messagebox.showinfo('Success',"User has been updated successfully")

    
    def CLEAR():
        firstname.set("")
        lastname.set("")
        username.set("")
        password.set("")
        status.set(value="Inactive")
        id.set("")
        search_box.set("FIRSTNAME")
        searchEntry.set("")

    def DELETE():
        con=pymysql.connect(host='localhost',user='root',password='',database='eagle_eye')
        cur=con.cursor()
        cur.execute("delete from users where id=%s", id.get())
        con.commit()
        con.close()
        GET_DATA()
        CLEAR()
        messagebox.showinfo('Success','User has been deleted successfully')    

    def FOCUS():
        cursor=User_table.focus()
        if cursor:
            print("cursor", cursor)
            content=User_table.item(cursor)
            print("content", content)
            row=content['values']
            print("row", row)
            id.set(row[0])
            firstname.set(row[1])
            print("row[1]", row[1])
            lastname.set(row[2])
            username.set(row[3])
            password.set(row[4])
            status.set(row[5])
        else:
            messagebox.showerror('Error','Select data row to edit')



    #buttons
    Frame_Btn = tk.Frame(Frame_Details,  bd=2, relief=tk.GROOVE)
    Frame_Btn.place(x=15, y=300, width=365, height=50)

    Edit_Button = tk.Button(Frame_Btn, text="Edit", bd=2, font=(15), width=6, command=FOCUS)
    Edit_Button.grid(row=0, column=4, padx=4, pady=5)

    Add_Button = tk.Button(Frame_Btn, text="Add", bd=2, font=(15), width=6, command=ADD_DATA)
    Add_Button.grid(row=0, column=0, padx=4, pady=1)
    
    Delete_Button = tk.Button(Frame_Btn, text="Delete", bd=2, font=(15), width=6, command=DELETE)
    Delete_Button.grid(row=0, column=1, padx=4, pady=1)
    
    Update_Button = tk.Button(Frame_Btn,  text="Update", bd=2, font=(15), width=6, command=UPDATE_DATA)
    Update_Button.grid(row=0, column=2, padx=4, pady=1)
    
    Clear_Button = tk.Button(Frame_Btn, text="Clear", bd=2, font=(15), width=6, command=CLEAR)
    Clear_Button.grid(row=0, column=3, padx=4, pady=1)


    # Search Frame
    Frame_Search = tk.Frame(Frame_Data , bd=2, relief=tk.GROOVE)
    Frame_Search.pack(side=tk.TOP, fill=tk.X)
    
    Label_Search = tk.Label(Frame_Search, text="SEARCH BY",  font=(16))
    Label_Search.grid(row=0, column=0, padx=12, pady=2)
    
    Search_Box = ttk.Combobox(Frame_Search, font=(6), state="readonly", textvariable=search_box)
    Search_Box['values'] = ("FIRSTNAME","LASTNAME", "USERNAME", "STATUS")
    Search_Box.current(0)
    Search_Box.grid(row=0, column=1, padx=12, pady=2)

    Entry_Search = tk.Entry(Frame_Search, bd=2, font=(12), width=20, textvariable=searchEntry)
    Entry_Search.grid(row=0, column=2, padx=12, pady=2)

    Search_Button = tk.Button(Frame_Search, text="SEARCH", bd=2, font=(15), width=10, command=GET_DATA_SEARCH)
    Search_Button.grid(row=0, column=3, padx=4, pady=1)
    
    Show_Button = tk.Button(Frame_Search, text="SHOW ALL", bd=2, font=(15), width=10, command=GET_DATA)
    Show_Button.grid(row=0, column=4, padx=4, pady=1)

    logout = tk.Button(Frame_Search, text="LOGOUT", bd=2, font=(15), width=10, command=LOG_OUT)
    logout.grid(row=0, column=5, padx=4, pady=1)

    # Database Frame
    Frame_Database = tk.Frame(Frame_Data, bd=2, relief=tk.GROOVE)
    Frame_Database.pack(fill=tk.BOTH, expand=True)
    
    Scroll_X = tk.Scrollbar(Frame_Database, orient=tk.HORIZONTAL)
    Scroll_Y = tk.Scrollbar(Frame_Database, orient=tk.VERTICAL)
    
    User_table = ttk.Treeview(Frame_Database, columns=("USER ID", "FIRSTNAME", "LASTNAME", "USERNAME","PASSWORD","STATUS"), yscrollcommand= Scroll_Y.set,xscrollcommand= Scroll_X.set)
    
    Scroll_X.config(command=User_table.xview)
    Scroll_X.pack(side=tk.BOTTOM, fill=tk.X)
    Scroll_Y.config(command=User_table.yview)
    Scroll_Y.pack(side=tk.RIGHT, fill=tk.Y)

    User_table.heading("USER ID", text="USER ID") 
    User_table.heading("FIRSTNAME", text="FIRSTNAME")
    User_table.heading("LASTNAME", text="LASTNAME")
    User_table.heading("USERNAME", text="USERNAME")
    User_table.heading("PASSWORD", text="PASSWORD")
    User_table.heading("STATUS", text="STATUS")

    User_table['show']='headings'
    User_table.column("USER ID",width= 10)
    User_table.column("FIRSTNAME",width= 100)
    User_table.column("LASTNAME",width= 100)
    User_table.column("USERNAME",width= 100)
    User_table.column("PASSWORD",width= 100)
    User_table.column("STATUS",width= 10)

    
    User_table.pack(fill=tk.BOTH, expand=True)

    GET_DATA()

    mainloop()

if __name__ == "__main__":
    main()