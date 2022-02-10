from tkinter.constants import N
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from konlpy.tag import Kkma
import collections
import matplotlib.pyplot as plt
from wordcloud import WordCloud  #대소문자 주의

driver = webdriver.Chrome('C://Users/20060025/test/chromedriver.exe') # 대소문자 주의.

result_list = [] 

for i in range(1,10) :
    url = "https://www1.president.go.kr/petitions/?c=0&only=1&page={}&order=1".format(i)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')  #driver.page_source 현재 조정하고 있는 웹 드라이버의 코드  #lxml이 html.parser더 빠르다고 함
        
    for i in soup.select("#cont_view > div.cs_area > div > div > div.ct_petitions > div.ct_petitions_area.ct_txt_left > div.ct_list1 > div > div.b_list.category.b_list2 > div.bl_body > ul > li") :    #slect 대신 find_all로 해도 됨.
            result_list.append(i.find("div", attrs = {"class": "bl_subject"}).get_text()[3:].strip())  #get_text() 와 text는 동일 기능
    time.sleep(2)

driver.close()

# 리스트를 텍스트로 변환
result_text = " "
for i in range(0, len(result_list)) :
    result_text = result_text + " " + result_list[i]


# 여러 블로그의 JPype1을 윈도우버전, 파이선 버전에 맞추어 관련 Jpype1을 인스톨했는데도 안되고
# 이리저리 삽질끝에 기존 Jpype1을 언인스톨하고,
# JPype1-py3 0.5.5.4 설치 끝에 됨. https://todaycodeplus.tistory.com/m/41 참조
# kkma.py, jvmfinder.py jvm.py 에서 java_home지정하라는데로 했었는데도 실패. jv.
# _kkma.py에서 jvmpath = "C:/Program Files/Java/jdk-17.0.1/bin/server/jvm.dll"  # 새로 추가한 라인 명환. 
# jvm.py에서  # convertStrings=True   #명환 주석처리함

Kkma = Kkma()  

result_noun  = Kkma.nouns(result_text)


# 리스트 중 한글자는 제외
sort_list = []
for i in range(0, len(result_noun)) :
    if len(result_noun[i]) >1 :
        sort_list.append(result_noun[i])
    else :
        pass

# 리스트를 텍스트로 변환
sort_text = " "
for i in range(0, len(sort_list)) :
    sort_text = sort_text + " " + sort_list[i]

# 한글 폰트 사용을 위해서 세팅
# from matplotlib import font_manager, rc
# font_path='C://Windows/Fonts/malgun.ttf'
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)
# word =  WordCloud().generate(sort_text)
# 여기부터 구름모양에 wordcloud 넣기 위함  (아직 코드만 옮김. 그림 파일 애매)
from os import path
from PIL import Image
import numpy as np
import os

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd() # __file__ 은 경로 및 파일명, path.dirname(__file__)과os.getcwd()은 경로 알기 위함
# 둘의 차이는 모르지만, print해본 결과 path.dirname(__file__)) 는 현재 파일의 상위폴더를 표시, os.getcwd() 는 현재 파일의 현재 폴더를 표시
mask = np.array(Image.open(path.join(d, 'cloud.png')))
# path.join(d, 'cloud.png')는 괄호 안에 있는 string을 join하여 한개의 경로로 만들어줌
# image.opne(경로 및 파일)은 PIL 라이브러리로서 이미지 읽음.
# np.array(image파일.jpg)는 image를 숫자(2차원 배열로 변환)
word = WordCloud(font_path='C://Windows/Fonts/malgun.ttf', mask=mask, background_color='white', colormap='winter').generate(sort_text)
# 여기까지 구름모양에 wordcloud 넣기 위함.

#원래 모양은 아래로. 네모 박스에 나옴.
# word = WordCloud(font_path='C://Windows/Fonts/malgun.ttf', background_color='white', colormap='winter').generate(sort_text)


plt.figure()
plt.axis('off')
plt.imshow(word, interpolation='bilinear') 
plt.show()
