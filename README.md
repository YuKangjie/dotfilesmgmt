## Introduction

When we want to use git to manage the dotfiles in our home directory, we want the home directory to be treated as a git repo, but other times we don't want it to be treated as a repo by git.

Inspired by the article [Managing Dotfiles With Git](https://gpanders.com/blog/managing-dotfiles-with-git/) which written by one of the maintainer of [Neovim](https://neovim.io/), I write this piece of code of the same mechanism to help we use Git to maintain dotfiles under home directory.

### What does this package do? | Feature Approach, and Usage

After [installing and configuring](#installation-and-configuration) this package, if you run the `d5mgmt` or `d5mgmt.exe` executable in a shell, this executable will start a **subprocess** which is the current shell in interactive mode, setting following two git-related environment to the subprocess - the shell in interactive mode: the `GIT_WORK_TREE` and the `GIT_DIR`. The `GIT_WORK_TREE` is set to path of home directory (i.e., \$env:USERPFOFILE on Windows, \$HOME on LInux) and the `GIT_DIR` is set to the path of `.dotfilesmgmt.git` **bare** git repo(see also: [What is a "bare repo"?](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefbarerepositoryabarerepository)) which under the home directory.

Then if we run `git rev-parse --is-inside-work-tree` in home directory, we can get the result: the "**true**" string is output to stdout which mentions that git recognizes we are in the work(ing) tree of the bare repo since the two above git-related environment variable work. Thus, we can use git *normally* as we use git in a "not" bare repo under the home directory to manage dotfiles.

After we have managed dotfiles under the home directory already, just exit the subprocess shell (e.g., enter `exit`) and return to the shell without setting`GIT_DIR` and `GIT_WORK_TREE`.

## Installation and Configuration

* Install the `pipx' (reference: <https://pipx.pypa.io/stable/>)`
* Install this package by `pipx install dotfilesmgmt`. if you want to edit the source code to adjust this package's behavior, just run `pipx install --editable dotfilesmgmt`

* Create a bare repo named ".dotfilesmgmt.git" under the home directory by `git init --bare ~/.dotfilesmgmt.git`.
* Run the `d5mgmt` to enter the subprocess shell which has `GIT_WORK_TREE` and `GIT_DIR` environment variable setting.
* The subprocess shell will have the **shell prompt** start with `(dotfilesmgmt)`string
* stuse git to manager your dotfiles in the subprocess shell.
* Enter `exit` to exit the subprocess shell and return to the origin shell without `GIT_WORK_TREE` and `GIT_DIR` setting.

### posh-git model's git prompt string display issue

If you use Oh My Posh's themes' git segment to display git information within PowerShell installed with posh-git module, you may not see the **git prompt** string
while invoking the `d5mgmt`.

#### Solution

Run `mkdir .git` in the home directory to make a empty `.git` directory, then we can see the git's prompt string what we want after we run `d5mgmt`.

#### Possible Reason of the Issue

It seems that the **posh-git** PowerShell module not recognizes the truth we are in a repo(setting by `GIT_DIR`)'s work tree (setting by `GIT_WORK_TREE`) so that **posh-git** doesn't display the **git segment**'s prompt string as we in a **not**-bare repo.

Note: If we put our bare directory in the `.git` directly, the git prompt
of you shell will shows when we under the home path even we exit the `d5mgmt`, this is the situation we
don't want.
