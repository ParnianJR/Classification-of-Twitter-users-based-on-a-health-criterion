from Constants import diseases_dict, data_path, data_columns, dates

import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
import time


def scrape_diseases():
    path = os.path.join(data_path + 'raw_data/')
    # a dictionary includes queries for each disease
    for date in dates:
        queries_dict = dict()
        # constructing queries
        for disease in diseases_dict:
            queries_dict.update({disease: []})
            for key_word in diseases_dict[disease]:
                queries_dict[disease].append('I diagnosed' + ' ' + key_word + ' ' + date)
        
        print('{}'.format(date))
        start = time.time()
        
        for disease in diseases_dict:
            # if disease == 'hypertension':
            print('------------------- {} --------------'.format(disease))
            tweets_list = list()            
            for query in queries_dict[disease]:
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                    # if i > 20:
                    #     break
                    if i != 0 and i % 1000 == 0:
                        print(i)
                    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    
            tweets_df = pd.DataFrame(tweets_list, columns=data_columns)
            tweets_df.to_csv(data_path + disease +'_'+ date + '.csv', index=False)
            print('saved data successfully')
            
        end = time.time()
        print("Execution time: {}".format(end-start))



if __name__ == "__main__":
    scrape_diseases()
