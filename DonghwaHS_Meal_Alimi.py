from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import *
from flask import Flask, request, jsonify
import time
from datetime import datetime
import socket
import getmac

application = Flask(__name__)

today_m = datetime.today().month
today_d = datetime.today().day
today_w = datetime.today().weekday()

print("Server turned ON ({})".format(datetime.today()))
print("Server Computer: {}".format(socket.gethostname()))
print("Server IP: {}".format(socket.gethostbyname(socket.gethostname())))
print("Server MAC: {}".format(getmac.get_mac_address()))

if today_w == 5 or today_w == 6:
    meals = "주말에는 급식이 제공되지 않습니다."
    print("Today Message: \n", meals)
else:
    if (today_d+2) / 7 < 1:
        link = 1152 + today_d
    elif (today_d+2) / 7 < 2 and (today_d+2) / 7 >= 1:
        link = 1152 + today_d
    elif (today_d+2) / 7 < 3 and (today_d+2) / 7 >= 2:
        link = 1152 + today_d - 2
    elif (today_d+2) / 7 < 4 and (today_d+2) / 7 >= 3:
        link = 1152 + today_d - 4
    elif (today_d+2) / 7 < 5 and (today_d+2) / 7 >= 4:
        link = 1152 + today_d - 6
    elif (today_d+2) / 7 < 6 and (today_d+2) / 7 >= 5:
        link = 1152 + today_d - 8
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('(Your Chrom Driver Route)', options=options)
    url = 'https://donghwa.hs.kr/bbs/board.php?bo_table=gup_02&wr_id='+str(link)
    driver.get(url)
    time.sleep(1)

    date = driver.find_element(By.XPATH, '//*[@id="bo_v_title"]')
    lunch = driver.find_element(By.XPATH, '//*[@id="bo_v"]/div[2]/div/div[1]/div')
    dinner = driver.find_element(By.XPATH, '//*[@id="bo_v"]/div[2]/div/div[2]/div')
    
    meals = "=================\n" + date.text + "\n=================\n" + lunch.text + "\n------------------------\n" + dinner.text + "\n------------------------" + ""
    print("출력 메세지: ", meals)

@application.route("/")
def hello():
    return "GET OUT!!"

@application.route("/meal",methods=['POST'])
def Meal():
    answers = meals

    res = {"version": "2.0","template": {"outputs": [{"simpleText": {"text": answers}}]}}
    
    return jsonify(res)
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
