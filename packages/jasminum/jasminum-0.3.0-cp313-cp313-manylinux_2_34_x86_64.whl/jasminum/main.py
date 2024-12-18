import argparse
import importlib.metadata
import readline
import traceback

from termcolor import cprint

from .context import Context
from .engine import Engine
from .eval import eval_src
from .history_console import HistoryConsole

__version__ = importlib.metadata.version("jasminum")

parser = argparse.ArgumentParser(description="jasminum, the python engine for jasmine")

parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    default=False,
    dest="debug",
    help="enable debug mode",
)


def main():
    args = parser.parse_args()
    print(
        "\x1b[1;32m\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣗⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣶⣦⣄⣀⠀⠀⠀⢸⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣽⣿⣿⣦⡀⣾⣿⣿⣿⣿⣿⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⣻⣿⣿⣿⣿⣿⣿⣿⣷⡜⢿⣿⣿⣿⣿⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣿⣿⡿⢡⣴⣾⣿⣶⣿⣷⣦⣄⡀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣷⡽⠿⣛⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣧⣤⣿⡻⠿⠿⢿⣿⣿⠿⠛⠉⠛⠋⠉⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠳⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠟⠁⠀⠈⠻⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠉⠀⠀⠀⠀⠀⠀⠀ \n\
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⠉                            jasminum ver {} \x1b[0m\n".format(
            __version__
        )
    )

    engine = Engine()
    HistoryConsole()
    src = ""
    readline.set_completer(engine.complete)
    while src != "exit":
        try:
            src = []
            line = input("j*  ")
            if line == "":
                continue
            else:
                src.append(line)
            while True:
                line = input("*   ")
                if not line:
                    break
                src.append(line)
            src = "\n".join(src)
            engine.sources[0] = (src, "")
            try:
                res = eval_src(src, 0, engine, Context(dict()))
                cprint(res, "light_green")
            except Exception as e:
                if args.debug:
                    traceback.print_exc()
                cprint(e, "red")
        except EOFError:
            cprint("exit on ctrl+D", "red")
            exit(0)
        except KeyboardInterrupt:
            print()
            continue
