"""Draft -> pause for human review -> save or stop."""

import logging
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from actions import save_announcement
from draft_agent import build_draft_agent


class ReviewState(TypedDict):
    request: str
    run_id: str
    draft: str
    approved: bool
    saved_path: str


def build_workflow(model, output_folder):
    writer = build_draft_agent(model)

    def draft(state):
        logging.info("DRAFT | Gemini is preparing the announcement")
        result = writer.invoke({"messages": [{"role": "user", "content": state["request"]}]})
        text = result["messages"][-1].text
        if not text.strip():
            raise ValueError("The writer returned an empty draft.")
        return {"draft": text}

    def review(state):
        # No file writes before interrupt(): this node restarts when resumed.
        decision = interrupt({"draft": state["draft"], "options": ["approve", "edit", "reject"]})
        action = decision["action"]
        if action == "reject":
            logging.info("REVIEW | rejected; nothing saved")
            return {"approved": False}
        if action == "edit":
            edited = decision.get("draft", "").strip()
            if not edited:
                raise ValueError("An edited announcement cannot be empty.")
            logging.info("REVIEW | human-edited version approved")
            return {"approved": True, "draft": edited}
        if action == "approve":
            logging.info("REVIEW | draft approved")
            return {"approved": True}
        raise ValueError("Choose approve, edit, or reject.")

    def save(state):
        path = save_announcement(state["draft"], output_folder, state["run_id"])
        logging.info("SAVED | %s", path)
        return {"saved_path": path}

    graph = StateGraph(ReviewState)
    graph.add_node("draft", draft)
    graph.add_node("review", review)
    graph.add_node("save", save)
    graph.add_edge(START, "draft")
    graph.add_edge("draft", "review")
    graph.add_conditional_edges("review", lambda state: state["approved"], {True: "save", False: END})
    graph.add_edge("save", END)
    return graph.compile(checkpointer=InMemorySaver())
