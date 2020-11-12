from market.models import Products
import csv


with open(".././goods.csv", encoding='utf-8') as f:
    csv_reader = csv.DictReader(f, delimiter=";")
    for row in csv_reader:
        try:
            f_price = int(row["Цена"])
            if f_price < 1000:
                sale_price = f_price*1.2
            else:
                sale_price = f_price*1.1
            Products.objects.create(vendor_code="ПТ" +
                                    row["Код товара"], name=row["Наименование"], purchase_price=0.9*int(row["Цена"]), sale_price=sale_price)
        except ValueError:
            print("price in file has wrong type")
