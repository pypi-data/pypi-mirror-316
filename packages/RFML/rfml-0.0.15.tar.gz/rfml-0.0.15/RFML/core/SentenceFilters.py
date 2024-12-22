from RFML.interface.ISentenceFilter import ISentenceFilter


class SentenceFilters:
    one_word_patterns = []
    block_sentences_patterns = []

    multi_word_patterns = {}
    multi_word_list = {}
    multi_word_enabled = {}

    def allow_multi_word_patterns(self, filter_name, sentence_filter: ISentenceFilter, root_lemmas, enabled=True):
        # auto name model_name+label+lemma
        self.multi_word_list[filter_name] = root_lemmas
        self.multi_word_patterns[filter_name] = sentence_filter
        self.multi_word_enabled[filter_name] = enabled

    def allow_one_word_patterns(self, one_words: []):
        for item in one_words:
            if item not in self.one_word_patterns: self.one_word_patterns.append(item)
        # if one_words: self.one_word_patterns.extend(one_words)

    def block_invalid_sentences(self, block_sentences: []):
        for item in block_sentences:
            if item not in self.block_sentences_patterns: self.block_sentences_patterns.append(item)
        # if block_sentences: self.block_sentences_patterns.extend(block_sentences)

    # class MultiWordPatterns:
    #     def __init__(self, sentence_filter: ISentenceFilter, enabled=True, root_lemmas=[]):
    #         self.multi_word_patterns = sentence_filter
    #         self.enabled = enabled
    #         self.root_lemmas = root_lemmas


