# Setup necessary packages
from __future__ import print_function
import sys
import tweepy
from configparser import ConfigParser
import time
import csv

# prompt the user for a word
query = input('What word/hashtag should we search for? (Enter a single word): ').strip()
max_num = int(input('How many tweets do you want to collect: '))

# check that the user input is a valid string
try:
    str(query)
    pass

except ValueError:
    print("Sorry, that is not a valid word, perhaps you mistyped?")
    query = input('Try again, what word/hashtag should we search for? (Enter a single word): ').strip()

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.itera = 0
        self.max = max_num
        # Create a file with user's input and  and the current time to save the tweets to
        self.filename = query + 'tweets' + '_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.csv'
        # Create a new file with that filename
        csvFile = open(self.filename, 'w')
        # Create a csv writer
        writer = csv.writer(csvFile)
        # Write a single row with the headers of the columns
        writer.writerow(['text',
                        'hashtags',
                        'date',
                        'user',
                        'users number of followers',
                        'location'])

    # when tweet appears
    def on_status(self, status):
         
        # Open the csv file created previously
        csvFile = open(self.filename, 'a')

        # Create a csv writer
        writer = csv.writer(csvFile)
        
        if status.truncated:
            text = status.extended_tweet['full_text'].replace('\n', ' ') + '\n'
        else:
            text = status.text.replace('\n', ' ') + '\n'
        
        hashtags = []   #　make an empty list
        for hashtag in status.entities['hashtags']:    #　iterate over the list
            hashtags.append(hashtag["text"])        #　append each hashtag to 'hashtags'

        # If the tweet is not a retweet
        if not 'RT @' in status.text:
            try:
                self.itera += 1
                if self.itera <= int(max_num):
                    # Write the tweet's information to the csv file
                    writer.writerow([text,
                                hashtags,
                                status.created_at,
                                status.user.screen_name,
                                status.user.followers_count,
                                status.user.location])
                    
                    # print something after every 100th iterable element
                    if self.itera % 100 == 0:
                        print("We collected " + str(self.itera) + " tweets\n")    
                    
                else:
                    myStream.disconnect
                    csvFile.close()
                    sys.exit()

            except Exception as e:
                print(e)
                pass
    
    # When an error occurs
    def on_error(self, status_code):
        # Print the error code
        print('Encountered error with status code:', status_code)
        
        # If the error code is 401, which is the error for bad credentials
        if status_code == 401:
            # End the stream
            return False
        

if __name__ == "__main__":
    print("Writing tweets to: " + query + 'tweets' + '_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.csv\n')
    print("Press CTRL + c to terminate...\n")
    time.sleep(2)

    config = ConfigParser()
    # read configuration file containing consumer key + secret, and accesss token + secret
    config.read('config.cfg')


    auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'),
                               config.get('twitter', 'consumer_secret'))

    auth.set_access_token(config.get('twitter', 'access_token'),
                          config.get('twitter', 'access_token_secret'))

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    try:
        myStream.filter(languages=["en"], track=[query, '#' + query])
    except KeyboardInterrupt:
        print('*****************************\nInterrupted')
        sys.exit()