from model.model import WriterModel
import textract
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow.keras.utils as ku

class Writer():
    def __init__(self, files):
        self.max_sentence_size = 0
        self.set_vocab = set()
        self.tokenizer = Tokenizer()
        corpus = []
        org = []
        for i in files:
            lis = str(textract.process(i, encoding = 'utf-8'))
            corpus+=lis.split(".")
        input_sequence, self.vocabular_size = self.get_sequence_of_tokens(corpus)
        predictors, label, max_sequence_len = self.generate_padded_sequences(input_sequence, self.vocabular_size)
        print(" Size of vocab : "+str(self.vocabular_size))
        self.model = WriterModel(max_sequence_len ,self.vocabular_size)
        self.model.model.fit(predictors, label, epochs=10, verbose=5)

    def get_sequence_of_tokens(self, corpus):
        ## tokenization
        self.tokenizer.fit_on_texts(corpus)
        total_words = len(self.tokenizer.word_index) + 1
        input_sequences = []
        for line in corpus:
            token_list = self.tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                input_sequences.append(n_gram_sequence)
        return input_sequences, total_words

    def generate_padded_sequences(self, input_sequences, total_words):
        max_sequence_len = max([len(x) for x in input_sequences])
        input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
        predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
        label = ku.to_categorical(label, num_classes=total_words)
        return predictors, label, max_sequence_len


    def generate_text(self, seed_text, next_words, max_sequence_len):
        for _ in range(next_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
            predicted = self.model.model.predict_classes(token_list, verbose=0)

            output_word = ""
            for word,index in tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text += " "+output_word
        return seed_text.title()