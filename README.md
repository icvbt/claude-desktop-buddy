<p align="center">
  <img src="characters/clawdie/sleep.gif" alt="clawdie sleep" width="96">
  <img src="characters/clawdie/idle.gif" alt="clawdie idle" width="96">
  <img src="characters/clawdie/busy.gif" alt="clawdie busy" width="96">
  <img src="characters/clawdie/attention.gif" alt="clawdie attention" width="96">
  <img src="characters/clawdie/celebrate.gif" alt="clawdie celebrate" width="96">
  <img src="characters/clawdie/dizzy.gif" alt="clawdie dizzy" width="96">
  <img src="characters/clawdie/heart.gif" alt="clawdie heart" width="96">
</p>

<h1 align="center">CLAUDE DESKTOP BUDDY · PLUS2 EDITION</h1>

<p align="center">
  <b>A pixel companion for your Claude sessions.</b><br>
  sleep &nbsp;→&nbsp; idle &nbsp;→&nbsp; busy &nbsp;→&nbsp; attention &nbsp;→&nbsp; celebrate &nbsp;→&nbsp; dizzy &nbsp;→&nbsp; heart
</p>

---

> This is a fork of [anthropics/claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy) adapted for the M5StickC Plus2.

Claude for macOS and Windows can connect Claude Cowork and Claude Code to maker devices over BLE, so developers and makers can build hardware that displays permission prompts, recent messages, and other interactions. We've been impressed by the creativity of the maker community around Claude - providing a lightweight, opt-in API is our way of making it easier to build fun little hardware devices that integrate with Claude.

> **Building your own device?** You don't need any of the code here. See **[REFERENCE.md](https://github.com/anthropics/claude-desktop-buddy/blob/main/REFERENCE.md)** for the wire protocol: Nordic UART Service UUIDs, JSON schemas, and the folder push transport.

As an example, we built a desk pet on ESP32 that lives off permission approvals and interaction with Claude. It sleeps when nothing's happening, wakes when sessions start, gets visibly impatient when an approval prompt is waiting, and lets you approve or deny right from the device.

---

## What's Here

```
┌─────────────────────────────────────────────────────────────┐
│ 12-hour clock       shows 2:05, not 14:05                   │
│ Clawdie pixel pet   seven 96px GIF states over USB          │
│ Plus2 support       M5Unified build (from PR #3)            │
│ State tester        busy and attention over serial          │
└─────────────────────────────────────────────────────────────┘
```

## Project Layout

```
claude-desktop-buddy/
├── src/main.cpp                 firmware (12-hour clock lives here)
├── characters/clawdie/          manifest.json + 7 GIF states
├── tools/
│   ├── flash_character.py       USB character flasher
│   └── test_states_win.py       busy / attention tester
└── REFERENCE.md                 BLE protocol and folder transfer
```

## How It Works

```
Claude Desktop ──BLE──▶ M5StickC Plus2 ──▶ state
                              ▲
PC (USB) ── flash_character.py┘   GIFs written to storage
PC (USB) ── test_states_win.py┘   fake JSON states for testing
```

- **Firmware:** PlatformIO + M5Unified
- **Bluetooth:** Hardware Buddy pairs and streams state
- **Characters:** 96px-wide GIFs, one per state
- **Testing:** serial JSON, no Claude needed

---

<details>
<summary><b>Prerequisites</b></summary>

- **Windows 10 or 11** (the commands below are for PowerShell)
- **An M5StickC Plus2** and a **USB-C cable that carries data**. Charge-only cables are not detected by PlatformIO.
- **Claude Desktop** (macOS or Windows), for Bluetooth pairing
- **Git for Windows**: [git-scm.com/downloads/win](https://git-scm.com/downloads/win)
- **Python 3.11 or newer**: [python.org/downloads](https://www.python.org/downloads/). During install, tick **Add python.exe to PATH**.

</details>

---

<details>
<summary><b>Install PlatformIO</b></summary>

PlatformIO is the build and upload tool. Pick one of the two options below.

**Option A: VS Code (easiest)**

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Open **Extensions** (Ctrl+Shift+X), search for **PlatformIO IDE**, and install it.
3. Restart VS Code. The first start downloads the core packages, which takes a few minutes.
4. Open the `claude-desktop-buddy` folder with **File → Open Folder**. PlatformIO detects `platformio.ini` automatically.

**Option B: Command line only**

```powershell
python -m pip install --upgrade platformio
pio --version
```

If `pio` is not recognized, the Scripts folder isn't on your PATH. Add it for the current window:

```powershell
$env:PATH = "$env:USERPROFILE\.platformio\penv\Scripts;" + $env:PATH
```

To make it permanent, add that folder under **Settings → Environment Variables → Path**. Or skip PATH entirely and run `python -m platformio` in place of `pio`.

Check the install:

```powershell
pio --version
```

</details>

---

<details>
<summary><b>First-Time Setup</b></summary>

Run each line in **PowerShell**, from a folder you want the project in.

**1. Clone and switch to the Plus2 branch**

```powershell
git clone https://github.com/YOURUSERNAME/claude-desktop-buddy.git
cd claude-desktop-buddy
git checkout clawdie
```

**2. Install the Python packages the tools use**

```powershell
python -m pip install pillow pyserial
```

**3. Build (checks the toolchain, doesn't flash)**

The first build downloads the ESP32 toolchain and can take several minutes.

```powershell
pio run -e m5stickc-plus
```

Wait for `[SUCCESS]`.

**4. Flash the firmware**

> Close Claude Desktop first, then plug the stick in over USB-C.

```powershell
pio run -e m5stickc-plus -t upload
```

Wait for `[SUCCESS]`, then unplug and replug the stick.

If the stick has old firmware and behaves oddly, wipe it first:

```powershell
pio run -e m5stickc-plus -t erase
pio run -e m5stickc-plus -t upload
```

You can also factory reset from the device: hold **A → Settings → Reset → Factory Reset**, then tap twice to confirm.

**5. Flash the clawdie pack over USB**

```powershell
python tools\flash_character.py characters\clawdie
```

> If PlatformIO starts building `m5stack-sticks3`, press **Ctrl+C**. That's a different board, and you don't need it.

**6. Pair with Claude Desktop**

1. In Claude Desktop, go to **Help → Troubleshooting → Enable Developer Mode**.
2. Go to **Developer → Open Hardware Buddy**.
3. Click **Connect** and pick the stick from the list.
4. Grant Bluetooth permission if Windows asks.

</details>

---

<details>
<summary><b>Pin the ESP32 platform version (optional)</b></summary>

PlatformIO updates the ESP32 platform automatically. A newer release can occasionally break a working build. If that happens, open `platformio.ini`, find the `[env:m5stickc-plus]` section, and set the platform to the version this project was built with:

```ini
platform = espressif32@7.1.3
```

Then rebuild with `pio run -e m5stickc-plus`.

</details>

---

## Pairing

To pair your device with Claude, first enable developer mode (**Help → Troubleshooting → Enable Developer Mode**). Then open the Hardware Buddy window in **Developer → Open Hardware Buddy…**, click **Connect**, and pick your device from the list. On macOS, grant Bluetooth permission when prompted. On Windows, allow Bluetooth access if asked.

Once paired, the bridge reconnects automatically whenever both sides are awake.

If discovery isn't finding the stick:

- Make sure it's awake (press any button).
- Check the stick's settings menu and confirm Bluetooth is on.
- Keep the stick within about a metre of the PC, with other Bluetooth devices turned off.
- If the panel says **Disconnected**, click **Connect** again before sending anything.

**Plus2 note:** Over Bluetooth, large folder transfers timed out on our setup. If a full character pack fails, send it in smaller batches (see [GIF pets](#gif-pets)), or flash it over USB with `tools\flash_character.py`.

## Controls

| Button | Normal | Approval |
| --- | --- | --- |
| **A** (front) | Next screen | Approve |
| **B** (right) | Next page | Deny |
| **Hold A** | Settings | Settings |
| **Power** (short) | Screen off | — |

The screen turns off after 30 seconds of inactivity and stays on while an approval is waiting. Any button press wakes it.

## ASCII pets

The default buddy is an ASCII pet. Each of the eighteen species has seven animations: sleep, idle, busy, attention, celebrate, dizzy, and heart. Use **Menu → next pet** to cycle through them, and the choice is saved to the device.

## GIF pets

To use a custom GIF character instead of an ASCII buddy, drag a character pack folder onto the drop target in the Hardware Buddy window. The app streams it over Bluetooth, and the stick switches to GIF mode live. To go back to ASCII, use **Settings → delete char** on the stick.

A character pack is a folder with a `manifest.json` and 96px-wide GIFs, one per state:

```json
{
  "name": "clawdie",
  "colors": {
    "body": "#D97757",
    "bg": "#000000",
    "text": "#FFFFFF",
    "textDim": "#808080",
    "ink": "#000000"
  },
  "states": {
    "sleep": "sleep.gif",
    "idle": "idle.gif",
    "busy": "busy.gif",
    "attention": "attention.gif",
    "celebrate": "celebrate.gif",
    "dizzy": "dizzy.gif",
    "heart": "heart.gif"
  }
}
```

A state can also be an array of GIFs. Each loop-end advances to the next file, which keeps the home screen from repeating one clip forever.

**Tips for making character packs:**

- GIFs must be **96px wide** and no taller than about **140px**, which fits the 135×240 portrait screen.
- The whole folder must stay under **1.8 MB**.
- Compress with `gifsicle --lossy=80 -O3 --colors 64 input.gif -o output.gif`. It usually cuts the size by 40–60%.
- `tools/prep_character.py` resizes source GIFs to the right width, keeping the character at the same scale in every state.
- To flash a pack over USB instead of Bluetooth, close Claude Desktop and run `python tools\flash_character.py characters\clawdie`.

See `characters/clawdie/` for a working example.

---

## The Seven States

| GIF | State | Shown when |
| --- | --- | --- |
| <img src="characters/clawdie/sleep.gif" width="64"> | `sleep` | Not connected |
| <img src="characters/clawdie/idle.gif" width="64"> | `idle` | Connected, nothing running |
| <img src="characters/clawdie/busy.gif" width="64"> | `busy` | A session is running |
| <img src="characters/clawdie/attention.gif" width="64"> | `attention` | An approval is waiting |
| <img src="characters/clawdie/celebrate.gif" width="64"> | `celebrate` | Level up (every 50K tokens) |
| <img src="characters/clawdie/dizzy.gif" width="64"> | `dizzy` | You shook the stick |
| <img src="characters/clawdie/heart.gif" width="64"> | `heart` | You approved in under 5 seconds |

---

<details>
<summary><b>Test Without Claude</b></summary>

1. Close Claude Desktop, or disconnect Hardware Buddy.
2. Find the stick's COM port in **Device Manager** (under **Ports (COM & LPT)**).
3. Set `PORT` at the top of `tools\test_states_win.py` to match.
4. Run:

```powershell
python tools\test_states_win.py
```

The stick shows **busy** for 10 seconds, then **attention** for 10 seconds, then the script prints `done`.

</details>

---

<details>
<summary><b>Troubleshooting</b></summary>

| Problem | Fix |
| --- | --- |
| `pio` not recognized | Add `%USERPROFILE%\.platformio\penv\Scripts` to PATH, or use `python -m platformio` |
| `python` not recognized | Reinstall Python and tick **Add python.exe to PATH** |
| `&&` is not a valid separator | Run each command on its own line |
| Upload fails or the port isn't found | Use a data-capable USB-C cable, close Claude Desktop, and replug the stick |
| Stick shows old firmware or won't boot after a flash | Run the erase and upload commands in step 4 |
| `chunk ack timeout` over Bluetooth | Reconnect, keep the stick close, or flash over USB |
| `Could not resolve host` | Run `ipconfig /flushdns`, then retry |
| `git push` returns HTTP 408 | Run `git config http.postBuffer 524288000`, then push again |
| Low disk space | Run `pio run -t clean`, then `pio system prune` |

</details>

---

## More

- **[REFERENCE.md](REFERENCE.md)**: Bluetooth protocol, JSON schemas, folder transfer format

## Credits

- Firmware base: [anthropics/claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy)
- Clawdie sprite: adapted from [bryant24hao/deskpet-firmware](https://github.com/bryant24hao/deskpet-firmware)
- Setup steps adapted from the [OpenELAB StickS3 tutorial](https://www.hackster.io/openelab/claude-desktop-buddy-tutorial-sticks3-cardputer-48f922)
- Built with help from Claude (Anthropic).
