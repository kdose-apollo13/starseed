"""
    return self to chain rshifts
"""
import subprocess


class Shell:
    def __init__(self):
        self.history = []

    def __rshift__(self, command):
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True
        )
        self.history.append(result.stdout + result.stderr)
        return self

    def __iter__(self):
        yield from self.history


history = (
    Shell()
    >> "echo 'iatrogenics of money'"
    >> "seq -s ' ' 5"
    >> "ls -la"
)

for entry in history:
    print(entry)

