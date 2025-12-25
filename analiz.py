import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

#veri yükle
df=pd.read_excel("fortune_500_detayli_veri5.xlsx")

#kaç satir kaç süütn var
print(f"veri boyutu: {df.shape[0]} satır, {df.shape[1]} sütün")

#Null metinleri temizle
df.replace("Null",pd.NA,inplace=True)

#boş alanları temizle
df_clean=df.dropna(subset=['Revenue','Employees','Age'])

df_clean['Revenue_per_Employee']= df_clean['Revenue']/df_clean['Employees']

df_clean['Age_Category']=pd.cut(df_clean['Age'], bins=[0,25,50,100,500], labels=['Genç','Orta','Olgun','Köklü'])

# Çalışan kategorisi
df_clean['Size_Category'] = pd.cut(df_clean['Employees'],
                                    bins=[0, 50000, 200000, 500000, float('inf')],
                                    labels=['Küçük', 'Orta', 'Büyük', 'Dev'])
# 3. Sektör isimlerini (metin) sayıya çevirelim (Modelin anlaması için)
le=LabelEncoder()
df_clean['Industry_Encoded']=le.fit_transform(df_clean['Industry'].fillna('Unknown'))

print("✓ Yeni sütunlar eklendi!")
print("\nYeni sütunlarla ilk 3 satır:")
print(df_clean[['Company', 'Revenue_per_Employee', 'Age_Category', 'Industry_Encoded']].head(3))




