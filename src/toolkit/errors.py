class ConvertExpression(Exception):
    """ Базовый класс для всех пользовательских ошибок конвертера. """

    default_message = "Некорректные данные для конвертации!"

    def __init__(self, expression: str = "", message: str = ""):
        self.expression = expression

        base_msg = message if message else self.default_message
        full_message = f"{base_msg}: {expression}" if expression else base_msg

        super().__init__(full_message)

class InvalidUnit(ConvertExpression):
    """Ошибка, возникающая при передаче некорректных единиц измериния."""
    default_message = "Введены некорректные единицы измерения!"

class DifferentUnits(ConvertExpression):
    """Ошибка, возникающая при передаче несовместимых единиц измериния."""
    default_message = "Введены несовместимые единицы измерения!"

class BelowAbsoluteZero(ConvertExpression):
    """ Ошибка, возникающая при вводе температуры ниже абсолютного нуля. """
    default_message = "Температура должна быть не ниже абсолютного нуля!"



class CalcExpression(Exception):
    """ Базовый класс для всех пользовательских ошибок калькулятора. """

    default_message = "Некорректные данные для вычисления!"

    def __init__(self, expression: str = "", message: str = ""):
        self.expression = expression

        base_msg = message if message else self.default_message
        full_message = f"{base_msg}: {expression}" if expression else base_msg

        super().__init__(full_message)

class InvalidOperand(CalcExpression):
    """ Ошибка, возникающая при вводе некорректных операндов. """
    default_message = "Введены некорректные операнды!"

class InvalidBracket(CalcExpression):
    """ Ошибка, возникающая при некорректном вводе скобок. """
    default_message = "Скобочные группы введены некорректно!"

class InvalidOrder(CalcExpression):
    """ Ошибка, возникающая при недопустимом порядке ввода операнадов. """
    default_message = "Порядок ввода операндов недопустим!"

class DivisionByZero(CalcExpression):
    """ Ошибка, возникающая при делении на ноль. """
    default_message = "Деление на ноль запрещено!"