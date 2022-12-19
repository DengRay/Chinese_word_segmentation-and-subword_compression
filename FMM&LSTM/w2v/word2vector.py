"""
定义训练词向量类
"""
import os
import codecs
import pandas as pd
import numpy as np
from nltk.probability import FreqDist
from nltk.text import Text
from gensim.models import Word2Vec
from pickle import dump


class TrainWord2Vec(object):

    def __init__(self):
        self.corpus_path = "corpus/my_msr_cl.txt"
        self.input_text = None
        self.freq_df = None
        self._dictionary_path = 'dictionary/'
        self._w2v = None
        self._model_path = 'model/'
        self._w2v_path = self._model_path + 'word_vector.model'
        self._word2idx = {}
        self._word2idx_path = self._dictionary_path + 'word2idx.pickle'
        self._idx2word = {}
        self._idx2word_path = self._dictionary_path + 'idx2word.pickle'
        self._init_weight_wv = []
        self._init_weight_wv_path = self._model_path + 'init_weight_wv.pickle'

    def __str__(self):
        return "This is train word2vector!"

    def load_file(self, input_file):
        """

        :param input_file: 输入预料文件
        :return:
        """
        input_data = codecs.open(input_file, 'r', 'UTF-8')
        try:
            self.input_text = input_data.read()
            #print(self.input_text)
            try:
                input_data.close()
            except Exception as e:
                print('[word2vector_close_input_data]' + str(e))
        except Exception as e:
            print("[load_file]" + str(e))

    def _freq_func(self):
        if self.input_text is not None:
            input_txt = [w for w in self.input_text.split()]
            #print(input_txt)
        else:
            raise Exception('The attr input_text object is None!')
        corpus = Text(input_txt)
        f_dist = FreqDist(corpus)
        w, v = zip(*f_dist.items())
        self.freq_df = pd.DataFrame({'word': w, 'freq': v})
        self.freq_df.sort_values('freq', ascending=False, inplace=True)
        self.freq_df['idx'] = np.arange(len(v))

    def _create_freq_dict(self):
        self._freq_func()
        self._word2idx = dict((c, i) for c, i in zip(self.freq_df.word, self.freq_df.idx))
        self._idx2word = dict((i, c) for c, i in zip(self.freq_df.word, self.freq_df.idx))

    def train_word2vec(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        corpus = [line.split() for line in self.input_text.split('\n') if line != '']
        #print(corpus)
        print("Train is begin...")
        self._w2v = Word2Vec(
            sentences=corpus,
            iter=kwargs['epochs'],
            workers=kwargs['num_workers'],
            sample=kwargs['sample'],
            size=kwargs['num_features'],
            min_count=kwargs['min_word_count'],
            window=kwargs['context']
        )
        print("w2v train is done...")
        self._save_w2v()

    def train_on_word2vec(self, corpus, epochs):
        """

        :param corpus: 新补充的预料
        :param epochs: 训练迭代次数
        :return:
        """
        np.random.shuffle(corpus)
        self._w2v.build_vocab(corpus)
        print("Train is begin...")
        np.random.shuffle(corpus)
        self._w2v.train(corpus, total_examples=self._w2v.corpus_count, epochs=epochs)
        print("w2v train is done...")
        self._save_w2v()

    def load_w2v(self):
        try:
            self._w2v = Word2Vec.load(self._w2v_path)
        except Exception as e:
            print("[load_w2v_model]" + str(e))

    def check_similarity(self, vocab_1, vocab_2):
        """

        :param vocab_1: 输入待检测的词1
        :param vocab_2: 输入待检测的词2
        :return:
        """
        if self._w2v is not None:
            if isinstance(vocab_1, str) and isinstance(vocab_2, str):
                return self._w2v.similarity(vocab_1, vocab_2)
            else:
                raise Exception("The vocab_1 or vocab_2 type is wrong!")
        else:
            raise Exception("The w2v model is None object!")

    def check_most_similar(self, vocab):
        """

        :param vocab: 输入待检测的词
        :return:
        """
        if self._w2v is not None:
            if isinstance(vocab, str):
                return self._w2v.most_similar(vocab)
            else:
                raise Exception("The vocab type is wrong!")
        else:
            raise Exception("The w2v model is None object!")

    def transform_func(self):
        """ 定义 'U'为未登陆新字, 'P'为两头padding用途, 并增加两个相应的向量表示
        :return:
        """
        self._create_freq_dict()
        if self._w2v is None:
            raise Exception('The w2v object is None!')
        for i in range(len(self._idx2word)):
            self._init_weight_wv.append(self._w2v[self._idx2word[i]])
        #print(self._w2v["上"])
        char_num = len(self._init_weight_wv)
        print(char_num)
        #print(char_num)
        # idx2word
        self._idx2word[char_num] = u'U'
        self._idx2word[char_num + 1] = u'P'
        self._save_idx2word()
        # word2idx
        self._word2idx[u'U'] = char_num
        self._word2idx[u'P'] = char_num + 1
        self._save_word2idx()
        # init_weight_wv
        self._init_weight_wv.append(np.random.randn(100, ))
        self._init_weight_wv.append(np.zeros(100, ))
        self._save_init_weight()

    def _save_w2v(self):
        if os.path.exists(self._model_path) is False:
            os.mkdir(self._model_path)
        if self._w2v is not None:
            self._w2v.save(self._w2v_path)
        else:
            raise Exception("The w2v object is None!")

    def _save_init_weight(self):
        if os.path.exists(self._model_path) is False:
            os.mkdir(self._model_path)
        if self._init_weight_wv is not None:
            with open(self._init_weight_wv_path, "wb") as f:
                dump(self._init_weight_wv, f)
        else:
            raise Exception("The init_weight_wv object is None!")

    def _save_idx2word(self):
        if os.path.exists(self._dictionary_path) is False:
            os.mkdir(self._dictionary_path)
        if self._idx2word is not None:
            with open(self._idx2word_path, "wb") as f:
                dump(self._idx2word, f)
        else:
            raise Exception("The idx2word object is None!")

    def _save_word2idx(self):
        if os.path.exists(self._dictionary_path) is False:
            os.mkdir(self._dictionary_path)
        if self._word2idx is not None:
            with open(self._word2idx_path, "wb") as f:
                dump(self._word2idx, f)
        else:
            raise Exception("The word2idx object is None!")

    def get_word2vec(self):
        return self._w2v

    def get_init_weight(self):
        return self._init_weight_wv

    def get_idx2word(self):
        return self._idx2word

    def get_word2idx(self):
        return self._word2idx
