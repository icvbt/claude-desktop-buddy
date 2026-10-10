<p align="center">
  <img src="characters/clawdie/idle.gif" alt="clawdie idle" width="96">
  <img src="characters/clawdie/busy.gif" alt="clawdie busy" width="96">
  <img src="characters/clawdie/attention.gif" alt="clawdie attention" width="96">
  <img src="characters/clawdie/celebrate.gif" alt="clawdie celebrate" width="96">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/M5StickC%20Plus2-ESP32--PICO-ff6b35?style=for-the-badge" alt="M5StickC Plus2">
  <img src="https://img.shields.io/badge/PlatformIO-Arduino-orange?style=for-the-badge&logo=platformio" alt="PlatformIO">
  <img src="https://img.shields.io/badge/Claude%20Desktop-Buddy-d97757?style=for-the-badge" alt="Claude Desktop Buddy">
  <img src="https://img.shields.io/badge/platform-Windows-0078d6?style=for-the-badge&logo=windows" alt="Windows">
</p>

<h1 align="center">CLAUDE DESKTOP BUDDY · PLUS2 EDITION</h1>

<p align="center">
  <b>A pixel companion for your Claude sessions.</b><br>
  sleep &nbsp;→&nbsp; idle &nbsp;→&nbsp; busy &nbsp;→&nbsp; attention &nbsp;→&nbsp; celebrate &nbsp;→&nbsp; dizzy &nbsp;→&nbsp; heart
</p>

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
<summary><b>First-Time Setup</b></summary>

Run each line in **PowerShell**, from the project folder.

**1. Clone and switch branch**
```powershell
git clone https://github.com/YOURNAME/claude-desktop-buddy.git
cd claude-desktop-buddy
git checkout m5unified-pr3
```

**2. Install Python packages**
```powershell
C:\Users\Lenovo\.platformio\penv\Scripts\python.exe -m pip install pillow pyserial
```

**3. Build (checks the toolchain, doesn't flash)**
```powershell
C:\Users\Lenovo\.platformio\penv\Scripts\pio.exe run -e m5stickc-plus
```

**4. Flash the firmware**

> Close Claude Desktop first, then plug the stick in over USB-C.

```powershell
C:\Users\Lenovo\.platformio\penv\Scripts\pio.exe run -e m5stickc-plus -t upload
```

**5. Flash the clawdie pack**
```powershell
C:\Users\Lenovo\.platformio\penv\Scripts\python.exe tools\flash_character.py characters\clawdie
```

> If it starts building `m5stack-sticks3`, press **Ctrl+C**. That's a different board.

**6. Pair with Claude Desktop**

1. **Help → Troubleshooting → Enable Developer Mode**
2. **Developer → Open Hardware Buddy**
3. Click **Connect** and pick the stick

</details>

---

## Controls

| Button | Normal | Approval |
| --- | --- | --- |
| **A** (front) | Next screen | Approve |
| **B** (right) | Next page | Deny |
| **Hold A** | Settings | Settings |
| **Power** (short) | Screen off | — |

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
2. Find the stick's COM port in **Device Manager**.
3. Set `PORT` at the top of `tools\test_states_win.py`.
4. Run:

```powershell
C:\Users\Lenovo\.platformio\penv\Scripts\python.exe tools\test_states_win.py
```

The stick shows **busy** for 10 seconds, then **attention** for 10 seconds, then the script prints `done`.

</details>

---

<details>
<summary><b>Troubleshooting</b></summary>

| Problem | Fix |
| --- | --- |
| `pio` not recognized | Use the full path shown in setup |
| `&&` is not a valid separator | Run each command on its own line |
| `chunk ack timeout` over Bluetooth | Reconnect, keep the stick close, or flash over USB |
| `Could not resolve host` | `ipconfig /flushdns`, then retry |
| `git push` returns HTTP 408 | `git config http.postBuffer 524288000`, then push again |
| Low disk space | `pio run -t clean`, then `pio system prune` |

</details>

---

## More

- **[REFERENCE.md](REFERENCE.md)**: Bluetooth protocol, JSON schemas, folder transfer format

## Credits

- Firmware base: [anthropics/claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy)
- Clawdie sprite: adapted from [bryant24hao/deskpet-firmware](https://github.com/bryant24hao/deskpet-firmware)
