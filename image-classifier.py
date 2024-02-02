import sys
import os
import re
import csv
import tkinter as tk

class mainGUI(object):
    def __init__(self):
        self.ROOT = tk.Tk()
        self.directory = './experiments' #Directory with all the images
        self.csvFile = './MasterExperiment.csv'
        self.newCSVFile = './MasterExperimentEdit.csv' #When exporting, the csv is temporarily saved in this file before the overwrite
        self.allFiles = sorted(os.listdir(self.directory))
        self.fIndex = 0 #File index, tracks currently opened file
        self.file = "" #File that's currently open
        self.experiment = -1
        self.step = -1
        self.saveData = {} #Tracks updated rows for when the data is exported

        self.ROOT.title("Image Classifier")

        self.fileLabel = tk.Label(self.ROOT, text="File Name")
        self.fileLabel.place(relx=0.5, rely=1, anchor='n')
        self.fileLabel.pack()

        self.canvas = tk.Canvas(width=400, height=800, bg='white')
        self.canvas.pack(side='left')

        self.observationLabel = tk.Label(self.ROOT, text="Observation")
        self.observationLabel.pack()

        self.observationText = tk.Text(self.ROOT, height=1, width=30, bg='white', fg='black')
        self.observationText.bind("<Tab>", self.FocusNext)
        self.observationText.pack()

        self.classTextLabel = tk.Label(self.ROOT, text="Class")
        self.classTextLabel.pack()

        self.classText = tk.Text(self.ROOT, height=1, width=6, bg='white', fg='black')
        self.classText.bind("<Tab>", self.FocusPrev)
        self.classText.pack()

        self.saveButton = tk.Button(self.ROOT, text="Next Image", command=lambda:self.SaveNotes())
        self.saveButton.pack()

        self.saveExitButton = tk.Button(self.ROOT, text="Export and Exit", command=lambda:self.SaveExit())
        self.saveExitButton.pack()

        self.img = self.canvas.create_image(200, 400)
        self.NextImage()
        self.ROOT.mainloop()

    def SaveNotes(self):
        #Grabs the class and observation from the text boxes
        sClass = self.classText.get("1.0", tk.END).strip()
        sObser = self.observationText.get("1.0", tk.END).strip()

        print("Saving Experiment " + str(self.experiment) + " Step " + str(self.step))
        print("Class:",sClass)
        print("Observation:",sObser)

        # We open the file and find the row we edited in order to get the data we need to build our row for saving
        with open(self.csvFile) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=',')
            lineCount = 0
            lineMin = 18*self.experiment+10 
            lineMax = lineMin+14
            for row in csvReader:
                if lineCount > lineMin and lineCount < lineMax:
                    if int(row[0]) == self.step:
                        self.saveData[lineCount] = [row[0], row[1], sClass, row[3], row[4], row[5], row[6], row[7], sObser]
                        print("Saved!")
                        break
                lineCount += 1

        self.NextImage()

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
        
        #This gets the experiment number and step from the file name
        regRes = re.findall("\d+", self.file)
        self.experiment = int(regRes[0])
        self.step = int(regRes[1])

        #This skips any images that we've already entered data for in the csv
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
        self.FocusPrev('') #This is a hack so the event param is satisfied

    def NextFile(self):
        self.photo = tk.PhotoImage(file=self.file)
        self.photo = self.photo.subsample(3, 5)
        self.canvas.itemconfig(self.img, image=self.photo)
        self.fileLabel.config(text=self.file)
        self.classText.delete('1.0', tk.END)
        self.observationText.delete('1.0', tk.END)
        self.fIndex += 1

    def SaveExit(self):
        #This writes a new CSV using the data from the original CSV
        print("Exiting App")
        with open(self.csvFile) as csv_file:
            with open(self.newCSVFile, "w+") as new_csv_file:
                csvReader = csv.reader(csv_file, delimiter=',')
                csvWriter = csv.writer(new_csv_file, delimiter=',')
                lineCount = 0
                for row in csvReader:
                    #This adds in our new data
                    if lineCount in self.saveData:
                        csvWriter.writerow(self.saveData[lineCount])
                    else:
                        csvWriter.writerow(row)
                    lineCount += 1

        # Overwrite our file
        os.remove(self.csvFile)
        os.rename(self.newCSVFile, self.csvFile)
        sys.exit()

    def ReadAsCSV(self):
        return ""
    
    def FocusNext(self, event):
        event.widget.tk_focusNext().focus()
        return("break")
    
    def FocusPrev(self, event):
        self.observationText.focus_set()
        return("break")


if __name__ == "__main__":
    gui = mainGUI()
