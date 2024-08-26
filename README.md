## # Using dotfilesmgmt to manager your dotfiles(configuration files) under your home directory

## Introduction

When we want to use git to manage the dotfiles in our home directory, we want the home directory to be treated as a git repo, but other times we don't want it to be treated as a repo by git.

Inspired by the article [Managing Dotfiles With Git](https://gpanders.com/blog/managing-dotfiles-with-git/) which written by one of the maintainer of [Neovim](https://neovim.io/), I write this piece of code of the similar mechanism to help we use Git to maintain dotfiles under home directory.

You can use it in PowerShell or Bash in current version, other shells have not been tested not yet.

## Installation and Configuration and Usage

* Install the `pipx` (reference: <https://pipx.pypa.io/stable/>)`
* Install this package by `pipx install dotfilesmgmt`. if you want to edit the source code to adjust this package's behavior, just run `pipx install --editable dotfilesmgmt`
* Create a bare repo named ".dotfiles.git" under the home directory by `git init --bare ~/.dotfiles.git`.
* If you use bash, please export your \$PS1 variable such as appending `export PS1` in your
`~/.bashrc`.
* Run the `d5mgmt` to enter the subprocess shell which has `GIT_WORK_TREE` and `GIT_DIR` environment variable setting.

The subprocess shell will have the **shell prompt** start with `(dotfilesmgmt)`string, then you
can:

* Use git to manager your dotfiles in the subprocess shell.
* Enter `exit` to exit the subprocess shell(this action will also exit the d5mgmt program) and return to the origin shell without `GIT_WORK_TREE` and `GIT_DIR` setting.
* All done.

### What does this package do? | Feature Approach, and Usage

After [installing and configuring](#installation-and-configuration) this package, if you run the `d5mgmt` or `d5mgmt.exe` executable in a shell, this executable will start a **subprocess** — the new instance of the shell interpreter, and setting following two git-related environment variable to the subprocess: the `GIT_WORK_TREE` and the `GIT_DIR`. The `GIT_WORK_TREE` is set to path of home directory (i.e., `$env:USERPFOFILE` on Windows, `$HOME` on LInux) and the `GIT_DIR` is set to the path of `.dotfiles.git` **bare** git repo(see also: [What is a "bare repo"?](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefbarerepositoryabarerepository)) which under the home directory.

Then if we run `git rev-parse --is-inside-work-tree` in home directory, we can get the result: the "**true**" string is outputted to stdout which mentions that git recognizes we are in the work(ing) tree of the bare repo because of two above git-related environment variable. Thus, we can use git *normally* as what we use git in a "**not**" bare repo under the home directory to manage dotfiles.

After we have managed dotfiles under the home directory already, just exit the subprocess shell (e.g., enter `exit`) and return to the shell which doesn't setting`GIT_DIR` and `GIT_WORK_TREE`.

### If you meet oh-my-posh's "[git segment](https://ohmyposh.dev/docs/segments/scm/git)" display issue after running `d5mgmt` in PowerShell, how to solve it?

#### How to solve it? - two steps

1. Install **posh-git** module and `Import-Module posh-git` in your pwsh \$profile.

2. Insert the following JavaScript object before or after the **git-segment**'s object in the `"segments": []` list in the **oh-my-posh theme** which you used:

```json
{
	"type": "text",
	"style": "plain",
	"template": "{{if .Segments.Git}}{{else}}{{if .Env.POSH_GIT_STRING}}git:{{ .Env.POSH_GIT_STRING }}{{end}}{{end}}",
	"properties": {
	}
},
```

**Explain the "template" property above**: using the [cross-segment-template-properties](https://ohmyposh.dev/docs/configuration/templates#cross-segment-template-properties) `.Segments.Git` in this ["text" segment](https://ohmyposh.dev/docs/segments/system/text)'s template". If the `.Segments.Git` is empty and the `.Env.POSH_GIT_STRING` (the `$env:POSH_GIT_STRING` itself) is not empty, show the `$env:POSH_GIT_STRING` in the shell prompt.

#### The issue of oh-my-posh's "git segment" which we can solve(bypass) by above method.

In PowerShell,   if we set the `$env:GIT_DIR` and `$env:GIT_WORK_TREE`, [**posh-git**](https://github.com/dahlbyk/posh-git) module can  recognize which is the bare repo and which is the work tree of the bare repo but oh-my-posh's [**git segment**](https://ohmyposh.dev/docs/segments/scm/git) can't. 

Here is the example  showing the differences between **posh-git** and **oh-my-posh** (support the posh-git and oh-my-posh already installed and the `$env:GIT_DIR` and `$env:GIT_WORK_TREE` are not set at the beginning):

##### §About **posh-git**:

1. Run`pwsh.exe -NoProfile` to start a PowerShell session without any PowerShell **`$PROFILE`** (see also: [about_Profiles](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.4))

2. Enter `Import-Module posh-git` to import the module.

3. `cd ~/.dotfiles.git` to into the **bare repo**, the value of **posh-git**'s **git string** (value of `$env:POSH_GIT_STRING`) is automatically appended to the shell prompt.

4. Now, outside the bare repo (e.g.: `cd ~`), the `$env:POSH_GIT_STRING` be **empty** , then:

   1. set `$env:GIT_DIR` to the path of the bare repo (e.g.: `$env:GIT_DIR="C:\Users\User\.dotfiles.git"`)

   2. set `$env:GIT_WORK_TREE` to our home directory (e.g.: `$env:GIT_WORK_TREE="C:\Users\User"`)

   we can see the `$env:POSH_GIT_STRING` appends to the   shell string.

##### §About **oh-my-posh**:

1. Running `pwsh.exe` without options and without arguments in above step 1 will load **\$Profile** file automatically. If we have `oh-my-posh init pwsh --config "path\to\oh-my-posh\theme.json" | Invoke-Expression` in **$PROFILE**, The **oh-my-posh** will use **git segment** to show the git prompt string,

2. Same as above §[About posh-git](#about-posh-git) step 2.
3. `cd  ~/.dotfiles.git` as above step 3, but now the git prompt is display by **git segment**.
4. Same as above step 4, after we set those two variable, the **git segment** is <mark>missing in shell prompt</mark> although we can also get the value of`$env:POSH_GIT_STRING`provided by **posh-git** in stdout by run `$env:POSH_GIT_STRING`.

Solution see [How to solve it?](#how-to-solve-it---two-steps) above.
