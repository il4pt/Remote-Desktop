import socket
import re

def send_magic_packet(mac_address: str, ip_address: str = "255.255.255.255", port: int = 9) -> bool:
    """
    Hedef MAC adresine Wake-on-LAN Magic Packet gönderir.
    LAN içinde 255.255.255.255 broadcast'e, WAN üzerinde ise hedef router IP/port yönlendirmesine atılır.
    """
    try:
        # MAC adresini temizle ve doğrula (AA:BB:CC:DD:EE:FF veya AA-BB-CC-DD-EE-FF)
        clean_mac = re.sub(r'[^a-fA-F0-9]', '', mac_address)
        if len(clean_mac) != 12:
            raise ValueError(f"Geçersiz MAC adresi: {mac_address}")

        # Magic Packet: 6 byte 0xFF + 16 kez tekrarlanan MAC adresi (toplam 102 byte)
        packet_bytes = bytes.fromhex('FF' * 6 + clean_mac * 16)

        # UDP soketi oluştur ve broadcast izni ver
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(packet_bytes, (ip_address, port))
        
        return True
    except Exception as e:
        print(f"[WoL Hatası] {e}")
        return False
