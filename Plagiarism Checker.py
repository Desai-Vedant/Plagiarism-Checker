
#######################################--PLAGARISM CHECKER--##############################################

#######################################--IMPORTING LIBRARIES--############################################

import tkinter
from tkinter.messagebox import showinfo
from tkinter import *
import tkinter as tk
import customtkinter
from PIL import Image
import os
from tkinter.filedialog import askopenfile,askopenfiles,asksaveasfile,asksaveasfilename
import string
from openpyxl import Workbook


#######################################--DECLARING GLOBAL VARIABLES--#####################################

#Variable For Two Files Text
global FileText
FileText=["",""]
#Variable for Multiple FILES
global Files
Files =[]
#Variable to Store Multiple File Text
global FilesText
FilesText=[]
#Variable to Store Duplicate Sentences
global Duplicates
Duplicates=[]
#Variable To Store Details of file and Corresponding Percentage
global Datalist
Datalist =[]



##############################################--FUNCTIONS--###############################################

#Function To Return Plagarism Percentage
def PlagarismPercentage(FileText_1,FileText_2):
    Sentences1=FileText_1.split("\n")
    Sentences2=FileText_2.split("\n")
    Count=0
    for x in Sentences1:
        for y in Sentences2:
            if x==y:
                if x!="":
                    Count=Count+len(x)
                    break
    Similarity=Count*100/(len(FileText_1)-len(Sentences1))
    return int(limit(Similarity))

#Function to Store Duplicate Sentences in Global Duplicates Array
def DuplicateSentences(FileText_1,FileText_2):
    Sentences1=FileText_1.split("\n")
    Sentences2=FileText_2.split("\n")
    global Duplicates
    Duplicates.clear()
    for x in Sentences1:
        x=x.strip()
    for x in Sentences2:
        x=x.strip()
    for x in Sentences1:
        for y in Sentences2:
            if x==y:
                Duplicates.append(x)
                break

#Function To Open File 1
def OpenFile1(ButtonText):
    ButtonText.set("Loading..")
    File1 = askopenfile(mode = 'r', title="Choose a File", filetypes=[("All files","*"),
                                                                      ("text file","*.txt"),
                                                                      ("java File","*.java"),
                                                                      ("python file","*.py"),
                                                                      ("C file","*.c"),
                                                                      ("C++ file","*.cpp")])
    if File1 :
        ButtonText.set(os.path.basename(File1.name))
        global FileText
        FileText[0]=File1.read()
    else:
        ButtonText.set("Choose File 1")

#Function To Open File 2
def OpenFile2(ButtonText):
    ButtonText.set("Loading..")
    File2 = askopenfile(mode = 'r', title="Choose a File", filetypes=[("All files","*"),
                                                                      ("text file","*.txt"),
                                                                      ("java File","*.java"),
                                                                      ("python file","*.py"),
                                                                      ("C file","*.c"),
                                                                      ("C++ file","*.cpp")])
    if File2 :
        ButtonText.set(os.path.basename(File2.name))
        global FileText
        FileText[1]=File2.read()
    else:
        ButtonText.set("Choose File 2")

#Function To Open Multiple Files
def OpenFiles(ButtonText):
    ButtonText.set("Loading..")
    global Files
    global FilesText
    Files.clear()
    Files = askopenfiles(mode ='r', title="Choose Multiple Files", filetypes=[("All files","*"),
                                                                      ("text file","*.txt"),
                                                                      ("java File","*.java"),
                                                                      ("python file","*.py"),
                                                                      ("C file","*.c"),
                                                                      ("C++ file","*.cpp")])
    if Files:
        ButtonText.set((str(len(Files))+" Files Selected"))
        FilesText.clear()
        for x in Files:
            FilesText.append(x.read())
    else:
        ButtonText.set("CHOOSE FILES")

#Function to print result into textbox for two files
def TwoFileCompareResult(TextBox):
    TextBox.delete("1.0","end")
    global FileText
    global Duplicates
    Similarity = PlagarismPercentage(FileText[0],FileText[1])
    DuplicateSentences(FileText[0],FileText[1])
    for x in range(len(Duplicates)-1,0,-1):
        if Duplicates[x]!="":
            TextBox.insert("1.0",Duplicates[x])
            TextBox.insert("1.0","\n")
    TextBox.insert("1.0","\n\nDuplicate Sentences Are:\n")
    TextBox.insert("1.0",("Similarity Percentage is : "+str(Similarity)))

def MultipleCompareResult(TextBox):
    TextBox.delete("1.0","end")
    global Files
    global FilesText
    for x in FilesText:
        a=FilesText.index(x)
        for y in FilesText:
            b=FilesText.index(y)
            Similarity = PlagarismPercentage(x,y)
            FileName1=os.path.basename(Files[a].name)
            FileName2=os.path.basename(Files[b].name)
            TextBox.insert("1.0",(FileName1+"\t and \t"+FileName2+"\t  -  \t"+str(Similarity)))
            TextBox.insert("1.0","\n")

def MultipleCompTable(Frame):
    global Files
    global FilesText
    k=1
    Datalist.clear()
    Datalist.append(("No","File 1","File 2","Similarity"))
    for widget in Frame.winfo_children():
        widget.destroy()
    for x in FilesText:
        a=FilesText.index(x)
        for y in FilesText:
            b=FilesText.index(y)
            Similarity = PlagarismPercentage(x,y)
            FileName1=os.path.basename(Files[a].name)
            FileName2=os.path.basename(Files[b].name)
            Datalist.append((k,FileName1,FileName2,Similarity))
            k=k+1
    if(len(Datalist)<10):
        columns = len(Datalist)
    else:
        columns = 10
    for i in range(columns):
        for j in range(4):
            e = customtkinter.CTkEntry(Frame,width=500,font=('Arial',16))
            e.grid(row=i, column=j, sticky = "nsew")
            e.insert(END, Datalist[i][j])

def SaveReport():
    global Datalist
    wb = Workbook()
    ws = wb.active
    for row in Datalist:
        ws.append(row)
    wb.save('Report.xlsx')

def limit(k):
    if k>100:
        return 100
    else:
        return k

#######################################--GRAPHICAL USER INTERFACE--#######################################


#Setting Color Theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Create App Object
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Plagarisim Checker")
        self.geometry(f"{1100}x{580}")
        self.minsize(1100,580)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx = (20,10), pady = (20,20), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Welcome to \nPlagarism Checker", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text_color=("black","white"), text="HOMOEPAGE", command=self.Homepage)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text_color=("black","white"), text="COMPARE TWO FILES", command=self.TwoFilePage)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text_color=("black","white"), text = "MULTIPLE COMPARE", command=self.MultipleFilePage)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,text_color=("black","white"), text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,text_color=("black","white"), values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame,text_color=("black","white"), text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,text_color=("black","white"), values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        #Set Default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.Homepage()


    #Appearance Modes (Light Dark System)
    def change_appearance_mode_event(self,new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    #Scaling Menu(80% 90% 100% 110% 120%)
    def change_scaling_event(self,new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    #Homepage Definatiion
    def Homepage(self):
        Frame = customtkinter.CTkFrame(self, corner_radius = 10)
        Frame.grid_columnconfigure((0), weight=1)
        Frame.grid_rowconfigure((0), weight=1)
        Frame.grid(row = 0, column = 1, padx=(10,20), pady=(20,20), rowspan = 4, columnspan = 3, sticky="nsew")
        Banner = customtkinter.CTkImage(light_image=Image.open("light_bg.png"),dark_image=Image.open("dark_bg.png"), size=(900,540))

        Banner_label = customtkinter.CTkLabel(Frame, text = "",image=Banner)
        Banner_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")

    #Two File Comparision Page
    def TwoFilePage(self):
        Frame = customtkinter.CTkFrame(self, corner_radius = 10)
        Frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        Frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        Frame.grid(row = 0, column = 1, padx=(10,20), pady=(20,20), rowspan = 4, columnspan = 3, sticky="nsew")
        Label = customtkinter.CTkLabel(Frame,text_color=("black","white"), text="CHOOSE TWO FILES", font=customtkinter.CTkFont(size=20, weight="bold"))
        Label.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 20), sticky="ew")

        Button_1_text = tkinter.StringVar()
        Button_1_text.set("CHOOSE FILE 1")
        Button_1 = customtkinter.CTkButton(Frame,text_color=("black","white"), textvariable= Button_1_text, command = lambda:OpenFile1(Button_1_text))
        Button_1.grid(row=1, column=1, padx=20, pady=20, sticky ="ew")

        Button_2_text = tkinter.StringVar()
        Button_2_text.set("CHOOSE FILE 2")
        Button_2 = customtkinter.CTkButton(Frame,text_color=("black","white"), textvariable=Button_2_text,  command = lambda:OpenFile2(Button_2_text))
        Button_2.grid(row=1, column=3, padx=20, pady=20, sticky ="ew")

        Button_3 = customtkinter.CTkButton(Frame,text_color=("black","white"), text = "CHECK PLAGIARISM",  command = lambda:TwoFileCompareResult(textbox))
        Button_3.grid(row=2, column=2, padx=20, pady=20, sticky = "ew")

        textbox = customtkinter.CTkTextbox(Frame)
        textbox.grid(row=3, column=0, columnspan= 5, rowspan= 3, padx=(20,20), pady=(20,20), sticky="nsew")

    #Multiple File Compare Page
    def MultipleFilePage(self):
        Frame = customtkinter.CTkFrame(self, width = 500, corner_radius = 10)
        Frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        Frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        Frame.grid(row = 0, column = 1, padx=(10,20), pady=(20,20), rowspan = 4, columnspan = 3, sticky="nsew")

        Frame2 = customtkinter.CTkFrame(Frame)
        Frame2.grid_columnconfigure((0), weight=3)
        Frame2.grid_columnconfigure((1,2), weight=1)
        Frame2.grid_columnconfigure((3), weight=2)
        Frame2.grid_columnconfigure((4), weight=5)
        Frame2.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        Frame2.grid(row = 1, column = 0, columnspan = 5, rowspan = 3, padx = 20, pady = 20, sticky = "nsew")

        Button_text = tkinter.StringVar()
        Button_text.set("CHOOSE FILES")
        Button_1 = customtkinter.CTkButton(Frame,text_color=("black","white"), textvariable= Button_text, command = lambda:OpenFiles(Button_text))
        Button_1.grid(row=0, column=1, padx=20, pady=20, sticky ="ew")

        Button_2 = customtkinter.CTkButton(Frame,text_color=("black","white"), text= "Check Plagarism", command = lambda:MultipleCompTable(Frame2))
        Button_2.grid(row=0, column=3, padx=20, pady=20, sticky ="ew")

        Button_3 = customtkinter.CTkButton(Frame,text_color=("black","white"), text = "Save Report", command = lambda:SaveReport())
        Button_3.grid(row=4, column=3, padx=20, pady=20, sticky ="ew")

        Button_4 = customtkinter.CTkButton(Frame,text_color=("black","white"), text = "View Complete Report", command = lambda:DetailedReport(self))
        Button_4.grid(row=4, column=1, padx=20, pady=20, sticky ="ew")



        def DetailedReport(self):
            Report = Toplevel()
            Report.title("Detailed Report")
            Report.geometry("1100x580")

            columns = ('No', 'File1', 'File2', 'Similarity')

            tree = tkinter.ttk.Treeview(Report, columns=columns, show='headings')

            # define headings
            tree.heading('No', text='Sr No')
            tree.heading('File1', text='File 1 Name')
            tree.heading('File2', text='File 2 Name')
            tree.heading('Similarity', text='Similarity Percentage')

            global Datalist

            # add data to the treeview
            for data in Datalist:
                tree.insert('', tk.END, values=data)

            tree.pack(expand=True, fill='both')

            Report.mainloop()



if __name__ == "__main__":
    app = App()
    app.mainloop()


##################################################--END--#################################################
