import socket
TOKEN = "Meiw0@v1"

IP = 'localhost'
PORT = 50001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Menghubungi Server Terpadu...")

try:
    s.connect((IP, PORT))
    print(f"Terhubung! Token sesi: {TOKEN}")
    print("Perintah: nama, nim, system, parameter 1=.., hitung, keluar")

    pesan = ''
    while pesan.lower() != 'keluar':
        pesan = input(">> ")
        paket = TOKEN + pesan
        
        s.send(paket.encode())

        if pesan.lower() != 'keluar':
            try:
                jawaban = s.recv(1024).decode()
                print(f"Server: {jawaban}")
            except:
                print("Koneksi terganggu.")
                break

except ConnectionRefusedError:
    print("Gagal konek! Server mati atau menolak koneksi.")

finally:
    s.close()