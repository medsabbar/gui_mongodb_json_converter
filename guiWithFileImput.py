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

        # create a label to display help text
        self.help_label = tk.Label(
            self.root, text="Please select a JSON file to convert.", wraplength=280)
        self.help_label.pack()

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

        if dictionaryFileType:
            dictionary = pd.read_json(self.input_dictionary_file_path)
            for i in range(len(dictionary)):
                for key in dictionary.iloc[i].keys():
                    dictionary.iloc[i][key] = dictionary.iloc[i][key].lower()

        # read the input file into a pandas DataFrame
        try:
            df = pd.read_json(self.input_file_path)
        except ValueError:
            tk.messagebox.showinfo("Error",
                                   "File could not be converted to DataFrame")

        # iterate through each key in the DataFrame
        for i in range(len(df)):
            valuesToConvert = ['$oid', '$date', '$numberLong']
            for key in df.iloc[i].keys():
                print(df.iloc[i][key])
                if isinstance(df.iloc[i][key], object):
                    for value in valuesToConvert:
                        if value in df.iloc[i][key]:
                            if value == '$date':
                                dt = datetime.datetime.strptime(
                                    df.iloc[i][key][value], '%Y-%m-%dT%H:%M:%S.%fZ')
                                print(df.iloc[i][key][value])
                                df.iloc[i][key] = dt.strftime(
                                    '%Y-%m-%d %H:%M')
                            else:
                                df.iloc[i][key] = df.iloc[i][key][value]

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
