from __future__ import division
'''
Created on March 1, 2014

@author: Mahdi Abdinejadi
'''


'''
import libraries
'''
import nltk


'''
Constants definitions
'''


'''
Function definitions
'''
# def main():

def print_brown_statistics(genre):
	print "== Part 1: Brown genre statistics"
	print ""
	print "Brown genre\t\tTags\tSents\tWords\tSentlen\tWordlen                 "
	print "--------------------------------------------------------------------------------"
	for gen in genre:
		# print type(brown_tagged_sents(gen))
		tagged =  brown_tagged_sents(gen)
		# print tagged
		# print len(tagged)
		pos_tags = len(set([tag for sen in tagged for (_w,tag) in sen]))
		sentence = len(tagged)
		words = len([w for sen in tagged for (w,_tag) in sen])
		avg_sent = words /sentence
		avg_word = sum([len(w) for sen in tagged for (w,_tag) in sen]) / words
		# print "\t\t\t\t"+str(pos_tags)+ "\t" + str(sentence) + "\t" + str(words) + "\t"+ str(avg_sent) +"\t"+str(avg_word)
		print gen + (" " * (16-len(gen))) +str(pos_tags)+ "\t\t" + str(sentence) + "\t" + str(words) + "\t"+ "{0:.2f}".format(round(avg_sent,2)) +"\t"+"{0:.2f}".format(round(avg_word,2))
	print ""

def brown_tagged_sents(genre, simplify_tags=True):
    """Returns the tagged sentences of the given Brown category."""
    return nltk.corpus.brown.tagged_sents(categories=genre, simplify_tags=simplify_tags)

def print_common_tag_ngrams(genre, n, rows, simplify_tags=True):
	print "== Part 2: N-gram statistics"


'''
Global
'''
if __name__ == "__main__":
	print "test main function " + __file__
	print_brown_statistics(["fiction", "government", "news", "reviews"])
	# print_brown_statistics(["fiction"])
	# print type(brown_tagged_sents("fiction", True))