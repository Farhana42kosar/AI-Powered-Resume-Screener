
import re

# Comprehensive Job Profiles with variations for better matching
JOB_PROFILES = {
    "Full Stack Developer": [
        "react", "node", "javascript", "js", "mongodb", "express", "html", "css", 
        "typescript", "nextjs", "frontend", "backend", "fullstack", "sql"
    ],
    "Backend Developer": [
        "python", "django", "flask", "java", "spring", "microservices", 
        "docker", "kubernetes", "sql", "postgresql", "mysql", "api", "rest", "golang"
    ],
    "Frontend Developer": [
        "react", "vue", "angular", "javascript", "css", "tailwind", "bootstrap", 
        "figma", "sass", "frontend", "ui", "ux", "jquery"
    ],
    "AI/ML Engineer": [
        "python", "pytorch", "tensorflow", "keras", "scikit-learn", "numpy", 
        "pandas", "nlp", "computer vision", "machine learning", "deep learning", "ai"
    ],
    "Data Scientist": [
        "python", "r", "statistics", "analysis", "tableau", "power bi", 
        "visualization", "sql", "modeling", "data science"
    ],
   
    "HR": {
        "Recruiter": ["sourcing", "interviewing", "talent acquisition", "hiring", "ats"],
        "HR Manager": ["payroll", "employee relations", "compliance", "policy", "benefits"]
    },
    "ACCOUNTANT": {
        "Tax Accountant": ["gst", "income tax", "filing", "audit", "compliance"],
        "Financial Analyst": ["excel", "forecasting", "budgeting", "p&l", "reporting"]
    },
    "SALES": {
        "Sales Manager": ["revenue growth", "crm", "lead generation", "sales pipeline", "forecasting"],
        "Business Development": ["market research", "cold calling", "partnership", "client acquisition", "negotiation"],
        "Retail Associate": ["customer service", "inventory", "point of sale", "merchandising", "upselling"]
    },
    "ADVOCATE": {
        "Litigation Lawyer": ["courtroom", "legal research", "pleadings", "trials", "dispute resolution"],
        "Corporate Counsel": ["contracts", "compliance", "mergers", "intellectual property", "arbitration"],
        "Legal Assistant": ["documentation", "notary", "filing", "case management", "legal drafting"]
    },
    "FINANCE": {
        "Investment Analyst": ["portfolio", "equity", "asset management", "valuation", "market analysis"],
        "Risk Manager": ["mitigation", "credit risk", "compliance", "derivatives", "insurance"],
        "Wealth Manager": ["financial planning", "investments", "retirement", "estate planning", "banking"]
    }
    
}
def extract_skills_with_regex(text, skill_list):
    """Finds keywords regardless of case or surrounding punctuation."""
    found = []
    text = text.lower()
    for skill in skill_list:
        # This regex ensures we find the word 'js' but not inside 'just'
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    return found

def get_job_recommendations(resume_text):
    match_results = []

    for job_title, required_skills in JOB_PROFILES.items():
        found_skills = extract_skills_with_regex(resume_text, required_skills)
        
        # Calculation: (Found / Total) * 100
        match_percentage = (len(found_skills) / len(required_skills)) * 100
        
        match_results.append({
            "role": job_title,
            "match_percentage": round(match_percentage, 2),
            "matched_skills": found_skills
        })

    # Sort by highest match
    match_results = sorted(match_results, key=lambda x: x['match_score' if 'match_score' in x else 'match_percentage'], reverse=True)
    return match_results[:3]

def calculate_ats_score(resume_text, top_match_percentage):
    """Calculates ATS score based on formatting and skill density."""
    score = 0
    text = resume_text.lower()
    
    # 1. Structural Check (Does it have these sections?)
    sections = ["experience", "education", "skills", "projects", "contact", "summary", "languages", "certification"]
    section_count = sum(1 for section in sections if section in text)
    score += (section_count / len(sections)) * 40 # Max 40 points
            
    # 2. Skill Density Check
    # We take the best match percentage and give it a weight of 60%
    score += (top_match_percentage * 0.6)
    
    return round(min(score, 100), 2)