from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from time import sleep
import urllib3
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
with open("./myPid","w") as dosya:
                dosya.write(str(os.getpid()))



def state():
        with open("./chatID","r") as dosya:
                r=dosya.read();
        return r=="True"



def getID():
        with open("./chatID","r") as dosya:
                r=dosya.read()
        r=r.split()
        return r[1:]


def duzenle(mesaj):
    duzenlenmis_mesaj = " ".join(mesaj.split())
    duzenlenmis_mesaj = duzenlenmis_mesaj.replace("\r", "")
    return duzenlenmis_mesaj




def zaman():
   
    # Şu anki tarihi ve saati al
    anlik_zaman = datetime.now()
    # Yıl, ay, gün, saat ve dakika bilgilerini al
    yil = anlik_zaman.year
    ay = anlik_zaman.month
    gun = anlik_zaman.day
    return str(gun)+str(ay)+str(yil)

def link(soup):
    linkler=[]
    for link in soup.find_all("a"):
        href=link.get("href")
        if href != None:
                if href.startswith('https://bilgisayarmf.firat.edu.tr/'):
                    linkler.append(href)
                    #print(linkler)
    return linkler

with open("token.txt","r") as f:
    bot_token=f.read()  
def send(message):

    
    bot = Bot(token=bot_token)
    
    for chat_id in getID():
        try:
                bot.send_message(chat_id=chat_id, text=message)
        except:
                continue
        sleep(0.5)
def duyurular():
    duyuru_tarihleri=[]
    duyuru_metinleri=[]
    duyuru_basliklari=[]
    duyuru_linkleri=[]
    main_url = 'https://bilgisayarmf.firat.edu.tr/tr/announcements-all'
    
    #internetten sayfayı indir
    response=requests.get(main_url,verify=False)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        urls=link(soup)
        
        for url in urls:
            response = requests.get(url,verify=False)
            if response.status_code == 200:
            
                soup = BeautifulSoup(response.text, 'html.parser')
                title= soup.find('div', {'class': 'new-section-detail-title'})
                duyurular_etiketi = soup.find_all('div', {'class': 'index-content-info'})
                date = soup.find('div', {'class': 'new-section-detail-date'})
                if title != None:
                    duyuru_linki="\n "+url
                    # Duyurunun URL'sini al
                   
         
                        
                    for duyuru in duyurular_etiketi:
                        duyuru_basliklari.append(duzenle(title.get_text()))
                        a0=duzenle(date.get_text().replace(".",""))
                        a1=a0.split(" ")
                        y2=a1[0]+a1[1]+a1[2]
                        duyuru_tarihleri.append(y2)
                        duyuru_metinleri.append(duzenle(duyuru.get_text()))
                        metin = duzenle(duyuru.get_text())
                        img=duyuru.find("img")
                        if img!=None:
                                adres=img.get("src")
                                if not adres.startswith('https://bilgisayarmf.firat.edu.tr/'):
                                        adres ='https://bilgisayarmf.firat.edu.tr/' + adres.lstrip('/')
                        
                                adres="\n "+adres
                        
                                if not verilerde_mevcut(adres):
                                        send("RESİM DOSYASI ALGILANDI\n"+adres)
                        
                                        kaydet(ascii_donustur(adres))
                        
                        
                        
                        
                        if 'tıkla' in duyuru.text.lower() or 'tıklayınız' in duyuru.text.lower() or 'TIKLAYINIZ' in duyuru.text or 'tiklayiniz' in duyuru.text.lower():
                                a_tag=duyuru.find('a')
                                href = a_tag.get('href')
                                if href:
                                        href=quote(href.encode('utf-8'))
                                        if href and not href.startswith('https://bilgisayarmf.firat.edu.tr/'):
                                                href = 'https://bilgisayarmf.firat.edu.tr/' + href.lstrip('/')
                                        duyuru_linki = href
                        
                                        duyuru_linki = "\n " + duyuru_linki
                                        #print(duyuru_linki)

         
                        
                        duyuru_linkleri.append(duyuru_linki)
                                  
  
                
            else:
                continue
        
    return duyuru_tarihleri,duyuru_metinleri,duyuru_basliklari,duyuru_linkleri


def ascii_donustur(karekterler):
    toplam=0
    ascii_basliklar=[]
    
    for indis,char in enumerate(karekterler):
        ascii_karsiligi=ord(char)
        toplam+=int(ascii_karsiligi/(indis+1))
    ascii_basliklar.append(int(toplam))
    #print(toplam)
    toplam=0
        
    return ascii_basliklar[0]
            
    
    

def kaydet(duyuru_baslik):
    # Var olan dosyayı açın veya yoksa oluşturun
    dosya_yolu = '/home/ubuntu/Documents/BOT/FU_BilgisayarMUH_Duyurular/duyuruBasliklar.csv'

    try:
        # Dosyayı 'a' (append) modunda açın
        duyuru_df = pd.read_csv(dosya_yolu)
    except FileNotFoundError:
        # Dosya yoksa, yeni bir veri çerçevesi oluşturun
        duyuru_df = pd.DataFrame()

    # Yeni verileri ekleyin
    yeni_veriler = {
        'Basliklar': duyuru_baslik
    }
    yeni_df = pd.DataFrame(yeni_veriler, index=[0])

    # Var olan veri çerçevesine yeni verileri ekleyin
    duyuru_df = pd.concat([duyuru_df, yeni_df], ignore_index=True)

    # Güncellenmiş veri çerçevesini dosyaya kaydedin
    duyuru_df.to_csv(dosya_yolu, index=False)

    #print(f"{dosya_yolu} adlı dosyaya veri eklendi.")

# Örnek kullanım

def verilerde_mevcut(duyuru_baslikk):
    son=False
    
    dosya_yolu = '/home/ubuntu/Documents/BOT/FU_BilgisayarMUH_Duyurular/duyuruBasliklar.csv'
    veriler=pd.read_csv(dosya_yolu)
    
    for i in list(veriler.Basliklar):
        son=str(int(i))==str(ascii_donustur(duyuru_baslikk))

        #print(str(ascii_donustur(duyuru_baslikk)))


        if son:
            break
            

    return son
     

def filtrele():
    state=False

    duyuru_tarihleri,duyuru_metinleri,duyuru_basliklari,duyuru_linkleri=duyurular()

    if duyuru_tarihleri ==False:
        state=False
        return False
    else:
        state=True
    
    #print("yazdırıyorum\n")
    
    
    
    for indis,duyuru_bass in enumerate(duyuru_basliklari):
  
        
        #if duyuru_tarihi==zaman():
            #print(duyuru_basliklari[indis])

            #print(not verilerde_mevcut(duyuru_basliklari[indis]))
            if not verilerde_mevcut(duyuru_bass):
                #print(duyuru_linkleri[indis])
                send(duyuru_metinleri[indis]+duyuru_linkleri[indis])
                kaydet(ascii_donustur(duyuru_bass))
    return state

     
            
        
        
    
while(True):

        cevap=filtrele()
                
        sleep(300)
