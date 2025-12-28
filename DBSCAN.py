import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



print("daha önce hazırlanmıs normalıze dosya")
df=pd.read_excel("fortune_500_Normalize.xlsx")

#analiz için normalize olan 3 sütünü seciyorum
features=['Revenue_Normalize','Employees_Normalize','Age_Normalize']
Veri_array=df[features].values

# mesafe hesapla
def mesafe(p1,p2):
    return np.sqrt(np.sum((p1-p2)**2))



#eps(yariçap)=0.5 minpts=4 min nokta sayisi
def dbscan(veri,Eps,MinPts):
    n=len(veri) # toplam şirket sayisi
    etiketler=np.zeros(n) # başlangıçta her nokta 0 henüz işlenmemiş -1 gürültü
    kume_id=0 #küme sayaci

    for i in range(n):
        if etiketler[i]!=0: #bu noktalar işlendimi
            continue #zaten işelenmiş atla

        komsular=[] #komsulari bul
        for j in range(n):
            if mesafe(veri[i], veri[j])<=Eps:
                komsular.append(j)
        if len(komsular) < MinPts: #yeterli komşu var mi
            etiketler[i]=-1
            continue

        #yeni küme oluştur
        kume_id+=1
        etiketler[i]=kume_id

        #komşulari işlemek için bir kuyruk oluştuer
        kuyruk=komsular.copy()
        kuyruk.remove(i) #kendini kuyruktan çıkar

        while kuyruk:
            komsu_id=kuyruk.pop(0)
            #gürültülü noktayı kümeye al
            if etiketler[komsu_id]==-1:
                etiketler[komsu_id]=kume_id
            #zaten kumeye eklenmıs
            if etiketler[komsu_id] !=0:
                continue
            #kumeye ekle
            etiketler[komsu_id]=kume_id

            #bu nokta merkez nokta mı
            komsu_komsular=[]
            for j in range(n):
                if mesafe(veri[komsu_id],veri[j]) <=Eps:
                    komsu_komsular.append(j)

            if len(komsu_komsular)>=MinPts:
                for yeni_komsu in komsu_komsular:
                    if etiketler[yeni_komsu]==0:
                        if yeni_komsu not in kuyruk:
                            kuyruk.append(yeni_komsu)






    print(f"\n{'─'*60}")
    print(f"✅ DBSCAN Tamamlandı!")
    print(f"   • Bulunan küme sayısı: {kume_id}")
    print(f"   • Anomali sayısı: {np.sum(etiketler == -1)}")

    return etiketler
#eps(yariçap)=0.5 minpts=4 min nokta sayisi
Eps=0.10
MinPts=4

df['Cluster']=dbscan(Veri_array,Eps, MinPts).astype(int)
anomaliler=df[df['Cluster']==-1]
normal_noktalar=df[df['Cluster']>0]

print(f"\n✅ ANALİZ TAMAMLANDI")
print(f"--------------------------------------------------")
print(f"• Toplam Şirket Sayısı  : {len(df)}")
print(f"• Bulunan Küme Sayısı   : {int(df['Cluster'].max())}")
print(f"• Tespit Edilen Anomali : {len(anomaliler)} (Gürültü Noktalar)")
print(f"--------------------------------------------------")

print(f"\n{'='*60}")
print(f"📊 ANALİZ SONUÇLARI")
print(f"{'='*60}")
print(f"• Toplam Şirket Sayısı     : {len(df)}")
print(f"• Bulunan Küme Sayısı      : {int(df['Cluster'].max())}")
print(f"• Normal Nokta Sayısı      : {len(normal_noktalar)}")
print(f"• Tespit Edilen Anomali    : {len(anomaliler)} ({len(anomaliler)/len(df)*100:.2f}%)")
print(f"{'='*60}")

# Küme dağılımını göster
if df['Cluster'].max() > 0:
    print(f"\n📈 KÜME DAĞILIMI:")
    for kume in range(1, int(df['Cluster'].max()) + 1):
        kume_sayisi = len(df[df['Cluster'] == kume])
        print(f"   Küme {kume}: {kume_sayisi} şirket")

# Anomalileri göster
if len(anomaliler) > 0:
    print(f"\n🚨 TESPİT EDİLEN ANOMALİLER:")
    print(f"{'─'*60}")
    if 'Company' in anomaliler.columns:
        print(anomaliler[['Company', 'Revenue_Normalize', 'Employees_Normalize',
                         'Age_Normalize', 'Cluster']].to_string(index=False))

# ============================================================================
# SEKTÖR BAZLI ANOMALİ ANALİZİ
# ============================================================================
import seaborn as sns

# Sadece anomalileri filtrele
anomali_df = df[df['Cluster'] == -1]

if not anomali_df.empty:
    plt.figure(figsize=(14, 8))

    # Sektörlere göre anomali sayılarını hesapla
    sektor_counts = anomali_df['Industry'].value_counts()

    # Görselleştirme
    sns.barplot(x=sektor_counts.values, y=sektor_counts.index, palette='magma')

    plt.title('🚨 SEKTÖR BAZLI ANOMALİ DAĞILIMI', fontsize=16, fontweight='bold')
    plt.xlabel('Anomali Sayısı (Şirket)')
    plt.ylabel('Sektör')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Sayıları barların üzerine ekle
    for i, v in enumerate(sektor_counts.values):
        plt.text(v + 0.1, i, str(v), color='black', fontweight='bold', va='center')

    plt.tight_layout()
    plt.show()

    # Detaylı Tablo Çıktısı
    print("\n📊 SEKTÖR BAZLI ANOMALİ ÖZETİ:")
    print("-" * 40)
    summary = anomali_df.groupby('Industry').agg({
        'Company': 'count',
        'Revenue_Normalize': 'mean',
        'Employees_Normalize': 'mean'
    }).rename(columns={'Company': 'Şirket Sayısı', 'Revenue_Normalize': 'Ort. Gelir (Norm)'})
    print(summary.sort_values(by='Şirket Sayısı', ascending=False))
# ============================================================================
# DÜZENLENMİŞ VE TEMİZLENMİŞ DASHBOARD
# ============================================================================
plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(22, 12))

# Kaç küme olduğunu belirle (Anomalileri -1 hariç tut)
mevcut_kumeler = [c for c in sorted(df['Cluster'].unique()) if c != -1]
n_clusters = len(mevcut_kumeler)
colors = plt.cm.tab10(np.linspace(0, 1, n_clusters))

# 1. PANEL: 3D Görünüm
ax1 = fig.add_subplot(1, 2, 1, projection='3d')

# Önce Anomalileri Çiz
anomali_verisi = df[df['Cluster'] == -1]
if not anomali_verisi.empty:
    ax1.scatter(anomali_verisi['Revenue_Normalize'], anomali_verisi['Employees_Normalize'],
               anomali_verisi['Age_Normalize'], c='red', marker='x', s=150,
               linewidths=3, label='Anomali', alpha=0.9, zorder=5)

# Sonra Sadece İçinde Veri Olan Kümeleri Çiz
for i, kume_id in enumerate(mevcut_kumeler):
    c_data = df[df['Cluster'] == kume_id]
    ax1.scatter(c_data['Revenue_Normalize'], c_data['Employees_Normalize'],
               c_data['Age_Normalize'], s=70, alpha=0.6,
               label=f'Küme {kume_id}', c=[colors[i]])

ax1.set_title('3D ŞİRKET DAĞILIMI VE ANOMALİLER', fontsize=15, fontweight='bold')
ax1.set_xlabel('Revenue (Norm)')
ax1.set_ylabel('Employees (Norm)')
ax1.set_zlabel('Age (Norm)')
ax1.legend(loc='upper left')

# 2. PANEL: Küme Dağılımı (Bar Chart)
ax2 = fig.add_subplot(2, 2, 2)
counts = df['Cluster'].value_counts().sort_index()
# Etiketleri ve renkleri ayarla
labels = ['Anomali' if i == -1 else f'Küme {i}' for i in counts.index]
bar_colors = ['red' if i == -1 else '#3498db' for i in counts.index]

bars = ax2.bar(labels, counts.values, color=bar_colors, edgecolor='black', alpha=0.8)
ax2.bar_label(bars, padding=3, fontweight='bold')
ax2.set_title(f'TOPLAM {n_clusters} KÜME VE ANOMALİ DAĞILIMI', fontsize=13, fontweight='bold')

# 3. PANEL: Analiz Özeti Tablosu
ax3 = fig.add_subplot(2, 2, 4)
ax3.axis('off')
summary_data = [
    ["Toplam Şirket", len(df)],
    ["Bulunan Küme Sayısı", n_clusters],
    ["Tespit Edilen Anomali", len(df[df['Cluster'] == -1])],
    ["Anomali Oranı", f"%{len(df[df['Cluster'] == -1])/len(df)*100:.2f}"],
    ["Eps (Yarıçap)", Eps],
    ["MinPts (Min Nokta)", MinPts]
]
table = ax3.table(cellText=summary_data, colLabels=["Parametre", "Değer"],
                  loc='center', cellLoc='left', bbox=[0.1, 0.2, 0.8, 0.7])
table.auto_set_font_size(False)
table.set_fontsize(12)
ax3.set_title('ANALİZ İSTATİSTİKLERİ', fontsize=13, fontweight='bold')

plt.suptitle('🎯 FORTUNE 500 DBSCAN ANOMALİ ANALİZ RAPORU', fontsize=20, fontweight='bold', y=0.96)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

