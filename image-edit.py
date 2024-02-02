import sys
import os
import cv2
import re
import csv
import tkinter as tk
from tkinter import PhotoImage
from tkinter import Label

class mainGUI(object):
    def __init__(self):
        self.ROOT = tk.Tk()
        self.ROOT.title = "Image Classifier"
        self.directory = './experiments'
        self.csvFile = './MasterExperiment.csv'
        self.allFiles = sorted(os.listdir(self.directory))
        self.fIndex = 0
        self.file = ""
        self.experiment = -1
        self.step = -1
        self.saveData = []

        self.fileLabel = tk.Label(self.ROOT, text="File Name")
        self.fileLabel.place(relx=0.5, rely=1, anchor='n')
        self.fileLabel.pack()

        self.canvas = tk.Canvas(width=400, height=800, bg='white')
        self.canvas.pack(side='left')

        self.observationLabel = tk.Label(self.ROOT, text="Observation")
        self.observationLabel.pack()

        self.observationText = tk.Text(self.ROOT, height=1, width=30, bg='white', fg='black')
        self.observationText.pack()

        self.classTextLabel = tk.Label(self.ROOT, text="Class")
        self.classTextLabel.pack()

        self.classText = tk.Text(self.ROOT, height=1, width=6, bg='white', fg='black')
        self.classText.pack()

        self.saveButton = tk.Button(self.ROOT, text="Save", command=lambda:self.SaveNotes())
        self.saveButton.pack()

        self.nextButton = tk.Button(self.ROOT, text="Next Image", command=lambda:self.NextImage())
        self.nextButton.pack()

        self.img = self.canvas.create_image(200, 400)
        self.ROOT.mainloop()

    def SaveNotes(self):
        sClass = self.classText.get("1.0", tk.END).strip()
        sObser = self.observationText.get("1.0", tk.END).strip()

        print("Saving Experiment " + str(self.experiment) + " Step " + str(self.step))
        print("Class:",sClass)
        print("Observation:",sObser)

        with open(self.csvFile) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=',')
            #csvWriter = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            lineCount = 0
            lineMin = 18*self.experiment+10
            lineMax = lineMin+14
            for row in csvReader:
                if lineCount > lineMin and lineCount < lineMax:
                    if int(row[0]) == self.step:
                        self.saveData.extend([row[0], row[1], sClass, row[3], row[4], row[5], row[6], row[7], sObser])
                        print("Saved!")
                        return
                lineCount += 1

    def NextImage(self):

        if (self.fIndex >= len(self.allFiles)):
            self.fileLabel.config(text="No more files to view!")
            return

        self.file = os.path.join(self.directory, self.allFiles[self.fIndex])

        print("Displaying File:", self.file)
        if (os.path.isfile(self.file) == False):
            print("Not a file!")
            self.fIndex += 1
            return
        
        regRes = re.findall("\d+", self.file)
        self.experiment = int(regRes[0])
        self.step = int(regRes[1])

        with open(self.csvFile) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=',')
            lineCount = 0
            lineMin = 18*self.experiment+10
            lineMax = lineMin+14
            for row in csvReader:
                if lineCount > lineMin and lineCount < lineMax:
                    if int(row[0]) == self.step:
                        if row[2] != '' and row[8] != '':
                            print("Entry already there, skipping row:", lineCount)
                            self.NextFile()
                            self.NextImage()
                            return
                lineCount += 1
        
        self.NextFile()
        #self.ROOT.update()

    def NextFile(self):
        self.photo = tk.PhotoImage(file=self.file)
        self.photo = self.photo.subsample(3, 5)
        self.canvas.itemconfig(self.img, image=self.photo)
        self.fileLabel.config(text=self.file)
        self.classText.delete('1.0', tk.END)
        self.observationText.delete('1.0', tk.END)
        self.fIndex += 1

    def ReadAsCSV(self):
        return ""


if __name__ == "__main__":
    gui = mainGUI()
