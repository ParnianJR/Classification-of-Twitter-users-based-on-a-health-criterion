import unicodedata
from Constants import data_columns, diseases_dict, data_path, stopwords_set, punctuation_set, emoticon_re, word_re
import pandas as pd
import re
# import string
import contractions

punctuations = {x for x in punctuation_set if (x != '#' and x != '@')}

punctuations_string = ''.join(punctuations)
stopwords = stopwords_set.remove('not')


def remove_tagged_account(tweet):
  return ' '.join([token if token[0]!='@'  else '' for token in tweet.split()])

def strip_accents(text):
    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")
    return str(text)


def expand_contractions(text):
    return contractions.fix(' '.join(text.split(' ')))


def remove_url(text):
    return re.sub(r'http\S+', '', text)


def alter_punctuations(text):
    # add space before and after each punctuation if it's not an emoticon
    # if it's @ or # , do not change it s its a person who's been tagged or a hashtag
    words = text.split()
    altered_words = []

    for word in words:
        for punc in punctuation_set:
            if punc in word:
                if emoticon_re.search(word):
                    pass
                else:
                    word = word.replace(punc, ' ' + punc + ' ')
        altered_words.append(word)

    return ' '.join(' '.join(altered_words).split())



def remove_stopwords(tweet):
  words = [word if word not in stopwords_set else '' for word in tweet.split()]
  return ' '.join((' '.join(words)).split())

def remove_punctuation(tweet):
  words = word_re.findall(tweet)
  words = map((lambda word: word if emoticon_re.search(word) else word.lower().translate(str.maketrans('', '', punctuations_string))), words)
  return ' '.join(words)

def normalize_tweet(tweet):
  return remove_stopwords(remove_punctuation(remove_url(strip_accents(expand_contractions(remove_tagged_account(tweet.replace("&amp;", " and ")))))))


def process_tweet(tweet):
    return alter_punctuations(remove_url(expand_contractions(strip_accents(tweet.replace("&amp;", " and ")))))



def min_distance(text, w1, w2):
    # two list to store each word appearance index in the text
    w1_appearance = list()
    w2_appearance = list()

    if len(w1.split()) == 1:
        w1_appearance = single_word_appearance(text, w1)
    else:
        w1_appearance = sequence_appearance(text, w1)

    if len(w2.split()) == 1:
        w2_appearance = single_word_appearance(text, w2)
    else:
        w2_appearance = sequence_appearance(text, w2)

    # check if two given word have appeared in the text or not (if not, return False)
    if len(w1_appearance) == 0 or len(w2_appearance) == 0:
        return False

    # pointer two W1_appearance and w2_appearance respectfully (currently, which block we are at)
    pointer_w1, pointer_w2 = 0, 0
    # value of the current pointed block of eah w1_appearance and w2_appearance list respectfully
    val_w1, val_w2 = 0, 0

    # to check when these two list has ended in the while loop 
    n, m = len(w1_appearance), len(w2_appearance)

    # to check if two words has appeared in order, if they did, their distance would be less than assigned int to the min
    min = len(text.split())

    while pointer_w1 < n and pointer_w2 < m:

        # assign the proper value to val_w1 and val_w2 based on the pointers to the w1_appearance and w2_appearance lists
        val_w1, val_w2 = w1_appearance[pointer_w1], w2_appearance[pointer_w2]

        # print(f'w1: {val_w1}\t w2: {val_w2}\t pointer_w1: {pointer_w1}\t pointer_w2: {pointer_w2}')

        # as w2 must appear after the w1, this index of w2 is not proper, go to the next one and go to the loop's begining
        if val_w1 > val_w2:
            pointer_w2 += 1
            continue

        # w2 appeared after w1
        if val_w1 < val_w2:
            # print(f'{min} > {val_w2-val_w1-1} : {min > val_w2-val_w1-1}')

            # is this distance less than what has been saved for the min?
            if min > val_w2 - val_w1 - 1:
                # then update min to this distnace
                min = val_w2 - val_w1 - 1
            # go to the next index of w1
            pointer_w1 += 1

    #  if min distance has been altered, return it
    if min < len(text.split()):
        return min
    else:
        # min distance has not been altered, it means that these two words have not appeared in order, so return False
        return False


def single_word_appearance(text, w):
    # add each appearance index
    appeared_index = list()

    # the text's list of words
    text_words = [word.lower() for word in text.split()]
    # convert  the input word to the lowercase 
    w = w.lower()
    punctuation_count = 0

    for index, word in enumerate(text_words):

        if '#' in word:  # if the given word is appeared as a hashtag
            word = word.replace('#', '')

        if word in punctuation_set:  # do not count the punctuations in the indexing
            punctuation_count += 1
            continue

        if word == w:  # if the word is appeared, add the index
            appeared_index.append(index - punctuation_count)

    return appeared_index  # return the filled list


def sequence_appearance(text, sequence):
    # a list to store appeared index (index of the first term)
    appearance_index = list()

    # split text into its words
    text_words = [word.lower() for word in text.split()]
    # len of the given text in term of word count
    text_len = len(text_words)

    # split the given sequence into its words
    sequence_words = [word.lower() for word in sequence.split()]
    # len of the given sequence in term of its word count
    sequence_len = len(sequence_words)

    punctuation_count = 0

    for index, word in enumerate(text_words):
        if '#' in word:
            word = word.replace('#', '')
        if word in punctuation_set:
            punctuation_count += 1
            continue
        if (word == sequence_words[0]) and (index + sequence_len < text_len):
            # it is possible that this "word" is the start of an appearance of the given sequence in the given text 
            all_match = True
            # check if the rest of the sentence match the rest of the sequence or not
            for sequence_w, text_w in zip(sequence_words[1:], text_words[index + 1: index + sequence_len]):
                if sequence_w != text_w:
                    all_match = False
                    break

            if all_match:  # if they fully match, add the index of first sequence's term to the appearance_index list
                appearance_index.append(index - punctuation_count)

    return appearance_index

# if __name__ == '__main__':
  # st = '@JuliaBradbury @TheyaHealthcare I was diagnosed with cancer in both breasts in August this year although caught early it was invasive surgery I am a month on from surgery and am still in awful pain ! The surgical bras are torture! Albeit my lumps are taken away it’s rare to have in both at the same time! Big 🥰'
  # print(st)
  # print(remove_stopwords(remove_punctuation(remove_url(strip_accents(expand_contractions(st.replace("&amp;", " and ")))))))
  
  # print(normalize_tweet(st))












