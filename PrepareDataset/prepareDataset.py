import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import pandas as pd

from Credentials.secrets import username, password

class scrape:
	def init(self):
		pass

	def loginToFacebook(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--disable-notifications")

		self.driver = webdriver.Chrome('chromedriver.exe')
		self.url = 'https://www.facebook.com'
		self.driver.get(self.url)
		time.sleep(2)
		email = self.driver.find_element_by_name("email")
		pswrd = self.driver.find_element_by_name("pass")
		email.send_keys(username)
		time.sleep(1)
		pswrd.send_keys(password)
		time.sleep(3)
		email.submit()
		time.sleep(10)
		return self.driver

	def searchPosts(self):
		searchURL = 'https://www.facebook.com/search/posts/?q=' + self.query
		self.driver.get(searchURL)

		time.sleep(5)

		SCROLL_PAUSE_TIME = 3

		last_height = self.driver.execute_script("return document.body.scrollHeight")

		starttime=time.time()

		while True:
		    currenttime=time.time()
		    if currenttime-starttime>20:
		        break
		        
		    try:    
		        if self.driver.find_element_by_xpath("//*[contains(text(),'See more')]"):
		            try:
		                wait = WebDriverWait(self.driver, 10)
		                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"See more")]')))
		                element.click()
		            except:
		                pass
		    except:
		        pass

		    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
		    
		    try:    
		        if self.driver.find_element_by_xpath("//*[contains(text(),'See more')]"):
		            try:
		                wait = WebDriverWait(self.driver, 10)
		                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"See more")]')))
		                element.click()
		            except:
		                pass
		    except:
		        pass

		    time.sleep(SCROLL_PAUSE_TIME)

		    new_height = self.driver.execute_script("return document.body.scrollHeight")
		    if new_height == last_height:
		        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		    last_height = new_height
		    
		try:
		    self.driver.find_element_by_xpath("//*[contains(text(),'See more')]").click()
		except:
		    pass

	def getPageContent(self):
		self.searchPosts()

		pageContent = self.driver.page_source
		self.soup = BeautifulSoup(pageContent, 'lxml')

	def getPostCaptions(self, mydivstr):
		result = []
		for div in mydivstr:
		    tempstr = div[1:len(mydivstr[0])-1]
		    tempstr=re.sub('"', "", tempstr)
		    resultstr=''
		    while tempstr:
		        try:
		            start=tempstr.index(">")
		            end=tempstr.index("<")
		            resultstr+=tempstr[start+1: end]
		            tempstr=tempstr[end+1:]
		        except:
		            break
		    result.append(resultstr.strip(' '))
		return result

	def convertToDataframe(self):
		self.getPageContent()

		mydivs = self.soup.find_all("div", {"class": "ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"})
		mydivstr = []

		for divs in mydivs:
		    mydivstr.append(str(divs))

		result = self.getPostCaptions(mydivstr)

		df = pd.DataFrame(result)
		df.columns=['Post']

		return df

	def getDataSet(self, query, driver):
		self.query = query
		self.driver = driver

		df = self.convertToDataframe()

		time.sleep(2)

		return df 