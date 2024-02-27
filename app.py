#!/usr/bin/env python
# coding: utf-8


"""
Pre-code tutorial on concordance
"""
# Import libraries
from pathlib import Path

import streamlit as st
import nltk
import pandas as pd
import plotly.graph_objs as go

# Define constants
MAX_LINES = 2**63 - 1


@st.cache_data
def read_file(fname):
    """read in the data of a file"""
    path = Path(__file__).parent / "data" / fname
    with open(path, "r") as f:
        content = f.read()
    return content


othello_data = read_file("othello.txt")
lear_data = read_file("king_lear.txt")
tame_data = read_file("taming_of_the_shrew.txt")
merchant_data = read_file("merchant_of_venice.txt")


# define a function to load images
def display_image(image, caption=None):
    """Display a centered image and caption. Enclose it with a border."""
    path = Path(__file__).parent / "data" / image
    col1, col2, col3 = st.columns([2, 5, 2])

    with col2:
        image_container = st.container(border=True)
        image_container.image(str(path), caption=caption)


def try_another_word():
    st.markdown("""#### Try a different word/phrase""")
    st.markdown(
        "Enter a keyword of your interest to generate a KWIC index for *Othello*, *King Lear*, *Taming of the Shrew*, and *The Merchant of Venice*."
    )
    st.markdown(
        """
    *Note: We have decided to lowercase all the letters for our analysis. The benefit to this approach is we can collect all examples of the key word, whether they occur at the beginning of a sentence or not. One downside is that
     certain information could get mistaken, for example, if 'Black' referred to a person's name. A major benefit of learning to write your own code is the flexibility for making these kinds of research choices.*
    """
    )
    display_num_lines_message()
    user_input = str(st.text_input("""Enter a keyword 👇"""))
    if user_input:
        # Compute word frequencies for each text
        freq_othello = len(
            get_concordance(
                user_input,
                othello_data,
                lines=MAX_LINES,
                display=False,
            )
        )

        freq_lear = len(
            get_concordance(user_input, lear_data, lines=MAX_LINES, display=False)
        )

        freq_tame = len(
            get_concordance(user_input, tame_data, lines=MAX_LINES, display=False)
        )

        freq_merchant = len(
            get_concordance(user_input, merchant_data, lines=MAX_LINES, display=False)
        )

        # Display the KWIC indices
        display_freq(user_input, freq_othello, "Othello")
        get_concordance(user_input, othello_data)

        display_freq(user_input, freq_lear, "King Lear")
        get_concordance(user_input, lear_data)

        display_freq(user_input, freq_tame, "Taming of the Shrew")
        get_concordance(user_input, tame_data)

        display_freq(user_input, freq_merchant, "Merchant of Venice")
        get_concordance(user_input, merchant_data)

        # section three: Expand the comparison

        plot_comparison(user_input)


@st.cache_data
def tokenize(data_string):
    """tokenize the file content string and return a nltk Text object"""
    data_string = data_string.lower()
    tokens = nltk.word_tokenize(data_string)
    text_obj = nltk.Text(tokens)
    return text_obj


@st.cache_data
def get_concordance(input_string, data_string, lines=25, width=100, display=True):
    """take an input string and a data string and write out the concordance of the input string
    in data string or return the concordance"""
    input_string = input_string.lower()
    input_ls = input_string.split()
    concordance = tokenize(data_string).concordance_list(input_ls, width, lines)
    if display:
        for i, line in enumerate(concordance):
            st.markdown(
                '<p style="font-family:courier;text-align:center;white-space:pre"><small>'
                + line.left_print
                + "&nbsp;"
                + "<strong>"
                + line.query
                + "</strong>"
                + "&nbsp;"
                + line.right_print
                + "</small></p>",
                unsafe_allow_html=True,
            )
    else:
        return concordance


def display_freq(word, freq, text):
    ### display freq message
    st.markdown(f"##### The word *{word}* appears {freq} times in *{text}*.")


def display_num_lines_message():
    st.markdown("""At most 25 concordances lines are displayed.""")


@st.cache_data
def plot_comparison(user_input="black"):
    ### bar chart showing freq of 'black' in Othello, King Lear, Taming of the Shrew, Merchant of Venice
    freq_othello = len(
        get_concordance(
            user_input, othello_data, lines=MAX_LINES, width=100, display=False
        )
    )
    freq_lear = len(
        get_concordance(
            user_input, lear_data, lines=MAX_LINES, width=100, display=False
        )
    )
    freq_tame = len(
        get_concordance(
            user_input, tame_data, lines=MAX_LINES, width=100, display=False
        )
    )
    freq_merchant = len(
        get_concordance(
            user_input, merchant_data, lines=MAX_LINES, width=100, display=False
        )
    )
    df = pd.DataFrame(
        {
            "Canon": [
                "Othello",
                "King Lear",
                "Taming of the Shrew",
                "Merchant of Venice",
            ],
            "Freq": [freq_othello, freq_lear, freq_tame, freq_merchant],
        }
    )
    trace = go.Bar(x=df["Canon"], y=df["Freq"])
    layout = go.Layout(
        title=f"Frequency of '{user_input}' in four of Shakespeare's works"
    )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)


@st.cache_data
def create_social_science_table():
    concordance_lines = [
        """This varied group of postmodern thinkers employs the tool of deconstruction
                to critically evaluate indeed, to peel back the discursive layers of-development's 
                assumptions: capitalist economics, progress, modernity and rationality.""",
        """Their deconstructions reveal development's asymmetric dichotomization of the world
                into modern, Westernized societies on the one hand and traditional, 
                "backward" societies on the other.""",
        """It will be the purpose of this article to utilize the deconstructive tool from 
                a feminist perspective, to carry the postmodern theorists deconstructions one step 
                further ot unravel the elements of development theory that carry Western gender biases 
                regarding proper roles for women and men based on their "true nature." """,
        """This process of feminist deconstruction correlates with a contemporary trend in 
                feminist analysis, that of deconstructing institutions such as the state and law, 
                and discourses of democratic theory and international relations theory, to expose 
                their reliance upon, and infusion with, gender.""",
        """Feminist deconstruction, then, is distinct from the earlier empirical project that 
                enumerates women's experiences with development.""",
        """Feminist deconstruction si "not simply about women," but about the interdependent 
                constructions of masculine and feminine, and about shifting feminist analysis from the 
                margin to the centre.""",
        """The first step in this exercise si to briefly describe the postmodern approach to
                Western development theory, following which a theoretical feminist deconstruction can 
                be carried out.""",
        """I will be instructive, as well, to apply this deconstruction to an example of 
                development in practice, the maquiladora project of Mexico.""",
        """Deconstruction wil be used here to refer to a critical method, a conceptual tool, 
                with which the ideological layers of development are peeled back and examined.""",
        """The process of deconstruction si part of the larger postmodern project, which is to 
                de-naturalize some of the dominant features of our way of life; to point out that 
                those entities that we unthinkingly experience as "natural" (they might even include 
                capitalism, patriarchy, liberal humanism) are ni fact "cultural"; made by us, not given 
                to us (Hutcheon 1989:2).""",
        """Postmodern deconstructions of development recognize that world cultures have always 
                been mutually influencing and that there exists no such thing as a "pure" culture to be 
                preserved and cloistered away.""",
        """A viable deconstruction of development can be commenced without relying on the binarism of 
                universal/relative.""",
        """What deconstruction does show si that development has, from its inception, posited a Western 
                model sa "the most successful way of life mankind [sic] has ever known" (Ayres 1978: xxxii-xxxiii)
                and that the implementation of this assumption through development has proved destructive to viable 
                and vital cultures and societies.""",
        """It is this gap in postmodern theorizing that necessitates a specifically feminist deconstruction 
                of the development paradigm.""",
        """Moreover, a feminist deconstruction of development theory takes as axiomatic the idea that women, 
                in practice, transgress the border between public and private""",
        """Just as postmodern theory finds the dichotomies of developed/underdeveloped, modern/traditional, 
                and so forth to be central features of development thought, a feminist deconstruction reveals that 
                development theory is phallocentric as ti organizes social life along the lines of the dichotomies 
                of man/woman, public/ private, reason/emotion and knowledge/experience.""",
        """Rather than trying to reconcile these dichotomies, as women and development theory has tried to do, 
                a feminist deconstruction recognizes them as instrumental to the Westernizing project of development.""",
        """Feminist deconstruction, then, must involve changing the parameters of who can know and who can 
                produce theory; it must involve relocating the site of knowledge and theory creation.""",
        """Derrida, who coined the term, refuses to define deconstruction, arguing that any attempt to define
                    it is also subject to the process of deconstruction.""",
    ]
    df = pd.DataFrame({"Concordance": concordance_lines}, index=range(1, 20))
    return df


@st.cache_data
def create_natural_science_table():
    concordance_lines = [
        "New",
        "Biological",
        "Emerging",
        "Genetic",
        "Global",
        "Synthetic",
        "Artificial",
        "Evolutionary",
        "Inductrial",
        "Metabolic",
        "Potential",
        "Brave",
        "Future",
        "Other",
        "Clinical",
        "International",
        "Natural",
        "Cutting-Edge",
        "Advanced",
        "Ethical",
    ]
    df = pd.DataFrame({"Adjective": concordance_lines}, index=range(1, 21))
    return df


def main():
    """
    Main function of the app. Use this to call function definitions above.
    Ultimately, this function is called by the root Streamlit app, main.py.
    """

    # set the customized heading sizes
    css = read_file("style.css")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    ### Section one: Introduction
    st.markdown("# What is a concordance?")
    st.markdown(
        """A concordance is an alphabetical list of the usage of a *key word* within a significant text (or body of texts), such as the Christian Bible or the works of Shakespeare. 
    A concordance is useful for close-reading and textual analysis since it gathers together every context for the use of a particular word or phrase. For example, we could see
    every context in which Shakespeare mentions the color "red", the concept of "allegiance", or the feeling of "jealousy," revealing the way he framed and understood them. 
    To use the Christian Bible as an example, we could find every example of a particular term in Biblical Hebrew or Aramaic and discover how they might be translated into the King James's Version.

## Using Key Word in Context (KWIC) for visualizing concordances
The most common way to visualize a concordance is a type of index called Key Word in Context, or KWIC. We can generate a KWIC index for any key word using text analysis. The
index places the key word in a central column within a "context window," a chosen number of words or characters that occur both before and after the given word."""
    )

    display_image(
        "effect.png",
        "Figure 1: The key word 'effect' in context from the [BNC-Baby corpus](http://www.natcorp.ox.ac.uk/corpus/babyinfo.html).",
    )

    st.markdown("## Concordance in text analysis")
    st.markdown(
        """Creating a KWIC index is a useful approach whenever a scholar wants to examine how a particular word or phrase is used over a significant body of materials. 
    The body of materials could represent the works of a single author (such as Toni Morrison), a community of writers (2010s rappers), a period (19th century newspapers), or some other category. 
    A KWIC can help us go beyond word frequencies by giving the context of the word use for future analysis. Using a concordance usually means combining distant reading (in this case, algorithmically collating
    the contexts) with close reading (examining word choice and meaning in detail). After the KWIC index is created, the scholar can analyze the contexts for their research.
    """
    )

    ### Section two: Disciplinary Examples
    st.markdown("### Choose a discipline to see an example KWIC index")
    tab1, tab2, tab3 = st.tabs(["Humanities", "Social sciences", "Natural sciences"])
    with tab1:
        with st.container(border=True):
            st.markdown("#### Studying Shakespeare and identity")
            st.markdown(
                """
            Race is an essential issue in the study of Shakespeare's plays, including *The Merchant of Venice* and *Othello: The Moor of Venice*. In "The Racial Disgust in Early Modern England: The Case of *Othello*" (2022), Bradley J. Irish
             affirms that "The ongoing development of Premodern Critical Race Studies (PCRS) is perhaps the most exciting intellectual current in early modern studies today" (224). For his part, Michael Neill, the editor of *Othello* for *The Oxford Shakespeare* (2006), observes: 
            "Anxieties about the treatment of race in *Othello* are a recurrent feature of both its critical and performance histories: where they once focused on the supposed scandal of miscegenation, 
            they are nowadays more likely to address the play's complicity in racial stereotyping" (41). While the concept of "race" was not understood in the same terms we use today, it is still
            evident in the language within Shakespeare's plays, particularly around terms like "black," "white," "fair," and "complexion." When thinking about race, we might look at how the concept of "blackness" is weaponized in *Othello*.
             This can reveal more about how Shakespeare and his contemporaries understood issues of race. 
            """
            )
            st.markdown("""##### The Key Word "black" in Othello and King Lear""")
            st.markdown(
                "This example uses the [The Folger Shakespeare](https://www.folger.edu/explore/shakespeares-works/download/) editions."
            )
            freq_othello = len(
                get_concordance(
                    "black", othello_data, lines=MAX_LINES, width=100, display=False
                )
            )
            display_freq("black", freq_othello, "Othello")
            get_concordance("black", othello_data)
            freq_lear = len(
                get_concordance(
                    "black", lear_data, lines=MAX_LINES, width=100, display=False
                )
            )
            display_freq("black", freq_lear, "King Lear")
            get_concordance("black", lear_data)

            # section three: Expand the comparison
            st.markdown("#### Expand the comparison")
            st.markdown(
                """The KWIC index reveals that Shakespeare uses 'black' in *Othello* and *King Lear* differently. We can see that Shakespeare uses "black" often to refer to Othello's
                skin, considering whether his appearance matches his inner self. We can see this comparison in examples like, "your son-in-law is far more fair than black," "is now begrimed and black
                as mine own face," and "i am black and have not those soft parts of conversation." In all these cases, Shakespeare mines the question of outward appearances and inward truth."""
            )
            st.markdown(
                """We can also see that "blackness" is mentioned more often in *Othello* than *King Lear*. Let's compare the frequency of 'black' in four of Shakespeare's works: *Othello*, *King Lear*, *Taming of the Shrew*, and *The Merchant of Venice*."""
            )

            plot_comparison("black")

            # section four: Try another word
            st.markdown(
                """Creating a KWIC can help draw our attention to important contexts. Are there other words that could help us understand race in context? Try examining other key words in context below. 
            What about if we wanted to study race in *The Merchant of Venice?* Or gender in the *The Taming of the Shrew*?"""
            )
            try_another_word()
    with tab2:
        with st.container(border=True):
            st.markdown("""## Understanding "deconstruction" as used by one author""")
            st.markdown(
                """The concept of "deconstruction" is an abstract term coined by Jacques Derrida, who did not define it.
                In an example concordance study, Bernard et al. (2017) wondered how Joanne Wright used this term in her 
                interesting article titled "Deconstructing Development Theory: Feminism, the Public/Private 
                Dichotomy and the Mexican Maquiladoras". The authors searched for "deconstruction" or its plural 
                "deconstructions". They found 19 concordances of "deconstruction"/"deconstructions" in the article."""
            )
            deconstruction_df = create_social_science_table()
            st.markdown(
                """The authors then sorted these sentences based on the various meanings of "deconstruction/deconstructions".
                They found that Wright uses "deconstruction" to mean a tool, a process of analysis, the results of an analysis 
                and a theory. The concordance method gives the authors a way to deconstruct the meaning of the word "deconstruction" 
                as used by one author."""
            )
            st.table(deconstruction_df)
            st.caption(
                """Concordances of "deconstruction"/"deconstructions" in Wright (1997)"""
            )
    with tab3:
        with st.container(border=True):
            st.markdown("## Studying science communication using concordances")
            st.markdown(
                """
                The International Genetically Engineered Machines (iGEM) team at the University of New Castle conducted a research to examine how 
                the public engage with synthetic biology and related topic areas by identifying any patterns in language use 
                in texts that address these issues, and investigating how they are discussed in the media. The research results 
                were then be used to help produce guidelines for communicating synthetic biology to the largest possible audience to 
                improve the impact of the advancements in science on this team. For example, the researchers searched for *Synthetic Biology* 
                in NOW: Corpus of News on the Web (Davies, 2013), found the concordance lines and studied the top 20 adjectives that co-occur 
                with *Synthetic Biology*. With the concordance lines as context, they could identify if these adjectives are being 
                used to portray synthetic biology in a positive or negative light. 
            """
            )
            adj_df = create_natural_science_table()
            st.table(adj_df)
            st.markdown(
                """
                    The results indicate that the adjectives surrounding synthetic biology have both positive and negative associations 
                    and therefore the authors came to the conclusion that it is important to acknowledge this when discussing the iGEM project.  
                    """
            )

    ## Section three: Paste your own text
    st.markdown("## Explore concordances with your own text")
    st.markdown(
        """Try creating a KWIC index with your own text. For example, copy the text from a research article on [JSTOR](https://jstor.org) or a novel from
                [Project Gutenberg](https://www.gutenberg.org/). *The maximum number of characters is 1,000,000.*
                
                """
    )

    user_text = st.text_area("Paste your text here", max_chars=1_000_000)
    user_term = st.text_input("Enter your key word here", max_chars=20)

    # Create a download file and show first 25 results
    if user_text and user_term:

        # Collect all the results in a string
        kwic_results = get_concordance(
            user_term, user_text, lines=MAX_LINES, display=False
        )
        kwic_string = ""
        for i in kwic_results:
            kwic_string = kwic_string + i.line + "\n"

        # Display the first 25 results
        st.markdown(
            """*Up to 25 occurrences are displayed. To view all occurrences, download your KWIC data as a text file to your computer.*
                """
        )

        get_concordance(user_term, user_text, lines=25, display=True)

        # Allow the user to download all results
        st.download_button(
            "Download .txt file",
            kwic_string,
            f"{user_term}_concordance.txt",
        )

    ## Section four: Share Additional Learning Resources
    st.markdown("## Get more out of your analysis with code!")
    st.markdown(
        """
    Want to analyze a larger documents or more documents at a time? Search multiple keywords? Try our code notebook on concordance to get started.
    """
    )
    st.link_button(
        "View code notebook in lab :arrow_right:",
        "https://constellate.org/lab?repo=https%3A%2F%2Fgithub.com%2Fithaka%2Fconstellate-notebooks&filepath=concordance.ipynb",
    )

    ### Section five: References
    st.markdown("## References")
    st.markdown(
        """
        - Bernard, H. R., Wutich, A., & Ryan, G. W. (2017). *Analyzing qualitative data: Systematic approaches*. SAGE publications.
        - Brinkman, Eric. "Iago as the Racist-Function in *Othello*." *Shakespeare Bulletin*, vol. 40, no. 1, 2022.
        - Davies, Mark. (2013) Corpus of News on the Web (NOW): 3+ billion words from 20 countries, updated every day. Available online at https://corpus.byu.edu/now/.
        - Folger Shakespeare - Complete Set, The. *The Folger Shakespeare Library*, https://www.folger.edu/explore/shakespeares-works/download/. Accessed 31 Jan 2024.
        - Dhar, Amrita. "Shakespeare, Race, and Disability: *Othello* and the Wheeling Strangers of Here and Everywhere." *The Oxford Handbook of Shakespeare and Race*, Ed. Patricia Akhimie, Oxford UP, 2024.
        - Irish, Bradley J. "Racial Disgust in Early Modern England: The Case of *Othello*".*Shakespeare Quarterly*, vol. 73, no. 3-4, Fall-Winter 2022, pp. 224-245.
        - Newcastle University iGEM Team. (2017). *A corpus based investigation into science communication*. https://static.igem.org/mediawiki/2017/9/95/T--newcastle--zw-corpus_investigation.pdf
        - Shakespeare, William. *Othello: The Moore of Venice*, edited by Michael Neill, Oxford University Press, 2006.
        - Wright, J. (1997). Deconstructing development theory: Feminism, the public/private dichotomy and the Mexican Maquiladoras. *Canadian Review of Sociology/Revue Canadienne de Sociologie, 34*(1), 71-91. 
        """
    )


if __name__ == "__main__":
    ###Conditional that checks if this file is being run directly.
    ###This is the entrypoint for running the app locally or on it's own.
    ###Code in this block will not be run when the app is imported.

    main()
