# import os
import re
import string
from nltk.corpus import stopwords

diseases_list = ['cancer', 'hypertension', 'hiv', 'hyperlipidemia', 'diabetes', 'depression', 'asthma', 'arthritis',
                 'anxiety']

headers = ['username', 'data', 'label']

diseases_dict = {'cancer': ['cancer'],
                 'hypertension': ['hypertension', 'hypertention', 'high blood pressure', 'high bp'],
                 'hiv': ['hiv', 'aids'],
                 'hyperlipidemia': ['hyperlipidemia', 'lipid disorder', ' hypercholesterolemia',
                                    'high blood cholesterol', 'high cholesterol'],
                 'diabetes': ['diabetes', 'dt1', 'dt2'],
                 'depression': ['depression'],
                 'asthma': ['asthma'],
                 'arthritis': ['arthritis'],
                 'anxiety': ['anxiety']}

common_cancer_types = {'bladder', 'breast', 'colorectal', 'kidney', 'lung', 'lymphoma', 'melanoma', 'oral', 'oropharyngeal', 'pancreastic', 'prostate', 'thyroid', 'uterine'}

dates = ['since:2021-01-01 until:2021-02-01','since:2021-02-01 until:2021-03-01','since:2021-03-01 until:2021-04-01',
          'since:2021-04-01 until:2021-05-01', 'since:2021-05-01 until:2021-06-01', 'since:2021-06-01 until:2021-07-01',
          'since:2021-07-01 until:2021-08-01', 'since:2021-08-01 until:2021-09-01', 'since:2021-09-01 until:2021-10-01',
          'since:2021-10-01 until:2021-11-01', 'since:2021-11-01 until:2021-12-01', 'since:2021-12-01 until:2022-01-01'
         ]
   

data_columns = ['datetime', 'id', 'text', 'username']

data_path = 'drive/MyDrive/Bachelor Project/Data/'
#data_path = 'C:/Users/pjrad/OneDrive/Desktop/Term7/Bachelor_project/Data'
train_data_path = data_path + 'Train/'
test_data_path = data_path + 'Test/'
stopwords_set = set(stopwords.words('english'))

punctuation_set = set(string.punctuation)

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

# The components of the tokenizer:
regex_strings = (
    # Phone numbers:
    r"""
    (?:
      (?:            # (international)
        \+?[01]
        [\-\s.]*
      )?            
      (?:            # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?    
      \d{3}          # exchange
      [\-\s.]*   
      \d{4}          # base
    )"""
    ,
    # Emoticons:
    emoticon_string
    ,
    # HTML tags:
    r"""<[^>]+>"""
    ,
    # Twitter username:
    r"""(?:@[\w_]+)"""
    ,
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots. 
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
)

# This is the core tokenizing regex:
word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)

# The emoticon string gets its own regex so that we can preserve case for them as needed:
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)
#
# with open(data_path+ 'test.txt', 'w') as file:
#     file.write('Hi!')
if __name__ =='__main__':
  print(punctuation_set)
  punctuation = punctuation_set
  print(punctuation)