"""
Rich-based neon-green hacker terminal UI for Cyber Career Compass.
Graphically rich: rules, progress bars, styled panels, and cyber aesthetic.
"""

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich import box
from rich.style import Style
from rich.align import Align

from nice_framework import WorkRole, Certification, get_work_role, get_certifications

# Neon cyber palette
NEON_GREEN = "#39ff14"
DIM_GREEN = "#0d3d0d"
DARK_BG = "#0a0a0a"
ACCENT = "#00ff88"
ACCENT_CYAN = "#00ffff"
WARN = "#ffaa00"
MAGENTA = "#ff00ff"
DIM = "#555555"

console = Console(force_terminal=True)


def style_heading(s: str) -> Text:
    return Text(s, style=Style(color=NEON_GREEN, bold=True))


def style_body(s: str) -> Text:
    return Text(s, style=Style(color=ACCENT))


def style_dim(s: str) -> Text:
    return Text(s, style=Style(color=DIM))


def print_rule(title: str = "", style: str = NEON_GREEN) -> None:
    """Print a horizontal rule with optional title."""
    console.print(Rule(title=title, style=style, characters="═"))


def print_banner() -> None:
    """Print a graphically rich game title banner."""
    console.print()
    print_rule(style=DIM)
    # Bold title lines (fit narrow terminals)
    title1 = Text("  ██████╗██╗   ██╗██████╗ ███████╗██████╗  ", style=NEON_GREEN)
    title2 = Text("  ██╔═══╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗ ", style=ACCENT)
    title3 = Text("  ██║     ╚████╔╝ ██████╔╝█████╗  ██████╔╝ ", style=Style(color=NEON_GREEN, bold=True))
    title4 = Text("  ██║      ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗ ", style=Style(color=ACCENT, bold=True))
    title5 = Text("  ╚██████╗  ██║   ██║  ██║███████╗██║  ██║  ", style=NEON_GREEN)
    title6 = Text("   ╚═════╝  ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ", style=ACCENT)
    sub = Text("  C A R E E R   C O M P A S S  ", style=Style(color=ACCENT_CYAN, bold=True))
    tagline = Text("  NIST NICE Framework · Terminal Assessment · Find Your Path  ", style=Style(color=DIM, italic=True))
    inner = Group(title1, title2, title3, title4, title5, title6, Text(), sub, Text(), tagline)
    console.print(Panel(Align.center(inner), border_style=NEON_GREEN, box=box.DOUBLE, padding=(1, 2)))
    print_rule(style=DIM)
    console.print()


def print_section_title(title: str, icon: str = "▸") -> None:
    """Print a section header with rule and icon."""
    console.print()
    print_rule(style=DIM)
    header = Text(f"  {icon} ", style=NEON_GREEN) + Text(title, style=Style(color=NEON_GREEN, bold=True))
    console.print(Panel(header, border_style=ACCENT_CYAN, box=box.ROUNDED, padding=(0, 2)))
    console.print()


def print_phase_progress(current: int, total: int, phase_name: str) -> None:
    """Show a static progress bar for the current phase (e.g. Question 3 of 5)."""
    width = 24
    filled = int(width * current / total) if total else 0
    bar = "█" * filled + "░" * (width - filled)
    text = Text()
    text.append(f"  {phase_name}  ", style=Style(color=ACCENT_CYAN))
    text.append(bar, style=NEON_GREEN)
    text.append(f"  {current}/{total}", style=Style(color=DIM))
    console.print(Panel(text, border_style=DIM, box=box.SIMPLE, padding=(0, 1)))
    console.print()


def print_question(phase: str, index: int, total: int, prompt: str) -> None:
    """Print a question with phase, progress bar, and styled panel."""
    # Progress bar (current question / total)
    phase_label = "Instinct (Personality)" if "Instinct" in phase else "Technical (Triage)"
    print_phase_progress(index, total, phase_label)

    header = Text(f"  [{phase}] ", style=MAGENTA) + Text(f"Question {index} of {total}", style=NEON_GREEN)
    prompt_text = Text(prompt, style=Style(color=ACCENT))
    console.print(Panel(Group(header, Text(), prompt_text), border_style=ACCENT_CYAN, box=box.ROUNDED, padding=(1, 3), title="◉", title_align="left"))
    console.print()


def print_choices(choices: list, start_at: int = 1) -> None:
    """Print lettered choices in a compact styled table."""
    letters = "abcdefghij"
    choice_table = Table(show_header=False, box=box.SIMPLE, border_style=DIM, padding=(0, 1))
    choice_table.add_column("", style=NEON_GREEN, width=4)
    choice_table.add_column("", style=ACCENT, width=2)
    choice_table.add_column("", style=ACCENT)
    for i, choice in enumerate(choices):
        letter = letters[i] if i < len(letters) else str(i + 1)
        choice_table.add_row(f"  [{letter}]", "→", choice.text)
    console.print(Panel(choice_table, border_style=DIM, box=box.ROUNDED, padding=(0, 2)))
    console.print()


def print_dossier(aptitude: str, knowledge_level: int) -> None:
    """Generate and display the NICE Career Dossier with rich layout."""
    role = get_work_role(aptitude, knowledge_level)
    certs = get_certifications(aptitude, knowledge_level)

    print_rule(" YOUR NICE CAREER DOSSIER ", NEON_GREEN)
    console.print()

    # —— Role badge: compact highlight ——
    role_badge = Text()
    role_badge.append("  ", style=NEON_GREEN)
    role_badge.append(role.id, style=Style(color=NEON_GREEN, bold=True))
    role_badge.append("  ·  ", style=DIM)
    role_badge.append(role.title, style=Style(color=ACCENT_CYAN, bold=True))
    role_badge.append("  ·  ", style=DIM)
    role_badge.append(role.category, style=WARN)
    console.print(Panel(role_badge, border_style=NEON_GREEN, box=box.HEAVY, padding=(0, 2)))
    console.print()

    # —— Work Role details table ——
    role_table = Table(show_header=False, box=box.ROUNDED, border_style=ACCENT_CYAN, row_styles=["", "dim"])
    role_table.add_column("Key", style=NEON_GREEN, width=14)
    role_table.add_column("Value", style=ACCENT)
    role_table.add_row("Work Role ID", role.id)
    role_table.add_row("Title", role.title)
    role_table.add_row("Category", role.category)
    role_table.add_row("Definition", role.definition)

    console.print(Panel(role_table, title="[bold]Work Role[/bold]", border_style=ACCENT_CYAN, padding=(1, 2), box=box.ROUNDED))
    console.print()

    # —— Strengths: highlighted panel ——
    strengths_text = Text(role.strengths_summary, style=Style(color=ACCENT))
    console.print(Panel(strengths_text, title="[bold]Your Strengths[/bold]", border_style=WARN, padding=(1, 2), box=box.ROUNDED))
    console.print()

    # —— Certification roadmap table ——
    cert_table = Table(
        title="Roadmap — Next Certifications to Pursue",
        box=box.ROUNDED,
        border_style=NEON_GREEN,
        show_header=True,
        header_style=Style(color=NEON_GREEN, bold=True),
        row_styles=["", "dim"],
    )
    cert_table.add_column("#", style=NEON_GREEN, width=4)
    cert_table.add_column("Certification", style=ACCENT)
    cert_table.add_column("Issuer", style=ACCENT_CYAN)
    cert_table.add_column("Level", style=WARN)
    for i, c in enumerate(certs, 1):
        cert_table.add_row(str(i), c.name, c.issuer, c.level)
    console.print(Panel(cert_table, border_style=NEON_GREEN, padding=(1, 2), box=box.DOUBLE))
    console.print()

    # Closing line with rule
    print_rule(style=DIM)
    console.print(Align.center(Text(">> Assessment complete. Align your path with the NICE Framework. <<", style=Style(color=NEON_GREEN, italic=True))))
    console.print()


def print_farewell() -> None:
    """Print closing message with style."""
    msg = Text("Thank you for using Cyber Career Compass. ", style=ACCENT) + Text("Good luck on your path.", style=NEON_GREEN)
    console.print(Panel(Align.center(msg), border_style=ACCENT_CYAN, box=box.ROUNDED, padding=(1, 3)))
    console.print()
