import os 
import time
from datetime import datetime, timedelta
import threading
import tkinter as tk

def buat_parkir(kapasitas):
    slots = ['kosong'] * kapasitas
    #Bikin beberapa slot sudah terisi memang
    slots[0:5] = ['terisi']*(5)
    slots[55:60] = ['terbooking']*(5)
    slots[32:37] = ['terbooking']*(5)
    slots[73:78] = ['terisi']*(5)
    return slots
    
def lihat_slot_kosong(slots):
    for i, status in enumerate(slots):
        if status == 'kosong':
            print(f"\x1b[37m{chr(65 + i // 10)}{i % 10 + 1}\x1b[0m", end=' ')  #Mengubah warna angka slot menjadi putih
        elif status == 'booking':
            print(f"\x1b[33;4;1m{chr(65 + i // 10)}{i % 10 + 1}\x1b[0m", end=' ')  #Mengubah warna angka slot menjadi kuning
        elif status == 'merah':
            print(f"\x1b[31;4;1m{chr(65 + i // 10)}{i % 10 + 1}\x1b[0m", end=' ')  #Mengubah warna angka slot menjadi merah
        elif status == 'terbooking':
            print(f"\x1b[33m{chr(65 + i // 10)}{i % 10 + 1}\x1b[0m", end=' ')  #Mengubah warna angka slot menjadi kuning
        elif status == 'terisi':
            print(f"\x1b[31m{chr(65 + i // 10)}{i % 10 + 1}\x1b[0m", end=' ')  #Mengubah warna angka slot menjadi merah
        
        if (i + 1) % 10 == 0: #Membuat baris baru setelah 10 slot
           print()

def konversi_input_slot(input_slot):
    if len(input_slot) < 2 or not input_slot[0].isalpha() or not input_slot[1:].isdigit():
        #Memeriksa apakah panjang input kurang dari 2 karakter, huruf pertama bukan huruf, atau sisanya bukan digit
        return -1 #return -1 supaya ini jadi tidak valid karena tidak ada di slot
    
    row = ord(input_slot[0]) - ord('A')
    col = int(input_slot[1:]) 

    if row < 0 or row >= 10 or col < 1 or col > 10:
        #Memeriksa apakah baris di luar rentang A-J dan kolom di luar rentang 1-10
        return -1#return -1 supaya ini jadi tidak valid karena tidak ada di slot
    
    return row * 10 + col

def timer_booking_timeout(slot, slot_parkir):
    global sudah_booking
    if slot_parkir[slot - 1] == 'booking' and sudah_booking:
        slot_parkir[slot - 1] = 'kosong'
        sudah_booking = False
        print(f"\nWaktu Booking untuk Slot \033[34m{inp_slot}\033[0m Telah Habis.")
        #Append History
        history.append(f"Waktu Booking slot \033[31m{inp_slot}\033[0m Telah Habis")
        time.sleep(2)
        os.system('cls')
        
        #tambahan hitung ulang available di function ini supaya terupdate bagian kosongnya, karena klau tidak ada bakal terprint available sebelumnya 
        available = [i + 1 for i, status in enumerate(slot_parkir) if status == 'kosong']
        print(homepage)
        print('='*29 + f"\n\x1b[37;1mSlot yang tersedia:\x1b[0m \033[34m{len(available)}/100\033[0m" + '\n' + '='*29)
        print("Masukkan pilihan (1/2/3/4/5/6): ")
        
def parkir(slots, slot, sudah_parkir, sudah_booking):
    if 1 <= slot <= len(slots):
        if not sudah_parkir:
            if sudah_booking and slots[slot - 1] == 'booking':
                confirmation = input(f"Apakah Anda ingin parkir di slot \033[34m{inp_slot}\033[0m yang telah Anda booking sebelumnya? (Y/N): ")
                if confirmation.upper() == 'Y':
                    slots[slot - 1] = 'merah'  #Mengubah status slot menjadi 'merah'
                    print(f"Mobil berhasil diparkir di slot \033[34m{inp_slot}\033[0m")
                    sudah_parkir = True
                    #Append History
                    waktu_sekarang=datetime.now()
                    history.append(f"Parkiran \033[34m{inp_slot}\033[0m diisi pada {waktu_sekarang.strftime("%Y-%m-%d %H:%M")}")
                elif confirmation.upper() == 'N':
                    print("Parkir dibatalkan.")
                    time.sleep(2)
            elif not sudah_booking and slots[slot - 1] == 'kosong':
                slots[slot - 1] = 'merah'  #Mengubah status slot menjadi 'merah'
                print(f"Mobil berhasil diparkir di slot \033[34m{inp_slot}\033[0m")
                sudah_parkir = True
                #Append History
                waktu_sekarang=datetime.now()
                history.append(f"Parkiran \033[34m{inp_slot}\033[0m diisi pada {waktu_sekarang.strftime("%Y-%m-%d %H:%M")}")
            else:
                print("Slot sudah terisi.")
        else:
            print("Anda sudah melakukan parkir sebelumnya.")
            time.sleep(2)
    else:
        print("Slot parkir tidak valid.")
        time.sleep(2)
    return sudah_parkir

def keluar_parkir(slots, sudah_parkir, sudah_booking):
    if sudah_parkir:
        confirmation = input(f"Apakah Anda ingin mengeluarkan mobil dari slot \033[31m{inp_slot}\033[0m? (Y/N): ")
        if confirmation.upper() =='Y':
            slots[slot-1] = 'kosong'
            print(f"Mobil berhasil keluar dari slot \033[31m{inp_slot}\033[0m")
            #Append history
            waktu_sekarang=datetime.now()
            history.append(f"Anda keluar dari parkiran \033[31m{inp_slot}\033[0m pada {waktu_sekarang.strftime("%Y-%m-%d %H:%M")}")
            sudah_booking = False
            sudah_parkir = False
            return slots, sudah_parkir, sudah_booking
        elif confirmation.upper() == 'N':
            print("Pengeluaran mobil dibatalkan.")
            return slots, sudah_parkir, sudah_booking
        else:
            print("Masukan tidak valid. Pengeluaran mobil dibatalkan.")
            return slots, sudah_parkir, sudah_booking
    else:
        print("Anda belum melakukan parkir.")
        return slots, sudah_parkir, sudah_booking

# NOTIFIKASI


# def notireminder():
#     global sudah_booking
#     if sudah_booking:
#         popup = tk.Tk()
#         popup.wm_title("Parkirki' Notification")
#         label = tk.Label(popup, text="Waktu booking Anda tersisa 15 detik.")
#         label.pack(side="top", fill="x", pady=50)


# NOTIFIKASI
def notibooking():
    popup = tk.Tk()
    popup.wm_title("Parkirki' Notification")
    label = tk.Label(popup, text="Anda telah sukses booking.")
    label.pack(side="top", fill="x", pady=50)

def notireminder():
    global sudah_booking
    if sudah_booking:
        popup = tk.Tk()
        popup.wm_title("Parkirki' Notification")
        label = tk.Label(popup, text="Waktu booking Anda tersisa 15 detik.")
        label.pack(side="top", fill="x", pady=50)
        popup.mainloop()

def notiparked():
    popup = tk.Tk()
    popup.wm_title("Parkirki' Notification")
    label = tk.Label(popup, text=f"Anda telah sukses parkir.")
    label.pack(side="top", fill="x", pady=50)

daftar_pengguna=[]
#Funsi untuk registrasi 
def registrasi():
    print("Silakan registrasi.")
    username = input("Masukkan username baru: ").lower()
    password = input("Masukkan password baru: ")
    
    #buat dictionary dalam array jadi mudah di cek pakai for loop
    daftar_pengguna.append({'username': username, 'password': password})
    
    os.system('cls')
    print(loginpage)
    print("Registrasi berhasil.")
    
#Fungsi untu login
def login():
    print("Login")
    username = input("Masukkan username: ").lower()
    password = input("Masukkan password: ")

    # cek menggunakan for loop, jika if sesuai maka hasilnya kembali true, jika tidak maka hasil kembali false
    for i in daftar_pengguna:
        if i['username'] == username and i['password'] == password:
            os.system('cls')
            print(loginpage)
            print(f"Login berhasil!\nSelamat datang {username}!")
            return True

    os.system('cls')
    print(loginpage)
    print("Username atau password salah. Login gagal atau akun belum terdaftar.")
    time.sleep(2)
    return False

#!ERORRRRRR
# def keluar_parkir(slots, sudah_parkir):
#     if sudah_parkir:
#         slot_parkir = [i + 1 for i, status in enumerate(slots) if status == 'merah']
#         if slot_parkir:
#             slot = slot_parkir[0]  # Mengambil slot pertama yang telah diparkir
#             confirmation = input(f"Apakah Anda ingin mengeluarkan mobil dari slot \033[31m{inp_slot}\033[0m? (Y/N): ")
#             if confirmation.upper() == 'Y':
#                 slots[slot - 1] = 'kosong'  # Mengubah status slot menjadi 'kosong'
#                 print(f"Mobil berhasil keluar dari slot \033[31m{inp_slot}\033[0m")
#                 #Append history
#                 waktu_sekarang=datetime.now()
#                 history.append(f"Anda keluar dari parkiran \033[31m{inp_slot}\033[0m pada {waktu_sekarang.strftime("%Y-%m-%d %H:%M")}")
#                 return False
#             elif confirmation.upper() == 'N':
#                 print("Pengeluaran mobil dibatalkan.")
#                 return True
#             else:
#                 print("Masukan tidak valid. Pengeluaran mobil dibatalkan.")
#                 return True
#         else:
#             print("Anda belum melakukan parkir.")
#             return True
#     else:
#         print("Anda belum melakukan parkir.")
#         return 

kapasitas_parkir = 100
slot_parkir = buat_parkir(kapasitas_parkir)
sudah_parkir = False
sudah_booking = False


history = []

#UI
loginpage = '='*21 + '\n' + "ParkirKi'".center(21) + '\n' + '='*21 + '\n' + '1. Registrasi' + '\n' + '2. Login' + '\n' + '3. Exit' + '\n'
homepage = '='*29 + '\n' + "ParkirKi'".center(29) + '\n' + '='*29 + '\n' + '1. Lihat slot parkir kosong' + '\n' + '2. Booking Slot / Cancel Booking' + '\n' + '3. Parkir mobil' + '\n' + '4. Keluar dari tempat parkir' + '\n' + '5. History Anda' + '\n' + '6. Logout'

while True:
    os.system('cls')
    print(loginpage)
    opsi = input("Pilih Opsi (1/2/3): ")

    #menggunakan kondisi if untuk cek opsi yang dipilih
    if opsi == '1':
        os.system('cls')
        print(loginpage)
        
        #panggil fungsi regis
        registrasi()
        
    elif opsi == '2': 
        os.system('cls')
        print(loginpage)

        #panggil fungsi login, jika return true maka if true akan berjalan
        if login():
            time.sleep(2)
            os.system('cls')
            while True:
                available = [i + 1 for i, status in enumerate(slot_parkir) if status == 'kosong']
                #print(f"\n\x1b[37;1mSlot yang tersedia:\x1b[0m \033[34m{len(available)}/100\033[0m")
                
                os.system('cls')
                print(homepage)
                print('='*29 + f"\n\x1b[37;1mSlot yang tersedia:\x1b[0m \033[34m{len(available)}/100\033[0m" + '\n' + '='*29)
                pilihan = input("Masukkan pilihan (1/2/3/4/5/6): ")

                if pilihan == '1':
                    os.system('cls')
                    print('='*30)
                    lihat_slot_kosong(slot_parkir)
                    input(f"{'='*30}\nTekan Enter untuk Kembali")
                elif pilihan == '2':
                    if not sudah_booking and not sudah_parkir: #cek sudah booking/parkir, kalau ada yang false maka kode ini tidak berjalan
                        os.system('cls')
                        print('='*30)
                        lihat_slot_kosong(slot_parkir)
                        print('='*30)
                        inp_slot = input("Masukkan nomor slot yang akan dibooking: ").upper()
                        slot = konversi_input_slot(inp_slot)
                        if 1 <= slot <= len(slot_parkir) and slot_parkir[slot - 1] == 'kosong': #cek apakah slot yang dimasukkan ada / valid / sesuai dengan rentang array yg sudah di buat , and cek status  slot yang dipilih kosong atau tidak 
                            slot_parkir[slot - 1] = 'booking' #ubah status yang sebelumnya kosong jadi booking pada slot yang dipilih
                            sudah_booking = True #ubah status variabel sudah booking menjadi true
                            notibooking()
                            # TIMER
                            thread = threading.Timer(30 ,timer_booking_timeout, args=(slot, slot_parkir))
                            thread.start()
                            threadreminder = threading.Timer(15 , notireminder)
                            threadreminder.start()
                            #append history
                            waktu_sekarang = datetime.now()
                            waktu_selesai = datetime.now() + timedelta(minutes=30)
                            history.append(f"Parkiran \033[34m{inp_slot}\033[0m dibooking pada {waktu_sekarang.strftime("%Y-%m-%d %H:%M")} dan akan berakhir pada {waktu_selesai.strftime("%Y-%m-%d %H:%M")}")
                        else: #jika slot yang di input tidak sesuai
                            print("Slot yang Anda pilih tidak tersedia atau sudah terisi.")
                            time.sleep(2)
                    elif sudah_booking and not sudah_parkir:
                        cancel = input(f"Apakah Anda ingin membatalkan booking untuk slot \033[31m{inp_slot}\033[0m? (Y/N): ")
                        if cancel.upper() =='Y':
                            if slot_parkir[slot - 1] == 'booking':
                                slot_parkir[slot - 1] = 'kosong'
                                sudah_booking = False
                                print(f"Booking slot \033[31m{inp_slot}\033[0m berhasil dibatalkan.")
                                #Append History
                                waktu_sekarang=datetime.now()
                                history.append(f"Booking slot \033[31m{inp_slot}\033[0m dibatalkan pada {waktu_sekarang.strftime("%Y-%m-%d %H:%M")}")
                        elif cancel.upper() == 'N':
                                print()
                    else: #jika user sudah booking atau parkir.
                        print("Anda sudah melakukan parkir atau booking sebelumnya.")
                        time.sleep(2)
                elif pilihan == '3':
                    if not sudah_parkir and not sudah_booking: #berjalan jika belum parkir dan sudah/belum booking
                        os.system('cls')
                        print('='*30)
                        lihat_slot_kosong(slot_parkir)
                        print('='*30)
                        inp_slot = input("Masukkan nomor slot yang akan diparkirkan: ").upper()
                        slot = konversi_input_slot(inp_slot)
                        sudah_parkir = parkir(slot_parkir, konversi_input_slot(inp_slot), sudah_parkir, sudah_booking)
                        notiparked()
                    elif not sudah_parkir and sudah_booking:
                        sudah_parkir = parkir(slot_parkir, slot, sudah_parkir, sudah_booking)
                        notiparked()
                    else:
                        print("Anda sudah melakukan parkir atau booking sebelumnya.")
                        time.sleep(1)
                elif pilihan == '4':
                    slot_parkir, sudah_parkir, sudah_booking = keluar_parkir(slot_parkir, sudah_parkir, sudah_booking)
                    # Reset sudah_booking and sudah_parkir saat sudah keluar
                elif pilihan == '5':
                    if history:
                        print("==================================")
                        #show history
                        for i in range(0,len(history)):
                            print(f"{i+1}. {history[i]}")
                        input("==================================")
                        os.system('cls')
                    else:
                        print("=")
                        print("History kosong.")
                        input("==================================")
                        os.system('cls')
                elif pilihan == '6':
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")
    elif opsi == '3': 
                break   
    else:
            os.system('cls')
            print(loginpage)
            print("Opsi tidak ditemukan!\n")
            