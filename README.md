🚀 Orion Roketi Yer Kontrol İstasyonu - README

📖 Proje Açıklaması

Bu proje, "Orion Roketi Yer Kontrol İstasyonu" isimli bir arayüz uygulamasıdır. Python'un Tkinter kütüphanesi kullanılarak geliştirilmiştir ve roketten gelen verileri gerçek zamanlı olarak kullanıcıya sunar. Kullanıcı, arayüz üzerinden roketin konumunu, hızını, yüksekliğini takip edebilir ve paraşütleri manuel olarak açabilir.

⚙️ Özellikler

Gerçek zamanlı seri port iletişimi (Serial Communication)

Roketin konumunu, hızını ve yüksekliğini gösterme

Roketin yönünü dinamik olarak simüle eden grafik



ve 2. paraşütleri açma butonları

Bağlantı durumunu anlık kontrol etme

🛠️ Gereksinimler

Python 3.x

tkinter (standart Python kütüphanesinde mevcuttur)

pyserial

📦 Kurulum

Gerekli kütüphaneyi yükleyin:

pip install pyserial

Projeyi çalıştırın:

python rocket_ui.py

Not: Uygulamanın seri port iletişimi için COM3 varsayılan olarak ayarlanmıştır. Kullanılan cihaza göre bu ayarı güncelleyin.

🚀 Kullanım

Program başlatıldığında, bağlantı durumunu kırmızı olarak "Bağlanmadı" şeklinde göreceksiniz.

Arduino cihazınızdan verileri göndermeye başladığınızda, bağlantı durumu "Bağlı" olarak yeşile döner.

Roketin X, Y, Z koordinatları, hızı ve yüksekliği anlık olarak ekranda güncellenir.

"1. Paraşüt Aç" ve "2. Paraşüt Aç" butonlarını kullanarak manuel olarak paraşütleri açabilirsiniz.

🔍 Veri Formatı

Arduino veya başka bir cihazdan gelen veri, aşağıdaki formatta olmalıdır:

X,Y,Z,Hız,Yükseklik,Paraşüt1,Paraşüt2

Örnek:

12.34,56.78,90.12,15.5,120.7,0,1

X, Y, Z: Roketin uzaydaki konum koordinatları

Hız: Roketin anlık hızı (m/s)

Yükseklik: Roketin yerden yüksekliği (m)

Paraşüt1 ve Paraşüt2: 1 veya 0 (açık/kapalı durumu)

🛠️ Kod Yapısı

RocketUI: Ana arayüz sınıfı

connect_serial: Seri port bağlantısı kurar

read_data_from_serial: Arduino'dan veri okur ve arayüzü günceller

update_tilt: Roketin yönünü grafiksel olarak günceller

open_parachute1 / open_parachute2: Paraşütleri açar

⚠️ Olası Hatalar ve Çözümler

Bağlantı hatası:

COM3 portu dolu olabilir veya yanlış ayarlanmış olabilir. Doğru portu bulmak için Aygıt Yöneticisini kontrol edin.

Veri okuma hatası:

Arduino'nun gönderdiği veri formatının yukarıda belirtilen formata uygun olduğundan emin olun.

Arayüz güncellenmiyor:

Arduino'nun veri göndermeye başladığından emin olun.

👨‍💻 Geliştirici Notları

Roketin yön simülasyonu için math kütüphanesinden trigonometri fonksiyonları kullanılmıştır.

Arayüz, koyu temalı olacak şekilde tasarlanmıştır.

Orion Roketi Yer Kontrol İstasyonu; eğitim, simülasyon ve hobi projeleri için uygundur.

🎯 Başarılar dileriz! 🚀
