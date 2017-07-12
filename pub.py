# -*- coding: cp949 -*-
import requests
from bs4 import BeautifulSoup
import re
import paho.mqtt.client as mqtt
import time

broker = "IP Address"

pattern = re.compile(r'�s+') # ���鹮�� ���Ÿ� ���� ����ǥ����

url = 'https://www.airkorea.or.kr/index' #�̼�����

client = mqtt.Client()
client.connect(broker, 1883) #MQTT ����
client.loop_start()

while True:
    now = time.localtime()

    urlToindex = 'http://www.kma.go.kr/weather/observation/currentweather.jsp?tm=%04d.%02d.%02d.%02d:00&type=t99&mode=0&auto_man=m&stn=108'% (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour)

    source_code = requests.get(url) #�� �Ľ�
    plain_text = source_code.text #Text ��� ����
    soup = BeautifulSoup(plain_text, "html.parser") #BeautifulSoup ���̺귯���� Ȱ���Ͽ� ũ�Ѹ��� ������ ����
    local = soup.find("ul", id="mcc_02_list")

    dust = local.contents[1].text #local�� ù��° text���� �����Ѵ�.

    dust = dust.replace('����', '') #���ڸ� �����ϱ� ���� replace�Լ��� ������ �ѱ��� �����.
    dust = re.sub(pattern, '', dust) #���������� ������ ��������� ����ǥ������ ����Ѵ�.

    client.publish('dust', dust) #MQTT Publish

    print('publish dust : ' + dust) #Ȯ�� �޼���

    source_code = requests.get(urlToindex)
    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, "html.parser")

    # Class �̸��� table_develop3�� Table�� tbody��� �� 8��° td����� ���� �����Ѵ�.
    discom = soup.find("table", {"class": "table_develop3"}).tbody('td')[7].text

    client.publish('discom', discom)

    print('publish discom : ' + discom)

    time.sleep(3600) #1�ð����� �ݺ��� ���� sleep�Լ�
