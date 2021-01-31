from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mbox

import sqlite3

con = sqlite3.connect("database.sqlite")
c = con.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS personel
                 (personel_id INTEGER PRIMARY KEY,
                  ad varchar(20) NOT NULL,
                  soyad varchar(20) NOT NULL,
                  no integer NOT NULL)''')
def phone_format(n):                                                                                                                                  
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1] 

class personelislemleri:
    
    def __init__(self,ad,soyad,no):
        self.personeladi = ad
        self.personelsoyadi = soyad
        self.personelno = no
      
    def PersonelEkle(self):
        evet = mbox.askyesno(title="PERSONEL ISLEMLERI",message=""+self.personeladi+" "+self.personelsoyadi+" Kimlikli yeni personel eklemek istediğinize eminmisiniz ?")
        if evet:
            data_person_name = [(self.personeladi,self.personelsoyadi,self.personelno)]
            c.executemany('INSERT INTO personel(ad, soyad,no) VALUES (?,?,?)', data_person_name)
            #print("Personel Adı:",self.personeladi,"Personel Soyadı:",self.personelsoyadi,"Personel Numarasi:",self.personelno)
            con.commit()
     
     
    def PersonelSil(self):
        evet = mbox.askyesno(title="PERSONEL ISLEMLERI",message=""+self.personeladi+" "+self.personelsoyadi+" Kimlikli personeli silmek istediğinize eminmisiniz ?")
        if evet:
            item = table.selection()[0]
            table.delete(item)
            #print(self.personeladi)
            data_person_name = [(self.personeladi,self.personelsoyadi,self.personelno)]
            c.executemany('DELETE FROM personel WHERE ad=? and soyad=? and no=?', data_person_name)
            con.commit()

    def PersonelListeGuncelle(self):
        c.execute("SELECT * FROM personel")
        rows = c.fetchall()
        table.delete(*table.get_children())
        for row in rows:
            #print(row) 
            table.insert("",END,values=row)

def treeViewCiftTik(event):
    
    rowid = table.identify_row(event.y)
    item = table.item(table.focus())

    #print(item["values"][0])

    personeladi.delete(0,END)
    personeladi.insert(0,item["values"][1])
    personelsoyadi.delete(0,END)
    personelsoyadi.insert(0,item["values"][2])
    numarasi.delete(0,END)
    numarasi.insert(0,item["values"][3])

def personelekle():
    if personeladi.get() != "" and personelsoyadi.get() != "" and numarasi.get() != "":
        personelislemi = personelislemleri(personeladi.get(),personelsoyadi.get(),phone_format(numarasi.get()))
        personelislemi.PersonelEkle()
        personelislemi.PersonelListeGuncelle()
    else:
        mbox.showerror("PERSONEL ISLEMLERI","Lütfen bilgileri doldurunuz.")
        
  

def personelsil():
    if personeladi.get() != "" and personelsoyadi.get() != "" and numarasi.get() != "":
        personelislemi = personelislemleri(personeladi.get(),personelsoyadi.get(),numarasi.get())
        personelislemi.PersonelSil()
        personelislemi.PersonelListeGuncelle()
    else:
        mbox.showerror("PERSONEL ISLEMLERI","Lütfen bilgileri doldurunuz veya kişinin üzerine çift tıklayarak seçiniz.")
    


pencere = Tk()
pencere.iconbitmap(r'ico/database.ico')
frame = Frame(pencere)
frame2 = Frame(pencere)
pencere.title("PERSONEL ISLEMLERI")

pencere.resizable(False, False) 


window_height = 400
window_width = 440

screen_width = pencere.winfo_screenwidth()
screen_height = pencere.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

pencere.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


label1 = Label(frame,text="Personel Adı",padx=20,pady=20)
label2 = Label(frame,text="Personel SoyAdı")
label3 = Label(frame,text="Personel Telefon Numarası",padx=20,pady=20)
labelbos1 = Label(frame,text="",padx=10,pady=10)
labelbos2 = Label(frame,text="",padx=10,pady=10)
personeladi = Entry(frame)
personelsoyadi = Entry(frame)
numarasi = Entry(frame)

ekle = Button(frame,text="Ekle",width=15,bg="green",fg="white",pady=5,command=personelekle)
sil = Button(frame,text="Sil",width=15,bg="red",fg="white",pady=5,command=personelsil)


col = ("id","Ad","SoyAd","Telefon")

global table
table = ttk.Treeview(frame2,height=5,show="headings",columns=col)
table.bind('<Double-1>', treeViewCiftTik)

table.column("id",width=50,anchor=CENTER)
table.column("Ad",width=130,anchor=CENTER)
table.column("SoyAd",width=130,anchor=CENTER)
table.column("Telefon",width=140,anchor=CENTER)
table.heading("id",text="id")

table.heading("Ad",text="Ad")
table.heading("SoyAd",text="SoyAd")
table.heading("Telefon",text="Telefon")

c.execute("SELECT * FROM personel")
rows = c.fetchall()
for row in rows:
    #print(row)
    table.insert("",END,values=row)


      


label1.grid(row=0)
label2.grid(row=1)
label3.grid(row=2)
labelbos1.grid(row=3)
labelbos2.grid(row=4)
personeladi.grid(row=0,column=1)
personelsoyadi.grid(row=1,column=1)
numarasi.grid(row=2,column=1)
ekle.grid(row=3,column=1)
sil.grid(row=4,column=1)


frame.grid(row=1)
frame2.grid(row=0,column=0)
#frame2.grid_forget() GİZLEME
table.grid(row=0)
pencere.mainloop();


