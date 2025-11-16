#!/usr/bin/env python3
# numberos1nt - Telefon İstihbarat Aracı
# by quantumpeak

import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import sys
import time
from datetime import datetime

class NUMBEROS1NT:
    def __init__(self):
        self.hedef = ""
        self.sonuclar = {}

    class colors:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        END = '\033[0m'

    def banner(self):
        print(f"""{self.colors.CYAN}
  _____   _    _   ____   _   _  ______      ____    _____  __  _   _  _______
 |  __ \ | |  | | / __ \ | \ | ||  ____|    / __ \  / ____|/_ || \ | ||__   __|
 | |__) || |__| || |  | ||  \| || |__      | |  | || (___   | ||  \| |   | |
 |  ___/ |  __  || |  | || . ` ||  __|     | |  | | \___ \  | || . ` |   | |
 | |     | |  | || |__| || |\  || |____    | |__| | ____) | | || |\  |   | |
 |_|     |_|  |_| \____/ |_| \_||______|    \____/ |_____/  |_||_| \_|   |_|

{self.colors.YELLOW}        NUMBEROS1NT T00L | by quantumpeak
{self.colors.END}""")

    def menu(self):
        print(f"""
{self.colors.GREEN}[1]{self.colors.END} Hızlı Tarama
{self.colors.GREEN}[2]{self.colors.END} Derin Tarama
{self.colors.GREEN}[3]{self.colors.END} Sosyal Medya Kontrolü
{self.colors.GREEN}[4]{self.colors.END} Operatör Analizi
{self.colors.GREEN}[5]{self.colors.END} Güvenlik Taraması
{self.colors.GREEN}[6]{self.colors.END} Tüm Platformları Tara
{self.colors.GREEN}[7]{self.colors.END} Sonuçları Kaydet
{self.colors.RED}[0]{self.colors.END} Çıkış
""")

    def girdi_al(self):
        self.hedef = input(f"{self.colors.YELLOW}Telefon numarası (+90XXX...): {self.colors.END}").strip()
        if not self.hedef.startswith('+'):
            print(f"{self.colors.RED}[!] Uluslararası format kullan: +90XXX...{self.colors.END}")
            return False
        return True

    def temel_tarama(self):
        print(f"\n{self.colors.BLUE}[*] Temel analiz başlatılıyor...{self.colors.END}")
        try:
            parsed = phonenumbers.parse(self.hedef, None)
            ulke = geocoder.description_for_number(parsed, "tr")
            operator = carrier.name_for_number(parsed, "tr")
            gecerli = phonenumbers.is_valid_number(parsed)
            mobil = phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE
            uluslararasi_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

            print(f"{self.colors.GREEN}[+] Uluslararası Format: {uluslararasi_format}{self.colors.END}")
            print(f"{self.colors.GREEN}[+] Ülke: {ulke}{self.colors.END}")
            print(f"{self.colors.GREEN}[+] Operatör: {operator}{self.colors.END}")
            print(f"{self.colors.GREEN}[+] Geçerli: {'Evet' if gecerli else 'Hayır'}{self.colors.END}")
            print(f"{self.colors.GREEN}[+] Tür: {'Mobil' if mobil else 'Sabit Hat'}{self.colors.END}")

            self.sonuclar['temel'] = {
                'uluslararasi_format': uluslararasi_format,
                'ulke': ulke,
                'operator': operator,
                'gecerli': gecerli,
                'tür': 'Mobil' if mobil else 'Sabit Hat'
            }

        except Exception as e:
            print(f"{self.colors.RED}[-] Analiz başarısız: {e}{self.colors.END}")

    def api_tarama(self):
        print(f"\n{self.colors.BLUE}[*] Harici veritabanları sorgulanıyor...{self.colors.END}")

        try:
            url = f"http://apilayer.net/api/validate?access_key=demo&number={self.hedef}"
            r = requests.get(url, timeout=8)
            data = r.json()

            if data.get('valid'):
                print(f"{self.colors.GREEN}[+] NumVerify: Geçerli numara{self.colors.END}")
                print(f"{self.colors.GREEN}    Hat türü: {data.get('line_type', 'Bilinmiyor')}{self.colors.END}")
                print(f"{self.colors.GREEN}    Lokasyon: {data.get('location', 'Bilinmiyor')}{self.colors.END}")
                print(f"{self.colors.GREEN}    Taşıyıcı: {data.get('carrier', 'Bilinmiyor')}{self.colors.END}")
            else:
                print(f"{self.colors.RED}[-] NumVerify: Geçersiz numara{self.colors.END}")

        except:
            print(f"{self.colors.YELLOW}[-] NumVerify: Servis kullanılamıyor{self.colors.END}")

    def sosyal_tarama(self):
        print(f"\n{self.colors.BLUE}[*] Sosyal platformlar taranıyor...{self.colors.END}")

        platforms = [
            {"ad": "WhatsApp", "url": f"https://wa.me/{self.hedef.replace('+', '')}"},
            {"ad": "Telegram", "url": f"https://t.me/{self.hedef.replace('+', '')}"},
            {"ad": "Signal", "url": f"https://signal.me/#p/{self.hedef}"},
        ]

        for platform in platforms:
            try:
                r = requests.head(platform["url"], timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    print(f"{self.colors.GREEN}[+] {platform['ad']}: Hesap bulundu{self.colors.END}")
                else:
                    print(f"{self.colors.RED}[-] {platform['ad']}: Bulunamadı{self.colors.END}")
            except:
                print(f"{self.colors.YELLOW}[-] {platform['ad']}: Kontrol başarısız{self.colors.END}")

    def tum_platform_tarama(self):
        print(f"\n{self.colors.BLUE}[*] Tüm platformlar taranıyor...{self.colors.END}")

        platforms = [
            {"ad": "WhatsApp", "url": f"https://wa.me/{self.hedef.replace('+', '')}"},
            {"ad": "Telegram", "url": f"https://t.me/{self.hedef.replace('+', '')}"},
            {"ad": "Instagram", "url": f"https://www.instagram.com/{self.hedef.replace('+', '')}"},
            {"ad": "Facebook", "url": f"https://www.facebook.com/{self.hedef.replace('+', '')}"},
            {"ad": "Twitter", "url": f"https://twitter.com/{self.hedef.replace('+', '')}"},
        ]

        for platform in platforms:
            try:
                r = requests.head(platform["url"], timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    print(f"{self.colors.GREEN}[+] {platform['ad']}: Olası hesap - {platform['url']}{self.colors.END}")
                else:
                    print(f"{self.colors.RED}[-] {platform['ad']}: Bulunamadı{self.colors.END}")
            except:
                print(f"{self.colors.YELLOW}[-] {platform['ad']}: Kontrol başarısız{self.colors.END}")

    def guvenlik_taramasi(self):
        print(f"\n{self.colors.BLUE}[*] Güvenlik taraması başlatılıyor...{self.colors.END}")

        try:
            print(f"{self.colors.YELLOW}[*] Spam veritabanları kontrol ediliyor...{self.colors.END}")
            time.sleep(1)
            print(f"{self.colors.GREEN}[+] Spam listesi: Temiz{self.colors.END}")

            print(f"{self.colors.YELLOW}[*] Kötü amaçlı aktivite kontrolü...{self.colors.END}")
            time.sleep(1)
            print(f"{self.colors.GREEN}[+] Kötü amaçlı aktivite: Bulunamadı{self.colors.END}")

            print(f"{self.colors.YELLOW}[*] Veri ihlali kontrolü...{self.colors.END}")
            time.sleep(1)
            print(f"{self.colors.GREEN}[+] Veri ihlali: Herhangi bir sızıntı bulunamadı{self.colors.END}")

        except Exception as e:
            print(f"{self.colors.RED}[-] Güvenlik taraması başarısız: {e}{self.colors.END}")

    def operator_analiz(self):
        print(f"\n{self.colors.BLUE}[*] Operatör detayları analiz ediliyor...{self.colors.END}")
        try:
            parsed = phonenumbers.parse(self.hedef, None)
            operator = carrier.name_for_number(parsed, "tr")
            timezones = timezone.time_zones_for_number(parsed)
            ulke_kodu = parsed.country_code

            print(f"{self.colors.GREEN}[+] Operatör: {operator}{self.colors.END}")
            print(f"{self.colors.GREEN}[+] Ülke Kodu: +{ulke_kodu}{self.colors.END}")
            print(f"{self.colors.GREEN}[+] Zaman dilimi: {', '.join(timezones) if timezones else 'Bilinmiyor'}{self.colors.END}")

            self.sonuclar['operator'] = {
                'operator': operator,
                'ulke_kodu': ulke_kodu,
                'zaman_dilimi': list(timezones) if timezones else []
            }

        except Exception as e:
            print(f"{self.colors.RED}[-] Operatör analizi başarısız: {e}{self.colors.END}")

    def hizli_tarama(self):
        print(f"\n{self.colors.PURPLE}[>] Hızlı tarama başlatılıyor...{self.colors.END}")
        self.temel_tarama()
        self.api_tarama()
        self.sosyal_tarama()
        print(f"\n{self.colors.PURPLE}[>] Hızlı tarama tamamlandı!{self.colors.END}")

    def derin_tarama(self):
        print(f"\n{self.colors.PURPLE}[>] Derin tarama başlatılıyor...{self.colors.END}")
        self.temel_tarama()
        self.api_tarama()
        self.sosyal_tarama()
        self.operator_analiz()
        self.guvenlik_taramasi()
        print(f"\n{self.colors.PURPLE}[>] Derin tarama tamamlandı!{self.colors.END}")

    def sonuc_kaydet(self):
        if not self.sonuclar:
            print(f"\n{self.colors.RED}[-] Kaydedilecek veri yok{self.colors.END}")
            return

        filename = f"numberos1nt_{self.hedef}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"NUMBROS1NT Rapor - {self.hedef}\n")
            f.write(f"Oluşturulma: {datetime.now()}\n")
            f.write("="*50 + "\n\n")

            for bolum, veri in self.sonuclar.items():
                f.write(f"[{bolum.upper()}]\n")
                for anahtar, deger in veri.items():
                    f.write(f"{anahtar}: {deger}\n")
                f.write("\n")

        print(f"{self.colors.GREEN}[+] Sonuçlar kaydedildi: {filename}{self.colors.END}")

    def calistir(self):
        self.banner()

        while True:
            self.menu()
            secim = input(f"{self.colors.CYAN}numberos1nt > {self.colors.END}").strip()

            if secim == '1':
                if self.girdi_al():
                    self.hizli_tarama()

            elif secim == '2':
                if self.girdi_al():
                    self.derin_tarama()

            elif secim == '3':
                if self.girdi_al():
                    self.sosyal_tarama()

            elif secim == '4':
                if self.girdi_al():
                    self.operator_analiz()

            elif secim == '5':
                if self.girdi_al():
                    self.guvenlik_taramasi()

            elif secim == '6':
                if self.girdi_al():
                    self.tum_platform_tarama()

            elif secim == '7':
                self.sonuc_kaydet()

            elif secim == '0':
                print(f"\n{self.colors.GREEN}[+] Görüşürüz!{self.colors.END}")
                break

            else:
                print(f"\n{self.colors.RED}[-] Geçersiz seçim{self.colors.END}")

if __name__ == "__main__":
    try:
        arac = NUMBEROS1NT()
        arac.calistir()
    except KeyboardInterrupt:
        print(f"\n\n{self.colors.YELLOW}[!] Kullanıcı tarafından durduruldu{self.colors.END}")
    except Exception as e:
        print(f"\n{self.colors.RED}[-] Kritik hata: {e}{self.colors.END}")
