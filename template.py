#!/usr/bin/env python
# coding: utf-8

"""
# My first app, home page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""
import streamlit as st
from io import StringIO
import nltk
import numpy as np
import pandas as pd
import streamlit_ext as ste
import plotly.express as px
import plotly.graph_objs as go
import re
import string 
import constellate
import urllib.request 

max_lines = 2**63-1

def set_page_configuration():
    """set page configuration"""
    st.set_page_config(page_title="Concordance",layout="centered")
    # st.sidebar.header("Intro to concordance")

def add_title():
    """add app title"""
    st.markdown("# Introduction to Concordance")

# define a function to load the video example
def download_video_to_play(url): 
    """preview first 20 lines of example file and return file content as a string"""
    try: 
        response = urllib.request.urlopen(url) 
        video_bytes = response.read()
        st.video(video_bytes)
    except urllib.request.URLError:
        warning_message = '<p style="font-family:roboto; color:Green;font-size:36px;">No video displayed? Please check your internet connection.</p>'
        st.markdown(warning_message, unsafe_allow_html=True)

# define a function to load the image of concordance line
def download_image(url): 
    """preview first 20 lines of example file and return file content as a string"""
    try: 
        response = urllib.request.urlopen(url) 
        image = response.read()
        st.image(image, caption="Figure 1:  Concordance lines of 'effect' in the BNC-Baby corpus. (Wynne, 2008)")
    except urllib.request.URLError:
        warning_message = '<p style="font-family:roboto; color:Green;font-size:36px;">No image displayed? Please check your internet connection.</p>'
        st.markdown(warning_message, unsafe_allow_html=True)

def raise_humanities_question():
    """give a research question"""
    st.header("A view of Othello through the prism of concordances")
    st.write("""Here is the synopsis of Othello: Iago is furious about being overlooked for promotion
     and plots to take revenge against his General: Othello, the Moor of Venice. 
     Iago manipulates Othello into believing his wife Desdemona is unfaithful, stirring Othello's 
     jealousy. Othello allows jealousy to consume him, murders Desdemona, and then kills himself (citation).

From the synopsis, we may predict that uses of "jealous" are frequent in Othello, but how frequent 
compared to other works in Shakespeare's Canon, e.g. King Lear?

We can use concordances to answer this question.""")

def expand_comparison():
    st.header("Expand the comparison")
    st.write(f"""Let's compare the frequency of '{othello_input}' in four works in Shakespeare's Canon:
        Othello, King Lear, Taming of the Shrew, and Romeo and Juliet.""")

def try_another_word():
    st.header("Try a different word/phrase")
    st.markdown("""Return to [Find concordances in Othello](#find-concordances-in-othello)
     and try a different word/phrase.""")

def link_to_notebook(url):
    st.header("Run concordances in Constellate lab")
    st.write("Try our concordance lesson with more flexibility for actual research!")
    with st.expander('Preview the concordance notebook lesson'):
        st.markdown("""# Concordance and Collocation

**Description:** This notebook describes how to create a concordance and collocation starting from text files and from a Constellate dataset file.

**Use Case:** For Learners (Detailed explanation, not ideal for researchers)

**Difficulty:** Intermediate

**Completion Time:** 45 minutes

**Knowledge Required:** 
* Python Basics Series ([Start Python Basics I](./python-basics-1.ipynb))

**Knowledge Recommended:** None

**Data Format:** Text, Constellate JSON File

**Libraries Used:** NLTK

**Research Pipeline:** None""")
    st.link_button("Run the concordance notebook in lab", url)

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

### Section one: Intro
add_title()
st.write("## What is a concordance?")
st.markdown("""The concordance has a long history in humanities study.
   A concordance is a list of all the contexts in which a certain word/phrase occurs in a text (Lindquist and Levin 2018, 5). 
   For example, if you go to [OpenSourceShakespeare](https://www.opensourceshakespeare.org) and enter a keyword to search,
    you will find concordances compiled for people to study how the word is used in Shakespeare's works.""")
st.write("Play the following video to get a sense of concordances.")
download_video_to_play("https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/OpenSourceShakespeareForConcordanceApp.mp4")
st.caption('<div style="text-align: center">Search for concordances of \'honesty\' on OpenSourceShakespeare</div>', unsafe_allow_html=True)

st.markdown("""<br>In natural language processing, concordances are often presented in the form of keyword-in-context (KWIC) 
   with one line of context and the keyword centered in the line.""",unsafe_allow_html=True)
download_image("https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/tdmdocs/ConcordanceImageForConcordanceApp.jpg")

st.write("## Why are concordances useful?")
st.markdown("""Concordance data are useful in many ways. First of all, getting information using concordances is much faster than 
   reading closely through the complete texts. Second, with the knowledge of how a certain word or phrase is used, literary scholars can go on to 
   do comparative analysis. For example, a reseacher in comparative literature may use concordances to find out how Shakespeare used 
   astronomical terms in his works and then compare how the uses differ in his comedies and tragedies. Last, concordances provide important 
   information such as word frequency and frequency of cooccurences of certain words. Researchers can compare frequencies to describe differences 
   between geographical locations, spoken and written language, text from different historical periods, et cetera (Lindquist and Levin 2018, 8).""")

### Section two: Choose an example from a certain discipline
st.write('## Select an example to explore')
tab1, tab2, tab3 = st.tabs(["Humanities", "Social sciences", "Natural sciences"])
with tab1:
    raise_humanities_question()
    st.header("Find concordances in Othello")
    othello_data = read_file('othello.txt')
    othello_input = str(st.text_input(""" """, """jealous"""))
    if othello_input:
        get_concordance(othello_input, othello_data)
        freq_othello = len(get_concordance(othello_input, othello_data, lines=max_lines, width=79, display=False))
        othello_message = f"\"{othello_input}\" appears {freq_othello} times."
        display_freq(othello_message, othello_input, freq_othello)
        st.header("Find concordances in King Lear") 
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
with tab2:
    st.header("Blah blah blah")
    st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Erat pellentesque adipiscing commodo elit at. Sed elementum tempus egestas sed sed risus. Sem nulla pharetra diam sit amet. In pellentesque massa placerat duis. Aliquam vestibulum morbi blandit cursus risus at ultrices mi tempus. Nam aliquam sem et tortor. Cras fermentum odio eu feugiat. Ultrices mi tempus imperdiet nulla malesuada. Posuere urna nec tincidunt praesent semper feugiat nibh sed pulvinar. Cum sociis natoque penatibus et. Mi sit amet mauris commodo quis imperdiet. Sed turpis tincidunt id aliquet risus feugiat in ante metus. A erat nam at lectus urna. In nulla posuere sollicitudin aliquam ultrices.

Pellentesque habitant morbi tristique senectus et. Turpis egestas integer eget aliquet nibh praesent tristique magna. Rhoncus dolor purus non enim praesent elementum. Consectetur libero id faucibus nisl tincidunt eget nullam non nisi. Ultrices dui sapien eget mi proin sed libero enim. Accumsan lacus vel facilisis volutpat est velit egestas dui id. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit sed. Quam viverra orci sagittis eu volutpat odio facilisis. Et sollicitudin ac orci phasellus. Lectus quam id leo in vitae turpis massa sed. Potenti nullam ac tortor vitae purus faucibus ornare. At lectus urna duis convallis convallis tellus id. Elementum nibh tellus molestie nunc non blandit massa enim nec. At in tellus integer feugiat scelerisque varius morbi enim.

Iaculis at erat pellentesque adipiscing. Diam ut venenatis tellus in metus vulputate eu scelerisque. Non blandit massa enim nec. Venenatis cras sed felis eget velit aliquet sagittis id. Ultrices sagittis orci a scelerisque. Vitae auctor eu augue ut lectus. Odio morbi quis commodo odio aenean. Facilisis gravida neque convallis a cras semper. Sagittis id consectetur purus ut faucibus pulvinar elementum integer enim. Quam vulputate dignissim suspendisse in est ante in nibh mauris.

Lacinia at quis risus sed. Velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Adipiscing elit pellentesque habitant morbi. Ut diam quam nulla porttitor. Diam maecenas ultricies mi eget mauris. Sit amet tellus cras adipiscing enim eu turpis egestas pretium. Viverra nam libero justo laoreet sit amet cursus sit amet. Quis hendrerit dolor magna eget est. Nisl purus in mollis nunc sed id. Eget velit aliquet sagittis id consectetur purus ut faucibus. A arcu cursus vitae congue mauris rhoncus aenean vel elit. Interdum varius sit amet mattis vulputate. Tincidunt ornare massa eget egestas purus viverra. Ut tortor pretium viverra suspendisse potenti. Ac turpis egestas integer eget aliquet nibh praesent. Ultrices in iaculis nunc sed augue.

Sed velit dignissim sodales ut eu sem. Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus et. Dolor morbi non arcu risus quis varius quam quisque. Non odio euismod lacinia at quis risus sed. Ultrices dui sapien eget mi proin. Semper viverra nam libero justo laoreet sit amet cursus. Urna neque viverra justo nec ultrices dui sapien. Purus sit amet luctus venenatis lectus magna fringilla urna porttitor. Enim neque volutpat ac tincidunt vitae semper. Interdum varius sit amet mattis. Id volutpat lacus laoreet non curabitur. Eu tincidunt tortor aliquam nulla facilisi cras. Lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi tincidunt. Urna id volutpat lacus laoreet non curabitur.""")
with tab3:
    st.header("Blah blah blah")
    st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Erat pellentesque adipiscing commodo elit at. Sed elementum tempus egestas sed sed risus. Sem nulla pharetra diam sit amet. In pellentesque massa placerat duis. Aliquam vestibulum morbi blandit cursus risus at ultrices mi tempus. Nam aliquam sem et tortor. Cras fermentum odio eu feugiat. Ultrices mi tempus imperdiet nulla malesuada. Posuere urna nec tincidunt praesent semper feugiat nibh sed pulvinar. Cum sociis natoque penatibus et. Mi sit amet mauris commodo quis imperdiet. Sed turpis tincidunt id aliquet risus feugiat in ante metus. A erat nam at lectus urna. In nulla posuere sollicitudin aliquam ultrices.

Pellentesque habitant morbi tristique senectus et. Turpis egestas integer eget aliquet nibh praesent tristique magna. Rhoncus dolor purus non enim praesent elementum. Consectetur libero id faucibus nisl tincidunt eget nullam non nisi. Ultrices dui sapien eget mi proin sed libero enim. Accumsan lacus vel facilisis volutpat est velit egestas dui id. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit sed. Quam viverra orci sagittis eu volutpat odio facilisis. Et sollicitudin ac orci phasellus. Lectus quam id leo in vitae turpis massa sed. Potenti nullam ac tortor vitae purus faucibus ornare. At lectus urna duis convallis convallis tellus id. Elementum nibh tellus molestie nunc non blandit massa enim nec. At in tellus integer feugiat scelerisque varius morbi enim.

Iaculis at erat pellentesque adipiscing. Diam ut venenatis tellus in metus vulputate eu scelerisque. Non blandit massa enim nec. Venenatis cras sed felis eget velit aliquet sagittis id. Ultrices sagittis orci a scelerisque. Vitae auctor eu augue ut lectus. Odio morbi quis commodo odio aenean. Facilisis gravida neque convallis a cras semper. Sagittis id consectetur purus ut faucibus pulvinar elementum integer enim. Quam vulputate dignissim suspendisse in est ante in nibh mauris.

Lacinia at quis risus sed. Velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Adipiscing elit pellentesque habitant morbi. Ut diam quam nulla porttitor. Diam maecenas ultricies mi eget mauris. Sit amet tellus cras adipiscing enim eu turpis egestas pretium. Viverra nam libero justo laoreet sit amet cursus sit amet. Quis hendrerit dolor magna eget est. Nisl purus in mollis nunc sed id. Eget velit aliquet sagittis id consectetur purus ut faucibus. A arcu cursus vitae congue mauris rhoncus aenean vel elit. Interdum varius sit amet mattis vulputate. Tincidunt ornare massa eget egestas purus viverra. Ut tortor pretium viverra suspendisse potenti. Ac turpis egestas integer eget aliquet nibh praesent. Ultrices in iaculis nunc sed augue.

Sed velit dignissim sodales ut eu sem. Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus et. Dolor morbi non arcu risus quis varius quam quisque. Non odio euismod lacinia at quis risus sed. Ultrices dui sapien eget mi proin. Semper viverra nam libero justo laoreet sit amet cursus. Urna neque viverra justo nec ultrices dui sapien. Purus sit amet luctus venenatis lectus magna fringilla urna porttitor. Enim neque volutpat ac tincidunt vitae semper. Interdum varius sit amet mattis. Id volutpat lacus laoreet non curabitur. Eu tincidunt tortor aliquam nulla facilisi cras. Lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi tincidunt. Urna id volutpat lacus laoreet non curabitur.""")
# # Use the value of a session state variable 'step' to track the sequencing relation between widgets
# if st.session_state.get('step') is None:
#     st.session_state['step'] = 0

# datapick_cols = st.columns(3)
# with datapick_cols[0]:
#     with st.container():
        
#         st.info('Humanities')
#         st.write('A view of Othello through the prism of concordance')
#         humanities = st.button('Select', key='humanities')
#         if humanities:
#            st.session_state['step'] = 1
# with datapick_cols[1]:
#     with st.container():
#         st.info('Social sciences')
#         social = st.button('Select', key='social')
#         if social:
#             st.session_state['step'] = 2
# with datapick_cols[2]:
#     with st.container():
#         st.info('Natural sciences')
#         social = st.button('Select', key='natural')
#         if social:
#             st.session_state['step'] = 3

# if st.session_state['step'] == 1:
#     # raise research question
#     raise_humanities_question()
    # st.header("Find concordances in Othello")
    # othello_data = read_file('othello.txt')
    # othello_input = str(st.text_input(""" """, """jealous"""))
    # if othello_input:
    #     get_concordance(othello_input, othello_data)
    #     freq_othello = len(get_concordance(othello_input, othello_data, lines=max_lines, width=79, display=False))
    #     othello_message = f"\"{othello_input}\" appears {freq_othello} times."
    #     display_freq(othello_message, othello_input, freq_othello)
    #     st.header("Find concordances in King Lear") 
    #     lear_data = read_file('king_lear.txt')
    #     get_concordance(othello_input, lear_data)
    #     freq_lear = len(get_concordance(othello_input, lear_data, lines=max_lines, width=79, display=False))
    #     lear_message = f"\"{othello_input}\" appears {freq_lear} times."
    #     display_freq(lear_message, othello_input, freq_lear)
    #     # section three: Expand the comparison
    #     expand_comparison()
    #     plot_comparison(othello_input)
    #     # section four: Try another word
    #     try_another_word()
# elif st.session_state['step'] == 2:  
#     pass
# elif st.session_state['step'] == 3:
#     pass

# # section five: Go to the associated notebook
link_to_notebook("""https://constellate.org/lab?repo=https%3A%2F%2Fgithub.com%2Fithaka%2Fconstellate-notebooks&filepath=concordance.ipynb""")
### Section six: References
st.write("## References")
st.markdown("""Lindquist, H., & Levin, M. (2018). *Corpus Linguistics and the Description of English*. Edinburgh: Edinburgh University Press.

   Wynne, Martin (2008), Searching and concordancing, in Anke Lüdeling and Merja Kytö (eds), *Corpus Linguistics: An International Handbook*. Vol. I, Berlin:
de Gruyter, 706–737.""")
 




