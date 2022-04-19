from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app
)
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])

def index():
    
    websites={
    "jiji":"https://jiji.co.ke/search?query={}",
    "jumia":"https://www.jumia.co.ke/catalog/?q={}",
    "jamboShop":"https://www.jamboshop.com/search?k={}",
    "avechi":"https://avechi.co.ke/?s={}"
    }

    searches = list()
    if request.method == 'POST':
  
        if request.form['name']:
            name = request.form['name']
            item = name.replace(" ","+")
            searches.append(item)
    print(searches)     
    global avechi_title
    global avechi_image
    global avechi_link

    avechi_title = list()
    avechi_image = list()
    avechi_link = list()

    global jambo_title
    global jambo_price
    global jambo_image
    global jambo_link
    
    jambo_title = list()
    jambo_price = list()
    jambo_image = list()
    jambo_link = list()

    global jumia_title
    global jumia_price
    global jumia_image
    global jumia_link
    
    jumia_title = list()
    jumia_price = list()
    jumia_image = list()
    jumia_link = list()

    global jiji_title
    global jiji_price
    global jiji_image
    global jiji_link
    
    jiji_title = list()
    jiji_price = list()
    jiji_image = list()
    jiji_link = list()

    # look = input("what are you looking for: ")
    # searches.append(look)

    urls = list()
    webs =list()
    for website, ur in websites.items():
        webs.append(website)
        for s in searches:
            url =(ur.format(s))
            urls.append(url)
            
    weburls=dict(zip(webs, urls))
    
    for website, url in weburls.items():
        print("FETCHING PRODUCT FROM:" +website)


        if website == "jiji":

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            products = soup.find_all(class_="qa-advert-list-item")

            for product in products:

                if product:

                    title = product.find(class_='qa-advert-title').get_text()
                    price = product.find(class_='b-list-advert__item-price').get_text()
                    link = product.find('a')
                    img = product.find('img')

                    jiji_title.append(title)
                    jiji_price.append(price)
                    jiji_image.append(img['src'])
                    jiji_link.append(link['href'])


        elif website == "jumia":

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            products = soup.find_all(class_="c-prd")

            for product in products:

                if product:

                    title = product.find(class_='name').get_text()
                    price = product.find(class_='prc').get_text()
                    link = product.find('a')
                    img = product.find('img')

                    jumia_title.append(title)
                    jumia_price.append(price)
                    jumia_image.append(img['data-src'])
                    jumia_link.append(link.get('href'))

                    

                   



        elif website == "jamboShop":

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            products = soup.find_all(class_="category-product")

            for product in products:

                if product:

                    title = product.find(class_='prd-title').get_text()
                    price = product.find(class_='offer-price').get_text()
                    link = product.find('a')
                    img = product.find('img')

                    jambo_title.append(title)
                    jambo_price.append(price)
                    jambo_image.append(img['src'])
                    jambo_link.append(link['href'])




        elif website == "avechi":

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            products = soup.find_all(class_="info_in_dealgrid")

            for product in products:

                if product:

                    title = product.find(class_='flowhidden').get_text()
                    link = product.find('a')
                    img = product.find('img')

                    avechi_title.append(title)
                    avechi_image.append(img['src'])
                    avechi_link.append(link['href'])


    return render_template("index.html", jambo=zip(jambo_title,jambo_price,jambo_image,jambo_link),
    jumia=zip(jumia_title,jumia_price,jumia_image),
    jiji=zip(jiji_title,jiji_price,jiji_image,jiji_link),
    avechi=zip(avechi_title,avechi_image,avechi_link))                

if __name__ == "__main__":
    app.run(debug=True)