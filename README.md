# AI Trip Planner

## Overview
A web application that is designed to help users plan their trips with ease using the power of AI, specifically leveraging the capabilities of Gemini. Users can input their travel preferences, and the app generates a detailed trip itinerary including destination, dates, activities, and accommodation options. The application allows users to save their planned trips and provide feedback on generated plans.

## Key Features
Plan Generation: Automatically generate travel plans based on user input.
Database Integration: Save and retrieve trip details and user feedback using a PostgreSQL database.
User Feedback: Users can rate and comment on their planned trips, allowing for continuous improvement of the planning AI.

## First time setup
- Create virtual environment
python -m venv venv
- Activate virtual environment
source venv/bin/activate
- Install dependencies
pip install -r requirements.txt
- Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run app.py
## What I Learned
### I gained insights and skills:

- API Integration: Learned to integrate the Google Gemini API for generating content based on user prompts.
- Database Management: Enhanced my understanding of PostgreSQL for handling data persistence with user-generated content and feedback.
- Streamlit Development: Developed skills in creating interactive web applications using Streamlit.

### Challenges and Solutions:
- Database Connectivity Issues: Initially struggled with establishing a reliable connection to PostgreSQL. Resolved by implementing context managers to ensure that database connections are properly opened and closed.
- Handling API Errors: Encountered and resolved errors related to API permissions and data handling, which improved my debugging skills and understanding of error management in Python.
- User Interface Design: Faced challenges in creating a user-friendly interface. Overcame this by iteratively testing and refining the UI based on user feedback.

## Questions
Do you have suggestions for additional features or improvements in the AI Trip Planner? Feel free to comment and let me know.