import streamlit as st
import pickle
from recommender import recommend
# import pandas as pd


st.markdown("""
<style> 
.css-nqowgj.edgvbvh3
{
  visibility : hidden;
}
.css-h5rgaw.egzxvld1
{
  visibility : hidden;
}
div.st-ef.st-e6.st-de.st-eg.st-eh.st-ei 
{
  visibility: hidden;
}
div.st-ef.st-e6.st-de.st-eg.st-eh.st-ei:before
{
  content: "Choose project requirement(s)"; 
  visibility: visible;
}
<\style>
""", unsafe_allow_html=True)


# Loading the data
data = pickle.load(open('new_data.pkl' , 'rb'))
# data = pd.read_excel('Global Staffing Tracker.xlsx')

# List of skillset
skillsets = data.columns[9:-3]


st.title("EMPLOYEE RECOMMENDER SYSTEM")
st.write("---")


# Project type
project_type = st.radio("**PROJECT TYPE:**", options=('Internal', 'Client'),horizontal= True)
 
#Project Name
st.text_input('Project Name', placeholder='Project Name')

# Client requirement input
client_req = st.multiselect("", options=skillsets)

# Level
# if client_req:
#   levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
#   client_req_level = st.multiselect("", options=levels)

with st.expander("Set custom skill level"):
  cols=st.columns(1)
  with cols[0]:
    if client_req:
      levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
      custom_levels = st.multiselect("", options=levels)

# Custom weights
with st.expander("Set custom weights"):
  cols=st.columns(6)
  with cols[0]:
    skill = st.number_input('**Skill**', min_value=1, max_value=3, value= 3, step=1)
  with cols[1]:
    rank = st.number_input('**Rank**', min_value=1, max_value=3, value= 2, step=1)
  with cols[2]:
    experience = st.number_input('**Yrs. of Exp.**', min_value=1, max_value=3, value= 2, step=1)
  with cols[3]:
    cdc = st.number_input('**CDC Score**', min_value=1, max_value=3, value= 3, step=1)
  with cols[4]:
    internal = st.number_input('**Internal Project**', min_value=1, max_value=3, value= 1, step=1)
  with cols[5]:
    client = st.number_input('**Client Project**', min_value=1, max_value=3, value= 3, step=1)


if st.button('**Recommend**'):
    st.write("")
    try:
      ideal, nonideal, all = recommend(data, client_req, project_type, skill, rank, experience, cdc, internal, client, custom_levels)

      st.write("**IDEAL:** Employee(s) with expertise in **all** project requirement(s)")
      ideal.iloc[:10, :]

      st.write("---")

      st.write("**ALL FEASIBLE EMPLOYEES:**")
      all.iloc[:10, :]
    except :
       st.write("*Choose project requirement(s) to proceed*")



   