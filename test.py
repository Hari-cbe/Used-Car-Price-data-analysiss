import requests 
import csv 
import pandas 


URL = "hhttps://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/car-sales.csv.gz"


# with requests.session() as req:
#     data = req.get(URL)

#     data_encoded = data.content.decode("utf-8")

#     csv_dowload = csv.reader(data_encoded,delimiter=",",quotechar='"')


#     lst_csv = list(csv_dowload)

#     print(lst_csv)

df = pandas.read_csv(URL,index_col=0,delimiter=',',nrows=50,compression='gzip')

print(df)