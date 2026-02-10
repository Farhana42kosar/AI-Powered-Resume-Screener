import streamlit as st
import requests
import os   

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="AI Resume Intelligence", page_icon="📊", layout="wide")

st.title("🚀 AI Resume Intelligence System")
st.markdown("---")

# File Uploader
uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    
    with st.spinner('🤖 Analyzing resume...'):
        try:
            
            response = requests.post(f"{BASE_URL}/predict", files=files)
            
            if response.status_code == 200:
                data = response.json()
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Predicted Domain", data.get('predicted_domain', 'N/A'))
                
                with col_b:
                    conf = data.get('model_confidence', "0").replace('%', '')
                    st.metric("Model Confidence", f"{conf}%")
                
                with col_c:
                    ats_raw = data.get('ats_score', "0").replace('%', '')
                    ats_val = float(ats_raw)
                    st.metric("Overall ATS Score", f"{ats_val}%")

                st.write("### 📈 Match Progress")
                
                if ats_val >= 70:
                    st.success(f"Great match! Your resume scored {ats_val}%")
                elif ats_val >= 40:
                    st.warning(f"Moderate match. Your resume scored {ats_val}%")
                else:
                    st.error(f"Low match. Your resume scored {ats_val}%")
                
                st.progress(ats_val / 100)
                st.markdown("---")

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("🎯 Recommended Roles")
                    recs = data.get('job_recommendations', [])
                    if recs:
                        for job in recs:
                            with st.expander(f"**{job['role']}** - {job['match_percentage']}% Match"):
                                st.write("**Matched Skills:**")
                                skills = job.get('matched_skills', [])
                                if skills:
                                    st.write(" , ".join([f"`{s.upper()}`" for s in skills]))
                                else:
                                    st.write("No specific skills matched.")
                    else:
                        st.write("No recommendations available.")

                with col2:
                    st.subheader("📝 File Metadata")
                    st.write(f"**Filename:** `{data.get('filename')}`")
                    st.write(f"**Analysis Status:** Completed")
                    
                    with st.expander("View Raw JSON Data"):
                        st.json(data)

            else:
                st.error("Backend Error: Please check if your FastAPI server is working.")

        except Exception as e:
            st.error(f"Connection Error: {e}")

st.markdown("---")
st.caption("Resume Screener v2.0 | Powered by FastAPI")
