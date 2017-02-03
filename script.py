import csv
import json
import tweepy
import time

# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    with open (key_file) as file1:
        AuthKeys = json.load(file1)
    return(AuthKeys["api_key"], AuthKeys["api_secret"], AuthKeys["token"], AuthKeys["token_secret"])

def getFollowers(api, root_user, no_of_followers):
    primary_followers = []
    counter = True

    while counter == True:
        try:
            newUser = api.get_user(root_user)
            followers = newUser.followers()
            for index in range(no_of_followers):
                primary_followers.append((str(followers[index].screen_name), root_user))
            counter == False
            #print(primary_followers)
            return primary_followers
        except (tweepy.error.RateLimitError):
            print("Sleeping on getFollowers. Please wait")
            time.sleep(15*60)

def getSecondaryFollowers(api, followers_list, no_of_followers):
    # implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
    secondary_followers = []
    counter = True

    while counter == True:
        try:
            for user in followers_list:
                try:
                    newUser = api.get_user(user[0])
                    followers = newUser.followers()
                    count = 0

                    for username in followers:
                        if count < no_of_followers:
                            secondary_followers.append((username.screen_name, user[0]))
                            count += 1
                except (tweepy.TweepError):
                    print ("Not authorized to view user. Skipping to next user")
                    pass
            counter == False

            #print(secondary_followers)
            return secondary_followers
        except (tweepy.error.RateLimitError):
            print ("Sleeping on getSecondaryFollowers. Please wait")
            time.sleep(15*60)

def getFriends(api, root_user, no_of_friends):
    # implement the method for fetching 'no_of_friends' friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    counter = True
    newUser = api.get_user(screen_name = root_user)

    while counter == True:
        try:
            count = 0
            for friend in newUser.friends():
                if count < no_of_friends:
                    primary_friends.append((root_user, friend.screen_name))
                    count += 1
            counter == False
            #print(primary_friends)
            return primary_friends

        except (tweepy.error.RateLimitError):
            print("Sleeping on getFriends. Please wait")
            time.sleep(15*60)

def getSecondaryFriends(api, friends_list, no_of_friends):
    # implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    secondary_friends = []
    counter = True

    while counter == True:
        try:
            for friend in friends_list:
                try:
                    newUser = api.get_user(screen_name = friend[1])
                    count = 0
                    for friend_of_user in newUser.friends():
                        if count < no_of_friends:
                            secondary_friends.append((friend[1], friend_of_user.screen_name))
                            count += 1
                except (tweepy.TweepError):
                    print ("Not authorized to view user. Skipping to next user")
                    pass
            counter == False
            #print(secondary_friends)
            return secondary_friends
        except (tweepy.error.RateLimitError):
            print ("Sleeping on getSecondaryFriends. Please wait")
            time.sleep(15*60)

def writeToFile(data, output_file):
    outFile = open(output_file, "w")
    csvWriter = csv.writer(outFile, lineterminator = "\n")
    csvWriter.writerow(['Source','Target'])
    for element in data:
        csvWriter.writerow(element)
    print("Successfully Exported to CSV")


def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_FOLLOWERS = 'followers.csv'
    OUTPUT_FILE_FRIENDS = 'friends.csv'

    ROOT_USER = 'PoloChau'
    NO_OF_FOLLOWERS = 10
    NO_OF_FRIENDS = 10


    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
    secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)
    followers = primary_followers + secondary_followers

    primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)
    secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)
    friends = primary_friends + secondary_friends

    writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
    writeToFile(friends, OUTPUT_FILE_FRIENDS)


if __name__ == '__main__':
    testSubmission()

