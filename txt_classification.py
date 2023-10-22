import os
#import random as rd
from nltk import word_tokenize
from collections import defaultdict
from nltk import FreqDist
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pickle

import nltk
nltk.download('stopwords')
nltk.download('punkt')

#import csv
import string

#OCR PDF and IMG
from OCR_for_pdf_and_pic import *

import os
import sys

stop_words = set(stopwords.words('english'))
stop_words.add('said')
stop_words.add('mr.')

BASE_DIR = r'C:\Users\msi\OneDrive - acsp.ac.th\Desktop\Text Classification\data'
LABELS = ['accounts', 'biology', 'com-tech', 'geography', 'history', 'maths', 'physics']

def creat_data_set():
    with open('data.txt', 'w', encoding='utf8', newline='') as outfile:
        for label in LABELS:
            dir = r'%s\%s' %(BASE_DIR, label)
            for filename in os.listdir(dir):
                fullfilename = r'%s\%s' %(dir, filename)
                #print(fullfilename)
                with open(fullfilename, 'r', encoding="utf8") as file:
                    line = file.readlines()
                    text = ''.join([i.replace('\n', '') for i in line])

                    outfile.write('%s\t%s\t%s\n' %(label, filename, text))

def setup_docs():
    docs = []
    with open('data.txt', 'r', encoding='utf8') as datafile:
        for row in datafile:
            parts = row.split('\t')
            #print(row)
            try:
                doc = ( parts[0], parts[2].strip() )
                docs.append(doc)
            except IndexError:
                print("Error:   ", parts, row)

    return docs

def clean_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    return text

def get_tokens(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if not t in stop_words]
    return tokens

def get_tokens(text):
    tokens = word_tokenize(text)
    
    tokens = [t for t in tokens if not t in stop_words]

    return tokens

def print_frequency_dist(docs):
    tokens = defaultdict(list)
    
    for doc in docs:
        doc_label = doc[0]
        
        doc_text = clean_text(doc[1])
        
        #doc_tokens = word_tokenize(doc_text)
        doc_tokens = get_tokens(doc_text)
        
        tokens[doc_label].extend(doc_tokens)
        
        #doc_text = clean_text(doc[1])
        
        #doc_tokens = get_tokens(doc_text)
        
        #tokens[doc.label].extend(doc_tokens)


    for category_label, category_tokens in tokens.items():
        print(category_label)
        fd = FreqDist(category_tokens)
        print(fd.most_common(20))

#Split Data to train and test
def get_split(docs):
    #rd.shuffle(docs)
    
    X_train = []
    y_train = []
    
    X_test = []
    y_test = []
    
    pivot = int(.80 * len(docs)) #splt train 80% | test 20%
    
    for i in range(0, pivot):
        X_train.append(docs[i][1]) #train data
        y_train.append(docs[i][0]) #train label
    for i in range (pivot, len(docs)):
        X_test.append(docs[i][1]) #test data
        y_test.append(docs[i][0]) #test label
        
    return X_train, X_test, y_train, y_test

def evaluate_classifier(title, classifier, vectorizer, X_test, y_test):
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = classifier.predict(X_test_tfidf)
    
    precision = metrics.precision_score(y_test, y_pred,
                                        labels='positive',
                                        average='micro')
    recall = metrics.recall_score(y_test, y_pred, 
                                  labels='positive', 
                                  average='micro')
    
    f1 = metrics.f1_score(y_test, y_pred, 
                          labels='positive', 
                          average='micro')
    
    print("%s\t%f\t%f\t%f\n" % (title, precision, recall, f1))

#Training
def train_classifier(docs):
    X_train, X_test, y_train, y_test = get_split(docs)
    
    #text to Vector
    vectorizer = CountVectorizer(stop_words='english',
                                 ngram_range=(1, 3),
                                 min_df=3, analyzer='word')
    
    #print("AAAAAAAAAA: ", len(X_train), len(X_test))
    #print(X_train[0])
    #print("\n\n\n")
    #print(X_test[0])
    
    #Create doc-term matrix
    dtm = vectorizer.fit_transform(X_train)
    
    naive_bayes_classifier = MultinomialNB().fit(dtm, y_train)
    
    evaluate_classifier("Naive Bayes\tTRAIN\t", naive_bayes_classifier, vectorizer, X_train, y_train)
    evaluate_classifier("Naive Bayes\tTEST\t", naive_bayes_classifier, vectorizer, X_test, y_test)

    #store claasifier
    clf_filename = 'naive_bayes_classifier.pkl'
    pickle.dump(naive_bayes_classifier, open(clf_filename, 'wb'))
    
    #also store vectorizer (so we can transform new data)
    vec_filename = 'count_vectorizer.pkl'
    pickle.dump(vectorizer, open(vec_filename, 'wb'))
    

def classify(text):
    #load classifier
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    clf_filename = fr'{script_directory}\naive_bayes_classifier.pkl'
    nb_clf = pickle.load(open(clf_filename, 'rb'))
    
    #vectorize the new text
    vec_filename = fr'{script_directory}\count_vectorizer.pkl'
    vectorizer = pickle.load(open(vec_filename, 'rb'))
    
    pred = nb_clf.predict(vectorizer.transform([text]))
    
    return pred[0]

if __name__ == '__main__':
    #creat_data_set()
    #docs = setup_docs()
    #print(docs)
    #print(len(docs))
    #print_frequency_dist(docs)
    
    #train_classifier(docs)

    #new_doc = get_text_from_img(img)
    #classify(new_doc)
    
    #new_doc = get_text_from_pdf_tika(path_to_pdf)
    #classify(new_doc)
    
    #new_doc = get_text_from_pdf_PyPDF2(path_to_pdf)
    #classify(new_doc)

    print('done')