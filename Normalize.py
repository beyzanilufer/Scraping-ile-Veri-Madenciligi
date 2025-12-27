import pandas as pd

# ══════════════════════════════════════════════════════
# ADIM 1: VERİYİ YÜKLE
# ══════════════════════════════════════════════════════
df = pd.read_excel("fortune_500_detayli_veri6.xlsx")
df.replace("Null", pd.NA, inplace=True)
df = df.dropna(subset=['Revenue', 'Employees', 'Age'])

print("ORIJINAL VERİ:")
print(df[['Company', 'Revenue', 'Employees', 'Age']].head(3))

# ══════════════════════════════════════════════════════
# ADIM 2: MIN-MAX NORMALİZASYON (ELLE)
# ══════════════════════════════════════════════════════

# Revenue için
revenue_min = df['Revenue'].min()
revenue_max = df['Revenue'].max()

df['Revenue_Normalize'] = (df['Revenue'] - revenue_min) / (revenue_max - revenue_min)

# Employees için
emp_min = df['Employees'].min()
emp_max = df['Employees'].max()

df['Employees_Normalize'] = (df['Employees'] - emp_min) / (emp_max - emp_min)

# Age için
age_min = df['Age'].min()
age_max = df['Age'].max()

df['Age_Normalize'] = (df['Age'] - age_min) / (age_max - age_min)

print("\n" + "="*80)
print("NORMALIZE EDİLMİŞ VERİ:")
print("="*80)
print(df[['Company', 'Revenue_Normalize', 'Employees_Normalize', 'Age_Normalize']].head(5))

# ══════════════════════════════════════════════════════
# ADIM 3: KARŞILAŞTIRMA TABLOSU
# ══════════════════════════════════════════════════════
print("\n" + "="*80)
print("KARŞILAŞTIRMA: İlk 3 Şirket")
print("="*80)

compare = df[['Company', 'Revenue', 'Revenue_Normalize',
              'Employees', 'Employees_Normalize',
              'Age', 'Age_Normalize']].head(3)

for idx, row in compare.iterrows():
    print(f"\n{row['Company']}:")
    print(f"  Revenue:   {row['Revenue']:>10,.0f}  →  {row['Revenue_Normalize']:.4f}")
    print(f"  Employees: {row['Employees']:>10,.0f}  →  {row['Employees_Normalize']:.4f}")
    print(f"  Age:       {row['Age']:>10.0f}  →  {row['Age_Normalize']:.4f}")
"""# ══════════════════════════════════════════════════════
# ADIM 4: GÖRSELLEŞTİRME
# ══════════════════════════════════════════════════════
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Öncesi
axes[0].scatter(df['Revenue'], df['Employees'], s=df['Age']*2, alpha=0.6)
axes[0].set_xlabel('Revenue (Orijinal)')
axes[0].set_ylabel('Employees (Orijinal)')
axes[0].set_title('NORMALİZASYON ÖNCESİ\n(Değerler çok farklı!)')
axes[0].grid(True, alpha=0.3)

# Sonrası
axes[1].scatter(df['Revenue_Normalize'], df['Employees_Normalize'],
                s=df['Age_Normalize']*200, alpha=0.6, color='green')
axes[1].set_xlabel('Revenue (Normalize)')
axes[1].set_ylabel('Employees (Normalize)')
axes[1].set_title('NORMALİZASYON SONRASI\n(Hepsi 0-1 arası!)')
axes[1].set_xlim(-0.1, 1.1)
axes[1].set_ylim(-0.1, 1.1)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('normalizasyon_karsilastirma.png', dpi=300, bbox_inches='tight')
print("\n✓ Grafik kaydedildi: normalizasyon_karsilastirma.png")

# ══════════════════════════════════════════════════════
# ADIM 5: EXCEL'E KAYDET
# ══════════════════════════════════════════════════════
df.to_excel("fortune_500_Normalize.xlsx", index=False)
print("✓ Normalize veri kaydedildi: fortune_500_Normalize.xlsx")

print("\n" + "="*80)
"""
# ══════════════════════════════════════════════════════
# ADIM 4: GÖRSELLEŞTİRME (YAŞI EKSENE EKLEYEREK)
# ══════════════════════════════════════════════════════
import matplotlib.pyplot as plt

# 3 grafiklik bir alan oluşturalım (2D Karşılaştırmalar ve 3D Dağılım)
fig = plt.figure(figsize=(18, 5))

# 1. Grafik: Revenue vs Employees (Yaş renk olarak kullanıldı)
ax1 = fig.add_subplot(1, 3, 1)
sc1 = ax1.scatter(df['Revenue_Normalize'], df['Employees_Normalize'],
                  c=df['Age_Normalize'], cmap='viridis', s=50, alpha=0.7)
ax1.set_xlabel('Revenue (Normalize)')
ax1.set_ylabel('Employees (Normalize)')
ax1.set_title('Revenue vs Employees\n(Renk tonu = Normalize Yaş)')
plt.colorbar(sc1, ax=ax1, label='Yaş (0-1)')
ax1.grid(True, alpha=0.3)

# 2. Grafik: Revenue vs Age (Yaşın eksendeki yerini görmek için)
ax2 = fig.add_subplot(1, 3, 2)
ax2.scatter(df['Revenue_Normalize'], df['Age_Normalize'],
            color='purple', s=50, alpha=0.6)
ax2.set_xlabel('Revenue (Normalize)')
ax2.set_ylabel('Yaş (Normalize)')
ax2.set_title('Revenue vs YAŞ\n(Yaş artık Y ekseninde!)')
ax2.set_ylim(-0.1, 1.1)
ax2.grid(True, alpha=0.3)

# 3. Grafik: 3D Dağılım (Her 3 değişkenin 0-1 arası kutusu)
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
ax3.scatter(df['Revenue_Normalize'], df['Employees_Normalize'], df['Age_Normalize'],
            c='green', s=60, alpha=0.7)
ax3.set_xlabel('Revenue')
ax3.set_ylabel('Employees')
ax3.set_zlabel('Age')
ax3.set_title('3D TÜM VERİLER\n(Hepsi 0-1 Arasında!)')

plt.tight_layout()
plt.savefig('normalizasyon_tam_karsilastirma.png', dpi=300, bbox_inches='tight')
print("\n✓ Yaşın dahil edildiği yeni grafik kaydedildi: normalizasyon_tam_karsilastirma.png")