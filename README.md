<div align="center">
    
# Anmu-Buddy 

</div>

## About
Anmu-Buddy is a lightweight Git helper tool that automates staging, committing, and pushing — using Notepad as your commit message editor.
It is designed for developers who prefer writing commit messages comfortably in a text editor instead of the terminal.

## Requirements
- Python 3.9+
- Git installed and available in PATH

## Features
- Write commit messages in Notepad automatically
- Auto-stage files after saving Notepad
- Support for multiple files
- Combined staging + commit + push
- Clean CLI commands (anmubuddy git ...)

## Why Not Just Use Git Normally?
- Git already works well, but Anmu-Buddy focuses on simplifying repetitive workflows.
- Perfect for users who:
- dislike writing commit messages in the terminal
- prefer full-screen editing
- want faster commit cycles
- often forget to run multiple commands

## How it works
![Image](https://github.com/user-attachments/assets/a5161a52-6758-485e-8f2e-85e9095f5b07)
1. You run the command
2. Notepad opens with a temporary file
3. You write your commit message
4. When you save & close Notepad → the tool automatically:
    - stages the specified files
    - commits with your message
    - optionally pushes (if using git push)

## Roadmap
- [ ] Add template-based commit messages
- [ ] Auto-check Git username/email
- [ ] Confirmation prompts before committing/pushing
- [ ] Al-generated commit message (optional future)
- [ ] Refactor codebase
- [ ] Better error handling
    
## Project Structure
```bash
anmu_buddy/
├── src/
│   └── anmu_buddy/
│       ├── core/
│       │   ├── __init__.py
│       │   ├── file_utils.py
│       │   ├── git_utils.py
│       │   ├── input_helper.py
│       │   └── validator.py
│       ├── git/
│       │   ├── __init__.py
│       │   ├── cli.py
│       │   └── service.py
│       └── cli.py
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
````

## Installation

Clone the repository:

```bash
git clone https://github.com/fakhrulnurmulyana/commit-anmu
```

Enter the project directory:

```bash
cd commit-anmu
```

Install the package:

```bash
pip install -e .
```

## How to Use

### Staging + Commit

**Single file:**

```bash
anmubuddy git commit -f file_to_commit
```

**Multiple files:**

```bash
anmubuddy git commit -f file1_to_commit -f file2_to_commit
```

---

### Staging + Commit + Push

**Single file:**

```bash
anmubuddy git push -f file_to_commit
```

**Multiple files:**

```bash
anmubuddy git push -f file1_to_commit -f file2_to_commit
```

## 📄 License
This project is licensed under the MIT License — see the `LICENSE` file for details.


