<h1>Vox <a href="#Favicon"><img src="https://raw.githubusercontent.com/Vauth/vox/main/src/media/vpn.png" width="33px"></a> Unofficial Warp Client for Windows</h1>
<a href="https://www.virustotal.com/gui/url/2e623797af0a425434f475e861e50eb208128e2b681745ceecc3675cdf8e3c61"><img src="https://img.shields.io/badge/-VirusTotal-5238ff?style=flat&logo=virustotal&logoColor=white"></a>
<a href="https://github.com/Vauth/vox/actions"><img src="https://img.shields.io/badge/-Github%20Actions-5238ff?style=flat&logo=githubactions&logoColor=white"></a>
<a href="https://www.studytonight.com/post/x86-vs-x64-what-is-the-difference-between-x86-and-x64-architecture"><img src="https://img.shields.io/badge/-Windows%20x64-5238ff?style=flat&logo=windows&logoColor=white"></a>


### 🔎 Features:
- **User-Friendly:** Simple, intuitive interface.
- **WARP:** Connect to warp (ipv6).
- **CFON:** Handshake between warp & psiphon (ipv4).
- **SCAN:** Scan clean cloudflare ips.
- **WARP+:** Insert your warp+ key.

#### 🔗 CFON Country List:

- Austria (AT) | Belgium (BE) | Bulgaria (BG)
- Brazil (BR) | Canada (CA) | Switzerland (CH)
- Czech Republic (CZ) | Germany (DE) | Denmark (DK)
- Estonia (EE) | Spain (ES) | Finland (FI)
- France (FR) | United Kingdom (GB) | Hungary (HU)
- reland (IE) | India (IN) | Italy (IT)
- Japan (JP) | Latvia (LV) | Netherlands (NL)
- Norway (NO) | Poland (PL) | Romania (RO)
- Serbia (RS) | Sweden (SE) | Singapore (SG)
- Slovakia (SK) | Ukraine (UA) | United States (US)


#### 🗝 WARP+ Key:
- Get your warp+ key from [@generatewarpplusbot](https://t.me/generatewarpplusbot) .

</br>

## 🚀 Quick Start
- **Download:** Grab the EXE from our [Releases](https://github.com/Vauth/vox/releases) .
- **Connect:** Launch Vox and hit the connect button.

</br>

## ⚙️ Building The Application
- #### Clone Repository:
```shell
git clone https://github.com/Vauth/vox
cd vox
```

- #### Install Requirements:
```shell
python3 -m pip install -r requirements.txt
```

- #### Build The Project:
```shell
pyinstaller --onefile --icon=src/media/vpn.ico  --add-data="src/media;media" --add-data="src/tool;tool" src/Vox.py
```

</br>

## 📚 Additional Tutorials
#### 📌 Proxy DNS For Browsers (mozilla):
- Go to `browsers settings > network settings` .
- Enable `Proxy DNS when using SOCKS v5` .

#### 🛠 Not Working?
- Disable system antivirus & browsers privacy, unsigned apps may be detected as `malicious software` .
- You are connected to `socks5` through `system proxy` , so some apps may not support socks5 proxies .
- Socks5 only works correctly on browsers if you set `Proxy DNS For Browsers` .
- Vox has been tested on `Windows 10 (x64)`. if it crashes on your system, feel free to [contact us](https://t.me/ExecalChat).

</br>

## 📷 Screenshot

<a href="#Screenshot"><img src="https://i.ibb.co/KmnfdCw/5975e06f697a.png" width="400px"></a>
