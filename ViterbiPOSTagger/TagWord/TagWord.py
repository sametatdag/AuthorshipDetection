class TagWord:
  def __init__(self, tag, word):
    self.tag = tag
    self.word = word

  def __repr__(self):
    return "<%s,%s>" % (self.tag, self.word)

  def __str__(self):
    return "<%s,%s>" % (self.tag, self.word)

  def combined_rep(self): # <Adv,Hayir> tagword is represented as Adv|Hayir
    return self.tag + "|" + self.word

  tag = ""
  word = ""
