<div align="center">

# Anmu-Buddy  
![build](https://img.shields.io/badge/build-passing-brightgreen)
![license](https://img.shields.io/badge/license-MIT-blue)

</div>

## About
A personal Git helper that lets you write commit messages in Notepad — no manual `git add` or `git commit` required.

## Why Anmu-Buddy Exists
Because writing commit messages in the terminal is annoying.  
Anmu-Buddy lets you type commit messages comfortably in Notepad.

## Requirements
- Python 3.9+
- Git installed and available in PATH

## Main Features
- Staging + commit  
- Staging + commit + push

## Project Structure
```bash
ANMU_BUDDY/
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

## 🚀 Installation

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
