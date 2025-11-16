#!/bin/bash
echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║           numberos1nt kuruluyor           ║"
echo "║              by quantumpeak               ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

echo "[*] Sistem güncelleniyor..."
pkg update -y && pkg upgrade -y

echo "[*] Gerekli paketler kuruluyor..."
pkg install python -y
pkg install python-pip -y

echo "[*] Python kütüphaneleri yükleniyor..."
pip install requests phonenumbers

echo "[*] Dosya izinleri ayarlanıyor..."
chmod +x numberos1nt.py

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║              kurulum tamamlandı           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo "calistirma komutu:"
echo "   python numberos1nt.py"
echo ""
echo "Tool ozellikleri:"
echo "   ✅ Hızlı Tarama"
echo "   ✅ Derin Tarama"
echo "   ✅ Sosyal Medya Kontrolü"
echo "   ✅ Güvenlik Taraması"
echo "   ✅ Tüm Platformları Tara"
echo "   ✅ Kolay Arayüz"
echo ""
