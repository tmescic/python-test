#!/usr/bin/python2.7
# encoding: utf-8
'''
Created on Dec 15, 2014

Write a script that takes a file containing a number of words (one per line) and sorts them
by the number of times they occur in the file (descending order), but exclude words that only
occur once. Ignore the case of the words and filter out any punctuation characters. The output
should contain lines each with word and the number of times it occurs in the input separated
by space.

Example input:

microsoft
apple
microsoft.
Apple
security
microsoft
internet

Example output:

microsoft 3
apple 2

@author: tmescic
'''

import string, operator

if __name__ == '__main__':
    # { word : number of occurrences of the word }
    words = {}
    fin = open('in.txt')

    for line in fin:
        # format word:  remove right CR -> convert to lowercase, and -> remove punctuation
        c_line = line.rstrip().lower().translate(string.maketrans("",""), string.punctuation)

        # increase word count
        words[c_line] = words[c_line]+1 if words.has_key(c_line) else 1

    fin.close()

    # sort the words by number of occurrences, descending
    s_words = sorted(words.items(), key=operator.itemgetter(1), reverse = True)

    fout = open('out.txt', 'w')

    # write result in out.txt
    for word in s_words:
        if word[1] > 1:
            fout.write("%s %s\n" % word)
        else:
            break

    fout.close()
