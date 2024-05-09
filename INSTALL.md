## CentOS/RHEL 9

Install.
```
cd /tmp
curl -s https://api.github.com/repos/netcons/openvpn-stat/releases \
| grep "browser_download_url.*.el9.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -

dnf install openvpn-stat-*.el9.noarch.rpm

rm openvpn-stat-*.el9.noarch.rpm
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
