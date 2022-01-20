import json
from collections import Counter
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    '''Generates chat statistics from a telegram chat json file'''
    
    def __init__(self, chat_json: Union[str, Path]):
        # Load Chat Data
        logger.info(f"Loading Chat Data from {chat_json}")
        with open(chat_json) as f:
            self.chat_data = json.load(f)
            
            self.normalizer = Normalizer()
            # load stopwords
            
            stop_words = open(str(DATA_DIR / 'stopword.txt')).readlines()
            stop_words = list(map(str.strip,stop_words))
            self.stop_words = list(map(self.normalizer.normalize,stop_words))
       
       
    def generate_word_cloud(self,output_dir: Union[str, Path]):
        text_content = ''
        for i in self.chat_data['messages']:
            if type(i['text']) is str:
                tokens = word_tokenize(i['text'])
                tokens = list(filter(lambda item: item not in self.stop_words,tokens))
                text_content += f" {' '.join(tokens)}"
        
        text_content = self.normalizer.normalize(text_content)
        self.text_content = arabic_reshaper.reshape(text_content)
        #text_content = get_display(text_content)
           
        wordcloud = WordCloud(
            width=1800,
            height=800,
            background_color='Black',
            font_path=str(DATA_DIR / 'Vazir-Black.ttf')).generate(text_content)
        
        wordcloud.to_file(Path(output_dir) / 'wordcloud.png')





if __name__ == "__main__":
    obj = ChatStatistics(chat_json=DATA_DIR / 'result.json')
    obj.generate_word_cloud(DATA_DIR)
