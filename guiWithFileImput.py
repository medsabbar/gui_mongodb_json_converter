import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import pandas as pd
import os
import subprocess
import sys
import platform
import json
import datetime
from modalData import print_fields, flatten_object, flatten_object_no_translation


totalProce = 4

if getattr(sys, 'frozen', False):
    import pyi_splash


def handleTranslation(self, df, dictionary, language, curentDoc, totaDoc, curenLang=1):
    labe = 'labele' + language
    newDf = []
    myMap = {}
    for i in range(len(df)):
        curentDoc = curentDoc + 1
        if curenLang == 2 and curentDoc < totaDoc / 2:
            curentDoc = (totaDoc / 2) + 1
        prog = curentDoc / totaDoc * 100
        self.progress['value'] = prog
        self.progress.update_idletasks()
        self.progress_label.config(text=str("{:.2f}".format(prog)) + "%")
        self.progress_label.update_idletasks()
        newDf.append({})
        if len(dictionary) < 1:
            newDf[i] = flatten_object_no_translation(
                df[i], ''
            )
            continue
        else:
            df[i] = flatten_object(
                df[i], '', myMap, dictionary, labe)

        for key in df[i].keys():
            if key in myMap:
                newDf[i][myMap[key]] = df[i][key]
                continue
            for j in range(len(dictionary)):
                if key == dictionary[j]['key']:
                    newDf[i][dictionary[j][labe]] = df[i][key]
                    myMap[key] = dictionary[j][labe]
                    break
                # if the last one and not found
                elif j == len(dictionary) - 1:
                    newDf[i][key] = df[i][key]
    for i in range(len(newDf)):
        if len(dictionary) < 1:
            continue
        curentDoc = curentDoc + 1
        if curenLang == 2 and curentDoc < totaDoc / 2:
            curentDoc = (totaDoc / 2) + 1
        prog = curentDoc / totaDoc * 100
        self.progress['value'] = prog
        self.progress.update_idletasks()
        self.progress_label.config(text=str("{:.2f}".format(prog)) + "%")
        self.progress_label.update_idletasks()
        for key in newDf[i].keys():
            if key in myMap:
                newDf[i][key] = myMap[key]
                continue
            for j in range(len(dictionary)):
                if newDf[i][key] == dictionary[j]['key']:
                    newDf[i][key] = dictionary[j][labe]
                    myMap[key] = dictionary[j][labe]
                    break
    return newDf


class FileInputGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sabbar convert")

        # create a label to display help text
        self.help_label = tk.Label(
            self.root, text="Selectionnez un fichier JSON à convertir.", wraplength=280)
        self.help_label.pack()

        # create the browse button for the file dialog
        self.browse_button = tk.Button(
            self.root, text="Fichier des données", command=self.browse_file)
        self.browse_button.pack(pady=10)

        # create a label to display the file path
        self.file_label = tk.Label(
            self.root, text="", wraplength=280, fg="blue")
        self.file_label.pack()

        # create the browse button for the dictionary file dialog
        self.browse_button = tk.Button(
            self.root, text="Fichier des traduction", command=self.browse_file2)
        self.browse_button.pack(pady=10)

        # create a label to display the dictionary file path
        self.dictionary_file_label = tk.Label(
            self.root, text="", wraplength=280, fg="blue")
        self.dictionary_file_label.pack()

        # create a button to convert the file
        self.convert_button = tk.Button(
            self.root, text="Convertir", command=self.convert_file)
        self.convert_button.pack(pady=10)

        self.progress = Progressbar(self.root, orient=tk.HORIZONTAL,
                                    length=100, mode='determinate')
        self.progress.pack(pady=(10, 0))

        self.progress_label = tk.Label(
            self.root, text="", wraplength=280, fg="blue")
        self.progress_label.pack()

        # create a watermark label
        self.watermark_label = tk.Label(
            self.root, text="V-0.2 ~ Created by: Sabbar Mohamed", fg="gray")
        self.watermark_label.pack(side=tk.BOTTOM)

    def browse_file(self):
        # open a file dialog to browse for a file
        file_path = filedialog.askopenfilename()
        self.file_label.config(text=file_path)
        self.input_file_path = file_path

    def browse_file2(self):
        # open a file dialog to browse for a dictionary file
        file_path = filedialog.askopenfilename()
        self.dictionary_file_label.config(text=file_path)
        self.input_dictionary_file_path = file_path

    def convert_file(self):
        fileType = os.path.splitext(self.input_file_path)[-1]
        dictionaryFileType = ''
        if hasattr(self, "input_dictionary_file_path"):
            dictionaryFileType = os.path.splitext(
                self.input_dictionary_file_path)[-1]

        if fileType != ".json" or dictionaryFileType and dictionaryFileType != ".json":
            tk.messagebox.showinfo("Error",
                                   "Unsupported file type " + str(fileType))
            return

        # read the input file into a pandas DataFrame
        try:
            mdf = json.load(open(self.input_file_path))
        except ValueError:
            tk.messagebox.showinfo("Error",
                                   "File could not be converted to DataFrame")

        dictionary = []
        totaDoc = len(mdf) * totalProce
        curentDoc = 0
        if dictionaryFileType:
            dictionary = json.load(open(self.input_dictionary_file_path))
            newDfFr = handleTranslation(
                self, mdf, dictionary, "Fr", curentDoc, totaDoc, 1)
            newDfAr = handleTranslation(
                self, mdf, dictionary, "Ar", curentDoc, totaDoc, 2)
            if len(newDfFr) > 0 and len(newDfAr) > 0:
                mdf = {
                    "Fr": newDfFr,
                    "Ar": newDfAr
                }
            else:
                mdf = {
                    "sheet": handleTranslation(
                        self, mdf, dictionary, "Fr", curentDoc, totaDoc, 1)
                }
        else:
            mdf = {
                "sheet": handleTranslation(
                    self, mdf, dictionary, "Fr", curentDoc, totaDoc, 1)
            }

        # go through the mdf object and convert the sub-objects to new strings
        # myMap = {}
        # for sheet_name in mdf.keys():
        #     typeToConvert = ['$oid', '$date', '$numberLong']
        #     for key in sheet_name:
        #         for i in range(len(mdf[sheet_name])):
        #             mdf[sheet_name][i] = flatten_object(
        #                 mdf[sheet_name][i], parent_key='', myMap=myMap, dictionary=dictionary)

        # iterate through the mdf object to convert each sheet to a DataFrame
        for sheet_name, dfff in mdf.items():
            mdf[sheet_name] = pd.DataFrame(dfff)

        # open a file dialog to select the output file path
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx")

        self.progress['value'] = 0
        self.progress_label.config(text='')

        # write the DataFrame to an Excel file
        with pd.ExcelWriter(output_file_path) as writer:
            for sheet_name, dfff in mdf.items():
                # write each dataframe to a sheet in the Excel file
                dfff.to_excel(writer, sheet_name=sheet_name, index=False)

        # display a message box to indicate conversion is complete
        tk.messagebox.showinfo("Conversion Complete",
                               "JSON file has been converted to Excel file.")

        # open the output file location
        if platform.system() == "Windows":
            os.startfile(output_file_path)

        elif platform.system() == "Darwin":
            def open_file(output_file_path):
                subprocess.call(["open", output_file_path])
            open_file(output_file_path)

        else:
            tk.messagebox.showinfo(
                "Unsupported platform: " + platform.system())
            sys.exit(1)

    def run(self):
        self.root.resizable(False, False)
        self.root.configure(padx=20, pady=20)
        self.root.mainloop()


class Authenticate:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Authentication")
        self.root.geometry("300x100")

        self.label = tk.Label(self.root, text="Enter your password")
        self.label.pack()

        self.password = tk.Entry(self.root, show="*")
        self.password.pack(pady=5)

        self.button = tk.Button(
            self.root, text="Authenticate", command=self.authenticate)
        self.button.pack(pady=5)

    def authenticate(self):
        if self.password.get() == "admin":
            self.root.destroy()
            gui = FileInputGUI()
            gui.run()
        else:
            tk.messagebox.showinfo(
                "Authentication Failed", "Incorrect password")

    def run(self):
        self.root.resizable(False, False)
        self.root.configure(padx=20, pady=20)
        self.root.mainloop()


if __name__ == "__main__":
    gui = FileInputGUI()
    gui.run()
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
