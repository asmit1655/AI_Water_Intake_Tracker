import streamlit as st
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import log_intake,get_intake_history
import pandas as pd

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False
    
if not st.session_state.tracker_started:
    st.write("Welcome to the Ai Water Intake Tracker! 🤖💧")
    st.markdown("An intelligent hydration tracking system powered by AI to help you stay healthy, hydrated, and on track with your wellness goals.")
    if st.button("Start Tracking 🕒"):
        st.session_state.tracker_started = True
        st.rerun()

else:
    st.title("💧 AI WATER TRACKER DASHBOARD")
    st.sidebar.text("Log your water intake")
    user_id=st.sidebar.text_input("USER_id")
    intake_ml=st.sidebar.number_input("Water Intake (ml)", min_value=0, step=100)
    
    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id,intake_ml)
            agent = WaterIntakeAgent()
            feedback=agent.analyze_input(intake_ml)
            st.success(f"Logged {intake_ml}ml for {user_id}")
            
            st.write(f"🤖 {feedback}")
    
    st.header("Water Intake History")
    
    if user_id:
        history=get_intake_history(user_id)
        if history:
            date=[datetime.strptime(row[1],"%Y-%m-%d") for row in history]
            values=[row[0] for row in history]
            
            df=pd.DataFrame({"Dates":date,"Water Intake(ml)":values})
            
            st.dataframe(df)
            
            st.line_chart(df,x="Dates",y="Water Intake(ml)")
        else:
            st.warning("⚠️ No Water Intake history found for this user.")