import xml.etree.ElementTree as ET
tree = ET.parse('nlp.txt.xml')
root = tree.getroot()
list = root.findall('.//token')
#<word>タグの値を取得
for word in list:
    print(word.findtext('word'))

#これもライブラリを使っているので，実装しただけ．xml.etree.ElementTreeは理解した方がいいのかなぁ