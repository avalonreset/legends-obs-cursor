# Credits

Legends OBS Cursor is an Avalon Reset project.

## Original Design

- Original cursor art direction, rotating momentum dots, click language, and OBS use case: Benjamin / Avalon Reset.
- Production packaging, installer hardening, documentation, and optional floaty-follow controls: Avalon Reset with Codex assistance.

## Platform And Runtime

- Built for [OBS Studio](https://obsproject.com/), an open source broadcasting and recording application.
- Runs as an OBS Lua script through OBS scripting support.
- Uses LuaJIT FFI to call the Windows `user32.dll` cursor APIs at runtime.

## Third-Party Code

This repository does not intentionally vendor third-party source code or assets.
If that changes, this file should be updated before release.

## Related Optional Tools

Some local Avalon Reset OBS scenes may also use other OBS filters, such as shader
crop or rounded-corner filters. Those are not bundled in this repository.

