import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="HR Chatbot", page_icon="🤖", layout="wide")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .employee-card {
        border: 1px solid #ddd;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
        color: #333333;
    }
    .chat-bubble {
        background: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 16px;
        line-height: 1.6;
        color: #000000; /* ensures text is visible in dark theme */
        font-weight: 400;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE & INSTRUCTIONS ---
st.title("🤖 HR Resource Query Chatbot")
st.write("Find employees quickly based on skills, experience, and availability.")
st.info("**Try:** _Find Python developers with 3+ years experience_")

# --- INPUT & FILTERS ---
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    query = st.text_input("Enter your query:")
with col2:
    filter_skill = st.selectbox("Filter by skill (optional):", ["None", "Python", "React", "AWS", "Docker"])
with col3:
    filter_availability = st.radio("Availability:", ["All", "Available Only"])

# --- SEARCH BUTTONS ---
search_btn = st.button("🔍 Search")
clear_btn = st.button("Clear")

if clear_btn:
    st.experimental_rerun()

if search_btn:
    if not query.strip():
        st.warning("Please enter a query to search employees.")
    else:
        with st.spinner("Searching employees..."):
            try:
                # Prepare query with filters
                final_query = query
                if filter_skill != "None":
                    final_query += f" with skill {filter_skill}"
                if filter_availability == "Available Only":
                    final_query += " who are available"

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"query": final_query},
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                # --- FORMATTED CHAT RESPONSE ---
                if "response" in data:
                    formatted_response = f"""
                    **Query:** {query}

                    **AI Recommendation:**  
                    {data['response']}
                    """
                    st.markdown(f"<div class='chat-bubble'>{formatted_response}</div>", unsafe_allow_html=True)
                else:
                    st.error("Unexpected response format from API.")
                    st.stop()

                # --- EMPLOYEE CARDS ---
                employees = data.get("results", [])
                if employees:
                    st.subheader("Matching Employees")
                    for emp in employees:
                        availability_color = "green" if emp["availability"].lower() == "available" else "red"
                        st.markdown(f"""
                        <div class="employee-card">
                            <h4>{emp['name']}</h4>
                            <p><b>Experience:</b> {emp['experience_years']} years</p>
                            <p><b>Skills:</b> {', '.join(emp['skills'])}</p>
                            <p><b>Projects:</b> {', '.join(emp['projects'])}</p>
                            <p><b>Availability:</b> 
                            <span style="color:{availability_color};font-weight:bold;">{emp['availability']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No employees matched your query.")
            except requests.exceptions.Timeout:
                st.error("The server took too long to respond. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {e}")
            except ValueError:
                st.error("Invalid response format from the backend.")
