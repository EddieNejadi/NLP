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
### Part 1 ###########################################################
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


### Part 2 ###########################################################
def print_common_tag_ngrams(genre, n, rows, simplify_tags=True):
	print "== Part 2: N-gram statistics"
	print ""
	print "\t"+str(n)+"-gram\t\t\t\tFrequency\tAccum.freq."
	print "--------------------------------------------------------------------------------"
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

### Part 3 ###########################################################
def most_common_tag(tagged_sents):
	frqdis = nltk.FreqDist([tag for sen in tagged_sents for (_w,tag) in sen])
	return frqdis.max()

def train_nltk_taggers(train_sents):
	# print "trained_nltk_taggers"
	default_tagger = nltk.DefaultTagger(most_common_tag(train_sents))
	default_tagger.tag(train_sents)
	affix_tagger = nltk.AffixTagger(train_sents, backoff = default_tagger)
	unigram_tagger = nltk.UnigramTagger(train_sents, backoff = affix_tagger)
	bigram_tagger = nltk.BigramTagger(train_sents, backoff = unigram_tagger)
	trigram_tagger = nltk.TrigramTagger(train_sents, backoff = bigram_tagger)
	return (default_tagger, affix_tagger, unigram_tagger, bigram_tagger, trigram_tagger)

def print_report_header(title, comment=""):
    """I'm in desperate need of a docstring!"""
    print ("%-20s Accuracy     Errors            %s" % (title, comment))
    # print 80 * "-"

def print_report_line(title, accuracy, comment=""):
    """Me too!"""
    errors = 1.0 / (1.0 - accuracy)
    print ("%-20s%7.2f%%    %4.1f words/error    %s" % (title, 100.0 * accuracy, errors, comment))

def print_nltk_taggers_table(genre):
	print "== Part 3: NLTK's built-in taggers"
	print ""
	train, test = split_sents(brown_tagged_sents(genre))
	# print len(train)
	taggers = train_nltk_taggers(train)
	print_report_header(genre)
	print "--------------------------------------------------------------------------------"
	print_report_line("default", taggers[0].evaluate(test))
	print_report_line("affix", taggers[1].evaluate(test))
	print_report_line("unigram", taggers[2].evaluate(test))
	print_report_line("bi-gram", taggers[3].evaluate(test))
	print_report_line("tri-gram", taggers[4].evaluate(test))

### Part 4 ###########################################################
'''
Define a function train_bigram_tagger(train_sents) that calls train_nltk_taggers 
and returns only the bi-gram tagger.
'''
def train_bigram_tagger(train_sents):
	return train_nltk_taggers(train_sents)[3]

def test_on_training_set(genre):
	print "\tTraining sentences\t\tAccuracy\tErrors\tTesting sentences"
	print "--------------------------------------------------------------------------------" 
	train, test = split_sents(brown_tagged_sents(genre))
	bigram_tagger = train_bigram_tagger(train)
	accuracy = bigram_tagger.evaluate(test)
	# print len(test)
	errors = 1.0 / (1.0 - accuracy)
	# errors = 1.0 / (1.0 - accuracy)
	print ("\tnews-train\t\t\t\t%4.2f%%\t\t%4.1f\tnews-test" % (100.0 * accuracy, errors))
	accuracy = bigram_tagger.evaluate(train)
	errors = 1.0 / (1.0 - accuracy)
	# errors = 1.0 / (1.0 - accuracy)
	print ("\tnews-train\t\t\t\t%4.2f%%\t\t%4.1f\tnews-train" % (100.0 * accuracy, errors))
	print ""

def test_different_genres(genre, genres):
	print "\tTraining sentences\t\tAccuracy\tErrors\tTesting sentences"
	print "--------------------------------------------------------------------------------" 
	train, _test = split_sents(brown_tagged_sents(genre))
	# print len(train)
	bigram_tagger = train_bigram_tagger(train)
	for g in genres:
		_train , test = split_sents(brown_tagged_sents(g))
		# print len(test)
		accuracy = bigram_tagger.evaluate(test)
		errors =1.0 / (1.0 - accuracy)
		print ("\tnews-train\t\t\t\t%4.2f%%\t\t%4.1f\t%s-test" % (100.0 * accuracy, errors,g))

	print ""

def train_different_sizes(genre, portions):
	print "\tTraining sentences\t\t\tAccuracy\tErrors\tTesting sentences"
	print "--------------------------------------------------------------------------------" 
	train, test = split_sents(brown_tagged_sents(genre))
	for p in portions:
		train_part = train[:int(len(train)*(p/100))]
		bigram_tagger = train_bigram_tagger(train_part)
		accuracy = bigram_tagger.evaluate(test)
		errors =1.0 / (1.0 - accuracy)
		print ("\tnews-train %s\t\t\t%4.2f%%\t\t%4.1f\tnews-test" % ("({}%)".format(p),100.0 * accuracy, errors))
	print ""

def compare_train_test_partitions(genre):
	print "\tTraining sentences\t\t\tAccuracy\tErrors\t\tPartition"
	print "--------------------------------------------------------------------------------" 
	# train, test = split_sents(brown_tagged_sents(genre))
	bts = brown_tagged_sents(genre)
	bigram_tagger_first = train_bigram_tagger(bts[500:])
	accuracy = bigram_tagger_first.evaluate(bts[:500])
	errors =1.0 / (1.0 - accuracy)
	print ("\tnews\t\t\t\t\t%4.2f%%\t\t%4.1f\ttest = news[:500], train = news[500:]" % (100.0 * accuracy, errors))
	bigram_tagger_second = train_bigram_tagger(bts[:-500])
	accuracy = bigram_tagger_second.evaluate(bts[-500:])
	errors =1.0 / (1.0 - accuracy)
	print ("\tnews\t\t\t\t\t%4.2f%%\t\t%4.1f\ttest = news[-500:], train = news[:-500]" % (100.0 * accuracy, errors))


def print_compare_different_training_test_set():
	print "== Part 3: Compare Different Training/Test Sets"
	print ""



### Helper function #################################################
def split_sents(sents):
	return (sents[500:],sents[:500])

def brown_tagged_sents(genre, simplify_tags=True):
    """Returns the tagged sentences of the given Brown category."""
    return nltk.corpus.brown.tagged_sents(categories=genre, simplify_tags=simplify_tags)



'''
Global
'''
if __name__ == "__main__":
	print "test main function " + __file__
	# print_brown_statistics(["fiction", "government", "news", "reviews"]) # part1
	# print_common_tag_ngrams("news", 2, 10) # part2

	# news_train, news_test = split_sents(brown_tagged_sents("news"))
	# train_nltk_taggers(news_train)
	# print most_common_tag(news_train)
	# print_nltk_taggers_table("news")
	# test_on_training_set("news")
	# test_different_genres("news", ["fiction", "government", "news", "reviews"])
	# train_different_sizes("news", [100, 75, 50, 25])
	compare_train_test_partitions("news")
	# print_brown_statistics(["fiction"])
	# print type(brown_tagged_sents("fiction", True))