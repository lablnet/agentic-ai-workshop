"""The action that is allowed only after human approval."""


def save_announcement(draft, output_folder, run_id):
    """
    Persist an approved announcement to disk.

    Args:
        draft: Final announcement text.
        output_folder: Directory for saved markdown files.
        run_id: Unique id so each run gets its own file.

    Returns:
        Path to the saved file as a string.
    """
    output_folder.mkdir(exist_ok=True)
    path = output_folder / f"announcement-{run_id}.md"
    path.write_text(draft + "\n", encoding="utf-8")
    return str(path)
