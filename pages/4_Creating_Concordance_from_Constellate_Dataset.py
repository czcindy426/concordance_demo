#!/usr/bin/env python
# coding: utf-8

"""
# My first app, upload user's Constellate dataset page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""
import streamlit as st
from io import StringIO
import nltk
import pandas as pd
import constellate
import streamlit_ext as ste
nltk.download('punkt')


### set page configuration
st.set_page_config(page_title="Creating concordance from a Constellate dataset",
    layout="wide")

st.markdown("# Creating concordance from a Constellate dataset")
st.sidebar.header("Concordance from a Constellate dataset")

# section: Enter a dataset id
st.header("Enter a Constellate dataset id")

def tokenize(data):
    """tokenize a string and produce a nltk text object"""
    data = data.lower()
    tokens = nltk.word_tokenize(data)
    text = nltk.Text(tokens)
    return text
def get_concordance(input_string, data_string, lines=25, width=79, write=True):
    """takes an input string and return a concordance list"""
    input_string = input_string.lower()
    input_ls = input_string.split()
    text = tokenize(data_string)
    concordance = text.concordance_list(input_ls, width, lines)
    if write:
        for i in concordance:
            st.write(i.line)
    else:
        return concordance
def get_id_title_fulltext(docs):
    """takes a generator of dictionaries from Constellate dataset
     and return a list of ids, titles, full text"""
    id_title_fulltext = [(f['id'], f['title'], ''.join(f['fullText'])) for f in docs]
    ids = [item[0] for item in id_title_fulltext]
    titles = [item[1] for item in id_title_fulltext]
    texts = [item[2] for item in id_title_fulltext]
    return ids, titles, texts

# Use the value of a session state variable 'step' to track the sequencing relation between widgets
if st.session_state.get('step') is None:
    st.session_state['step'] = 0

# First step: enter a dataset id to download a Constellate dataset
ds_id = str(st.text_input("Paste your dataset id here 👇")).strip()
if ds_id:
    dataset_file = constellate.download(ds_id, 'jsonl')
    success_message = '<p style="font-family:roboto; color:Green;font-size:20px;">Dataset downloaded successfully.</p>'
    st.markdown(success_message, unsafe_allow_html=True)
    st.session_state['step'] = 1

# Second step:
if st.session_state['step'] == 1:
    st.header("Specify parameters to get concordance")
    # User enter a word/phrase and specify number of lines and characters
    string = str(st.text_input("""Give a word/phrase to get concordance 👇""", key='upstring'))
    num_lines= str(st.text_input("""Enter an integer to specify how many lines you want to show 👇""", key='num_lines'))
    num_char = str(st.text_input("""Enter an integer to specify how many characters you want to show on each line 👇""", key='num_char'))     
    string = string.lower()  
    ### Create a dataframe to store the concordance from the files for users to download
    # read in the documents from the dataset
    if string and num_lines and num_char:
        with st.spinner('Concordance in generation. Please wait. Depending on the size of your dataset, this may take 10 - 30min.'):
            docs = constellate.dataset_reader(dataset_file)
            f_id_ls, f_name_ls, fulltext_ls = get_id_title_fulltext(docs)
            concordance_all = [[i.line for i in get_concordance(string, content, lines=int(num_lines), width=int(num_char), write=False)] for content in fulltext_ls]
            df = pd.DataFrame({'id': f_id_ls, 'title': f_name_ls, 'concordance':concordance_all})
            df = df.explode('concordance').reset_index(drop=True)
            df['Target word/phrase'] = string
            # df_to_csv = df.to_csv(index=False)
        # preview the first five rows of the df
        st.header("Preview the first 5 rows of the concordance dataframe")
        st.dataframe(df.head())
        # download file
        st.header("Download your concordance csv file")
        ste.download_button("Download your concordance csv file", df, "concordance.csv")



