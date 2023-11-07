# Import pandas, streamlit and plotly.express
import streamlit as st
import pandas as pd
import plotly.express as px

# Make header
st.header('Hey, do you want a car?')
# Import dataframe
df = pd.read_csv('vehicles_us.csv')

# Loop over column names and replace missing values in 'is_4wd' column with 0.
df['is_4wd'] = df['is_4wd'].fillna(0)
# Loop over column names and replace missing values in 'model_year' column with average year for the model.
df['model_year'] = df['model_year'].fillna(df.groupby(['model'])['model_year'].transform('median'))

# Loop over column names and replace missing values with 'unknown'.
columns_to_replace = ['cylinders', 'odometer', 'paint_color']
for column in columns_to_replace:
    df[column] = df[column].fillna('unknown')

#Create the 'manufacturer' column.
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

#Create a function converts a column to int type.
def column_in_int(data, column_name):
    column = data[column_name]
    new_column = []
    for i in range(len(column)):
        if (pd.isna(column[i])) | (column[i] == 'unknown'):
            new_column.append('unknown')
        else:
            new_column.append(int(column[i]))
    df[column_name] = new_column

# Convert columns.
column_in_int(df, 'price')
column_in_int(df, 'model_year')
column_in_int(df, 'odometer')
column_in_int(df, 'is_4wd')
column_in_int(df, 'cylinders')

# Create a text header above the dataframe.
st.write('Well, we really sold a lot of them over the years of work! Look:')

# display the dataframe with streamlit.
st.dataframe(df)

# Create a text header above the chart.
st.header('Vehicle types by manufacturer')
# Create a plotly histogram figure.
fig = px.histogram(df, x='manufacturer', color='type')
# display the figure with streamlit
st.write(fig)

# Create a text header above the chart and a plotly histogram figure.
st.header('Histogram of `condition` vs `model_year`')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

st.header('What about Retro?')
fig = px.histogram(df, x='model_year', y='price', histfunc='avg')
# display the figure with streamlit
st.write(fig)

st.header('Color or price?')
# А здесь "можете поиграть немного тут"

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
# ТУТ СЛОВА ПРО ТО, ЧТО ДЕЛО ВООБЩЕ-ТО В КОЛИЧЕСТВЕ МАШИН ТОЖЕ!!!
# а ещё про то, что оранжевые и жёлтые шевроле в тоовом топе
# И про то, что на самом деле всё зависит от типа машины гораздо больше, чем от цвета


years = st.slider('How old is your dream car? Select a range of years', 1908, 2019, (2007, 2019))
#st.write('Values:', age)
years_1 = years[0]
years_2 = years[1]

df_new = df[df['model_year'] != 'unknown']

on = st.toggle('Just automatic transmission')
if on:
    df_new = df_new[df['transmission'] == 'automatic']

on = st.toggle('Just all-wheel drive')
if on:
    df_new = df_new[df['is_4wd'] == 1]

mask_filter = (df_new['model_year'] >=years_1) & (df_new['model_year'] <= years_2)
df_filtered = df_new[mask_filter]

type_list = sorted(df['type'].unique())

options = st.multiselect(
    'What types are you interested in?',
    type_list,
    'sedan')

#df_filtered = df_filtered[df_filtered['type'] in options]
df_filtered = df_filtered[df_filtered.type.isin(options)]

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='manufacturer',
                      y='price',
                      histfunc='avg')
st.write(fig)

st.write('Here are details about the selected cars:')
st.dataframe(df_filtered)

st.write('And here is some more interesting information about the evolution of prices, if you want:')

decades = []
years = df['model_year']
for i in range(len(years)):
    if years[i] == 'unknown':
        decades.append('unknown')
    else:
        decades.append(years[i].round(-1))
#df['model_year'] = years_int
df['decades'] = decades



# ФИЛЬТРЫ И ВЫБОР
# ПОКА ЕЕ РАБОТАЕТ И ПОКАЗЫВАЕТ ВСЕ МАШИНЫ.
# НУЖНО ПОПРОБОВАТЬ СНАЧАЛА ВЫСЧИТАТЬ СРЕДНЮЮ ЦЕНУ,
# ПОТОМ ФИГАЧИТЬ ДИАГРАММУ. УЧИТЫВАЯ ВСЕ ФИЛЬТРЫ

# количество для марки и года
counts = df.groupby(['decades','manufacturer'])['decades'].transform('count')
df['count'] = counts

#средняя цена для марки и года
df['mean_price'] = df.groupby(['decades','manufacturer'])['price'].transform('mean')
column_in_int(df, 'mean_price')
top_by_count = ['ford', 'toyota', 'honda', 'chevrolet', 'ram', 'jeep', 'nissan']
df_filtered = df[df.manufacturer.isin(top_by_count)]


fig = px.scatter(df_filtered,
                      x='decades',
                      y='mean_price',
                      size = 'count',
                      color = 'manufacturer')
# МОЖНО ДОБАВИТЬ size='КОЛИЧЕСТВО МАШИН'
st.write(fig)

st.header('Good luck with your choice!')