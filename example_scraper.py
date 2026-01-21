import requests
import json
import re
from bs4 import BeautifulSoup

url = "https://dir.indiamart.com/impcat/pvc-pipes.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract JSON data from script tag
script = soup.find('script', string=re.compile('window.__INITIAL_STATE__'))
# print(script)
json_data = re.search(r'window.__INITIAL_STATE__ = (.*?);', script.string, re.DOTALL).group(1)
data = json.loads(json_data)

with open('output.txt', 'w') as f:
    print('', file = f)

# Extract product data
products = data['data']
for product in products:
    product_name = product.get('p_nm', 'N/A')
    supplier_name = product.get('CMP', 'N/A')
    price = product.get('pr', 'N/A')
    location = f"{product.get('city', 'N/A')}, {product.get('ad', 'N/A')}"
    product_url = product.get('p_url', 'N/A')
    supplier_url = product.get('s_url', 'N/A')
    rating = product.get('wt_avg', 'N/A')
    reviews = product.get('tr_c', 'N/A')

    # Print or save to CSV
    # print(f"Product: {product_name}")
    # print(f"Supplier: {supplier_name}")
    # print(f"Price: {price}")
    # print(f"Location: {location}")
    # print(f"Product URL: {product_url}")
    # print(f"Supplier URL: {supplier_url}")
    # print(f"Rating: {rating} ({reviews} reviews)")
    # print("---")

    with open('output.txt', 'a') as f:
        print('', file = f)
        print(f"Product: {product_name}", file = f)
        print(f"Supplier: {supplier_name}", file = f)
        print(f"Price: {price}", file = f)
        print(f"Location: {location}", file = f)
        print(f"Product URL: {product_url}", file = f)
        print(f"Supplier URL: {supplier_url}", file = f)
        print(f"Rating: {rating} ({reviews} reviews)", file = f)
        print("---", file = f)
