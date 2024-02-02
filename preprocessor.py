import re
import pandas as pd

def preprocess_android(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}'

    messages = re.split(pattern, data)[2:]
    dates = re.findall(pattern, data)[1:]

    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'])

    df['user_message'].replace(to_replace=r'^\u202f(PM|AM|am|pm) - ',value='',regex=True,inplace=True)


    users = []
    messages = []
    for msg in df['user_message']:
        entry = re.split('([\w\W]+?):\s',msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    return df


def preprocess_ios(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}:\d{1,2}'

    messages = re.split(pattern,data)[2:]
    dates = re.findall(pattern,data)[1:]
    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    df['message_date'].replace(to_replace=r'\[',value='',inplace=True,regex=True)
    df['message_date'] = pd.to_datetime(df['message_date'])
    df['user_message'].replace(to_replace=r'\u202f(PM|AM|am|pm)]',value='',regex=True,inplace=True)


    users = []
    messages = []
    for msg in df['user_message']:
        entry = re.split('([\w\W]+?):\s',msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)
    

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day

    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    return df
