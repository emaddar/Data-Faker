            ##https://zetcode.com/python/faker/
            ## https://www.youtube.com/watch?v=nJHrSvYxzjE&t=0s

from cProfile import label
from pickle import TRUE
#from tkinter import CENTER
import pandas as pd
from faker import Faker
from faker.providers import internet
import streamlit as st
import numpy as np
import random
import io
from datetime import datetime
import matplotlib.pyplot as plt
import plotly_express as px








st.set_page_config(
    page_title="Generate data",
    page_icon=":checkered_flag:",
    layout="wide"
)



#st.sidebar.text("Choose one or more locales")
Local_options = st.sidebar.multiselect(
     'Choose one or more locales',
     ["ar_AA","ar_AE","ar_BH","ar_EG","ar_JO","ar_PS","ar_SA","az_AZ","bg_BG","bn_BD","bs_BA","cs_CZ","da_DK","le de","de_AT","de_CH","de_DE","dk_DK","el_CY","el_GR","le en","en_AU","en_CA","en_GB","en_IE","en_IN","en_NZ","en_PH","en_TH","en_US","le es","es_CA","es_CL","es_CO","es_ES","es_MX","et_EE","fa_IR","fi_FI","il_PH","fr_CA","fr_CH","fr_FR","fr_QC","ga_IE","he_IL","hi_IN","hr_HR","hu_HU","hy_AM","id_ID","it_CH","it_IT","ja_JP","ka_GE","ko_KR","le la","lb_LU","lt_LT","lv_LV","mt_MT","ne_NP","nl_BE","nl_NL","no_NO","or_IN","pl_PL","pt_BR","pt_PT","ro_RO","ru_RU","sk_SK","sl_SI","sq_AL","sv_SE","ta_IN","le th","th_TH","tl_PH","tr_TR","tw_GH","uk_UA","vi_VN","zh_CN","zh_TW"],
     ['fr_FR', 'en_US'])


fake = Faker(Local_options, use_weighting=False)   # see https://faker.readthedocs.io/en/master/#pytest-fixtures


#fake = Faker(['en_US', 'en_UK', 'it_IT', 'de_DE', 'fr_FR'], use_weighting=True)

#intput_val = st.text_input("Input rows number (Max : 100000)", 20)
#if not intput_val.isnumeric():
#    st.text("Please input a valid number,  Try : 25")
#if int(intput_val) >100000:
#    st.text("Please input a number smaller than 100000")





st.sidebar.markdown('---')


st.sidebar.text("Input rows number (Max : 1000)")
intput_val = st.sidebar.slider(
     'Select a range of values',
     1, 1000, 100)
#st.write('Values:', values)

#st.sidebar.markdown('---')

Select_ALL = st.sidebar.checkbox("**   Select All   **")

col1, col2, col3 = st.sidebar.columns(3)


ID = col1.checkbox('ID', value=Select_ALL)
First_name = col2.checkbox('First_name', value=Select_ALL)
Last_name= col3.checkbox('Last_name', value=Select_ALL)

Gender = col1.checkbox('Gender', value=Select_ALL)


address = col2.checkbox('Address', value=Select_ALL)
phone_number = col3.checkbox('Phone_num', value=Select_ALL)
Blood_Type = col1.checkbox('Blood_Type', value=Select_ALL)
Job = col2.checkbox('Job', value=Select_ALL)
email = col3.checkbox('email', value=Select_ALL)
dob = col1.checkbox('DOB', value=Select_ALL)
SSN = col2.checkbox('SSN', value=Select_ALL)
Age = col3.checkbox('Age', value=Select_ALL)
note = col2.checkbox('note', value=Select_ALL)

proba_M = st.sidebar.slider('Male Probability : ',0.0,1.0 , 0.5)
st.sidebar.write("Female Probability :", round(1-proba_M,2))



if Select_ALL or ID or Gender or First_name or Last_name or address or phone_number or Blood_Type or Job or email or dob or SSN or note:
    #st.sidebar.markdown('---')



    Blood_list = ["A+", "A-", "B+", "B-", "O+", "O-", "AB", "AB-"]
    customers = {}

    if Age and not dob :
                st.markdown("<h5 style='text-align: left; color: red;'>  Please Select DOB first to generate Age </h5>", unsafe_allow_html=True)
                


    for i in range(0, int(intput_val)):
        customers[i]={}
        if ID: customers[i]['id'] = i+1

        if Gender: 
                customers[i]['Gender'] = np.random.choice(["M","F"], p=[proba_M,1- proba_M])
        if First_name :
            if Gender: 
                customers[i]['First_name'] = fake.first_name_male() if customers[i]['Gender'] =="M" else fake.first_name_female()
            else:
                customers[i]['First_name'] =  fake.first_name()
        if Last_name: customers[i]['Last_name'] = fake.last_name()
        if address: customers[i]['address'] = fake.address().replace('\n', ', ')
        if phone_number: customers[i]['phone_number'] = fake.phone_number()
        if email:
            if First_name and Last_name:
                customers[i]['email'] = f"{customers[i]['First_name']}.{customers[i]['Last_name']}@{fake.company_email()}.com" 
            elif First_name:
                customers[i]['email'] = f"{customers[i]['First_name']}.{fake.random_int(1,546)}@{fake.company_email()}.com" 
            elif Last_name:
                customers[i]['email'] = f"{customers[i]['Last_name']}.{fake.random_int(1,546)}@{fake.company_email()}.com" 
            else :
                customers[i]['email'] = fake.company_email()
        
        if Blood_Type : 
            random_blood_type = random.choices(Blood_list, weights =(30,30,30,30,30,5,30,30 ) )
            customers[i]['Blood_Type'] = ''.join(random_blood_type)

        if dob: 
            
            customers[i]['dob'] = datetime.strptime(fake.date(), "%Y-%m-%d").date()
            Age_i = datetime.now().year - customers[i]['dob'].year

            if Age:
                customers[i]['Age'] = Age_i

        if Job and dob : 
            if Age_i >=18:
                   customers[i]['Job'] = fake.job() 
            else:
                customers[i]['Job'] = ''

        if SSN: customers[i]['Secur. Soc. N.'] = fake.ssn()
        if note: customers[i]['note'] = fake.text().replace('\n', ' ')
        
        if Select_ALL: customers[i]['id'] = i+1


    df = pd.DataFrame(customers).T


    st.markdown("<h4 style='text-align: left; color: black;'>  Data preview </h4>", unsafe_allow_html=True)

    st.dataframe(df)


    col1, col2, col3 , col4, col5= st.columns(5)

    with col1 :

        st.markdown("<h4 style='text-align: left; color: black;'>  Download data as : </h4>", unsafe_allow_html=True)
        data_type = st.radio("",("csv","xlsx"))


        if data_type == "csv":
            data = df.to_csv(index = False).encode('utf-8')

            st.download_button(
            label=f"Download data as {data_type}",
            data=data,
            file_name=f'Data_{datetime.now()}.{data_type}',
            mime='text/csv',
            )

        elif data_type == "xlsx":
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Data')
                    writer.save() # Close the Pandas Excel writer and output the Excel file to the buffer

                    st.download_button(
                        label=f"Download data as {data_type}",
                        data=buffer,
                        file_name=f'Data_{datetime.now()}.{data_type}',
                        mime="application/vnd.ms-excel"
                    )


    with col2:

        if Gender :
            st.markdown("<h4 style='text-align: center; color: black;'>  Per Gender </h4>", unsafe_allow_html=True)

            fig1, ax1 = plt.subplots(figsize=(3,3))
            df.groupby('Gender').size().plot(kind='pie', textprops={'fontsize': 8},
                                        autopct='%1.1f%%',
                                        #colors=['#ee82ee', "#0083b8"],
                                        wedgeprops={'alpha':0.5},
                                        ax=ax1)
            #fig1.set_facecolor('#00172b')
            ax1.set_ylabel('')
            st.pyplot(fig1)
    
    with col3:
        if Gender and Blood_Type:
            F_num = df['Gender'].tolist().count('F')
            M_num = df['Gender'].tolist().count('M')
            st.markdown("<h4 style='text-align: left; color: black;'>  Per Blood Type </h4>", unsafe_allow_html=True)
            df_pivot = ddd= df.groupby(['Blood_Type', 'Gender'])["Gender"].count().unstack().fillna(0)

            if F_num>0 and M_num>0:
                        df_pivot["% of M"] = round((df_pivot.M/ df_pivot.M.sum()*100),2).astype(str) + '%'
                        df_pivot["% of F"] = round((df_pivot.F/ df_pivot.F.sum()*100),2).astype(str) + '%'
                        df_pivot = df_pivot.drop(["F", "M"], axis=1)
                        st.dataframe(df_pivot)
            elif F_num == 0:
                        df_pivot["% of M"] = round((df_pivot.M/ df_pivot.M.sum()*100),2).astype(str) + '%'
                        df_pivot = df_pivot.drop(["M"], axis=1)
                        st.dataframe(df_pivot)
            else:
                        df_pivot["% of F"] = round((df_pivot.F/ df_pivot.F.sum()*100),2).astype(str) + '%'
                        df_pivot = df_pivot.drop(["F"], axis=1)
                        st.dataframe(df_pivot)
                    
        elif Blood_Type and not Gender :
            st.markdown("<h4 style='text-align: left; color: black;'>  Per Blood Type </h4>", unsafe_allow_html=True)
            df_groupby = df.groupby(["Blood_Type"])['Blood_Type'].count()
            st.dataframe(df_groupby)
                
        with col4:

            if (dob and Gender) and not Age :
                st.markdown("<h4 style='text-align: left; color: black;'>  Aver. Age per Gender </h4>", unsafe_allow_html=True)
                df["Age"] = round(datetime.now().year - pd.to_datetime(df['dob'],format =  "%Y-%m-%d").dt.year,2)
                df_pivot_age_gender = pd.pivot_table(data = df, values='Age', index='Gender', aggfunc='mean', fill_value=0)                
                st.dataframe(df_pivot_age_gender.astype(str))
            elif dob and Gender and Age:
                st.markdown("<h4 style='text-align: left; color: black;'>  Aver. Age per Gender </h4>", unsafe_allow_html=True)
                df["Age"] = round(datetime.now().year - pd.to_datetime(df['dob'],format =  "%Y-%m-%d").dt.year,2)
                df_pivot_age_gender = pd.pivot_table(data = df, values='Age', index='Gender', aggfunc=np.average, fill_value=0).round(0)
                st.dataframe(df_pivot_age_gender.astype(str))
            elif (dob and Age) and not Gender:
                st.markdown("<h4 style='text-align: left; color: black;'>  Average Age </h4>", unsafe_allow_html=True)
                st.write('Average Age : ', round(df.Age.mean(),0))
            elif dob and not (Age and Gender):
                st.markdown("<h4 style='text-align: left; color: black;'>  Average Age </h4>", unsafe_allow_html=True)
                df["Age"] = round(datetime.now().year - pd.to_datetime(df['dob'],format =  "%Y-%m-%d").dt.year,2)
                st.write('Average Age : ', round(df.Age.mean(),0))
            elif Age and not (dob and Gender):
                st.markdown("<h4 style='text-align: left; color: black;'>  "" </h4>", unsafe_allow_html=True)

        #with col5:
        #    if dob or Age:
        #        fig = px.histogram(df, x="Age", color='Gender')
        #        st.plotly_chart(fig)


else:
    st.write("Your data will be generated here")


