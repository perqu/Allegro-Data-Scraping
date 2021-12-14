# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Firefox()
links = []
pages = 2
sleep_time = 5

loaded = False

#Clear console
os.system('clear')

#Load links
try:
    with open('Links.txt', 'r') as f:
        links = [line for line in f]
        loaded = True
except:
    print("No 'Links.txt' file")

#Getting links to all products
if not loaded:
    for i in range (pages):
        driver.get("https://allegro.pl/kategoria/komputery-stacjonarne-486?order=qd&p="+str(i))
        elements = driver.find_elements(By.CLASS_NAME, "_w7z6o._uj8z7.meqh_en.mpof_z0.mqu1_16.m6ax_n4._6a66d_2vTdY")
        links += [el.get_attribute('href') for el in elements]
        time.sleep(sleep_time)
        os.system('clear')
        print("Gathering links: " + str(i) + "%")

    os.system('clear')
    print("Saving links")  
    with open('Links.txt', 'w') as f:
        for link in links:
            f.write(str(link) + '\n')
    os.system('clear')
    print("Links Saved")

#Load products data
os.system('clear')
print("Loading Products Data")
file_length = 0

try:
    with open('Allegro_Data.txt', 'r') as f:
        nonempty_lines = [line.strip("\n") for line in f if line != "\n"]
        file_length = len(nonempty_lines)
except:
    print("No 'Allegro_Data.txt' file")

#Getting products data
os.system('clear')
print("Gathering Products Data")
for count, link in enumerate(links):
    if count >= file_length:
        driver.get(link)
        p1 = driver.find_element(By.CLASS_NAME, "_1svub._lf05o.mpof_vs.munh_8.mp4t_4")
        p2 = driver.find_element(By.CLASS_NAME, "_1h7wt._1bo4a")

        Name = str(driver.title)[0:-45]
        try:
            Price = float(p1.get_attribute('aria-label')[5:-3].replace(' ',''))
        except:
            Price = 'None'
        try:
            Rating = float(p2.get_attribute("data-analytics-view-custom-rating-value"))
        except:
            Rating = 'None'
        try:
            Amount_of_Ratings = int(p2.get_attribute("data-analytics-view-custom-rating-count"))
        except:
            Amount_of_Ratings = 'None'

        with open('Allegro_Data.txt', 'a') as f:
            f.write(str(count+1) + ',' + str(Name) + ',' + str(Price) + ','  + str(Rating) + ','  + str(Amount_of_Ratings) + '\n' )
            os.system('clear')
            print("Saved " + str(count+1) + "/" + str(len(links)) + " products data.")
        time.sleep(sleep_time)
driver.quit()