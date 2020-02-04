from datetime import date
import os

today = date.today()
today = today.strftime("%d%B%Y")

path1 = "data/order/" + today
path2 = "data/portfolio/" + today

os.makedirs(path1)
os.makedirs(path2)