import typer
from .converter import to_convert
from .calculator import calculate
from .errors import *
from rich.panel import Panel
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def calc(expr: str = typer.Option(help="expression")):
    """Calculate the expression"""
    try:
        res = calculate(expr)
        panel = Panel(f"Результат выражения: {res.to_eng_string()}", title="Успешно!", border_style="green")
        console.print(panel)
        typer.Exit(code=0)
    except InvalidOperand as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except InvalidOrder as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except InvalidBracket as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except CalcExpression as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except DifferentUnits as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)

@app.command()
def convert(value: str = typer.Option(help="value"),
            from_unit: str = typer.Option(help="input unit"),
            to_unit: str = typer.Option(help="output unit"),):
    try:
        res = to_convert(value, from_unit, to_unit)
        panel = Panel(f"Результат конвертации: {res.to_eng_string()}", title="Успешно!", border_style="green")
        console.print(panel)
        typer.Exit(code=0)
    except InvalidUnit as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except DifferentUnits as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except BelowAbsoluteZero as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)
    except ConvertExpression as e:
        panel = Panel(str(e), title="Ошибка!", border_style="red")
        console.print(panel)
        typer.Exit(code=2)

if __name__ == "__main__":
    app()