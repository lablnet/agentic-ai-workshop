"""The announcement writer's instructions."""

DRAFT_PROMPT = """
Draft a short university announcement from the user's request.
Use a title and a clear message in Markdown. Preserve supplied dates and details.
Do not invent missing details; mark them as [to be confirmed].
Return only the draft. A human will review it before it is saved locally.
"""
