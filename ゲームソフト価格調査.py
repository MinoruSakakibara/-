from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
import signal
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import messagebox

year = ''
month = ''

# メイン処理
def exe():
    year = entry_year.get()
    month = combobox.get()
    
    def fullwidth_char(year):
        return '０' <= year <= '９'
    
    
    # 不正入力時のエラー処理
    if year == '' or month == '':
        messagebox.showinfo('エラー', '空欄に必要事項を入力してください')
        return
    elif not (isinstance(year, str) and len(year) == 4 and year.isdigit()):
        messagebox.showinfo('エラー', '「年」には4桁の半角数字で入力してください')
        return
    elif fullwidth_char(year):
        messagebox.showinfo('エラー', '「年」には4桁の半角数字で入力してください')
        return
    
    # Webページ接続
    def scr():
        options = webdriver.ChromeOptions()
        options.set_capability("browserVersion", "113")
        # options.add_argument('--headless')

        driver = webdriver.Chrome(options = options)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(10)
        driver.get('https://kakaku.com/')

        try:
            
            btnGame = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[4]/div/div/ul[7]/li[2]/a/p')
            btnGame.click()
            
            btnSchedule = driver.find_element(By.XPATH, '//*[@id="game"]/div[2]/div[2]/div[2]/ul/li[5]/dl/dd/a')

            btnSchedule.click()
            
            dropdown = driver.find_element(By.ID, 'year')
            dropdown_select = Select(dropdown)
            dropdown_select.select_by_value(year)
            
            btnMonth = driver.find_element(By.LINK_TEXT, month)
            btnMonth.click()
            
            # テーブル取得
            table = driver.find_element(By.XPATH, '//*[@id="titleSche"]')
            
            rows = table.find_elements(By.TAG_NAME, 'tr')
            
            data = []
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                cols =  [col.text for col in cols]
                
                if len(cols) == 4:
                    cols.insert(0, "")
                
                data.append(cols)
            
            # データフレーム作成、エクセル出力
            df = pd.DataFrame(data)
            
            df.to_excel(year + '月' + month + '.xlsx', index=False, header=False)
            
            messagebox.showinfo('確認', '処理が終了しました')
         
        # 処理中エラー発生時の処理   
        except NoSuchElementException as e:
            messagebox.showinfo('エラー', '入力内容を確認してください')
        except TimeoutException as e:
            messagebox.showinfo('タイムアウトエラー', '再度実行してみてください')
        # finally:
        #     os.kill(driver.service.process.pid,signal.SIGTERM)
        
    scr()

# 入力ウィンドウ作成
root = tk.Tk()
root.title('ゲームソフト価格調査')
root.geometry('300x150')

l_year = tk.Label(root, text = '年：西暦を4桁の半角数字で入力してください')
l_year.pack(pady=2)

entry_year = tk.Entry(root, width=23)
entry_year.pack()

l_month = tk.Label(root, text = '月：プルダウンから選択してください')
l_month.pack()

month_list = ['1月','2月','3月','4月','5月','6月',
              '7月','8月','9月','10月','11月','12月']
combobox = ttk.Combobox(root, values=month_list)
combobox.pack()

button1 = tk.Button(root, text='実行', command=exe)
button1.pack(pady=2)

root.mainloop()