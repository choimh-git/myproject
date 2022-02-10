import requests
import re
#import Word2Vec
from gensim.models.word2vec import Word2Vec
from selenium import webdriver
from bs4 import BeautifulSoup
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding

# res = requests.get('https://www.gutenberg.org/files/2591/2591-0.txt')  # request 로 하니 "Max retries exceeded with url"의 에러가 생겨 webdriver이용
# grimm = res.text[2801:530661]

driver = webdriver.Chrome('C://Users/20060025/test/chromedriver.exe') # 대소문자 주의.

url = "https://www.gutenberg.org/files/2591/2591-0.txt"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')  #driver.page_source 현재 조정하고 있는 웹 드라이버의 코드  #lxml이 html.parser더 빠르다고 함

grimm = soup.find("pre").get_text()[2801:530900]

driver.close()

grimm = re.sub(r'[^a-zA-Z\. ]', ' ', grimm) # 불필요한 단어 제거 #정규식 연습가능 https://www.regexpal.com/
# r 은 문자 그대로 판단. raw string 역 슬래시를 사용하기 위히??
# \.(점을 이스케이프 처리) A.B 인경우 A*B로 인식되어 AAB, ABB 등을 포함, \. 인 경우 .을 그대로 인식
# 메타문자 [ ] 문자 클래스  . (점 하나는 글자 하나를 의미) ^은 시작을 의미, [^] ^가 괄호안에 있으면 not
# 메타문자 이스케이프, 또는 메타 문자를 일반 문자로 인식하게 한다


sentences = grimm.split('. ')  # 문장 단위로 자름
data = [s.split() for s in sentences]   # split() 괄호내 공백 인 경우 스페이스, 탭, 엔터를 기준으로 split

model = Word2Vec(data,         # 리스트 형태의 데이터
                 sg=1,         # 0: CBOW, 1: Skip-gram
                 vector_size=100,     # 벡터 크기
                 window=3,     # 고려할 앞뒤 폭(앞뒤 3단어)
                 min_count=3,  # 사용할 단어의 최소 빈도(3회 이하 단어 무시)
                 workers=4)    # 동시에 처리할 작업 수(코어 수와 비슷하게 설정)


# word2vec 시각화 https://soohee410.github.io/embedding_projector 참조
# tensorboard에서 https://projector.tensorflow.org/ 에서 word2vec 모델을 시각화위해 tsv파일 생성
# from gensim.models import KeyedVectors  
# model.wv.save_word2vec_format('naver_w2v')
# 위를 실행한 뒤 아래 문장을 prompt에 넣으면 tsv 파일 2개 생성.
# python -m gensim.scripts.word2vec2tensor --input naver_w2v --output naver_w2v  


model.save('word2vec.model')
model = Word2Vec.load('word2vec.model')

model.wv['princess']  # 단어를 100차원 벡터로 변환하기
#print(model.wv.similarity('princess', 'queen'))  # 두 단어간의 코사인 유사도
#print(model.wv.most_similar('princess')) # 가장 유사한 단어 추출
# words = list(model.wv.index_to_key) 단어 리스트들


print(model.wv.most_similar(positive=['he', 'princess'], negative=['she'])) #"woman:princess = man:?" man+princess-woman


NUM_WORDS, EMB_DIM = model.wv.vectors.shape   #MODEL 의 총 단어수는 NUM_WORDS, 차원수는 EMB_DIM

# gensim으로 학습된 단어 임베딩 model.wv.vectors를 케라스의 임베딩 레이어의 가중치로 사용
emb = Embedding(input_dim=NUM_WORDS, output_dim=EMB_DIM,
                trainable=False, weights=[model.wv.vectors]) #trainable=False이면 추가학습 안함.

net = Sequential()
net.add(emb)

i = model.wv.index_to_key.index('princess')
print(net.predict([i]))   # 위에서 word2vec에서의 princess의 100차원 벡터와 동일한 값을 출력

