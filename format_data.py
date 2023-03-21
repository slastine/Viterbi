import json
import re
import os

tagList = list()
wordMatrix = list()
emissionMatrix = list()
transitionMatrix = list()

f = open('data.json')
data = json.load(f)
f.close()

for i in data:
  raw = "S/start " + i["raw_text"]
  regex = "(\w+)[/](\w+)"
  matches = re.findall(regex, raw, re.MULTILINE)
  for match in matches:
    if matches != None:
      if not any(d["tag"] == match[1] for d in tagList):
        tagList.append({"tag": match[1], "frequency": 1})
      else:
        for tag in tagList:
          if tag['tag'] == match[1]:
            tag["frequency"] += 1
            break
      word = match[0].lower()
      tag = match[1]
      if not any(d["word"] == word for d in wordMatrix):
        wordMatrix.append({"word": word, tag: 1, "frequency": 1})
      else:
        for item in wordMatrix:
          if item["word"] == word:
            item["frequency"] += 1
            if tag in item.keys():
              item[tag] += 1
              break
            else:
              item[tag] = 1
              break

for i in wordMatrix:
  emissionMatrix.append({"word": i["word"]})
  for mat in emissionMatrix:
    if mat["word"] == i["word"]:
      for key in i.keys():
        for tag in tagList:
          if key == tag["tag"]:
            mat[tag["tag"]] = i[key] / i["frequency"]

for i in tagList:
  transitionMatrix.append({"tag": i["tag"], "tags": list()})
for i in range(len(data)):
  regex = "(\w+)[/](\w+)"
  raw = "S/start " + data[i]["raw_text"]
  matches = re.findall(regex, raw, re.MULTILINE)
  for word in range(len(matches)):
    if word > 0:
      for tag in transitionMatrix:
        if tag["tag"] == matches[word - 1][1]:
          if not any(d["tag"] == matches[word][1] for d in tag["tags"]):
            tag["tags"].append({"tag": matches[word][1], "frequency": 1})
          else:
            for tags in tag["tags"]:
              if tags["tag"] == matches[word][1]:
                tags["frequency"] += 1
                
for i in transitionMatrix:
  for tag in i["tags"]:
    for tagInList in tagList:
      if tagInList["tag"] == i["tag"]:
        tag["frequency"] = tag["frequency"] / tagInList["frequency"]

if os.path.exists("emit.txt"):
  os.remove("emit.txt")
f = open("emit.txt", "x")
f.write(json.dumps(emissionMatrix))
f.close()

if os.path.exists("trans.txt"):
  os.remove("trans.txt")
f = open("trans.txt", "x")
f.write(json.dumps(transitionMatrix))
f.close()
