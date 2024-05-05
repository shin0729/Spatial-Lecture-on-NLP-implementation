import re
with open("nlp.txt", encoding = "utf-8") as f:
    content = f.read()
result = re.sub("([.;:!?]) (\s*[A-Z])", r"\1\n\2", content)
# print(result)

word = re.sub("(\s)", r"\1\n", result)
print(word)

#→正規表現の後方参照というのがあるのか．re,sub()の第二引数にr"\1\n\2"というのがある．これは，正規表現の第一引数で指定したグループを後方参照している．第一引数は括弧でグループ分けされている．\1は最初のグループ，\2は２番目のグループを指す．