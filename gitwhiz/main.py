import os
import re
import subprocess
from typing import List, Dict

import click

from core.template_engine import TemplateEngine

COMMIT_TYPES = ["feature", "bugfix", "docs", "refactor"]


def run(cmd: List[str], cwd: str = ".", capture_output: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=False, text=True, capture_output=capture_output)


def get_changed_files(repo_path: str = ".") -> List[str]:
    # git status --porcelain shows changed files
    cp = run(["git", "status", "--porcelain"], cwd=repo_path)
    if cp.returncode != 0:
        return []
    lines = [l.strip() for l in cp.stdout.splitlines() if l.strip()]
    files = []
    for line in lines:
        # format: XY <path> (path may be quoted)
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            files.append(parts[1].strip())
    return files


def show_diffs(files: List[str], repo_path: str = ".") -> None:
    for f in files:
        click.echo(f"\n--- Diff for: {f} ---")
        cp = run(["git", "diff", "--", f], cwd=repo_path)
        if cp.returncode == 0 and cp.stdout:
            click.echo(cp.stdout)
        else:
            click.echo("(no unstaged changes or unable to show diff)")


def prompt_for_file_selection(files: List[str]) -> List[str]:
    if not files:
        return []
    click.echo("Changed files:")
    for i, f in enumerate(files, start=1):
        click.echo(f"  {i}) {f}")
    sel = click.prompt("Enter files to stage (comma-separated indices, 'all' to stage all)", default="all")
    sel = sel.strip()
    if sel.lower() in ("all", "a", "*", ""):
        return files[:]
    picks = []
    for part in sel.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            idx = int(part)
            if 1 <= idx <= len(files):
                picks.append(files[idx - 1])
        except ValueError:
            # allow direct file names
            if part in files:
                picks.append(part)
    # dedupe while preserving order
    seen = set()
    result = []
    for p in picks:
        if p not in seen:
            result.append(p)
            seen.add(p)
    return result


def extract_placeholders(template_text: str) -> List[str]:
    # match {{Key}} or {Key}
    pattern = re.compile(r"\{\{\s*(?P<k>\w+)\s*\}\}|\{\s*(?P<k2>\w+)\s*\}")
    placeholders = []
    for m in pattern.finditer(template_text):
        key = m.group("k") or m.group("k2")
        if key and key not in placeholders:
            placeholders.append(key)
    return placeholders


@click.group()
def cli():
    pass


@cli.command("smart-commit")
@click.option("--repo", default=".", help="Path to repository (default: current dir).")
def smart_commit(repo):
    """
    Interactive smart commit:
      1) Show changed files
      2) Ask which files to stage
      3) Show diffs
      4) Ask commit type
      5) Load template and prompt for fields
      6) Show final message preview
      7) Ask to push now and perform git add/commit/push
    """
    os.chdir(repo)
    te = TemplateEngine()

    files = get_changed_files(repo_path=".")
    if not files:
        click.echo("No changed files detected.")
        return

    to_stage = prompt_for_file_selection(files)
    if not to_stage:
        click.echo("No files selected. Aborting.")
        return

    # show diffs for selected files
    show_diffs(to_stage)

    # choose commit type
    commit_type = click.prompt("Commit type", type=click.Choice(COMMIT_TYPES), default=COMMIT_TYPES[0])
    template_text = te.load_template(commit_type)
    if not template_text:
        click.echo("Failed to load template. Aborting.")
        return

    # collect placeholder values
    placeholders = extract_placeholders(template_text)
    values: Dict[str, str] = {}
    # prefill Changes with the list of staged files
    changes_prefill = "\n".join(f"- {p}" for p in to_stage)
    for ph in placeholders:
        default = ""
        if ph.lower() == "changes":
            default = changes_prefill
        elif ph.lower() == "issuenumber":
            default = ""
        # use click.prompt so users can leave blank
        resp = click.prompt(f"{ph}", default=default, show_default=bool(default))
        values[ph] = resp

    # render commit message
    commit_message = te.render_template(template_text, values)
    click.echo("\n--- Commit Message Preview ---\n")
    click.echo(commit_message)
    click.echo("\n--- End Preview ---\n")

    if not click.confirm("Proceed with staging and committing?"):
        click.echo("Aborted by user.")
        return

    # stage files
    cp = run(["git", "add", "--"] + to_stage)
    if cp.returncode != 0:
        click.echo(f"git add failed: {cp.stderr}")
        return

    # commit
    cp = run(["git", "commit", "-m", commit_message])
    if cp.returncode != 0:
        click.echo(f"git commit failed: {cp.stderr}")
        return
    click.echo(cp.stdout or "Committed.")

    # ask to push
    if click.confirm("Push commit now?"):
        cp = run(["git", "push"])
        if cp.returncode != 0:
            click.echo(f"git push failed: {cp.stderr}")
            return
        click.echo("Pushed.")

if __name__ == "__main__":
    cli()