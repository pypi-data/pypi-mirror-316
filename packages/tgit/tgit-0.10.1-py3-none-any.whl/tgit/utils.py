import subprocess
import sys
from typing import Optional

import rich
from rich.panel import Panel
from rich.syntax import Syntax

from tgit.settings import settings

console = rich.get_console()

import inquirer

type_emojis = {
    "feat": ":sparkles:",
    "fix": ":adhesive_bandage:",
    "chore": ":wrench:",
    "docs": ":page_with_curl:",
    "style": ":lipstick:",
    "refactor": ":hammer:",
    "perf": ":zap:",
    "test": ":rotating_light:",
    "version": ":bookmark:",
    "ci": ":construction_worker:",
}


def get_commit_command(commit_type: str, commit_scope: Optional[str], commit_msg: str, use_emoji=False, is_breaking=False):
    if commit_type.endswith("!"):
        commit_type = commit_type[:-1]
        is_breaking = True
        breaking_str = "!"
    else:
        breaking_str = "!" if is_breaking else ""
    if commit_scope is None:
        msg = f"{commit_type}{breaking_str}: {commit_msg}"
    else:
        msg = f"{commit_type}({commit_scope}){breaking_str}: {commit_msg}"
    if use_emoji:
        msg = f"{type_emojis.get(commit_type, ':wrench:' )} {msg}"
    return f'git commit -m "{msg}"'


def simple_run_command(command: str):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr != b"" and process.returncode != 0:
        sys.stderr.write(stderr.decode())
    if stdout != b"":
        sys.stdout.write(stdout.decode())


def run_command(command: str):
    if settings.get("show_command", True):
        panel = Panel.fit(
            Syntax(command, "bash", line_numbers=False, theme="github-dark", background_color="default", word_wrap=True),
            title="The following command will be executed:",
            border_style="cyan",
            highlight=True,
            padding=(1, 4),
            title_align="left",
            subtitle_align="right",
        )
        print()
        console.print(panel)

    if not settings.get("skip_confirm", False):

        ok = inquirer.prompt([inquirer.Confirm("continue", message="Do you want to continue?", default=True)])
        if not ok or not ok["continue"]:
            return
        console.print()

    with console.status("[bold green]Executing...") as status:
        # use subprocess to run the command
        commands = command.split("\n")
        for command in commands:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status.update(f"[bold green]Executing: {command}[/bold green]")

            # get the output and error
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                status.update("[bold red]Error[/bold red]")
            else:
                status.update("[bold green]Execute successful[/bold green]")
            if stderr != b"" and process.returncode != 0:
                sys.stderr.write(stderr.decode())
            if stdout != b"":
                sys.stdout.write(stdout.decode())
