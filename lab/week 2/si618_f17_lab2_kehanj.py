#!/usr/bin/python

'''
An old version was created by Dr. Yuhang Wang

'''

import mrjob
from mrjob.job import MRJob
import re

WORD_RE = re.compile(r'\b[\w\']+\b')

class BigramCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    words = WORD_RE.findall(line)
    # +++your code here+++
    for i in range(len(words) - 1):
    	yield str(words[i]).lower() + " " + str(words[i + 1]).lower(), 1

  def combiner(self, bigram, counts):
    # +++your code here+++
    yield bigram, sum(counts)
        
  def reducer(self, bigram, counts):
    # +++your code here+++
    yield bigram, str(sum(counts))

if __name__ == '__main__':
  BigramCount.run()