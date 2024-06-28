import re
from pyknp import KNP

def analyze_pas(sentence):
    knp = KNP(option = '-tab -anaphora', jumanpp=False)
    result = knp.parse(sentence)
    for b in  result.bnst_list():
        match = re.search(r"<項構造:(.+)>", b.spec())
        if match:
            pas =  match.group(1)
            items = pas.split(":")
            print(b.bnst_id, items)

if __name__=="__main__":
    sentence = "アテンションヘッドは、トランスフォーマーモデルにおいて異なる視点からデータを分析するための重要な構成要素です。マルチヘッドアテンションにより、モデルは入力の多様な側面を同時に考慮し、より豊かな情報を学習できるようになります。これにより、自然言語処理タスクにおいて高い性能を発揮することができます。"
    analyze_pas(sentence)
    