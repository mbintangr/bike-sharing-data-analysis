import calendar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_user_type_df(df):
    user_type_df = df.agg({
        "casual": "sum",
        "registered": "sum"
    }).reset_index()

    user_type_df.rename(columns={
        "index": "user_type",
        0: "user_count"
    }, inplace=True)

    return user_type_df

def create_yearly_user_df(df):
    yearly_user_df = df.groupby(by="yr").agg({
        "cnt": "sum"
    }).reset_index() 
    return yearly_user_df

def create_seasonal_user_df(df):
    seasonal_user_df = df.groupby(by="season").cnt.mean().reset_index()
    return seasonal_user_df

def create_monthly_user_df(df):
    monthly_user_df = df.groupby(by="mnth").agg({
        "cnt": "sum"
    }).reset_index()
    return monthly_user_df

def create_daily_user_df(df):
    daily_user_df = round(df.groupby(by="weekday").cnt.mean().reset_index())
    return daily_user_df

def create_holiday_df(df):
    holiday_df = df.groupby(by="holiday").agg({
        "cnt": "mean"
    }).reset_index()
    return holiday_df

def create_working_day_df(df):
    working_day_df = df.groupby(by="workingday").agg({
        "cnt": "mean"
    }).reset_index()
    return working_day_df

def create_timegroup_user_df(df):
    timegroup_user_df = round(df.groupby(by="time_group").cnt.mean()).reset_index()
    return timegroup_user_df

def create_day_timegroup_user_df(df):
    day_timegroup_user_df = round(hour_df.groupby(by=["weekday", "time_group"]).cnt.mean()).reset_index()
    return day_timegroup_user_df

# Filter data
day_df = pd.read_csv(r"..\data\day.csv")
day_df['yr'] = day_df['yr'].apply(lambda x: "2011" if x == 0 else "2012")
day_df['mnth'] = day_df['mnth'].apply(lambda x: calendar.month_name[x])
day_df['season'] = day_df['season'].apply(lambda x: "Spring" if x == 1 else ("Summer" if x == 2 else ("Fall" if x == 3 else "Winter")))
day_df['holiday'] = day_df['holiday'].apply(lambda x: "Holiday" if x == 1 else "Non Holiday")
day_df['weekday'] = day_df['weekday'].apply(lambda x: calendar.day_name[(x-1)%7])
day_df['workingday'] = day_df['workingday'].apply(lambda x: "Working Day" if x == 1 else "Non Working Day")

hour_df = pd.read_csv(r"..\data\hour.csv")
hour_df['yr'] = hour_df['yr'].apply(lambda x: "2011" if x == 0 else "2012")
hour_df['mnth'] = hour_df['mnth'].apply(lambda x: calendar.month_name[x])
hour_df['season'] = hour_df['season'].apply(lambda x: "Spring" if x == 1 else ("Summer" if x == 2 else ("Fall" if x == 3 else "Winter")))
hour_df['holiday'] = hour_df['holiday'].apply(lambda x: "Holiday" if x == 1 else "Non Holiday")
hour_df['weekday'] = hour_df['weekday'].apply(lambda x: calendar.day_name[(x-1)%7])
hour_df['workingday'] = hour_df['workingday'].apply(lambda x: "Working Day" if x == 1 else "Non Working Day")
hour_df["time_group"] = hour_df["hr"].apply(lambda x: "Morning" if x >= 3 and x < 10 else ("Afternoon" if x >= 10 and x < 14 else ("Evening" if x >= 14 and x < 20 else "Night")))

min_date = pd.to_datetime(day_df["dteday"].min())
max_date = pd.to_datetime(day_df["dteday"].max())

with st.sidebar:
    st.header("Bike Sharing")
    st.image(r"..\bicycle.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

top_color = "#72BCD4"
other_color = "#D3D3D3"

st.header("Bike Sharing Data Dashboard")

tab1, tab2 = st.tabs(["Selected Time Data", "Full Data"])

with tab1:
    user_type_df = create_user_type_df(main_day_df)
    daily_user_df = create_daily_user_df(main_day_df)
    timegroup_user_df = create_timegroup_user_df(main_hour_df)
    st.header("Selected Time Data")
    st.subheader("Average Weather Condition")

    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = round(main_day_df["temp"].mean() * 47 - 8)
        formatted_temperature = f"{temperature} °C"
        st.metric("Temperature", formatted_temperature)
    with col2:
        atemperature = round(main_day_df["atemp"].mean() * 47 - 8)
        formatted_atemperature = f"{atemperature} °C"
        st.metric("Feels Like", formatted_atemperature)
    with col3:
        humidity = round(main_day_df["temp"].mean() * 100)
        formatted_humidity = f"{humidity}%"
        st.metric("Humidity", formatted_humidity)

    fig,ax = plt.subplots(figsize=(16,7))
    ax = sns.lineplot(data=main_day_df, x="dteday", y=round(main_day_df["temp"] * 47 - 8), color="#D3D3D3", linewidth=0.5, label="Temperature")
    ax = sns.lineplot(data=main_day_df, x="dteday", y=round(main_day_df["atemp"] * 47 - 8), color="#72BCD4", linewidth=0.5, label="Feels Like")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature")
    ax.set(xticklabels=[])
    st.pyplot(fig)

    st.subheader("Casual User and Registered User Comparison")

    col1, col2 = st.columns(2)

    with col1:
        fig,ax = plt.subplots()
        ax.pie(user_type_df['user_count'], labels=user_type_df['user_type'], autopct='%1.1f%%', explode=(0, 0.07), colors=["#72BCD4", "#D3D3D3"])
        ax.set_title("Casual User vs Registered User")
        st.pyplot(fig)

    with col2:
        casualUser = user_type_df.loc[user_type_df['user_type'] == 'casual', 'user_count'].values[0]
        registeredUser = user_type_df.loc[user_type_df["user_type"] == "registered", "user_count"].values[0]
        totalUser = casualUser + registeredUser
        st.metric("Total Users:", totalUser)
        st.metric("Number of Casual Users:", casualUser)
        st.metric("Number of Registered Users:", registeredUser)


    st.subheader("Daily Average Number of User")
    max_count = daily_user_df["cnt"].max()

    colors = [top_color if count == max_count else other_color for count in daily_user_df["cnt"]]

    fig, ax = plt.subplots()
    ax = sns.barplot(data=daily_user_df, x="weekday", y="cnt", palette=colors)
    ax.set_xlabel(None)
    ax.set_ylabel("Average Number of User")
    st.pyplot(fig)

    st.subheader("Average Number of User based on Time")
    max_count = timegroup_user_df["cnt"].max()

    colors = [top_color if count == max_count else other_color for count in timegroup_user_df["cnt"]]

    fig, ax = plt.subplots()
    ax = sns.barplot(data=timegroup_user_df, x="time_group", y="cnt", palette=colors)
    ax.set_xlabel(None)
    ax.set_ylabel("Average Number of User")
    st.pyplot(fig)

with tab2:
    user_type_df = create_user_type_df(day_df)
    yearly_user_df = create_yearly_user_df(day_df)
    seasonal_user_df = create_seasonal_user_df(day_df)
    monthly_user_df = create_monthly_user_df(day_df)
    daily_user_df = create_daily_user_df(day_df)
    holiday_df = create_holiday_df(day_df)
    working_day_df = create_working_day_df(day_df)
    timegroup_user_df = create_timegroup_user_df(hour_df)
    day_timegroup_user_df = create_day_timegroup_user_df(hour_df)

    st.header("Full Data")

    # Weather
    st.subheader("Average Weather Condition")
    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = round(day_df["temp"].mean() * 47 - 8)
        formatted_temperature = f"{temperature} °C"
        st.metric("Temperature", formatted_temperature)
    with col2:
        atemperature = round(day_df["atemp"].mean() * 47 - 8)
        formatted_atemperature = f"{atemperature} °C"
        st.metric("Feels Like", formatted_atemperature)
    with col3:
        humidity = round(day_df["temp"].mean() * 100)
        formatted_humidity = f"{humidity}%"
        st.metric("Humidity", formatted_humidity)
    
    fig,ax = plt.subplots(figsize=(16,7))
    ax = sns.lineplot(data=main_day_df, x="dteday", y=round(main_day_df["temp"] * 47 - 8), color="#D3D3D3", linewidth=0.5, label="Temperature")
    ax = sns.lineplot(data=main_day_df, x="dteday", y=round(main_day_df["atemp"] * 47 - 8), color="#72BCD4", linewidth=0.5, label="Feels Like")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature")
    ax.set(xticklabels=[])
    st.pyplot(fig)

    # Q1
    st.subheader("Casual User and Registered User Comparison")

    col1, col2 = st.columns(2)

    with col1:
        fig,ax = plt.subplots()
        ax.pie(user_type_df['user_count'], labels=user_type_df['user_type'], autopct='%1.1f%%', explode=(0, 0.07), colors=["#72BCD4", "#D3D3D3"])
        ax.set_title("Casual User vs Registered User")
        st.pyplot(fig)

    with col2:
        casualUser = user_type_df.loc[user_type_df['user_type'] == 'casual', 'user_count'].values[0]
        registeredUser = user_type_df.loc[user_type_df["user_type"] == "registered", "user_count"].values[0]
        totalUser = casualUser + registeredUser
        st.metric("Total Users:", totalUser)
        st.metric("Number of Casual Users:", casualUser)
        st.metric("Number of Registered Users:", registeredUser)

    # Q2
    st.subheader("2011 vs 2012 User Comparison")
    fig, ax = plt.subplots()
    sns.barplot(data=yearly_user_df, x="yr", y="cnt", hue="yr", palette=["#D3D3D3", "#72BCD4"], ax=ax)
    ax.set_title("Number of users in 2011 and 2012")
    ax.set_yticks(yearly_user_df["cnt"])
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Users")
    st.pyplot(fig)

    # Q3
    st.subheader("Number of User Based on Season")

    max_count = seasonal_user_df["cnt"].max()
    colors = [top_color if count == max_count else other_color for count in seasonal_user_df["cnt"]]
    
    fig, ax = plt.subplots()
    sns.barplot(data=seasonal_user_df, x="season", y="cnt", hue="season", palette=colors, ax=ax)
    ax.set_title("Seasonal User Report")
    ax.set_yticks(seasonal_user_df.cnt)
    ax.set_xlabel(None)
    ax.set_ylabel("Number of User")
    st.pyplot(fig)

    # Q4
    st.subheader("Best and Worst Monthly User Average")

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(20,8))

    sns.barplot(x="mnth", y="cnt", data=monthly_user_df.sort_values(by="cnt", ascending=False).head(5), palette=colors, hue="mnth", ax=ax[0])
    ax[0].set_ylabel("Number of User")
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Month", loc="center", fontsize=15)
    ax[0].tick_params(axis ='y', labelsize=12)
    
    sns.barplot(x="mnth", y="cnt", data=monthly_user_df.sort_values(by="cnt", ascending=True).head(5), palette=colors, hue="mnth", ax=ax[1])
    ax[1].set_ylabel("Number of User")
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Month", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)
    
    st.pyplot(fig)

    # Q5
    st.subheader("Daily Average Number of User")
    max_count = daily_user_df["cnt"].max()

    colors = [top_color if count == max_count else other_color for count in daily_user_df["cnt"]]

    fig, ax = plt.subplots()
    ax = sns.barplot(data=daily_user_df, x="weekday", y="cnt", palette=colors)
    ax.set_xlabel(None)
    ax.set_ylabel("Average Number of User")
    st.pyplot(fig)

    # Q6
    st.subheader("Holiday and Non-holiday User Comparison")

    max_count = holiday_df["cnt"].max()

    colors = [top_color if count == max_count else other_color for count in holiday_df["cnt"]]

    fig,ax = plt.subplots()
    ax = sns.barplot(data=holiday_df, x="holiday", y="cnt", palette=colors, hue="holiday")
    ax.set_title("Holiday vs Non Holiday User")
    ax.set_xlabel(None)
    ax.set_ylabel("Number of User")

    st.pyplot(fig)

    # Q7
    st.subheader("Working day and non Working day User Comparison")

    max_count = working_day_df["cnt"].max()

    colors = [top_color if count == max_count else other_color for count in working_day_df["cnt"]]

    fig,ax = plt.subplots()
    ax = sns.barplot(data=working_day_df, x="workingday", y="cnt", palette=colors, hue="workingday")
    ax.set_title("Working Day vs Non Working Day")
    ax.set_xlabel(None)
    ax.set_ylabel("Number of User")

    st.pyplot(fig)
    
    # Q8
    st.subheader("Average Number of User based on Time")
    max_count = timegroup_user_df["cnt"].max()

    colors = [top_color if count == max_count else other_color for count in timegroup_user_df["cnt"]]

    fig, ax = plt.subplots()
    ax = sns.barplot(data=timegroup_user_df, x="time_group", y="cnt", palette=colors)
    ax.set_xlabel(None)
    ax.set_ylabel("Average Number of User")
    st.pyplot(fig)

    # Additional Analysis
    st.subheader("Average user per day per time group")

    fig,ax = plt.subplots()
    ax = sns.barplot(data=day_timegroup_user_df, x="weekday", y="cnt", hue="time_group", color="#72BCD4")
    ax.set_xlabel(None)
    ax.set_ylabel("Average Number of User")
    st.pyplot(fig)