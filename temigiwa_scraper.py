#scrapping data fremigiwa from instagram

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import wget
import re
from time import sleep
from datetime import datetime
import csv
from tqdm import tqdm
import json
import requests
from os import environ

#to remove existing directory
if os.path.exists("temigiwa.csv"):
    os.remove("temigiwa.csv")
else: 
    print("no directory available") 


#Save data in csv file

def save_data(web_link,image,alt1):
    
    with open('temigiwa.csv', mode='a' , newline='',encoding='utf-8') as product_details:
        product_writer = csv.writer(product_details, quoting=csv.QUOTE_MINIMAL)
        print("\n")
        product_writer.writerow([web_link,image,alt1])
def to_csv(new):
    
    with open('new.csv', mode='a' , newline='',encoding='utf-8') as product_details:
        product_writer = csv.writer(product_details, quoting=csv.QUOTE_MINIMAL)
        print("\n")
        product_writer.writerow([new])



#to amximize window

root = os.path.abspath(os.path.dirname(__file__))
profile_path = root + '\\profile\\temigiwa'
print(profile_path)

# #for headless running 
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--headless")
chrome_options.add_argument('user-data-dir=%s' % profile_path)


#for heroku
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-sh-usage")


url = 'https://www.instagram.com/'



driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"),options = chrome_options)




chrome_options = webdriver.ChromeOptions()
driver.maximize_window()

#open webpage
driver.get(url)

driver.implicitly_wait(10)


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return  ")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height



# 1st handle not now button
if driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button'):
  not_now = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
 
else:
  print("no element found")

#2nd handle not now button
if driver.find_elements_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]'):
  not_now = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
  
else:
  print("no element found")


#target the searchbox field
searchbox= driver.find_element_by_xpath('//*[@id="react-root"]//div[2]/input')
searchbox.clear()

# search for hashtag cat
#keyword= input("Enter handle  Here........")
searchbox.send_keys("zephansandco")

#wait for 2 to 3 seconds
time.sleep(3)

# press enter
searchbox.send_keys(Keys.ENTER)
searchbox.send_keys(Keys.ENTER)
time.sleep(2)
listoflinks=[]






for i in range(1,15):
  driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
  sleep(4)
  driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
  sleep(4)
  images = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div/div')
  
  


  
  for e in images:
    
    anchor=e.find_element_by_tag_name('a')

    listoflinks.append(anchor.get_property('href'))

print(len(listoflinks))

#start loading posts
for i in tqdm(listoflinks):
  
  driver.get(i)
  
  if driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span'):
    alt1 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text.lower()
    #print(alt1)
    sleep(5)
  
  if driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/div/div/time'):
    weeks = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/div/div/time').text
    print(weeks)
  
  if "w" in weeks:
    weeks1 = int(weeks.replace("w",""))
    print(weeks1)
    cond= 16
    if weeks1 <= cond:

      if re.search(r"(N([0-9]+)|(\/\$[0-9])+)|(\$[0-9]+)|(\$+)|(price:|Price:)|(price|Price)|(₦)", alt1): 
        urls= driver.current_url
        x=f'{urls}?__a=1'
        driver.get(x)
        sleep(1)

        x = driver.find_element_by_tag_name("pre").text
        
        y= json.loads(x)
        #print(y)
        web_link =driver.current_url
          

          
        image=y['graphql']['shortcode_media']['display_resources'][0]['src']
          
        print(image)

        save_data(web_link,image,alt1)
      
      else:
        print("no description found")
    
    else:
      print("data out of range")
  
  #else of  if"w" in weeks1
  else:
        
        
    if re.search(r"(N([0-9]+)|(\/\$[0-9])+)|(\$[0-9]+)|(\$+)|(price:|Price:)|(price|Price)|(₦)", alt1):
          
      urls= driver.current_url
      x=f'{urls}?__a=1'
      driver.get(x)
      sleep(1)

      x = driver.find_element_by_tag_name("pre").text
        
      y= json.loads(x)
      #print(y)
      web_link =driver.current_url
          

          
      image=y['graphql']['shortcode_media']['display_resources'][0]['src']
          
      print(image)

      save_data(web_link,image,alt1)
          

        
    else:
      print("no description found")




