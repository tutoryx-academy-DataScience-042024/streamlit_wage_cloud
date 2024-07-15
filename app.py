import streamlit as st
import os
import re
from pymongo.mongo_client import MongoClient


uri = st.secrets['MONGODB_URI']
# Create a new client and connect to the server
client = MongoClient(uri)

#database
db = client['employee_management_cloud']

#collections
employees_collections = db['employees']
wages_collections = db['wages']

#attach indexes
employees_collections.create_index('name', unique=True)
# wages_collections.create_index('name')


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
    return re.match(email_regex, email) is not None 

def is_valid_dob(dob):
    dob_regex = r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'
    return re.match(dob_regex, dob) is not None 

    
st.title('Employee Management App')

menu = ['Register Employee','Calculate Wage']

choice = st.sidebar.selectbox('Menu: ', menu)

if choice=='Register Employee':
    st.subheader('Register Employee')
    name = st.text_input('Enter Employee Name')
    dob = st.text_input('Enter DOB (yyyy-mm-dd)')
    email = st.text_input('Enter Your Email')
    if st.button('Submit'):
        if not name or not dob or not email:
            st.error('All fields are required')
        if not is_valid_dob(dob):
            st.error('Not valid DOB format!')
        if not is_valid_email(email):
            st.error('Not valid email format')
       
        employee_dict ={'name':name,
                        'dob':dob,
                        'email':email}
        try:
            employees_collections.insert_one(employee_dict)
            st.success(f'Employee {name} registered!')
        except Exception as e:
            st.error(e)
    
elif choice=='Calculate Wage':
    st.subheader('Calculate Wage')
    name =  st.text_input('Enter Employee Name')
    hours_worked = st.number_input('Enter Hours Worked', min_value=0)
    rate = st.number_input('Enter Hourly Rate', min_value=0)
    if st.button('Submit'):
        wage_calculated = hours_worked * rate

        wage_dict = {
            'name':name,
            'hours':hours_worked,
            'rate':rate
        }

        try:
            wages_collections.insert_one(wage_dict)
            st.success(f'Wage for employee {name} calculated!')
        except Exception as e:
            st.error(e)