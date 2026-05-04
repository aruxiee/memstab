# memstab
Zero-file, LotL command for memory-resident binary execution. Bypasses EDR vectors by leveraging memfd_create and os.execve to pivot from an obfuscated Base85/Bit-Shift one-liner to a fileless process execution masquerading as a kernel thread without disk footprints.
