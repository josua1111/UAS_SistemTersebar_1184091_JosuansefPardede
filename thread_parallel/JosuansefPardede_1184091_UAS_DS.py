"""

@author: Josuansef Pardede (1184091) UAS Sistem Tersebar
"""
from threading import Thread, currentThread, Lock, RLock, Event
from queue import Queue
import os
import requests

queue = Queue()
event = Event()

class Josuansef1184091_Consumer(Thread):
        
    def __init__(self,name,thread_number,filenya):
       Thread.__init__(self)    
       self.threadLock = Lock()
       self.name = name
       self.thread_number = thread_number
       self.filenya=os.path.join(os.path.dirname(__file__), filenya)
       self.event = event

    def run(self):
        print("\n"+str(self.thread_number)+". ---> " + self.name + "jalan")
        print('class Josuansef1184091_Consumer eksekusi event.wait lalu clear. Jalankan fungsi Read File')
        self.event.wait()
        self.threadLock.acquire()
        print('read file : '+self.filenya)
        self.readfile()
        self.event.wait()
        self.threadLock.release()
        print("\n"+str(self.thread_number)+". ---> " + currentThread().getName() + "Read file telah selesai")
        print ("eksekusi event clear")
        self.event.clear()
   
    def readfile(self):
       q=queue.get()
       f = open(self.filenya, "r+")
       print("Isi Filenya apaan yaa : "+f.read())
       print("Sudah selesai baca isi file nya nih, jalanin queue task done \n")
       queue.task_done()

class Josuansef1184091_Producer(Thread):
      
   def __init__(self, name,thread_number, alpha, beta, filenya):
       Thread.__init__(self)
       self.threadLock = Lock()
       self.event = event
       self.rlock = RLock()
       self.name = name
       self.alpha=alpha
       self.beta=beta
       self.filenya=os.path.join(os.path.dirname(__file__), filenya)
       self.thread_number = thread_number

   def run(self):

       print("\n"+str(self.thread_number)+". ---> " + self.name + "jalan")
       self.threadLock.acquire()
       print("threeadlock acquire utama")
       self.count()
       self.event.set()
       print('class Josuansef1184091_Producer sudah selesai melakukan event set')
       self.threadLock.release()
       print("\n"+str(self.thread_number)+". ---> " + currentThread().getName() + "telah selesai")
       
   def apijosua(self):
       with self.rlock:
           print('akses webservices api seperti berikut')
           url='https://api-lk21.herokuapp.com/comingsoon'
           response = requests.get(url)
           html=response.json()
           queue.put(html)
           self.createfile(html)

   def count(self):
       with self.rlock:
           print('rlock count')
           self.apijosua()   
 
   def createfile(self, konten):
       print('membuat file baru : '+ self.filenya)
       f = open(self.filenya, "x")
       f.write(str(konten))
       f.close()
       print('File telah di create,eksekusi event set')

