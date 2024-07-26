import os
import sys
import site
from subprocess import STDOUT, Popen
from pathlib import Path
import shlex
site

BARE_REPO_NAME = ".dotfilesmgmt.git"

def get_home_dir() -> None | str:
    home_dir = None
    if os.name == "posix":
        home_dir = os.environ.get("HOME")
    elif os.name == "nt":
        home_dir = os.environ.get("USERPROFILE")
    else:
        pass
    return home_dir


def set_git_env(GIT_DIR: str, GIT_WORK_TREE: str):
    os.environ["GIT_DIR"] = GIT_DIR
    os.environ["GIT_WORK_TREE"] = GIT_WORK_TREE


def set_env():
    home_dir = None
    dotfilesmgmt_dir = None
    if (home_dir := get_home_dir()) is None:
        raise FileNotFoundError("Error: can't find home directory")
    elif not (dotfilesmgmt_dir := Path(home_dir, f"{BARE_REPO_NAME}")).exists():
        raise FileNotFoundError(f"Error: can't find ~/{BARE_REPO_NAME} dir")

    dotfilesmgmt_dir = str(dotfilesmgmt_dir)
    set_git_env(GIT_DIR=dotfilesmgmt_dir, GIT_WORK_TREE=home_dir)
    print(dotfilesmgmt_dir)
    print(home_dir)


def run_interactive_cli():
    pass
    print(exit)
    while True:
        try:
            print(f"dotfilesmgmt shell {Path.cwd()} > ", end="")
            line = input().rstrip()
            if "exit()" == line:
                raise EOFError
            elif "help" == line:
                print(exit)
                continue
        except EOFError:
            print("----exit the gotfilesmgmt----")
            break
        else:
            if line == "":
                continue
            # do arguments prase
            args = None
            # args = shlex.split(line)
            if os.name == "posix":
                args = shlex.split(line)
                if __debug__:
                    print(args)
            else:
                args = line
            try:
                proc = Popen(args, stderr=STDOUT, text=True)
                proc.wait()
            except FileNotFoundError:
                print("File not found", file=sys.stderr)


def run_subshell():
    """
    * [args, on windows as string due to implement in CreateProcess()](https://docs.python.org/zh-cn/3/library/subprocess.html#popen-constructor)
    * [about pwsh | commmand line options and arguments](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.4)
    * [pwsh prompt construct](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_prompts?view=powershell-7.4)
    * [about about quoting rules | single quote VS double quote, escape doube quote within double quote](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.4)
    * [special char - empty space](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_special_characters?view=powershell-7.4)
    """
    if "nt" == os.name:
        args = """pwsh.exe -WorkingDirectory ~ -NoExit -Command "
            $originalPromptFunc=(Get-Command prompt).ScriptBlock;
            function prompt {
                Write-Host ""(dotfilesmgmt) $(& $originalPromptFunc)"" -NoNewLine;
                return ""`0"";
            }
            """
        try:
            proc = Popen(args)
        except FileNotFoundError:
            raise
        else:
            proc.wait()  # cretical statement
    if sys.platform.startswith("linux") is True:
        if (PS1 := os.environ.get("PS1")) is None:
            print("""Error: PS1 not found!
                Please export PS1 in your ~/.bashrc
                Then `source ~/.bashrc` or `. ~/.bashrc`
            """)
            raise RuntimeError
        PS1 = "(dotfilesmgmt)" + PS1
        os.environ["PS1"] = PS1
        # bash [--long option] [-c]
        try:
            proc = Popen(["bash", "--login", "-i"], cwd=os.environ.get("HOME"))
        except FileNotFoundError:
            raise
        else:
            proc.wait()

def run_subshell2():
    """
    * [args, on windows as string due to implement in CreateProcess()](https://docs.python.org/zh-cn/3/library/subprocess.html#popen-constructor)
    * [about pwsh | commmand line options and arguments](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.4)
    * [pwsh prompt construct](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_prompts?view=powershell-7.4)
    * [about about quoting rules | single quote VS double quote, escape doube quote within double quote](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.4)
    * [special char - empty space](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_special_characters?view=powershell-7.4)
    """
    if "nt" == os.name:
        args = """pwsh.exe -NoExit -Command "
            $originalPromptFunc=(Get-Command prompt).ScriptBlock;
            function prompt {
                Write-Host ""(dotfilesmgmt) $(& $originalPromptFunc)"" -NoNewLine;
                return ""`0"";
            }
            """
        try:
            proc = Popen(args)
        except FileNotFoundError:
            raise
        else:
            proc.wait()  # cretical statement
    if sys.platform.startswith("linux") is True:
        if (PS1 := os.environ.get("PS1")) is None:
            print("""Error: PS1 not found!
                Please export PS1 in your ~/.bashrc
                Then `source ~/.bashrc` or `. ~/.bashrc`
            """)
            raise RuntimeError
        PS1 = "(dotfilesmgmt)" + PS1
        os.environ["PS1"] = PS1
        # bash [--long option] [-c]
        try:
            proc = Popen(["bash", "--login", "-i"])
        except FileNotFoundError:
            raise
        else:
            proc.wait()


def main():
    print("??? modifitable???")
    import shutil
    print(shutil.which("python"))
    print(__file__)
    try:
        set_env()
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    # run_interactive_cli()
    try:
        run_subshell2()
    except (FileNotFoundError, RuntimeError):
        return 1


if __name__ == "__main__":
    sys.exit(main())
