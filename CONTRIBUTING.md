# Contributing

Thanks for helping improve Legends OBS Cursor.

## Development Priorities

1. Preserve the original cursor look by default.
2. Add new visual ideas as optional modes or settings.
3. Keep OBS scene edits conservative and backup-first.
4. Keep Windows and PowerShell install paths working.
5. Avoid committing local OBS scene files, secrets, recordings, or workstation artifacts.

## Local Checks

Run the package validator before opening a pull request:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\validate_package.ps1
```

The validator checks required files, obvious private-path leaks, and packaging
artifacts that should stay out of git.

## Visual Changes

For changes to the shader, defaults, or click behavior, include before/after
screenshots or a short screen recording. New effects should be disabled or
selectable unless they are a strict bug fix.

## Pull Request Checklist

- [ ] The default `Legends Cursor Filter` look still includes rotating momentum ticks.
- [ ] Left-click and right-click effects remain visually distinct.
- [ ] Installer changes still backup the active OBS scene collection before editing.
- [ ] Documentation matches the current settings names.
- [ ] `tools\validate_package.ps1` passes locally.

