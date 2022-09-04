# News Express Web App
## Visit Web app:- https://news-expressapp.herokuapp.com

News Express is a python web app build using Streamlit. This app provides us with daily news articles in short summarized form. This app derives news from Google Rss feeder and then uses Natural language processing, word frequency based Extractive summarization method, to produce a short Summary for the readers. 

This app is deployed on Heroku Cloud Platform.

![image](https://user-images.githubusercontent.com/96365389/186627483-f8fb2023-c0ce-4427-b1b2-a22cfc4c8961.png)
![image](https://user-images.githubusercontent.com/96365389/186627636-b4ec3166-4645-4fa5-aef7-fcd510bab6e1.png)


---

## Tech Stack:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

##### `Streamlit` `Natural Language processing` `SpaCy`
---

---

## Project Walkthrough

1. Collecting data from Google RSS Feeder
2. Extracting text using beautiful Soup
3. Text summarization using NLP and SpaCy.
4. Building a Streamlit Web App
---

## NLP (Natural Language Processing) 
It is the field of artificial intelligence that studies the interactions between computers and human languages, in particular how to program computers to process and analyze large amounts of natural language data. The hardest NLP tasks are the ones where the output isn’t a single label or value (like Classification and Regression), but a full new text (like Translation, Summarization and Conversation).

## Text Summarization

Text summarization is the process of creating shorter text without removing the semantic structure of text.

![image](https://user-images.githubusercontent.com/96365389/186690772-cd8a5bfb-c594-4130-87db-ee119c7f46fe.png)

### Extractive Text Summarization:

It is the traditional method developed first. The main objective is to identify the significant sentences of the text and add them to the summary. You need to note that the summary obtained contains exact sentences from the original text.

### Abstractive Text Summarization:

It is a more advanced method, many advancements keep coming out frequently(I will cover some of the best here). The approach is to identify the important sections, interpret the context and reproduce in a new way. This ensures that the core information is conveyed through shortest text possible. Note that here, the sentences in summary are generated, not just extracted from original text.

In this project I have used TextRank algorithm.

### What is TextRank algorithm?

TextRank is an extractive summarization technique. It is based on the concept that words which occur more frequently are significant. Hence , the sentences containing highly frequent words are important . Based on this , the algorithm assigns scores to each sentence in the text . The top-ranked sentences make it to the summary.


