import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("hostel.db", check_same_thread=False)
c = conn.cursor()

# Create Tables
c.execute("""CREATE TABLE IF NOT EXISTS members
             (id INTEGER PRIMARY KEY, name TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS meals
             (member TEXT, breakfast INTEGER, lunch INTEGER, dinner INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS expenses
             (category TEXT, amount REAL)""")

st.title("🏠 Hostel Mess Manager")

menu = st.sidebar.selectbox("Menu", ["Add Member", "Add Meal", "Add Expense", "Monthly Report"])

# Add Member
if menu == "Add Member":
    name = st.text_input("Member Name")
    if st.button("Add"):
        c.execute("INSERT INTO members (name) VALUES (?)", (name,))
        conn.commit()
        st.success("Member Added")

# Add Meal
elif menu == "Add Meal":
    members = pd.read_sql("SELECT * FROM members", conn)
    member = st.selectbox("Select Member", members['name'])
    b = st.number_input("Breakfast", 0)
    l = st.number_input("Lunch", 0)
    d = st.number_input("Dinner", 0)

    if st.button("Save Meal"):
        c.execute("INSERT INTO meals VALUES (?, ?, ?, ?)", (member, b, l, d))
        conn.commit()
        st.success("Meal Saved")

# Add Expense
elif menu == "Add Expense":
    category = st.text_input("Category")
    amount = st.number_input("Amount", 0.0)

    if st.button("Add Expense"):
        c.execute("INSERT INTO expenses VALUES (?, ?)", (category, amount))
        conn.commit()
        st.success("Expense Added")

# Monthly Report
elif menu == "Monthly Report":
    meals = pd.read_sql("SELECT * FROM meals", conn)
    expenses = pd.read_sql("SELECT * FROM expenses", conn)

    total_meals = meals[['breakfast','lunch','dinner']].sum().sum()
    total_expense = expenses['amount'].sum()

    if total_meals > 0:
        per_meal = total_expense / total_meals
    else:
        per_meal = 0

    st.write("Total Expense:", total_expense)
    st.write("Total Meals:", total_meals)
    st.write("Per Meal Cost:", round(per_meal,2))