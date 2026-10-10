import json, time, serial

PORT = "COM3"   # check Device Manager; it was COM3 for the last flash
s = serial.Serial(PORT, 115200)

busy = {"total": 4, "running": 3, "waiting": 0,
        "msg": "test busy", "tokens": 0, "tokens_today": 0}
attention = {"total": 1, "running": 1, "waiting": 1,
             "msg": "test attention", "tokens": 0, "tokens_today": 0,
             "prompt": {"id": "t1", "tool": "Bash", "hint": "test"}}

for name, state, secs in [("busy", busy, 10), ("attention", attention, 10)]:
    print(f"showing {name} for {secs}s")
    end = time.time() + secs
    while time.time() < end:
        s.write((json.dumps(state) + "\n").encode())
        time.sleep(1)
print("done")