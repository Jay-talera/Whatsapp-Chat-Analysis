import streamlit as st
import time
import preprocessor,helper
import matplotlib.pyplot as plt 

# st.sidebar.title('Whatsapp Chat Analyzer')

df = None
device_type = None


# with st.sidebar:
#     device_type = st.selectbox("Device",['Select a Device','Android','Ios'])

with st.sidebar:
    device_type = st.selectbox('Device Type',['Select A Device Type','Android','IOS'])
    uploaded_file = st.file_uploader("Choose a file without media")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode('utf-8')
        if device_type == "Android":
            df = preprocessor.preprocess_android(data)
        elif device_type == 'IOS':
            df = preprocessor.preprocess_ios(data)
        else:
            st.warning('Please Select A Device')
if df is not None:
    # st.dataframe(df)

    # Unique User
    user_list = df['user'].unique().tolist()
    user_list.sort()
    
    user_list.insert(0,"Overall")
    if len(user_list)>int(len(df)-len(df)*0.8):
        st.sidebar.warning('Please Check Device Type')
        st.sidebar.warning('File Format Not Supported')
    else:
        if "group_notification" in user_list:
            user_list.remove('group_notification')
        selected_user = st.sidebar.selectbox("User",user_list,index=0)
        if st.sidebar.button("Show analysis"):
            num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)
            col1,col2,col3,col4 =  st.columns(4)

            with col1:
                    st.header("Total Messages")
                    st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(num_words)
            with col3:
                st.header("Media Shared")
                st.title(num_media)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            if selected_user == 'Overall':
                    # st.title('Most Busy Users')
                    x,msg_percent_df = helper.most_busy_users(df)
                    col1,col2 = st.columns(2)
                    
                    figa,axa = plt.subplots()
                    plt.xticks(rotation=65)
                    figb,axb = plt.subplots()
                    plt.xticks(rotation=65)
                    

                    with col1:
                        st.header('Most Busy User')
                        axa.bar(x.index,x.values,color='#d9b3ff')
                        st.pyplot(figa)
                    with col2:
                        st.header('Message Percent')
                        axb.bar(msg_percent_df.index,msg_percent_df.values,color='#d9b3ff')
                        st.pyplot(figb)

                # wordcloud
            st.title('Word Cloud')
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)