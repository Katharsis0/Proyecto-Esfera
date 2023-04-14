from tkinter import *
from tkinter import filedialog
import myparser
from myparser import *
import subprocess
from mylexer import *


class MainWindow:

    #Init the main window
    def __init__(self, master):
        self.file_name = ""
        self.lineCounter = 0
        self.movementScroll = 0.0
        self.master = master
        self.master.title("Esfera IDE")#Title of window
        self.master.geometry("1000x650+0+0")
        self.master.resizable(False, False)
        photo = PhotoImage(file = "./Images/rosa.png")#Icon of window

        self.master.iconphoto(False, photo)        
        self.master.configure(background="#313335")
        self.canvas = Canvas(master, width=1000, height=650, highlightthickness=0, relief='ridge')
        self.canvas.place(x=0, y=0)
        self.canvas.configure(bg='#3C3F41')

        self.menu_bar = Menu(self.master, background='black', fg='white')
        self.file_menu = Menu(self.menu_bar)
        self.file_menu.add_command(label="Open...", command=self.openFileMenu)
        self.file_menu.add_command(label="Save", command=self.saveFile)
        self.file_menu.add_command(label="Save as", command=self.saveFileAs)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.menu_bar)

        self.editor_text_Scrollbar = Scrollbar(self.canvas)

        #Numberline config
        self.numberLine = Text(self.canvas, width=4, height=21, bg='#313335', fg="#A2A1A1",
                               font=('Lucida Sans Typewriter', 11),
                               yscrollcommand=self.editor_text_Scrollbar.set)
        self.numberLine.insert(1.0, "1")
        self.numberLine.config(state=DISABLED)
        self.numberLine.place(x=1, y=40)

        #Text editor config
        self.editor_text = Text(self.canvas, width=104, height=21, font=('Lucida Sans Typewriter', 11),
                                yscrollcommand=self.editor_text_Scrollbar.set)

        self.editor_text.bind("<KeyPress>", self.keyPress)

        self.editor_text.config(bg='#2B2B2B', fg='white')
        self.editor_text_Scrollbar.config(bg='#2B2B2B')

        self.editor_text_Scrollbar.config(command=self.multipleScroll)

        self.editor_text.place(x=40, y=40)
        self.editor_text_Scrollbar.place(x=980, y=40, height=361)

        self.canvas.bind_all("<MouseWheel>", self.scroll)
        
        #Run button
        self.run_button = Button(self.canvas,text="Run", width=8, height=1, bg='#4C5052', fg='white',command=self.run)
        self.run_button.place(x=920, y=7)

        #Compile button
        self.compile_button = Button(self.canvas,text="Compile", width=8, height=1, bg='#4C5052', fg='white',command=self.compile)
        self.compile_button.place(x=820, y=7)

        #Console
        self.console_text = Text(self.canvas, width=104, height=12, font=('Lucida Sans Typewriter', 11))
        self.console_text.insert(1.0, ">")
        self.console_text.config(state=DISABLED)
        self.console_text.place(x=40, y=410)
        self.console_text.config(bg='#2B2B2B', fg='white')

        self.console_text_Scrollbar = Scrollbar(self.canvas)
        self.console_text_Scrollbar.config(command=self.console_text.yview)
        self.console_text_Scrollbar.place(x=980, y=410, height=208)

    def multipleScroll(self, *args):
        self.editor_text.yview(*args)
        self.numberLine.yview(*args)

    def scroll(self, event):
        self.movementScroll = self.editor_text.yview()[0]
        self.numberLine.yview("moveto", self.movementScroll)
        return 'break'

    #Open file function
    def openFileMenu(self):
        filetypes = (("Esfera File","*.sfra"),("All files", "*.*"))

        self.file_name = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=filetypes)
        self.master.title("Esfera IDE - " + self.file_name)
        self.editor_text.insert(END, self.file_name)
        self.loadFile(self.file_name)


    def saveFileAs(self):
        if self.file_name == '':
            self.file_name = filedialog.asksaveasfilename(initialdir="./Tests", title="Save file", filetypes=(("Esfera File","*.sfra"), ("All files", "*.*")))
            self.file_name = self.file_name + ".sfra"
        else:
            self.file_name = self.file_name
        self.file_name = self.file_name + ".sfra"
        self.master.title("Esfera IDE - " + self.file_name)
        file = open(self.file_name,"x")
        file.write(self.editor_text.get(1.0,END))
        file.close()

    #Save file function
    def saveFile(self):
        #self.file_name = filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(("Esfera File","*.sfra"), ("All files", "*.*")))
        self.file_name = filedialog.asksaveasfilename(initialdir="./Tests", title="Save file", filetypes=(("Esfera File","*.sfra"), ("All files", "*.*")))
        self.file_name = self.file_name + ".sfra"
        self.master.title("Esfera IDE - " + self.file_name)
        file = open(self.file_name,"x")
        file.write(self.editor_text.get(1.0,END))
        file.close()


    def keyPress(self, event):
        self.updateScroll()
        self.updateLines()

    #Update line number function
    def updateLines(self):
        lines = 0
        for i in self.editor_text.get(1.0, END):
            if i == "\n":
                lines += 1
        self.numberLine.config(state=NORMAL)
        self.numberLine.delete(1.0, END)
        for i in range(1, lines + 1):
            if i == 1:
                self.numberLine.insert(END, str(i))
            else:
                self.numberLine.insert(END, "\n" + str(i))
        self.updateScroll()

    #Load file function
    def loadFile(self, file_name):
        file = open(file_name, "r", encoding="utf-8")
        self.editor_text.delete(1.0, END)
        self.editor_text.insert(END, file.read())
        file.close()
        self.updateLines()



    # def set_file_path(self, path):
    #     self.file_name = self.path
    #
    # def get_file_path(self):
    #     return self.file_name



    def updateScroll(self):
        self.numberLine.config(state=DISABLED)
        self.movementScroll = self.editor_text.yview()[0]
        self.numberLine.yview("moveto", self.movementScroll)

    #Add text to console
    def addTextToConsole(self, text):
        self.console_text.config(state=NORMAL)
        self.console_text.insert(END, text)
        self.console_text.config(state=DISABLED)
        self.console_text.see(END)

    #Run process TODO: Add run process
    def run(self):
        if self.file_name== '':
            self.save_prompt = Toplevel()
            self.save_prompt.title('Error')
            self.save_prompt.geometry('200x100')
            self.save_prompt.resizable(False, False)
            self.save_prompt.configure(bg="#313335")

            photo2 = PhotoImage(file = "./Images/rosa.png")
            self.save_prompt.iconphoto(False, photo2)

            text = Label(self.save_prompt, text='Please save your code first', font=('Arial', 12), fg ='white', bg="#313335")
            text.pack(pady=10)
            return
        # command = f'python {file_path}'
        # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # output, error = process.communicate()
        # self.code_output.insert('1.0', output)
        # self.code_output.insert('1.0',  error)

        print(self.editor_text.get(1.0, END))

    #Compile process. TODO: Add compile process 
    def compile(self):
        myparser.file_path(self.file_name)
        print("Compiling...")
        # #create parser and lexer
        # parser = yacc.yacc(debug=True)
        # lexer = lex.lex()
        # #Open file
        # with open(inputFile, 'r') as file:
        #     data=file.read()
        #     res=parser.parse(data)
        #     lexer.input(data)
        #     if res != None:
        #         res = list(filter(None, res))
        #     print(res)
        # while True:
        #     tok = lexer.token()
        #     if not tok:
        #         break
        #     print(tok)

