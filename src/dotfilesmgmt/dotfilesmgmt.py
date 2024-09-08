import os
import sys
import site
from subprocess import STDOUT, Popen
from pathlib import Path
import shlex
import shutil
import re
from tempfile import NamedTemporaryFile

site

__DEBUG__ = False
# you can change the name of the executable "d5mgmt" to what
# you want in pyproject.toml
BARE_REPO_NAME = ".dotfiles.git"


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
    print("GIT_DIR:", dotfilesmgmt_dir)
    print("GIT_WORK_DIR:", home_dir)


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
            print("----exit the dotfilesmgmt----")
            break
        else:
            if line == "":
                continue
            # do arguments prase
            args = None
            # args = shlex.split(line)
            if os.name == "posix":
                args = shlex.split(line)
                if __DEBUG__:
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
    * [about pwsh | command line options and arguments](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.4)
    * [pwsh prompt construct](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_prompts?view=powershell-7.4)
    * [about about quoting rules | single quote VS double quote, escape double quote within double quote](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.4)
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
            proc.wait()  # crucial statement
    if sys.platform.startswith("linux") is True:
        if (PS1 := os.environ.get("PS1")) is None:
            print(
                """Error: PS1 not found!
                Please export PS1 in your ~/.bashrc
                Then `source ~/.bashrc` or `. ~/.bashrc`
            """
            )
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
    * [about pwsh | command line options and arguments](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.4)
    * [pwsh prompt construct](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_prompts?view=powershell-7.4)
    * [about about quoting rules | single quote VS double quote, escape double quote within double quote](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.4)
    * [special char - empty space](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_special_characters?view=powershell-7.4)
    """
    if "nt" == os.name:
        args = """pwsh.exe -NoExit -Command "
            $originalPromptFunc=(Get-Command prompt).ScriptBlock;
            function prompt {
                Write-Host ""(dotfilesmgmt) $(& $originalPromptFunc)"" -NoNewLine;
                return ""`0"";
            }
            "
            """
        try:
            proc = Popen(args)
        except FileNotFoundError:
            raise
        else:
            proc.wait()  # crucial statement
    if sys.platform.startswith("linux") is True:
        if (PS1 := os.environ.get("PS1")) is None:
            print(
                """Error: PS1 not found!
                Please export PS1 in your ~/.bashrc
                Then `source ~/.bashrc` or `. ~/.bashrc`
            """
            )
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


def run_subshell3():
    if __DEBUG__:
        print("in run_subshell3")

    if not os.path.islink(temp_path := shutil.which("d5mgmt")):
        print("""
            d5mgmt relays on venv, please use `pipx install dotfilesmgmt` to install dotfilesmgmt.
            See README.md for details on this package.
        """)
        return 1

    activate_dirname = os.path.dirname(os.readlink(temp_path))

    if "nt" == os.name:
        activate_path = os.path.join(activate_dirname, "activate.ps1")
        activate_path = re.sub(r"\\\\\?\\", "", activate_path)
        # args = f'pwsh.exe -NoExit -NoProfile -File {activate_path}'
        args = """pwsh.exe -NoExit -Command \"
            & """ + f"{{{activate_path}}}\""

        # args = """pwsh.exe -NoExit -NoProfile -Command "
        #     $originalPromptFunc=(Get-Command prompt).ScriptBlock;
        #     # function prompt {
        #     #     Write-Host ""(dotfilesmgmt) $(& $originalPromptFunc)"" -NoNewLine;
        #     #     return ""`0"";
        #     # };
        #     Import-Module posh-git
        #     """
        try:
            proc = Popen(args)
        except FileNotFoundError:
            raise
        else:
            proc.wait()  # critical
    elif "posix" == os.name:
        # step1: activate file detect
        activate_str = None
        activate_path = os.path.join(activate_dirname, "activate")
        if __DEBUG__:
            print(activate_path)
        with open(activate_path, "r") as f:
            activate_str = f.read()

        # step2: shell detect
        shell = None
        if (shell := os.environ.get("SHELL")) is None:
            print("$SHELL environ variable is not found!", file=sys.stderr)
            return 1
        shell_name = re.search(r"[^/]+$", shell).group(0)
        if __DEBUG__:
            print(shell_name)
        if shell_name not in ["bash"]:
            print("this program only support bash in posix platform now", file=sys.stderr)
            return 1

        # step3: shell profile detect
        if shell_name == "bash":
            profile_str = None
            try:
                for profile in (profiles := ['~/.bash_profile', '~/.bash_login', '~/.profile']):
                    if os.path.isfile((profile_path := os.path.expanduser(profile))):
                        with open(profile_path, "r") as f:
                            profile_str = f.read()
                            if __DEBUG__:
                                print(f"the profile file is {profile_path}")
                            break
            except Exception as e:
                print(f"Error in reading profile: {e}", file=sys.stderr)
        else:
            return 1
        
        temp_file = None
        temp_file_path = None
        try:
            temp_file = NamedTemporaryFile(mode='w+', delete=True)
            temp_file_path = temp_file.name
            temp_file.write(profile_str + activate_str)
            if temp_file.seekable():
                temp_file.seek(0) # key point
        except Exception as e:
            print(f"Error about temp file: {e}", file=sys.stderr)
        else:
            try:
                if __DEBUG__:
                    proc = Popen(["cat", str(temp_file_path)])
                else:
                    proc = Popen([shell, "--rcfile", temp_file_path])
            except RuntimeError as e:
                print(e, file=sys.stderr)
            else:
                proc.wait()
                # stdout, stderr = proc.communicate()
                # print(f"stdout: {stdout}"); print(f"stderr {stderr}")
        finally:
            if temp_file is not None and not temp_file.closed:
                temp_file.close()

def main():
    if __DEBUG__:
        print("-- in main --")
    if __DEBUG__:
        print(shutil.which("python"))
    if __DEBUG__:
        print(__file__)
    try:
        set_env()
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    # run_interactive_cli()
    try:
        run_subshell3()
    except (FileNotFoundError, RuntimeError):
        return 1
    else:
        print("exit dotfilesmgmt")

if __name__ == "__main__":
    sys.exit(main())
