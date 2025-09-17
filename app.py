import streamlit as st
import requests
import json

st.title("🛠️ Application Management Bug Description Analyser")

bug_description = st.text_area("Enter Bug Description", height=150)
bug_id = st.text_input("Bug ID")
status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
bug_type = st.selectbox("Bug Type", ["Backend", "UI/UX", "Database", "Performance", "Security", "Other"])
comments = st.text_area("Comments")

if st.button("Analyse Bug"):
    prompt = f"""
    You are an AI bug analyser. Given the bug details, identify the root cause and provide metadata in JSON.

    Bug ID: {bug_id}
    Status: {status}
    Type: {bug_type}
    Description: {bug_description}
    Comments: {comments}

    Expected JSON output:
    {{
      "bug_id": "...",
      "root_cause": "...",
      "impact": "...",
      "recommended_fix": "...",
      "priority": "High/Medium/Low"
    }}
    """

    # Call Ollama API
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt},
        stream=True   # important: stream=True
    )

    full_response = ""
    for line in response.iter_lines():
        if line:  # skip empty lines
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                full_response += data["response"]

    st.subheader("🔎 Analysis Result")
    try:
        st.json(json.loads(full_response))  # try parsing as JSON
    except:
        st.write(full_response)             # fallback to plain text
