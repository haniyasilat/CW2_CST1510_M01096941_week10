import streamlit as st
from openai import OpenAI
client=OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("Cybersecuirity AI Assistant")
if "messages" not in st.session_state:
    st.session_state.messages = [{
		"role":	"system",
		"content":	"""You	are	a	cybersecurity	expert	assistant.
		- Analyze	incidents	and	threats
		- Provide	technical	guidance
		- Explain	attack	vectors	and	mitigations
		- Use	standard	terminology	(MITRE	ATT&CK,	CVE)
		- Prioritize	actionable	recommendations
		Tone:	Professional,	technical
		Format:	Clear,	structured	responses"""
		}
		]
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Say something...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})   
    completion = client.chat.completions.create(
        model="gpt-5-nano",
        messages=st.session_state.messages
    )
    response=completion.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})