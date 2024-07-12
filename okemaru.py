import urllib
import urllib.request
import urllib.parse
import urllib.error
import re
from queue import SimpleQueue
import requests
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def get_pages(title):
    base_url = "https://www.weblio.jp/content/"
    url = base_url + urllib.parse.quote(title)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "ja",
        "Accept-Charset": "utf-8",
    }
    response = requests.get(url)
    if response.status_code == 200:
      req = urllib.request.Request(url, headers=headers, method="GET")
      with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return(body)
    else:
       print("failed")

def get_japanese(user_word):
  japanese=[]
  new_japanese=[]
  count=0
  delete_list=[]
  count_list=[]
  pat_japanese = re.compile(r"[\u3041-\u3094\u30A1-\u30F4\u4E00-\u9FFF]+")
  result = get_pages(user_word)
  japanese=pat_japanese.findall(result)
  for i in japanese:
    if "の意味" in i:
        delete_list.append(i)
    elif "解説" in i:
        delete_list.append(i)
    elif "辞" in i:
        delete_list.append(i)
    elif "翻訳"  in i:
        delete_list.append(i)
    elif "語" in i:
        delete_list.append(i)
    elif "検索"in i:
        delete_list.append(i)
    elif "とは"in i:
        delete_list.append(i)
  for i in delete_list:
      japanese.remove(i)
  for i in japanese:
      if i not in new_japanese:
          new_japanese.append(i)
  for i in range(len(new_japanese)):
      if "不適切な項目" in new_japanese[i]:
          new_japanese=new_japanese[:i+1]
          break
  for i in range(len(new_japanese)):
    if "ログイン" in new_japanese[i]:
      count_list.append(i)
    if "凡例" in new_japanese[i]:
        count_list.append(i)
        new_japanese=new_japanese[:count_list[0]]+new_japanese[count_list[1]+1:]
        break
  return(new_japanese)

def make_file():
  basic_list=["穏やか","華やか","明るい","暗い","美しい"]
  basic_file_list=[]
  for a in basic_list:
    basic_file_list.append(a+".txt")
  added_basic_list=[["優しい","落ち着いた","静か"],
                    ["きらきら","騒がしい","自信"],
                    ["活発な","元気な","鮮やかな"],
                    ["憂鬱","いやな","悲しい"],
                    ["繊細な","きれい","妖艶"]]
  current_dir = os.path.dirname(os.path.abspath(__file__))
  for i in range(len(basic_list)):
    filename=os.path.join(current_dir, basic_file_list[i])
    if not os.path.isfile(filename):
      sentence=""
      for word in get_japanese(basic_list[i]):
          sentence+=","
          sentence+=word
      for added in added_basic_list[i]:
        for word in get_japanese(added):
          sentence+=","
          sentence+=word   
      with open(filename, 'w',encoding="utf-8") as f:
       f.write(sentence + '\n')
make_file()

basic_list=["穏やか","華やか","明るい","暗い","美しい"]
basic_file_list=[]
for a in basic_list:
  basic_file_list.append(a+".txt")
basic_dict={}
count=0
for i in basic_list:
    basic_dict[i]=""
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
for file in basic_file_list:
    filepath = os.path.join(current_dir,basic_file_list[count])
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        basic_dict[basic_list[count]]=content.split(",")
    count+=1

def near(word):
    vectorizer = CountVectorizer()
    basic_list = ["穏やか", "華やか", "明るい", "暗い", "美しい"]
    basic_list.append(word)
    basic_dict[word]=get_japanese(word)
    basic_list_list = []
    for i in basic_list:
        basic_list_list.append(" ".join(basic_dict[i]))
    X = vectorizer.fit_transform(basic_list_list)
    similarity_matrix = cosine_similarity(X, X)

    # basic_list_listの長さに合わせてループを行い、最も類似度が高い奴を表示する
    answer=0
    keep=0
    for i in range(len(basic_list_list)):
        for j in range(i+1, len(basic_list_list)):
            printing=f"{basic_list[i]} と {basic_list[j]} の類似度: {similarity_matrix[i,j]:.2f}"
            if word in printing:
                a=similarity_matrix[i,j]
                if a>keep:
                    keep=a
                    if basic_list[i]==word:
                        answer=basic_list[j]
                    else:
                        answer=basic_list[i]
    return(answer)

def recommend(mood,famous):
    music_list=[["展覧会の絵より「第一プロムナード」,https://youtu.be/TJd67EBR2R0?si=xE5eywPGpe1pM-T2","シベリウス「交響曲第二番」より第一楽章,https://youtu.be/GNKmfzDI3BU?si=MygX2j7pX9JyQT6V"],
                ["アルルの女より「ファランドール」,https://youtu.be/JnPpFUmN6lY?si=pnASoGvJckwEhVrZ","イーゴリ公より「韃靼人の踊り」,https://youtu.be/wiexn6O9To4?si=dYdYmuIRaZNDSR7q"],
                ["くるみ割り人形より「花のワルツ」,https://youtu.be/XgtboV5Ycnw?si=OWMxfuZFUkDYn_U0","ニュルンベルクのマイスタージンガーより「第一幕への前奏曲」,https://youtu.be/MYXFp5O75Ow?si=ZNdHDqM1ojb4bC_j"],
                ["ベートーヴェン「交響曲第五番」より第一楽章,https://youtu.be/4du7kv9gIeo?si=BrGjIA6WRCmv9Tfm","交響詩「フィンランディア」,https://youtu.be/D8DxmUutTgc?si=inOZ_9Kp-4Xkzz15"],
                ["白鳥の湖より「憧憬」,https://youtu.be/LKFlSoLGXxo?si=6ac9AAxkhSvnstlw","死の舞踏,https://youtu.be/71fZhMXlGT4?si=eYFAWXjDkou2i7mk"]]
    for i in range(len(basic_list)):
        if mood==basic_list[i]:
            mood_point=i
            break
        if famous=="はい":
            famous_point=0
        else:
            famous_point=1
    return music_list[mood_point][famous_point].split(",")
    


class RestaurantReserveStateMachine:
  def __init__(self):
    # 状態の種類
    # 'ASK_NAME'：ユーザの氏名を質問（初期状態）
    # 'ASK_DATE'：予約日を質問
    # 'ASK_PEOPLE'：人数を質問
    # 'CONFIRMATION'：予約内容を確認
    # 'COMPLETION'：完了（終了状態）
    self.states = ['ASK_MOOD', 'ASK_FAMOUS', 'CONFIRMATION', 'COMPLETION']
    # 初期状態
    self.current_state = 'ASK_MOOD'
    # 聞き取りした情報を保持するためのインスタンス変数
    self.mood = None
    self.famous = None
    self.country = None
    # 遷移状態の一覧
    # dict の value はインスタンスメソッドを呼び出している
    self.transitions = {
      # 'ASK_NAME' が呼び出されたときには　'handle_ask_name()' 呼び出される
      'ASK_MOOD': self.handle_ask_mood,
      'ASK_FAMOUS': self.handle_ask_famous,
      'CONFIRMATION': self.handle_confirmation,
    }

  # 入力された氏名を処理
  def handle_ask_mood(self, user_input):
    # ユーザの入力をインスタンス変数　'name' に代入
    self.mood = near(user_input)

    # ２つの値を戻り値として返す．１つ目はシステムの応答，２つ目は次の状態
    return "有名な曲が好みですか？「はい」か「いいえ」でお答えください", 'ASK_FAMOUS'

  # 入力された日付を処理
  def handle_ask_famous(self, user_input):
    self.famous = user_input
    if user_input=="はい" or user_input=="いいえ":
      return  f"情報を提供頂きありがとうございました．教えていただいた内容を確認させて頂きます．\n" + \
      f"System: 雰囲気「{self.mood}」\nSystem: 有名なほうがいいか「{self.famous}」\n" + \
      f"System: 以上で間違いございませんでしょうか?\n" + \
      "System: 「はい」か「いいえ」で回答ください．", 'CONFIRMATION'
    else:
      return  "お手数ですがもう一度「はい」か「いいえ」でお答えください","ASK_FAMOUS"
  # 予約内容の確認
  def handle_confirmation(self, user_input):
    # ユーザの入力を確認
    if user_input == "はい":
      return f"入力いただいた内容でしたら {recommend(self.mood,self.famous)} が気に入っていただけると思います！", 'COMPLETION'
    # 初期状態から再スタート
    elif user_input == "いいえ":
      return "承知いたしました．お手数ですが改めて情報提供をお伺いします．まずはお客様の好きな曲の雰囲気を一語で教えてください（例：明るい、不思議）", 'ASK_MOOD'
    # 再度確認を行う
    else:
      return "お手数ですが再度確認させて頂きます．" + \
      f"System: 雰囲気：「{self.mood}」\nSystem: 有名なほうがいいか：「{self.famous}」\n" + \
      f"System: 以上で間違いございませんでしょうか?\n" + \
      "System: 「はい」か「いいえ」で回答ください．", 'CONFIRMATION'

  # システムの応答を取得
  def get_response(self, user_input):
    # 現在の状態 'current_state' に基づいてインスタンスメソッドが呼び出される
    # その際の引数としてユーザの入力 'user_input' が渡される
    # 戻り値はシステムの応用と次の状態
    response, next_state = self.transitions[self.current_state](user_input)
    # システムの状態を更新
    self.current_state = next_state
    return response

def talk():
  dialog_system = RestaurantReserveStateMachine()

# 最初のシステムからの問いかけ
  print("System: こんにちは，クラシックおすすめシステムの「おけまる」です．")
  print("System: まずはお客様の好きな曲の雰囲気を一語で教えてください（例：明るい、不思議）．")

  # 状態が 'COMPLETION' となるまで対話を継続
  while dialog_system.current_state != 'COMPLETION':
    user_input = input('User:')
    response = dialog_system.get_response(user_input)
    print('System:', response)



talk()