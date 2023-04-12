from tkinter import *
import GUI.MainWindow


def main():
    window = Tk()
    mainWindow = GUI.MainWindow.MainWindow(window)
    window.mainloop()



if __name__ == '__main__':
    main()