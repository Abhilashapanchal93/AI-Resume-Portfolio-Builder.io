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
    "📊 AI Resume Optimizer"    
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
    st.subheader("🤖 ATS Resume Optimizer")
    st.markdown("Optimize your resume for ATS with AI-driven insights and personalized feedback!")

    # -------- INPUTS --------
    st.header("Job Description & Resume")

    jd_input = st.text_area(
        "Enter Job Description",
        placeholder="Paste the job description here...",
        height=180
    )

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:
        st.success("Resume uploaded successfully!")

    # -------- HELPER FUNCTIONS --------
    def run_text_response(prompt, title):
        if not uploaded_file or not jd_input:
            st.warning("Please upload resume and paste job description.")
            return

        with st.spinner("⏳ Processing..."):
            pdf_text = ExtractPDF(uploaded_file)
            response = SendRequest(jd_input, pdf_text, prompt)

        st.subheader(title)
        st.write(response)

    def run_pdf_generation(prompt, filename_prefix):
        if not uploaded_file or not jd_input:
            st.warning("Please upload resume and paste job description.")
            return

        with st.spinner("📄 Generating document..."):
            pdf_text = ExtractPDF(uploaded_file)
            optimized_text = SendRequest(jd_input, pdf_text, prompt)
            output_file = CreatePDF(optimized_text, filename_prefix)

        with open(output_file, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                f,
                file_name=output_file,
                mime="application/pdf"
            )

        st.success("Document generated successfully!")

    # -------- 7 TABS --------
    t1,t2,t3,t4,t5,t6,t7 = st.tabs([
        "📄JD Insights",
        "Skills Gap",
        "📊Match %",
        "ATS Check",
        "📝Resume Feedback",
        "Optimized Resume",
        "✉️Cover Letter"
    ])

    with t1:
        with st.spinner("⏳ Analyzing Job Description..."):
           # generate_response(prompt1)
            run_text_response(prompt1, "Job Description Insights")

    with t2:
        run_text_response(prompt2, "Skills Gap Analysis")

    with t3:
        run_text_response(prompt3, "Resume Match Percentage")

    with t4:
        run_text_response(prompt4, "ATS Compatibility Check")

    with t5:
        run_text_response(prompt5, "Professional Resume Feedback")

    with t6:
        run_pdf_generation(prompt6, "Optimized_Resume")

    with t7:
        run_pdf_generation(prompt7, "Cover_Letter")


