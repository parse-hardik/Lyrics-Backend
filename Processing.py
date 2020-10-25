# %cd "/content/drive/My Drive/IR/useFiles"
"""
Modules
numpy
operator
json
sys
math
"""

import numpy as np
from numpy import linalg as la
import operator
import json
import sys
import math
try:
    from stemming.porter2 import stem
except ImportError:
    print('You need to install the following stemming package:')
    sys.exit(0)

#file1 = open("songsprocessed.txt",'r')
file2 = open("wordsprocessed.txt",'r')
#songset1 = file1.read()
wordset1 = file2.read()
#songset = songset1.split(";")
wordset = wordset1.split(",")

# print(len(songset),len(wordset))

#song_number = len(songset)-1
#word_number = len(wordset)

# print(sys.argv[1])
"""
VARIABLES

# 1.   wordset - **collection of all the words to be used in our model** : List
# 2.   song_name - **names of songs** : List
# 3.   song_word_freq= **total words in a song** : List
# 4.   word_song_dict= **dictionary : ith row-words, jth column-song, cell-frequency of the i-th word in j-th song** : Dictionary

### PRE-PROCESSING DATASET

#term document frequency table created
# song_name = []
# song_word_freq=[]
# word_song_dict = {}
# N = 0

# #creating an empty dictionary corresponding to every word

# for i in range(0, word_number+1):
#   word_song_dict[i] = {}

FILES

# 1. dict.txt : we have created a dictionary here which stores the freq of every word occuring in the song lyrics
# 2. names.txt : a list of song names corresponding to the indices
# 3. freq.txt : frequency list of number of words each song contains

FUNCTIONS 

# 1. top_ten_given_query(query) : takes the query and prints the top ten songs which are similar to the query using tf-idf method and cosine similarity
      input parameters : list of strings(words)
      output : none
# 2. query_processing(lyrics) : takes the input string and performs pre-processing on the words
      input parameters : string
      output : list of strings(words)

"""
# def get_songs(answer):
#   file = open("answer.txt",'w')
#   # s = len(answer)
#   ar = ""
#   for x in answer.keys():
#    ar = ar + song_name[x]+" "
#   file.write(ar)

### QUERY FUNCTION

# PRE_PROCESSING FUNCTION

"""
def pre_processing():  
  for i in range(0, song_number):
    song_details = songset[i].split(',')
    song_name.append(song_details[1])
    l = len(song_details)
    total_words = 0
    for j in range(2,l):
      worddata = song_details[j].split(':')
      index = int(worddata[0])
      freq = int(worddata[1])
      word_song_dict[index][i] = freq
      total_words+=freq
    song_word_freq.append(total_words)
    N+=total_words
"""

def top_ten_given_query(query):

  #get query
 #query = input("Enter your query : ")
#   print(var)
  q_size = len(query)
  with open("dict.txt","r") as file:
    word_song_dict = json.load(file)
    file.close()
  with open("names.txt","r") as file:
    song_name = json.load(file)
    file.close()
  with open("freq.txt","r") as file:
    song_word_freq = json.load(file)
    file.close()
  #get query words present in corpus
  q_dict = {}
  s = False
  for i in range(0,q_size):
    if query[i] in wordset1:
      s = True
      if query[i] in q_dict:
        q_dict[query[i]]+=1
      else:
        q_dict[query[i]]=1

  if s==False:
    print('No songs available')

  
  else:
    q_word=[]
    q_freq=[]
    for word in q_dict.keys():
      q_word.append(word)
      q_freq.append(q_dict.get(word))
    q_length = len(q_word)  #relevant query length

    #tf-idf calculation 

    word_doc_freq = np.zeros((210519,q_length)) 
    counter=0
    
    for word in q_word:
      word_id = str(wordset.index(word)+1)

      doc_freq = len(word_song_dict[word_id])

      idf = np.log(210519/(doc_freq+1))

      for doc in word_song_dict[word_id]:
        tf_doc = word_song_dict[word_id][doc]/song_word_freq[int(doc)]
        word_doc_freq[int(doc)][counter] = tf_doc*idf
      
      counter+=1

    #cosine similarity

    q_freq = np.array(q_freq)
    similarity_dict = {}
    for i in range(0,210519):
      denominator = la.norm(word_doc_freq[i])*la.norm(q_freq)
      if denominator == 0:
        denominator=1
      cos_inv = np.dot(word_doc_freq[i],q_freq)/denominator
      similarity_dict[i] = cos_inv

    sorted_dict = sorted(similarity_dict.items(),key=operator.itemgetter(1),reverse=True)
    answer = sorted_dict[0:10]
    answer.reverse()
    # for i in range(0,10):
    #   print(answer[i])
    answer = dict(answer)
  #   get_songs(answer)
    for x in answer.keys():
      print(song_name[x])
  #   return var+1

def query_processing(lyrics):
    
    # remove end of lines
    lyrics_flat = lyrics.replace('\r', '\n').replace('\n', ' ').lower()
    lyrics_flat = ' ' + lyrics_flat + ' '
    #print("check1")
    # special cases (English...)
    lyrics_flat = lyrics_flat.replace("'m ", " am ")
    lyrics_flat = lyrics_flat.replace("'re ", " are ")
    lyrics_flat = lyrics_flat.replace("'ve ", " have ")
    lyrics_flat = lyrics_flat.replace("'d ", " would ")
    lyrics_flat = lyrics_flat.replace("'ll ", " will ")
    lyrics_flat = lyrics_flat.replace(" he's ", " he is ")
    lyrics_flat = lyrics_flat.replace(" she's ", " she is ")
    lyrics_flat = lyrics_flat.replace(" it's ", " it is ")
    lyrics_flat = lyrics_flat.replace(" ain't ", " is not ")
    lyrics_flat = lyrics_flat.replace("n't ", " not ")
    lyrics_flat = lyrics_flat.replace("'s ", " ")
    # remove boring punctuation and weird signs
    punctuation = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')',
                   '{', '}', '/', '\\', '_', '|', '-', '@', '#', '*')
    for p in punctuation:
        lyrics_flat = lyrics_flat.replace(p, '')
    words = filter(lambda x: x.strip() != '', lyrics_flat.split(' '))
    # stem words
    words = map(lambda x: stem(x), words)
    list_words = []
    for w in words:
        #print(w)
        list_words.append(w)
    return list_words
#print(sys.argv[1:])
s=""
for i in range(1,len(sys.argv[1:])+1):
  s = s+sys.argv[i]
  s = s+" "
top_ten_given_query(query_processing(s))
# print(a)
