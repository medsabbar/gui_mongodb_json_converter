import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import subprocess
import sys
import platform
import json
import datetime


class FileInputGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Input GUI")
        self.root.geometry("300x300")

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
            df = json.load(open(self.input_file_path))
        except ValueError:
            tk.messagebox.showinfo("Error",
                                   "File could not be converted to DataFrame")
        if dictionaryFileType:
            dictionary = json.load(open(self.input_dictionary_file_path))
            # convert all the headers to the dictionary header using the key and labeleFr
            # create a hashmap for the already converted headers
            map = {}
            newDf = []
            for i in range(len(df)):
                newDf.append({})
                for key in df[i].keys():
                    if key in map:
                        newDf[i][map[key]] = df[i][key]
                        continue
                    for j in range(len(dictionary)):
                        if key == dictionary[j]['key']:
                            newDf[i][dictionary[j]['labeleFr']] = df[i][key]
                            map[key] = dictionary[j]['labeleFr']
                            break
                        # if the last one and not found
                        elif j == len(dictionary) - 1:
                            newDf[i][key] = df[i][key]

            print('first')
            print(newDf[0])
            # convert all the values to the dictionary values using the key and labeleFr
            for i in range(len(newDf)):
                for key in newDf[i].keys():
                    if key in map:
                        newDf[i][key] = map[key]
                        continue
                    for j in range(len(dictionary)):
                        if newDf[i][key] == dictionary[j]['key']:
                            newDf[i][key] = dictionary[j]['labeleFr']
                            map[key] = dictionary[j]['labeleFr']
                            break
            print(newDf[0])

        df = pd.DataFrame(df)

        if len(newDf) > 0:
            df = pd.DataFrame(newDf)

        print('second')
        print(newDf[0])

        # iterate through each key in the DataFrame
        for i in range(len(df)):
            valuesToConvert = ['$oid', '$date', '$numberLong']
            for key in df.iloc[i].keys():
                if isinstance(df.iloc[i][key], dict):
                    for valueToConvert in valuesToConvert:
                        print("df.iloc[i][key]")
                        print(df.iloc[i][key])
                        if valueToConvert in df.iloc[i][key]:
                            if valueToConvert == '$oid':
                                df.iloc[i][key] = df.iloc[i][key][valueToConvert]
                            elif valueToConvert == '$date':
                                df.iloc[i][key] = datetime.datetime.fromtimestamp(
                                    df.iloc[i][key][valueToConvert]/1000.0)
                            elif valueToConvert == '$numberLong':
                                df.iloc[i][key] = df.iloc[i][key][valueToConvert]

        print('third')
        print(newDf[0])

        # open a file dialog to select the output file path
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx")

        # write the DataFrame to an Excel file
        df.to_excel(output_file_path, index=False)

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
        self.root.mainloop()


if __name__ == "__main__":
    gui = FileInputGUI()
    gui.run()
