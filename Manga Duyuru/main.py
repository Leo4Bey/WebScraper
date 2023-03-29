from bs4 import BeautifulSoup
from config import *
import requests
import time
import pymongo

from discord_webhook import DiscordWebhook, DiscordEmbed

client = pymongo.MongoClient(url)
db = client.adumanga



def bildirim():
    r = requests.get("https://adumanga.com/manga/?order=update")
    soup = BeautifulSoup(r.content, "html")
    mangalar = soup.find("div",attrs={"class":"bs"})
    manga_link = mangalar.a.get("href")
    manga_title = mangalar.a.get("title")
    manga_resim = mangalar.img.get("src")
    manga_bolum = soup.find("div",attrs={"class":"epxs"}).text
    hex = {"manga_link": f"{manga_link}"}
    hex2 = {"manga_bolum": f"{manga_bolum}"}
    hex3 = {"leo": "leo"}
    hex4 = {"$set": {"manga_link": f"{manga_link}"}}
    hex5 = {"$set": {"manga_bolum": f"{manga_bolum}"}}

    kontrol = db.manga.count_documents(hex) and db.manga.count_documents(hex2) == 1
    
    if kontrol == False:
        webhook = DiscordWebhook(url=webhook_url, content="<@&{bildirim_rol_id}>")
        embed = DiscordEmbed(
                title = "Yeni Manga Geldi!",
                description = f"Manga adı: {manga_title}\nBölüm: {manga_bolum}\n\n[Tıklayıp mangayı okumaya başla]({manga_link})",
            )
        embed.set_thumbnail(url=f"{manga_resim}")
        webhook.add_embed(embed)
        resp = webhook.execute()
        print("Yeni manga gelmiş")
        db.manga.update_one(hex3, hex4)
        db.manga.update_one(hex3, hex5)
    elif kontrol == True:
        return
               

while True:
    bildirim()
    time.sleep(10)
