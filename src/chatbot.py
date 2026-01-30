import streamlit as st
from build_kb_index import build_index
from slm_reasoner import ReasonerSLM
from rag_search import search
from db import fetch_order
import re

@st.cache_resource
def load_resources():
    index, chunks, meta, model = build_index()
    reasoner = ReasonerSLM()
    return index, chunks, meta, model, reasoner


def extract_order_number(text):
    match = re.search(r"\b\d{4,}\b", text)
    return match.group() if match else None

def pipeline(question):
    # ✅ ALWAYS define interpreted
    interpreted = {
        "intent": "unknown",
        "task": "reasoning",
        "expanded_query": question
    }

    # Load cached resources
    index, chunks, meta, model, reasoner = load_resources()

    # Retrieve KB context
    retrieved = search(
        query=question,
        model=model,
        index=index,
        chunks=chunks,
        sources=meta,
        k=3
    )

    # Order number detection
    order_id = extract_order_number(question)

    if order_id:
        order_data = fetch_order(order_id)

        if not order_data:
            return {
                "interpreted": interpreted,
                "retrieved": retrieved,
                "final_answer": (
                    f"I couldn’t find any order with number {order_id}. "
                    "Please check the order number and try again."
                )
            }

        return {
            "interpreted": interpreted,
            "retrieved": retrieved,
            "final_answer": (
                f"Here is the current status of your order {order_id}:\n"
                f"- Order status: {order_data['status']}\n"
                f"- Delivery status: {order_data['delivery_status']}\n"
                f"- Last known location: {order_data['last_known_location']}\n\n"
                "We are investigating this with our logistics partners."
            )
        }

    # No order number → let LLM reason
    answer = reasoner.respond(
        question,
        interpreted,
        retrieved,
        db_context=""
    )

    return {
        "interpreted": interpreted,
        "retrieved": retrieved,
        "final_answer": answer
    }
