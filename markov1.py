"""Generate markov text from text files."""

import os
import twitter

from random import choice


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here

    with open(file_path) as f:
        text = f.read()

    return text

def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
    """

    # chain_dict = {}
    # words_list = []

    # words = text_string.split()

    # for i in range(len(text_string)-4):

        
    #     chain_dict = {(words[i], words[i+1]): words[i+2]}
    #     print chain_dict

    # return chain_dict



    chain_dict = {}

    words = text_string.split()


    for i in range(len(words) - 2):

        current_key = (words[i], words[i + 1])
        values = [words[i + 2]]

        if current_key in chain_dict:
            chain_dict[current_key].extend(values)

        else:
            chain_dict[current_key] = values

    
    return chain_dict


def make_text(chains):
    """Returns text from chains."""

    words = []

    current_key = choice(chains.keys())
    words.extend(current_key)

    while chains.get(current_key,None):
        new_key = (current_key[1],choice(chains[current_key]))
        words.append(new_key[1])
        current_key = new_key


    return " ".join(words)


def tweet(random_text):
    """Tweet our random Markov chain to Twitter!"""

    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


# This will print info about credentials to make sure 
# they're correct
    print api.VerifyCredentials()

# Send a tweet
    status = api.PostUpdate(random_text)
    print status.text


input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print random_text

tweet(random_text)
