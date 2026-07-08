# Assets

This folder contains generated presentation assets for the GitHub README.

- `banner-source.png` is the source banner image generated for this project.
- `banner.webp` is the optimized README banner.
- `social-preview.jpg` is prepared for GitHub social preview upload when needed.
- `demo/legends-cursor-demo.webp` is the animated README demo generated from a
  deterministic simulation of the Lua filter defaults.
- `demo/legends-cursor-demo.gif` is the GIF fallback for viewers that do not
  animate WebP.
- `screenshots/*.png` are keyframes from the same deterministic demo renderer.

Regenerate optimized assets with:

```powershell
python .\tools\render_assets.py
```
