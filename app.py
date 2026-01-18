import streamlit as st
from processor import validate_data, draw_ats_standard, draw_modern_sidebar, draw_creative
from portfolio_generator import generate_portfolio
from prompts import *
from helper import ExtractPDF, SendRequest, CreatePDF

# page config
st.set_page_config(
    page_title="AI Resume Builder",
    layout="centered",
    page_icon="📄"
)

st.title("📄 AI Resume & Portfolio Builder")

# tabs
tab1, tab2, tab3 = st.tabs([
    "📝 Resume Builder",
    "🌐 Portfolio Builder",
    "📊 Ai resume Optimizer"
     
])

#Resume Builder
with tab1:
    st.subheader("AI Resume Builder")

    if "data_confirmed" not in st.session_state:
        st.session_state.data_confirmed = False

    @st.dialog("Verify Your Details")
    def preview_modal(data):
        st.write(f"**Name:** {data['name']}")
        st.write(f"**Email:** {data['email']}")
        st.write(f"**Phone:** {data['phone']}")
        st.write(f"**Profession:** {data['profession']}")

        st.divider()
        st.write("**Education:**", data["edu"])
        st.write("**Experience:**", data["exp"])
        st.write("**Skills:**", data["skills"])
        st.write("**Projects:**", data["project"])
        st.write("**Certificates:**", data["certificate"])

        if st.button("Confirm & Generate Resume"):
            st.session_state.data_confirmed = True
            st.rerun()

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        profession = st.text_input("Profession")
        edu = st.text_area("Education")
        exp = st.text_area("Experience")
        skills = st.text_input("Skills (comma-separated)")
        project = st.text_area("Projects")
        certificate = st.text_area("Certificates")

        submitted = st.form_submit_button("Preview & Verify")

    if submitted:
        valid, msg = validate_data(name, email, phone)
        if not valid:
            st.error(msg)
        else:
            st.session_state.resume_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "profession": profession,
                "edu": edu,
                "exp": exp,
                "skills": skills,
                "project": project,
                "certificate": certificate
            }
            preview_modal(st.session_state.resume_data)

    if st.session_state.data_confirmed:
        st.success("Resume Generated Successfully ✅")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("ATS Standard"):
                draw_ats_standard(st.session_state.resume_data, "resume.pdf")
                st.download_button("Download PDF", open("resume.pdf", "rb"))

        with col2:
            if st.button("Modern Sidebar"):
                draw_modern_sidebar(st.session_state.resume_data, "resume.pdf")
                st.download_button("Download PDF", open("resume.pdf", "rb"))

        with col3:
            if st.button("Creative Blue"):
                draw_creative(st.session_state.resume_data, "resume.pdf")
                st.download_button("Download PDF", open("resume.pdf", "rb"))

        st.info("💡 Your resume is ATS-friendly. For more designs:")

        st.markdown("""
        - https://www.canva.com/resumes/templates/
        - https://novoresume.com/resume-templates
        - https://resume.io/resume-templates
        - https://flowcv.com/
        """)
#Portfolio Generator
with tab2:
    st.subheader("🌐 Portfolio Generator")

    theme = st.radio(
        "Choose Portfolio Theme",
        ["Basic", "Modern", "Creative"],
        horizontal=True
    )

    if st.button("🚀 Generate Portfolio"):
        if "resume_data" not in st.session_state:
            st.warning("Please generate resume first.")
        else:
            portfolio_file = generate_portfolio(
                st.session_state.resume_data,
                theme=theme
            )

            with open(portfolio_file, "r", encoding="utf-8") as f:
                st.download_button(
                    "⬇ Download Portfolio Website",
                    f,
                    file_name="portfolio.html",
                    mime="text/html"
                )

            st.success("Portfolio generated successfully!")

    st.markdown("""
    **Free Portfolio Website Builders**
    - https://base44.com
    
    """)
    
#ATS Resume optimizer
with tab3:
    st.subheader("📊 ATS Resume optimizer")
    st.markdown("Optimize your resume for ATS with AI-driven insights and personalized feedback!")


    # Left Column - User Inputs (Job Description and Resume)
    with st.container():
        st.header("Job Description & Resume")
        jd_input = st.text_area(
            "Enter Job Description", 
            placeholder="Paste the job description here.", 
            key="text",
            height=150,
            help="Paste the job description for the position you're applying for."
        )
        
        uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"], label_visibility="collapsed")
        if uploaded_file:
            st.success("Resume uploaded successfully!")

    # Middle Section: Action Buttons
    st.header("AI-Generated Insights & Feedback")
    st.markdown(
        "<p style='font-size:14px; color:#777;'>Click on the buttons below to get actionable insights and recommendations.</p>",
        unsafe_allow_html=True
    )

    # Buttons to trigger actions
    with st.expander("Resume Analysis Options"):
        
        submit1 = st.button("Job Description Insights")
        submit2 = st.button("Skills Gap Analysis")
        submit3 = st.button("Resume Percentage Match")
        submit4 = st.button("ATS Compatibility Check")
        submit5 = st.button("Resume Feedback")
        submit6 = st.button("Generate Optimized Resume")
        submit7 = st.button("Generate Cover Letter")

    # Function to generate the response based on button clicked
    def generate_response(prompt):
        if uploaded_file is not None:
            # Extract text content from the uploaded PDF resume
            pdf_content = ExtractPDF(uploaded_file)
            
            # Send request to AI model with job description and resume content
            response = SendRequest(jd_input, pdf_content, prompt)
            
            # Display the response from AI
            st.subheader("Generated Response:")
            st.write(response)
        else:
            st.warning("Please upload a resume to proceed!")

    # Function to generate the optimized PDF based on button clicked
    def generate_pdf(prompt):
        if uploaded_file is not None:
            # Extract text content from the uploaded PDF resume
            pdf_content = ExtractPDF(uploaded_file)
            
            # Send request to AI model for optimization
            optimized_text = SendRequest(jd_input, pdf_content, prompt)
            
            # Generate the optimized PDF file
            input_filename = uploaded_file.name.split('.')[0]  # Get the original filename
            optimized_filename = CreatePDF(optimized_text, input_filename)
            
            if optimized_filename:
                with open(optimized_filename, "rb") as file:
                    st.download_button("Click Here to Download Generated File", file, file_name=optimized_filename)
            else: 
                st.error("There was an issue generating the optimized resume.")
        else:
            st.warning("Please upload a resume to proceed!")

    # Button Logic to trigger respective analysis
    if submit1:
        with st.spinner("⏳ Analyzing Job Description..."):
            generate_response(prompt1)

    elif submit2:
        with st.spinner("🔍 Performing Skills Gap Analysis..."):
            generate_response(prompt2)

    elif submit3:
        if uploaded_file:
            with st.spinner("📊 Calculating ATS Score..."):
              generate_response(prompt4)  
           

    elif submit4:
        with st.spinner("✅ Checking ATS Compatibility..."):
            generate_response(prompt4)

    elif submit5:
        with st.spinner("📝 Generating Resume Feedback..."):
            generate_response(prompt5)

    elif submit6:
        with st.spinner("📄 Generating Optimized Resume PDF..."):
            generate_pdf(prompt6)

    elif submit7:
        with st.spinner("✉️ Generating Cover Letter..."):
            generate_pdf(prompt7)




