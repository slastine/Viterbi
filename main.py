import json

emissionMatrix = list()
transitionMatrix = list()

f = open('trans.txt')
transitionMatrix = json.load(f)
f.close()

f = open('emit.txt')
emissionMatrix = json.load(f)
f.close()

test = input("Enter a sentence to receive POS tags: ")
raw = test.split(" ")
for i in raw:
  prevTag = "start"
  trans = list()
  emit = list()
  allTags = list()
  for transit in transitionMatrix:
    if transit["tag"] == prevTag:
      for tags in transit["tags"]:
        trans.append({"tag": tags["tag"], "prob": tags["frequency"]})
  for emis in emissionMatrix:
    if emis["word"] == i:
      for tags in emis.keys():
        if tags != "word":
          emit.append({"tag": tags, "prob": emis[tags]})
  for t in trans:
    for e in emit:
      if t["tag"] == e["tag"]:
        final = t["prob"] * e["prob"]
        allTags.append({"tag": t["tag"], "prob": final})
  largestTag = ""
  largestTagProb = 0
  for all in allTags:
    if all["prob"] > largestTagProb:
      largestTag = all["tag"]
      largestTagProb = all["prob"]
  print(i + ": " + str(largestTag))
