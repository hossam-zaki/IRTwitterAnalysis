# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time


os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAJ4ZiAEAAAAAOD9SxuvtqQ5%2FISoulV8l3uc9rSc%3DKTs0Tg2DJe0X5WMvO82I3Sy81gdnp7yJrkkbVAkFxxUqNfXlGL'

def auth():
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, max_results = 10):
    
    search_url = "https://api.twitter.com/2/tweets/search/recent" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'max_results': max_results,
                    'expansions': 'author_id,attachments.media_keys',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,conversation_id,created_at,lang,public_metrics,referenced_tweets',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that
        print(tweet)

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        #7. Media included
        media_incl = False

        if 'attachments' in tweet:
            media_incl = True
        

        # 8. Tweet text
        text = tweet['text']
        
        # Assemble all data in a list
        res = [tweet_id, author_id, created_at,like_count, quote_count, reply_count, retweet_count, media_incl, text]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter) 

#Inputs for the request
bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "ablation lang:en -is:retweet" #For embolization: Embolization,
max_results = 15



# Create file
csvFile = open("ablation.csv", "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)
total_tweets = 0

csvWriter.writerow(["tweet_id", "author_id", "created_at","like_count", "quote_count", "reply_count", "retweet_count", "media_incl", "text"])
csvFile.close()


# Inputs
count = 0 # Counting tweets per time period
max_count = 100 # Max tweets per time period
flag = True
next_token = None

# Check if flag is true
while flag:
    # Check if max_count reached
    if count >= max_count:
        break
    print("-------------------")
    print("Token: ", next_token)
    url = create_url(keyword, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
    result_count = json_response['meta']['result_count']

    if 'next_token' in json_response['meta']:
        # Save the token to use for next call
        next_token = json_response['meta']['next_token']
        print("Next Token: ", next_token)
        if result_count is not None and result_count > 0 and next_token is not None:
            append_to_csv(json_response, "ablation.csv")
            count += result_count
            total_tweets += result_count
            print("Total # of Tweets added: ", total_tweets)
            print("-------------------")
            time.sleep(5)                
    # If no next token exists
    else:
        if result_count is not None and result_count > 0:
            print("-------------------")
            append_to_csv(json_response, "ablation.csv")
            count += result_count
            total_tweets += result_count
            print("Total # of Tweets added: ", total_tweets)
            print("-------------------")
            time.sleep(5)
        
        #Since this is the final request, turn flag to false to move to the next time period.
        flag = False
        next_token = None
    time.sleep(5)
print("Total number of results: ", total_tweets)




