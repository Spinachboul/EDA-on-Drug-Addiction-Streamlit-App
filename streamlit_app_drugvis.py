import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

@st.cache_data
def get_data():
     df = pd.read_csv('drugAddiction.csv',encoding='cp1252')
     df['values'] = [1]*len(df)
     return df

# Plotting funtion
@st.cache_data
def create_heatmap(index, columns,title):
     fig, ax = plt.subplots(1)
     df_heatmap = df.pivot_table(values = 'values',index=index,columns=columns,aggfunc=np.sum)
     sns.heatmap(df_heatmap,annot=True,ax=ax).set_title(title)
     return fig

@st.cache_data
def create_histplot(df, pick, AGE,GENDER,EDULVL,columns = ['Age','Gender','Education']):
     n = len(columns)
     fig, ax = plt.subplots(n)
     fig.set_figheight(5)
     fig.set_figheight(10)
     df = df.where(df['Gender'].isin(GENDER)).dropna()
     df = df.where(df['Age'].isin(AGE)).dropna()
     df = df.where(df['Education'].isin(EDULVL)).dropna()
     
     for i in range(n): 
          sns.histplot(x = df[pick], hue=df[columns[i]], ax = ax[i], multiple='dodge').set_title(f"Based on {columns[i]}", fontname="Times New Roman",fontweight = 'bold')
     fig.tight_layout()
     return fig

#configuration of the page
st.set_page_config(layout="wide")

hcol1, hcol2 = st.columns((4,1))
hcol1.title("Exploring the effects of Drug Addiciton")
hcol1.write("Presented by TAM (The AI and ML Club)")
hcol1.write("This app performs a simple visulisation of open source data the **Drug Addiction in Bangladesh with reasons** ")

hcol2.image("TAM_logo.jpg", width=200)

# Loading the dataset
df = get_data()

# First type of analysis
st.subheader("Investigate features based on their Age group,Gender and Education level")

fscol1, fscol2, fscol3 = st.columns(3)

AGE = fscol1.multiselect("Pick Age Groups", list(df['Age'].unique()))
GENDER = fscol2.multiselect("Pick Gender", list(df['Gender'].unique()))
EDULVL = fscol3.multiselect("Pick Education Levels", list(df['Education'].unique()))
COMP_FEATURE = ['Age','Gender','Education']

col1, col2 = st.columns((1,3))
pick = col1.selectbox("Pick a feature to investigate",list(set(df.columns)-{'Age','Gender','Education','values'}))
col2.pyplot(create_histplot(df,pick,AGE,GENDER,EDULVL,COMP_FEATURE))

# Second type of investigation
st.subheader("Investigate relationship between two features")
bcol1, bcol2 = st.columns((1,3))
feat1 = bcol1.selectbox("Select first feature to investigate",list(set(df.columns)-{'values'}))
feat2 = bcol1.selectbox("Select second feature to investigate",list(set(df.columns)-{'values',feat1}))
if feat1 and feat2:
     bcol2.pyplot(create_heatmap(feat1,feat2, f"{feat1} vs {feat2}"))

