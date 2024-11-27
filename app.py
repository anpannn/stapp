import datetime as dt
import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

def loadJSON(path):
    with open(path, 'r', encoding = 'UTF-8') as f:
        res = json.load(f)
    return res

def saveItems(path):
    f = open(path, 'w', encoding='UTF-8')
    json.dump(items, f, ensure_ascii=False)
    f.close()

def deleteItem(path, cont):
    pos = st.session_state['pos']
    if items[pos]['status'] == 'Done':
        items.pop(pos)
        saveItems(path)
        st.session_state['pos'] = 0
        st.rerun()
    else:
        cont.error('Error! The task must be done before deleting!')

def hasClicked(buttonName):
    event = 'clicked' + buttonName.capitalize()
    if event in st.session_state.keys() and st.session_state[event]:
        return True
    else:
        return False

def makeHTML(x):
    html = '''
    <style>

    div.container {
        border: black double 3px;
        border-radius:5px;
        width: 100%;
    }
    div.item_pending {
        padding: 2px;
        margin: 2px;
        border-left: green solid 5px;
        background-color: rgba(0,255,0,0.3);
    }
    div.item_priority {
        padding: 2px;
        margin: 2px:
        border-left: red solid 5px;
        background-color: rgba(255,0,0,0.3);
    }
    div.item_done {
        padding: 2px;
        margin: 2px:
        border-left: grey solid 5px;
        background-color: rgba(128,128,128,0.3);
        text-decoration: line-through;
    }
    .active {
        border: red solid 2px;
        padding: 2px;
        margin:5px;
    }
    .inactive{
        border: white solid 2px;
        padding: 2px;
        margin:5px;
    }
    p.desc {
        font-size: 20px;
        margin: 2px 10px;
    }
    p.time {
        font-size: 16px;
        margin: 2px 10px;
    }
    </style>
    
    <div class="container">
    ''' + x + '</div>'
    return html

items = loadJSON('data.json')


if 'pos' not in st.session_state:
    st.session_state['pos'] = 0

col1, col2 = st.columns([1,2])
with col1:
    lottie = loadJSON('lottie-load.json')
    st_lottie(lottie, speed=1, loop=True, width=150, height=150)
with col2:
    ''
    ''
    components.html('<div style="front-size:40px; padding:10px;">To Do List</div>',height=100, scrolling=False)

col1, col2 = st.columns([6,1])

with col1:
        cont1 = st.container()
    
with col2:
        cont2 = st.container()
    
with cont2:
    ''
    if st.button(":arrow_up:") and not hasClicked('add') and not hasClicked('edit') and st.session_state['pos'] != 0:
         st.session_state['pos'] -= 1

    if st.button(":arrow_down:") and not hasClicked('add') and not hasClicked('edit') and st.session_state['pos'] != len(items) -1:
         st.session_state['pos'] += 1
 
    if st.button('DELETE') and not hasClicked('add') and not hasClicked('edit') and (len(items) != 0) :
         deleteItem('data.json' , cont1)

temp = ''
for i, item in enumerate(items):
    if i == st.session_state['pos']:
         current = 'active'
    else:
         current = 'inactive'
    status = 'item_' + item['status'].lower()

    temp += f'''<div class="{current}">
                    <div class="{status}">
                        <p class="desc"> {item["description"]} </p>
                        <p class="time"> {item["date"]}    {item["time"]} </p>
                    </div>
                </div>'''
html=makeHTML(temp)

with cont1:
    if hasClicked('add'):
        with st.form(key='myForm1', clear_on_submit=False):
            what = st.text_input('TO DO',placeholder='What do you want to do?')
            when_date = str(st.date_input('DATE',min_value =dt.datetime.today()))
            when_time = str(st.time_input('TIME'))
            status = st.selectbox('STATUS', options=['Pending','Priority'])
            if st.form_submit_button('CONFIRM'):
                items.append({'description':what, 'date':when_date, 'time':when_time, 'status': status})
                saveItems('data.json')
                st.session_state['pos'] = len(items) - 1
                st.session_state['clickedAdd'] = False
                st.rerun()
    else:
        if cont2.button('ADD'):
            if not ('clickedEdit' in st.session_state.keys() and st.session_state['clickedEdit']):
                st.session_state['clickedAdd'] = True
                st.rerun()
    if hasClicked('edit'):
        with st.form(key='myForm2', clear_on_submit=False):
            pos = st.session_state['pos']
            item = items[pos]
            what = st.text_input('TO DO',value=item['description'])
            when_date = str(st.date_input('DATE',value=dt.datetime.strptime(item['date'], '%Y-%m-%d')))
            when_time = str(st.time_input('TIME',value=dt.datetime.strptime(item['time'], '%H:%M:%S')))
            status_new = st.selectbox('STATUS', options=['Pending', 'Priority', 'Done'], index = ['Pending', 'Priority', 'Done'].index(item['status']) )
            if st.form_submit_button('CONFIRM'):
                items[pos]['description'] = what
                items[pos]['date'] = when_date
                items[pos]['time'] = when_time
                items[pos]['status'] = status_new
                saveItems('date.json')
                st.session_state['clickedEdit'] = False
                st.rerun()
            if st.form_submit_button('CANCEL'):
                st.session_state['clickedEdit'] = False
                st.rerun()
    else:
        if cont2.button('Edit'):
            if not ('clickedAdd' in st.session_state.keys() and st.session_state['clickedAdd']):
                st.session_state['clickedEdit'] = True
                st.rerun()

components.html(html, height=2000, scrolling=False)


            
         
             

    