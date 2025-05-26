""" Streamlit-based multimodal news assistant querying TheBatch LLM and displaying relevant articles and images. """

import streamlit as st

from TheBatch.LLM.the_batch_trained_llms import the_batch_llm
from Internals.utils import load_image_documents_from_json
from TheBatch.the_batch_configs import THE_BATCH_IMAGE_DOCUMENTS_STORE

image_documents = load_image_documents_from_json(THE_BATCH_IMAGE_DOCUMENTS_STORE)

def main():
    st.set_page_config(page_title="The Batch Multimodal News Assistant",
                       layout="wide")
    st.title("The Batch Multimodal New Assistant")
    st.markdown("""Welcome to the **The Batch Multimodal News Assistant**!
                Ask a question and receive answer from relevent articles and images from TheBatch site.
                """)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["images"]:
                st.caption("**Note**: The retrieved images are potentially relevant to your question, but may not exactly match your intended request.")
                retrieved_images = [image_documents[retrieved_image.id] for retrieved_image in message["images"]]
                for retrieved_image in retrieved_images:
                    st.image(retrieved_image.image)
    
    if user_query := st.chat_input("Ask you question"):
        st.session_state.messages.append({
            "role": "user",
            "content": user_query,
            "images": None,
        })
        with st.spinner("Generating response..."):
            try:
                the_batch_llm_response = the_batch_llm.query(user_query=user_query)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": the_batch_llm_response.text_response,
                    "images": the_batch_llm_response.image_response
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Something went wrong while generating answer. Please try again."
                })
        st.rerun()
    
    with st.sidebar:
        if st.button("Clear Chat History"):
            st.session_state.messages.clear()
            st.rerun()
    
if __name__ == '__main__':
    main()

