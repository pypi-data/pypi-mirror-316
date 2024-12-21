import os, sys, subprocess, webbrowser, platform, json # NOQA
# above line is noqa due to readline not being used.

from typing import Literal
from pathlib import Path
from colorama import Style, Fore, Back
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PTStyle
from prompt_toolkit.formatted_text import FormattedText

DIR: Path = Path(__file__).parent
SYS_ROOT: str = os.path.abspath(os.sep)
STORAGE_PATH: Path = DIR / "storage"
EP_MODULE: str = str(DIR).removeprefix(SYS_ROOT).replace("\\", "/").replace("/", ".")
PLATFORM: str = platform.system().lower()
STYLE = PTStyle.from_dict({
    'yellow': 'bold fg:yellow',
    'magenta': 'fg:magenta',
    'blue': 'bold fg:blue',
    'reset': '',
})
JSON_FRAME: str = """
{
    "cmd_history": [],
    "cd_history": [],
    "aliases": {}
}
"""

history: InMemoryHistory = InMemoryHistory()

def error(text: str) -> None:
    print(f"🚨 {Fore.RED}error: {text}{Style.RESET_ALL}")
def hint(text: str) -> None:
    print(f"💡 {Fore.BLUE}hint: {text}{Style.RESET_ALL}")
def warning(text: str) -> None:
    print(f"⚠  {Fore.YELLOW}warning: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def important(text: str) -> None:
    print(f"⚠  {Back.YELLOW}{Fore.BLACK}important: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def info(text: str) -> None:
    print(f"➤➤ {text}")

class MutablePath:
    def __init__(self, path: Path | None = None):
        self.root: str = os.path.abspath(os.sep)
        self.path: Path = path or Path(self.root)
        self.set(str(self.path), [])
    def set(self, path: str, cd_history: list[str], ucd: bool = False, st: bool = False):
        old_path = self.path
        if str(self.path) == str(STORAGE_PATH) and not (ucd or st):
            warning("cannot use cd in storage mode, use st to exit storage mode first.")
            return
        if path == str(STORAGE_PATH) and not st:
            hint("use the st command to switch to storage mode easier")
        if path == "..":
            self.path = self.path.parent
        elif path == ".":
            ...
        else:
            self.path /= path
        if not self.path.exists() and st:
            warning("storage directory does not exist, creating now.")
            os.mkdir(str(self.path))
            info("storage directory created successfully")
        if not self.path.exists() or not self.path.is_dir():
            error(f"{self.path} is not a valid path.")
            self.path = old_path
        else:
            cd_history.append(str(old_path))

def subprocess_run(command: list[str]):
    try:
        subprocess.run(command)
    except Exception as exc:
        error(f"solo: {exc}")

class Timestamp:
    def __init__(self, date: dict, time: dict, time_format: Literal["eu", "us"] = "eu"):
        self.date: dict = date
        self.time: dict = time
        self.repr_date_eu: str = f"{date['name']} {date['day']}.{date['month']}.{date['year']}"
        self.repr_date_us: str = f"{date['name']} {date['month']}/{date['day']}/{date['year']}"
        self.repr_date: str = self.repr_date_us if time_format == "us" else self.repr_date_eu
        self.repr_time: str = f"{time['hours']}:{time['minutes']}:{time['seconds']}"
        self.repr_full: str = f"{self.repr_date} {self.repr_time}"
        self.time_format: str = time_format
    def __repr__(self):
        return self.repr_full
    def __str__(self):
        return repr(self)
    @classmethod
    def from_now(cls, time_format: Literal["eu", "us"] = "eu"):
        from datetime import datetime

        now = datetime.now()
        return cls(
            date={
                "name": now.strftime("%A").lower(),
                "day": now.strftime("%d"),
                "month": now.strftime("%m"),
                "year": now.strftime("%Y")
            },
            time={
                "hours": now.strftime("%H"),
                "minutes": now.strftime("%M"),
                "seconds": now.strftime("%S")
            },
            time_format=time_format
        )
    @classmethod
    def from_dict(cls, obj):
        return cls(
            date={
                "name": obj["name"],
                "day": obj["day"],
                "month": obj["month"],
                "year": obj["year"]
            },
            time={
                "hours": obj["hours"],
                "minutes": obj["minutes"],
                "seconds": obj["seconds"]
            },
            time_format=obj["time_format"]
        )
    def to_dict(self):
        return {
            "name": self.date["name"],
            "day": self.date["day"],
            "month": self.date["month"],
            "year": self.date["year"],
            "hours": self.time["hours"],
            "minutes": self.time["minutes"],
            "seconds": self.time["seconds"],
            "time_format": self.time_format
        }

class MetaJSON:
    def __init__(self, path: Path):
        self.path: Path = path
    def create(self):
        with self.path.open("w", encoding="utf-8") as file:
            file.write(JSON_FRAME)
    def write(self, data: dict):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4) # NOQA
    def read(self) -> dict:
        if not self.path.exists():
            raise FileNotFoundError(f"The file {self.path} does not exist.")
        with self.path.open(encoding="utf-8") as file:
            return json.load(file)


def parse_command(parts: list[str]):
    new: list[str] = []
    string: str = ""

    for part in parts:
        if not part:
            continue
        elif string:
            if part[-1] == string:
                new[-1] += " " + part[:-1]
                string = ""
            else:
                new[-1] += " " + part
        elif part[0] in "\"'":
            if len(part) > 1 and part[-1] == part[0]:
                new.append(part[1:-1])
            else:
                new.append(part[1:])
                string = part[0]
        else:
            new.append(part)
    return new, string

def main() -> None:
    meta: MetaJSON = MetaJSON(DIR / "meta.json")
    meta.create()
    at: str = os.getcwd()
    if len(sys.argv) > 1:
        at = str(STORAGE_PATH) if sys.argv[1] == "storage" else sys.argv[1]
    abs_at = os.path.abspath(at).removesuffix("-n").replace(" ", "\\ ")
    running_as_new: bool = "--running-as-new" in sys.argv
    if "-n" in sys.argv or "--new" in sys.argv:
        match PLATFORM:
            case "windows":
                subprocess_run(["cmd", "/C", "start", "python", "-m", repr(EP_MODULE), abs_at, "--running-as-new"])
            case "linux":
                hint("not working? make sure gnome-terminal is available")
                subprocess_run(["gnome-terminal", "--", "bash", "-c", f"cd {SYS_ROOT}; python3 -m '{EP_MODULE}' {abs_at} --running-as-new; exec bash"])
            case _:
                error("unidentified operating system; could not find a way to open a new terminal.")
        exit(0)
    mutable_location: MutablePath = MutablePath(Path(os.getcwd()))
    cd_history: list[str] = meta.read()["cd_history"]
    cmd_history: list[tuple[Timestamp, str]] = []
    for timestamp, cmd in meta.read()["cmd_history"]:
        cmd_history.append((Timestamp.from_dict(timestamp), cmd))
    mutable_location.set(at, [], st=at==str(STORAGE_PATH))
    solo_mode: str = ""
    aliases: dict[str, str] = meta.read()["aliases"]
    while True:
        if (os.path.getsize(meta.path) / 1024) > 500:
            warning("pistol's meta file is getting quite big! run analyse to learn more and free up space.")
        try:
            loc: Path = mutable_location.path
            disp_loc: str = f"{Back.YELLOW}{Fore.BLACK}storage{Style.RESET_ALL}" if str(loc) == str(STORAGE_PATH) else loc
            autocomplete: list[str] = [f"./{item}" for item in os.listdir(loc) if not item.startswith(".")] + [".."]
            completer: WordCompleter = WordCompleter(autocomplete, ignore_case=True)
            session: PromptSession = PromptSession(history=history, completer=completer)
            try:
                if solo_mode:
                    prompt_text: FormattedText = FormattedText([
                        ('class:yellow', f"➤➤ {os.name}: "),
                        ('', f"{disp_loc} "),
                        ('class:magenta', f"[{solo_mode}]"),
                        ('class:blue', "> "),
                    ])
                    full_command: str = (solo_mode + " " + session.prompt(prompt_text)).removeprefix(f"{solo_mode} pistol ")
                    full_command = full_command.removeprefix(f"{solo_mode} ") if full_command.startswith(f"{solo_mode} cd ") else full_command
                    if full_command == f"{solo_mode} exit":
                        info(f"exited {solo_mode}")
                        solo_mode = ""
                        continue
                else:
                    prompt_text: str = FormattedText([
                        ("", "➤➤ "),
                        ("class:yellow", f"{os.name}: "),
                        ("", f"{disp_loc}"),
                        ("class:blue", "> "),
                    ])
                    full_command: str = session.prompt(prompt_text)
            except EOFError:
                print()
                try:
                    import getpass

                    hint("press ^C to exit pistol")
                    hint("press any other button to return to pistol")

                    getpass.getpass(f"➤➤ ")
                    continue
                except KeyboardInterrupt:
                    full_command: str = "exit --no-hint"
                    print()
                except EOFError:
                    print()
                    continue

            parts: list[str] = full_command.split(" ")
            new, string = parse_command(parts)
            if string:
                error("unclosed string in command.")
                continue
            if not new:
                continue
            command: str = new[0]
            args: list[str] = new[1:]

            cmd_history.append((Timestamp.from_now(), full_command))

            try:
                def exit_pistol():
                    meta_contents = meta.read()
                    meta_contents["cd_history"] = cd_history
                    writable_cmd_history = []
                    for timestamp, cmd in cmd_history: # NOQA
                        writable_cmd_history.append((timestamp.to_dict(), cmd))
                    meta_contents["cmd_history"] = writable_cmd_history
                    meta_contents["aliases"] = aliases
                    meta.write(meta_contents)
                    info("exited pistol")
                    if "--no-hint" not in args:
                        hint("pressing ^D chord to ^C will exit pistol as well")
                    if running_as_new:
                        hint("press ^D to exit the terminal entirely")
                    exit()
                def run_solo(c: list[str]):
                    nonlocal solo_mode

                    if args not in [
                        [],
                        ["pwsh", "-Command"]
                    ]:
                        force_cwd: bool = "--force-cwd" in args
                        args.remove("--force-cwd") if "--force-cwd" in args else ...
                        if args[0] in c:
                            warning(f"{args[0]} may not work properly when executing using {solo_mode or command}")
                        old_dir: str = os.getcwd()
                        try:
                            os.chdir(loc)
                        except FileNotFoundError:
                            if force_cwd:
                                info(f"created {disp_loc}")
                                os.mkdir(loc)
                                os.chdir(loc)
                            else:
                                warning(f"tried to execute a solo command in a directory that does not exist. solo will execute it in {old_dir} instead.")
                                hint(f"rerun the command with the --force-cwd option to run in {disp_loc}.")
                        subprocess_run(args)
                        os.chdir(old_dir)
                    else:
                        solo_mode = command
                def undo_cd(internal: bool = False):
                    try:
                        mutable_location.set(cd_history.pop(), [], ucd=True)
                    except IndexError:
                        if internal:
                            return False
                        else:
                            warning("nothing left to undo")
                    return True
                def st():
                    if str(loc) != str(STORAGE_PATH):
                        mutable_location.set(str(STORAGE_PATH), cd_history, st=True),
                        hint("use st again to return to normal mode")
                    elif not undo_cd(internal=True):
                        warning(f"could not find location to exit to, defaulting to {os.getcwd()}")
                        mutable_location.set(os.getcwd(), [], st=True)
                def view_cd_history():
                    if not cd_history:
                        info("cd history empty")
                    else:
                        index: int = 1
                        for index, item in enumerate(cd_history, start=1):
                            info(f"{index}: {item}")
                        info(f"{index+1}: {disp_loc}")
                        hint(f"{index+1} is your current location. the next ucd will take you to {index}")
                def clear_cd_history():
                    nonlocal cd_history
                    cd_history = []

                from . import VERSION

                def reverse_search():
                    if not cmd_history:
                        error("cannot reverse search; no command history")
                    else:
                        hint("find a command in your command history by entering it exactly,")
                        hint("or just a part of it you remember. type help for more info.")
                        search: str = input(f"➤➤ {Back.YELLOW}query{Style.RESET_ALL}> ")
                        if search == "help":
                            info("command history is saved even after you exit pistol")
                            important("command history may not be saved if pistol is reinstalled,")
                            important("tampered with, or reset.")
                            info("you can also just press return to list all command history")
                            info("you can run rmc <full command> to delete a command from your history")
                            info("you can run cch to clear your command history entirely")
                        else:
                            for cmd in cmd_history: # NOQA
                                if search in cmd[1]:
                                    info(f"{cmd[0]} - {cmd[1]}")
                def clear_command_history():
                    nonlocal cmd_history
                    cmd_history = []
                def clear_from_command_history(internal: bool = False):
                    query: str = " ".join(args)
                    for i, cmd in enumerate(cmd_history): # NOQA
                        if cmd[1] == query:
                            break
                    else:
                        if not internal:
                            error(f"{query} could not be found in the command history")
                        return False
                    cmd_history.pop(i)
                    if not internal:
                        info(f"removed {query}")
                    clear_from_command_history(internal=True)
                    return True
                def remove_from_aliases():
                    try:
                        del aliases[args[0]]
                    except KeyError:
                        error(f"alias {args[0]} does not exist.")
                def clear_aliases():
                    nonlocal aliases
                    aliases = {}
                def analyse():
                    info(f"pistol's meta file is currently {os.path.getsize(meta.path) / 1024:.2f}kb large")
                    info(f"the meta file includes {len(cd_history)} cd history item(s),")
                    info(f"{len(cmd_history)} command history item(s),")
                    info(f"and {len(aliases)} alias(es).")
                    info("to free up this space, you can run:")
                    info("- cch to clear command history (usually takes up the most space)")
                    info("- ccdh to clear cd history")
                    info("- ca to clear aliases")
                    important("pistol must be restarted in order for changes to take effect")

                try:
                    commands: dict = {
                        "exit": lambda: exit_pistol(),
                        "cd": lambda: mutable_location.set(args[0], cd_history),
                        "ucd": lambda: undo_cd(),
                        "cdh": lambda: view_cd_history(),
                        "ccdh": lambda: (
                            clear_cd_history(),
                            info("cd history cleared")
                        ),
                        "solo": lambda c: run_solo(c),
                        "clear": lambda: subprocess.run("clear"),
                        "cls": lambda: subprocess.run("clear"),
                        "help": lambda: webbrowser.open("https://github.com/pixilll/pistol/issues"),
                        "version": lambda: info(f"pistol for {PLATFORM} {VERSION}"),
                        "pwsolo": lambda c: (
                            args.insert(0, "pwsh"),
                            args.insert(1, "-Command"),
                            run_solo(c)
                        ),
                        "whereami": lambda: info(f"{disp_loc}{(' ('+str(loc)+')') if str(loc) == str(STORAGE_PATH) else ''}"),
                        "root": lambda: mutable_location.set(SYS_ROOT, cd_history),
                        "search": lambda: webbrowser.open(args[0]),
                        "st": lambda: st(),
                        "rs": lambda: reverse_search(),
                        "cch": lambda: (
                            clear_command_history(),
                            info("command history cleared")
                        ),
                        "rmc": lambda: clear_from_command_history(),
                        "alias": lambda: aliases.update({args[0]: " ".join([f"\"{arg}\"" for arg in args[1:]])}),
                        "rma": lambda: remove_from_aliases(),
                        "ca": lambda: (
                            clear_aliases(),
                            info("aliases cleared")
                        ),
                        "analyse": lambda: analyse()
                    }
                    solo_commands: list[str] = [
                        "solo",
                        "pwsolo"
                    ]
                    if command in aliases.keys():
                        new, _ = parse_command(aliases[command].split(" "))
                        command = new[0]
                        args = new[1:]
                    if command in solo_commands:
                        commands[command](commands)
                    else:
                        commands[command]()
                except KeyError:
                    error(f"{command} is not a valid command")
                    hint(f"try solo {command}")
            except IndexError:
                error(f"not enough arguments supplied for {command}")
        except KeyboardInterrupt:
            print()