
### ------------------------------IMPORTING LIBRARIES--------------------------------------


import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import io
from newspaper import Article
import nltk
import streamlit as st
nltk.download('punkt')


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
nlp = spacy.load('en_core_web_sm')


### --------------------------------FUNCTIONS USED-----------------------------------


# Function that gives the list of todays Top news:-
def get_top_news():
    url = 'https://news.google.com/news/rss'
    open = urlopen(url)  # Open that url
    read = open.read()  # read data from url
    open.close()  # close the object
    sp_page = soup(read, 'xml')  # scrapping data from site using beautifulSoup
    news_list = sp_page.find_all('item')  # finding all the <item> tags using bs. This will contain the list of news.
    return news_list


# Function that gets the list of topics
def get_news_topic(topic):
    url = 'https://news.google.com/rss/search?q={}'.format(topic)
    open = urlopen(url)  # Open that site
    read = open.read()  # read data from site
    open.close()  # close the object
    sp_page = soup(read, 'xml')  # scrapping data from site using beautifulSoup
    news_list = sp_page.find_all('item')  # finding all the <item> tags using bs. This will contain the list of news.
    return news_list


# Function that gets the list of category topics
def get_category_news(topic):
    url = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    open = urlopen(url)  # Open that site
    read = open.read()  # read data from site
    open.close()  # close the object
    sp_page = soup(read, 'xml')  # scrapping data from site using beautifulSoup
    news_list = sp_page.find_all('item')  # finding all the <item> tags using bs. This will contain the list of news.
    return news_list


# Function that gets poster link
def get_news_poster(poster_link):
    try:
        url = urlopen(poster_link)
        raw_data = url.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except:
        st.warning("No PREVIEW IMAGE FOUND")
        
# A Function that summarises the test using Word frequency method.
def article_summary(text_article):

    doc = nlp(text_article)
    # Word tokenisation
    tokens = [token.text for token in doc]
    #print(tokens)
    stopwords = list(STOP_WORDS)
    # We will include \n into punctuation.
    punctuations = punctuation + '\n' + '\n\n'


    # Finding out the most used words.
    word_frequency = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuations:
                if word.text.lower() not in word_frequency.keys():
                    word_frequency[word.text.lower()] = 1
                else:
                    word_frequency[word.text.lower()] += 1


    # Max Frequency
    max_frequency = max(word_frequency.values())
    # Normalising the word frequencies 
    for word in word_frequency.keys():
        word_frequency[word] = word_frequency[word]/max_frequency


    # Sentence tokenisation
    sent_token = [sent for sent in doc.sents]

    # Most relevant sentence to our passage.

    sentence_score = {}

    for sent in sent_token:
        for word in sent:
            if word.text.lower() in word_frequency.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequency[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequency[word.text.lower()]


    # Selecting 35% of sentences from total passage as summary.
    select_length = int(len(sent_token)*0.35)
    # Importing nlargest from heapq
    from heapq import nlargest

    summary = nlargest(select_length, sentence_score, key=sentence_score.get)

    summary_untokenised = [word.text for word in summary]
    end_product = ' '.join(summary_untokenised)

    end_product = end_product.replace('\n', '')

    return end_product

        
# Function that displays news.
def display_news(list_of_news, no_of_news):

    for news in list_of_news[0:no_of_news]:
        
        # st.markdown(f"({c})[ {news.title.text}]({news.link.text})")
        st.markdown("""##### {}""".format(news.title.text))
        article = Article(news.link.text)
        try:
            article.download()
            article.parse()
            text_article = article.text
        except Exception as e:
            st.error("Could not extract this news from url. Please check the next one.")


        st.markdown("`Published Date`: {}".format(news.pubDate.text))
        get_news_poster(article.top_image)
    
        with st.expander('Read this article:'):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(article_summary(text_article)),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        
### -----------------------------------------END----------------------------------------------------






### ---------------------------------------------STREAMLIT WEB APP-------------------------------------        



# Sidebar ----------------------------------------
with st.sidebar.form(key='columns_in_form'):
    
    st.subheader("App Parameters:")
    
    no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

    preference = ['Trending News', 'Choose a Topics', 'Search Keyword']

    news_type = st.selectbox(
                "Select your preference:", preference , index=0, help='The default type is {}.'.format(preference[0]))
    

    if news_type == preference[1]:
        
        preferred_topic = [ 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                        'HEALTH']
        chosen_topic = st.selectbox("Choose your preferred Topic", preferred_topic, index=0, help='The default is choosen: {}.'.format(preferred_topic[0]))
        
    st.form_submit_button()
    st.markdown('`Click Submit to update app!`')


    

# App Body ------------------------------------------

st.title("News Express", )

#Adding an expander to the app 
with st.expander("About the App"):
     st.write(""" 
        This is a Streamlit based web app that provides you with news articles in short and summarised form so that you can go through it quickly. 
        We use the Google RSS feeder to provide you with the trending news, catagorical news and Searched news articles. The main aim of this app is
        to provide you with short summarized news articles so that you can

         """)




if news_type == preference[0]:
    
    st.subheader("Trending Today:")
    news_list = get_top_news()
    display_news(news_list, no_of_news)

elif news_type == preference[1]:
        
    news_list = get_category_news(chosen_topic)
    if news_list:
        st.subheader("{} News:".format(chosen_topic))
        display_news(news_list, no_of_news)
    else:
        st.error("No News found for {}".format(chosen_topic))


elif news_type == preference[2]:
    user_topic = st.text_input("Enter Topic Here....")

    try:
            
        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = get_news_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("News based on your search: {} ".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please provide a topic to search")
    except:
        st.warning("Please enter a valid keyword")


### ---------------------------------------------------------END-----------------------------------------------