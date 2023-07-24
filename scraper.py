from selenium import webdriver
from bs4 import BeautifulSoup
import time, csv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

planet_url="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get(planet_url)
time.sleep(10)
data_list=[]

def scraper():
    headers=["name","distance","mass","magnitude","discovery","hyperlink"]
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
        with open("scraper.csv","w") as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow(headers)
            csvwriter.writerows(data_list)

scraper()