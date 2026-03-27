# VS Code White Window Recovery Notes

Symptom: opening a new VS Code window shows a blank white screen on Ubuntu/Linux.

Most likely cause:
- VS Code renderer or GPU acceleration failure
- Corrupted VS Code renderer cache or window state
- Stale `code` processes still running in the background

Quick recovery:

```bash
pkill -f '/usr/share/code/code'
code --disable-gpu --disable-extensions
```

If that works, make the GPU workaround permanent:

```bash
mkdir -p ~/.config/Code
printf '{\n  "disable-hardware-acceleration": true\n}\n' > ~/.config/Code/argv.json
code
```

If the white window still appears, clear caches and try again:

```bash
pkill -f '/usr/share/code/code'
rm -rf ~/.config/Code/Cache ~/.config/Code/GPUCache ~/.config/Code/'Code Cache'
code --disable-gpu --disable-extensions
```

If it is still broken, test with a clean VS Code profile:

```bash
code --user-data-dir ~/.vscode-clean --disable-gpu --disable-extensions
```

How to interpret the result:
- If the clean profile works, the main profile in `~/.config/Code` is likely corrupted.
- If `--disable-gpu` works, hardware acceleration was the issue.

Environment checked on this machine:
- OS: Ubuntu Linux
- VS Code: `1.113.0`
- Code binary: `/usr/bin/code`

Notes:
- There were multiple lingering `code` processes running when this issue was checked.
- The expected VS Code cache directories existed under `~/.config/Code/`.
