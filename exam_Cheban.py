import sqlite3
import requests
from bs4 import BeautifulSoup
import lxml


connection = sqlite3.connect("DB.sl3", 5)
cur = connection.cursor()

# cur.execute("CREATE TABLE discount_table (title TEXT, price TEXT);")

url_first = 'https://hard.rozetka.com.ua/monitors/c80089/'
page = int(input('Input page '))

class Parsing():
    def __init__(self, user='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                 session=requests.Session()):
        self.user = user
        self.headers = {'user-agent': self.user}
        self.session = session

    def pars(self):
        for j in range(1, page + 1):
            url = f'{url_first}page={j}'
            response = self.session.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            all_product = soup.find('ul', class_="catalog-grid ng-star-inserted")
            product_list = all_product.find_all('div', class_='goods-tile__inner')

            for i in range(len(product_list)):
                title = product_list[i].find('a', class_='goods-tile__heading ng-star-inserted').text
                try:
                    discount = product_list[i].find('p', class_='ng-star-inserted').text
                    with open('my_product.txt', 'a', encoding='UTF-8') as file:
                        file.write(f"{title}    Price: {discount}'\n'")
                    cur.execute(f"INSERT INTO discount_table (title, price) VALUES ('{title}', '{discount}') ;")
                    cur.execute(f"SELECT * FROM discount_table;")

                except AttributeError:
                    pass

rozetka = Parsing()
rozetka.pars()
# cur.execute("DROP TABLE discount_table;")


connection.commit()
res = cur.fetchall()
print(res)

connection.close()
