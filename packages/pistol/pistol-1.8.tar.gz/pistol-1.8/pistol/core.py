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
        if str(self.path) == str(STORAGE_PATH) and not ucd:
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
    if "-n" in sys.argv or "--new" in sys.argv:
        match PLATFORM:
            case "windows":
                subprocess_run(["cmd", "/C", "start", "python", "-m", repr(EP_MODULE), abs_at])
            case "linux":
                subprocess_run(["gnome-terminal", "--", "bash", "-c", f"cd {SYS_ROOT}; python3 -m '{EP_MODULE}' {abs_at}; exec bash"])
            case _:
                error("unidentified operating system; could not find a way to open a new terminal.")
        info("exited pistol")
        exit(0)
    mutable_location: MutablePath = MutablePath(Path(os.getcwd()))
    mutable_location.set(at, [])
    solo_mode: str = ""
    cd_history: list[str] = []
    while True:
        try:
            loc: Path = mutable_location.path
            disp_loc: str = f"{Back.YELLOW}{Fore.BLACK}storage{Style.RESET_ALL}" if str(loc) == str(STORAGE_PATH) else loc
            try:
                if solo_mode:
                    command: str = (solo_mode + " " + input(
                        f"➤➤ {Fore.YELLOW}{PLATFORM}:{Style.RESET_ALL} {disp_loc} {Fore.MAGENTA}"
                        f"[{solo_mode}]{Style.RESET_ALL}{Fore.BLUE}>{Style.RESET_ALL} ")).removeprefix(f"{solo_mode} pistol ")
                    command = command.removeprefix(f"{solo_mode} ") if command.startswith(f"{solo_mode} cd ") else command
                    if command == f"{solo_mode} exit":
                        info(f"exited {solo_mode}")
                        solo_mode = ""
                        continue
                else:
                    command: str = input(f"➤➤ {Fore.YELLOW}{PLATFORM}:{Style.RESET_ALL} {disp_loc}{Fore.BLUE}>{Style.RESET_ALL} ")
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
                    if args not in [
                        [],
                        ["pwsh", "-Command"]
                    ]:
                        force_cwd: bool = False
                        if "--force-cwd" in args:
                            args.remove("--force-cwd")
                            force_cwd = True
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
                            "root"
                        ]:
                            warning(f"{args[0]} may not work properly when executing using {name}")
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
                        nonlocal solo_mode
                        solo_mode = command
                def undo_cd():
                    try:
                        mutable_location.set(cd_history.pop(), [], ucd=True)
                    except IndexError:
                        warning("nothing left to undo")

                from . import VERSION

                try:
                    {
                        "exit": lambda: (
                            info("exited pistol"),
                            hint("pressing ^D chord to ^C will exit pistol as well") if "--no-hint" not in args else ...,
                            exit()
                        ),
                        "cd": lambda: mutable_location.set(args[0], cd_history),
                        "ucd": lambda: undo_cd(),
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
                        "st": lambda: (
                            mutable_location.set(str(STORAGE_PATH), cd_history, st=True),
                            hint("use st again to return to normal mode")
                        ) if str(loc) != str(STORAGE_PATH) else undo_cd()
                    }[command]()
                except KeyError:
                    error(f"{command} is not a valid command")
                    hint(f"try solo {command}")
            except IndexError:
                error(f"not enough arguments supplied for {command}")
        except KeyboardInterrupt:
            print()