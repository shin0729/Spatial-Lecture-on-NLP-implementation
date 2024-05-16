import xml.etree.ElementTree as ET
tree = ET.parse('nlp.txt.xml')
root = tree.getroot()
list = root.findall('.//token')
for word in list:
    print(word.findtext('word'))
    print(word.findtext('lemma'))
    print(word.findtext('POS'))

#これもライブラリを使っているので，実装しただけ．xml.etree.ElementTreeは理解した方がいいのかなぁ