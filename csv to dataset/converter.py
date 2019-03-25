import pandas as pd
import csv
import numpy as np
import scipy.stats
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder


def csv_to_txt():
    d = pd.read_csv('emails.csv')
    df = pd.DataFrame(d)

    for row in df['message']:
        # Indexes of From, To, Subject, CC to parse strings
        _from = row.find('From:')
        _to = row.find('To:')
        _subject = row.find('Subject:')
        _cc = row.find('cc:')

        if (_to < _subject):
            print(row[_from:_to].rstrip(), file=open("newcsv.txt", "a"))             # FROM

            if (_cc < _subject):                                                     # There is CC
                print(row[_to:_cc].rstrip(), file=open("newcsv.txt", "a"))
            else:                                                                    # There is not CC
                print(row[_to:_subject].rstrip(), file=open("newcsv.txt", "a"))

    file = open('newcsv.txt', 'r')


def txt_to_graph():
    with open('newcsv.txt') as file:
        print('{}\t{}\n'.format('from'.rstrip(), 'to'.rstrip()), file=open("enron.txt", "a"))
        for row in file:
            _from = row.find('From')
            _to = row.find('To')
            
            if _from >= 0:
                from_email = row[_from+6:len(row)]      # Parse From string

            if _to >= 0:
                to_string = row[_to+4:len(row)]
                splitted = to_string.split(',')

                for s in splitted:                      # Parse To string list
                    if len(s.rstrip()) > 0:
                        print('{}\t{}\n'.format(from_email.rstrip(), s.rstrip()), file=open("enron.txt", "a"))


def graph_normalizer():
    d = pd.read_csv('enron.txt')
    df = pd.DataFrame(d)

    encoders = [(["from"], LabelEncoder()), (["to"], LabelEncoder())]
    mapper = DataFrameMapper(encoders, df_out=True)
    new_cols = mapper.fit_transform(df.copy())
    df = pd.concat([df.drop(columns=["from", "to"]), new_cols], axis="columns")

    print(df)

#csv_to_txt()
#txt_to_graph()
graph_normalizer()