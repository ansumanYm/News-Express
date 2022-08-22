# !pip install transformers

# Importing pipeline from HuggingFace transformers.
from transformers import pipeline
# Using the summarization pipeline from HuggingFace transformers.
# For further knowledge: Transformer pipeline: - https://huggingface.co/docs/transformers/v4.20.1/en/main_classes/pipelines#transformers.SummarizationPipeline
# We are not passing any models, just for faster results.

summarizer = pipeline("summarization")


def article_summary(text_article):
  # Using the summarization pipeline from HuggingFace transformers.
  # For further knowledge: Transformer pipeline: - https://huggingface.co/docs/transformers/v4.20.1/en/main_classes/pipelines#transformers.SummarizationPipeline
  # We are not passing any models, just for faster results.


  # Replacing '.', '!', '?' with end of sentence tag so that when we split on '.!?' we don't lose punctuations.

  text_article = text_article.replace('.', '.<eos>')
  text_article = text_article.replace('?', '?<eos>')
  text_article = text_article.replace('!', '!<eos>')

  # Splitting sentences on <eos> tags.
  sentences = text_article.split('<eos>')

  # Breaking the sentences into chunks with maximum of 500 words.
  max_chunk = 400
  current_chunk = 0 
  chunks = []
  for sentence in sentences:
      if len(chunks) == current_chunk + 1: 
          if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
              chunks[current_chunk].extend(sentence.split(' '))
          else:
              current_chunk += 1
              chunks.append(sentence.split(' '))
      else:
          print(current_chunk)
          chunks.append(sentence.split(' '))

  # Appending the words inside a chunk back to a sentence.
  for words in range(len(chunks)):
      chunks[words] = ' '.join(chunks[words])  

  # Using the summarizer pipline from huggingFace transformers to summarize each chunks of the article.
  result = summarizer(chunks, max_length=80, min_length=50, do_sample=False)

  article_short = ' '.join([summ['summary_text'] for summ in result])

  return article_short