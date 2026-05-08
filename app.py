import streamlit as st
from datetime import date 
from database import add_expense, expense_table, get_expenses, total_expenses , today_expenses, week_expenses, month_expenses, delete_expense, add_income, get_income, total_income, month_income, delete_income, get_category_summary, get_daily_spending_summary
import pandas as pd

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide"
)

expense_table()
st.title("Expense Tracker")
st.write("Samarth's personal expense tracker. ")


today = today_expenses()
week = week_expenses()
month = month_expenses()
total = total_expenses()
income = total_income()
month_income = month_income()

remaining_money = month_income - month
if month_income > 0:
    savings_percentage = (remaining_money / month_income) * 100
else:
    savings_percentage = 0

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

with col1:
    st.metric("This Month's Income", f"€{month_income:.2f}")
with col2:
    st.metric("This Month's Spending", f"€{month:.2f}")
with col3:
    st.metric("Remaining Money", f"€{remaining_money:.2f}")
with col4: 
    st.metric("Savings Percentage", f"{savings_percentage:.2f}%")
with col5:
    st.metric("Today's Spending", f"€{today:.2f}")
with col6:
    st.metric("This Week's Spending", f"€{week:.2f}")
with col7:
    st.metric("Total Income", f"€{income:.2f}")
with col8:
    st.metric("Total Spending", f"€{total:.2f}")
    
st.subheader("Category-wise Summary for the Current Month")
category_summary = get_category_summary()
if category_summary:
    category_df = pd.DataFrame(
        category_summary,
        columns = ["Category", "Total Amount"]
    )
    st.dataframe(category_df, use_container_width=True)
    st.bar_chart(category_df.set_index("Category"))
else:
    st.info("No expenses found for the current month. Please add some expenses to see the category-wise summary.")

st.subheader("Daily Spending Summary for the Current Month")
daily_summary = get_daily_spending_summary()
if daily_summary:
    daily_df = pd.DataFrame(
        daily_summary,
        columns = ["Date", "Total Amount"]
    )
    st.dataframe(daily_df, use_container_width=True)
    st.line_chart(daily_df.set_index("Date"))
else:
    st.info("No expenses found for the current month. Please add some expenses to see the daily spending summary.")

st.subheader("Add a New Expense")
with st.form("Expense Form"):
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    category = st.selectbox(
        "Category",
        ["Food", "Groceries(Other than Lidl)", "Transport", "Rent", "Entertainment", "LLMs", "Gym", "Health Insurance", "Lidl", "Party", "Sim", "Radio Tax", "Other"]
    )
    note = st.text_input("Note (optional)")
    date = st.date_input("Date", value=date.today())
    submit = st.form_submit_button("Add Expense")
    if submit:
        if amount <=0:
            st.error("Amount must be greater than zero.")
        else:
            add_expense(amount, category, note, date)
            st.success("Expense added successfully.")
            st.rerun()
            

st.subheader("Add Income")
with st.form("Income Form"):
    amount = st.number_input("Amount", min_value = 0.0, step=0.01)
    source = st.selectbox(
        "Source",
        ["Hiwi Salary", "Werkstudent Salary", "Freelance", "Friend Borrow", "Refund", "Other"]
    )
    note = st.text_input("Note (optional)")
    date = st.date_input("Date", value=date.today())
    submit = st.form_submit_button("Add Income")
    if submit:
        if amount <=0:
            st.error("Amount must be greater than zero.")
        else:
            add_income(amount, source, note, date)
            st.success("Income added successfully.")
            st.rerun()

st.subheader("All Expenses")
expenses = get_expenses()
if expenses:
    df = pd.DataFrame(
        expenses,
        columns=["ID", "Amount", "Category", "Note", "Date"]
    )
    st.dataframe(df, use_container_width=True)
    st.subheader("Delete Expense")
    expense_id = df["ID"].tolist()
    selected_id = st.selectbox("Select Expense ID to delete", expense_id)
    
    if st.button("Delete Expense"):
        delete_expense(selected_id)
        st.success(f"Expense with ID {selected_id} deleted successfully.")
        st.rerun()
else:
    st.info("No expenses found. Please add some expenses to track your spending.")
    
st.subheader("All Income")
income = get_income()
if income:
    df_income = pd.DataFrame(
        income,
        columns=["ID", "Amount", "Source", "Note", "Date"]
    )
    st.dataframe(df_income, use_container_width=True)
    st.subheader("Delete Income")
    income_id = df_income["ID"].tolist()
    selected_id = st.selectbox("Select Income ID to delete", income_id)

    if st.button("Delete Income"):
        delete_income(selected_id)
        st.success(f"Income with ID {selected_id} deleted successfully.")
        st.rerun()
else:
    st.info("No income found. Please add some income to track your earnings.")