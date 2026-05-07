import streamlit as st
from datetime import date 
from database import add_expense, expense_table, get_expenses, total_expenses , today_expenses, week_expenses, month_expenses, delete_expense
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
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Today's Spending", f"€{today:.2f}")
with col2:
    st.metric("This Week's Spending", f"€{week:.2f}")
with col3:
    st.metric("This Month's Spending", f"€{month:.2f}")
with col4: 
    st.metric("Total Spending", f"€{total:.2f}")
    
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
    