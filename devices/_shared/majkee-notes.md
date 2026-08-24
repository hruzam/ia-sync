Verification after both steps:
1. Tablet: ssh hruzam@hruzam → must now say permission denied (publickey) — reaching sshd (allowed, port 22) but keyless. No shell.
2. Tablet: mysql -h 100.110.27.60 or any non-22 touch → must time out (grant blocks it).
3. Office: ssh -p 8022 100.127.230.71 'echo ok' → must still connect (computer mesh intact).
4. Office ↔ home ssh + db-reach → unaffected.



