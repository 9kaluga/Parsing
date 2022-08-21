import requests
from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent
import xlsxwriter


ua = UserAgent()
headers = {"User-Agent": ua.random}


def download(url):
    response = requests.get(url, stream=True)
    r = open('C:\\Users\\KalugaOne\\Desktop\\images\\' + url.split('/')[-1],'wb')
    for value in response.iter_content(1024*1024):
        r.write(value)
    r.close()
    

def get_url():
    for num in range(1,8):
        url = f"https://scrapingclub.com/exercise/list_basic/?page={num}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")
        
        for i in data:
            url_card = "https://scrapingclub.com" + i.find("a").get("href")
            yield url_card
            
            
def array():
    for url_card in get_url():
        response = requests.get(url_card, headers=headers)
        
        sleep(1)
        
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("div", class_="card mt-4 my-4")
        name = data.find("h3", class_="card-title").text
        price = data.find("h4").text
        text = data.find("p", class_="card-text").text
        url_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top img-fluid").get("src")

        download(url_img)

        yield name, price, url_img, url_card, text


def write(parametr):
    book = xlsxwriter.Workbook(r'C:\Users\KalugaOne\Desktop\book.xlsx')
    page = book.add_worksheet('Товар')

    row = 0
    column = 0

    page.set_column('A:A', 24)
    page.set_column('B:B', 7)
    page.set_column('C:C', 45)
    page.set_column('D:D', 55)
    page.set_column('E:E', 180)

    for i in parametr():
        page.write(row, column, i[0])
        page.write(row, column+1, i[1])
        page.write(row, column+2, i[2])
        page.write(row, column+3, i[3])
        page.write(row, column+4, i[4])
        row+=1

    book.close()


write(array)

