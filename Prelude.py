#!/usr/bin/env python
# coding: utf-8

"""
# My first app, home page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""

import streamlit as st
import urllib.request 

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
# Set page config
st.set_page_config(
    page_title="Introduction to concordance")
st.sidebar.success("Intro")

### Section one: what is concordance?
st.write("# Introduction to Concordance")
st.write("## What is a concordance?")
st.markdown("""The concordance has a long history in humanities study.
   A concordance is a list of all the contexts in which a certain word/phrase occurs in a text (Lindquist and Levin 2018, 5). 
   For example, if you go to [OpenSourceShakespeare](https://www.opensourceshakespeare.org) and enter a keyword to search,
    you will find concordances compiled for people to study how the word is used in Shakespeare's works.""")
st.write("Play the following video to get a sense of concordances.")
download_video_to_play("https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/OpenSourceShakespeareForConcordanceApp.mp4")
st.caption('<div style="text-align: center">Search for concordances of \'honesty\' on OpenSourceShakespeare</div>', unsafe_allow_html=True)

### Section two: what is a concordance line?
st.write("## What is a concordance line?")
st.markdown("""In natural language processing, concordances are often presented in the form of keyword-in-context (KWIC) 
   with one line of context and the keyword centered in the line.""")
download_image("https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/tdmdocs/ConcordanceImageForConcordanceApp.jpg")

### Section three: why are concordances useful?
st.write("## Why are concordances useful?")
st.markdown("""Concordance data are useful in many ways. First of all, getting information using concordances is much faster than 
   reading closely through the complete texts. Second, with the knowledge of how a certain word or phrase is used, literary scholars can go on to 
   do comparative analysis. For example, a reseacher in comparative literature may use concordances to find out how Shakespeare used 
   astronomical terms in his works and then compare how the uses differ in his comedies and tragedies. Last, concordances provide important 
   information such as word frequency and frequency of cooccurences of certain words. Researchers can compare frequencies to describe differences 
   between geographical locations, spoken and written language, text from different historical periods, et cetera (Lindquist and Levin 2018, 8).""")
 
### Section four: References
st.write("## References")
st.markdown("""Lindquist, H., & Levin, M. (2018). *Corpus Linguistics and the Description of English*. Edinburgh: Edinburgh University Press.

   Wynne, Martin (2008), Searching and concordancing, in Anke Lüdeling and Merja Kytö (eds), *Corpus Linguistics: An International Handbook*. Vol. I, Berlin:
de Gruyter, 706–737.""")
 




