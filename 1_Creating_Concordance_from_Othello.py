#!/usr/bin/env python
# coding: utf-8

"""
# My first app, example page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""

import streamlit as st
from io import StringIO
import urllib.request 
import nltk
nltk.download('punkt')

def set_page_configuration():
    """set page configuration"""
    st.set_page_config(page_title="Creating concordance from Othello",layout="wide")
    st.sidebar.header("Concordance from an example file")

def add_title():
    """add app title"""
    st.markdown("# Creating concordance from Othello")
    st.write("""In this example, we use othello.txt to create a concordance.""")

def add_read_data_section_header():
    """add section one header"""
    st.header("Step 1: Read in a text file --- Othello as an example")
    st.write("In this step, we read in the content of the othello.txt file as a big string.")
    st.subheader("Preview first 20 lines")

def add_tokenize_section_header():
    """add section two header"""
    st.header("Step 2: Tokenization")
    st.write("In this step, we tokenize the string obtained in step 1.")
    st.subheader("A glimpse of the first 15 tokens from the file...")

def add_concordance_section_header():
    """add section three header"""
    st.header("Step 3: Fill in a word/phrase to create a concordance")
    st.write("""In this step, we choose a word/phrase to get its concordance, 
    i.e. its preceding and tailing text.""")

def add_download_section_header():
    """add section four header"""
    st.header("Step 4: Save concordance to a text file and download it")
    st.write("In this step, we save the concordance of the given word/phrase in a text file and download the file.")

def display_concordance_message():
    """display concordance default setting message"""
    message = """<p style="font-family:roboto; color:Green;font-size:20px;">By default, the first 25 matches 
    are printed. Each line is a match and is 80 characters long. </p>"""
    st.markdown(message, unsafe_allow_html=True)

def download_example_file(url): 
    """preview first 20 lines of example file and return file content as a string"""
    try: 
        response = urllib.request.urlopen(url) 
        data = response.read().decode("utf-8")
        for line in data.split('\n')[:20]:
            st.write(line)
    except urllib.request.URLError:
        warning_message = '<p style="font-family:roboto; color:Green;font-size:36px;">No preview output? Please check your internet connection.</p>'
        st.markdown(warning_message, unsafe_allow_html=True)
    return data

def tokenize(data_string):
    """tokenize the file content string and return a nltk Text object"""
    data_string = data_string.lower()
    tokens = nltk.word_tokenize(data_string)
    text_obj = nltk.Text(tokens)
    return text_obj

def get_concordance(input_string, data_string, display=True):
    """define a function that takes an input string and writes out the concordance lines"""
    input_string = input_string.lower()
    input_ls = input_string.split()
    concordance_ls = tokenize(data_string).concordance_list(input_ls)
    if display:      
        for i in concordance_ls:
            st.write(i.line)
    else:
        return concordance_ls

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
        st.download_button(label='Download example concordance file', 
            data = f,
            file_name = fname,
            mime = 'text/plain')

# set page configuration
set_page_configuration()

# add page title
add_title()

# Step 1: read the example file; preview first 20 lines
add_read_data_section_header()
url = "https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/tdmdocs/othello_TXT_FolgerShakespeare.txt" 
content = download_example_file(url)

# Step 2: tokenize the string read from file and preview the first 15 tokens
add_tokenize_section_header()
text = tokenize(content)
st.write(text[:15])

# Step 3: Fill in a word/phrase to create a concordance for the given word
add_concordance_section_header()
input_string = str(st.text_input("""Enter a word/phrase to get concordance 👇
    (input default to 'honest iago', feel free to try a different word/phrase!)""", 
    "honest iago"))

if input_string:
    get_concordance(input_string, content)
    display_concordance_message()
    # Step 4: Save concordance to a file and download it
    add_download_section_header()
    fname = 'othello_concordance.txt'
    write_concordance_to_file(input_string, content, fname)
    download_concordance(fname)

