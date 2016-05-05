import sys
import getopt
import codecs


def usage():
  print "\nUsage: /usr/bin/python2.7 evaluate_hmm_tagger.py --output-filename <output filename> \n"

try:
  opts, args = getopt.getopt(sys.argv[1:], 'o:h', ['output-filename='])
  if len(opts) < 1:
    usage()
    sys.exit(2)
except getopt.GetoptError as e:
  usage()
  sys.exit(2)

for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-p', '--output-filename'):
    output_filename = arg
  else:
    usage()
    sys.exit(2)


def remove_newlines(text):
  return text.replace("\n", "")

total = 0
correctly_estimated = 0

pos_tags = [
  "Adv", "Punc", "Noun",
  "Adj", "Verb", "Det",
  "Pron", "Postp", "Conj",
  "Ques", "Num", "Interj",
  "Dup", "Zero"
]

confusion = {}
for tag in pos_tags:
  confusion[tag] = {}
  for t in pos_tags:
    confusion[tag][t] = 0

for i in codecs.open(output_filename, encoding="utf-8").readlines():
  if i != "\n":
    line = remove_newlines(i)
    parsed = line.split("\t")

    word, estimated_tag, true_tag = parsed

    if word not in ["START", "END"]:
      confusion[true_tag][estimated_tag] += 1
      total += 1
      if estimated_tag == true_tag:
        correctly_estimated += 1

print "\n\n\tACCURACY"
# print overall accuracy
print "\t(correct/total) =>\t%d / %d = %.2f%%\n\n" % (correctly_estimated, total, float(correctly_estimated)/total*100)

print "\n\n\tCONFUSION MATRIX\n"

# print confusion matrix
for tag in pos_tags:
  sys.stdout.write("\t%s" % tag)
sys.stdout.write("\n")
for tag in pos_tags:
  sys.stdout.write("%s\t" % tag)
  for t in pos_tags:
    # sys.stdout.write("%s\t" % t)
    sys.stdout.write("%s\t" % str(confusion[tag][t]))
  sys.stdout.write("\n")
