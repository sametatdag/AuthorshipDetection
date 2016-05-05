import sys
import codecs
import getopt
from decimal import Decimal
from json import dumps
from TagWord import TagWord


def remove_newlines(text):
  return text.replace("\n", "")

def decimal_default(obj):
  if isinstance(obj, Decimal):
    return float(obj)
  raise TypeError

def process_sentence(sentence):
  for tagword in sentence:
    uniq_words.add(tagword.word)

    # count each tag
    if tagword.tag not in tag_counts:
      tag_counts[tagword.tag] = 0
    tag_counts[tagword.tag] += 1
    combined_rep = tagword.combined_rep()

      
    # count tag-word pairs 
    if combined_rep not in tagword_counts:
      tagword_counts[combined_rep] = 0
    tagword_counts[combined_rep] += 1
    
  prev = None  
  for tagword in sentence:
    if tagword.word == "START":
      prev = "START"
      continue

    tag = tagword.tag

    pair = prev + "|" + tag

    if pair not in tag_transition_counts:
      tag_transition_counts[pair] = 0

    tag_transition_counts[pair] += 1
    prev = tag

def usage():
  print "\nUsage: /usr/bin/python2.7 train_hmm_tagger.py --training-filename <training filename> --postag-type cpostag|postag \n"

try:
  opts, args = getopt.getopt(sys.argv[1:], 't:p:h', ['training-filename=', 'postag-type='])
  if len(opts) < 2:
    usage()
    sys.exit(2)
except getopt.GetoptError as e:
  usage()
  sys.exit(2)

for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-t', '--training-filename'):
    training_filename = arg
  elif opt in ('-p', '--postag-type'):
    postag_type = arg

    if postag_type == "cpostag":
      tag_index = 3 # CPOSTAG
    else:
      tag_index = 4  # POSTAG
  else:
    usage()
    sys.exit(2)





uniq_words = set()

tag_counts = {}
tagword_counts = {}
tag_transition_counts = {}

sentence = []

for i in codecs.open(training_filename, "r", "utf-8").readlines():
  if i == "\n":
    start_tagword = TagWord("START", "START")
    end_tagword = TagWord("END", "END")

    sentence.insert(0, start_tagword)
    sentence.append(end_tagword)

    process_sentence(sentence)
    sentence = []
  else:
    line = remove_newlines(i)
    parsed = line.split("\t")

    word = parsed[1]
    tag = parsed[tag_index]

    tagword = TagWord(tag, word)
    sentence.append(tagword)

pos_tags = [
  "START", 
  "Adv", "Punc", "Noun",
  "Adj", "Verb", "Det",
  "Pron", "Postp", "Conj",
  "Ques", "Num", "Interj",
  "Dup", "Zero",
  "END"
]

pos_tags_with_start = list(pos_tags)
pos_tags_with_start.insert(0 ,"START")

probs = {}

for t in pos_tags_with_start:
  for k in pos_tags:
    tag_transition = t + "|" + k
    numerator = Decimal(tag_transition_counts.get(tag_transition, 0))
    denominator = Decimal(tag_counts.get(t, 1))
    prob = numerator / denominator
    prob_rep = k + "|" + t
    probs[prob_rep] = prob

observation_likelihoods = {}
for word in uniq_words:
  observation_likelihoods[word] = {}

  for tag in pos_tags:
    observation_likelihoods[word][tag] = 0.0
    rep = tag + "|" + word
    numerator = Decimal(tagword_counts.get(rep, 0))
    denominator = Decimal(tag_counts.get(tag, 1))
    p = numerator / denominator
    observation_likelihoods[word][tag] = p

json_tag_transitions = dumps(probs, ensure_ascii=False, default=decimal_default)
json_observation_likelihoods = dumps(observation_likelihoods, ensure_ascii=False, default=decimal_default)

with codecs.open("tag_transitions.txt", "w", "utf-8") as f:
  f.write(json_tag_transitions)
  
with codecs.open("observation_likelihoods.txt", "w", "utf-8") as f:
  f.write(json_observation_likelihoods)
