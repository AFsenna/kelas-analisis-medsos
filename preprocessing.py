import json
import string
import nltk
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class preprocessing:
    def __init__(self):
        # self.caseFolding()
        # self.stemming()
        # self.tokenizing()
        # self.tfidf()
        self.cekHasil()

    def openJSONfile(self, namaFile):
        file_json = open(namaFile, encoding="utf8")
        dataset = json.loads(file_json.read())
        return dataset

    def caseFolding(self):
        dataset = self.openJSONfile('S:/!FILE KULIAH/Tugas Analisis '
                                    'Medsos/UTS_AnalisisMedsos/data/datasetKekerasanFisik.json')
        l = list()
        for data in dataset['data']:
            lower = data['text'].lower()
            data['text'] = lower
            l.append(data)
        with open('hasilCaseFolding.json', 'w') as f:
            f.write('%s\n' % json.dumps(l, indent=4, sort_keys=True))

    def stemming(self):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        dataset = self.openJSONfile('S:/!FILE KULIAH/Tugas Analisis Medsos/UTS_AnalisisMedsos/hasilCaseFolding.json')
        l = list()
        for data in dataset:
            stem = stemmer.stem(data['text'])
            data['text'] = stem
            l.append(data)
        with open('hasilStemming.json', 'w') as f:
            f.write('%s\n' % json.dumps(l, indent=4, sort_keys=True))

    def tokenizing(self):
        dataset = self.openJSONfile('S:/!FILE KULIAH/Tugas Analisis Medsos/UTS_AnalisisMedsos/hasilStemming.json')
        l = list()
        for data in dataset:
            hapusAngka = re.sub(r"\d+", "", data['text'])
            hapusTandaBaca = hapusAngka.translate(str.maketrans("", "", string.punctuation))
            hapusSpasi = hapusTandaBaca.strip()
            token = nltk.tokenize.word_tokenize(hapusSpasi)
            filter = self.filtering(token)
            data['text'] = filter
            l.append(data)
        with open('hasilTokenizing.json', 'w') as f:
            f.write('%s\n' % json.dumps(l, indent=4, sort_keys=True))

    def filtering(self,tokens):
        listStopword = set(stopwords.words('indonesian'))
        filter = []
        for t in tokens:
            if t not in listStopword:
                filter.append(t)
        return filter

    def tfidf(self):
        dataset = self.openJSONfile('S:/!FILE KULIAH/Tugas Analisis Medsos/UTS_AnalisisMedsos/hasilTokenizing.json')
        dataText = []
        for data in dataset:
            dataText.append(data['text'])
        tfidf = TfidfVectorizer(tokenizer=lambda i: i, lowercase=False)
        hasilTFIDF = tfidf.fit_transform(dataText)
        return hasilTFIDF

    def cekHasil(self):
        dataset = self.openJSONfile('S:/!FILE KULIAH/Tugas Analisis Medsos/UTS_AnalisisMedsos/hasilTokenizing.json')
        labelNP = 0
        labelPP = 0
        labelNTP = 0
        labelNK = 0
        labelPK = 0
        labelNTK = 0
        for data in dataset:
            if(data['labelPelaku'] == 'Positif'):
                labelPP = labelPP+1
            elif(data['labelPelaku'] == 'Negatif'):
                labelNP = labelNP+1
            elif (data['labelPelaku'] == 'Netral'):
                labelNTP = labelNTP + 1

            if (data['labelKorban'] == 'Positif'):
                labelPK = labelPK + 1
            elif (data['labelKorban'] == 'Negatif'):
                labelNK = labelNK + 1
            elif (data['labelKorban'] == 'Netral'):
                labelNTK = labelNTK + 1

        print('Positif Pelaku = ', labelPP)
        print('Negatif Pelaku = ', labelNP)
        print('Netral Pelaku = ', labelNTP)
        print('Positif Korban = ', labelPK)
        print('Negatif Korban = ', labelNK)
        print('Netral Korban = ', labelNTK)

