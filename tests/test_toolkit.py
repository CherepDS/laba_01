import pytest
from src.toolkit.converter import to_convert
from src.toolkit.errors import *
from decimal import Decimal
from typer.testing import CliRunner
from src.toolkit.__main__ import app
from src.toolkit.calculator import tokenization, rpn_covert, calculate

# Позитивные тесты для калькулятора
def test_correct_tokenization():
    assert tokenization("1*(5-3)") == ['1', '*', '(', '5', '-', '3',")"]

def test_calc_priority():
    assert calculate("2+3*4") == Decimal("14")

def test_calc_division():
    assert calculate("10/4") == Decimal("2.5")

def test_calc_multiplication():
    assert calculate("-2*-3") == Decimal("6")

def test_calc_unary_operations():
    assert calculate("1+-2") == Decimal("-1")

# Негативные тесты для калькулятора
def test_incorrect_token():
    with pytest.raises(InvalidOperand):
        tokenization("2+a")

def test_incorrect_order():
    with pytest.raises(InvalidOrder):
        calculate("2*/3")

def test_division_by_zero():
    with pytest.raises(DivisionByZero):
        calculate("1/0")

def test_empty_expression():
    with pytest.raises(CalcExpression):
        calculate("")



# Позитивные тесты конвертера
def test_convert_length():
    assert to_convert("1000","mm","m") == Decimal("1")

def test_convert_mass():
    assert to_convert("1.5","kg","g") == Decimal("1500")

def test_convert_temp_1():
    assert to_convert("0","c","f") == Decimal("32")

def test_convert_temp_2():
    assert to_convert("-273.15","c","k") == Decimal("0")

def test_convert_upper():
    assert to_convert("2","M","CM") == Decimal("200")

# Негативные тесты конвертера
def test_error_absolute_zero():
    with pytest.raises(BelowAbsoluteZero):
        to_convert("-300","c","k")

def test_incorrect_units():
    with pytest.raises(DifferentUnits):
        to_convert("24","kg","m")



# Тесты CLI
runner = CliRunner()

def test_cli_calc_success():
    """Позитивный тест: сложение через CLI"""
    # Аргументы передаются списком строк, точно так же, как в терминале
    result = runner.invoke(app, ["calc", "--expr", "2+2"])

    # Typer пишет в stdout через typer.echo, это попадает в result.output
    assert result.exit_code == 0
    assert "4" in result.output

def test_cli_convert_success():
    """Позитивный тест: конвертация температуры"""
    # Пример вызова: python -m toolkit convert 54 f c
    result = runner.invoke(app, ["convert", "--value", "54", "--from-unit", "f", "--to-unit", "c"])

    assert result.exit_code == 0
    assert "12.222" in result.output

def test_cli_help():
    """Проверка работы --help"""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0

    assert "Usage:" in result.output
    # Проверяем, что в хелпе есть наши команды
    assert "calc" in result.output
    assert "convert" in result.output
    
