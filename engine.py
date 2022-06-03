import streamlit
import streamlit.cli as cli
streamlit.__version__ # Just in case you need to update this.
import sys

sys.argv = ['0','run','Main_Page.py']
name = "main"
cli.main()