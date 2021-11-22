class color:
    BOLD = '\033[1m'
    RED = '\033[31m'
    CLEAR = '\033[0m'

def error(message):
    return f'{color.RED}{color.BOLD}{message}{color.CLEAR}'
