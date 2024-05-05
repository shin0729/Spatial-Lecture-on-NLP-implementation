import re
with open("nlp.txt", encoding = "utf-8") as f:
    content = f.read()
char_list = []
for ch in content:
    char_list.append(ch)
for i in range(len(char_list)):
    if char_list[i] in [".", ";", ":", "?", "!"]:
        if char_list[i+1] == " ":
            if char_list[i+2].isupper() == True:
                char_list.insert(i+2, "\n")
result = "".join(char_list)
print(result)

#一回リストにしてしまうのはメモリ効率が悪いので他の方法を考える．→正規表現の後方参照というのがあるのか