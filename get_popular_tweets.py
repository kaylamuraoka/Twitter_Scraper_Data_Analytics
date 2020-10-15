# import necessary libraries
import requests as rq
from requests_oauthlib import OAuth1
import pandas as pd
import time

# prompt the user for a word
query = input('What word/hashtag should we search for? (Enter a single word): ').strip()

# check that the user input is a valid string
try:
    str(query)
    pass

except ValueError:
    print("Sorry, that is not a valid word, perhaps you mistyped?")
    query = input('Try again, what word/hashtag should we search for? (Enter a single word): ').strip()

# The function by default has the result_type = 'popular'
def get_most_popular_twitter_tweets(query, result_type = 'popular'):

    print("Searching for tweets within the last week that mention " + query + '\n')
    # Define API Key, Search Type, and authorization
    twitter_search_path = 'https://api.twitter.com/1.1/search/tweets.json'

    auth = OAuth1 ('U57SZ7qXdxFgFIrfdn6E2yk1U',
                   'fVSW996YZyTlJdA4xvRSVWne9hSRdPBTrnQRnKGhr2pGZchlzB',
                   '765282870172803072-u90XOV6lFK6sN6MiDUqbml8yVAmSjiF',
                   'ONCkmYBLH71EHJpiOoE7uFxMzbE47B6bcIq0Y8roRKlcw'
     )

    # Define the Parameters of the search
    search_params = {
        'q': [query, '#' + query],
        'lang':'en',
        'result_type': result_type, # Specifies what type of search results you would prefer to receive.
        'count': 15,  # The number of tweets to return per page, up to a maximum of 15.
        
    }

    # Make a Request to the API, and return results
    # Convert response to a JSON String
    response = rq.get(twitter_search_path, params=search_params, auth=auth).json()
    
    # Calling DataFrame constructor 
    df = pd.DataFrame([])
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'retweet_count': [], 'hashtags': []}

    count = 0
    
    for tweet in response['statuses']:
        count += 1
        if count <= 15 and 'RT @' not in tweet['text']:
 
            dict_['user'].append(tweet['user']['screen_name'])
            dict_['date'].append(tweet['created_at'])
            dict_['text'].append(tweet['text'].replace('\n', ' '))
            dict_['favorite_count'].append(tweet['favorite_count'])
            dict_['retweet_count'].append(tweet['retweet_count'])
            hashtags = tweet['entities']['hashtags']
            for hashtag in hashtags:
                hashtags = hashtag['text']
            dict_['hashtags'].append(hashtags)  
            
            print(str(count) + ':', tweet['text'].replace('\n', ' '), '\n')
                
    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    
    # export df to a csv file in the same directory
    df.to_csv ('trending_' + query + '_at_' + time.strftime('%Y-%m-%d-%H-%M') + '.csv', index = False, header=True)

    print("Tweets written on: trending_" + query + '_at_' + time.strftime('%Y-%m-%d-%H-%M') + '.csv')

most_popular_Tweets=get_most_popular_twitter_tweets(query, result_type = 'popular')