import csv
import requests


with open('temp.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    with open('out1.csv', 'w+', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['ID', 'Title', 'Description', 'Sku', 'Price', 'Size', 'Flavor', 'Image URL',
                      'Product Type', 'Product categories', 'Brands', 'Weight', 'Length', 'Width', 'Height']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            print(row)
            url = "https://www.europasports.com/Mercury/index.cfm/product/read/0/" + \
                row['\ufeffID']
            page = requests.get(url)
            data = page.json()['data']
            product = data['PRODUCT'][0]
            details = "<h4>DETAILS</h4><p>"+product['productdetails']+"</p><h4>DIRECTIONS</h4><p>" + \
                product['directions'] + "</p><h4>WARNINGS</h4><p>" + \
                product['warnings'] + "</p>"

            if (len(data['MATRIX']) > 1):
                product_type = 'varible'
            else:
                product_type = 'simple'
            data = {'ID': product['productid'], 'Title': product['productname'], 'Description': details, 'Sku': product['stockcode'],
                    'Price': product['wholesaleprice'], 'Size': product['size'], 'Flavor': product['flavor'], 'Image URL': 'https://www.europasports.com'+product['picfile'], 'Product Type': product_type, 'Product categories': product['primarycategory']+','+product['generalcategory'], 'Brands': product['vendorname'], 'Weight': product['weight'], 'Length': product['depth'], 'Width': product['width'], 'Height': product['height']}
            print(product['productid'])
            writer.writerow(data)
