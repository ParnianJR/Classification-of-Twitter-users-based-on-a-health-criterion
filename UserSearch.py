from Constants import diseases_dict, data_path, data_columns

import snscrape.modules.twitter as sntwitter
import pandas as pd
import json as js
import time
from datetime import datetime


def convert_str_into_datetime(date_str):
  try:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S+00:00")
  except ValueError:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

def diff_timedate(d1, d2):
    # diff = d1 - d2 if d1 > d2 else d2 - d1
    diff = d1 - d2
    return diff.days


def scrape_users_tweet(username, date, limit=60):
  search_str = 'from:' + username.replace('@', '')
  
  date = convert_str_into_datetime(str(date))

  # Creating list to append tweet data to
  tweets_list = []
  user_tweets = {'before': {'datetime': list(), 'id': list(), 'text': list()},
                  'after': {'datetime': list(), 'id': list(), 'text': list()}
                  }

  # Using TwitterSearchScraper to scrape data 
  for index, tweet in enumerate(sntwitter.TwitterSearchScraper(search_str).get_items()):

      current_date = convert_str_into_datetime(str(tweet.date))
      
      if current_date > date: # after
        time_diff = diff_timedate(current_date, date)

        if time_diff > limit:
          continue
        
        user_tweets['after']['datetime'].append(str(tweet.date))
        user_tweets['after']['id'].append(int(tweet.id))
        user_tweets['after']['text'].append(tweet.content)
          

      elif current_date < date: # before
        time_diff = diff_timedate(date, current_date)

  
        if time_diff > limit: # we spcraped all tweets for this user in the given timespace, stop continueing 
          break

        user_tweets['before']['datetime'].append(str(tweet.date))
        user_tweets['before']['id'].append(int(tweet.id))
        user_tweets['before']['text'].append(tweet.content)
        
      

  return user_tweets


def scrape_all_diseases_users_tweet(usernames_datapath):

  def sort_users_date(user_date_dict):
    converted_users_dict = dict()
    for username in user_date_dict:
      converted_users_dict.update({username: min([convert_str_into_datetime(str(date)) for date in user_date_dict[username]])})
    return dict(sorted(converted_users_dict.items(), key=lambda item: item[1], reverse= True))
  

  # load usernames for each disease
  
  with open(usernames_datapath + 'users.json', 'r') as users_file:
    users_dict = js.load(users_file)

    for disease in users_dict:
      
        print(f'----------    {disease}    ------------')
        for subsection in users_dict[disease]:
          print('{:10} {}'.format('', subsection))

          # the file path that this data will be stored in
          file_path = data_path +'Users//' + '{}_{}_users_data.json'.format(disease,subsection)
          users_data_dict = dict()
          
          # sort users based on the time that tweeted about being diagnosed with the chosen disease
          # this way in a given time, more users tweet will be scraped
          users_sorted_dict = sort_users_date(users_dict[disease][subsection])
          
          for count, username in enumerate(users_dict[disease][subsection]):
            
            date_list = [convert_str_into_datetime(date) for date in users_dict[disease][subsection][username]]
            # get first time that this user mentioned being diagnosed with the chosen disease
            date = min(date_list)
            # add this user to our dictionary
            users_data_dict.update({username: scrape_users_tweet(username, date)})

            if users_data_dict[username] is None:
              users_data_dict[username] = {'detection_date':str(date)}
            else:
              users_data_dict[username].update({'detection_date':str(date)})

            if count% 10 ==0 and count !=0:
              time.sleep(10)
              
            with open(file_path, 'w') as data_file:
              js.dump(users_data_dict, data_file)
              print("a copy has been made!")  
            print(count)
          
          with open(file_path, 'w') as data_file:
            js.dump(users_data_dict, data_file)
            print("a copy has been made!")  



              
          
if __name__ == '__main__':
    print('USerSearch is runing')
    scrape_all_diseases_users_tweet(data_path )
