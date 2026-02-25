"""
Zor Çalışan Simülatörü
----------------------
Yöneticilerin zor çalışanlarla iletişim pratiği yapabileceği bir mini rol oyunu.
Çalıştırmak için: streamlit run app.py
"""

import streamlit as st
import random

# ─────────────────────────────────────────────
# SENARYO VERİTABANI
# ─────────────────────────────────────────────
SENARYOLAR = [
    {
        "kategori": "🏆 Performansı Yüksek Ama Egolu Çalışan",
        "metin": (
            "Ahmet, şirketinizin en iyi satış temsilcisi. Geçen çeyrekte hedefini %140 oranında aştı. "
            "Ancak son toplantıda ekip arkadaşlarının fikirlerini açıkça küçümsedi: 'Bu kadar basit bir şeyi "
            "neden anlayamıyorlar?' dedi. Diğer çalışanlar şikayetlerini size iletmeye başladı. "
            "Ahmet ise durumun abartıldığını düşünüyor ve özür dilemeyi reddediyor. "
            "Ekip morali sarsılmaya başladı."
        ),
    },
    {
        "kategori": "😤 Sürekli Şikayet Eden Çalışan",
        "metin": (
            "Selin, her hafta en az bir kez odanıza gelip yeni bir şikayetle çıkıyor. "
            "Bu hafta: 'Klima çok soğuk, maaş zamanı geç yatıyor, toplantılar çok uzun ve "
            "ofis kahvesi berbat.' Şikayetlerinin bir kısmı haklı olsa da sürekli olumsuz enerji "
            "ekibi yıpratıyor. Diğer çalışanlar Selin'den uzak durmaya başladı. "
            "Selin ise 'Sadece gerçekleri söylüyorum' diyor."
        ),
    },
    {
        "kategori": "⚔️ Yönetici Otoritesini Test Eden Çalışan",
        "metin": (
            "Kaan, 8 yıllık kıdemli bir yazılım geliştirici. Siz 6 ay önce müdür oldunuz. "
            "Kaan, toplantılarda kararlarınızı açıkça sorguluyor: 'Biz bunu daha önce denedik, olmadı.' "
            "Ekip önünde sizi zor durumda bırakmaktan çekinmiyor. "
            "Teknik bilgisi gerçekten güçlü ama tutumu ekip dinamiğini bozuyor. "
            "Son projede sizin kararınız olmadan farklı bir yöntem uyguladı."
        ),
    },
    {
        "kategori": "😢 Duygusal ve Kırılgan Çalışan",
        "metin": (
            "Zeynep, detaylı ve özenli işler çıkaran bir içerik editörü. "
            "Ancak herhangi bir geri bildirimde gözleri doluyor ve uzun süre motivasyonunu kaybediyor. "
            "Geçen hafta küçük bir düzeltme notunun ardından tuvalette ağladı. "
            "Ekip arkadaşları artık ona geri bildirim vermekten çekiniyor. "
            "Bu durum Zeynep'in gelişimini de engelliyor. Zeynep'le konuşmanız gerekiyor."
        ),
    },
    {
        "kategori": "📊 Çok Analitik Ama İletişimi Zor Çalışan",
        "metin": (
            "Mert, veri analistiniz. Sunumlarında 40 sayfalık Excel dosyaları hazırlıyor "
            "ve her kararı için 12 farklı senaryo modeli sunuyor. "
            "Yönetim kurulu toplantılarında herkes sıkılıyor çünkü Mert asla özet geçemiyor. "
            "Son toplantıda CEO 'Bu ne demek?' diye sordu ve Mert 30 dakika daha anlattı. "
            "Mert'e göre sorun dinleyicilerde: 'Veriye bakmadan karar veremem.'"
        ),
    },
]

# ─────────────────────────────────────────────
# ANAHTAR KELİMELER (Puanlama için)
# ─────────────────────────────────────────────

# Empati gösteren kelimeler
EMPATI_KELIMELERI = [
    "anlıyorum", "hissediyorum", "değerli", "takdir", "saygı", "zor",
    "desteklemek", "birlikte", "dinlemek", "endişe", "önemli", "anlamak",
    "teşekkür", "güçlü", "farkındayım", "empati", "yaklaşım", "his",
    "his", "duygu", "perspektif", "bakış açısı", "hissettiriyorum"
]

# Netlik gösteren kelimeler / ifadeler
NETLIK_KELIMELERI = [
    "beklentim", "hedef", "açıkça", "net", "sonuç", "adım", "yapmalı",
    "yapmamalı", "kural", "politika", "karar", "öncelik", "tarih",
    "süre", "sorumluluk", "görev", "plan", "somut", "ölçülebilir"
]

# Otorite ve sınır koyma kelimeleri
OTORITE_KELIMELERI = [
    "sınır", "kabul edilemez", "değiştirmeli", "bekliyorum", "gerekli",
    "zorunlu", "uyarı", "sonuç", "tutarsız", "standart", "norm",
    "politikaya aykırı", "müdahale", "düzeltme", "aksiyon", "adım"
]

# Stratejik yaklaşım kelimeleri
STRATEJI_KELIMELERI = [
    "uzun vadeli", "çözüm", "gelişim", "plan", "strateji", "hedef",
    "ilerleme", "fırsat", "potansiyel", "kariyer", "eğitim", "koçluk",
    "mentor", "destek", "izleme", "takip", "süreç", "yol haritası"
]

# Zayıf/belirsiz ifadeler (netlik puanını düşürür)
BELIRSIZ_IFADELER = [
    "belki", "sanırım", "galiba", "bir şekilde", "nasılsa", "zaten",
    "bilmiyorum", "olur mu", "isterseniz", "acaba", "falan", "filan"
]

# ─────────────────────────────────────────────
# PUANLAMA FONKSİYONU
# ─────────────────────────────────────────────
def puanla(cevap: str, senaryo: dict) -> dict:
    """Kullanıcının cevabını analiz eder ve puanlar."""
    cevap_kucuk = cevap.lower()
    kelime_sayisi = len(cevap.split())

    # --- EMPATİ PUANI (0-25) ---
    empati_eslesmesi = sum(1 for k in EMPATI_KELIMELERI if k in cevap_kucuk)
    empati_puan = min(25, empati_eslesmesi * 5 + (5 if kelime_sayisi > 30 else 0))

    # --- NETLİK PUANI (0-25) ---
    netlik_eslesmesi = sum(1 for k in NETLIK_KELIMELERI if k in cevap_kucuk)
    belirsiz_eslesmesi = sum(1 for k in BELIRSIZ_IFADELER if k in cevap_kucuk)
    netlik_puan = min(25, netlik_eslesmesi * 5 - belirsiz_eslesmesi * 4 + (5 if kelime_sayisi > 20 else 0))
    netlik_puan = max(0, netlik_puan)  # Negatife düşmesin

    # --- OTORİTE PUANI (0-25) ---
    otorite_eslesmesi = sum(1 for k in OTORITE_KELIMELERI if k in cevap_kucuk)
    otorite_puan = min(25, otorite_eslesmesi * 6 + (3 if kelime_sayisi > 25 else 0))

    # --- STRATEJİK YAKLAŞIM PUANI (0-25) ---
    strateji_eslesmesi = sum(1 for k in STRATEJI_KELIMELERI if k in cevap_kucuk)
    strateji_puan = min(25, strateji_eslesmesi * 5 + (5 if kelime_sayisi > 40 else 0))

    toplam = empati_puan + netlik_puan + otorite_puan + strateji_puan

    return {
        "empati": empati_puan,
        "netlik": netlik_puan,
        "otorite": otorite_puan,
        "strateji": strateji_puan,
        "toplam": toplam,
        "kelime_sayisi": kelime_sayisi,
        "belirsiz_eslesmesi": belirsiz_eslesmesi,
    }


def liderlik_profili(toplam: int) -> tuple[str, str]:
    """Skora göre liderlik profili ve açıklama döndürür."""
    if toplam >= 80:
        return "🦅 Stratejik Lider", "Durumu hem insani hem de kurumsal açıdan mükemmel yönetiyorsunuz."
    elif toplam >= 60:
        return "🌱 Gelişen Lider", "Doğru yöndesiniz. Birkaç kritik alanda güçlenme fırsatınız var."
    elif toplam >= 40:
        return "⚙️ Operasyonel Müdür", "Süreci yönetebiliyorsunuz ama insan boyutunu güçlendirmeniz gerekiyor."
    else:
        return "🛡️ Savunma Modu", "Zor durumlar karşısında reaktif kalıyorsunuz. Proaktif yaklaşım geliştirmek önemli."


def guclu_yonler(puan: dict) -> list[str]:
    """Güçlü yönleri listele."""
    yonler = []
    if puan["empati"] >= 15:
        yonler.append("✅ Güçlü empati kuruyorsunuz — çalışan kendini duyulmuş hissediyor.")
    if puan["netlik"] >= 15:
        yonler.append("✅ Net ve anlaşılır bir iletişim dili kullanıyorsunuz.")
    if puan["otorite"] >= 15:
        yonler.append("✅ Sınırlarınızı otoriteyle ve saygıyla koyabiliyorsunuz.")
    if puan["strateji"] >= 15:
        yonler.append("✅ Uzun vadeli ve çözüm odaklı düşünüyorsunuz.")
    if puan["kelime_sayisi"] > 50:
        yonler.append("✅ Detaylı ve kapsamlı bir yanıt oluşturdunuz.")
    if not yonler:
        yonler.append("⚠️ Şu an belirgin bir güçlü yön tespit edilemedi — aşağıdaki öneriye göz atın.")
    return yonler


def gelistirme_alanlari(puan: dict) -> list[str]:
    """Geliştirme alanlarını listele."""
    alanlar = []
    if puan["empati"] < 10:
        alanlar.append("🔧 Empati: Çalışanın bakış açısını daha fazla yansıtmayı deneyin.")
    if puan["netlik"] < 10:
        alanlar.append("🔧 Netlik: Beklentilerinizi somut adımlarla ifade edin.")
    if puan["belirsiz_eslesmesi"] > 0:
        alanlar.append("🔧 Belirsiz ifadeler ('belki', 'galiba' vb.) otoritenizi zayıflatıyor.")
    if puan["otorite"] < 10:
        alanlar.append("🔧 Otorite: Kabul edilemez davranışların sonuçlarını açıkça belirtmelisiniz.")
    if puan["strateji"] < 10:
        alanlar.append("🔧 Strateji: İleriye dönük bir gelişim planı veya takip mekanizması ekleyin.")
    if puan["kelime_sayisi"] < 20:
        alanlar.append("🔧 Yanıtınız çok kısa — daha kapsamlı bir iletişim deneyin.")
    if not alanlar:
        alanlar.append("🌟 Tüm alanlarda yeterli performans gösterdiniz!")
    return alanlar


def ornek_yanit(senaryo: dict) -> str:
    """Senaryoya göre örnek model yanıt döndür."""
    kategori = senaryo["kategori"]
    if "Egolu" in kategori:
        return (
            "\"Ahmet, performansına gerçekten değer veriyorum ve bu başarıyı takdir ediyorum. "
            "Aynı zamanda ekip içi iletişimimiz hakkında konuşmam gerekiyor. "
            "Arkadaşlarının fikirlerini toplantıda küçümsemenin kabul edilemez olduğunu açıkça söylemeliyim. "
            "Uzun vadeli başarı için teknik yetkinlik kadar ekip uyumu da kritik. "
            "Birlikte bu alanda nasıl ilerliyebiliriz, bunu konuşalım.\""
        )
    elif "Şikayet" in kategori:
        return (
            "\"Selin, geri bildirimlerini paylaşmanı önemsiyorum. "
            "Hangi konular gerçekten acil ve çözülebilir, birlikte sıralayalım. "
            "Bununla birlikte, şikayetlerin yoğunluğunun ekip enerjisini nasıl etkilediğini "
            "fark etmeni istiyorum. Yapıcı bir çözüm ortağı olmak için birlikte nasıl çalışabiliriz?\""
        )
    elif "Otorite" in kategori:
        return (
            "\"Kaan, teknik deneyimin ekip için büyük bir değer. "
            "Aynı zamanda karar süreçlerinin nasıl işlediğini netleştirmem gerekiyor: "
            "Farklı görüşleri toplantılarda paylaşmak doğru, ama toplantı dışında kendi inisiyatifinle "
            "farklı yöntemler uygulamak kabul edilemez. Beklentimi net koyuyorum. "
            "Görüşlerini her zaman dinlemeye hazırım — doğru kanalda.\""
        )
    elif "Duygusal" in kategori:
        return (
            "\"Zeynep, seninle açık bir konuşma yapmak istiyorum çünkü gelişimini önemsiyorum. "
            "Geri bildirim vermek, işin doğal bir parçası. Duygusal tepkilerin bazen seni "
            "ve ekibi zorladığını fark ediyorum. Bu konuda sana destek olmak istiyorum. "
            "Geri bildirimleri büyüme fırsatı olarak nasıl ele alabiliriz, bunu birlikte çalışabiliriz.\""
        )
    else:
        return (
            "\"Mert, analizlerinin derinliği gerçekten etkileyici. "
            "Yönetim kademesinin ihtiyacını da seninle paylaşmam gerekiyor: "
            "Karar vericiler için 3-5 dakikalık özet sunumlar hazırlamana ihtiyacım var. "
            "Detaylar ekte olabilir ama ana mesajı net ve hızlı iletmek kritik. "
            "Bunu birlikte nasıl yapılandırabiliriz?\""
        )

# ─────────────────────────────────────────────
# STREAMLIT ARAYÜZÜ
# ─────────────────────────────────────────────
def main():
    # Sayfa yapılandırması
    st.set_page_config(
        page_title="Zor Çalışan Simülatörü",
        page_icon="💼",
        layout="centered"
    )

    # Başlık
    st.title("💼 Zor Çalışan Simülatörü")
    st.markdown(
        "_Zor bir çalışan senaryosunda nasıl tepki verirdin? "
        "Liderlik becerilerini test et ve geliştir._"
    )
    st.divider()

    # Session state: uygulama durumunu saklar
    if "senaryo" not in st.session_state:
        st.session_state.senaryo = None
    if "degerlendirme" not in st.session_state:
        st.session_state.degerlendirme = None

    # ── SENARYO BAŞLATMA ──────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🎲 Senaryoyu Başlat", use_container_width=True, type="primary"):
            st.session_state.senaryo = random.choice(SENARYOLAR)
            st.session_state.degerlendirme = None  # Önceki değerlendirmeyi sıfırla

    with col2:
        if st.session_state.senaryo and st.button("🔄 Yeni Senaryo", use_container_width=True):
            st.session_state.senaryo = random.choice(SENARYOLAR)
            st.session_state.degerlendirme = None

    # ── SENARYO GÖSTERİMİ ─────────────────────
    if st.session_state.senaryo:
        senaryo = st.session_state.senaryo

        st.subheader(f"📋 Senaryo: {senaryo['kategori']}")
        st.info(senaryo["metin"])
        st.divider()

        # ── KULLANICI YANITI ───────────────────
        st.subheader("💬 Bu durumda çalışana ne söylersiniz?")
        cevap = st.text_area(
            label="Yanıtınızı buraya yazın...",
            height=150,
            placeholder="Örn: 'Ahmet, seninle özel olarak konuşmam gerekiyor. Performansın harika, "
                         "ancak ekip iletişiminde bazı değişiklikler bekliyorum...'",
            key="kullanici_cevap"
        )

        # Değerlendirme butonu
        if st.button("📊 Cevabı Değerlendir", type="primary", use_container_width=True):
            if not cevap.strip():
                st.warning("⚠️ Lütfen önce bir yanıt yazın.")
            elif len(cevap.split()) < 5:
                st.warning("⚠️ Yanıtınız çok kısa. Lütfen daha kapsamlı bir yanıt yazın.")
            else:
                st.session_state.degerlendirme = puanla(cevap, senaryo)
                st.session_state.degerlendirme["ornek"] = ornek_yanit(senaryo)
                st.session_state.degerlendirme["guclu"] = guclu_yonler(st.session_state.degerlendirme)
                st.session_state.degerlendirme["gelistir"] = gelistirme_alanlari(st.session_state.degerlendirme)

        # ── DEĞERLENDİRME SONUÇLARI ────────────
        if st.session_state.degerlendirme:
            d = st.session_state.degerlendirme
            st.divider()
            st.subheader("🎯 Değerlendirme Sonuçları")

            # Puan göstergeleri (4 kolon)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💬 Netlik", f"{d['netlik']}/25")
            c2.metric("⚡ Otorite", f"{d['otorite']}/25")
            c3.metric("❤️ Empati", f"{d['empati']}/25")
            c4.metric("🧠 Strateji", f"{d['strateji']}/25")

            st.divider()

            # Toplam skor ve profil
            toplam = d["toplam"]
            profil_adi, profil_aciklama = liderlik_profili(toplam)

            # Skor çubuğu
            st.markdown(f"### Toplam Skor: **{toplam}/100**")
            st.progress(toplam / 100)

            # Liderlik profili
            if toplam >= 80:
                st.success(f"**{profil_adi}** — {profil_aciklama}")
            elif toplam >= 60:
                st.info(f"**{profil_adi}** — {profil_aciklama}")
            elif toplam >= 40:
                st.warning(f"**{profil_adi}** — {profil_aciklama}")
            else:
                st.error(f"**{profil_adi}** — {profil_aciklama}")

            st.divider()

            # Güçlü yönler
            st.subheader("💪 Güçlü Yönleriniz")
            for g in d["guclu"]:
                st.write(g)

            # Geliştirme alanları
            st.subheader("📈 Geliştirme Alanlarınız")
            for a in d["gelistir"]:
                st.write(a)

            # Model yanıt
            st.subheader("💡 Örnek Model Yanıt")
            st.success(d["ornek"])

            st.divider()
            st.caption("💡 İpucu: Yanıtınızı düzenleyip tekrar değerlendirebilirsiniz.")

    else:
        # Henüz senaryo seçilmedi
        st.markdown(
            """
            ### Nasıl Çalışır?
            1. **"Senaryoyu Başlat"** butonuna bas
            2. Karşına gerçekçi bir çalışan senaryosu çıkacak
            3. Yönetici olarak nasıl yanıt vereceğini yaz
            4. **"Cevabı Değerlendir"** ile liderlik skorunu gör
            """
        )


# Uygulamayı çalıştır
if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────
# ÇALIŞTIRMA KOMUTU:
# streamlit run app.py
# ─────────────────────────────────────────────
