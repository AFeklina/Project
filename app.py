# Import pandas, streamlit and plotly.express
import streamlit as st
import pandas as pd
import plotly.express as px

# make header
st.header('Hey, do you want a car?')

# import dataframe
df = pd.read_csv('vehicles_us.csv')

# loop over column names and replace missing values in 'is_4wd' column with 0
df['is_4wd'] = df['is_4wd'].fillna(0)
# replace missing values in 'model_year' column with average year for the model
df['model_year'] = df['model_year'].fillna(df.groupby(['model'])['model_year'].transform('median'))

# create a text header above the data
st.write('Well, we really sold a lot of them over the years of work! Look:')
st.dataframe(df)

# loop over column names and replace missing values with 'unknown'
columns_to_replace = ['cylinders', 'odometer', 'paint_color']
for column in columns_to_replace:
    df[column] = df[column].fillna('unknown')

# create the 'manufacturer' column
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# create a function converts a column to int type
def column_in_int(data, column_name):
    column = data[column_name]
    new_column = []
    for i in range(len(column)):
        if (pd.isna(column[i])) | (column[i] == 'unknown'):
            new_column.append('unknown')
        else:
            new_column.append(int(column[i]))
    df[column_name] = new_column

# convert columns
column_in_int(df, 'model_year')
column_in_int(df, 'odometer')
column_in_int(df, 'is_4wd')
column_in_int(df, 'cylinders')

# create a plotly histogram figure
fig = px.histogram(df, x='manufacturer', color='type')
# display the figure with streamlit
st.write(fig)

# create a text header above the data
st.header('New car is a good car!')
# create a text header above the chart and a plotly histogram figure
st.write('Histogram of `condition` vs `model_year`')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

# create a text header above the chart and a plotly histogram figure
st.header('What about Retro?')
st.write('Well, you can see, that retro cars are really expensive.')
fig = px.histogram(df, x='model_year', y='price', histfunc='avg')
st.write(fig)

# create a text header above the chart
st.header('Color or price?')
st.write('Hey, are orange cars really trendy?')
# get user's inputs from a dropdown menu
manufac_list = sorted(df['manufacturer'].unique())
what_manufacturer = st.selectbox(
                              label='Select manufacturer', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )

# filter the dataframe
mask_filter = (df['manufacturer'] == what_manufacturer) & (df['paint_color'] != 'unknown')
df_filtered = df[mask_filter]

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='paint_color',
                      y='price',
                      histfunc='avg')
# display the figure with streamlit
st.write(fig)

# create a text comment for the histogram above
st.write('No, of course not! But you can play with the charts some more:)')

# create a text header above the chart
st.header('Okay, let\'s go! What about the prices?')
st.write('Show what you are really waiting for from the car.')

# get user's input: slider for years
years = st.slider('How old is your dream car? Select a range of years', 1908, 2019, (2007, 2019))
years_1 = years[0]
years_2 = years[1]

df_new = df[df['model_year'] != 'unknown']

# and create two checkboxes
#on = st.toggle('Just automatic transmission')
#if on:
#    df_new = df_new[df['transmission'] == 'automatic']

#on = st.toggle('Just all-wheel drive')
#if on:
#    df_new = df_new[df['is_4wd'] == 1]

#============================

on = st.checkbox('Just automatic transmission', value=False)
if on:
    df_new = df_new[df['transmission'] == 'automatic']

on = st.checkbox('Just all-wheel drive', value=False)
if on:
    df_new = df_new[df['is_4wd'] == 1]

#============================


#filter data
mask_filter = (df_new['model_year'] >=years_1) & (df_new['model_year'] <= years_2)
df_filtered = df_new[mask_filter]

# get user's input from a dropdown menu
type_list = sorted(df['type'].unique())
options = st.multiselect(
    'What types are you interested in?',
    type_list,
    'sedan')

#filter data
df_filtered = df_filtered[df_filtered.type.isin(options)]

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='manufacturer',
                      y='price',
                      histfunc='avg')
st.write(fig)

# create a text header above the data
st.header('Price history')
st.write('And here is some more interesting information about the evolution of prices, if you want:')

# create the 'decades' column
decades = []
years = df['model_year']
for i in range(len(years)):
    if years[i] == 'unknown':
        decades.append('unknown')
    else:
        decades.append(years[i].round(-1))
#df['model_year'] = years_int
df['decades'] = decades

# create the column with count by decades
counts = df.groupby(['decades','manufacturer'])['decades'].transform('count')
df['count'] = counts

# create the column with average price by decades and manufacturer
df['avg_price'] = df.groupby(['decades','manufacturer'])['price'].transform('mean')
column_in_int(df, 'avg_price')
top_by_count = ['ford', 'toyota', 'honda', 'chevrolet', 'ram', 'jeep', 'nissan']
df_filtered = df[df.manufacturer.isin(top_by_count)]

# create a plotly scatterplot figure
fig = px.scatter(df_filtered,
                      x='decades',
                      y='avg_price',
                      size = 'count',
                      color = 'manufacturer')
st.write(fig)

# create a final text
st.write('As you can see, while cars were rare, their prices were really high.')
st.write('With the development of technology, they have decreased greatly.')
st.write('Now they are growing again, but you can certainly find something for yourself!')
st.header('Good luck with your choice!')