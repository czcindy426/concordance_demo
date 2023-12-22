import streamlit as st
state = st.session_state
# from streamlit_extras.switch_page_button import switch_page
# st.session_state.update(st.session_state)
#!/usr/bin/env python
# coding: utf-8

# from scripts import tools, getdata
# tools.page_config()
# tools.css()
from io import StringIO
import nltk
import pandas as pd
import streamlit_ext as ste
import plotly.express as px
import plotly.graph_objs as go
import re
import string 
import constellate


max_lines = 2**63-1

def set_page_configuration():
    """set page configuration"""
    st.set_page_config(page_title="Upload data to get concordances",layout="wide")
    st.sidebar.header("Concordances from uploaded data")

def add_title():
    """add app title"""
    st.markdown("# Upload data to get concordances")

def display_upload_success_message():
    """display upload success message"""
    success_message = '<p style="font-family:roboto; color:Green;font-size:20px;">File uploaded successfully.</p>'
    st.markdown(success_message, unsafe_allow_html=True)  

def display_upload_complete_message():
    """message to confirm upload complete"""
    reminder = """<p style="font-family:roboto; color:Green;font-size:18px;">
    Click on the button after you are done.</p>"""
    st.markdown(reminder, unsafe_allow_html=True)  

def read_upload_file(uploaded_file):
    """read the uploaded file as a string"""
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    content = stringio.read()
    return content


def tokenize(data):
    """tokenize a string and produce a nltk text object"""
    data = data.lower()
    tokens = nltk.word_tokenize(data)
    text = nltk.Text(tokens)
    return text

def get_concordance(input_string, data_string, lines=max_lines, width=79, display=True):
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

def get_name_content(uploaded_files):
    """return a list of file names and content from uploaded files"""
    f_names = [f.name for f in uploaded_files]
    content = [StringIO(f.getvalue().decode("utf-8")).read() for f in uploaded_files]
    return f_names, content

def create_df_from_upload_files(uploaded_files, user_input):
    """create a df storing concordance from uploaded files"""
    f_name_ls, content_ls = get_name_content(uploaded_files)
    concordance_all = [[i.line for i in get_concordance(user_input, content, display=False)] for content in content_ls]
    df = pd.DataFrame({'File': f_name_ls, 'Concordance':concordance_all})
    df = df.explode('Concordance').reset_index(drop=True)
    df['Keyword'] = user_input
    return df

def get_docs(id):
    dataset_file = constellate.download(ds_id, 'jsonl')
    docs = constellate.dataset_reader(dataset_file)
    return docs

def get_id_title_fulltext(docs):
    """takes a generator of dictionaries from Constellate dataset
     and return a list of ids, titles, full text"""
    id_title_fulltext = [(f['id'], f['title'], ''.join(f['fullText'])) for f in docs]
    ids = [item[0] for item in id_title_fulltext]
    titles = [item[1] for item in id_title_fulltext]
    texts = [item[2] for item in id_title_fulltext]
    return ids, titles, texts

def create_df_from_constellate(docs, user_input):  
    f_id_ls, f_name_ls, fulltext_ls = get_id_title_fulltext(docs)
    concordance_all = [[i.line for i in get_concordance(user_input, content, lines=max_lines, width=79, display=False)] for content in fulltext_ls]
    df = pd.DataFrame({'id': f_id_ls, 'title': f_name_ls, 'concordance':concordance_all})
    df = df.explode('concordance').reset_index(drop=True)
    df['keyword'] = user_input
    return df

def plot_comparison_upload_files(uploaded_files, user_input):
    ### bar chart showing freq of 'jealous' in Othello, King Lear, Taming of the Shrew, Romeo and Juliet
    df = create_df_from_upload_files(uploaded_files, user_input)
    df = df.groupby('File').size().reset_index()
    df = df.rename(columns={0:'Freq'})
    df['keyword'] = user_input
    trace = go.Bar(x=df['File'],y=df['Freq'])
    layout = go.Layout(title = f"Frequency of '{user_input}' in uploaded files")
    data = [trace]
    fig = go.Figure(data=data,layout=layout)
    st.plotly_chart(fig)

def plot_comparison_constellate(df, user_input):
    df = df.groupby('id').size().reset_index()
    # st.dataframe(df)
    df = df.rename(columns={0:'Freq'})
    df['keyword'] = user_input
    trace = go.Bar(x=df['id'],y=df['Freq'])
    layout = go.Layout(title = f"Frequency of '{user_input}' in constellate dataset")
    data = [trace]
    fig = go.Figure(data=data,layout=layout)
    st.plotly_chart(fig)

set_page_configuration()
add_title()
with st.expander('Wonder where to find a file to try?'):

    st.write("""[The Gutenberg Project](https://www.gutenberg.org) is a great place to start. You can download a free ebook to your computer and 
        upload it below to find the concordance of a word/phrase you are interested in.""")
    st.markdown("""Here are some other resources for open e-books.""")
    st.markdown("""
        - [Directory of Open Access Books](https://www.doabooks.org)
        - [Google Books](https://books.google.com)
        - [Hathi Trust](https://www.hathitrust.org)
        - [Path to Open](https://about.jstor.org/path-to-open/titles/)
        """)

# Use the value of a session state variable 'step' to track the sequencing relation between widgets
if st.session_state.get('step') is None:
    st.session_state['step'] = 0

datapick_cols = st.columns(2)
with datapick_cols[0]:
    with st.container():
        st.info('Use your own content')
        uploaded_files = st.file_uploader("Upload .txt files", accept_multiple_files=True, key='own')
        # text to remind the user to click the upload complete button
        display_upload_complete_message()
        submit = st.button('Upload completed', key='upload complete')
        if uploaded_files and submit:
           st.session_state['step'] = 1
with datapick_cols[1]:
    with st.container():
        st.info('Use a Constellate dataset')
        ds_id = str(st.text_input("Paste your dataset id here 👇")).strip()
        if ds_id:
            dataset_file = constellate.download(ds_id, 'jsonl')
            st.session_state['step'] = 2

st.write('## Process uploaded data')
if st.session_state['step'] == 1:
    st.success(f"You've uploaded your own data.")
    user_input = str(st.text_input("""Enter a word/phrase to download concordances from uploaded files"""))
    if user_input:
        df = create_df_from_upload_files(uploaded_files, user_input)
        # download file
        ste.download_button("Download your concordance file", df, "concordance.xlsx")
        plot_comparison_upload_files(uploaded_files, user_input)
elif st.session_state['step'] == 2:  
    st.success(f"You've uploaded a constellate dataset.")
    user_input = str(st.text_input("""Enter a word/phrase to download concordances from uploaded dataset"""))
    if user_input:
        docs = constellate.dataset_reader(dataset_file)
        df = create_df_from_constellate(docs, user_input)
        ste.download_button("Download your concordance file", df, "concordance.xlsx")
        plot_comparison_constellate(df, user_input)
