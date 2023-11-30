#!/usr/bin/env python
# coding: utf-8

"""
# My first app, home page 
Here's our first attempt at using streamlit to make a no-code tutorial for concordance
"""

import streamlit as st

# Set page config

st.set_page_config(
    page_title="Introduction to concordance")

st.write("# Introduction to Concordance")
st.sidebar.success("Intro")
st.write("""The concordance has a long history in humanities study.
    A concordance gives the context of a given word or phrase in a body of texts. 
    For example, a literary scholar might ask: how often and in what context does Shakespeare use the phrase 
    "honest Iago" in Othello? 
    A historian might examine a particular politician's speeches, looking for examples of a particular dog whistle.""")






