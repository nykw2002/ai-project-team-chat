import streamlit as st
import pandas as pd
import time
from PIL import Image
import base64
import PyPDF2
import io
import os

# Function to display PDF preview
def display_pdf(pdf_path):
    try:
        # Display PDF using an iframe
        st.write(f"PDF: {pdf_path.split('\\')[-1]}")
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64.b64encode(open(pdf_path, "rb").read()).decode()}" width="700" height="1000" type="application/pdf"></iframe>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")

# Function to create an animated colored text box
def animated_text_box(text, color, direction="left"):
    animation = "slide-in-left" if direction == "left" else "slide-in-right"
    unique_class = f"message-box-{direction}-{color.replace('#', '')}-{int(time.time() * 1000)}"
    st.markdown(
        f"""
        <style>
        @keyframes {animation} {{
            0% {{ transform: translateX({'-' if direction == 'left' else ''}100%); opacity: 0; }}
            100% {{ transform: translateX(0); opacity: 1; }}
        }}
        .{unique_class} {{
            background-color: {color}EE;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            animation: {animation} 0.5s ease-out;
            font-size: 18px;
        }}
        </style>
        <div class="{unique_class}">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to set a background image
def set_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        .stApp > header {{
            background-color: rgba(0,0,0,0.5);
        }}
        .stApp .block-container {{
            background-color: rgba(0,0,0,0.7);
            padding: 20px;
            border-radius: 10px;
        }}
        .streamlit-expanderHeader {{
            color: white !important;
            background-color: rgba(0,0,0,0.5) !important;
        }}
        .streamlit-expanderContent {{
            background-color: rgba(0,0,0,0.5) !important;
            color: white !important;
        }}
        p, h1, h2, h3, h4, h5, h6 {{
            color: white !important;
            font-size: 18px;
        }}
        .stTextInput > div > div > input {{
            font-size: 18px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background
set_background("C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\ai-artificial-intelligence-technology-microchip-background_951586-28864.jpg")

st.title("🤖 AI Project Team Chat")

# Sidebar
st.sidebar.title("🎨 Theme Customization")
st.sidebar.color_picker("Choose accent color", "#00BFFF")

st.sidebar.title("📚 Knowledge Base")
uploaded_files = st.sidebar.file_uploader("Add files to Knowledge Base", accept_multiple_files=True)
if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} file(s) added successfully!")
    for file in uploaded_files:
        st.sidebar.write(f"Added: {file.name}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.show_files = False

# User input
user_input = st.text_input("💬 Enter your message to the AI Project Team:", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.show_files = False  # Reset file display
    
    # Simulate AI team's response
    with st.spinner("Thinking..."):
        time.sleep(4)
    
    # AI team responses with different colors
    responses = [
        ("🧑‍💼 Project Manager", "Thank you for your input. I'll coordinate with the team to address your request.", "#1E88E5"),
        ("🧑‍🔬 AI Researcher", "Based on recent advancements, we can implement a transformer-based model for this task.", "#43A047"),
        ("👨‍💻 Software Developer", "I'll start working on a prototype using PyTorch. We should have a working model soon.", "#FDD835"),
        ("✍️ Technical Writer", "I'll begin drafting the documentation for our new model, including its architecture and usage instructions.", "#8E24AA"),
        ("🧑‍💼 Project Manager", "Excellent progress, team. Let's schedule a review meeting to discuss the prototype.", "#1E88E5"),
        ("🧑‍🔬 AI Researcher", "I've completed the initial analysis. The model shows promising results in early tests.", "#43A047"),
        ("👨‍💻 Software Developer", "The prototype is ready for testing. I've implemented the core functionalities as discussed.", "#FDD835"),
        ("✍️ Technical Writer", "The first draft of the documentation is complete. I'll need input from the team for technical details.", "#8E24AA"),
        ("🧑‍💼 Project Manager", "Great work, everyone. Let's prepare for a client presentation next week.", "#1E88E5"),
        ("🧑‍🔬 AI Researcher", "I've optimized the model further. We're seeing a 15% improvement in performance.", "#43A047"),
        ("👨‍💻 Software Developer", "I've addressed the feedback from testing. The model is now more robust and efficient.", "#FDD835")
    ]
    
    for i, (role, message, color) in enumerate(responses):
        with st.spinner("Thinking..."):
            time.sleep(2)
        animated_text_box(f"{role}: {message}", color, "left" if i % 2 == 0 else "right")
    
    # Final summary message
    with st.spinner("Generating summary..."):
        time.sleep(2)
    summary = """
    🤖 AI Assistant: Here's a summary of the team's progress:
    1. A transformer-based model has been implemented and optimized.
    2. The prototype is complete and has undergone initial testing.
    3. Documentation is drafted and awaiting final technical details.
    4. The team is preparing for a client presentation.
    5. Overall, the project is progressing well with notable performance improvements.
    """
    animated_text_box(summary, "#1C2833", "left")
    
    st.session_state.show_files = True

# Display file previews
if st.session_state.show_files:
    st.header("📊 Project Files")

    # Excel file preview
    st.subheader("Excel Data Preview")
    excel_path = "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\Solution_Prices_for_Different_Company_Sizes.csv"
    try:
        if excel_path.endswith('.csv'):
            df = pd.read_csv(excel_path)
        elif excel_path.endswith('.xlsx'):
            df = pd.read_excel(excel_path)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")
        
        # Convert all columns to string type to avoid Arrow serialization issues
        df = df.astype(str)
        
        # Use st.dataframe with styling
        st.dataframe(
            df.style
            .highlight_max(axis=0)
            .highlight_min(axis=0),
            height=300
        )
        
        # Show summary statistics
        st.write("Summary Statistics:")
        st.write(df.describe())
        
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        st.warning("Please make sure the file path is correct and the file is not corrupted.")

    # PDF files
    st.subheader("📄 PDF Reports")
    pdf_files = [
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\3.Declaratie-privind-eligibilitatea-societatii-in-vederea-acordarii-ajutorului-de-minimis.pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\AIPRO VISION S.R.L..pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\auction1.pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\auction2.pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\Licitatie.pdf"
    ]

    for i, pdf_path in enumerate(pdf_files, 1):
        with st.expander(f"PDF Report {i}"):
            display_pdf(pdf_path)

    # Image file
    st.subheader("📈 Data Visualization")
    image_path = "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\sales_graph.png"
    try:
        image = Image.open(image_path)
        st.image(image, caption="Data Visualization", use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")
        st.warning("Please make sure the image file path is correct.")