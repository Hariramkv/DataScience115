import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

def hash_pin(pin):
    return hashlib.sha256(str(pin).encode()).hexdigest()

INITIAL_ACCOUNTS = {
    "12345": {"pin": hash_pin("1234"), "balance": 1000.0, "transactions": []},
    "67890": {"pin": hash_pin("5678"), "balance": 5000.0, "transactions": []}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_account" not in st.session_state:
    st.session_state.current_account = None
if "accounts" not in st.session_state:
    st.session_state.accounts = INITIAL_ACCOUNTS.copy()

st.title("🏧 ATM Application")

def login():
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Login"):
        if acc in st.session_state.accounts and \
           st.session_state.accounts[acc]["pin"] == hash_pin(pin):
            st.session_state.logged_in = True
            st.session_state.current_account = acc
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Wrong account or PIN")

def dashboard():
    acc = st.session_state.current_account
    balance = st.session_state.accounts[acc]["balance"]

    st.sidebar.write(f"Account: {acc}")
    st.sidebar.write(f"Balance: ₹{balance}")

    choice = st.sidebar.radio(
        "Menu",
        ["Balance", "Deposit", "Withdraw", "Transactions", "Logout"]
    )

    if choice == "Balance":
        st.info(f"Balance: ₹{balance}")

    if choice == "Deposit":
        amt = st.number_input("Amount", min_value=1.0)
        if st.button("Deposit"):
            st.session_state.accounts[acc]["balance"] += amt
            st.session_state.accounts[acc]["transactions"].append(
                ("Deposit", amt, datetime.now())
            )
            st.success("Deposit successful")

    if choice == "Withdraw":
        amt = st.number_input("Amount", min_value=1.0)
        pin = st.text_input("Confirm PIN", type="password")
        if st.button("Withdraw"):
            if hash_pin(pin) == st.session_state.accounts[acc]["pin"]:
                if balance >= amt:
                    st.session_state.accounts[acc]["balance"] -= amt
                    st.success("Withdraw successful")
                else:
                    st.error("Not enough balance")
            else:
                st.error("Wrong PIN")

    if choice == "Transactions":
        st.write(st.session_state.accounts[acc]["transactions"])

    if choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_account = None
        st.rerun()

if not st.session_state.logged_in:
    login()
else:
    dashboard()
