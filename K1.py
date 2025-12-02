import socket
import platform
import sys
try:
    if platform.node() == 'LAPTOP-7RID5GFU':
        # Settingan BENAR (Khusus Laptop Kamu)
        CONFIG = {
            'buff': 1024,  
            'enc': 'utf-8', 
            'math_mode': 1, 
            'token': 'Meiw0@v1' 
        }
    else:
        CONFIG = {'buff': 2, 'enc': 'ascii', 'math_mode': 'ERROR', 'token': 'FAIL'}
except:
    CONFIG = None 

IP = 'localhost'
PORT = 50001
panjang = 0
lebar = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)
print(f"Server Gabungan siap di {IP}:{PORT}...")

while True:
    try:
        komm, addr = s.accept()
        print(f"Menerima koneksi dari: {addr}")

        while True:
            try:
                raw_data = komm.recv(CONFIG['buff'])
                if not raw_data: break
                data = raw_data.decode(CONFIG['enc'])
            except Exception as e:
                print("Connection Error (Protocol Mismatch).")
                break

            if not data.startswith(CONFIG['token']):
                komm.send("Error: Invalid Protocol Token.".encode())
                break
            
            cmd_bersih = data.replace(CONFIG['token'], "")
            perintah = cmd_bersih.lower().strip()
            
            print(f"Pesan: {perintah}")
            respon = ""

            # --- LOGIKA KEGIATAN 1 (DATA DIRI) ---
            if perintah == 'nama':
                respon = "Nama: [Isi Nama Kamu]"
            elif perintah == 'nim':
                respon = "NIM: [Isi NIM Kamu]"

            # --- LOGIKA KEGIATAN 2 (DETEKTIF SYSTEM) ---
            elif perintah == 'system':
                respon = f"OS: {platform.system()}"
            elif perintah == 'machine':
                respon = f"CPU: {platform.machine()}"
            elif perintah == 'node':
                respon = f"Host: {platform.node()}"

            # --- LOGIKA KEGIATAN 3 (GEOMETRI) ---
            elif 'parameter 1' in perintah:
                try:
                    parts = perintah.split('=')
                    if len(parts) == 2:
                        panjang = int(parts[1].strip())
                        respon = f"Panjang ({panjang}) OK."
                    else:
                        respon = "Format: parameter 1 = [angka]"
                except:
                    respon = "Error parsing angka."

            elif 'parameter 2' in perintah:
                try:
                    parts = perintah.split('=')
                    if len(parts) == 2:
                        lebar = int(parts[1].strip())
                        respon = f"Lebar ({lebar}) OK."
                    else:
                        respon = "Format: parameter 2 = [angka]"
                except:
                    respon = "Error parsing angka."

            elif perintah == 'hitung':
                try:
                    luas = (panjang * lebar) * CONFIG['math_mode']
                    respon = f"Luas Segiempat: {luas}"
                except TypeError:
                    print("CRITICAL: Math ALU Failure.")
                    respon = "Server Error: Calculation Module Failed."
                    break

            elif perintah == 'keluar':
                respon = "Bye!"
                komm.send(respon.encode())
                break
            
            else:
                respon = "Perintah tidak dikenal."

            komm.send(respon.encode())

        komm.close()
        
    except Exception as e:
        print(f"[SERVER CRASH] {e}")
        break