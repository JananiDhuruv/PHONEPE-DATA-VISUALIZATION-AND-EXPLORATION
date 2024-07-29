import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import requests
import json
from PIL import Image
import plotly.express as px
import time

# Establish MySQL connection and fetch data into DataFrames (omitting for brevity)
#df creation
mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhuruvanth@29",
    database="pe",
    port="3306"
)

mycursor = mydatabase.cursor(buffered=True)
#agree TRANS
mycursor.execute("SELECT *FROM agg_df")
mydatabase.commit()
agg_table1=mycursor.fetchall()
agg_trans=pd.DataFrame(agg_table1,columns=("states","years","quarter","transaction_type","transaction_count","transaction_amount"))

#aggree user
mycursor.execute("SELECT *FROM agg_user_df2")
mydatabase.commit()
agg_table2=mycursor.fetchall()
agg_user=pd.DataFrame(agg_table2,columns=("states","years","quarter","brands","transaction_count","percentage"))

#map trans
mycursor.execute("SELECT *FROM map_trans")
mydatabase.commit()
map_table3=mycursor.fetchall()
map_table_trans=pd.DataFrame(map_table3,columns=("states","years","quarter","districts","transaction_count","transaction_amount"))

#map user
mycursor.execute("SELECT *FROM map_user")
mydatabase.commit()
map_table4=mycursor.fetchall()
map_table_user=pd.DataFrame(map_table4,columns=("states","years","quarter","districts","registeredUser","appOpens"))

#top trans
mycursor.execute("SELECT *FROM top_trans")
mydatabase.commit()
top_table5=mycursor.fetchall()
top_table_trans=pd.DataFrame(top_table5,columns=("states","years","quarter","pincodes","transaction_count","transaction_amount"))

#top user
mycursor.execute("SELECT *FROM top_user_df")
mydatabase.commit()
top_table6=mycursor.fetchall()
top_table_user=pd.DataFrame(top_table6,columns=("states","years","quarter","pincodes","registeredusers"))



# Functional block for transaction amount and count by year
def Trans_amt_year_wise(df, YEAR):
    trans = df[df["years"] == YEAR]
    trans.reset_index(drop=True, inplace=True)
    trans_y_group = trans.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    trans_y_group.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(trans_y_group, x="states", y="transaction_amount",
                        title=f"{YEAR} **TRANSACTION AMOUNT**", color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(trans_y_group, x="states", y="transaction_count",
                        title=f"{YEAR} **TRANSACTION COUNT**", color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width=600)
        st.plotly_chart(fig_count)


    col1,col2 = st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for features in data1["features"]:
            states_name.append(features["properties"]["ST_NM"])
        states_name.sort()

        fig_india=px.choropleth(trans_y_group, geojson=data1, locations="states",featureidkey="properties.ST_NM",
                                color="transaction_amount", color_continuous_scale="viridis",
                                range_color=(trans_y_group["transaction_amount"].min(),trans_y_group["transaction_amount"].max()),
                                hover_name="states",title=f"{YEAR}**TRANSACTION AMOUNT**",fitbounds="locations",
                                height=600,width=600)
        fig_india.update_geos(visible= False)
        st.plotly_chart(fig_india)

    with col2:
        fig_india1=px.choropleth(trans_y_group, geojson=data1, locations="states",featureidkey="properties.ST_NM",
                                color="transaction_count", color_continuous_scale="viridis",
                                range_color=(trans_y_group["transaction_count"].min(),trans_y_group["transaction_count"].max()),
                                hover_name="states",title=f"{YEAR}**TRANSACTION COUNT**",fitbounds="locations",
                                height=600,width=600)
        fig_india1.update_geos(visible= False)
        st.plotly_chart(fig_india1)
    return trans


#functional block--quarter
def Trans_amt_quarterwise(df, QUARTER):
    tquarter=df[df["quarter"]==QUARTER]
    tquarter.reset_index(drop=True,inplace=True)
    transy_group=tquarter.groupby("states")[["transaction_count","transaction_amount"]].sum()
    transy_group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(transy_group,x="states",y="transaction_amount",title=f"{tquarter['years'].min()} YEAR {QUARTER} **QUARTER TRANSACTION AMOUNT**", color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(transy_group,x="states",y="transaction_count",title=f"{tquarter['years'].min()} YEAR {QUARTER} **QUARTER TRANSACTION COUNT**",color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for features in data1["features"]:
            states_name.append(features["properties"]["ST_NM"])
        states_name.sort()

        fig_india=px.choropleth(transy_group, geojson=data1, locations="states",featureidkey="properties.ST_NM",
                                color="transaction_amount", color_continuous_scale="viridis",
                                range_color=(transy_group["transaction_amount"].min(),transy_group["transaction_amount"].max()),
                                hover_name="states",title=f"{tquarter['years'].min()} YEAR {QUARTER}**TRANSACTION AMOUNT**",fitbounds="locations",
                                height=600,width=600)
        fig_india.update_geos(visible= False)
        st.plotly_chart(fig_india)

    with col2:
        fig_india1=px.choropleth(transy_group, geojson=data1, locations="states",featureidkey="properties.ST_NM",
                                color="transaction_count", color_continuous_scale="viridis",
                                range_color=(transy_group["transaction_count"].min(),transy_group["transaction_count"].max()),
                                hover_name="states",title=f"{tquarter['years'].min()} YEAR {QUARTER}**TRANSACTION COUNT**",fitbounds="locations",
                                height=600,width=600)
        fig_india1.update_geos(visible= False)
        st.plotly_chart(fig_india1)
    return tquarter


#agg_trans_type--correcrt
def agg_trans_typewise(df,STATE):
    ttype=df[df["states"]==STATE]
    ttype.reset_index(drop=True,inplace=True)
    ttype_group=type.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()
    ttype_group.reset_index(inplace=True)
    fig_pie_1=px.pie(ttype_group, names= "transaction_type",values="transaction_count",
                    width=600,title="TRANSACTION COUNT",hole=0.5)
    st.plotly_chart(fig_pie_1)


    fig_pie_2=px.pie(ttype_group, names= "transaction_type",values="transaction_amount",
                    width=600,title="TRANSACTION AMOUNT",hole=0.5)
    st.plotly_chart(fig_pie_2)



def agg_user_plotwise(df,YEAR):
    ag_user_year=df[df["years"]==YEAR]
    ag_user_year.reset_index(drop=True, inplace=True)
    ag_user_year_g=pd.DataFrame(ag_user_year.groupby("brands")["transaction_count"].sum())
    ag_user_year_g.reset_index(inplace=True)
    fig_bar_1=px.bar(ag_user_year_g,x="brands",y="transaction_count",title=f"{YEAR} **BRAND AND TRANSACTION COUNT**",width=1000,color_discrete_sequence=px.colors.sequential.haline,hover_name="brands")
    st.plotly_chart(fig_bar_1)
    return ag_user_year


#agg user analysis
def agg_user_plot_2(df,QUARTER):
    ag_user_year_q=df[df["quarter"]==QUARTER]
    ag_user_year_q.reset_index(drop=True, inplace=True)
    ag_user_year_q_g=pd.DataFrame(ag_user_year_q.groupby("brands")["transaction_count"].sum())
    ag_user_year_q_g.reset_index(inplace=True)
    fig_bar_1=px.bar(ag_user_year_q_g,x="brands",y="transaction_count",title=f"{QUARTER} QUARTER BRAND AND TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="brands")
    st.plotly_chart(fig_bar_1)
    return ag_user_year_q


#agg user analysis--3
def agg_user_plot_3(df,STATE):
    auyqs=df[df["states"]==STATE]
    auyqs.reset_index(drop=True, inplace=True)
    fig_line_1=px.line(auyqs,x="brands",y="transaction_count",hover_name="brands",
                    title=f"{STATE.upper()} **BRAND TRANSACTION COUNT AND PERCENTAGE**",width=1000, markers=True)
    st.plotly_chart(fig_line_1)


#map_trans_type--correcrt
def agg_trans_typewise(df,STATE):
    tacy=df[df["states"]==STATE]
    tacy.reset_index(drop=True,inplace=True)
    tacy_group=tacy.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()
    tacy_group.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame= tacy_group, names= "transaction_type",values="transaction_count",
                        width=600,title="TRANSACTION COUNT",hole=0.5,color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame= tacy_group, names= "transaction_type",values="transaction_amount",
                        width=600,title="TRANSACTION AMOUNT",hole=0.5,color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_pie_2)


#map_trans_type--district--correcrt
def map_trans_districtwise(df, STATE):
    tacy = df[df["states"] == STATE]
    tacy.reset_index(drop=True, inplace=True)
    tacy_group = tacy.groupby("districts")[["transaction_count", "transaction_amount"]].sum()
    tacy_group.reset_index(inplace=True)
     
    col1,col2=st.columns(2)
    with col1: 
        fig_bar_1 = px.bar(tacy_group,x="transaction_amount", y="districts", orientation="h", title=f"{STATE.upper()} DISTRICT AND TRANSACTION AMOUNT",height=500,color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 =  px.bar(tacy_group,x="transaction_amount", y="districts", orientation="h", title=f"{STATE.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_2)


#map user plot1
def map_user_plot_1(df,YEAR):
    map_user_year=df[df["years"]==YEAR]
    map_user_year.reset_index(drop=True, inplace=True)

    map_user_year_g=map_user_year.groupby("states")[["registeredUser","appOpens"]].sum()
    map_user_year_g.reset_index(inplace=True)
    fig_line_1=px.line(map_user_year_g,x="states",y=["registeredUser","appOpens"],
                        title=f"{YEAR} YEAR REGISTERED-USER AND APP-OPENS**",width=1000,height=800, markers=True,color_discrete_sequence=px.colors.diverging.Spectral)
    st.plotly_chart(fig_line_1)
    return map_user_year


#map user plot2
def map_user_plot_2(df,QUARTER):
    map_user_q=df[df["quarter"]==QUARTER]
    map_user_q.reset_index(drop=True, inplace=True)

    map_user_q_g=map_user_q.groupby("states")[["registeredUser","appOpens"]].sum()
    map_user_q_g.reset_index(inplace=True)
    fig_line_1=px.line(map_user_q_g,x="states",y=["registeredUser","appOpens"],
                        title=f"{df['years'].min()} **{QUARTER} QUARTER REGISTERED-USER AND APP-OPENS**",width=1000,height=800, markers=True,color_discrete_sequence=px.colors.sequential.Inferno)
    st.plotly_chart(fig_line_1)
    return map_user_q
#3
def map_user_plot_3(df,STATE):
       map_user_q=df[df["states"]==STATE]
       map_user_q.reset_index(drop=True, inplace=True)
       col1,col2=st.columns(2)
       with col1:
            fig_mu_bar_1 = px.bar(map_user_q,x="registeredUser",y="districts",title="REGISTERED-USER", 
              orientation="h",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)       
            st.plotly_chart(fig_mu_bar_1)

       with col2:
            fig_mu_bar_2 = px.bar(map_user_q,x="appOpens",y="districts",title="APP-OPENS", 
              orientation="h",height=800,color_discrete_sequence=px.colors.sequential.Rainbow)       
            st.plotly_chart(fig_mu_bar_2)



def top_trans_plot1(df,STATE):
    top_ty = top_trans_tac_y[top_trans_tac_y["states"] == "Andaman & Nicobar"]
    top_ty.reset_index(drop=True, inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_top_t_bar_1 = px.bar(top_ty,x="quarter",y="transaction_amount",title="TRANSACTION AMOUNT BY QUARTER",hover_data=["pincodes"],height=600,width=600, 
            color="quarter",
            color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_top_t_bar_1)
    with col2:
        fig_top_t_bar_2 = px.bar(top_ty,x="quarter",y="transaction_count",title="TRANSACTION COUNT BY QUARTER",hover_data=["pincodes"],height=600,width=600, 
            color="quarter",
            color_discrete_sequence=px.colors.sequential.Purples)
        st.plotly_chart(fig_top_t_bar_2)


def top_user_plot_1(df,YEAR):
    top_user_year=df[df["years"]==YEAR]
    top_user_year.reset_index(drop=True, inplace=True)

    top_user_year_g=pd.DataFrame(top_user_year.groupby(["states","quarter"])["registeredusers"].sum())
    top_user_year_g.reset_index(inplace=True)
    fig_top_u_1=px.bar(top_user_year_g,x="states",y="registeredusers",title=f"{YEAR} REGISTERED-USERS",hover_name="states",color="quarter",width=800,height=1000,color_discrete_sequence=px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_u_1)
    return top_user_year


def top_user_plot_2(df,STATE): 
    top_user_ys=df[df["states"]==STATE]
    top_user_ys.reset_index(drop=True, inplace=True)
    fig_top_u_2=px.bar(top_user_ys,x="quarter",y="registeredusers",title=f"{STATE} REGISTERED-USER PINCODES AND QUARTER",width=600,height=800,hover_data="pincodes",color_continuous_scale=px.colors.sequential.Burgyl_r,color="registeredusers")
    st.plotly_chart(fig_top_u_2)
  
#sql querry1
def top_chart_trans_amt(change_table):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306")
    mycursor = mydatabase.cursor(buffered=True)
    #plot1 
    Q1=f'''SELECT states, sum(transaction_amount) as transaction_amount  FROM {change_table} group by states order by transaction_amount desc limit 10;'''
    
    mycursor.execute(Q1)
    table_1=mycursor.fetchall()
    mydatabase.commit()

    df1=pd.DataFrame(table_1,columns=("states","transaction_amount"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df1,x="states",y="transaction_amount",title="*** TOP 10 TRANSACTION AMOUNT ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot2 
    Q2= f'''SELECT states, sum(transaction_amount) as transaction_amount  FROM {change_table} group by states order by transaction_amount limit 10;'''
    
    mycursor.execute(Q2)
    table_2=mycursor.fetchall()
    mydatabase.commit()

    df2=pd.DataFrame(table_2,columns=("states","transaction_amount"))
    with col2:
        fig_amount_2=px.bar(df2,x="states",y="transaction_amount",title="*** BOTTOM 10 TRANSACTION AMOUNT ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #plot3  
    Q3=f'''SELECT states, avg(transaction_amount) as transaction_amount  FROM {change_table} group by states order by transaction_amount;'''
    
    mycursor.execute(Q3)
    table_3=mycursor.fetchall()
    mydatabase.commit()

    df3=pd.DataFrame(table_3,columns=("states","transaction_amount"))
    
    fig_amount_3=px.bar(df3,y="states",x="transaction_amount",title="*** AVERAGE OF 10 TRANSACTION AMOUNT ***",hover_name="states",orientation="h", color_discrete_sequence=px.colors.sequential.Blugrn_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql querry2
def top_chart_trans_count(change_table):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306")
    mycursor = mydatabase.cursor(buffered=True)
    #plot1 
    Q1=f'''SELECT states, sum(transaction_count) as transaction_count  FROM {change_table} group by states order by transaction_count desc limit 10;'''
    
    mycursor.execute(Q1)
    table_1=mycursor.fetchall()
    mydatabase.commit()

    df1=pd.DataFrame(table_1,columns=("states","transaction_count"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df1,x="states",y="transaction_count",title="*** TOP 10 TRANSACTION COUNT ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot2 
    Q2= f'''SELECT states, sum(transaction_count) as transaction_count  FROM {change_table} group by states order by transaction_count limit 10;'''
   
    mycursor.execute(Q2)
    table_2=mycursor.fetchall()
    mydatabase.commit()

    df2=pd.DataFrame(table_2,columns=("states","transaction_count"))
    
    with col2:
        fig_amount_2=px.bar(df2,x="states",y="transaction_count",title="*** BOTTOM 10 TRANSACTION COUNT ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #plot3  
    Q3=f'''SELECT states, avg(transaction_count) as transaction_count  FROM {change_table} group by states order by transaction_count;'''
    
    mycursor.execute(Q3)
    table_3=mycursor.fetchall()
    mydatabase.commit()

    df3=pd.DataFrame(table_3,columns=("states","transaction_count"))
    fig_amount_3=px.bar(df3,y="states",x="transaction_count",title="*** AVERAGE  TRANSACTION COUNT TOP 10 ***",hover_name="states",orientation="h", color_discrete_sequence=px.colors.sequential.Blugrn_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)



#sql querry3
def top_chart_register_user(change_table,STATE):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306")
    mycursor = mydatabase.cursor(buffered=True)
    #plot1 
    Q1=f'''SELECT districts, sum(registeredUser) as registeredUser FROM {change_table} WHERE states='{STATE}' GROUP BY districts order by registeredUser desc LIMIT 10;'''
    
    mycursor.execute(Q1)
    table_1=mycursor.fetchall()
    mydatabase.commit()

    df1=pd.DataFrame(table_1,columns=("districts","registeredUser"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df1,x="districts",y="registeredUser",title="*** TOP 10 OF REGISTERED USER ***",hover_name="districts", color_discrete_sequence=px.colors.sequential.Blugrn_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot2 
    Q2=f'''SELECT districts, sum(registeredUser) as registeredUser FROM {change_table} WHERE states='{STATE}' GROUP BY districts order by registeredUser LIMIT 10;'''
    
    mycursor.execute(Q2)
    table_2=mycursor.fetchall()
    mydatabase.commit()

    df2=pd.DataFrame(table_2,columns=("districts","registeredUser"))
    
    with col2:
        fig_amount=px.bar(df2,x="districts",y="registeredUser",title="*** BOTTOM 10 OF REGISTERED USER ***",hover_name="districts", color_discrete_sequence=px.colors.sequential.Blugrn_r,height=650,width=600)
        st.plotly_chart(fig_amount)
        
    #plot3 
    Q3=f'''SELECT districts, avg(registeredUser) as registeredUser FROM {change_table} WHERE states='{STATE}' GROUP BY districts order by registeredUser; '''
    
    mycursor.execute(Q3)
    table_3=mycursor.fetchall()
    mydatabase.commit()

    df3=pd.DataFrame(table_3,columns=("districts","registeredUser"))
    fig_amount=px.bar(df3,x="districts",y="registeredUser",title="***  AVERAGE OF REGISTERED USER ***",hover_name="districts", color_discrete_sequence=px.colors.sequential.Inferno,height=650,width=600)
    st.plotly_chart(fig_amount)


#sql querry4
def top_chart_app_opens(change_table,STATE):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306")
    mycursor = mydatabase.cursor(buffered=True)
    #plot1 
    Q1=f'''SELECT districts, sum(appOpens) as appOpens FROM {change_table} WHERE states='{STATE}' GROUP BY districts order by appOpens desc LIMIT 10;'''
    
    mycursor.execute(Q1)
    table_1=mycursor.fetchall()
    mydatabase.commit()

    df1=pd.DataFrame(table_1,columns=("districts","appOpens"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df1,x="districts",y="appOpens",title="*** TOP 10 OF APP-OPENS ***",hover_name="districts", color_discrete_sequence=px.colors.sequential.Cividis,height=650,width=600)
        st.plotly_chart(fig_amount)
    #plot2 
    Q2=f'''SELECT districts, sum(appOpens) as appOpens FROM {change_table} WHERE states='{STATE}' GROUP BY districts order by appOpens LIMIT 10;'''
    
    mycursor.execute(Q2)
    table_2=mycursor.fetchall()
    mydatabase.commit()

    df2=pd.DataFrame(table_2,columns=("districts","appOpens"))
    with col2:
        fig_amount=px.bar(df2,x="districts",y="appOpens",title="*** BOTTOM 10 OF APP-OPENS ***",hover_name="districts", color_discrete_sequence=px.colors.sequential.Cividis,height=650,width=600)
        st.plotly_chart(fig_amount)
    
    #plot3 
    Q3=f'''SELECT districts, avg(appOpens) as appOpens FROM {change_table} WHERE states='{STATE}' GROUP BY districts order by appOpens; '''
    
    mycursor.execute(Q3)
    table_3=mycursor.fetchall()
    mydatabase.commit()

    df3=pd.DataFrame(table_3,columns=("districts","appOpens"))
    fig_amount=px.bar(df3,x="districts",y="appOpens",title="***  AVERAGE OF APP-OPENS ***",hover_name="districts", color_discrete_sequence=px.colors.sequential.Cividis,height=650,width=600)
    st.plotly_chart(fig_amount)



#sql querry5
def top_chart_register_top_users(change_table):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306")
    mycursor = mydatabase.cursor(buffered=True)
    #plot1 
    Q1=f'''SELECT states, SUM(registeredUsers) as registeredUsers  FROM {change_table} GROUP BY states order by registeredUsers desc limit 10;'''
    
    mycursor.execute(Q1)
    table_1=mycursor.fetchall()
    mydatabase.commit()

    df1=pd.DataFrame(table_1,columns=("states","registeredUser"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df1,x="states",y="registeredUser",title="*** TOP 10 OF REGISTERED USER ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Viridis,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot2 
    Q2=f'''SELECT states, SUM(registeredUsers) as registeredUsers FROM {change_table} GROUP BY states order by registeredUsers limit 10;'''
    
    mycursor.execute(Q2)
    table_2=mycursor.fetchall()
    mydatabase.commit()

    df2=pd.DataFrame(table_2,columns=("states","registeredUsers"))
    with col2:
        fig_amount=px.bar(df2,x="states",y="registeredUsers",title="*** BOTTOM 10 OF REGISTERED USER ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Viridis,height=650,width=600)
        st.plotly_chart(fig_amount)
        
    #plot3 
    Q3=f'''SELECT states, avg(registeredUsers) as registeredUsers FROM {change_table} GROUP BY states order by registeredUsers limit 10; '''
    
    mycursor.execute(Q3)
    table_3=mycursor.fetchall()
    mydatabase.commit()

    df3=pd.DataFrame(table_3,columns=("states","registeredUsers"))
    fig_amount=px.bar(df3,x="states",y="registeredUsers",title="***  AVERAGE OF 10 REGISTERED USER ***",hover_name="states", color_discrete_sequence=px.colors.sequential.Viridis,height=650,width=600)
    st.plotly_chart(fig_amount)


#q8
def top_chart_trans_agg_type(change_table, STATE):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306"
    )
    mycursor = mydatabase.cursor(buffered=True)
    Q1 = f'''
        SELECT states, years, transaction_type, SUM(transaction_count) as total_transaction_count
        FROM {change_table}
        WHERE states = '{STATE}'
        GROUP BY states, years, transaction_type;
        '''
    mycursor.execute(Q1)
    table_1 = mycursor.fetchall()
    mydatabase.commit()
    df1 = pd.DataFrame(table_1, columns=["states", "years", "transaction_type", "transaction_count"])
    fig_amount = px.line(
                df1,
                x="years",
                y="transaction_count",
                title="***TRANSACTION COUNT OVER YEARS***",
                line_group="transaction_type",  
                color="transaction_type",  
                hover_name="transaction_type",  
                color_discrete_sequence=px.colors.qualitative.Vivid,  
                height=650,
                width=800)
    st.plotly_chart(fig_amount)

#q9
def top_chart_trans_agg_user_brand(change_table, STATE):
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306"
    )
    mycursor = mydatabase.cursor(buffered=True)
    
    Q1 = f'''
        SELECT states, years, brands, SUM(transaction_count) as total_transaction_count
        FROM {change_table}
        WHERE states = '{STATE}'
        GROUP BY states, years, brands
        ORDER BY total_transaction_count DESC
        LIMIT 10;
        '''
     
    mycursor.execute(Q1)
    
    table_1 = mycursor.fetchall()
    
    mydatabase.commit()
    
    df1 = pd.DataFrame(table_1, columns=["states", "years", "brands", "total_transaction_count"])
    
    fig_amount = px.pie(
            df1,
            values="total_transaction_count",
            names="brands",
            title=f"*** Total Transaction Count by Brand in {STATE} ***",
            hover_name="years",
            height=600,
            width=800
        )
    
    st.plotly_chart(fig_amount)

def top_chart_trans_top_pincode(change_table, STATE):#q10
    
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhuruvanth@29",
        database="pe",
        port="3306"
    )
    mycursor = mydatabase.cursor(buffered=True)
    q1 = f'''
        SELECT pincodes, SUM(transaction_count) as total_transaction_count, SUM(transaction_amount) as total_transaction_amount
        FROM {change_table}
        WHERE states = '{STATE}'
        GROUP BY pincodes
        ORDER BY total_transaction_count DESC
        LIMIT 10;
    '''
    mycursor.execute(q1)
    data = mycursor.fetchall()
    df = pd.DataFrame(data, columns=["pincodes", "total_transaction_count", "total_transaction_amount"])
    mycursor.close()
    mydatabase.close()
    fig = px.scatter(
        df,
        x="total_transaction_count",
        y="total_transaction_amount",
        color="pincodes",  
        hover_name="pincodes", 
        title=f"Scatter Plot of Total Transaction Count vs Amount for Top 10 Pincodes in {STATE}",
        labels={"total_transaction_count": "Total Transaction Count", "total_transaction_amount": "Total Transaction Amount"},
        height=600,
        width=800
    )
    st.plotly_chart(fig)
def create_marquee(text, color="#007bff"):
    st.markdown(
        f"""
        <style>
        .marquee {{
            width: 100%;
            overflow: hidden;
            white-space: nowrap;
            box-sizing: border-box;
            animation: marquee 10s linear infinite;
            color: {color};
        }}

        @keyframes marquee {{
            0%   {{ text-indent: 100% }}
            100% {{ text-indent: -100% }}
        }}
        </style>
        <div class="marquee">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# Streamlit application
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
select = option_menu("", ['ABOUT','INSIGHTS OF DATA','QUERIES ANALYSIS'],default_index=0,orientation="horizontal")


if select == "ABOUT":
    create_marquee("Welcome to PhonePe Data Visualization and Exploration! Experience the convenience and security of digital payments with PhonePe.", color="#33ff57")
    st.write('### :violet[PhonePe Pulse Data Visualization and Exploration :Overview]')
    st.write('''This project aims to visualize and explore data from PhonePe Pulse, providing insights into various metrics like transactions, user registrations, and app opens across different states, districts, and time periods. The project leverages Streamlit for interactive data exploration and Plotly for creating visually appealing charts. Project Structure Data Loading and Preparation Interactive Components with Streamlit Data Visualization with Plotly Deployment and Sharing''')
   
    st.download_button("Download APP","https://www.phonepe.com/app-download/")

  
    col3,col4=st.columns(2)
    with col3:
        st.image(Image.open(r"C:\Users\PERIYASAMY\OneDrive\Documents\images3.jpeg"),width=300)
    
        st.subheader("Basic Work Flow")
    
        st.image(Image.open(r"C:\Users\PERIYASAMY\OneDrive\Documents\IMG-20240630-WA0023.jpg"),width=400)
    create_marquee("DATA SCIENCE - GUVI ", color="#007bff")
    
elif select == "INSIGHTS OF DATA":
    tab1, tab2, tab3 = st.tabs(["PhonePe Aggregated Analysis", "PhonePe Map Analysis", "PhonePe Top Analysis"])
    create_marquee("DATA SCIENCE - GUVI", color="#ff5733")
    with tab1:
    
        with st.expander("PhonePe Aggregated Analysis"):
            method1 = st.radio("Select The Methods", ["Aggregated Transaction Analysis", "Aggregated User Analysis"])
            if method1 == "Aggregated Transaction Analysis":
                min_year = int(agg_trans["years"].min())
                max_year = int(agg_trans["years"].max())
                col1,col2= st.columns(2)
                with col1:
            
                    YEARS = st.slider("Select The Year", agg_trans["years"].min(), agg_trans["years"].max(), agg_trans["years"].min())
                agg_trans_tac_y= Trans_amt_year_wise(agg_trans, YEARS)

                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State",agg_trans_tac_y["states"].unique())
                agg_trans_typewise(agg_trans_tac_y, STATES)


                col1,col2=st.columns(2)
                with col1:
                    QUARTERS=st.slider("Select The Quarter",agg_trans_tac_y["quarter"].min(),agg_trans_tac_y["quarter"].max(),agg_trans_tac_y["quarter"].min())
                agg_trans_tac_y_q=Trans_amt_quarterwise(agg_trans_tac_y,QUARTERS)

                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State_Type",agg_trans_tac_y["states"].unique())
                agg_trans_typewise(agg_trans_tac_y_q, STATES)

            elif method1 == "Aggregated User Analysis":
                min_year = int(agg_trans["years"].min())
                max_year = int(agg_trans["years"].max())
                col1,col2= st.columns(2)
                with col1:
            
                    YEARS = st.slider("Select The Year", agg_user["years"].min(), agg_user["years"].max(), agg_user["years"].min())
                agg_user_y= agg_user_plotwise(agg_user, YEARS)

                col1,col2=st.columns(2)
                with col1:
                    QUARTERS=st.slider("Select The Quarter",agg_user_y["quarter"].min(),agg_user_y["quarter"].max(),agg_user_y["quarter"].min())
                agg_user_y_q=agg_user_plot_2(agg_user_y,QUARTERS)

     
    with tab2:
        with st.expander("PhonePe Map Analysis"):
            method2 = st.radio("Select The Methods", ["Map Transaction", "Map User"])
            if method2 == "Map Transaction":
                
                col1,col2= st.columns(2)
                with col1:
            
                    YEARS = st.slider("Select The Year Map Transaction", map_table_trans["years"].min(), map_table_trans["years"].max(), map_table_trans["years"].min())
                map_trans_tac_y=Trans_amt_year_wise(map_table_trans,YEARS)

                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State Map Transaction",map_trans_tac_y["states"].unique())
                map_trans_districtwise(map_trans_tac_y, STATES)

                col1,col2=st.columns(2)
                with col1:
                    QUARTERS=st.slider("Select The Quarter Map Transaction",map_trans_tac_y["quarter"].min(),map_trans_tac_y["quarter"].max(),map_trans_tac_y["quarter"].min())
                map_trans_tac_y_q=Trans_amt_quarterwise(map_trans_tac_y, QUARTERS)
                
                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State Map Transactions",map_trans_tac_y_q["states"].unique())
                map_trans_districtwise(map_trans_tac_y_q, STATES)

                
                
            elif method2 == "Map User":
                col1,col2= st.columns(2)
                with col1:
            
                    YEARS = st.slider("Select The Year Map User", map_table_user["years"].min(), map_table_user["years"].max(), map_table_user["years"].min())
                map_user_tac_y=map_user_plot_1(map_table_user,YEARS)

                col1,col2=st.columns(2)
                with col1:
                    QUARTERS=st.slider("Select The Quarter Map User",map_user_tac_y["quarter"].min(),map_user_tac_y["quarter"].max(),map_user_tac_y["quarter"].min())
                map_user_tac_y_q=map_user_plot_2(map_user_tac_y, QUARTERS)

                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State Map User Type",map_user_tac_y_q["states"].unique())
                map_user_plot_3(map_user_tac_y_q, STATES)
                
       
    with tab3:
        with st.expander("PhonePe Top Analysis"):
            method3 = st.radio("Select The Methods", ["Top Transaction", "Top User"])
            if method3 == "Top Transaction":
                col1,col2= st.columns(2)
                with col1:
            
                    YEARS = st.slider("Select The Year Top Transaction Year", top_table_trans["years"].min(), top_table_trans["years"].max(), top_table_trans["years"].min())
                top_trans_tac_y=Trans_amt_year_wise(top_table_trans,YEARS )

                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State Top Transaction state",top_trans_tac_y["states"].unique())
                top_trans_plot1(top_trans_tac_y,STATES)
                

                col1,col2=st.columns(2)
                with col1:
                    QUARTERS=st.slider("Select The Quarter Top",top_trans_tac_y["quarter"].min(),top_trans_tac_y["quarter"].max(),top_trans_tac_y["quarter"].min())
                top_trans_tac_y_q=Trans_amt_quarterwise(top_trans_tac_y,QUARTERS)
                
            elif method3 == "Top User":
                col1,col2= st.columns(2)
                with col1:
                    YEARS = st.slider("Select The Year Top Transaction Year",top_table_user["years"].min(),top_table_user["years"].max(), top_table_user["years"].min())
                top_user_y=top_user_plot_1(top_table_user,YEARS)

                col1,col2= st.columns(2)
                with col1:
                    STATES=st.selectbox("Select The State Top Transaction state",top_user_y["states"].unique())
                top_user_plot_2(top_user_y,STATES)
                

elif select == "QUERIES ANALYSIS":
    q=st.selectbox("Select the Questions",["1.Transaction Amount and Transaction Count of Aggregated Transaction Bar Plot",
                                           "2.Transaction Amount and Transaction Count of Map Transaction Bar Plot",
                                           "3.Transaction Amount and Transaction Count of Top Transaction Bar Plot",
                                           "4.Transaction Count of Aggregated User Bar Plot",
                                           "5.Registered user of Map User Bar Plot",
                                           "6.App-opens of Map User Bar Plot",
                                           "7.Registered user of Top User Bar Plot",
                                           "8.Transaction Count Over The Years Line plot",
                                           "9.Aggregated User Transaction Count Over The Years And Brands Using Pie Chart",
                                           "10.Scatter Plot of Total Transaction Count vs Amount for Top 10 Pincodes"])
    if q=="1.Transaction Amount and Transaction Count of Aggregated Transaction Bar Plot":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amt("agg_df")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("agg_df")

    elif q=="2.Transaction Amount and Transaction Count of Map Transaction Bar Plot":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amt("map_trans")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_trans")

    elif q=="3.Transaction Amount and Transaction Count of Top Transaction Bar Plot":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amt("top_trans")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_trans")    
        
    elif q=="4.Transaction Count of Aggregated User Bar Plot":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("agg_user_df2")    

    elif q=="5.Registered user of Map User Bar Plot":

        STATES= st.selectbox("Select the State",map_table_user["states"].unique())       
        st.subheader("REGISTERED USER")
        top_chart_register_user("map_user", STATES)
        
    elif q=="6.App-opens of Map User Bar Plot":
        
        STATES= st.selectbox("Select the State",map_table_user["states"].unique())       
        st.subheader("APP-OPENS")
        top_chart_app_opens("map_user", STATES)   

    elif q=="7.Registered user of Top User Bar Plot":
       
        st.subheader("REGISTERED USER")
        top_chart_register_top_users("top_user_df")    

    elif q=="8.Transaction Count Over The Years Line plot": 
        STATES= st.selectbox("Select the State",agg_trans["states"].unique())
        st.subheader("Transaction Type In States")
        top_chart_trans_agg_type("agg_df",STATES)

    elif q=="9.Aggregated User Transaction Count Over The Years And Brands Using Pie Chart": 
        STATES= st.selectbox("Select the State",agg_user["states"].unique())
        st.subheader("Aggregated User Brands In States")
        top_chart_trans_agg_user_brand("agg_user_df2",STATES )
    
    elif q=="10.Scatter Plot of Total Transaction Count vs Amount for Top 10 Pincodes": 
        STATES= st.selectbox("Select the State",top_table_trans["states"].unique())
        st.subheader("Top 10 Pincodes")
        top_chart_trans_top_pincode("top_trans", STATES)


        

    
                                                           
