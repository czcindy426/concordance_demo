#!/usr/bin/env python
# coding: utf-8

"""
# My first app, upload user's own files page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""
import streamlit as st
from io import StringIO
import nltk
import pandas as pd
import streamlit_ext as ste

def set_page_config():
    """set page configuration"""
    st.set_page_config(page_title="Creating concordance from multiple files",
    layout="wide")

def add_title():
    """add page title"""
    st.markdown("# Creating concordance from multiple files")
    st.sidebar.header("Concordance from multiple files")

def add_upload_section_header():
    """add upload section header"""
    st.header("Upload you files")

def download_file_section_header():
    """Download generated concordance file section header"""
    st.header("Download your concordance file")

def display_upload_complete_message():
    """message to confirm upload complete"""
    reminder = """<p style="font-family:roboto; color:Green;font-size:20px;">
    After uploading all the files, click on the button below.</p>"""
    st.markdown(reminder, unsafe_allow_html=True)  

def display_upload_success_message():
    """display upload success message"""
    success_message = '<p style="font-family:roboto; color:Green;font-size:20px;">File uploaded successfully.</p>'
    st.markdown(success_message, unsafe_allow_html=True)  

def read_upload_file(uploaded_file):
    """read the uploaded file as a string"""
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    content = stringio.read()
    return content

# section: Upload a text file of your own to create a concordance

def tokenize(data):
    """tokenize a string and produce a nltk text object"""
    data = data.lower()
    tokens = nltk.word_tokenize(data)
    text = nltk.Text(tokens)
    return text

def get_user_input():
    """Get user input of target word/phrase, num of lines and num of chars"""
    up_string = str(st.text_input("""Give a word/phrase to get concordance 👇"""))
    num_lines = str(st.text_input("""Enter an integer to specify how many concordance lines you want to show 👇"""))
    num_char = str(st.text_input("""Enter an integer to specify how many characters you want to show on each line 👇"""))
    return up_string.lower(), num_lines, num_char

def get_concordance(input_string, data_string, lines=25, width=79, write=True):
    """take an input string and a data string and write out the concordance of the input string 
    in data string or return the concordance"""    
    input_string = input_string.lower()
    input_ls = input_string.split()
    text = tokenize(data_string)
    concordance = text.concordance_list(input_ls, width, lines)
    if write:
        for i in concordance:
            st.write(i.line)
    else:
        return concordance

def get_name_content(uploaded_files):
    """return a list of file names and content from uploaded files"""
    f_names = [f.name for f in uploaded_files]
    content = [StringIO(f.getvalue().decode("utf-8")).read() for f in uploaded_files]
    return f_names, content

def create_df(uploaded_files, string, num_lines, num_char):
    """create a df storing concordance from uploaded files"""
    f_name_ls, content_ls = get_name_content(uploaded_files)
    concordance_all = [[i.line for i in get_concordance(string, content, lines=int(num_lines), width=int(num_char), write=False)] for content in content_ls]
    df = pd.DataFrame({'File': f_name_ls, 'Concordance':concordance_all})
    df = df.explode('Concordance').reset_index(drop=True)
    df['Target word/phrase'] = up_string
    return df

def preview_df(df):
    st.header("Preview the first 5 rows of the concordance dataframe")
    st.dataframe(df.head())

# set page configuration
set_page_config()

# add page title
add_title()

#Use the value of a session state variable step to track the dependency between widgets
if st.session_state.get('step') is None:
    st.session_state['step'] = 0

# First step: upload files
uploaded_files = st.file_uploader("Upload .txt files", accept_multiple_files=True, key='multiple files')
# text to remind the user to click the upload complete button
display_upload_complete_message()
submit = st.button('Upload completed', key='upload complete')
# if the button is hit, do the following
if submit: 
    # upload success message
    display_upload_success_message()
    st.session_state['step'] = 1 

# Second step: Enter target word/phrase, num of lines and num of characters on each line

if st.session_state['step'] == 1:
    # User enter a word/phrase and specify number of lines and characters
    up_string, num_lines, num_char = get_user_input()
    if up_string and num_lines and num_char:
    ### Create a dataframe to store the concordance from the files for users to download
        df = create_df(uploaded_files, up_string, num_lines, num_char)
        # preview the first five rows of the df
        preview_df(df)
        # download file
        download_file_section_header()
        ste.download_button("Download your concordance csv file", df, "concordance.csv")

