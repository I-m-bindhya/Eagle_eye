from tkinter import *
import exe, reports_, recipie, eagle


def main():

    def settings():
        root = delete()
        exe.main(root)

    def recipeList():
        root = delete()
        recipie.main(root)

    def report():
        root = delete()
        reports_.main(root)

    def logout():
        root.destroy()
        eagle.main()

    def delete():
        root.destroy()
        init()

    def init():
        global root
        root = Tk()
        root.state("zoomed")
        root.title("Eagle Eye")
        menubar = Menu(root)
        menubar.add_cascade(label="Settings", command=settings, font = ("", 50))
        menubar.add_cascade(label="Recipe list", command=recipeList, font = ("", 50))
        menubar.add_cascade(label="Reports", command=report, font = ("", 50))
        menubar.add_cascade(label="Log out", command=logout, font = ("", 50))
        root.config(menu=menubar, width=20, height=20, padx=20, pady=20)
        return root

    init()

    exe.main(root)

    root.mainloop()


if __name__ == "__main__":
    main()