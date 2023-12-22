#!/usr/bin/env python
# coding: utf-8

"""
# My first app, example page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""
 
import streamlit as st
import nltk
nltk.download('punkt')
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import re
import string   

max_lines = 2**63-1

def set_page_configuration():
    """set page configuration"""
    st.set_page_config(page_title="Concordance analysis of Othello",layout="wide")
    st.sidebar.header("Concordances from Othello")

def add_title():
    """add app title"""
    st.markdown("# A view of Othello through the prism of concordances")

def raise_research_question():
    """give a research question"""
    st.header("Research question")
    st.write("""Here is the synopsis of Othello: Iago is furious about being overlooked for promotion
     and plots to take revenge against his General: Othello, the Moor of Venice. 
     Iago manipulates Othello into believing his wife Desdemona is unfaithful, stirring Othello's 
     jealousy. Othello allows jealousy to consume him, murders Desdemona, and then kills himself (citation).

From the synopsis, we may predict that uses of "jealous" are frequent in Othello, but how frequent 
compared to other works in Shakespeare's Canon, e.g. King Lear?

We can use concordances to answer this question.""")

def jealous_concordance_Othello():
    """add section one header"""
    st.header("Find concordances in Othello")

def jealous_concordance_Lear():
    """add section two header"""
    st.header("Find concordances in King Lear") 

def expand_comparison():
    st.header("Expand the comparison")
    st.write(f"""Let's compare the frequency of '{othello_input}' in four works in Shakespeare's Canon:
        Othello, King Lear, Taming of the Shrew, and Romeo and Juliet.""")

def try_another_word():
    st.header("Try a different word/phrase")
    st.markdown("""Return to [Find concordances in Othello](#find-concordances-in-othello)
     and try a different word/phrase.""")

def read_file(fname): 
    """read in the data of a file"""
    with open("./data/"+fname, 'r') as f:
        content = f.read()
    return content

def tokenize(data_string):
    """tokenize the file content string and return a nltk Text object"""
    data_string = data_string.lower()
    tokens = nltk.word_tokenize(data_string)
    text_obj = nltk.Text(tokens)
    return text_obj

def get_concordance(input_string, data_string, lines=25, width=79, display=True):
    """take an input string and a data string and write out the concordance of the input string 
    in data string or return the concordance"""
    input_string = input_string.lower()
    input_ls = input_string.split()
    concordance = tokenize(data_string).concordance_list(input_ls, width, lines)
    if display:
        for i in concordance:
            st.markdown('<p style="font-family:monospace;text-align:center;white-space:pre">'
                +i.line[0:(width-len(input_string))//2]
                +'<strong>'+ input_string +'</strong>'
                +i.line[-(width-len(input_string)-1)//2:-1]
                +'</p>', unsafe_allow_html=True)
    else:
        return concordance

def display_freq(message, user_input, freq):
    ### diaplay freq message
    message = user_input + ' appears ' + str(freq) + ' times'
    st.markdown('<p class="big-font">'+message+'</p>', unsafe_allow_html=True)

def plot_comparison(othello_input):
    ### bar chart showing freq of 'jealous' in Othello, King Lear, Taming of the Shrew, Romeo and Juliet
    tame_data = read_file('taming_of_the_shrew.txt')
    freq_tame = len(get_concordance(othello_input, tame_data, lines=100, width=79, display=False))
    romeo_data = read_file('romeo_and_juliet.txt')
    freq_romeo = len(get_concordance(othello_input, romeo_data, lines=100, width=79, display=False))
    df = pd.DataFrame({'Canon': ['Othello', 'King Lear', 'Taming of the Shrew', 'Romeo and Juliet'],
        'Freq_of_jealous': [freq_othello, freq_lear, freq_tame, freq_romeo]})
    trace = go.Bar(x=df['Canon'],y=df['Freq_of_jealous'])
    layout = go.Layout(title = f"Frequency of '{othello_input}'' in Shakespeare's 4 works")
    data = [trace]
    fig = go.Figure(data=data,layout=layout)
    st.plotly_chart(fig)

set_page_configuration()
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)
# add page title
add_title()

# raise research question
raise_research_question()

# section one: find concordances of 'jealous' in Othello
jealous_concordance_Othello()
othello_data = read_file('othello.txt')
othello_input = str(st.text_input(""" """, """jealous"""))

if othello_input:
    get_concordance(othello_input, othello_data)
    freq_othello = len(get_concordance(othello_input, othello_data, lines=max_lines, width=79, display=False))
    othello_message = f"\"{othello_input}\" appears {freq_othello} times."
    display_freq(othello_message, othello_input, freq_othello)
    # section two: find concordances of 'jealous' in King Lear
    jealous_concordance_Lear()
    lear_data = read_file('king_lear.txt')
    get_concordance(othello_input, lear_data)
    freq_lear = len(get_concordance(othello_input, lear_data, lines=max_lines, width=79, display=False))
    lear_message = f"\"{othello_input}\" appears {freq_lear} times."
    display_freq(lear_message, othello_input, freq_lear)
    # section three: Expand the comparison
    expand_comparison()
    plot_comparison(othello_input)
    # section four: Try another word
    try_another_word()



