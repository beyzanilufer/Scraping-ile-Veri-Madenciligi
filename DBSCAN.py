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
# GÖRSELLEŞTİRME
# ============================================================================

plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(20, 12))

# Renk paleti oluştur
n_clusters = int(df['Cluster'].max())
colors = plt.cm.tab10(np.linspace(0, 1, n_clusters + 1))

# 1. 3D Scatter Plot
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
for cluster in range(-1, n_clusters + 1):
    cluster_data = df[df['Cluster'] == cluster]
    if cluster == -1:
        ax1.scatter(cluster_data['Revenue_Normalize'],
                   cluster_data['Employees_Normalize'],
                   cluster_data['Age_Normalize'],
                   c='red', marker='x', s=200, linewidths=3,
                   label='Anomali', alpha=0.8)
    else:
        ax1.scatter(cluster_data['Revenue_Normalize'],
                   cluster_data['Employees_Normalize'],
                   cluster_data['Age_Normalize'],
                   c=[colors[cluster]], s=100, alpha=0.7,
                   label=f'Küme {cluster}')

ax1.set_xlabel('Revenue (Normalize)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Employees (Normalize)', fontsize=10, fontweight='bold')
ax1.set_zlabel('Age (Normalize)', fontsize=10, fontweight='bold')
ax1.set_title('3D DBSCAN Kümeleme Sonuçları', fontsize=14, fontweight='bold', pad=20)
ax1.legend(loc='upper left', fontsize=8)
ax1.view_init(elev=20, azim=45)

# 2. Revenue vs Employees
ax2 = fig.add_subplot(2, 3, 2)
for cluster in range(-1, n_clusters + 1):
    cluster_data = df[df['Cluster'] == cluster]
    if cluster == -1:
        ax2.scatter(cluster_data['Revenue_Normalize'],
                   cluster_data['Employees_Normalize'],
                   c='red', marker='x', s=200, linewidths=3,
                   label='Anomali', alpha=0.8, zorder=5)
    else:
        ax2.scatter(cluster_data['Revenue_Normalize'],
                   cluster_data['Employees_Normalize'],
                   c=[colors[cluster]], s=100, alpha=0.7,
                   label=f'Küme {cluster}')

ax2.set_xlabel('Revenue (Normalize)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Employees (Normalize)', fontsize=11, fontweight='bold')
ax2.set_title('Revenue vs Employees', fontsize=13, fontweight='bold')
ax2.legend(loc='best', fontsize=8)
ax2.grid(True, alpha=0.3)

# 3. Revenue vs Age
ax3 = fig.add_subplot(2, 3, 3)
for cluster in range(-1, n_clusters + 1):
    cluster_data = df[df['Cluster'] == cluster]
    if cluster == -1:
        ax3.scatter(cluster_data['Revenue_Normalize'],
                   cluster_data['Age_Normalize'],
                   c='red', marker='x', s=200, linewidths=3,
                   label='Anomali', alpha=0.8, zorder=5)
    else:
        ax3.scatter(cluster_data['Revenue_Normalize'],
                   cluster_data['Age_Normalize'],
                   c=[colors[cluster]], s=100, alpha=0.7,
                   label=f'Küme {cluster}')

ax3.set_xlabel('Revenue (Normalize)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Age (Normalize)', fontsize=11, fontweight='bold')
ax3.set_title('Revenue vs Age', fontsize=13, fontweight='bold')
ax3.legend(loc='best', fontsize=8)
ax3.grid(True, alpha=0.3)

# 4. Employees vs Age
ax4 = fig.add_subplot(2, 3, 4)
for cluster in range(-1, n_clusters + 1):
    cluster_data = df[df['Cluster'] == cluster]
    if cluster == -1:
        ax4.scatter(cluster_data['Employees_Normalize'],
                   cluster_data['Age_Normalize'],
                   c='red', marker='x', s=200, linewidths=3,
                   label='Anomali', alpha=0.8, zorder=5)
    else:
        ax4.scatter(cluster_data['Employees_Normalize'],
                   cluster_data['Age_Normalize'],
                   c=[colors[cluster]], s=100, alpha=0.7,
                   label=f'Küme {cluster}')

ax4.set_xlabel('Employees (Normalize)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Age (Normalize)', fontsize=11, fontweight='bold')
ax4.set_title('Employees vs Age', fontsize=13, fontweight='bold')
ax4.legend(loc='best', fontsize=8)
ax4.grid(True, alpha=0.3)

# 5. Küme Dağılımı (Bar Chart)
ax5 = fig.add_subplot(2, 3, 5)
cluster_counts = df['Cluster'].value_counts().sort_index()
bar_colors = ['red' if x == -1 else colors[x] for x in cluster_counts.index]
bars = ax5.bar(range(len(cluster_counts)), cluster_counts.values, color=bar_colors, alpha=0.7, edgecolor='black')

# Bar üstüne değerleri yaz
for i, (bar, count) in enumerate(zip(bars, cluster_counts.values)):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax5.set_xlabel('Küme ID', fontsize=11, fontweight='bold')
ax5.set_ylabel('Şirket Sayısı', fontsize=11, fontweight='bold')
ax5.set_title('Küme Dağılımı', fontsize=13, fontweight='bold')
ax5.set_xticks(range(len(cluster_counts)))
ax5.set_xticklabels(['Anomali' if x == -1 else f'Küme {x}'
                     for x in cluster_counts.index], rotation=45, ha='right')
ax5.grid(True, alpha=0.3, axis='y')

# 6. İstatistiksel Özet Tablosu
ax6 = fig.add_subplot(2, 3, 6)
ax6.axis('off')

# Tablo verilerini hazırla
table_data = []
table_data.append(['📊 GENEL İSTATİSTİKLER', ''])
table_data.append(['─'*30, '─'*15])
table_data.append(['Toplam Şirket', f'{len(df)}'])
table_data.append(['Küme Sayısı', f'{n_clusters}'])
table_data.append(['Anomali Sayısı', f'{len(anomaliler)}'])
table_data.append(['Anomali Oranı', f'{len(anomaliler)/len(df)*100:.2f}%'])
table_data.append(['', ''])
table_data.append(['⚙️ PARAMETRELER', ''])
table_data.append(['─'*30, '─'*15])
table_data.append(['Eps (Yarıçap)', f'{Eps}'])
table_data.append(['MinPts', f'{MinPts}'])

table = ax6.table(cellText=table_data, cellLoc='left',
                 colWidths=[0.7, 0.3], loc='center',
                 bbox=[0, 0.2, 1, 0.8])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Hücre renklerini ayarla
for i in range(len(table_data)):
    for j in range(2):
        cell = table[(i, j)]
        if i in [0, 6]:  # Başlık satırları
            cell.set_facecolor('#4CAF50')
            cell.set_text_props(weight='bold', color='white')
        elif i in [1, 7]:  # Ayırıcı satırlar
            cell.set_facecolor('#E0E0E0')
        else:
            cell.set_facecolor('#F5F5F5')
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)

ax6.set_title('Analiz Özeti', fontsize=14, fontweight='bold', pad=20)

plt.suptitle('🎯 DBSCAN KÜMELEMESİ VE ANOMALİ TESPİTİ ANALİZİ',
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.97])

# Grafikleri kaydet
plt.savefig('dbscan_analiz.png', dpi=300, bbox_inches='tight')
print(f"\n💾 Grafik kaydedildi: dbscan_analiz.png")

plt.show()

print("\n✅ Analiz ve görselleştirme tamamlandı!")



