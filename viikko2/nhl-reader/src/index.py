from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

def main():
    console = Console()
    console.print("\n[bold cyan]NHL Statistics[/bold cyan]\n")

    season = Prompt.ask("Select season", choices=["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"], default="2024-25")
    nationality = Prompt.ask("Select nationality", default="FIN").upper()

    players = PlayerStats(PlayerReader(f"https://studies.cs.helsinki.fi/nhlstats/{season}/players")).top_scorers_by_nationality(nationality)

    table = Table(title=f"\nTop scorers from {nationality} season {season}")

    columns = [("Name", {"style": "cyan", "no_wrap": True}), ("Team", {"style": "magenta"}),
           ("Goals", {"justify": "right", "style": "green"}), ("Assists", {"justify": "right", "style": "green"}),
           ("Points", {"justify": "right", "style": "bold yellow"})]
    for header, kwargs in columns:
        table.add_column(header, **kwargs)

    for p in players:
        table.add_row(*[str(getattr(p, attr)) for attr in ("name", "team", "goals", "assists", "points")])

    console.print(table)

if __name__ == "__main__":
    main()
