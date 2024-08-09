# 必要モジュールのインポート
import os
import re

def load_file(file_path):
    with open(file_path, "r",encoding='CP932') as f:
        text = f.read()
        if "lines:" in text:
            text = text.split("lines:")[1]
    return text

def preprocess_text(file_path):
    contents = []
    files = os.listdir(file_path)
    # 削除する記号のコンパイル
    code_regex = re.compile('[\t\s!"#$%&\'\\\\()*+,-./:;；：<=>?@[\\]^_`{|}~○｢｣「」〔〕“”〈〉'\
        '『』【】＆＊（）＄＃＠？！｀＋￥¥％♪…◇→←↓↑｡･ω･｡ﾟ´∀｀ΣДｘ⑥◎©︎♡★☆▽※ゞノ〆εσ＞＜┌┘]')
    # 削除する数字のコンパイル
    num_regex = re.compile('\d+,?\d*')
    for file in files:
        target_file_path = os.path.join(file_path, file)
        text = load_file(target_file_path)
        # 文単位で分割
        text = text.split("\n")
        for i in range(len(text)):
            # 空白行を削除
            if text[i] == "":
                continue
            # 記号を削除
            text[i] = code_regex.sub("", text[i])
            # 数字を削除
            text[i] = num_regex.sub("", text[i])
            # 小文字に変換
            text[i] = text[i].lower()
            contents.append(text[i])
    return contents








# データの前処理