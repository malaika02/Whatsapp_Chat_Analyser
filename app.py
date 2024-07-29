import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8') # cnvrt chat into string format
    df = preprocessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)
    # Stats Area
    if st.sidebar.button('Show Analysis'):

        num_msgs, words, media_msg, links = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_msgs)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Messages')
            st.title(media_msg)
        with col4:
            st.header('Links Shared')
            st.title(links)

    #monthly timeline
    st.title('Monthly Timeline')
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'],color='green')
    st.pyplot(fig)

    #daily timeline
    st.title('Daily Timeline')
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

   # actvity map days

    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header('Most Busy Days')
        busy_day = helper.daily_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    #activity map monthly
    with col2:
        st.header('Most Busy Months')
        busy_month = helper.month_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # finding busiest user in group(group level)
    if selected_user == 'overall':
        st.title('Most Active Users')
        x,new_df = helper.most_busy_user(df)
        col1, col2 = st.columns(2)
        fig,ax = plt.subplots()
        with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    #wordcloud
    st.title('WordCloud')
    df_wc_img = helper.create_wordcloud(selected_user,df)
    plt.imshow(df_wc_img)
    plt.axis('off')
    st.pyplot(plt)

    #most common words
    st.title('Most Frequent Words')
    most_common_words = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    ax.barh(most_common_words[0],most_common_words[1])
    plt.xticks(rotation='vertical')
    st.pyplot(plt)

    #emoji analysis
    st.title('Emoji Analysis')
    emoji_df = helper.emoji_helper(selected_user, df)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        new_fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(new_fig)



