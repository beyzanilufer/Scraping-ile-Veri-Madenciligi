import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

# --- Yapılandırma ---
BASE_URL = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
WIKI_DOMAIN = "https://en.wikipedia.org"

# Kendi tarayıcınızın User-Agent bilgisini kullanmak iyi bir pratik.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,az-AZ;q=0.8,az;q=0.7,en-US;q=0.6,en;q=0.5",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

# Veri setini tutacak liste
company_data = []


# Bot algılanmamak için her istek arasında rastgele bekleme
def smart_delay():
    time.sleep(random.uniform(1, 3))


# --- Birinci Aşama: Ana Tabloyu Çekme ve Linkleri Toplama ---

print("👉 1/2: Ana Tablo Çekiliyor ve Detay Linkleri Toplanıyor...")
smart_delay()

try:
    response = requests.get(BASE_URL, headers=headers, timeout=10)
    response.raise_for_status()  # Hata kodu (4xx veya 5xx) varsa istisna fırlatır
    soup = BeautifulSoup(response.text, "html.parser")
except requests.RequestException as e:
    print(f"⚠️ Ana URL'e erişimde hata: {e}")
    exit()

# Tabloyu bulma (Sizin kodunuzdaki gibi)
table = soup.find_all("table", {"class": "wikitable"})[0]
rows = table.find_all("tr")[1:]  # Başlık satırını atla

for i, row in enumerate(rows):
    my_rows = row.find_all("td")
    if not my_rows:
        continue

    # Şirket Adı ve Linki (2. sütun, yani index 1)
    company_cell = my_rows[1]
    company_link_tag = company_cell.find("a") #satırlardakı linkleri al

    if company_link_tag and company_link_tag.get('href').startswith('/wiki/'):
        company_name = company_link_tag.text.strip()
        relative_link = company_link_tag.get('href')
        detail_url = WIKI_DOMAIN + relative_link
    else:
        # Link yoksa veya format yanlışsa
        company_name = my_rows[1].text.strip()
        detail_url = None

    # Diğer sütun verilerini alırken güvenli kontrol
    data_row = [item.text.strip() for item in my_rows]

    company_dict = {
        "Rank": my_rows[0].text.strip() if len(my_rows) > 0 else None,  # Index 0
        "Company": company_name,  # Index 1
        "Industry": my_rows[2].text.strip() if len(my_rows) > 2 else None,  # Index 2
        "Revenue": my_rows[3].text.strip() if len(my_rows) > 3 else None,  # Index 3 ✅
        "Revenue_Growth": my_rows[4].text.strip() if len(my_rows) > 4 else None,  # Index 4
        "Employees": my_rows[5].text.strip() if len(my_rows) > 5 else None,  # Index 5 ✅
        "Headquarters": my_rows[6].text.strip() if len(my_rows) > 6 else None,  # Index 6
        "Detail_URL": detail_url
    }
    company_data.append(company_dict)
    print(company_dict)

    if i % 20 == 0:
        print(f"  > {i + 1}. şirket: {company_name} linki alındı.")

# --- İkinci Aşama: Her Şirketin Detay Sayfasını Ziyaret Etme ---

print("\n👉 2/2: Detay Sayfalarından CEO ve Kuruluş Yılı Çekiliyor...")

for i, company in enumerate(company_data):

    if company['Detail_URL']:
        smart_delay()  # Her sayfa arasında bekleme

        try:
            detail_response = requests.get(company['Detail_URL'], headers=headers, timeout=10)
            detail_response.raise_for_status()
            detail_soup = BeautifulSoup(detail_response.text, "html.parser")

            # 💡 Bilgi Kutusundan (Infobox) Veri Çekme:
            infobox = detail_soup.find("table", {"class": "infobox"})

            founded_year = None
            ceo_name = None

            if infobox:
                # Infobox satırlarını döngüye al
                for row in infobox.find_all('tr'):
                    header = row.find('th')
                    data = row.find('td')

                    if header and data:
                        header_text = header.text.strip()
                        data_text = data.text.strip()

                        # Kuruluş Yılını Bulma
                        if "Founded" in header_text or "Kuruluş" in header_text:
                            founded_year = data_text.split('\n')[0].split(';')[0].replace('[', '').replace(']', '')
                        # CEO Adını Bulma
                        elif "CEO" in header_text:
                            ceo_name = data_text.split('\n')[0]

            # Verileri ana sözlüğe ekle
            company['Founded_Year'] = founded_year
            company['CEO'] = ceo_name

            # Sadece bir örneği gösterme
            if i < 5:
                print(f"  ✅ {company['Company']}: Kuruluş: {founded_year}, CEO: {ceo_name}")

        except requests.RequestException as e:
            # Hata oluşursa (Zaman aşımı, sayfa bulunamaması vb.)
            company['Founded_Year'] = None
            company['CEO'] = None
            if i < 3:
                print(f"  ⚠️ {company['Company']} detayı çekilemedi.")

# --- Üçüncü Aşama: Veriyi Temizleme ve Kaydetme ---

df = pd.DataFrame(company_data)

# Revenue temizleme
if 'Revenue' in df.columns:
    df['Revenue'] = df['Revenue'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

# Employees temizleme
if 'Employees' in df.columns:
    df['Employees'] = df['Employees'].astype(str).str.replace(r'[^\d]', '', regex=True)
    df['Employees'] = pd.to_numeric(df['Employees'], errors='coerce')

# Revenue Growth temizleme (yüzde işaretini kaldır)
if 'Revenue_Growth' in df.columns:
    df['Revenue_Growth'] = df['Revenue_Growth'].astype(str).str.replace('%', '').str.strip()
    df['Revenue_Growth'] = pd.to_numeric(df['Revenue_Growth'], errors='coerce')

# Kuruluş yılı temizleme
if 'Founded_Year' in df.columns:
    df['Founded_Year'] = df['Founded_Year'].astype(str).str.extract(r'(\d{4})', expand=False)
    df['Founded_Year'] = pd.to_numeric(df['Founded_Year'], errors='coerce')
    df['Age'] = 2025 - df['Founded_Year']
    df['Age'] = df['Age'].where(df['Age'] > 0, pd.NA)  # Negatif yaşları temizle


# Boş kalan (None veya NaN) tüm hücrelere "Null" metnini yazar
df = df.fillna("Null")

# VEYA CSV olarak kaydet (UTF-8-SIG ile)
df.to_excel("fortune_500_detayli_veri5.xlsx", index=False)

print("\n✅ Web Scraping Projesi Tamamlandı!")
print(f"Toplam Çekilen Şirket Sayısı: {df.shape[0]}")
print(f"Yeni Veri Boyutu: {df.shape}")
print("Veri 'fortune_500_detayli_veri5.xlsx' olarak kaydedildi.")