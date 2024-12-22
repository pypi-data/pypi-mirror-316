import math
from colorama import Style, Fore


def gradient_color(text, start_color, end_color):
    result = ""
    text_length = len(text)
    for i, char in enumerate(text):
        ratio = i / (text_length - 1) if text_length > 1 else 1
        r = math.floor((1 - ratio) * start_color[0] + ratio * end_color[0])
        g = math.floor((1 - ratio) * start_color[1] + ratio * end_color[1])
        b = math.floor((1 - ratio) * start_color[2] + ratio * end_color[2])
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result + Style.RESET_ALL

def show_codigo_ascii():
    ascii_art = """
:'######:::'#######::'########::'####::'######::::'#######::
'##... ##:'##.... ##: ##.... ##:. ##::'##... ##::'##.... ##:
 ##:::..:: ##:::: ##: ##:::: ##:: ##:: ##:::..::: ##:::: ##:
 ##::::::: ##:::: ##: ##:::: ##:: ##:: ##::'####: ##:::: ##:
 ##::::::: ##:::: ##: ##:::: ##:: ##:: ##::: ##:: ##:::: ##:
 ##::: ##: ##:::: ##: ##:::: ##:: ##:: ##::: ##:: ##:::: ##:
. ######::. #######:: ########::'####:. ######:::. #######::
:......::::.......:::........:::....:::......:::::.......:::
    """
    start_color = (128, 0, 128)
    end_color = (0, 0, 255)
    for line in ascii_art.splitlines():
        print(gradient_color(line, start_color, end_color))

def print_codigo_line(text: str) -> None:
    print(Fore.WHITE + '[' + Fore.GREEN + 'CODIGO' + Fore.WHITE + ']: ' + text + Fore.RESET)