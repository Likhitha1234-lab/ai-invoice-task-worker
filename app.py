import streamlit as st

from agent.agent import run_agent


st.set_page_config(
    page_title="AI Invoice Worker",
    page_icon="🤖"
)


st.title("🤖 AI Invoice Task Worker")


task = st.text_area(
    "Enter your task"
)


if st.button("Run Task"):

    if not task.strip():
        st.warning("Please enter a task.")

    else:
        with st.spinner("AI is working..."):

            response = run_agent(task)

        st.success("Task completed")

        st.subheader("AI Result")

        st.write(response.output_text)