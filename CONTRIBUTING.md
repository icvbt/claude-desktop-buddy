# Contributing

This is a personal fork of [anthropics/claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy), adapted for the M5StickC Plus2.

The best way to build on this is to fork it and make it your own. Issues and pull requests are welcome for:

- Bugs that stop the Plus2 build, upload, pairing, or display from working
- Corrections to the setup steps in the README
- Corrections to the character pack instructions

Feature requests and ports to other boards are better as a separate fork. For protocol questions, see the upstream [REFERENCE.md](https://github.com/anthropics/claude-desktop-buddy/blob/main/REFERENCE.md).

## Before you open a PR

1. Build with `pio run -e m5stickc-plus` and confirm `[SUCCESS]`.
2. Don't commit `.pio/`, `data/`, or PlatformIO caches.
3. If you change a character pack, keep GIFs 96px wide and the folder under 1.8 MB.