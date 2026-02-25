"""
╔══════════════════════════════════════════════════════════╗
║       ZOR ÇALIŞAN SİMÜLATÖRÜ — v2.0                     ║
║       Liderlik Gelişim Dashboard                         ║
╚══════════════════════════════════════════════════════════╝
Çalıştırma: streamlit run app.py
Gereksinimler: pip install streamlit plotly
"""

import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime

# ══════════════════════════════════════════════
# VERİ: SENARYOLAR
# ══════════════════════════════════════════════
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

# ══════════════════════════════════════════════
# VERİ: ANAHTAR KELİMELER
# ══════════════════════════════════════════════
EMPATI_KELIMELERI = [
    "anlıyorum", "hissediyorum", "değerli", "takdir", "saygı", "zor",
    "desteklemek", "birlikte", "dinlemek", "endişe", "önemli", "anlamak",
    "teşekkür", "güçlü", "farkındayım", "empati", "yaklaşım", "his",
    "duygu", "perspektif", "bakış açısı", "sen", "seninle", "sizi"
]
NETLIK_KELIMELERI = [
    "beklentim", "hedef", "açıkça", "net", "sonuç", "adım", "yapmalı",
    "yapmamalı", "kural", "politika", "karar", "öncelik", "tarih",
    "süre", "sorumluluk", "görev", "plan", "somut", "ölçülebilir", "deadline"
]
OTORITE_KELIMELERI = [
    "sınır", "kabul edilemez", "değiştirmeli", "bekliyorum", "gerekli",
    "zorunlu", "uyarı", "sonuç", "standart", "norm", "müdahale",
    "düzeltme", "aksiyon", "tutarsız", "politikaya aykırı", "netleştirmek"
]
STRATEJI_KELIMELERI = [
    "uzun vadeli", "çözüm", "gelişim", "plan", "strateji", "hedef",
    "ilerleme", "fırsat", "potansiyel", "kariyer", "eğitim", "koçluk",
    "mentor", "destek", "izleme", "takip", "süreç", "yol haritası", "gelecek"
]
BELIRSIZ_IFADELER = [
    "belki", "sanırım", "galiba", "bir şekilde", "nasılsa", "zaten",
    "bilmiyorum", "olur mu", "isterseniz", "acaba", "falan", "filan"
]

# ══════════════════════════════════════════════
# VERİ: GELİŞİM ÖNERİ MOTORu (rule-based)
# ══════════════════════════════════════════════
GELISIM_ONERILERI = {
    "empati": {
        "kritik": {
            "baslik": "🔴 Kritik Gelişim Alanı — Empati",
            "davranislar": [
                "Konuşmaya başlamadan önce çalışanın bakış açısını 30 saniye sessizce düşün.",
                "Her geri bildirimde önce bir 'güçlü yön' belirt, sonra gelişim alanına geç.",
                "Aktif dinleme tekniği: Karşındaki konuşurken not al, sonra özetle."
            ],
            "cumleler": [
                "\"Seni duyduğumu hissettirmek istiyorum — bu durumun sana zor geldiğini anlıyorum.\"",
                "\"Senin bakış açından baktığımda, bu durumun neden sinir bozucu olduğunu görüyorum.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta her zor konuşmaya 'Seni duyuyorum' veya 'Seni anlıyorum' cümlesiyle başla. 5 konuşmada uygula ve nasıl hissettirdiğini not et."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Empati",
            "davranislar": [
                "Yansıtma tekniğini kullan: Karşındakinin söylediklerini kendi cümlelerinle tekrarla.",
                "'Biz dili' kullan: 'Sen yanlış yapıyorsun' yerine 'Biz bunu birlikte çözelim' de.",
                "Vücut dili: Göz teması kur, kollarını kavuşturma."
            ],
            "cumleler": [
                "\"Birlikte bu zorluğun üstesinden gelebiliriz.\"",
                "\"Söylediklerini duydum — şimdi beraber çözüm üretelim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta 3 farklı toplantıda karşı tarafın söylediklerini kendi cümlelerinle özetle ve onay al."
        },
        "guclu": {
            "baslik": "🟢 Güçlü Alan — Empati",
            "davranislar": [
                "Bu becerini ekip kültürüne yay — diğer yöneticilere rol model ol.",
                "Empatiyi stratejik kararlarla dengele, sınırlarını koruyarak kullan.",
                "Empati becerini mentorluk ilişkilerinde daha sistematik kullan."
            ],
            "cumleler": [
                "\"Ekibimin duygusal iklimini düzenli olarak ölçmek istiyorum.\"",
                "\"Güçlü empatin var — şimdi bunu net sınırlarla dengeleme vakti.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Ekibindeki bir kişiyle bu hafta 'kariyer hedefleri' üzerine 15 dakikalık birebir görüşme yap."
        }
    },
    "netlik": {
        "kritik": {
            "baslik": "🔴 Kritik Gelişim Alanı — Netlik",
            "davranislar": [
                "Her konuşma sonunda 'Anlaştık mı?' yerine 'Bir sonraki adımın ne olduğunu söyler misin?' de.",
                "Kısa cümle kuralı: Bir fikri 15 kelimeden fazlasında anlatma.",
                "Somut talep: 'Daha iyi yap' yerine 'Raporun ilk sayfasında sadece 3 madde olsun' de."
            ],
            "cumleler": [
                "\"Bu konuşmadan çıkarken ikimizin de anlayacağı tek bir sonuç olsun: [X]\"",
                "\"Senden Cuma gününe kadar şunu bekliyorum: [net hedef].\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta her toplantıyı net bir kapanış cümlesiyle bitir: 'Bu toplantıdan çıkan karar: ...' — 5 toplantıda uygula."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Netlik",
            "davranislar": [
                "Konuşma başında hedefi söyle: 'Bugün 10 dakikada şu konuyu netleştireceğiz.'",
                "Eylem fiilleri kullan: 'Düşünelim' yerine 'Karar verelim' de.",
                "Belirsiz kelimelerden kaçın: 'yakında', 'biraz', 'daha iyi' gibi ifadeleri sayıyla değiştir."
            ],
            "cumleler": [
                "\"Senden şunu bekliyorum: [X tarihinde], [Y çıktısı].\"",
                "\"Bu konuşmanın tek amacı şu kararı almak: ...\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta 3 e-postanda 'yakında' veya 'biraz' kelimesi geçiyorsa, somut tarih ve sayıyla değiştir."
        },
        "guclu": {
            "baslik": "🟢 Güçlü Alan — Netlik",
            "davranislar": [
                "Netliğini empatiyle dengele — bazen çok doğrudan olmak ilişkiyi zedeleyebilir.",
                "Ekibine de net iletişim becerisi kazandır.",
                "Karmaşık konuları basitleştirme becerinizi daha geniş kitlelere taşı."
            ],
            "cumleler": [
                "\"Net iletişim kuruyorum — şimdi bunu ekip standartlarına dönüştürme zamanı.\"",
                "\"Beklentilerimi açık koyarım — bu güçlü yönümü ilişkileri güçlendirmek için de kullanabilirim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Ekibinle 'iletişim kuralları' belgesi hazırla — net beklentileri yazılı hale getir."
        }
    },
    "otorite": {
        "kritik": {
            "baslik": "🔴 Kritik Gelişim Alanı — Otorite & Sınır Koyma",
            "davranislar": [
                "Kararlarını açıklarken özür dileme — 'Bu konuda kararım şu' de.",
                "Kabul edilemez davranışa anında tepki ver, biriktirme.",
                "Sonuçları net söyle: 'Bu devam ederse şu adımı atacağım' cümlesini kullan."
            ],
            "cumleler": [
                "\"Bu davranışın ekip normlarına aykırı olduğunu ve değişmesi gerektiğini söylüyorum.\"",
                "\"Bu konuda kararım nettir. Süreci birlikte yönetelim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta en az 2 durumda 'Hayır' veya 'Bu kabul edilemez' cümlesini özür eklemeden kullan."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Otorite & Sınır Koyma",
            "davranislar": [
                "Sakin ama kararlı bir ton kullan — yüksek ses gerekmez.",
                "Sınırlarını önceden belirle ve tutarlı ol.",
                "Kararları ekip önünde sorgulandığında 'Bunu birebir konuşalım' de ve toplantıya devam et."
            ],
            "cumleler": [
                "\"Görüşünü duydum — karar bende ve şu an şu yönde ilerliyoruz.\"",
                "\"Ekip içinde farklı çalışma yöntemleri önce benimle paylaşılmalı.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta bir toplantıda biri seni sorguladığında 'Bunu birebir konuşalım' de ve toplantıyı kıs."
        },
        "guclu": {
            "baslik": "🟢 Güçlü Alan — Otorite & Sınır Koyma",
            "davranislar": [
                "Otoriteni empatiyle dengele — çalışanlar hem saygı hem güven hissetmeli.",
                "Sınır koyarken gerekçe sun — 'çünkü' kelimesini kullan.",
                "Gücünü ekibi geliştirmek için kullan, kontrol için değil."
            ],
            "cumleler": [
                "\"Sınırlarımı net koyarım — ve bunun arkasında her zaman ekibin iyiliği var.\"",
                "\"Otoriter değil, güvenilir bir lider olmak istiyorum.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta bir kararını ekiple paylaşırken gerekçesini de anlat — 'çünkü...' diye başlayan bir cümle ekle."
        }
    },
    "strateji": {
        "kritik": {
            "baslik": "🔴 Kritik Gelişim Alanı — Stratejik Yaklaşım",
            "davranislar": [
                "Her soruna 'Bunun altında ne var?' diye sor — kök nedeni bul.",
                "Sebep-sonuç bağla: 'Bu davranış devam ederse X olur, Y olur' çerçevesini kullan.",
                "Konuşmayı uzun vadeli çerçevede kur: 'Gelecek 3 ayda nasıl görünmek istiyorsun?'"
            ],
            "cumleler": [
                "\"Bu durumu kısa vadede değil, kariyer gelişimin açısından ele alalım.\"",
                "\"Bu hafta çözmek istediğimiz problem şu — uzun vadeli hedefimiz ise şu.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta bir çalışanınla 'kariyer hedefleri' konuşması yap ve 3 aylık ortak bir hedef belirle."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Stratejik Yaklaşım",
            "davranislar": [
                "Konuşmayı sadece mevcut soruna değil, gelişim fırsatına bağla.",
                "Takip mekanizması kur: 'Bunu 2 hafta sonra tekrar konuşalım' de.",
                "Birden fazla seçenek sun: 'İki yol var: biri X, diğeri Y.'"
            ],
            "cumleler": [
                "\"Bu konuşmayı 2 hafta sonra takip edeceğim — ne değişti göreceğiz.\"",
                "\"Sana iki seçenek sunuyorum — hangisi daha uygun olduğuna birlikte karar verelim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta yaptığın her zor konuşmaya bir 'takip tarihi' belirle ve takvime ekle."
        },
        "guclu": {
            "baslik": "🟢 Güçlü Alan — Stratejik Yaklaşım",
            "davranislar": [
                "Stratejik düşünceni ekibinle paylaş — onları da bu çerçeveye dahil et.",
                "Büyük resmi görürken günlük sorunları da kaçırma.",
                "Stratejik planlarını ölçülebilir metriklerle takip et."
            ],
            "cumleler": [
                "\"Uzun vadeli düşünürüm — şimdi bu vizyonu ekiple paylaşma zamanı.\"",
                "\"Stratejik bakışım güçlü — bunu somut aksiyon planlarına dönüştürmeye devam edeceğim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Ekibinle aylık 'strateji check-in' toplantısı başlat — 30 dakika, sadece büyük resim."
        }
    }
}

# ══════════════════════════════════════════════
# ÖRNEK MODEL YANITLAR
# ══════════════════════════════════════════════
def ornek_yanit(senaryo):
    kategori = senaryo["kategori"]
    if "Egolu" in kategori:
        return (
            "\"Ahmet, performansına gerçekten değer veriyorum ve bu başarıyı takdir ediyorum. "
            "Aynı zamanda ekip içi iletişimimiz hakkında konuşmam gerekiyor. "
            "Arkadaşlarının fikirlerini toplantıda küçümsemenin kabul edilemez olduğunu açıkça söylemeliyim. "
            "Uzun vadeli başarı için teknik yetkinlik kadar ekip uyumu da kritik. "
            "Birlikte bu alanda nasıl ilerleyebiliriz, bunu konuşalım.\""
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
            "Farklı görüşleri toplantılarda paylaşmak doğru, ancak kendi inisiyatifinle "
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

# ══════════════════════════════════════════════
# PUANLAMA FONKSİYONU
# ══════════════════════════════════════════════
def puanla(cevap: str) -> dict:
    """Kullanıcının metnini analiz eder, 4 boyutta 0-25 puan verir."""
    c = cevap.lower()
    kelime_sayisi = len(cevap.split())

    empati   = sum(1 for k in EMPATI_KELIMELERI   if k in c)
    netlik   = sum(1 for k in NETLIK_KELIMELERI    if k in c)
    otorite  = sum(1 for k in OTORITE_KELIMELERI   if k in c)
    strateji = sum(1 for k in STRATEJI_KELIMELERI  if k in c)
    belirsiz = sum(1 for k in BELIRSIZ_IFADELER     if k in c)

    p_empati   = min(25, empati   * 5 + (3 if kelime_sayisi > 30 else 0))
    p_netlik   = min(25, max(0, netlik * 5 - belirsiz * 4 + (3 if kelime_sayisi > 20 else 0)))
    p_otorite  = min(25, otorite  * 6 + (3 if kelime_sayisi > 25 else 0))
    p_strateji = min(25, strateji * 5 + (5 if kelime_sayisi > 40 else 0))

    return {
        "empati":   p_empati,
        "netlik":   p_netlik,
        "otorite":  p_otorite,
        "strateji": p_strateji,
        "toplam":   p_empati + p_netlik + p_otorite + p_strateji,
        "kelime":   kelime_sayisi,
        "belirsiz": belirsiz,
    }

# ══════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════
def seviye(puan: int) -> str:
    """0-10 kritik | 11-18 orta | 19-25 guclu"""
    if puan <= 10:
        return "kritik"
    elif puan <= 18:
        return "orta"
    return "guclu"


def liderlik_profili(toplam: int) -> tuple:
    if toplam >= 80:
        return "🦅 Stratejik Lider", "Durumu hem insani hem kurumsal açıdan mükemmel yönetiyorsunuz.", "success"
    elif toplam >= 60:
        return "🌱 Gelişen Lider", "Doğru yöndesiniz. Birkaç kritik alanda güçlenme fırsatınız var.", "info"
    elif toplam >= 40:
        return "⚙️ Operasyonel Müdür", "Süreci yönetebiliyorsunuz ama insan boyutunu güçlendirmeniz gerekiyor.", "warning"
    else:
        return "🛡️ Savunma Modu", "Reaktif kalıyorsunuz. Proaktif yaklaşım geliştirmek kritik.", "error"


def haftalik_plan(puan: dict) -> dict:
    """En düşük skoru bulup haftalık aksiyon planı üretir."""
    alanlar = {
        "empati":   puan["empati"],
        "netlik":   puan["netlik"],
        "otorite":  puan["otorite"],
        "strateji": puan["strateji"]
    }
    en_dusuk_alan = min(alanlar, key=alanlar.get)
    en_dusuk_puan = alanlar[en_dusuk_alan]

    planlar = {
        "empati": {
            "hedef":   "Empati kurma becerisini güçlendir",
            "aksiyon": "Bu hafta her zor konuşmaya empati kuran bir cümleyle başla.",
            "olcum":   "5 konuşmada uygula ve sonuçları not et.",
            "ipucu":   "💡 'Seni duyuyorum / Seni anlıyorum / Bu durumun zor olduğunu görüyorum' ile başla."
        },
        "netlik": {
            "hedef":   "Net ve somut iletişim kur",
            "aksiyon": "Bu hafta her toplantıyı net bir kapanış cümlesiyle bitir.",
            "olcum":   "5 toplantıda uygula: 'Bu toplantıdan çıkan karar: ...'",
            "ipucu":   "💡 'Yakında', 'biraz', 'daha iyi' yerine tarih ve sayı kullan."
        },
        "otorite": {
            "hedef":   "Sınırlarını kararlılıkla koy",
            "aksiyon": "Bu hafta en az 2 durumda 'Hayır' veya 'Bu kabul edilemez' de.",
            "olcum":   "Özür dilemeden, sakin ama net söyle — tepkiyi gözlemle.",
            "ipucu":   "💡 Otorite yüksek ses değil, net ve tutarlı bir tutum demektir."
        },
        "strateji": {
            "hedef":   "Uzun vadeli çerçeve kur",
            "aksiyon": "Her zor konuşmaya bir 'takip tarihi' belirle.",
            "olcum":   "Haftada 3 görüşmede sebep-sonuç bağlantısı kur ve takvime ekle.",
            "ipucu":   "💡 'Bu durumun uzun vadede sana ne kazandıracağını konuşalım' ile başla."
        }
    }

    return {"alan": en_dusuk_alan, "puan": en_dusuk_puan, **planlar[en_dusuk_alan]}


# ══════════════════════════════════════════════
# GRAFİK FONKSİYONLARI
# ══════════════════════════════════════════════
def radar_chart(puan: dict):
    """Radar (örümcek ağı) grafik oluşturur — 4 liderlik boyutu."""
    kategoriler = ["Netlik", "Empati", "Otorite", "Strateji", "Netlik"]  # Kapanış için ilk tekrar
    degerler    = [puan["netlik"], puan["empati"], puan["otorite"], puan["strateji"], puan["netlik"]]

    fig = go.Figure()

    # Gri referans alanı (max = 25)
    fig.add_trace(go.Scatterpolar(
        r=[25, 25, 25, 25, 25],
        theta=kategoriler,
        fill="toself",
        fillcolor="rgba(200,200,200,0.12)",
        line=dict(color="rgba(180,180,180,0.4)"),
        showlegend=False
    ))

    # Kullanıcı skoru
    fig.add_trace(go.Scatterpolar(
        r=degerler,
        theta=kategoriler,
        fill="toself",
        fillcolor="rgba(99,110,250,0.25)",
        line=dict(color="rgba(99,110,250,0.9)", width=2.5),
        name="Skorun",
        marker=dict(size=9, color="rgba(99,110,250,1)")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 25], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=14))
        ),
        showlegend=False,
        margin=dict(t=30, b=30, l=40, r=40),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def trend_chart(gecmis: list):
    """Geçmiş skorların line chart'ını oluşturur."""
    if len(gecmis) < 2:
        return None

    indeksler  = list(range(1, len(gecmis) + 1))
    toplamlar  = [g["toplam"] for g in gecmis]
    empatiler  = [g["empati"] for g in gecmis]
    netlikleri = [g["netlik"] for g in gecmis]
    otoriteler = [g["otorite"] for g in gecmis]
    stratejiler = [g["strateji"] for g in gecmis]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=indeksler, y=[t // 4 for t in toplamlar],
        name="Ort. Toplam", line=dict(color="#636EFA", width=3),
        mode="lines+markers", marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(x=indeksler, y=empatiler,   name="Empati",   line=dict(color="#EF553B", width=1.5, dash="dot"), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=indeksler, y=netlikleri,  name="Netlik",   line=dict(color="#00CC96", width=1.5, dash="dot"), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=indeksler, y=otoriteler,  name="Otorite",  line=dict(color="#AB63FA", width=1.5, dash="dot"), mode="lines+markers"))
    fig.add_trace(go.Scatter(x=indeksler, y=stratejiler, name="Strateji", line=dict(color="#FFA15A", width=1.5, dash="dot"), mode="lines+markers"))

    fig.update_layout(
        yaxis=dict(range=[0, 25], title="Puan (0-25)"),
        xaxis=dict(title="Deneme #", tickvals=indeksler),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=300,
        margin=dict(t=50, b=40, l=40, r=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


# ══════════════════════════════════════════════
# ANA UYGULAMA
# ══════════════════════════════════════════════
def main():
    st.set_page_config(
        page_title="Zor Çalışan Simülatörü v2",
        page_icon="💼",
        layout="wide"
    )

    # ── SESSION STATE başlangıç değerleri ─────
    for key, default in [
        ("senaryo", None),
        ("degerlendirme", None),
        ("gecmis_skorlar", [])
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── 2 SEKME ───────────────────────────────
    tab1, tab2 = st.tabs(["🎮 Simülatör", "📊 Gelişim Dashboard"])

    # ══════════════════════════════════════════
    # SEKME 1 — SİMÜLATÖR
    # ══════════════════════════════════════════
    with tab1:
        st.title("💼 Zor Çalışan Simülatörü")
        st.markdown("_Zor bir çalışan senaryosunda nasıl tepki verirdin? Liderlik becerilerini test et ve geliştir._")
        st.divider()

        # Butonlar
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🎲 Senaryoyu Başlat", use_container_width=True, type="primary"):
                st.session_state.senaryo = random.choice(SENARYOLAR)
                st.session_state.degerlendirme = None
        with col2:
            if st.session_state.senaryo:
                if st.button("🔄 Yeni Senaryo", use_container_width=True):
                    st.session_state.senaryo = random.choice(SENARYOLAR)
                    st.session_state.degerlendirme = None

        # Senaryo kartı
        if st.session_state.senaryo:
            senaryo = st.session_state.senaryo
            st.subheader(f"📋 {senaryo['kategori']}")
            st.info(senaryo["metin"])
            st.divider()

            # Yanıt alanı
            st.subheader("💬 Bu durumda çalışana ne söylersiniz?")
            cevap = st.text_area(
                "Yanıtınızı buraya yazın...",
                height=160,
                placeholder="Örn: 'Seninle özel olarak konuşmam gerekiyor. Performansın harika, ancak...'",
                key="kullanici_cevap"
            )

            if st.button("📊 Cevabı Değerlendir", type="primary", use_container_width=True):
                if not cevap.strip() or len(cevap.split()) < 5:
                    st.warning("⚠️ Lütfen en az birkaç cümle içeren bir yanıt yazın.")
                else:
                    puan = puanla(cevap)
                    puan["ornek"]   = ornek_yanit(senaryo)
                    puan["plan"]    = haftalik_plan(puan)
                    puan["zaman"]   = datetime.now().strftime("%H:%M")
                    puan["senaryo"] = senaryo["kategori"]
                    st.session_state.degerlendirme = puan
                    # Geçmişe ekle
                    st.session_state.gecmis_skorlar.append({k: puan[k] for k in
                        ["zaman", "toplam", "empati", "netlik", "otorite", "strateji", "senaryo"]})

            # ── DEĞERLENDİRME EKRANI ──────────
            if st.session_state.degerlendirme:
                d = st.session_state.degerlendirme
                st.divider()
                st.subheader("🎯 Değerlendirme Sonuçları")

                # 4 metrik kutucuğu
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💬 Netlik",   f"{d['netlik']}/25")
                c2.metric("⚡ Otorite",  f"{d['otorite']}/25")
                c3.metric("❤️ Empati",   f"{d['empati']}/25")
                c4.metric("🧠 Strateji", f"{d['strateji']}/25")

                st.divider()

                # Liderlik profili
                toplam = d["toplam"]
                profil, aciklama, stil = liderlik_profili(toplam)
                st.markdown(f"### Toplam Skor: **{toplam}/100**")
                st.progress(toplam / 100)

                if   stil == "success": st.success(f"**{profil}** — {aciklama}")
                elif stil == "info":    st.info(   f"**{profil}** — {aciklama}")
                elif stil == "warning": st.warning(f"**{profil}** — {aciklama}")
                else:                   st.error(  f"**{profil}** — {aciklama}")

                st.divider()

                # ── ALAN BAZLI GELİŞİM ÖNERİLERİ ──
                st.subheader("📈 Alan Bazlı Gelişim Önerileri")

                alan_listesi = [
                    ("empati",   "❤️ Empati",   d["empati"]),
                    ("netlik",   "💬 Netlik",    d["netlik"]),
                    ("otorite",  "⚡ Otorite",   d["otorite"]),
                    ("strateji", "🧠 Strateji",  d["strateji"]),
                ]

                for alan_key, alan_adi, alan_puani in alan_listesi:
                    sev   = seviye(alan_puani)
                    oneri = GELISIM_ONERILERI[alan_key][sev]

                    # Kritik alanlar otomatik açık gösterilsin
                    with st.expander(f"{oneri['baslik']} — {alan_puani}/25", expanded=(sev == "kritik")):

                        st.markdown("**🎯 Somut Davranış Önerileri:**")
                        for i, davranis in enumerate(oneri["davranislar"], 1):
                            st.markdown(f"{i}. {davranis}")

                        st.markdown("**💬 Pratik Cümle Örnekleri:**")
                        for cumle in oneri["cumleler"]:
                            st.markdown(f"- {cumle}")

                        st.info(oneri["egzersiz"])

                st.divider()

                # ── HAFTALIK AKSİYON PLANI ────────
                plan = d["plan"]
                alan_label = {
                    "empati": "❤️ Empati", "netlik": "💬 Netlik",
                    "otorite": "⚡ Otorite", "strateji": "🧠 Strateji"
                }
                st.subheader("📅 Bu Hafta Liderlik Aksiyon Planın")
                st.markdown(f"**Öncelikli alan:** {alan_label[plan['alan']]} ({plan['puan']}/25 — en düşük skor)")

                colA, colB = st.columns(2)
                with colA:
                    st.markdown(f"**🎯 Haftalık Hedef:**  \n{plan['hedef']}")
                    st.markdown(f"**✅ Aksiyon:**  \n{plan['aksiyon']}")
                with colB:
                    st.markdown(f"**📏 Ölçüm:**  \n{plan['olcum']}")
                    st.info(plan["ipucu"])

                st.divider()

                # ── ÖRNEK MODEL YANIT ─────────────
                st.subheader("💡 Örnek Model Yanıt")
                st.success(d["ornek"])
                st.caption("💡 Yanıtınızı düzenleyip tekrar değerlendirebilirsiniz.")

        else:
            # Henüz başlamadı
            st.markdown("""
            ### Nasıl Çalışır?
            1. **"Senaryoyu Başlat"** butonuna bas
            2. Gerçekçi bir çalışan senaryosuyla karşılaş
            3. Yönetici olarak yanıtını yaz
            4. **"Cevabı Değerlendir"** ile liderlik skorunu gör
            5. Kişisel gelişim planını ve alan bazlı önerileri incele
            6. **Gelişim Dashboard** sekmesinden ilerlemeni takip et
            """)

    # ══════════════════════════════════════════
    # SEKME 2 — GELİŞİM DASHBOARD
    # ══════════════════════════════════════════
    with tab2:
        st.title("📊 Liderlik Gelişim Dashboard")

        if not st.session_state.degerlendirme:
            st.info("ℹ️ Henüz bir değerlendirme yapılmadı. 🎮 Simülatör sekmesinden başlayın!")
            return

        d      = st.session_state.degerlendirme
        toplam = d["toplam"]
        profil, aciklama, stil = liderlik_profili(toplam)

        # ── ÖZET METRİKLER ────────────────────
        st.subheader("📌 Son Değerlendirme")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("🏆 Toplam",   f"{toplam}/100")
        m2.metric("💬 Netlik",   f"{d['netlik']}/25")
        m3.metric("❤️ Empati",   f"{d['empati']}/25")
        m4.metric("⚡ Otorite",  f"{d['otorite']}/25")
        m5.metric("🧠 Strateji", f"{d['strateji']}/25")

        if   stil == "success": st.success(f"**{profil}** — {aciklama}")
        elif stil == "info":    st.info(   f"**{profil}** — {aciklama}")
        elif stil == "warning": st.warning(f"**{profil}** — {aciklama}")
        else:                   st.error(  f"**{profil}** — {aciklama}")

        st.divider()

        # ── RADAR + ALAN ANALİZİ ──────────────
        col_radar, col_analiz = st.columns([1, 1])

        with col_radar:
            st.subheader("🕸️ Liderlik Profil Haritası")
            st.plotly_chart(radar_chart(d), use_container_width=True)

        with col_analiz:
            st.subheader("🔍 Alan Analizi")

            # Düşükten yükseğe sırala
            alanlar_sirali = sorted([
                ("❤️ Empati",   d["empati"]),
                ("💬 Netlik",   d["netlik"]),
                ("⚡ Otorite",  d["otorite"]),
                ("🧠 Strateji", d["strateji"]),
            ], key=lambda x: x[1])

            for alan_adi, puan_val in alanlar_sirali:
                sev    = seviye(puan_val)
                renk   = {"kritik": "🔴", "orta": "🟡",    "guclu": "🟢"}[sev]
                etiket = {"kritik": "Kritik", "orta": "Gelişiyor", "guclu": "Güçlü"}[sev]
                st.markdown(f"{renk} **{alan_adi}** — {puan_val}/25  *({etiket})*")
                st.progress(puan_val / 25)

            # En zayıf alan vurgusu
            plan = d["plan"]
            alan_label = {
                "empati": "❤️ Empati", "netlik": "💬 Netlik",
                "otorite": "⚡ Otorite", "strateji": "🧠 Strateji"
            }
            st.divider()
            st.markdown(f"**🎯 Öncelikli Alan:** {alan_label[plan['alan']]}")
            st.markdown(f"*{plan['aksiyon']}*")

        st.divider()

        # ── GELİŞİM TRENDİ LINE CHART ─────────
        st.subheader("📈 Gelişim Trendi")
        gecmis = st.session_state.gecmis_skorlar

        if len(gecmis) >= 2:
            fig_trend = trend_chart(gecmis)
            if fig_trend:
                st.plotly_chart(fig_trend, use_container_width=True)
        else:
            kalan = 2 - len(gecmis)
            st.info(f"📊 Trend grafiği için {kalan} değerlendirme daha yap. Simülatörden devam et!")

        # ── GEÇMİŞ SKORLAR TABLOSU ───────────
        if gecmis:
            st.divider()
            st.subheader("📋 Tüm Değerlendirmeler")

            for i, g in enumerate(reversed(gecmis), 1):
                gercek_no = len(gecmis) - i + 1
                with st.expander(
                    f"#{gercek_no} — {g['zaman']} | Toplam: {g['toplam']}/100 | {g['senaryo']}"
                ):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Netlik",   g["netlik"])
                    c2.metric("Empati",   g["empati"])
                    c3.metric("Otorite",  g["otorite"])
                    c4.metric("Strateji", g["strateji"])

            st.divider()
            if st.button("🗑️ Geçmişi Temizle", type="secondary"):
                st.session_state.gecmis_skorlar  = []
                st.session_state.degerlendirme   = None
                st.rerun()


# ══════════════════════════════════════════════
if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────
# ÇALIŞTIRMA KOMUTLARI:
# pip install streamlit plotly
# streamlit run app.py
# ─────────────────────────────────────────────
