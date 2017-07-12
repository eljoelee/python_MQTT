# -*- coding: cp949 -*-
import requests
from bs4 import BeautifulSoup
import re
import paho.mqtt.client as mqtt
import time

broker = "IP Address"

pattern = re.compile(r'굎+') # 공백문자 제거를 위한 정규표현식

url = 'https://www.airkorea.or.kr/index' #미세먼지

client = mqtt.Client()
client.connect(broker, 1883) #MQTT 연결
client.loop_start()

while True:
    now = time.localtime()

    urlToindex = 'http://www.kma.go.kr/weather/observation/currentweather.jsp?tm=%04d.%02d.%02d.%02d:00&type=t99&mode=0&auto_man=m&stn=108'% (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour)

    source_code = requests.get(url) #웹 파싱
    plain_text = source_code.text #Text 요소 추출
    soup = BeautifulSoup(plain_text, "html.parser") #BeautifulSoup 라이브러리를 활용하여 크롤링한 데이터 정리
    local = soup.find("ul", id="mcc_02_list")

    dust = local.contents[1].text #local의 첫번째 text값을 추출한다.

    dust = dust.replace('서울', '') #숫자만 추출하기 위해 replace함수를 적용해 한글을 지운다.
    dust = re.sub(pattern, '', dust) #마찬가지로 공백을 지우기위해 정규표현식을 사용한다.

    client.publish('dust', dust) #MQTT Publish

    print('publish dust : ' + dust) #확인 메세지

    source_code = requests.get(urlToindex)
    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, "html.parser")

    # Class 이름이 table_develop3인 Table의 tbody요소 중 8번째 td요소의 값을 추출한다.
    discom = soup.find("table", {"class": "table_develop3"}).tbody('td')[7].text

    client.publish('discom', discom)

    print('publish discom : ' + discom)

    time.sleep(3600) #1시간마다 반복을 위한 sleep함수
