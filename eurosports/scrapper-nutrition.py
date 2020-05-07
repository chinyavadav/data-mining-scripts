import csv
import requests


with open('temp.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    with open('nutrition.csv', 'w+', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['ID', 'Nutrition', 'Ingredients', 'Blends']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            url = "https://www.europasports.com/Mercury/index.cfm/product/read/0/" + \
                row['\ufeffID']
            page = requests.get(url)
            data = page.json()['data']
            product = data['PRODUCT'][0]
            blends = data['PROPRIETARYBLENDS']
            try:
                data = {'ID': product['productid'], 'Nutrition': data['NUTRIENT'],
                        'Ingredients': product['ingredients'], 'Blends': blends}
                print(product['productid'])
                writer.writerow(data)
            except Exception as e:
                print("Error with {}".format(row['\ufeffID']))
                data = {'ID': row['\ufeffID']}
                writer.writerow(data)
