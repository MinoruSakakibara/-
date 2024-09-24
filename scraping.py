from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
import signal
import tkinter as tk
import pandas as pd
from tkinter import ttk

year = ''
month = ''

def update():
    year = entry_year.get()
    year = str(year)
    month = combobox.get()

    def scr():
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
            
            dropdown = driver.find_element(By.ID, 'year')
            dropdown_select = Select(dropdown)
            dropdown_select.select_by_value(year)
            
            btnMonth = driver.find_element(By.LINK_TEXT, month)
            btnMonth.click()
            
            table = driver.find_element(By.XPATH, '//*[@id="titleSche"]')
            
            rows = table.find_elements(By.TAG_NAME, 'tr')
            
            data = []
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                cols =  [col.text for col in cols]
                data.append(cols)
            
            df = pd.DataFrame(data)
            
            for i in range(len(df)):
                
                head = df.iloc[i, 0]
                
                if head == 'PS5':
                    df.shift(axis=1)
                elif head == 'PS4':
                    df.shift(axis=1)
                elif head == 'Switch':
                    df.shift(axis=1)
                elif head == 'XSX':
                    df.shift(axis=1)
                
            df.to_excel(year + '月' + month + '.xlsx', index=False, header=False)
            
            # element = driver.find_element(By.XPATH, '//*[@id="titleSche"]')
            
            # trlist = element.find_elements(By.TAG_NAME, 'tr')
            
            # for elem in trlist:
            #     print(elem.text)
            
        finally:
            os.kill(driver.service.process.pid,signal.SIGTERM)
    scr()

root = tk.Tk()
root.title('ゲームソフト価格調査')
root.geometry('300x150')

l_year = tk.Label(root, text = '年')
l_year.pack(pady=2)

entry_year = tk.Entry(root, width=20)
entry_year.pack()

l_month = tk.Label(root, text = '月')
l_month.pack()

month_list = ['1月','2月','3月','4月','5月','6月',
              '7月','8月','9月','10月','11月','12月']
combobox = ttk.Combobox(root, values=month_list)
combobox.pack()

button1 = tk.Button(root, text='実行', command=update)
button1.pack(pady=2)

root.mainloop()

# def scr():
#     options = webdriver.ChromeOptions()
#     options.set_capability("browserVersion", "113")
#     # options.add_argument('--headless')

#     driver = webdriver.Chrome(options = options)
#     driver.implicitly_wait(10)
#     driver.get('https://kakaku.com/')

#     try:
        
#         btnGame = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[4]/div/div/ul[7]/li[2]/a/p')
#         btnGame.click()
        
#         btnSchedule = driver.find_element(By.XPATH, '//*[@id="game"]/div[2]/div[2]/div[1]/ul/li[5]/dl/dd/a')
#         btnSchedule.click()
        
#         dropdown = driver.find_element(By.ID, 'year')
#         dropdown_select = Select(dropdown)
#         dropdown_select.select_by_value(year)

#     finally:
#         os.kill(driver.service.process.pid,signal.SIGTERM)