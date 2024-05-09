## CentOS/RHEL 9

Install.
```
dnf install openvpn-stat
```

Monitor current sessions.
```
openvpn-statd -m
```

Generate a summary session history report.
```
openvpn-stat -s
```

Generate a detailed session history report.
```
openvpn-stat -d
```
