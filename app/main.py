from selenium import webdriver
import time
from datetime import date
import os
import pandas as pd
import datakicker as dk

def getData():
    chrome_options = webdriver.ChromeOptions()
    downloadPath= "/Users/jonock/PycharmProjects/corona-bl/app/data"
    prefs = {}
    prefs["download.default_directory"]=downloadPath
    prefs["profile.default_content_settings.popups"] = 0
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    chrome_options.add_experimental_option("prefs", prefs)
    chromedriverpath = "/Users/jonock/PycharmProjects/corona-bl/venv/chromedriver"
    driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriverpath)
    driver.get('https://cocontrol.bl.ch/public/dbw/209')
    #driver.get('https://cocontrol.bl.ch/public/dbw/216')
    driver.set_page_load_timeout(10)
    #time.sleep(1)
    datum = driver.find_element_by_css_selector('.highcharts-subtitle').text
    python_button = driver.find_elements_by_css_selector(".highcharts-button-symbol")
    python_button[0].click()
    python_b = driver.find_elements_by_css_selector(".highcharts-menu-item:nth-child(5)")
    python_b[0].click()
    time.sleep(2)
    driver.close()
    return datum

def modifyData(datum):
    os.rename('data/14-tage-inzidenz-pro-gemeinde.csv', modifyFilename(datum[62:].replace(')','')+ '_14d.csv'))
    print('Datei umbenannt')
    data = pd.read_csv(modifyFilename(datum[62:].replace(')','')+ '_14d.csv'))
    base = pd.read_csv('data/bl_base.csv')
    data = data.sort_values(by=['map_feature'], ignore_index=True)
    aggregated = pd.concat([base,data['value']], axis=1)
    filename = modifyFilename(datum[62:].replace(')','')+ '_14d_upload.csv')
    aggregated.to_csv(filename, index=False)
    dk.updatedwchart(id='59AH4', data=aggregated, timeframe=datum[62:].replace(')', ''))
    bigtowns = pd.read_csv('data/bl_above2k.csv', index_col=0)
    aggregatedbig = pd.concat([bigtowns,data['value']], axis=1, join='inner')
    dk.updatedwchart(id='guadQ', data=aggregatedbig, timeframe=datum[62:].replace(')', ''))
    return aggregated


def genDate():
    today = date.today()
    return today.strftime("%Y%m%d")

def modifyFilename(filename):
    filename = './data/' + genDate() + '_' + filename
    return filename

if __name__ == '__main__':
    print('Starte Skript')
    datum = getData()
    data = modifyData(datum)
    print('finito')
