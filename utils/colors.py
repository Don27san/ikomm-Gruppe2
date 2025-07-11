gui_logger = None

def red(text : str) -> None:
    print('\033[31m' + text + '\033[0m')
    if gui_logger: gui_logger(text)

def blue(text : str) -> None:
    print('\033[34m' + text + '\033[0m')
    if gui_logger: gui_logger(text)

def green(text : str) -> None:
    print('\033[32m' + text + '\033[0m')
    if gui_logger: gui_logger(text)

def yellow(text : str) -> None:
    print('\033[93m' + text + '\033[0m')
    if gui_logger: gui_logger(text)
