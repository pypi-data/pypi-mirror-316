import os, sys, subprocess, readline, webbrowser, platform # NOQA
# above line is noqa due to readline not being used.

from pathlib import Path
from colorama import Style, Fore, Back

DIR: Path = Path(__file__).parent
SYS_ROOT: str = os.path.abspath(os.sep)
STORAGE_PATH: Path = DIR / "storage"
EP_MODULE: str = str(DIR).removeprefix(SYS_ROOT).replace("\\", "/").replace("/", ".")
PLATFORM: str = platform.system().lower()

def error(text: str) -> None:
    print(f"🚨 {Fore.RED}error: {text}{Style.RESET_ALL}")
def hint(text: str) -> None:
    print(f"💡 {Fore.BLUE}hint: {text}{Style.RESET_ALL}")
def warning(text: str) -> None:
    print(f"⚠️  {Fore.YELLOW}warning: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def important(text: str) -> None:
    print(f"⚠️  {Back.YELLOW}{Fore.BLACK}important: {text}{Style.RESET_ALL}")
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
        if not os.path.exists(str(self.path)) and st:
            warning("storage directory does not exist, creating now.")
            os.mkdir(str(self.path))
            info("storage directory created successfully")
        if not os.path.exists(str(self.path)):
            error(f"{self.path} is not a valid path.")
            self.path = old_path
        else:
            cd_history.append(str(old_path))

def subprocess_run(command: list[str]):
    try:
        subprocess.run(command)
    except Exception as exc:
        error(f"solo: {exc}")

def main() -> None:
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
    mutable_location.set(at, [], st=at==str(STORAGE_PATH))
    solo_mode: str = ""
    cd_history: list[str] = []
    while True:
        try:
            loc: Path = mutable_location.path
            disp_loc: str = f"{Back.YELLOW}{Fore.BLACK}storage{Style.RESET_ALL}" if str(loc) == str(STORAGE_PATH) else loc
            try:
                if solo_mode:
                    command: str = (solo_mode + " " + input(
                        f"➤➤ {Fore.YELLOW}{os.name}:{Style.RESET_ALL} {disp_loc} {Fore.MAGENTA}"
                        f"[{solo_mode}]{Style.RESET_ALL}{Fore.BLUE}>{Style.RESET_ALL} ")).removeprefix(f"{solo_mode} pistol ")
                    command = command.removeprefix(f"{solo_mode} ") if command.startswith(f"{solo_mode} cd ") else command
                    if command == f"{solo_mode} exit":
                        info(f"exited {solo_mode}")
                        solo_mode = ""
                        continue
                else:
                    command: str = input(f"➤➤ {Fore.YELLOW}{os.name}:{Style.RESET_ALL} {disp_loc}{Fore.BLUE}>{Style.RESET_ALL} ")
            except EOFError:
                print()
                try:
                    import getpass

                    hint("press ^C to exit pistol")
                    hint("press any other button to return to pistol")

                    getpass.getpass(f"➤➤ ")
                    continue
                except KeyboardInterrupt:
                    command: str = "exit --no-hint"
                    print()
                except EOFError:
                    print()
                    continue

            # Split command into parts
            parts: list[str] = command.split(" ")
            new: list[str] = []
            string: str = ""

            for part in parts:
                if not part:
                    # Skip empty parts
                    continue
                elif string:
                    # If currently inside a quoted string
                    if part[-1] == string:
                        # Closing quote found
                        new[-1] += " " + part[:-1]
                        string = ""
                    else:
                        # Append part to the current quoted string
                        new[-1] += " " + part
                elif part[0] in "\"'":
                    # Opening quote found
                    if len(part) > 1 and part[-1] == part[0]:
                        # Handle single-word quoted strings
                        new.append(part[1:-1])
                    else:
                        # Start a new quoted string
                        new.append(part[1:])
                        string = part[0]
                else:
                    # Regular unquoted part
                    new.append(part)
            if string:
                error("unclosed string in command.")
                continue

            if not new:
                continue

            command: str = new[0]
            args: list[str] = new[1:]

            try:
                def run_solo():
                    nonlocal solo_mode

                    if args not in [
                        [],
                        ["pwsh", "-Command"]
                    ]:
                        force_cwd: bool = "--force-cwd" in args
                        args.remove("--force-cwd") if "--force-cwd" in args else ...
                        if args[0] in [
                            "cd",
                            "exit",
                            "help",
                            "version",
                            "clear",
                            "cls",
                            "st",
                            "ucd",
                            "search",
                            "whereami",
                            "cdh"
                            "root",
                            "pwsolo"
                        ]:
                            warning(f"{args[0]} may not work properly when executing using {solo_mode}")
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

                from . import VERSION

                try:
                    {
                        "exit": lambda: (
                            info("exited pistol"),
                            hint("pressing ^D chord to ^C will exit pistol as well") if "--no-hint" not in args else ...,
                            hint("press ^D to exit the terminal entirely") if running_as_new else ...,
                            exit()
                        ),
                        "cd": lambda: mutable_location.set(args[0], cd_history),
                        "ucd": lambda: undo_cd(),
                        "cdh": lambda: view_cd_history(),
                        "solo": lambda: run_solo(),
                        "clear": lambda: subprocess.run("clear"),
                        "cls": lambda: subprocess.run("clear"),
                        "help": lambda: webbrowser.open("https://github.com/pixilll/pistol"),
                        "version": lambda: info(f"pistol for {PLATFORM} {VERSION}"),
                        "pwsolo": lambda: (
                            args.insert(0, "pwsh"),
                            args.insert(1, "-Command"),
                            run_solo()
                        ),
                        "whereami": lambda: info(f"{disp_loc}{(' ('+str(loc)+')') if str(loc) == str(STORAGE_PATH) else ''}"),
                        "root": lambda: mutable_location.set(SYS_ROOT, cd_history),
                        "search": lambda: webbrowser.open(args[0]),
                        "st": lambda: st()
                    }[command]()
                except KeyError:
                    error(f"{command} is not a valid command")
                    hint(f"try solo {command}")
            except IndexError:
                error(f"not enough arguments supplied for {command}")
        except KeyboardInterrupt:
            print()