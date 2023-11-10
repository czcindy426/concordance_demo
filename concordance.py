#!/usr/bin/env python
# coding: utf-8

"""
# My first app
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""


import streamlit as st
from io import StringIO
import urllib.request 
import sys
import re

# Set page config
st.set_page_config(layout='wide')
st.markdown("""<style>
    .big-font {font-size:300px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.title('Concordance')
st.subheader("creating a concordance from text files")
st.write("""The concordance has a long history in humanities study.
    A concordance gives the context of a given word or phrase in a body of texts. 
    For example, a literary scholar might ask: how often and in what context does Shakespeare use the phrase 
    "honest Iago" in Othello? 
    A historian might examine a particular politician's speeches, looking for examples of a particular dog whistle.""")

# section: upload a file to read
st.header("Step 1: Read in a text file --- Othello as an example")
st.write("In this step, we read in the content of the othello.txt file as a big string.")
st.subheader("Preview first 20 lines")
# Read a text file 
url = "https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/tdmdocs/othello_TXT_FolgerShakespeare.txt" 
try: 
    response = urllib.request.urlopen(url) 
    data = response.read().decode("utf-8")
    for line in data.split('\n')[:20]:
        st.write(line)
except urllib.request.URLError:
    warning_message = '<p style="font-family:roboto; color:Green;font-size:36px;">No preview output? Please check your internet connection.</p>'
    st.markdown(warning_message, unsafe_allow_html=True)

# section: tokenize the string read from file
st.header("Step 2: Tokenization")
st.write("In this step, we tokenize the string obtained in step 1.")
# Tokenize the string and create a Text object out of it
import nltk
nltk.download('punkt')
data = data.lower()
tokens = nltk.word_tokenize(data)
text = nltk.Text(tokens)
# Print out the first 15 tokens as an example
st.subheader("A glimpse of the first 15 tokens from the file...")
st.write(text[:15])

# section: Fill in a word/phrase to create a concordance for the given word
st.header("Step 3: Fill in a word/phrase to create a concordance...")
st.write("In this step, we choose a word/phrase to get its concordance, i.e. its preceding and tailing text.")
input_string = str(st.text_input("Enter a word/phrase to get concordance 👇(input default to 'honest iago', feel free to try a different word/phrase!)", "honest iago"))
input_string = input_string.lower()

if input_string:
    input_ls = input_string.split()
    concordance_ls = text.concordance_list(input_ls)
    for i in concordance_ls:
        st.write(i.line)
    # section: Save concordance to a file and download it
    st.header("Step 4: Save concordance to a text file and download it")
    st.write("In this step, we save the concordance of the given word/phrase in a text file and download the file.")
    with open ('othello_concordance.txt', 'w') as f:
        for i in concordance_ls:
            f.write(i.line)
            f.write('\n')
    with open ('othello_concordance.txt', 'r') as f:
        st.download_button(label='Download example concordance file', 
            data = f,
            file_name = 'othello_concordance.txt',
            mime = 'text/plain')



# section: Upload a text file of your own to create a concordance
st.header("Your turn: Upload a text file of your own to create a concordance")
# upload file
uploaded_file = st.file_uploader("Choose a .txt file")
if uploaded_file:
    # upload success message
    success_message = '<p style="font-family:roboto; color:Green;font-size:20px;">File uploaded successfully.</p>'
    st.markdown(success_message, unsafe_allow_html=True)    # To read file as string:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    content = stringio.read()
    content = content.lower()
    #tokenize the file
    up_tks = nltk.word_tokenize(content)
    up_text = nltk.Text(up_tks)
    # enter a word/phrase
    up_string = str(st.text_input("Enter a word/phrase to get concordance 👇"))
    up_string = up_string.lower()
    if up_string:
        up_ls = up_string.split()
        concordance_up = up_text.concordance_list(up_ls, lines=len(up_tks))
        with open ('my_concordance.txt', 'w') as f:
            for i in concordance_up:
                f.write(i.line)
                f.write('\n')
        # write the concordance into a file for download
        with open ('my_concordance.txt', 'r') as f:
            st.download_button(label='Download your concordance file', 
                data = f,
                file_name = 'my_concordance.txt',
                mime = 'text/plain')


