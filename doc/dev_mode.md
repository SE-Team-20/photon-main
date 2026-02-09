# Dev mode

## Why dev mode?
This is for automated testing to effectively verify implementation correctness.

With this technique, at least, we can...
- skip the splashscreen waiting time
- avoid typing in info to the table to test APIs every time

## Commands to toggle dev mode
(all written for PowerShell)

set the program to a developer mode
```powershell: set to a developer mode
$env:APP_MODE="DEV";
python main.py

```
set the program to a release mode

```powershell: set to a release mode
$env:APP_MODE="";
python main.py

```

## How to implement a dev mode if statement
Please use a function at [src/util.py](../src/util.py).

Below is a demonstration.

```py:example.py
from util import isDevMode

if __name__ == "__main__":
  if isDevMode():
    print("dev mode!")
  else:
    print("release mode!")

```