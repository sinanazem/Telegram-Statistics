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
        '''
        :param chat_json: path to telegram export json file
        
        '''
        # Load Chat Data
        logger.info(f"Loading Chat Data from {chat_json}")
        with open(chat_json) as f:
            self.chat_data = json.load(f)
            
            self.normalizer = Normalizer()
            # load stopwords
            logger.info(f"Loading stopwords from {DATA_DIR / 'stopwords.txt'}")
            stop_words = open(str(DATA_DIR / 'stopword.txt')).readlines()
            stop_words = list(map(str.strip,stop_words))
            self.stop_words = list(map(self.normalizer.normalize,stop_words))
       
       
    def generate_word_cloud(self,output_dir: Union[str, Path]):
        '''Generates a word cloud from a chat data
        
        :param output_dir: path to output directory for word cloud image
        '''
        
        logger.info(f"Loading text content...")
        text_content = ''
        for i in self.chat_data['messages']:
            if type(i['text']) is str:
                tokens = word_tokenize(i['text'])
                tokens = list(filter(lambda item: item not in self.stop_words,tokens))
                text_content += f" {' '.join(tokens)}"
        # normalize, reshape for final word cloud
        text_content = self.normalizer.normalize(text_content)
        self.text_content = arabic_reshaper.reshape(text_content)
        #text_content = get_display(text_content)
        
        logger.info(f"generating word cloud")   
        #generate wordcloud
        wordcloud = WordCloud(
            width=1800,
            height=800,
            background_color='Black',
            font_path=str(DATA_DIR / 'Vazir-Black.ttf')).generate(text_content)
        
        wordcloud.to_file(Path(output_dir) / 'wordcloud.png')





if __name__ == "__main__":
    obj = ChatStatistics(chat_json=DATA_DIR / 'result.json')
    obj.generate_word_cloud(DATA_DIR)
