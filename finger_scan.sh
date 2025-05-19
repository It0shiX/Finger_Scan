#!/bin/bash

TARGET="192.168.1.100"
USER)

echo "[+] Skanuję port 79 na hoście $TARGET..."
PORT_STATUS=$(nmap -p 79 "$TARGET" | grep "79/tcp" | awk '{print $2}')

if [[ "$PORT_STATUS" != "open" ]]; then
    echo "[-] Port 79 jest $PORT_STATUS. Finger niedostępny."
    exit 1
fi

echo "[+] Port 79 OTWARTY. Wysyłam zapytania..."

for USER in "${USERS[@]}"; do
    echo -e "$USER\r\n" | nc -w 3 "$TARGET" 79 > /tmp/finger_result.txt 2>/dev/null

    if grep -iq "no such user" /tmp/finger_result.txt || [ ! -s /tmp/finger_result.txt ]; then
        echo "[-] Użytkownik '$USER' nie istnieje lub brak odpowiedzi."
    else
        echo "[+] Użytkownik '$USER' ZNALEZIONY:"
        cat /tmp/finger_result.txt
        echo "----------------------------------------"
    fi
done
