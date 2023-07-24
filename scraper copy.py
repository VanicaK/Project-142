from selenium import webdriver
from bs4 import BeautifulSoup
import time, csv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests

planet_url="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get(planet_url)
time.sleep(10)
data_list=[]
planet_list=[]
headers=["name","distance","mass","magnitude","discovery","hyperlink"]

def scraper():
    
    for page in range(0,5):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

        if current_page_num < page:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        elif current_page_num > page:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
        else:
                break
        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ultag.find_all("li")
            templist=[]
            for index,litag in enumerate(litags):
                if index==0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try: 
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            hyperlinklitag=litags[0]
            templist.append("https://exoplanets.nasa.gov"+ hyperlinklitag.find_all("a", href=True)[0]["href"])
            
            data_list.append(templist)

                
        browser.find_element(by=By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
       

def detailscraper(link):
    try:
        plpage=requests.get(link)
        soup=BeautifulSoup(plpage.content,"html.parser")
        templist=[]
        for trtag in soup.find_all("tr",attrs={"class","fact_row"}):
            tdtags=trtag.find_all("td")
            for tdtag in tdtags:
                try:
                    templist.append(tdtag.find_all("div",attr={"class","value"})[0].contents[0])
                except:
                    templist.append("")
        planet_list.append(templist)
    except:
        time.sleep(1)
        detailscraper(link)  


scraper()
for index,data in enumerate(data_list):
    detailscraper(data[5])
finalplanetdata=[]
for index,data in enumerate(data_list):
    newplanetdataelement=planet_list[index]
    newplanetdataelement=[elem.replace("\n","")for elem in newplanetdataelement]
    newplanetdataelement=newplanetdataelement[:7]
    finalplanetdata.append(data_list+newplanetdataelement)
with open("scraperF.csv","w") as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalplanetdata)

      
