import re

class SimpleTokenizer:
    def __init__(self):
        self.vocab = {'<PAD>': 0, '<UNK>': 1}
        self.reverse_vocab = {0: '<PAD>', 1: '<UNK>'}

    def build_vocab(self, code_samples, vocab_size=1000):
        word_count = {}
        for sample in code_samples:
            tokens = self.tokenize_code(sample)
            for token in tokens:
                word_count[token] = word_count.get(token, 0) + 1
        
        sorted_vocab = sorted(word_count, key=word_count.get, reverse=True)[:vocab_size]
        for idx, token in enumerate(sorted_vocab, start=2):
            self.vocab[token] = idx
            self.reverse_vocab[idx] = token

    def tokenize_code(self, code):
        return re.findall(r"[\w]+|[^\s\w]", code)

    def __call__(self, code):
        tokens = self.tokenize_code(code)
        return [self.vocab.get(token, self.vocab['<UNK>']) for token in tokens]

    def decode(self, tokens):
        return ' '.join([self.reverse_vocab.get(t, '<UNK>') for t in tokens])
