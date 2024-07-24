from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
import signal

options = webdriver.ChromeOptions()
options.set_capability("browserVersion", "113")
# options.add_argument('--headless')

driver = webdriver.Chrome(options = options)
driver.implicitly_wait(10)
driver.get('https://kakaku.com/')

try:
    
    btnGame = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[4]/div/div/ul[7]/li[2]/a/p')
    btnGame.click()
    
    btnSchedule = driver.find_element(By.XPATH, '//*[@id="game"]/div[2]/div[2]/div[1]/ul/li[5]/dl/dd/a')
    btnSchedule.click()

finally:
     os.kill(driver.service.process.pid,signal.SIGTERM)