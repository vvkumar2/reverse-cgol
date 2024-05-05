import streamlit as st
from st_pages import Page, show_pages, add_page_title

show_pages(
    [
        Page("src/pages/interactive_solver.py", "Interactive Solver", "🧩"),
        Page("src/pages/writeup.py", "Writeup", "📝"),
    ]
)
