import streamlit as st
import time
from visionlite import minivisionai, deepvisionai, visionai


def simulate_streaming(text):
    """Simulate streaming output by splitting text and adding delays"""
    chunks = text.split('\n')
    for chunk in chunks:
        if chunk.strip():
            yield chunk + '\n'
            time.sleep(0.05)


# Preset search queries
PRESET_QUERIES = {
    "📈 NVDA Stock Price": "what is the NVDA stock price today and analyst predictions",
    "🤖 CrewAI Updates": "what are the new features introduced in latest crewai framework",
    "🚀 SpaceX News": "latest SpaceX launch news and upcoming missions",
    "💻 Python Updates": "what are the new features in latest Python release",
    "📱 AI News": "latest breakthrough in artificial intelligence today",
    "💰 Crypto Updates": "Bitcoin and Ethereum price analysis and market trends",
}


def main():
    st.title("Vision AI Search Interface")

    # Quick search section
    st.header("Quick Search")
    cols = st.columns(3)
    current_col = 0

    # Store the clicked query
    if 'clicked_query' not in st.session_state:
        st.session_state.clicked_query = None

    # Create quick search buttons
    for label, preset_query in PRESET_QUERIES.items():
        with cols[current_col]:
            if st.button(label, use_container_width=True):
                st.session_state.clicked_query = preset_query
        current_col = (current_col + 1) % 3

    # Main search section
    st.header("Custom Search")

    # Search input and configuration row
    query = st.text_area(
        "Enter your search query:",
        value=st.session_state.clicked_query if st.session_state.clicked_query else "",
        height=100
    )

    # Configuration buttons row
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        with st.popover("Search Type"):
            model_type = st.radio(
                "Select Search Type",
                ["Mini Vision", "Standard Vision", "Deep Vision"],
                label_visibility="collapsed"
            )

    with col2:
        with st.popover("Model Settings"):
            model = st.text_input("Model Name", value="qwen2.5:7b-instruct")
            base_url = st.text_input("Base URL", value="http://localhost:11434")
            temperature = st.slider("Temperature",
                                    value=0.1 if model_type != "Deep Vision" else 0.05,
                                    min_value=0.0, max_value=1.0, step=0.05)

    with col3:
        with st.popover("Advanced Parameters"):
            col_left, col_right = st.columns(2)

            with col_left:
                max_urls = st.number_input("Max URLs",
                                           value=5 if model_type == "Mini Vision" else 10 if model_type == "Standard Vision" else 15,
                                           min_value=1, max_value=50)

                k = st.number_input("Top K Results",
                                    value=2 if model_type == "Mini Vision" else 3 if model_type == "Standard Vision" else 10,
                                    min_value=1, max_value=20)

                max_retries = st.number_input("Max Retries",
                                              value=3 if model_type == "Mini Vision" else 5 if model_type == "Standard Vision" else 10,
                                              min_value=1, max_value=20)

                animation = st.toggle("Enable Animation", value=False)
                allow_pdf = st.toggle("Allow PDF Extraction", value=True)

            with col_right:
                genai_query_k = st.number_input("GenAI Query K",
                                                value=3 if model_type == "Mini Vision" else 5 if model_type == "Standard Vision" else 7,
                                                min_value=1, max_value=20)

                query_k = st.number_input("Query K",
                                          value=5 if model_type == "Mini Vision" else 5 if model_type == "Standard Vision" else 15,
                                          min_value=1, max_value=20)

                allow_youtube = st.toggle("Allow YouTube", value=False)
                return_type = st.radio("Return Type", ["str", "list"])

    # Clear the clicked query after it's been used
    if st.session_state.clicked_query and query != st.session_state.clicked_query:
        st.session_state.clicked_query = None

    # Search button
    if st.button("Search", type="primary", use_container_width=True):
        if not query:
            st.warning("Please enter a search query.")
            return

        # Initialize the placeholder for streaming output
        output_placeholder = st.empty()

        # Show a spinner while processing
        with st.spinner("Searching..."):
            # Select the appropriate function based on model type
            if model_type == "Mini Vision":
                vision_func = minivisionai
            elif model_type == "Deep Vision":
                vision_func = deepvisionai
            else:
                vision_func = visionai

            try:
                result = vision_func(
                    query=query,
                    max_urls=max_urls,
                    k=k,
                    model=model,
                    base_url=base_url,
                    temperature=temperature,
                    max_retries=max_retries,
                    animation=animation,
                    allow_pdf_extraction=allow_pdf,
                    allow_youtube_urls_extraction=allow_youtube,
                    genai_query_k=genai_query_k,
                    query_k=query_k,
                    return_type=return_type
                )

                # Simulate streaming output
                full_response = ""
                for chunk in simulate_streaming(result):
                    full_response += chunk
                    output_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Vision AI Search",
        page_icon="🔍",
        layout="wide"
    )
    main()