import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Expert Assistant", page_icon="🤖")
#define three asisstants
assistants = {
    "Cybersecurity": {
        "prompt": "You are a cybersecurity expert. "
        "Analyze incidents, threats, and vulnerabilities. Provide technical guidance using MITRE ATT&CK, CVE references. Prioritize actionable recommendations.",
    },
    "Data Science": {
        "prompt": "You are a data science expert. "
        "Help with data analysis, visualization, statistical methods, and machine learning. Explain concepts clearly and suggest appropriate techniques.",
    },
    "IT Operations": {
        "prompt": "You are an IT operations expert."
        " Help troubleshoot issues, optimize systems, manage tasks, and provide infrastructure guidance. Focus on practical solutions.",
    }
}
#here i initialized session state for selected assistant
if "selected" not in st.session_state:
    st.session_state.selected = "Cybersecurity"

if "messages" not in st.session_state:
    st.session_state.messages = {}
#created chat history for each assistant
for name in assistants.keys():
    if name not in st.session_state.messages:
        st.session_state.messages[name] = [
            {"role": "system", "content": assistants[name]["prompt"]}
        ]
#sidebar for selecting assistant
with st.sidebar:
    st.title("Assistant Selector")
    #with help of radi buttons to chose assistant
    selected = st.radio(
        "Choose Expert:",
        list(assistants.keys()),
        index=list(assistants.keys()).index(st.session_state.selected)
    )
    #update selected assistant if user choses different one
    if selected != st.session_state.selected:
        st.session_state.selected = selected
        st.rerun()
    
    st.divider()
    #counts and displays number of user messages 
    current_messages = st.session_state.messages[st.session_state.selected]
    user_messages = [m for m in current_messages if m["role"] == "user"]
    message_count = len(user_messages)
    st.metric("Messages", message_count)
    
    st.divider()
    #button to clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages[st.session_state.selected] = [
            {"role": "system", "content": assistants[st.session_state.selected]["prompt"]}
        ]
        st.rerun()

st.title(f"{st.session_state.selected} Assistant")

current_messages = st.session_state.messages[st.session_state.selected]
#to display all previous messages in chat
for msg in current_messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input(f"Ask {st.session_state.selected}..."):
    current_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=current_messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
        current_messages.append({"role": "assistant", "content": full_response})