# Release Checklist

Use this checklist before making a public GitHub release.

## Code

- [ ] `tools\validate_package.ps1` passes.
- [ ] OBS loads `legends_cursor_filter.lua` without script errors.
- [ ] `Legends Cursor Filter` appears in the OBS filter list.
- [ ] Default settings show rotating momentum ticks.
- [ ] Right-click still uses the magenta diamond treatment.
- [ ] Floaty follow can be enabled and disabled.

## Installer

- [ ] OBS is closed before install testing.
- [ ] Installer backs up the active scene collection.
- [ ] Installer preserves `Legends Cursor Filter`.
- [ ] Installer preserves `legends_cursor_filter`.
- [ ] `-LaunchObs` starts OBS from the correct working directory.

## Documentation

- [ ] README screenshots match the current visual defaults.
- [ ] `CREDITS.md` has any new third-party attribution.
- [ ] `CHANGELOG.md` has release notes.
- [ ] GitHub topics and description are set.
- [ ] Social preview image is uploaded after the repo becomes public.

## GitHub Release

- [ ] Tag uses semantic versioning, such as `v0.1.0`.
- [ ] Release notes include install steps and OBS version tested.
- [ ] Release zip excludes local OBS config, recordings, and workstation artifacts.

