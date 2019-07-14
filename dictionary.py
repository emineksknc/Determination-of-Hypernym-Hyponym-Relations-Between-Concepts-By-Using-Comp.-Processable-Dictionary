import pymongo
from snowballstemmer import stemmer
import os
def clean_folder(new):
    files = os.listdir(new)
    for f in files:
        location = new + '/' + f
        if os.path.isdir(location) == True:
           clean_folder(location)
        else:
            if location.endswith(".txt") == True:
                os.remove(location)
                break





def create_file(file_name,word,word_name):
    path = 'C:/Users/Emine/Desktop/NLP/nlp-ödev/proje/hypernym/'
    new_path = path + file_name + '.txt'
    file = open(new_path, 'a')
    file.write('\n')
    file.write(word_name)
    file.write(":")
    file.write(word)


#Rule-1:The concept of the words ending with the word “bilimi” is determined as “BİLİM”.

def rule1(word,word_name):
    if word.endswith('bilimi'):
        create_file("rule-1/BİLİM",word,word_name)



# (nltk  stemmer was not efficient.)
#Rule-2:If a definiton of a word end with “olanlardan biri”, “olanlardan bazısı”, “olanlardan her biri” ,
# the word before these word phrases that processed according to the hypernym and the hypernym must be obtained.
def rule2(word,word_name):

    if word.endswith('olanlardan biri') or word.endswith('olanlardan bazısı'):
        words = word.split()
        word_new = words[len(words) - 3]
        word_new = find_stem.stemWords(word_new.split())
        for word1 in word_new:
            word1_name = 'rule-2/' + word1

            create_file(word1_name, word, word_name)


    if word.endswith('olanlardan her biri'):
        words = word.split()
        word_new = words[len(words) - 4]
        word_new = find_stem.stemWords(word_new.split())
        for word1 in word_new:
            word1_name = 'rule-2/' + word1
            create_file(word1_name, word, word_name)


#Rule-3:If a definiton of a word end with “biri”, “bazısı”, “her biri” ,the word before these words that processed
# according to the hypernym like that dropping effixes that “-lerin”, ”-ların”, “-lerinin”, “larının”, “-lerinden” , “-larından”,etc.
def rule3(word,word_name):
    if word.endswith('biri') or word.endswith('bazısı'):
        words = word.split()
        word_new = words[len(words) - 2]
        word_new = find_stem.stemWords(word_new.split())
        for word1 in word_new:
            word1_name = 'rule-3/' + word1
            create_file(word1_name, word, word_name)


    if word.endswith('her biri'):
        words = word.split()
        word_new = words[len(words) - 3]
        word_new = find_stem.stemWords(word_new.split())
        for word1 in word_new:
            word1_name = 'rule-3/' + word1
            create_file(word1_name, word, word_name)


#Rule-4:If a definiton of a word end with “kimse”,hypernym of word is “kişi”.

def rule4(word,word_name):
    if word.endswith('kimse'):
        word1_name = 'rule-4/kişi'
        create_file(word1_name, word, word_name)

#Rule-5:If a definiton of a word end with “işi”,hypernym of word is “iş”.

def rule5(word,word_name):
    if word.endswith('işi'):
        word1_name = 'rule-5/iş'
        create_file(word1_name, word, word_name)


#Rule-6:If a definiton of a word end with “tümü”,the word before that word processed according to the hypernym like that
# dropping effixes that “-lerin”, ”-ların”, “-lerinin”, “larının”.

def rule6(word,word_name):

    if word.endswith('tümü'):
        words = word.split()
        word_new = words[len(words)-2]

        if word_new.endswith('lerin'):
            word_new = word_new.replace('lerin','')
        else:
            if word_new.endswith('lerinin'):
                word_new = word_new.replace('lerinin','')
            else:
                if word_new.endswith('ların'):
                    word_new = word_new.replace('ların','')
                else:
                    if word_new.endswith('larının'):
                        word_new = word_new.replace('larının','')

        word1_name = 'rule-6/'+ word_new
        create_file(word1_name, word, word_name)




#Rule-7:If a definiton of a word end with “değil”, hypernym couldn’t be obtained.

def rule7(word,word_name):
    if word.endswith('değil'):
        word1_name = 'rule-7/değil'
        create_file(word1_name, word, word_name)



#Rule-8:If a definiton of a word end with “hepsi”, hypernym were obtained “grup”.

def rule8(word,word_name):
    if word.endswith('hepsi'):
        word1_name = 'rule-8/grup'
        create_file(word1_name, word, word_name)

#Rule-9:If a definiton of a word end with “vb.” the word before that word processed according to the hypernym but could not be detected like this word in this dictionary.

def rule9(word,word_name):
    if word.endswith('vb.'):
        words = word.split()
        word_new = words[len(words) - 2]
        word1_name = 'rule-9/vb'
        create_file(word1_name, word, word_name)


    if word.find('vb.') != -1:
        word1_name = 'rule-9/vb'
        create_file(word1_name, word, word_name)



try:
    d = "C:/Users/Emine/Desktop/NLP/nlp-ödev/proje/hypernym"

    find_stem = stemmer('turkish')
    location = "mongodb://localhost:27017"

    client = pymongo.MongoClient(location)
    database = client['Dictionary']
    collection = database['Words5']



    for word in collection.find():
        #clean_folder(d)  # should use for cleaning hypernym folder
        word_name = word.get('Name')

        word = word.get('Definitions')


        for x in word:
            word_term = x.get('Term')


            rule1(x.get('Explanation'), word_name)
            rule2(x.get('Explanation'), word_name)
            rule3(x.get('Explanation'), word_name)
            rule4(x.get('Explanation'), word_name)
            rule5(x.get('Explanation'), word_name)
            rule6(x.get('Explanation'), word_name)
            rule7(x.get('Explanation'), word_name)
            rule8(x.get('Explanation'), word_name)
            rule9(x.get('Explanation'), word_name)






except Exception as err:
    print(err)
    pass


