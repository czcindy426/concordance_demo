#!/usr/bin/env python
# coding: utf-8

"""
# My first app, home page 
Here's our first attempt at using streamlit to make a pre-code tutorial on concordance
"""
import streamlit as st
import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
nltk.download('punkt')

max_lines = 2**63-1
def read_file(fname): 
    """read in the data of a file"""
    with open("./data/"+fname, 'r') as f:
        content = f.read()
    return content

othello_data = read_file('othello.txt')
lear_data = read_file('king_lear.txt')
tame_data = read_file('taming_of_the_shrew.txt')
romeo_data = read_file('romeo_and_juliet.txt')

def set_page_configuration():
    """set page configuration"""
    st.set_page_config(page_title="Concordance",layout="wide")

# define a function to load images
def display_image(image, caption=None): 
    st.image(image, caption=caption)

def raise_humanities_question():
    """give a research question"""
    st.subheader("A view of Othello through the prism of concordances")
    st.write("""Here is the synopsis of Othello: Iago is furious about being overlooked for promotion
     and plots to take revenge against his General: Othello, the Moor of Venice. 
     Iago manipulates Othello into believing his wife Desdemona is unfaithful, stirring Othello's 
     jealousy. Othello allows jealousy to consume him, murders Desdemona, and then kills himself (citation).

From the synopsis, we may predict that uses of "jealous" are frequent in Othello, but how frequent 
compared to other works in Shakespeare's Canon, e.g. King Lear?

We can use concordances to answer this question.""")

def expand_comparison(othello_input):
    st.subheader("Expand the comparison")
    st.write(f"""Let's compare the frequency of '{othello_input}' in four works in Shakespeare's Canon:
        Othello, King Lear, Taming of the Shrew, and Romeo and Juliet.""")

def try_another_word():
    st.write("""### Try a different word/phrase""")
    st.write("Enter a keyword of your interest to get its concordances in Othello and King Lear")
    othello_data = read_file('othello.txt')
    othello_input = str(st.text_input(""" """))
    display_num_lines_message()
    if othello_input:
        freq_othello = len(get_concordance(othello_input, othello_data, lines=max_lines, width=79, display=False))
        display_freq(othello_input, freq_othello, 'Othello')
        get_concordance(othello_input, othello_data)
        freq_lear = len(get_concordance(othello_input, lear_data, lines=max_lines, width=79, display=False))
        display_freq(othello_input, freq_lear, 'King Lear')
        get_concordance(othello_input, lear_data)
        # section three: Expand the comparison
        expand_comparison(othello_input)
        plot_comparison(othello_input)

def link_to_notebook(url):
    st.write("Interested in learning more about concordance to apply to your research? Try out code tutorial on concordance.")
    st.link_button("View code tutorial $\longrightarrow$", url)


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

def display_freq(word, freq, text):
    ### display freq message
    st.write('#### '+ f"'{word}'" + ' appears ' + str(freq) + ' times in ' + text)

def display_num_lines_message():
    st.markdown("""At most 25 concordances lines are displayed. If you would like to learn how to save your concordance data
     to a text file, [run our concordance lesson in the Constellate lab](#run-concordances-in-constellate-lab)!""")

def plot_comparison(othello_input='jealous'):
    ### bar chart showing freq of 'jealous' in Othello, King Lear, Taming of the Shrew, Romeo and Juliet
    freq_othello = len(get_concordance(othello_input, othello_data, lines=max_lines, width=79, display=False))
    freq_lear = len(get_concordance(othello_input, lear_data, lines=max_lines, width=79, display=False))
    freq_tame = len(get_concordance(othello_input, tame_data, lines=max_lines, width=79, display=False))
    freq_romeo = len(get_concordance(othello_input, romeo_data, lines=max_lines, width=79, display=False))
    df = pd.DataFrame({'Canon': ['Othello', 'King Lear', 'Taming of the Shrew', 'Romeo and Juliet'],
        'Freq': [freq_othello, freq_lear, freq_tame, freq_romeo]})
    trace = go.Bar(x=df['Canon'],y=df['Freq'])
    layout = go.Layout(title = f"Frequency of '{othello_input}'' in Shakespeare's 4 works")
    data = [trace]
    fig = go.Figure(data=data,layout=layout)
    st.plotly_chart(fig)

set_page_configuration()

### Section one: Intro
st.write("## What is a concordance?")
st.markdown("""The concordance has a long history in humanities study.
   A concordance is a list of all the contexts in which a certain word/phrase occurs in a text (Lindquist and Levin 2018, 5). 
   For example, if you go to the Constellate builder and [search within the documents](https://constellate.org/builder?unigrams=patients,%20students#:~:text=the%20%22Keyphrases%22%20menu.-,Document%20categories%20over%20time,-Learn%20more) of a dataset that you are building,
    you will find concordances compiled for you to study how the keyword you have entered is used in the documents.""")
display_image("data/monticello.png", 'Figure 1: Search for concordances of \'monticello\' in the journal Papers of Thomas Jefferson')

st.markdown("""<br>In natural language processing, concordances are often presented in the form of keyword-in-context (KWIC) 
   with one line of context and the keyword centered in the line.""",unsafe_allow_html=True)
display_image("data/effect.png", 'Figure 2: Concordance lines of \'effect\' in the BNC-Baby corpus. (Wynne, 2008)')

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
    st.subheader("Find concordances of 'jealous' in Othello and King Lear")
    display_image('data/jealous_input.png')    
    display_num_lines_message()
    othello_data = read_file('othello.txt')
    freq_othello = len(get_concordance("jealous", othello_data, lines=max_lines, width=79, display=False))
    display_freq("jealous", freq_othello, 'Othello')
    get_concordance("jealous", othello_data)
    lear_data = read_file('king_lear.txt')
    freq_lear = len(get_concordance("jealous", lear_data, lines=max_lines, width=79, display=False))
    display_freq("jealous", freq_lear, 'King Lear')
    get_concordance("jealous", lear_data)
    # section three: Expand the comparison
    expand_comparison('jealous')
    plot_comparison("jealous")
    # section four: Try another word
    try_another_word()
with tab2:
    st.subheader("Lorem ipsum dolor")
    st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Erat pellentesque adipiscing commodo elit at. Sed elementum tempus egestas sed sed risus. Sem nulla pharetra diam sit amet. In pellentesque massa placerat duis. Aliquam vestibulum morbi blandit cursus risus at ultrices mi tempus. Nam aliquam sem et tortor. Cras fermentum odio eu feugiat. Ultrices mi tempus imperdiet nulla malesuada. Posuere urna nec tincidunt praesent semper feugiat nibh sed pulvinar. Cum sociis natoque penatibus et. Mi sit amet mauris commodo quis imperdiet. Sed turpis tincidunt id aliquet risus feugiat in ante metus. A erat nam at lectus urna. In nulla posuere sollicitudin aliquam ultrices.

Pellentesque habitant morbi tristique senectus et. Turpis egestas integer eget aliquet nibh praesent tristique magna. Rhoncus dolor purus non enim praesent elementum. Consectetur libero id faucibus nisl tincidunt eget nullam non nisi. Ultrices dui sapien eget mi proin sed libero enim. Accumsan lacus vel facilisis volutpat est velit egestas dui id. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit sed. Quam viverra orci sagittis eu volutpat odio facilisis. Et sollicitudin ac orci phasellus. Lectus quam id leo in vitae turpis massa sed. Potenti nullam ac tortor vitae purus faucibus ornare. At lectus urna duis convallis convallis tellus id. Elementum nibh tellus molestie nunc non blandit massa enim nec. At in tellus integer feugiat scelerisque varius morbi enim.

Iaculis at erat pellentesque adipiscing. Diam ut venenatis tellus in metus vulputate eu scelerisque. Non blandit massa enim nec. Venenatis cras sed felis eget velit aliquet sagittis id. Ultrices sagittis orci a scelerisque. Vitae auctor eu augue ut lectus. Odio morbi quis commodo odio aenean. Facilisis gravida neque convallis a cras semper. Sagittis id consectetur purus ut faucibus pulvinar elementum integer enim. Quam vulputate dignissim suspendisse in est ante in nibh mauris.

Lacinia at quis risus sed. Velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Adipiscing elit pellentesque habitant morbi. Ut diam quam nulla porttitor. Diam maecenas ultricies mi eget mauris. Sit amet tellus cras adipiscing enim eu turpis egestas pretium. Viverra nam libero justo laoreet sit amet cursus sit amet. Quis hendrerit dolor magna eget est. Nisl purus in mollis nunc sed id. Eget velit aliquet sagittis id consectetur purus ut faucibus. A arcu cursus vitae congue mauris rhoncus aenean vel elit. Interdum varius sit amet mattis vulputate. Tincidunt ornare massa eget egestas purus viverra. Ut tortor pretium viverra suspendisse potenti. Ac turpis egestas integer eget aliquet nibh praesent. Ultrices in iaculis nunc sed augue.

Sed velit dignissim sodales ut eu sem. Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus et. Dolor morbi non arcu risus quis varius quam quisque. Non odio euismod lacinia at quis risus sed. Ultrices dui sapien eget mi proin. Semper viverra nam libero justo laoreet sit amet cursus. Urna neque viverra justo nec ultrices dui sapien. Purus sit amet luctus venenatis lectus magna fringilla urna porttitor. Enim neque volutpat ac tincidunt vitae semper. Interdum varius sit amet mattis. Id volutpat lacus laoreet non curabitur. Eu tincidunt tortor aliquam nulla facilisi cras. Lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi tincidunt. Urna id volutpat lacus laoreet non curabitur.""")
with tab3:
    st.subheader("Lorem ipsum dolor")
    st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Erat pellentesque adipiscing commodo elit at. Sed elementum tempus egestas sed sed risus. Sem nulla pharetra diam sit amet. In pellentesque massa placerat duis. Aliquam vestibulum morbi blandit cursus risus at ultrices mi tempus. Nam aliquam sem et tortor. Cras fermentum odio eu feugiat. Ultrices mi tempus imperdiet nulla malesuada. Posuere urna nec tincidunt praesent semper feugiat nibh sed pulvinar. Cum sociis natoque penatibus et. Mi sit amet mauris commodo quis imperdiet. Sed turpis tincidunt id aliquet risus feugiat in ante metus. A erat nam at lectus urna. In nulla posuere sollicitudin aliquam ultrices.

Pellentesque habitant morbi tristique senectus et. Turpis egestas integer eget aliquet nibh praesent tristique magna. Rhoncus dolor purus non enim praesent elementum. Consectetur libero id faucibus nisl tincidunt eget nullam non nisi. Ultrices dui sapien eget mi proin sed libero enim. Accumsan lacus vel facilisis volutpat est velit egestas dui id. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit sed. Quam viverra orci sagittis eu volutpat odio facilisis. Et sollicitudin ac orci phasellus. Lectus quam id leo in vitae turpis massa sed. Potenti nullam ac tortor vitae purus faucibus ornare. At lectus urna duis convallis convallis tellus id. Elementum nibh tellus molestie nunc non blandit massa enim nec. At in tellus integer feugiat scelerisque varius morbi enim.

Iaculis at erat pellentesque adipiscing. Diam ut venenatis tellus in metus vulputate eu scelerisque. Non blandit massa enim nec. Venenatis cras sed felis eget velit aliquet sagittis id. Ultrices sagittis orci a scelerisque. Vitae auctor eu augue ut lectus. Odio morbi quis commodo odio aenean. Facilisis gravida neque convallis a cras semper. Sagittis id consectetur purus ut faucibus pulvinar elementum integer enim. Quam vulputate dignissim suspendisse in est ante in nibh mauris.

Lacinia at quis risus sed. Velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Adipiscing elit pellentesque habitant morbi. Ut diam quam nulla porttitor. Diam maecenas ultricies mi eget mauris. Sit amet tellus cras adipiscing enim eu turpis egestas pretium. Viverra nam libero justo laoreet sit amet cursus sit amet. Quis hendrerit dolor magna eget est. Nisl purus in mollis nunc sed id. Eget velit aliquet sagittis id consectetur purus ut faucibus. A arcu cursus vitae congue mauris rhoncus aenean vel elit. Interdum varius sit amet mattis vulputate. Tincidunt ornare massa eget egestas purus viverra. Ut tortor pretium viverra suspendisse potenti. Ac turpis egestas integer eget aliquet nibh praesent. Ultrices in iaculis nunc sed augue.

Sed velit dignissim sodales ut eu sem. Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus et. Dolor morbi non arcu risus quis varius quam quisque. Non odio euismod lacinia at quis risus sed. Ultrices dui sapien eget mi proin. Semper viverra nam libero justo laoreet sit amet cursus. Urna neque viverra justo nec ultrices dui sapien. Purus sit amet luctus venenatis lectus magna fringilla urna porttitor. Enim neque volutpat ac tincidunt vitae semper. Interdum varius sit amet mattis. Id volutpat lacus laoreet non curabitur. Eu tincidunt tortor aliquam nulla facilisi cras. Lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi tincidunt. Urna id volutpat lacus laoreet non curabitur.""")


## section three: Go to the associated notebook
st.header("Run concordances in Constellate lab")
link_to_notebook("""https://constellate.org/lab?repo=https%3A%2F%2Fgithub.com%2Fithaka%2Fconstellate-notebooks&filepath=concordance.ipynb""")
### Section four: References
st.write("## References")
st.markdown("""Lindquist, H., & Levin, M. (2018). *Corpus Linguistics and the Description of English*. Edinburgh: Edinburgh University Press.

   Wynne, Martin (2008), Searching and concordancing, in Anke Lüdeling and Merja Kytö (eds), *Corpus Linguistics: An International Handbook*. Vol. I, Berlin:
de Gruyter, 706–737.""")
 




