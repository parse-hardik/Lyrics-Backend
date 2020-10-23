# %cd "/content/drive/My Drive/IR/useFiles"

import numpy as np
from numpy import linalg as la
import operator
import sys

file1 = open("songsprocessed.txt",'r')
file2 = open("wordsprocessed.txt",'r')
songset1 = file1.read()
wordset1 = file2.read()
songset = songset1.split(";")
wordset = wordset1.split(",")

# print(len(songset),len(wordset))

song_number = len(songset)-1
word_number = len(wordset)

# print(sys.argv[1])

# **list of variables**

# 1.   songset - **msd songid,musicmx songid, <word,id> -> freq;** 
# 2.   wordset - **word,**
# 3.   song_name - **names of songs**
# 4.   song_word_freq= **total words in a song**
# 5.   word_song_dict= **dictionary : ith row-words, jth column-song, cell-frequency of the i-th word in j-th song**

### PRE-PROCESSING DATASET

#term document frequency table created
song_name = []
song_word_freq=[]
word_song_dict = {}
N = 0

#creating an empty dictionary corresponding to every word

for i in range(0, word_number+1):
  word_song_dict[i] = {}

#we are creating a dictionary here which stores the freq of every word occuring in the song lyrics

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
#N 

def get_songs(answer):
  file = open("answer.txt",'w')
  # s = len(answer)
  ar = ""
  for x in answer.keys():
   ar = ar + song_name[x]+" "
  file.write(ar)

### QUERY FUNCTION

def top_ten_given_query(var):

  #get query
 #query = input("Enter your query : ")
#   print(var)
  query = var
  q_size = len(query)

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

    word_doc_freq = np.zeros((song_number,q_length)) 
    counter=0
    
    for word in q_word:
      word_id = wordset.index(word)
      doc_freq = len(word_song_dict[word_id])

      idf = np.log(song_number/(doc_freq+1))

      for doc in word_song_dict[word_id]:
        tf_doc = word_song_dict[word_id][doc]/song_word_freq[doc]
        word_doc_freq[doc][counter] = tf_doc*idf
      
      counter+=1

      #cosine similarity

    q_freq = np.array(q_freq)
    similarity_dict = {}
    for i in range(0,song_number):
      denominator = la.norm(word_doc_freq[i])*la.norm(q_freq)
      if denominator == 0:
        denominator=1
      cos_inv = np.dot(word_doc_freq[i],q_freq)/denominator
      similarity_dict[i] = cos_inv
    
    sorted_dict = sorted(similarity_dict.items(),key=operator.itemgetter(1),reverse=True)
    answer = sorted_dict[0:10]
    answer = dict(answer)
  #   get_songs(answer)
    for x in answer.keys():
      print(song_name[x])
  #   return var+1

print(sys.argv[1:])

top_ten_given_query(sys.argv[1:])
# print(a)
