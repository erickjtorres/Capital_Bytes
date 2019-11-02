from flask_restful import Resource, reqparse
from resources.models.summary import ArticleSummary, ArticlesSummaries
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from resources.helper.get_news_articles import get_news_articles

#https://[heroku_url]/summary?companyName=apple
parser = reqparse.RequestParser()
parser.add_argument('companyName', type=str)

class GetSummaryOfArticles(Resource):
  def get(self):
    args = parser.parse_args()
    company_name = args['companyName']
    articles = get_news_articles(company_name)
    article_summaries = []
    for article in articles.articles:
      content = article.content 
      summary = compute_full_summary(content) 
      title = article.title 
      article_summaries.append(vars(ArticleSummary(content=summary, title=title)))
    return vars(ArticlesSummaries(article_summaries))


def compute_full_summary(text): 
  # 1 Create the word frequency table
  freq_table = _create_frequency_table(text)

  '''
  We already have a sentence tokenizer, so we just need 
  to run the sent_tokenize() method to create the array of sentences.
  '''

  # 2 Tokenize the sentences
  sentences = sent_tokenize(text)

  # 3 Important Algorithm: score the sentences
  sentence_scores = _score_sentences(sentences, freq_table)

  # 4 Find the threshold
  threshold = _find_average_score(sentence_scores)

  # 5 Important Algorithm: Generate the summary
  summary = _generate_summary(sentences, sentence_scores,  threshold)
  return summary 

def _create_frequency_table(text_string) -> dict:
  """
  we create a dictionary for the word frequency table.
  For this, we should only use the words that are not part of the stopWords array.
  Removing stop words and making frequency table
  Stemmer - an algorithm to bring words to its root word.
  :rtype: dict
  """
  stopWords = set(stopwords.words("english"))
  words = word_tokenize(text_string)
  ps = PorterStemmer()

  freqTable = dict()
  for word in words:
      word = ps.stem(word)
      if word in stopWords:
          continue
      if word in freqTable:
          freqTable[word] += 1
      else:
          freqTable[word] = 1

  return freqTable

def _score_sentences(sentences, freqTable) -> dict:
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words

        '''
        Notice that a potential issue with our score algorithm is that long sentences will have an advantage over short sentences. 
        To solve this, we're dividing every sentence score by the number of words in the sentence.
        
        Note that here sentence[:10] is the first 10 character of any sentence, this is to save memory while saving keys of
        the dictionary.
        '''

    return sentenceValue

def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary