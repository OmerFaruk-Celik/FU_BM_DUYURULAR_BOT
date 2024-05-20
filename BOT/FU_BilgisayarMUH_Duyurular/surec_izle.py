import psutil
import time
import os

while True:
        time.sleep(10)
        with open("./myPid","r") as dosya:
                pid=int(dosya.read())
                try:
                        pid=int(pid)
                except:
                        pid=0
        if not psutil.pid_exists(pid):
                os.system("/usr/bin/python3 ~/Documents/BOT/FU_BilgisayarMUH_Duyurular/duyurularBot.py &")

        with open("./myPid2","r") as dosya2:
                pid2=int(dosya2.read())

                try:
                        pid2=int(pid2)
                except:
                        pid2=0
        if not psutil.pid_exists(pid2):


                os.system("/usr/bin/python3 ~/Documents/BOT/FU_BilgisayarMUH_Duyurular/chatId.py &")

        time.sleep(300)
