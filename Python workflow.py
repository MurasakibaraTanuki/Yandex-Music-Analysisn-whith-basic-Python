# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 06:46:45 2025

Analysis of Yandex music data
 
@author: Shizik
"""
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import plotly.express as px


yandex_data = pd.read_csv("C:\\Users\\Shizik\\Desktop\\yandex music\\yandex_music_project.csv")
yandex_data.head(15)
print(yandex_data.columns)
yandex_data.info()
yandex_data.describe()
yandex_data.dtypes
yandex_data.isnull().sum()

# becouse there are no "nan" values in the City time and day column we can start and check the load sorted by cityes and days 
yandex_data = yandex_data.rename(columns = {"Track":"track_name","  City  ":"city","Day":"day_of_the_week"})
yandex_data.columns
# creating hours column 
yandex_data["hour"] = pd.to_datetime(yandex_data["time"],format="%H:%M:%S").dt.hour
def most_frequent(series):
    return series.mode().iloc[0] if not series.mode().empty else None

def least_frequent(series):
    return series.value_counts().idxmin()
load_data = yandex_data.groupby(["city","day_of_the_week"]).agg(min_used_h = ("hour",least_frequent),
                                                                max_used_h = ("hour",most_frequent)
                                                                )
yandex_data["day_of_the_week"].unique()

def frequent(series):
    return series.value_counts()

load_data = yandex_data.groupby(["city","day_of_the_week"])["hour"].apply(lambda x: x.value_counts())
load_data_reset = load_data.reset_index()
load_data_reset.columns = ["city", "day_of_the_week", "hour", "count"]
plot = {}

# Iterate through unique combinations of city and weekday
for city_idx in load_data_reset["city"].unique():
    for week_day in load_data_reset["day_of_the_week"].unique():
        # Filter the data for the specific city and weekday
        filtered_data = load_data_reset[
            (load_data_reset["city"] == city_idx) & 
            (load_data_reset["day_of_the_week"] == week_day)
        ]
        
        if not filtered_data.empty:
            # Create the plot
            plt.figure()  # Create a new figure
            bar_plot = sb.barplot(data=filtered_data, x="hour", y="count")
            plt.title(f"{city_idx} - {week_day}")
            plt.xlabel("Hour of the Day")
            plt.ylabel("Number of Songs Played")
            
            # Store the plot in the dictionary
            plot[f"{city_idx}_{week_day}"] = bar_plot
            
# switch nan values by unknown 
yandex_data.isnull().sum()
yandex_data.duplicated().sum()
yandex_data.loc[3826,:]
yandex_data = yandex_data.drop_duplicates().reset_index(drop=True)
yandex_data = yandex_data.fillna("unknown")

moscow_data = yandex_data[yandex_data["city"]== "Moscow"]
grouped_moscow_data = moscow_data.groupby("genre").agg(count = ("genre","count"))
grouped_moscow_data = grouped_moscow_data.reset_index()

# visualization of 10 most popular  in moscow 
most_popular = grouped_moscow_data.sort_values(by="count",ascending = False)
most_popular = most_popular.iloc[0:10,:]
pie = px.pie(most_popular, names="genre", values = "count",title="Most Popular Genres in Moscow")
pie.write_html("pie_chart Most Popular Genres in Moscow.html")

# visualization of 10 most popular in Saint-Petersburg
saint_petersburg_data = yandex_data[yandex_data["city"]== "Saint-Petersburg"].groupby("genre").agg(count = ("genre","count"))
saint_petersburg_data = saint_petersburg_data.reset_index()
most_popular = saint_petersburg_data.sort_values(by="count",ascending = False)
pie = px.pie(most_popular.iloc[0:10,:], names = "genre", values = "count", title = "Most Popular Genres in Saint-Petersburg")
pie.write_html("pie_chart Most Popular Genres in Saint-Petersburg.html")

# plot 10 most populat songs for each city (excluding unknown):

most_popular_songs_moscow = moscow_data.groupby("track_name").agg(count = ("track_name","count")).reset_index().sort_values(by="count",ascending = False).iloc[1:11,:]
pie = px.pie(most_popular_songs_moscow,names = "track_name", values = "count", title = "Most Popular track names in Moscow")
pie.write_html("pie_chart_most_popular_songs_moscow.html")

Saint_Petersburg_data = yandex_data[yandex_data["city"]== "Saint-Petersburg"]
most_popular_songs_Saint_Petersburg = Saint_Petersburg_data.groupby("track_name").agg(count = ("track_name","count")).reset_index().sort_values(by="count",ascending = False).iloc[1:11,:]
pie = px.pie(most_popular_songs_Saint_Petersburg,names = "track_name", values = "count", title = "Most Popular track names in Saint-Petersburg")
pie.write_html("pie_chart_most_popular_songs_Saint-Petersburg.html")

# most popular artist  for each city 
artist_data_by_city = yandex_data.groupby(["city","artist"]).agg(count = ("artist","count"))
# no dominant artist 

# most friquent user for each city 
user_data_by_city = yandex_data.groupby(["city","userID"]).agg(count = ("userID","count"))

# sorting using loops to practice loops 
moscow = {}
seint = {}

for idx in range(len(yandex_data)):
    # Get the current city and user_id
    city = yandex_data.loc[idx, "city"]
    user_id = yandex_data.loc[idx, "user_id"]
    
    if city == "Moscow":
        if user_id not in moscow:
            moscow[user_id] = 1
        else:
            moscow[user_id] += 1
    else:  # Assuming "else" refers to Saint Petersburg
        if user_id not in seint:
            seint[user_id] = 1
        else:
            seint[user_id] += 1
            
# extracting 10 bigest values (most active users)
print(max(moscow, key=moscow.get))
sorted_keys = sorted(moscow, key=moscow.get, reverse=True)[0:10] # to sort the keys 
sorted_moscow = dict(sorted(moscow.items(), key=lambda item: item[1], reverse=True)) # to sort the dictionary 
columns_data = ["user_id","number_of_songs"]
moscow_data_id = pd.DataFrame(columns=columns_data,data=list(sorted_moscow.items())[0:10])
needed_slice = {key : sorted_moscow[key] for key in sorted_keys if key in sorted_moscow} # slice by keys if they are known 
# bar plot 
sb.barplot(data = moscow_data_id, x = "number_of_songs", y = "user_id")
plt.xlabel("Activity (number of songs listened)")
plt.ylabel("User ID")
plt.title("Most active users in Moscow")

sorted_seint = dict(sorted(seint.items(),key= lambda item: item[1],reverse =True))
needed_keys = list(sorted_seint)[0:10]
needed_slice  = {key: sorted_seint[key] for key in needed_keys if key in sorted_seint}
saint_data_id = pd.DataFrame(columns = columns_data , data = list(sorted_seint.items())[0:10])

sb.barplot(data = saint_data_id, x = "number_of_songs", y = "user_id")
plt.xlabel("Activity (number of songs listened)")
plt.ylabel("User ID")
plt.title("Most active users in Saint Petersburg")

# heatmap 

activity_by_hour_genre = yandex_data.groupby(['hour', 'genre']).size().reset_index(name='count')

# Pivot the data to create a heatmap-friendly structure
heatmap_data = activity_by_hour_genre.pivot(index='hour', columns='genre', values='count').fillna(0)
sb.heatmap(heatmap_data, cmap='coolwarm', annot=False, fmt=".0f", cbar_kws={'label': 'Number of Songs Played'})
plt.title('Heatmap of Activity by Hour and Genre')
plt.xlabel('Genre')
plt.ylabel('Hour of the Day')
plt.tight_layout()
plt.show()

heatmap_data_flattened = activity_by_hour_genre.pivot(index='hour', columns='genre', values='count').fillna(0).reset_index()

# Create an interactive heatmap
fig = px.imshow(
    heatmap_data_flattened.set_index('hour').T,
    labels={'x': 'Hour of the Day', 'y': 'Genre', 'color': 'Number of Songs Played'},
    title='Heatmap of Activity by Hour and Genre'
)
fig.write_html("Heatmap of Activity by Hour and Genre.html")
