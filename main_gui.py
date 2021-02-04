from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json
import time
import tkinter as tk # pip install tkinter / pip install Tkinter
import numpy as np # pip install numpy

fields = ["Search Query", "Sort By", "Low Price", "High Price", "Pincode"]

from selenium.webdriver.support.select import Select

def search_amazon(item, user_defined_sorting, low_price=None, high_price=None, pincode=400072):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.amazon.in/')
    search_box = driver.find_element_by_id('twotabsearchtextbox').send_keys(item)
    search_button = driver.find_element_by_id("nav-search-submit-text").click()

    driver.implicitly_wait(10)

    # THIS IS FOR TASK 2
    sort_by_button = Select(driver.find_element_by_css_selector('select#s-result-sort-select'))
    sort_by_button.select_by_value(user_defined_sorting)

    if low_price is not None and high_price is not None:
        try:
            low_price_text = driver.find_element_by_id("low-price").send_keys(low_price)
            high_price_text = driver.find_element_by_id("high-price").send_keys(high_price)
            # go_button = driver.find_element_by_xpath(price_button_xpath).click()
           
            go_button = driver.find_element_by_xpath("//li[@id='p_36/price-range']//span[@class='a-list-item']//form//span[@class='a-button a-spacing-top-mini a-button-base s-small-margin-left']//span[@class='a-button-inner']//input[@type='submit']").click()
        except NoSuchElementException:
            print("Low price high price fields not found...")
    else:
        print("Either of the prices were not given, ignoring this step...")

    address_open = driver.find_element_by_id("glow-ingress-line2").click()
    driver.implicitly_wait(5)
    text_pincode = driver.find_element_by_id("GLUXZipUpdateInput").send_keys(pincode)
    # go_button = driver.find_element_by_class_name("a-button-input").click()
    go_button = driver.find_element_by_xpath("//input[@type='submit' and @aria-labelledby='GLUXZipUpdate-announce']").click()
    time.sleep(8)

    try:
        num_page = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[6]')
    except NoSuchElementException:
        num_page = None

    driver.implicitly_wait(5)

    url_list = []

    i = 0
    while True:
        page_ = i + 1
        url_list.append(driver.current_url)
        driver.implicitly_wait(5)
        click_next = driver.find_element_by_class_name('a-last')
        if "a-disabled" in click_next.get_attribute("class"):
            break
        click_next.click()
        i += 1
        print("Page " + str(page_) + " grabbed")

    driver.quit()


    with open('search_results_urls.txt', 'w') as filehandle:
        for result_page in url_list:
            filehandle.write('%s\n' % result_page)

    print("---DONE---")

def scrape(url, e):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)
"""
input_word = str(input("What do you want to search? "))
input_sorting = str(input("Sort by: [Featured/Price: Low to High/Price: High to Low/Avg. Customer Review/Newest Arrivals] "))
input_price_yn = str(input("Do you want to put a low price or high price limit? [Y/N]"))

if input_price_yn.upper() == "Y":
    input_price_low = str(input("Do you want to put a low price limit? "))
    input_price_high = str(input("Do you want to put a high price limit? "))
else:
    input_price_low = None
    input_price_high = None

is_pincode = str(input("Want to give us a pincode? [Y/N] "))
if is_pincode:
    pincode = str(input("pincode please: "))
else:
    pincode = None
"""

master = tk.Tk()
es = []
for i in range(len(fields)):
    text_field = fields[i]
    tk.Label(master, 
             text=text_field).grid(row=i)
    es.append(tk.Entry(master))
    es[i].grid(row=i, column=1)

# e1.grid(row=0, column=1)
# e2.grid(row=1, column=1)

tk.Button(master, 
          text='Quit', 
          command=master.quit).grid(row=len(fields), 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
def main():
    input_word = es[0].get()
    input_sorting = es[1].get()
    input_price_low = es[2].get()
    input_price_high = es[3].get()
    pincode = es[4].get()
    try:
        int(pincode)
    except:
        # Default
        pincode = "400072"

    if "Featured" in input_sorting:
        input_sorting = "relevanceblender"
    elif "Low to High" in input_sorting:
        input_sorting = "price-asc-rank"
    elif "High to Low" in input_sorting:
        input_sorting = "price-desc-rank"
    elif "Customer Review" in input_sorting:
        input_sorting = "review-rank"
    elif "Newest" in input_sorting:
        input_sorting = "date-desc-rank"
    else:
        input_sorting = "relevanceblender" # By default it will be Featured option

    search_amazon(input_word, input_sorting, input_price_low, input_price_high, pincode) # <------ search query goes here.

    # Create an Extractor by reading from the YAML file
    e = Extractor.from_yaml_file('search_results.yml')

    # product_data = []
    prices = []
    products = []
    with open("search_results_urls.txt",'r') as urllist, open('search_results_output.json','w') as outfile:
        count_products = 0
        for url in urllist.read().splitlines():
            data = scrape(url, e)
            if data:
                count_products += len(data['products'])
                for product in data['products']:
                    product['search_url'] = url

                    # Task 4
                    if product['price'] is not None:
                        prices.append(int(product['price'].encode('ascii', 'ignore').decode("utf-8").replace(',','')))
                        products.append(product)
                    print("Saving Product: %s"%product['title'].encode('utf8'))
                    json.dump(product,outfile)
                    outfile.write("\n")
                    # sleep(5)
    
    with open("lowest_priced_product.txt", "w") as lowest_prod:
        min_index_of_product = np.argmin(np.array(prices)) 
        json.dump(products[min_index_of_product], lowest_prod)
        lowest_prod.write("\n")

tk.Button(master, 
          text='Show', command=main).grid(row=len(fields), 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)
tk.mainloop()
