from urlextract import URLExtract
extractor = URLExtract()

from wordcloud import WordCloud

def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user']==selected_user]


    # Total Messages
    num_messages = df.shape[0]

    # Total Words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    num_words = len(words)

    # Total Media Messages
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Total Links
    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))
    num_links = len(links)


    return num_messages,num_words,num_media,num_links


def most_busy_users(df):
    x = df['user'].value_counts().head()
    msg_percent_df =  round(df['user'].value_counts()/df.shape[0] *100,2)
    return x,msg_percent_df


def create_wordcloud(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    wc = WordCloud(width=500,height=100,min_font_size=10,background_color='white',font_path='font/gargi.ttf')
    df = df[df['message']!='<Media omitted>\n']
    df = df[df['message'] != '\u200eimage omitted\n']
    df = df[df['message']!='\u200esticker omitted\n']

    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
