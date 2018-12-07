# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:51:09 2018

@author: Administrator
"""
import tweepy

def twitter_connect(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = tweepy.API(auth,
                          wait_on_rate_limit=True,
                          wait_on_rate_limit_notify=True)
    return auth_api

def get_tweeters(hashtag, auth_api):
    tweeters = set()
    for idx, page in enumerate(tweepy.Cursor(auth_api.search, q = (hashtag)).pages()):
        for i, tweet in enumerate(page):
            screenname = tweet.author.screen_name
            desc = tweet.author.description
            website = tweet.author.url
            followers = tweet.author.followers_count
            row = (screenname, followers, desc, website)
            tweeters.add(row)
    return tweeters

def save_tweeters(tweeters, hashtag):
    filename = hashtag[1:]+"tweeters.txt"
    headers = ["twitter_handle", "description", "url"]
    with open(filename, "w", encoding = "utf-8") as file:
        file.write("\t".join(headers)+"\n")
        for user in tweeters:
            file.write("\t".join([str(i) for i in user])+"\n")

def get_follower_ids(target, auth_api):
    followers = []
    for page in tweepy.Cursor(auth_api.followers_ids, user_id = target, parser = tweepy.parsers.JSONParser()).pages():
        followers.extend(page['ids'])
    return followers

def get_friend_ids(target, auth_api):
    friends = []
    for page in tweepy.Cursor(auth_api.friends_ids, user_id = target, parser = tweepy.parsers.JSONParser()).pages():
        friends.extend(page['ids'])
    return friends

def get_user_object(target, auth_api):
    user = auth_api.get_user(target)
    twitterid = user.id
    followers = user.followers_count
    friends = user.friends_count
    handle = user.screen_name
    desc = user.description
    website = user.url
    return [twitterid, handle, followers, friends, desc, website]

def get_users(user_ids, auth_api):
    users = auth_api.lookup_users(user_ids = user_ids)
    user_list = []
    for user in users:
        twitterid = user.id
        followers = user.followers_count
        friends = user.friends_count
        handle = user.screen_name
        desc = user.description
        website = user.url
        user_list.append([twitterid, handle, followers, friends, desc, website])
    return user_list

def get_user_timeline(target, auth_api):
    return auth_api.user_timeline(id = target, count = 50, tweet_mode = 'extended')