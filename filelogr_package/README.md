![Filelogr](https://raw.githubusercontent.com/Futuregus/filelogr/main/filelogr%20assets/filelogrlogo.png)

  ![license](https://img.shields.io/badge/license-MIT-green?style=flat) ![PyPI - Version](https://img.shields.io/pypi/v/filelogr)  ![PyPI - Downloads](https://img.shields.io/pypi/dm/filelogr) ![Static Badge](https://img.shields.io/badge/Python-4179a8?style=flat&label=Language&color=%234179a8&link=https%3A%2F%2Fwww.python.org%2F)




**File logging without the headache.**



---

## 📂 What’s Filelogr?
Filelogr is a lightweight zero dependency Python logging utility. Configure it once and forget it.
It handles writing timestamped messages to a file, printing to console with colors and most importantly it's easy to use!

---

##  📃 Features



-  Easy setup

-  Zero dependencies

- Timestamped file logging

- Color coded console output

- `@Logger.track` and `@Logger.catch` decorators for easy tracking

---
## ![Installation](https://raw.githubusercontent.com/Futuregus/filelogr/main/filelogr%20assets/cmdlogo.png) Installation

```bash

pip  install  filelogr

```

---
##  ❓ Why use filelogr?

Why not? It's simple, easy to set up, and gives you more than you'd expect from a small logging utility

---
## 🔨Usage:

All it takes is a couple lines of code and Filelogr is ready

```python
from filelogr import Logger

DATA_DIR = "path/to/data/directory"
LOG_FILE = "Example.log"


Logger.configure(data_dir=DATA_DIR, log_file=LOG_FILE)

Logger.log_action ("This is an info message.", tag="INFO", color="blue")

```


##  💬 Questions or ideas?

 **Open an issue or suggest a feature here:** [GitHub: Futuregus/filelogr/issues](https://github.com/Futuregus/filelogr/issues)

**Email at**: futuregus11@gmail.com