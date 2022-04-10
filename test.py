# -*- coding:utf-8 -*-
import csv
import pandas as pd
import numpy as np
import streamlit as st
import time

st.title('Parasites Test')

if 'parasite' not in st.session_state:
	st.session_state.parasite = pd.read_csv('parasite.csv')
if 'shuffle' not in st.session_state:
    st.session_state.shuffle = st.session_state.parasite.sample(frac=1).reset_index(drop=True)
    st.session_state.shuffle.insert(len(st.session_state.shuffle.columns), 'Correct', False)
if 'ind' not in st.session_state:
    st.session_state.ind = 0
if 'correct' not in st.session_state:
    st.session_state.correct = False
if 'state' not in st.session_state:
    st.session_state.state = 0

shuffle = st.session_state.shuffle


def check_ans(ans):
    if ans == 'a':
        st.session_state.correct = True
    else:
        st.session_state.correct = False

    st.session_state.state = 1

def next_qestion():
    st.session_state.ind += 1
    st.session_state.state = 0

def restart_quiz():
    st.session_state.ind = 0
    st.session_state.state = 0
    st.session_state.shuffle = st.session_state.parasite.sample(frac=1).reset_index(drop=True)

def quiz():
    st.subheader(shuffle.iloc[st.session_state.ind]['Chinese'])

    if st.session_state.state == 0:
        ans = st.text_input('請寫出英文原名：')
        result = st.button('SUBMIT', on_click=check_ans, args=(ans, ))
    else:

        if st.session_state.correct:
            st.caption(shuffle.iloc[st.session_state.ind]['English'])
            st.success('CORRECT!\n')
            st.session_state.shuffle.at[st.session_state.ind, 'Correct'] = True

        else:
            st.caption(shuffle.iloc[st.session_state.ind]['English'])
            st.error('INCORRECT!\n'+shuffle.iloc[st.session_state.ind]['Chinese'])
            st.session_state.shuffle.at[st.session_state.ind, 'Correct'] = False
            

        result = st.button('NEXT', on_click=next_qestion)

    progress = st.progress(st.session_state.ind / (st.session_state.shuffle.shape[0]-1))


def highlight_survived(s):
    return ['background-color: #336331']*len(s) if s.Correct else ['background-color: #633131']*len(s)

def color_survived(val):
    color = 'green' if val else 'red'
    return f'background-color: {color}'


ind = st.session_state.ind

if ind >= shuffle.shape[0]:
    st.table(shuffle.style.apply(highlight_survived, axis=1))
    result = st.button('RESTART', on_click=restart_quiz)

else:
    quiz()
