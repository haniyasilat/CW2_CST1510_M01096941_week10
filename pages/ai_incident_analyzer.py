import streamlit as st
from openai import OpenAI
from week08.app.data.incidents import get_all_incidents

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🔍 AI Incident Analyzer")

incidents_df = get_all_incidents()

if not incidents_df.empty:
    incidents = incidents_df.to_dict('records')
    
    incident_options = []
    for idx, inc in enumerate(incidents):
        incident_id = inc.get('id') or inc.get('ID') or inc.get('incident_id') or str(idx + 1)
        incident_type = inc.get('incident_type', 'Unknown')
        severity = inc.get('severity', 'Unknown')
        incident_options.append(f"{incident_id}: {incident_type} - {severity}")
    
    selected_idx = st.selectbox(
        "Select incident to analyze:",
        range(len(incidents)),
        format_func=lambda i: incident_options[i]
    )
    
    incident = incidents[selected_idx]
    
    st.subheader("📋 Incident Details")
    for key, value in incident.items():
        if value and key not in ['', None]:
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    if st.button("🤖 Analyze with AI", type="primary"):
        with st.spinner("AI analyzing incident..."):
            incident_type = incident.get('incident_type', 'Unknown')
            severity = incident.get('severity', 'Unknown')
            description = incident.get('description', 'No description available')
            status = incident.get('status', 'Unknown')
            
            analysis_prompt = f"""Analyze this cybersecurity incident:

Type: {incident_type}
Severity: {severity}
Description: {description}
Status: {status}

Provide:
1. Root cause analysis
2. Immediate actions needed
3. Long-term prevention measures
4. Risk assessment"""
            
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert."},
                        {"role": "user", "content": analysis_prompt}
                    ]
                )
                
                st.subheader("🧠 AI Analysis")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"AI Analysis failed: {e}")
    