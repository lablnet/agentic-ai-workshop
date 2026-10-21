"""The action that is allowed only after human approval."""


def save_announcement(draft, output_folder, run_id):
    output_folder.mkdir(exist_ok=True)
    path = output_folder / f"announcement-{run_id}.md"
    path.write_text(draft + "\n", encoding="utf-8")
    return str(path)
