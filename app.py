import os
import psycopg2
from contextlib import closing
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Database connection
def connect_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# Insert trip to the database
def insert_trip(destination, departure_date, return_date, activities, accommodation, plan_details):
    sql = """INSERT INTO trips (destination, departure_date, return_date, activities, accommodation, plan_details)
             VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute(sql, (destination, departure_date, return_date, activities, accommodation, plan_details))
        trip_id = cur.fetchone()[0]
        conn.commit()
    return trip_id

# Insert feedback for a trip
def insert_feedback(trip_id, rating, comments):
    sql = """INSERT INTO feedback (trip_id, rating, comments)
             VALUES (%s, %s, %s);"""
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute(sql, (trip_id, rating, comments))
        conn.commit()

# Fetch trips and feedback from the database
def fetch_trips():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM trips")
        trips = cur.fetchall()
    return trips

def fetch_feedback(trip_id):
    sql = """SELECT rating, comments FROM feedback WHERE trip_id = %s;"""
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute(sql, (trip_id,))
        feedback = cur.fetchall()
    return feedback

# Generate content using Gemini API
def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI for trip planning
st.title("🏝️ AI Travel Planning")

prompt_template = """
You are an expert at planning overseas trips.

Please take the users request and plan a comprehensive trip for them.

Please include the following details:
- The destination
- The duration of the trip
- The departure and return dates
- The flight options
- The activities that will be done
- The accommodation options

The user's request is:
{prompt}
"""

# User inputs
destination = st.text_input("Destination")
departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")
activities = st.text_area("Activities you're interested in")
accommodation_preference = st.selectbox("Accommodation Preference", ["Hotel", "Hostel", "Apartment", "Other"])

if st.button("Give me a plan!"):
    full_request = f"Destination: {destination}, Departure Date: {departure_date}, Return Date: {return_date}, Activities: {activities}, Accommodation: {accommodation_preference}"
    prompt = prompt_template.format(prompt=full_request)
    reply = generate_content(prompt)
    st.write(reply)
    trip_id = insert_trip(destination, departure_date, return_date, activities, accommodation_preference, reply)
    st.success("Trip saved successfully!")

    # Collect feedback
    if st.button("Save Feedback"):
        rating = st.slider("Rate your plan", 1, 5, 3)
        comments = st.text_area("Any comments on the plan?")
        insert_feedback(trip_id, rating, comments)
        st.success("Feedback saved successfully!")

# Display saved trips from the database
if st.checkbox("Show Saved Trips"):
    st.header("Saved Trips")
    trips = fetch_trips()
    if trips:
        for trip in trips:
            st.subheader(f"Trip to {trip[1]}")
            st.text(f"Dates: {trip[2]} to {trip[3]}")
            st.text(f"Activities: {trip[4]}")
            st.text(f"Accommodation: {trip[5]}")
            st.text(f"Plan Details: {trip[6]}")
            feedback = fetch_feedback(trip[0])
            if feedback:
                st.text(f"Rating: {feedback[0][0]}, Comments: {feedback[0][1]}")
            else:
                st.text("No feedback yet.")
    else:
        st.error("No saved trips found.")
