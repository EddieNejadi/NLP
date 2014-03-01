'''
Created on Nov 6, 2013

@author: Mahdi Abdinejadi
'''


'''
import libraries
'''
import nltk
import re


'''
Constants definitions
'''


'''
Function definitions
'''
def main():
#     print get_corpus_text()
    print "***************************************"
#     for c in get_gold_tokens():
#         print c
#     print "***************************************"

def get_corpus_text(nr_files=199):
    """Returns the raw corpus as a long string.
    'nr_files' says how much of the corpus is returned;
    default is 199, which is the whole corpus.
    """
    fileids = nltk.corpus.treebank_raw.fileids()[:nr_files]
    corpus_text = nltk.corpus.treebank_raw.raw(fileids)
    # Get rid of the ".START" text in the beginning of each file:
    corpus_text = corpus_text.replace(".START", "")
    return corpus_text

def fix_treebank_tokens(tokens):
    """Replace tokens so that they are similar to the raw corpus text."""
    return [token.replace("''", '"').replace("``", '"').replace(r"\/", "/")
            for token in tokens]

def get_gold_tokens(nr_files=199):
    """Returns the gold corpus as a list of strings.
    'nr_files' says how much of the corpus is returned;
    default is 199, which is the whole corpus.
    """
    fileids = nltk.corpus.treebank_chunk.fileids()[:nr_files]
    gold_tokens = nltk.corpus.treebank_chunk.words(fileids)
    return fix_treebank_tokens(gold_tokens)

def tokenize_corpus(text):
#     return text.split(' ')
#     return re.split('(\W+)', text)
#     return nltk.regexp_tokenize(text, '(\W+)')
#     from nltk.tokenize import RegexpTokenizer
#     tokenizer = RegexpTokenizer('\'s+|\Mr\.+|\Mrs\.+|\U\.S\.+|\Inc\.+|\$[\d\.]+|\.+|\,+|\'+|\"+|\:+|\;\S+|\w+')
#     tokenizer = RegexpTokenizer('\'s+|([A-Z]\w{0,4}\.)+|\.+|\,+|\'+|\"+|\:+|\.+|\;+|\S+|\w')
#     l = tokenizer.tokenize(text)
#     return l
#     pattern = r'''(?x)        # set flag to allow verbose regexps
#     ...     ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
#     ...   | \w+(-\w+)*        # words with optional internal hyphens
#     ...   | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
#     ...   | \.\.\.            # ellipsis
#     ...   | [][.,;"'?():-_`]  # these are separate tokens
#     ... '''
 
    pattern = r'''(?x)                            # set flag to allow verbose regexps
        ([A-Z]\.)+(?!=\s\[A-Z])                   # abbreviations, e.g. U.S.A.
        | U\.S\.                                    
        | [A-Z]([A-Za-z]{1,4}\.)+(?!=\s\[A-Z])
        | ((\d)*\,(\d)+)+
        | (\d)*\.(\d)+
        | (\d)*\/(\d)*
        | \d(\d)*\:\d(\d)*\s[pa]\.m
        | \.(\.)*
        | \,
        | \'s
        | \'ll
        | \'m
        | \'t
        | \'d
        | \'re
        | \'ve
        | \'(?!=[0-9t])
        | ([A-Z])*\&([A-Z])+
        | \&
        | \w+(?=n\'t)
        | n\'t
        | \w+(\/\w+(-\w+)*)+
        | \w+(-\w+)*
        | \"
        | \`
        | \(
        | \)
        | \#
        | \$
        | \:
        | \?
        | \!
        | \;
        | \%
        | \}
        | \{
        | --
    '''
    return nltk.regexp_tokenize(text, pattern)

def evaluate_tokenization(test_tokens, gold_tokens):
    """Finds the chunks where test_tokens differs from gold_tokens.
    Prints the errors and calculates similarity measures.
    """
    import difflib
    matcher = difflib.SequenceMatcher()
    matcher.set_seqs(test_tokens, gold_tokens)
    error_chunks = true_positives = false_positives = false_negatives = 0
    print " Token%30s  |  %-30sToken" % ("Error", "Correct")
    print "-" * 38 + "+" + "-" * 38
    for difftype, test_from, test_to, gold_from, gold_to in matcher.get_opcodes():
        if difftype == "equal":
            true_positives += test_to - test_from
        else:
            false_positives += test_to - test_from
            false_negatives += gold_to - gold_from
            error_chunks += 1
            test_chunk = " ".join(test_tokens[test_from:test_to])
            gold_chunk = " ".join(gold_tokens[gold_from:gold_to])
            print "%6d%30s  |  %-30s%d" % (test_from, test_chunk, gold_chunk, gold_from)
    precision = 1.0 * true_positives / (true_positives + false_positives)
    recall = 1.0 * true_positives / (true_positives + false_negatives)
    fscore = 2.0 * precision * recall / (precision + recall)
    print
    print "Test size: %5d tokens" % len(test_tokens)
    print "Gold size: %5d tokens" % len(gold_tokens)
    print "Nr errors: %5d chunks" % error_chunks
    print "Precision: %5.2f %%" % (100 * precision)
    print "Recall:    %5.2f %%" % (100 * recall)
    print "F-score:   %5.2f %%" % (100 * fscore)
    print

def nr_corpous_words(corpus):
    return len(tokenize_corpus(corpus))

def avarage_corpus_words_len(corpus):
    w_lens = [len(w) for w in tokenize_corpus(corpus_text)]
    return int(round(sum(w_lens) / len(w_lens) * 1.0))

def logest_corpus_word(corpus):
    words =  [(len(w),w) for w in tokenize_corpus(corpus_text)]
    words.sort()
    return words.pop()

def happax_words_in_corpus(corpus):
    from collections import Counter
    words =  [w for w in tokenize_corpus(corpus_text)]
    words_occurrneces = dict(Counter(words))
#     TODO: sort the dictionary based on occurrences
    print words_occurrneces


'''
Global
'''
# if __name__ == "__main__":
nr_files = 199
corpus_text = get_corpus_text(nr_files)
#     gold_tokens = get_gold_tokens(nr_files)
#     tokens = tokenize_corpus(corpus_text)
#     evaluate_tokenization(tokens, gold_tokens)
print '============================================'
print '============================================'
print nr_corpous_words(corpus_text)
w_lens = [len(w) for w in tokenize_corpus(corpus_text)]
# print tokenize_corpus(corpus_text)
print '============================================'
# print len(gold_tokens)
print sum(w_lens) / len(w_lens) * 1.0
print avarage_corpus_words_len(corpus_text)

print logest_corpus_word(corpus_text)
# print happax_words_in_corpus(corpus_text)