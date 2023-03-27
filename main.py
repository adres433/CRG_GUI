import os
import tkinter as tk
from ftplib import FTP

if __name__ != '__main__':
    pass
else:
    class MainWindow:

        ## EVENT FOR MOVE WINDOW
        def moveWindow(self, event):

            x, y = self.root.winfo_pointerxy()  ## pozycja kursora na ekranie
            a = self.root.winfo_rootx()  ## pozycja rogu okna na ekranie
            b = self.root.winfo_rooty()  ## pozycja rogu okna na ekranie

            moveX = self.curPosX - x
            moveY = self.curPosY - y

            self.root.geometry(f"+{a - moveX}+{b - moveY}")
            self.curPosX, self.curPosY = self.root.winfo_pointerxy()

        def grabPos(self, event):

            self.curPosX, self.curPosY = self.root.winfo_pointerxy()

        def genReaders(self):
            name = self.nameEntry.get()
            text = self.clineArea.get(float(1), tk.END).split("\n")  ## opuszczamy ostatni pusty element
            data = []

            for i, line in enumerate(text):
                tempLine = line.split(" ")
                if len(tempLine) < 5:
                    break
                tempLine[0] = f"\n\n[Reader]\nlabel={name}_{str(i+1)}\n"
                tempLine[1] = f"device={tempLine[1]}\n"
                tempLine[2] = f"port={tempLine[2]}\n"
                tempLine[3] = f"user={tempLine[3]}\n"
                tempLine[4] = f"password={tempLine[4]}\n"
                for j in self.configData[0:-2]:
                    tempLine.append(j)
                data.append(tempLine)

            if len(data) >= 1:

                ftpAddr = self.configData[-2].split('=')[1].replace("\n", "")
                ftp = FTP(host=ftpAddr)
                ftp.login(user='root', passwd=self.configData[-1].split('=')[1])
                ftp.cwd("usr/keys/")

                ## download old file and save backup from FTP
                bkpFile = open("oscam.server.bak", 'wb')
                ftp.retrbinary('RETR ' + "oscam.server", bkpFile.write)
                bkpFile.close()

                ## read local backup
                file = open("oscam.server.bak", "r")
                tempData = file.read()
                tempData += "\n"
                file.close()

                ## save new file
                file = open("output_reader.txt", "w")
                for i in data:
                    tempData += "".join(i)
                file.write(tempData)
                file.close()

                ## upload new file to FTP
                with open("output_reader.txt", 'rb') as file:
                    ftp.storbinary('STOR '+"oscam.server", file, callback=self.root.destroy())
                    ftp.quit()

            return

        def cfgFileModify(self, nData: str = ""):

            file = open(f"{self.cfgFile}\\reader.cfg", "r+")
            data = ""

            if len(nData) < 1:
                data = file.readlines()
            else:
                file.write(nData)

            file.close()
            return data

        def saveConfig(self):
            cfgReader = self.readerArea.get(float(1), tk.END)[0:-1]
            if cfgReader[-1] != '\n':
                cfgReader += "\n"
            cfgReader += f"host={self.hostEntry.get()}"
            if self.hostEntry.get().find("\n") == -1:
                cfgReader += "\n"
            cfgReader += f"passHost={self.passEntry.get()}"
            self.cfgFileModify(cfgReader)
            self.configData = cfgReader

        def closeApp(self):
            self.root.destroy()

        def __init__(self, bgColor: str, titleColor: str, width: int, height: int):

            self.winWidth = width
            self.winHeight = height
            self.curPosX = 0
            self.curPosY = 0
            self.winBgColor = bgColor
            self.winTitleColor = titleColor
            self.cfgFile = os.getenv("APPDATA")+"\\CRG"
            self.configData = self.cfgFileModify()


            self.root = tk.Tk()
            self.root.title("CcamReaderGUI")
            self.root.eval("tk::PlaceWindow . center")
            self.root.geometry(f"{self.winWidth}x{self.winHeight}")
            self.root.config(bg=self.winBgColor)
            ## window grid config
            self.root.columnconfigure(index=0, weight=1)
            self.root.columnconfigure(index=1, weight=0)
            self.root.columnconfigure(index=2, weight=2)
            self.root.overrideredirect(True)

            ## TITLE BAR
            self.titleFrame = tk.Frame(self.root, bg=self.winTitleColor)
            self.titleFrame.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
            self.titleFrame.columnconfigure(index=0, weight=0)
            self.titleFrame.columnconfigure(index=1, weight=1)
            self.titleFrame.bind("<B1-Motion>", self.moveWindow)
            self.titleFrame.bind("<Button-1>", self.grabPos)

            self.titleLabel = tk.Label(
                self.titleFrame,
                bg=self.winTitleColor,
                text="CcamReaderGUI",
                font=("TkMenuFont", 10, 'bold'),
                height=2)
            self.crossBtn = tk.Button(
                self.titleFrame,
                bg=self.winTitleColor,
                bd=0,
                activebackground=self.winTitleColor,
                text="X",
                font=("TkMenuFont", 12, 'bold'),
                command=self.closeApp)

            self.titleLabel.bind("<B1-Motion>", self.moveWindow)
            self.titleLabel.bind("<Button-1>", self.grabPos)

            self.titleLabel.grid(row=0, column=0, sticky=tk.NS)
            self.crossBtn.grid(row=0, column=1, sticky=tk.E)

            ## END TITLE BAR

            ## CONFIG CONTENT
            self.cfgFrame = tk.Frame(self.root, bg=self.winBgColor)
            self.conCfgLabel = tk.Label(self.cfgFrame, text="Wprowadź wspólną konfiguracje czytników:", bg=self.winBgColor)
            self.readerArea = tk.Text(self.cfgFrame, width=55, height=10, font=("TkMenuFont", 10))
            self.hostCfgLabel = tk.Label(self.cfgFrame, text="Adres FTP dekodera:", bg=self.winBgColor)
            self.hostEntry= tk.Entry(self.cfgFrame, width=10, font=("TkMenuFont", 10))
            self.passCfgLabel = tk.Label(self.cfgFrame, text="Hasło FTP:", bg=self.winBgColor)
            self.passEntry = tk.Entry(self.cfgFrame, width=10, font=("TkMenuFont", 10))

            for i in self.configData[0:-2]:
                self.readerArea.insert(tk.END, i)

            self.hostEntry.insert(0, self.configData[-2:-1][0].split("=")[1])
            self.passEntry.insert(0, self.configData[-1:][0].split("=")[1])

            self.cfgFrame.grid(row=2, column=1, columnspan=3, sticky=tk.NSEW)
            self.conCfgLabel.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=50, pady=15)
            self.readerArea.grid(row=1, column=1, sticky=tk.NSEW, padx=50, pady=10)
            self.hostCfgLabel.grid(row=2, column=1, sticky=tk.W, padx=0, pady=2)
            self.hostEntry.grid(row=3, column=1, columnspan=2, sticky=tk.EW, padx=0, pady=2)
            self.passCfgLabel.grid(row=4, column=1, sticky=tk.W, padx=0, pady=2)
            self.passEntry.grid(row=5, column=1, columnspan=2, sticky=tk.EW, padx=0, pady=2)

            ## END CONFIG CONTENT

            ## GENERATOR CONTENT
            self.genFrame = tk.Frame(self.root, bg=self.winBgColor)
            self.contentLabel = tk.Label(self.genFrame, text="Wprowadź C line [C: HOST PORT USER PASSWORD]:",
                                         bg=self.winBgColor)
            self.clineArea = tk.Text(self.genFrame, width=55, height=12, font=("TkMenuFont", 10))
            self.nameLabel = tk.Label(self.genFrame, text="Nazwa czytników:", bg=self.winBgColor)
            self.nameEntry = tk.Entry(self.genFrame, width=55, font=("TkMenuFont", 10))

            self.genFrame.grid(row=2, column=1, columnspan=3, sticky=tk.NSEW)
            self.contentLabel.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=50, pady=15)
            self.clineArea.grid(row=1, column=1, sticky=tk.NSEW, padx=50, pady=10)
            self.nameLabel.grid(row=2, column=1, sticky=tk.W, padx=50, pady=10)
            self.nameEntry.grid(row=3, column=1, sticky=tk.NSEW, padx=50)
            ## END GENERATOR CONTENT

            ## BUTTONS
            self.btnsFrame = tk.Frame(self.root, bg=self.winBgColor)
            self.genBtn = tk.Button(self.btnsFrame, text="GENERUJ", command=self.genReaders, bg=self.winBgColor,
                               activebackground=self.winBgColor)
            self.clsBtn = tk.Button(self.btnsFrame, text="ZAMKNIJ", command=self.closeApp, bg=self.winBgColor,
                               activebackground=self.winBgColor)
            self.cfgBtn = tk.Button(self.btnsFrame, text="USTAWIENIA", command=self.showCfgWindow, bg=self.winBgColor,
                               activebackground=self.winBgColor)

            self.btnsFrame.grid(row=3, column=1, padx=50, pady=25)
            self.genBtn.grid(row=0, column=0, padx=25, sticky=tk.W)
            self.cfgBtn.grid(row=0, column=1, padx=25, sticky=tk.EW)
            self.clsBtn.grid(row=0, column=2, padx=25, sticky=tk.E)
            ## END BUTTONS

            if not os.path.exists(self.cfgFile):
                os.mkdir(self.cfgFile)
                file = open(f"{self.cfgFile}\\reader.cfg", "w")
                file.write("ustawienie=wartosc\n" * 10)
                file.close()
            if not os.path.exists("output_reader.txt"):
                file = open("output_reader.txt", "w")
                file.write("")
                file.close()
            if not os.path.exists("oscam.server.bak"):
                file = open("oscam.server.bak", "w")
                file.write("")
                file.close()
            ##main loop of GUI
            self.root.mainloop()

        def showGenWindow(self):
            self.genFrame.tkraise()
            self.genBtn.config(command=self.genReaders)
            self.cfgBtn.config(command=self.showCfgWindow, text="USTAWIENIA")

        def showCfgWindow(self):
            self.cfgFrame.tkraise()
            self.genBtn.config(command=self.showGenWindow)
            self.cfgBtn.config(command=self.saveConfig, text="ZAPISZ")


    windowApp = MainWindow("#b0b0ae", "#8f8f8d", 500, 500)