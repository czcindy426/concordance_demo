#!/usr/bin/env python
# coding: utf-8

"""
# My first app, upload self's file page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""
import streamlit as st
from io import StringIO
import urllib.request 
import nltk

def set_page_configuration():
    """set page configuration"""
    st.set_page_config(page_title="Creating concordance from your own file",layout="wide")
    st.sidebar.header("Concordance from your own file")

def add_title():
    """add app title"""
    st.markdown("# Creating concordance from your own file")

def upload_file_section_header():
    """Upload a text file of your own to create a concordance section header"""
    st.header("Upload a text file of your own to create a concordance")

def download_file_section_header():
    """Download generated concordance file section header"""
    st.header("Download your concordance file")

def display_upload_success_message():
    """display upload success message"""
    success_message = '<p style="font-family:roboto; color:Green;font-size:20px;">File uploaded successfully.</p>'
    st.markdown(success_message, unsafe_allow_html=True)  

def read_upload_file(uploaded_file):
    """read the uploaded file as a string"""
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    content = stringio.read()
    return content

def tokenize(data):
    """tokenize the input string and return a nltk Text object"""
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

def get_concordance(input_string, data_string, lines=25, width=79, display=True):
    """take an input string and a data string and write out the concordance of the input string 
    in data string or return the concordance"""
    input_string = input_string.lower()
    input_ls = input_string.split()
    concordance = tokenize(data_string).concordance_list(input_ls, width, lines)
    if display:
        for i in concordance:
            st.write(i.line)
    else:
        return concordance

def write_concordance_to_file(input_string, data, fname):
    """write concordance to file"""
    concordance_obj = get_concordance(input_string, data, display=False)
    with open (fname, 'w') as f:
        for ele in concordance_obj:
            f.write(ele.line)
            f.write('\n')

def download_concordance(fname):
    """download cncordance file"""
    with open (fname, 'r') as f:
        st.download_button(label='Download your concordance file', 
            data = f,
            file_name = fname,
            mime = 'text/plain')

# set page configuration
set_page_configuration()

# add page title
add_title()

# Step 1: Upload a file
upload_file_section_header()
# upload file
uploaded_file = st.file_uploader("Choose a .txt file", type="txt", key='single file')
if uploaded_file:
    # upload success message
    display_upload_success_message()
    # read file as string:
    content = read_upload_file(uploaded_file)
    # enter a word/phrase
    up_string, num_lines, num_char = get_user_input()
    if up_string and num_lines and num_char:
        get_concordance(up_string, content, lines=int(num_lines), width=int(num_char))
        download_file_section_header()
        # create a name for downloaded concordance file
        down_fname = uploaded_file.name.removesuffix('.txt') + '_concordance.txt'
        write_concordance_to_file(up_string, content, down_fname)
        download_concordance(down_fname)