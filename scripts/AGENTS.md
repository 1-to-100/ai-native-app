# AGENTS.md — scripts/

The programs here enforce the repository mechanically.

- `check.py` reports findings and does not edit a governed document.
- `setup-scripts.py` manages vendor skill symlinks and does not edit a skill or a governed document.
- Keep scripts on the Python standard library.
- When a format, process, inventory, or reference rule changes, update `check.py` in the same change.
- When a script is added or renamed, update `scripts/README.md` in the same change.
- Regression tests live in `scripts/tests/`. They are not inventoried scripts.
- Do not put credentials in a script, a fixture, or a test output that gets committed.
