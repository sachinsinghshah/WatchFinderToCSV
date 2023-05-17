import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

# call chrome webdriver
driver = webdriver.Chrome()

# opens watch finder website
driver.get("https://www.watchfinder.co.uk/new-arrivals")


driver.maximize_window()
time.sleep(5)

# Bypassing the popup

close_popup = driver.find_element(By.XPATH, "//button[text()='Close ']")
close_popup.click()

time.sleep(3)

# Bypassing Cookies Popup

accept_cookies = driver.find_element(By.XPATH, "//*[@id='cookie_']/div/div/div[2]/div[2]/button")
accept_cookies.click()

time.sleep(3)

# Finds  product items
products = driver.find_elements(By.XPATH, '//div[@data-testid="watchItem"]')

# Creates a list to store the scraped data
data = []

# Iterates over every product element
for product in products:
    # Exception Handling block to ignore NoSuchElementException error
    try:
        item_id = product.find_element(By.XPATH, './/a[@data-testid="watchLink"]').get_attribute('href').split('/')[-1]
        url = product.find_element(By.XPATH, './/a[@data-testid="watchLink"]').get_attribute('href')
        name = product.find_element(By.XPATH, './/div[@data-testid="watchSeries"]').text
        brand = product.find_element(By.XPATH, './/div[@data-testid="watchBrand"]').text
        price_with_currency= product.find_element(By.XPATH, './/div[@data-testid="watchPrice"]').text
        price = price_with_currency[1:]
        final_price = price
        estimated_retail_price = None
        currency = price_with_currency[0]
        model = name
        model_no = product.find_element(By.XPATH, './/div[@data-testid="watchModelNumber"]').text
        gender = None
        year_element = product.find_element(By.XPATH, './/span[@data-testid="watchYearValue"]')
        year = year_element.text if year_element else None
        condition = None
        images = [img.get_attribute('src') for img in product.find_elements(By.XPATH, './/img')]
        description = None
        box = product.find_element(By.XPATH, './/span[@data-testid="watchBoxValue"]').text
        papers = product.find_element(By.XPATH, './/span[@data-testid="watchPapersValue"]').text
        case_size = None
        case_material = None
        case_shape = None
        dial_color = None
        movement = None
        band_color = None
        bracelet_material = None
        water_resistance = None
        details = None
        fetch_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        item_data = {
            'item_id': item_id,
            'url': url,
            'name': name,
            'brand': brand,
            'price': price,
            'final_price': final_price,
            'estimated_retail_price': estimated_retail_price,
            'currency': currency,
            'model': model,
            'model_no': model_no,
            'gender': gender,
            'year': year,
            'condition': condition,
            'images': images,
            'description': description,
            'box': box,
            'papers': papers,
            'case_size': case_size,
            'case_material': case_material,
            'case_shape': case_shape,
            'dial_color': dial_color,
            'movement': movement,
            'band_color': band_color,
            'bracelet_material': bracelet_material,
            'water_resistance': water_resistance,
            'details': details,
            'fetch_date': fetch_date
        }


        data.append(item_data)
    except NoSuchElementException:
        pass

# Defining fieldnames for the CSV file

fieldnames = [
    'item_id',
    'url',
    'name',
    'brand',
    'price',
    'final_price',
    'estimated_retail_price',
    'currency',
    'model',
    'model_no',
    'gender',
    'year',
    'condition',
    'images',
    'description',
    'box',
    'papers',
    'case_size',
    'case_material',
    'case_shape',
    'dial_color',
    'movement',
    'band_color',
    'bracelet_material',
    'water_resistance',
    'details',
    'fetch_date'
]

# converting dictionary to a csv file
with open("output.csv", 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


print(f"Please open output.csv file to access the requested data.")
