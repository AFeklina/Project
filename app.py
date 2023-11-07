# Import pandas, streamlit and plotly.express
import streamlit as st
import pandas as pd
import plotly.express as px

# Make header
st.header('Hey, do you want a car?')

df = pd.read_csv('vehicles_us.csv')

df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

def column_in_int(data, column_name):
    column = data[column_name]
    new_column = []
    for i in range(len(column)):
        if (pd.isna(column[i])) | (column[i] == 'unknown'):
            new_column.append('unknown')
#            st.write(new_column[i])
        else:
            new_column.append(column[i].astype('int'))
#            st.write(new_column[i])
    df[column_name] = new_column

column_in_int(df, 'price')
# ТУТ ГНЕВНЫЙ КОММЕНТАРИЙ st.write(df['price'][7])
column_in_int(df, 'model_year')
column_in_int(df, 'odometer')
column_in_int(df, 'is_4wd')

# create a text header above the dataframe
st.write('Well, we really sold a lot of them over the years of work! Look:')
# display the dataframe with streamlit
st.dataframe(df)

decades = []
years = df['model_year']
for i in range(len(years)):
    if years[i] == 'unknown':
        decades.append('unknown')
    else:
        decades.append(years[i].round(-1))
#df['model_year'] = years_int
df['decades'] = decades

# I'M HERE

st.header('Vehicle types by manufacturer')
# create a plotly histogram figure
fig = px.histogram(df, x='manufacturer', color='type')
# display the figure with streamlit
st.write(fig)

st.header('Histogram of `condition` vs `model_year`')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

st.header('Compare price distribution between manufacturers')
# get a list of car manufacturers
manufac_list = sorted(df['manufacturer'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select manufacturer 1', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select manufacturer 2',
                              options=manufac_list, 
                              index=manufac_list.index('hyundai')
                              )
# filter the dataframe 
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
st.write(fig)

# ЗДЕСЬ НУЖНЫ КОММЕНТАРИИ, И ВООБШЕ, ЭТО ЛАЖА КАКАЯ-ТО МОЯ

st.header('What about Retro?')
fig = px.histogram(df, x='model_year', y='price', histfunc='avg')
# display the figure with streamlit
st.write(fig)

st.header('Color or price?')
# ТУТ СЛОВА ПРО ТО, ЧТО ДЕЛО ВООБЩЕ-ТО В КОЛИЧЕСТВЕ МАШИН ТОЖЕ!!!
# а ещё про то, что оранжевые и жёлтые шевроле в тоовом топе

fig = px.histogram(df_filtered,
                      x='type',
                      y='price',
                      histfunc='avg')
st.write(fig)

# get user's inputs from a dropdown menu
what_manufacturer = st.selectbox(
                              label='Select manufacturer', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )

# filter the dataframe 
mask_filter = (df['manufacturer'] == what_manufacturer) & (df['paint_color'] != 'unknown')
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
#normalize = st.checkbox('Normalize histogram', value=True)
#if normalize:
#    histnorm = 'percent'
#else:
#    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='paint_color',
                      y='price',
                      histfunc='avg')
# display the figure with streamlit
st.write(fig)


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

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='manufacturer',
                      y='price',
                      histfunc='avg')
st.write(fig)

st.write('Here are details about the cars:')
st.dataframe(df_filtered)

st.write('And here is some more information about the evolution of prices, if you want:')

# ФИЛЬТРЫ И ВЫБОР
# ПОКА ЕЕ РАБОТАЕТ И ПОКАЗЫВАЕТ ВСЕ МАШИНЫ.
# НУЖНО ПОПРОБОВАТЬ СНАЧАЛА ВЫСЧИТАТЬ СРЕДНЮЮ ЦЕНУ,
# ПОТОМ ФИГАЧИТЬ ДИАГРАММУ. УЧИТЫВАЯ ВСЕ ФИЛЬТРЫ

df_new = df[df['model_year'] != 'unknown']
fig = px.scatter(df_new,
                      x='decades',
                      y='price',
                      #histfunc='avg',
                      color = 'manufacturer')
# МОЖНО ДОБАВИТЬ size='КОЛИЧЕСТВО МАШИН'
st.write(fig)

st.header('Good luck with your choice!')