import re
import snowballstemmer
with open("nlp.txt", encoding = "utf-8") as f:
    content = f.read()
result = re.sub("([.;:!?]) (\s*[A-Z])", r"\1\n\2", content)
# print(result)

word = re.sub("(\s)", r"\1\n", result)
print(word)

stemmer = snowballstemmer.stemmer("english")
for line in word.split("\n"):
    if line == "":
        continue
    for word in line.split(" "):
        print(word, stemmer.stemWord(word))
    print()