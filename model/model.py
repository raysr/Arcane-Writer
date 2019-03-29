import tensorflow as tf

class WriterModel():
    def __init__(self, max_sequence_len, total_words):
        input_len = max_sequence_len - 1
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Embedding(total_words, 10, input_length=input_len))
        self.model.add(tf.keras.layers.LSTM(200))
        self.model.add(tf.keras.layers.Dropout(0.1))
        self.model.add(tf.keras.layers.Dense(total_words, activation="softmax"))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

