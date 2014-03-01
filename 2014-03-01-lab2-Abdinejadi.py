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
		tagged =  brown_tagged_sents(gen)
		pos_tags = len(set([tag for sen in tagged for (_w,tag) in sen]))
		sentence = len(tagged)
		words = len([w for sen in tagged for (w,_tag) in sen])
		avg_sent = words /sentence
		avg_word = sum([len(w) for sen in tagged for (w,_tag) in sen]) / words
		print gen + (" " * (16-len(gen))) +str(pos_tags)+ "\t\t" + str(sentence) + "\t" + str(words) + "\t"+ "{0:.2f}".format(round(avg_sent,2)) +"\t"+"{0:.2f}".format(round(avg_word,2))
	print ""


def print_common_tag_ngrams(genre, n, rows, simplify_tags=True):
	print "== Part 2: N-gram statistics"
	print ""
	print "\t"+str(n)+"-gram\t\t\t\tFrequency\tAccum.freq."
	frqdis = nltk.FreqDist()
	tagged_sents = brown_tagged_sents(genre) 
	for tag_sent in tagged_sents:
		tags = [tag for (_w,tag) in tag_sent]
		ngrams = nltk.ngrams(tags, n, True, True, "$")
		frqdis.update(ngrams)
	samples = frqdis.keys()[:rows]
	acc_frq = 0.0
	for s in samples:
		acc_frq += frqdis.freq(s)
		if n == 1:
			print "\t" + s[0] + (" " * (20-(len(s[0])))) + "{0:.2f}%".format(round(frqdis.freq(s)*100,2)) +"\t\t"+"{0:.2f}%".format(round(acc_frq*100,2))
		elif n == 2:
			print "\t" + s[0] + " " + s[1] + (" " * (19-((len(s[0])+len(s[1]))))) + "{0:.2f}%".format(round(frqdis.freq(s)*100,2)) +"\t\t"+"{0:.2f}%".format(round(acc_frq*100,2))
		elif n == 3: 
			print "\t" + s[0] + " " + s[1] + " " + s[2] + (" " * (18-((len(s[0])+len(s[1])+len(s[2]))))) + "{0:.2f}%".format(round(frqdis.freq(s)*100,2)) +"\t\t"+"{0:.2f}%".format(round(acc_frq*100,2))
		else:
			print "Invalid ngrams! Please select n = 1,2,3"
	


def brown_tagged_sents(genre, simplify_tags=True):
    """Returns the tagged sentences of the given Brown category."""
    return nltk.corpus.brown.tagged_sents(categories=genre, simplify_tags=simplify_tags)

'''
Global
'''
if __name__ == "__main__":
	print "test main function " + __file__
	# print_brown_statistics(["fiction", "government", "news", "reviews"])
	print_common_tag_ngrams("news", 2, 10)
	# print_brown_statistics(["fiction"])
	# print type(brown_tagged_sents("fiction", True))