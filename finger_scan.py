import nmap
import socket

target_ip = "select target"
usernames = ["root", "admin", "user"]

print(f"[+] Skanuję port 79 na hoście {target_ip}...")
scanner = nmap.PortScanner()
scanner.scan(target_ip, '79')

port_state = scanner[target_ip]['tcp'][79]['state']

if port_state != 'open':
    print(f"[-] Port 79 (finger) jest {port_state}. Finger niedostępny.")
    exit(0)

print("[+] Port 79 jest OTWARTY. Wysyłam zapytania finger...\n")

for user in usernames:
    try:
        with socket.create_connection((target_ip, 79), timeout=5) as s:
            s.sendall(f"{user}\r\n".encode())
            response = s.recv(4096).decode(errors="ignore")
            if "no such user" in response.lower() or response.strip() == "":
                print(f"[-] Użytkownik '{user}' nie istnieje lub brak odpowiedzi.")
            else:
                print(f"[+] Użytkownik '{user}' ZNALEZIONY:")
                print(response)
                print("-" * 40)
    except Exception as e:
        print(f"[!] Błąd dla użytkownika {user}: {e}")
