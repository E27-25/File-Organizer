import os
import shutil
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import customtkinter as ct
import pathlib
from PIL import Image

from txt_classification import *

#setup icon button
img_path = os.path.dirname(os.path.realpath(__file__))
img_1 = ct.CTkImage(Image.open(img_path + 
                    "/add-folder_v3.png"), size=(35, 35))

#main window
root = ct.CTk()
root.title("File Organizer")
root.geometry("520x244")
#root.iconbitmap("bocchi.ico")

#Cut Long Path for show "Input Path" clearly
def cut_path(path):
    parts = list(pathlib.PurePath(path).parts)
    if len(parts) >= 4:
        parts [2:-1] = ['...']
    return pathlib.PurePath(*parts)

def smart_or():
    if check_var.get() == 'on':
        smart_status = True
    else:
        smart_status = False
    #print(smart_status)
    return smart_status

#Show dir
my_dir = ct.CTkLabel(master=root,
                            text="Current Directory: ",
                            width=120,
                            height=25,
                            fg_color=("white", "gray20"),
                            corner_radius=8)
my_dir.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Create the button
button = ct.CTkButton(master=root,
                      image=img_1,
                      text="Select Folder",
                      width=200, 
                      height=50,
                      command=lambda: main_func(filedialog.askdirectory()))
button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

#Check Box for "Smart Folder" || "Classification from txt"
check_var = ct.StringVar(value='off')
check_box = ct.CTkCheckBox(master=root, 
                          text='Smart Organize (Beta)', 
                          width=100, 
                          height=20,
                          variable=check_var, 
                          onvalue='on', offvalue='off', 
                          command=lambda: smart_or())
check_box.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

audio = (".3ga", ".aac", ".ac3", ".aif", ".aiff",
         ".alac", ".amr", ".ape", ".au", ".dss",
         ".flac", ".flv", ".m4a", ".m4b", ".m4p",
         ".mp3", ".mpga", ".ogg", ".oga", ".mogg",
         ".opus", ".qcp", ".tta", ".voc", ".wav",
         ".wma", ".wv")

video = (".webm", ".MTS", ".M2TS", ".TS", ".mov",
         ".mp4", ".m4p", ".m4v", ".mxf", ".MP4")

img = (".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png",
       ".gif", ".webp", ".svg", ".apng", ".avif")

doc = (".pdf", ".docx", ".ppt", ".doc", ".pptx")

smart_support = (".pdf", ".png", ".jpg")

#text = ["Audio", "Video", "Screenshots", "Images", input_name, "Slide"]
list_folder_name = ["Audios", "Videos", "Images", "Documents"]
main_folder = ['Smart Categories', 'File Categories']
list_smart_folder_name = {'Accounts': 'accounts', 'Biology': 'biology', 
                          'Com-Tech': 'com-tech', 'Geography': 'geography', 
                          'History': 'history', 'Maths': 'maths', 
                          'Physics': 'physics'}

def is_audio(file):
    return os.path.splitext(file)[1] in audio

def is_video(file):
    return os.path.splitext(file)[1] in video

def is_image(file):
    return os.path.splitext(file)[1] in img

def is_doc(file):
    return os.path.splitext(file)[1] in doc

def is_smart_support(file):
    return os.path.splitext(file)[1]


#Check Folder exists or not
def check_folder_exists(folder_name):
    """Checks if a folder exists and returns True if it does, False otherwise."""
    if os.path.exists(folder_name):
        return True
    else:
        return False

#Create Folder
def create_folder(folder_name):
    """Creates a folder if it does not exist."""
    if not check_folder_exists(folder_name):
        os.mkdir(folder_name)
        print("Folder created successfully.")
    else:
        print("Folder already exists.")

#Main Function of Program
def main_func(source):

    path = source
    os.chdir(path)
    my_dir.configure(text=f"Current Directory: {cut_path(path)}")

#Check Folder and Create Folder
    if main_folder[1] not in os.listdir():
        os.mkdir(main_folder[1])
    os.chdir(path+f'/{main_folder[1]}')
    for folder_name in list_folder_name:
        if not check_folder_exists(folder_name):
            create_folder(folder_name)
        else:
            print("Folder already exists.")

    if smart_or() == True:
        os.chdir(path)
        if main_folder[0] not in os.listdir():
            os.mkdir(main_folder[0])
        os.chdir(path+f'/{main_folder[0]}')
        for folder_name in list(list_smart_folder_name.keys()):
            if not check_folder_exists(folder_name):
                create_folder(folder_name)
            else:
                print("Folder already exists.")

#Sort File
    os.chdir(path)
    key_list = list(list_smart_folder_name.keys())
    val_list = list(list_smart_folder_name.values())
    new_doc = ''
    for file in os.listdir():
        if smart_or() == True and is_smart_support(file) in smart_support:
            #Import Doc and img
                if is_smart_support(file) == smart_support[0]:
                    new_doc = get_text_from_pdf_PyPDF2(file)
                else:
                    new_doc = get_text_from_img(file)
                #Find Key and Value
                    #print(f"AAAAA{new_doc.strip()}AAAAA")
                    #print(type(new_doc))
                value_name=classify(new_doc)
                print(value_name)
                    #print(type(value_name))
                    #print(key_list)
                    #print(val_list)
                key_name = key_list[val_list.index(value_name)]
                    #print(key_name)
                #move File
        if new_doc.strip()!='' and smart_or() == True and is_smart_support(file) in smart_support:
            shutil.move(file, path+f"\{main_folder[0]}\{key_name}")
        elif is_audio(file):
            shutil.move(file, path+f"\{main_folder[1]}\Audios")
        elif is_video(file):
            shutil.move(file, path+f"\{main_folder[1]}\Videos")
        elif is_image(file):
            shutil.move(file, path+f"\{main_folder[1]}\Images")
        elif is_doc(file):
            shutil.move(file, path+f"\{main_folder[1]}\Documents")

root.mainloop()
