# Assets

This folder contains generated presentation assets for the GitHub README.

- `banner-source.png` is the source banner image generated for this project.
- `banner.webp` is the optimized README banner.
- `social-preview.jpg` is prepared for GitHub social preview upload when needed.
- `demo/legends-cursor-showcase.webp` is the full-width looping README showcase.
- `demo/legends-cursor-demo.webp` is the shorter animated README demo generated
  from a deterministic simulation of the Lua filter defaults.
- `demo/legends-cursor-demo.gif` is the GIF fallback for viewers that do not
  animate WebP.
- `demo/legends-cursor-showcase-4k60.webm` is the `3840 x 2160`, `60 fps`
  WebM version of the showcase video.
- `demo/legends-cursor-showcase-4k60.mp4` is the full `3840 x 2160`, `60 fps`
  mode-switching showcase video.
- `screenshots/*.png` are keyframes from the same deterministic demo renderer.

Regenerate optimized assets with:

```powershell
python .\tools\render_assets.py
python .\tools\render_showcase.py
```
