import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import os
from pymongo.mongo_client import MongoClient


def imageScrapingProcess(searchString):
    uri = "mongodb+srv://TheSilentCoders:thesilentcoders@cluster0.x1ymrhc.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    save_dir = "image/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

    query = searchString
    response = requests.get(f"https://www.google.com/search?rlz=1C1ONGR_enIN983IN983&sxsrf=AB5stBgS7bWjywN5aTKWFkP68Qc2hma9Ag:1688727475799&q={query}&tbm=isch&sa=X&ved=2ahUKEwiIz8SKuPz_AhXiT2wGHS78AGAQ0pQJegQIEhAB&biw=1536&bih=714&dpr=1.25")

    soup = BeautifulSoup(response.content, 'html.parser')

    images_tag = soup.find_all("img")

    len(images_tag)
    img_data_mongo = []
    img_url = []

    del images_tag[0]

    for i in images_tag:
        image_url = i['src']
        print(image_url)
        image_data = requests.get(image_url).content
        mydict = {"index":image_url, "image": image_data}
        mydictresultpage = {"imgurl":image_url, "index": images_tag.index(i)}
        img_url.append(mydictresultpage)
        img_data_mongo.append(mydict)
        with open(os.path.join(save_dir, f"{query}_{images_tag.index(i)}.jpg"), "wb") as f:
            f.write(image_data)

    db = client['image_scrapper']

    coll_image = db['image_scrapper']

    coll_image.insert_many(img_data_mongo)

    return img_url
