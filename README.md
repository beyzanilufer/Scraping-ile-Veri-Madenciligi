Fortune 500 Veri Kazıma ve DBSCAN Anomali Analizi
Bu proje, Amerika'nın en büyük şirketlerinin (Fortune 500) verilerini Wikipedia üzerinden dinamik olarak çekmek, temizlemek ve DBSCAN kümeleme algoritması kullanarak bu şirketler arasındaki aykırı (anomali) değerleri tespit etmek amacıyla geliştirilmiştir.

Proje Aşamaları
Proje üç temel modülden oluşmaktadır:

1. Veri Kazıma (Web Scraping) 
veri.py ve scraping süreçleri ile Wikipedia üzerindeki "List of largest companies in the United States" sayfasından veriler çekilir.

Detaylı Scraping: Sadece ana tablo değil, her şirketin kendi özel sayfasına gidilerek kuruluş yılı ve CEO gibi bilgiler de toplanır.

Anti-Bot Önlemleri: smart_delay fonksiyonu ile istekler arasına rastgele süreler eklenerek sunucu dostu bir tarama yapılır.

2. Veri Ön İşleme ve Normalizasyon 
Normalize.py ve normalizasyon.py dosyaları, ham veriyi analize hazır hale getirir.

Veri Temizliği: Sayısal değerlerdeki özel karakterler ($ , % vb.) temizlenir.

Min-Max Normalizasyonu: Gelir (Revenue), Çalışan Sayısı (Employees) ve Şirket Yaşı (Age) verileri 0 ile 1 arasına ölçeklenir.

3. DBSCAN ile Anomali Tespiti 
DBSCAN.py içerisinde algoritma kütüphane kullanılmadan (from scratch) NumPy ile kodlanmıştır.

Kümeleme: Benzer özellik gösteren şirketler gruplandırılır.

Anomali Tespiti: Herhangi bir kümeye dahil olamayan (gürültü) şirketler "Anomali" olarak işaretlenir ve 3D grafik üzerinde görselleştirilir.

Dosya Yapısı
DBSCAN.py: Sıfırdan kodlanmış DBSCAN algoritması ve analiz motoru.

LineerRegresyon.py: Gelir ve çalışan sayısı arasındaki ilişkiyi inceleyen model.

Normalize.py / normalizasyon.py: Veri ölçekleme ve temizleme araçları.

fortune_500_detayli_veri5.xlsx: Kazınmış ham veri seti.

fortune_500_Normalize_Sonuc.xlsx: Analiz için hazır normalize edilmiş veri seti.

Örnek Çıktı Görselleştirmesi
Analiz sonucunda elde edilen 3D grafik; Gelir, Çalışan Sayısı ve Şirket Yaşı eksenlerinde şirketlerin dağılımını ve kırmızı renkle işaretlenmiş anomalileri gösterir.

Kurulum
Projeyi çalıştırmak için:

Depoyu klonlayın: git clone https://github.com/beyzanilufer/Scraping-ile-Veri-Analizi.git

Gerekli kütüphaneleri kurun: pip install pandas numpy matplotlib requests beautifulsoup4 openpyxl

Önce veriyi çekmek için veri.py, ardından analiz için DBSCAN.py dosyasını çalıştırın.
