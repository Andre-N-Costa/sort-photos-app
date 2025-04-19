import os
import os.path
import time

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox, QFileDialog

class Widget(QWidget):

    def __init__(self):
        
        super().__init__()

        """
        Created all buttons and labels for main window
        """

        self.repeats = {}

        self.months = {
        'Jan':'01',
        'Feb':'02',
        'Mar':'03',
        'Apr':'04',
        'May':'05',
        'Jun':'06',
        'Jul':'07',
        'Aug':'08',
        'Sep':'09',
        'Oct':'10',
        'Nov':'11',
        'Dec':'12'
        }

        self.folder_from_path = ""
        self.folder_to_path = ""

        self.setWindowTitle("Melhor organizador de fotos do mundo")

        label1 = QLabel("Pasta em que estão as fotos:")

        self.current_from_path = QLabel("")

        button1 = QPushButton("Escolher")
        button1.clicked.connect(self.addFromPath)

        label2 = QLabel("Pasta para irem as fotos organizadas:")

        self.current_to_path = QLabel("")

        button2 = QPushButton("Escolher")
        button2.clicked.connect(self.addToPath)

        sortButton = QPushButton("Hora de organizar")
        sortButton.clicked.connect(self.sortFilesFromButton)

        menu_layout1 = QHBoxLayout()
        menu_layout1.addWidget(label1)
        menu_layout1.addWidget(button1)
        menu_layout1.addWidget(self.current_from_path)


        menu_layout2 = QHBoxLayout()
        menu_layout2.addWidget(label2)
        menu_layout2.addWidget(button2)
        menu_layout2.addWidget(self.current_to_path)
        
        menu_layout = QVBoxLayout()
        menu_layout.addLayout(menu_layout1)
        menu_layout.addLayout(menu_layout2)
        menu_layout.addWidget(sortButton)
        

        self.setLayout(menu_layout)

    """
    Choose path for photos origin
    """
    def addFromPath(self):
        self.folder_from_path = QFileDialog.getExistingDirectory(self, "Escolhe a pasta em que estão as fotos")
        self.current_from_path.setText(self.folder_from_path)

    """
    Choose path for photos organization folder
    """
    def addToPath(self):
        self.folder_to_path = QFileDialog.getExistingDirectory(self, "Escolhe a pasta onde queres guardar as fotos")
        self.current_to_path.setText(self.folder_to_path)

    """
    Sort photos in organization folder
    """
    def sortFilesFromButton(self):

        # Check if all required paths exist
        if self.folder_from_path == "" or self.folder_to_path == "":
            ret = QMessageBox.warning(self,"!!!",f"Faltou escolheres uma das pastas pá", QMessageBox.Ok)
            if ret == QMessageBox.Ok:
                return
        
        # Check with user if paths are correct
        ret = QMessageBox.question(self,"Volta a dar uma vista de olhos",f"Está tudo em ordem?\n\nPasta onde estão as fotos:\n{self.folder_from_path}\n\nPasta para onde serão guardadas as fotos:\n{self.folder_to_path}\n\nAs fotos serão apagadas da pasta original por isso deves guardar um backup.", QMessageBox.Ok, QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
                
            pathItems = os.listdir(self.folder_from_path)

            # Go through all files and move them with new name according to modification date
            for item in pathItems:
                itemPath = os.path.join(self.folder_from_path,item)
                if os.path.isfile(itemPath):
                    modified_time = os.path.getmtime(itemPath)
                    readable_time = time.ctime(modified_time)
                    year = readable_time[-4:]
                    month = self.months[readable_time[4:7].lstrip()]
                    day = readable_time[8:10].lstrip()
                    if int(day) < 10:
                        day = "0" + day
                    hour = readable_time[11:19]

                    #New name consists of modification name"-"hour"h"minute"m"second"s"
                    name = day + "-" + hour[0:2] + "h" + hour[3:5] + "m" + hour[6:8] + "s"

                    #Check which folders it needs to create
                    if not os.path.exists(os.path.join(self.folder_to_path,year)):
                        os.makedirs(os.path.join(self.folder_to_path,year))

                    if not os.path.exists(os.path.join(self.folder_to_path,year,year + "-" + month)):
                        os.makedirs(os.path.join(self.folder_to_path,year,year + "-" + month))
                    try:
                        fileNewPath = os.path.join(self.folder_to_path,year,year + "-" + month,name + "." + item.split('.')[1])
                        os.rename(itemPath,fileNewPath)
                    except FileExistsError:
                        if fileNewPath not in self.repeats:
                            self.repeats[fileNewPath] = 1
                        else:
                            self.repeats[fileNewPath]+=1
                        os.rename(itemPath,os.path.join(self.folder_to_path,year,year + "-" + month,name + "-" + str(self.repeats[fileNewPath]) +  "." + item.split('.')[1] ))
                else:
                    #Get inside folders to move nested files
                    self.sortFilesRecursive(itemPath,self.folder_to_path)

            ret = QMessageBox.information(self,":3",f"Tá feito", QMessageBox.Ok)
            #Open in folder explorer 
            os.startfile(self.folder_to_path)

    def sortFilesRecursive(self,input,output):
        pathItems = os.listdir(input)

        for item in pathItems:
            itemPath = os.path.join(input,item)
            if os.path.isfile(itemPath):
                modified_time = os.path.getmtime(itemPath)
                readable_time = time.ctime(modified_time)
                year = readable_time[-4:]
                month = self.months[readable_time[4:7].lstrip()]
                day = readable_time[8:10].lstrip()
                if int(day) < 10:
                    day = "0" + day
                hour = readable_time[11:19]
                name = day + "-" + hour[0:2] + "h" + hour[3:5] + "m" + hour[6:8] + "s"

                if not os.path.exists(os.path.join(output,year)):
                    os.makedirs(os.path.join(output,year))

                if not os.path.exists(os.path.join(output,year,year + "-" + month)):
                    os.makedirs(os.path.join(output,year,year + "-" + month))
                try:
                    fileNewPath = os.path.join(self.folder_to_path,year,year + "-" + month,name + "." + item.split('.')[1])
                    os.rename(itemPath,fileNewPath)
                except FileExistsError:
                    if fileNewPath not in self.repeats:
                        self.repeats[fileNewPath] = 1
                    else:
                        self.repeats[fileNewPath]+=1
                    os.rename(itemPath,os.path.join(self.folder_to_path,year,year + "-" + month,name + "-" + str(self.repeats[fileNewPath]) +  "." + item.split('.')[1] ))
            else:
                self.sortFilesRecursive(itemPath,output)