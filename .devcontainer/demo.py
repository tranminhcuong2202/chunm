import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# To set a webpage title, header and subtitle
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")


#read in the file
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")
movies_data.info()
movies_data.duplicated()
movies_data.count()
movies_data.dropna()


# Creating sidebar widget filters from movies dataset
year_list = movies_data['year'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()


# Add the filters. Every widget goes in here
with st.sidebar:
    st.write("Select a range on the slider (it represents movie score) to view the total number of movies in each selected genre that falls within that range ")
    #create a slider to hold user scores
    new_score_rating = st.slider(label = "Choose a score range:",
                                     min_value = 1.0,
                                     max_value = 10.0,
                                     value = (3.0,4.0))


    st.write("Select your preferred genre(s) and year to view the movies released that year and in those genres")
    #create a multiselect option that holds genre
    new_genre_list = st.multiselect('Choose Genre(s):',
                                         genre_list, default = ['Animation', 'Horror', 'Fantasy', 'Romance'])

    #create a selectbox option that holds all unique years
    year = st.selectbox('Choose a Year', year_list, 0)

#Configure the slider widget for interactivity
score_info = (movies_data['score'].between(*new_score_rating))



#Configure the selectbox and multiselect widget for interactivity
new_genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data['year'] == year)


#VISUALIZATION SECTION
#group the columns needed for visualizations
col1, col2, col3 = st.columns([2, 2, 2]) # Adjust column ratios as needed
with col1:
    st.write(f"""#### List of movies in {', '.join(new_genre_list)} released in {year} """)
    dataframe_genre_year = movies_data[new_genre_year][['name', 'genre', 'year']]
    st.dataframe(dataframe_genre_year, width = 400)

with col2:
    st.write(f"""#### Number of movies per selected genre within the score range: {new_score_rating} """)
    filtered_by_score = movies_data[score_info]
    genre_counts = filtered_by_score[filtered_by_score['genre'].isin(new_genre_list)]['genre'].value_counts().reset_index()
    genre_counts.columns = ['genre', 'count']
    if not genre_counts.empty:
        figpx = px.bar(genre_counts, x = 'genre', y = 'count', title = 'Number of Movies per Genre')
        st.plotly_chart(figpx)
    else:
        st.warning("No movies found within the selected score range and genres.")

with col3:
    st.write("""#### Distribution of Movies by Genre """)
    genre_distribution = movies_data['genre'].value_counts().reset_index()
    genre_distribution.columns = ['genre', 'count']
    fig_pie = px.pie(genre_distribution, names='genre', values='count',
                     title='Distribution of Movies by Genre')
    st.plotly_chart(fig_pie)


 # creating a bar graph with matplotlib
st.write("""
Average Movie Budget, Grouped by Genre
    """)
avg_budget = movies_data.groupby('genre')['budget'].mean().round().reset_index()
genre_budget = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize = (19,10)) # Reduced figure size
plt.bar(genre_budget, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Average Budget of Movies in Each Genre')
st.pyplot(fig)



#Link web : http://localhost:8510/
#Thành viên: Trần Minh Cường 
