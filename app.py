"""
╔══════════════════════════════════════════════════════════╗
║       ZOR ÇALIŞAN SİMÜLATÖRÜ — v2.1                     ║
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
# VERİ: SENARYOLAR (15 adet, 5 kategori)
# ══════════════════════════════════════════════
SENARYOLAR = [

    # ── KATEGORİ 1: PERFORMANSLI AMA EGOLU ─────────────────
    {
        "kategori": "🏆 Performansı Yüksek Ama Egolu Çalışan",
        "metin": (
            "Ahmet, şirketinizin en iyi satış temsilcisi. Geçen çeyrekte hedefini %140 oranında aştı. "
            "Ancak son toplantıda ekip arkadaşlarının fikirlerini açıkça küçümsedi: "
            "'Bu kadar basit bir şeyi neden anlayamıyorlar?' dedi. "
            "Diğer çalışanlar şikayetlerini size iletmeye başladı. "
            "Ahmet ise durumun abartıldığını düşünüyor ve özür dilemeyi reddediyor."
        ),
    },
    {
        "kategori": "🏆 Performansı Yüksek Ama Egolu Çalışan",
        "metin": (
            "Defne, yazılım ekibinin en hızlı geliştiricisi. Her sprint'te en fazla görevi o tamamlıyor. "
            "Ancak code review toplantılarında diğerlerinin kodlarını 'amatörce' diye nitelendiriyor "
            "ve bunu yüzlerine karşı söylemekten çekinmiyor. "
            "İki junior çalışan geçen hafta içinde kovuşturma korkusuyla sessiz kalmayı tercih etti. "
            "Defne ise 'Ben sadece kalite standartlarını koruyorum' diyor."
        ),
    },
    {
        "kategori": "🏆 Performansı Yüksek Ama Egolu Çalışan",
        "metin": (
            "Burak, bölgenin en çok satış yapan müdürü. Rakamları mükemmel ama ekibin rotasyon oranı "
            "son 6 ayda %60'a çıktı. Çıkan çalışanların hepsi çıkış mülakatında Burak'ın "
            "yönetim tarzını gerekçe olarak gösterdi. "
            "Burak 'Zayıflar zaten kalmak zorunda değil, ben A takımı istiyorum' diyor. "
            "İK departmanı artık size resmi şikayette bulundu."
        ),
    },

    # ── KATEGORİ 2: SÜREKLİ ŞİKAYET EDEN ──────────────────
    {
        "kategori": "😤 Sürekli Şikayet Eden Çalışan",
        "metin": (
            "Selin, her hafta en az bir kez odanıza gelip yeni bir şikayetle çıkıyor. "
            "Bu hafta: 'Klima çok soğuk, maaş zamanı geç yatıyor, toplantılar çok uzun.' "
            "Şikayetlerinin bir kısmı haklı olsa da sürekli olumsuz enerji ekibi yıpratıyor. "
            "Diğer çalışanlar Selin'den uzak durmaya başladı. "
            "Selin ise 'Sadece gerçekleri söylüyorum' diyor."
        ),
    },
    {
        "kategori": "😤 Sürekli Şikayet Eden Çalışan",
        "metin": (
            "Tolga, her sabah kahve makinesinin yanında şikayet seansı düzenliyor. "
            "'Şirket bize değer vermiyor, zam yok, terfi yok, vizyon yok' söylemi artık "
            "ekibin günlük rutinine girdi. Yeni başlayan iki çalışan bu konuşmalardan etkilenip "
            "işten ayrılmayı düşündüklerini HR'a iletti. "
            "Tolga'nın performansı aslında orta seviyede — ne çok iyi ne çok kötü."
        ),
    },
    {
        "kategori": "😤 Sürekli Şikayet Eden Çalışan",
        "metin": (
            "Naz, proje toplantılarında her öneriye 'Bu daha önce de denendi, olmadı' ya da "
            "'Bütçemiz buna yetmez' diyerek itiraz ediyor. "
            "Ekip artık yeni fikirlerini toplantıda paylaşmak yerine size ayrıca geliyor. "
            "Naz farkında değil ama yaratıcılığın önündeki en büyük engel haline geldi. "
            "Kendisi ise 'Ben sadece gerçekçi biriyim' diye savunuyor."
        ),
    },

    # ── KATEGORİ 3: OTORİTE TEST EDEN ──────────────────────
    {
        "kategori": "⚔️ Yönetici Otoritesini Test Eden Çalışan",
        "metin": (
            "Kaan, 8 yıllık kıdemli yazılım geliştirici. Siz 6 ay önce müdür oldunuz. "
            "Kaan toplantılarda kararlarınızı sorguluyor: 'Biz bunu daha önce denedik, olmadı.' "
            "Ekip önünde sizi zor durumda bırakmaktan çekinmiyor. "
            "Son projede sizin kararınız olmadan farklı bir yöntem uyguladı. "
            "Teknik bilgisi gerçekten güçlü ama tutumu ekip dinamiğini bozuyor."
        ),
    },
    {
        "kategori": "⚔️ Yönetici Otoritesini Test Eden Çalışan",
        "metin": (
            "Ece, eski müdürünüzün en yakın çalışanıydı ve sizin yerinize terfi etmeyi bekliyordu. "
            "Artık her fırsatta eski müdürü referans gösteriyor: "
            "'[Eski müdür] böyle yapmazdı' ya da 'Biz eskiden farklı çalışıyorduk.' "
            "Ekipte bir kısım Ece'yi destekliyor gibi görünüyor. "
            "Kararlarınız uygulanıyor ama isteksizce ve geç."
        ),
    },
    {
        "kategori": "⚔️ Yönetici Otoritesini Test Eden Çalışan",
        "metin": (
            "Serkan, teknik lider pozisyonunda ve şirkette 10 yıldır çalışıyor. "
            "Son dönemde haftalık raporlarını geç teslim etmeye başladı ve "
            "bunu 'zaten kimse okumuyor ki' diyerek meşrulaştırıyor. "
            "Toplantılarda telefona bakıyor, sorulara tek kelimelik cevaplar veriyor. "
            "Diğer çalışanlar bu tutumu görünce benzer davranışlar sergilemeye başladı."
        ),
    },

    # ── KATEGORİ 4: DUYGUSAL VE KIRILGAN ───────────────────
    {
        "kategori": "😢 Duygusal ve Kırılgan Çalışan",
        "metin": (
            "Zeynep, detaylı ve özenli işler çıkaran bir içerik editörü. "
            "Ancak herhangi bir geri bildirimde gözleri doluyor ve motivasyonunu kaybediyor. "
            "Geçen hafta küçük bir düzeltme notunun ardından tuvalette ağladı. "
            "Ekip artık ona geri bildirim vermekten çekiniyor. "
            "Bu durum Zeynep'in gelişimini de engelliyor."
        ),
    },
    {
        "kategori": "😢 Duygusal ve Kırılgan Çalışan",
        "metin": (
            "Can, müşteri hizmetleri ekibinde çalışıyor ve zor müşterilerle her karşılaşmasından sonra "
            "derin bir motivasyon çöküşü yaşıyor. Bazen günün geri kalanında iş yapamıyor. "
            "Yöneticileri ona destek olmak istese de Can her seferinde "
            "'Kimse anlamıyor, bu iş benim için çok ağır' diyor. "
            "Performansı dalgalı, ekip üzerindeki etkisi ise giderek olumsuzlaşıyor."
        ),
    },
    {
        "kategori": "😢 Duygusal ve Kırılgan Çalışan",
        "metin": (
            "İrem, tasarım ekibinde 3 yıldır çalışıyor ve yaratıcı işlerde gerçekten başarılı. "
            "Ancak son 2 aydır her eleştiride savunmaya geçiyor ve bazen ağlamaya başlıyor. "
            "Bir müşteri toplantısında müşterinin sert geri bildirimi üzerine toplantıyı terk etti. "
            "Ekip arkadaşları artık onun önünde hiç yorum yapmıyor. "
            "İrem ise 'Bu şirket yaratıcılığı öldürüyor' diyor."
        ),
    },

    # ── KATEGORİ 5: ANALİTİK AMA İLETİŞİMİ ZOR ────────────
    {
        "kategori": "📊 Çok Analitik Ama İletişimi Zor Çalışan",
        "metin": (
            "Mert, veri analistiniz. Sunumlarında 40 sayfalık Excel dosyaları hazırlıyor "
            "ve her karar için 12 farklı senaryo modeli sunuyor. "
            "Yönetim kurulu toplantılarında herkes sıkılıyor çünkü Mert asla özet geçemiyor. "
            "Son toplantıda CEO 'Bu ne demek?' diye sordu ve Mert 30 dakika daha anlattı. "
            "Mert'e göre sorun dinleyicilerde: 'Veriye bakmadan karar veremem.'"
        ),
    },
    {
        "kategori": "📊 Çok Analitik Ama İletişimi Zor Çalışan",
        "metin": (
            "Leyla, finans departmanında çalışıyor ve raporları hatasız ama anlaşılmaz. "
            "Her basit soruya 15 dakikalık teknik bir açıklama yapıyor. "
            "Diğer departmanlar artık Leyla'yı toplantılara çağırmıyor çünkü "
            "'anlamaktan vazgeçtik' noktasına geldiler. "
            "Leyla ise 'İnsanlar finansı anlamak istemiyorlar' diye yakınıyor."
        ),
    },
    {
        "kategori": "📊 Çok Analitik Ama İletişimi Zor Çalışan",
        "metin": (
            "Onur, ürün geliştirme ekibinde kıdemli mühendis. Her özellik için "
            "kapsamlı teknik dokümanlar yazıyor ama bunları kimse okumuyor çünkü "
            "ortalama 50 sayfa ve teknik jargonla dolu. "
            "Sprint toplantılarında konuşmaya başlayınca herkes telefona bakıyor. "
            "Onur fark etmiyor ve 'Ben elimden geleni yapıyorum' diyor. "
            "Ekip onun fikirlerini ciddiye almaktan vazgeçmeye başladı."
        ),
    },
]

# ══════════════════════════════════════════════
# ANAHTAR KELİMELER (Puanlama için)
# ══════════════════════════════════════════════
EMPATI_KELIMELERI = [
    "anlıyorum", "hissediyorum", "değerli", "takdir", "saygı", "zor",
    "desteklemek", "birlikte", "dinlemek", "endişe", "önemli", "anlamak",
    "teşekkür", "güçlü", "farkındayım", "empati", "his", "duygu",
    "perspektif", "bakış açısı", "sen", "seninle", "sizi"
]
NETLIK_KELIMELERI = [
    "beklentim", "hedef", "açıkça", "net", "sonuç", "adım", "yapmalı",
    "yapmamalı", "kural", "politika", "karar", "öncelik", "tarih",
    "süre", "sorumluluk", "görev", "plan", "somut", "ölçülebilir"
]
OTORITE_KELIMELERI = [
    "sınır", "kabul edilemez", "değiştirmeli", "bekliyorum", "gerekli",
    "zorunlu", "uyarı", "sonuç", "standart", "norm", "müdahale",
    "düzeltme", "aksiyon", "tutarsız", "netleştirmek"
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
# GELİŞİM ÖNERİ MOTORU
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
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta her zor konuşmaya 'Seni duyuyorum' cümlesiyle başla. 5 konuşmada uygula."
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
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta 3 toplantıda karşı tarafın söylediklerini özetle ve onay al."
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
            "egzersiz": "🎯 Mini Egzersiz: Ekibindeki bir kişiyle bu hafta 'kariyer hedefleri' üzerine 15 dakikalık görüşme yap."
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
                "\"Bu konuşmadan çıkarken ikimizin de anlayacağı tek bir sonuç olsun.\"",
                "\"Senden Cuma gününe kadar şunu bekliyorum: [net hedef].\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta her toplantıyı 'Bu toplantıdan çıkan karar: ...' cümlesiyle bitir."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Netlik",
            "davranislar": [
                "Konuşma başında hedefi söyle: 'Bugün 10 dakikada şu konuyu netleştireceğiz.'",
                "Eylem fiilleri kullan: 'Düşünelim' yerine 'Karar verelim' de.",
                "Belirsiz kelimelerden kaçın: 'yakında', 'biraz' gibi ifadeleri sayıyla değiştir."
            ],
            "cumleler": [
                "\"Senden şunu bekliyorum: [X tarihinde], [Y çıktısı].\"",
                "\"Bu konuşmanın tek amacı şu kararı almak.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta 3 e-postanda 'yakında' yerine somut tarih yaz."
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
                "\"Beklentilerimi açık koyarım — bunu ilişkileri güçlendirmek için de kullanabilirim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Ekibinle 'iletişim kuralları' belgesi hazırla."
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
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta 2 durumda 'Hayır' veya 'Bu kabul edilemez' de — özür eklemeden."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Otorite & Sınır Koyma",
            "davranislar": [
                "Sakin ama kararlı bir ton kullan — yüksek ses gerekmez.",
                "Sınırlarını önceden belirle ve tutarlı ol.",
                "Kararlar sorgulandığında 'Bunu birebir konuşalım' de ve toplantıya devam et."
            ],
            "cumleler": [
                "\"Görüşünü duydum — karar bende ve şu an bu yönde ilerliyoruz.\"",
                "\"Farklı çalışma yöntemleri önce benimle paylaşılmalı.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta bir toplantıda sorgulandığında 'Bunu birebir konuşalım' de."
        },
        "guclu": {
            "baslik": "🟢 Güçlü Alan — Otorite & Sınır Koyma",
            "davranislar": [
                "Otoriteni empatiyle dengele — çalışanlar hem saygı hem güven hissetmeli.",
                "Sınır koyarken gerekçe sun — 'çünkü' kelimesini kullan.",
                "Gücünü ekibi geliştirmek için kullan, kontrol için değil."
            ],
            "cumleler": [
                "\"Sınırlarımı net koyarım — bunun arkasında her zaman ekibin iyiliği var.\"",
                "\"Otoriter değil, güvenilir bir lider olmak istiyorum.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta bir kararını 'çünkü...' diye başlayan bir gerekçeyle ekiple paylaş."
        }
    },
    "strateji": {
        "kritik": {
            "baslik": "🔴 Kritik Gelişim Alanı — Stratejik Yaklaşım",
            "davranislar": [
                "Her soruna 'Bunun altında ne var?' diye sor — kök nedeni bul.",
                "Sebep-sonuç bağla: 'Bu davranış devam ederse X olur' çerçevesini kullan.",
                "Konuşmayı uzun vadeli çerçevede kur: 'Gelecek 3 ayda nasıl görünmek istiyorsun?'"
            ],
            "cumleler": [
                "\"Bu durumu kısa vadede değil, kariyer gelişimin açısından ele alalım.\"",
                "\"Bu hafta çözmek istediğimiz problem şu — uzun vadeli hedefimiz ise şu.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta bir çalışanınla 3 aylık ortak bir hedef belirle."
        },
        "orta": {
            "baslik": "🟡 Orta Gelişim Alanı — Stratejik Yaklaşım",
            "davranislar": [
                "Konuşmayı mevcut soruna değil, gelişim fırsatına bağla.",
                "Takip mekanizması kur: 'Bunu 2 hafta sonra tekrar konuşalım' de.",
                "Birden fazla seçenek sun: 'İki yol var: biri X, diğeri Y.'"
            ],
            "cumleler": [
                "\"Bu konuşmayı 2 hafta sonra takip edeceğim.\"",
                "\"Sana iki seçenek sunuyorum — hangisi daha uygun birlikte karar verelim.\""
            ],
            "egzersiz": "🎯 Mini Egzersiz: Bu hafta her zor konuşmaya bir 'takip tarihi' belirle ve takvime ekle."
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
    k = senaryo["kategori"]
    if "Egolu" in k:
        return (
            "\"Performansına gerçekten değer veriyorum ve bu başarıyı takdir ediyorum. "
            "Aynı zamanda ekip içi iletişimimiz hakkında konuşmam gerekiyor. "
            "Arkadaşlarının fikirlerini toplantıda küçümsemenin kabul edilemez olduğunu açıkça söylemeliyim. "
            "Uzun vadeli başarı için teknik yetkinlik kadar ekip uyumu da kritik. "
            "Birlikte bu alanda nasıl ilerleyebiliriz, bunu konuşalım.\""
        )
    elif "Şikayet" in k:
        return (
            "\"Geri bildirimlerini paylaşmanı önemsiyorum. "
            "Hangi konular gerçekten acil ve çözülebilir, birlikte sıralayalım. "
            "Bununla birlikte, şikayetlerin yoğunluğunun ekip enerjisini nasıl etkilediğini "
            "fark etmeni istiyorum. Yapıcı bir çözüm ortağı olmak için birlikte nasıl çalışabiliriz?\""
        )
    elif "Otorite" in k:
        return (
            "\"Teknik deneyimin ekip için büyük bir değer. "
            "Aynı zamanda karar süreçlerinin nasıl işlediğini netleştirmem gerekiyor: "
            "Farklı görüşleri toplantılarda paylaşmak doğru, ancak kendi inisiyatifinle "
            "farklı yöntemler uygulamak kabul edilemez. Beklentimi net koyuyorum. "
            "Görüşlerini her zaman dinlemeye hazırım — doğru kanalda.\""
        )
    elif "Duygusal" in k:
        return (
            "\"Seninle açık bir konuşma yapmak istiyorum çünkü gelişimini önemsiyorum. "
            "Geri bildirim vermek, işin doğal bir parçası. Duygusal tepkilerin bazen seni "
            "ve ekibi zorladığını fark ediyorum. Bu konuda sana destek olmak istiyorum. "
            "Geri bildirimleri büyüme fırsatı olarak nasıl ele alabiliriz, bunu birlikte çalışabiliriz.\""
        )
    else:
        return (
            "\"Analizlerinin derinliği gerçekten etkileyici. "
            "Yönetim kademesinin ihtiyacını da seninle paylaşmam gerekiyor: "
            "Karar vericiler için 3-5 dakikalık özet sunumlar hazırlamana ihtiyacım var. "
            "Detaylar ekte olabilir ama ana mesajı net ve hızlı iletmek kritik. "
            "Bunu birlikte nasıl yapılandırabiliriz?\""
        )

# ══════════════════════════════════════════════
# PUANLAMA FONKSİYONU
# ══════════════════════════════════════════════
def puanla(cevap: str) -> dict:
    c = cevap.lower()
    n = len(cevap.split())

    e = sum(1 for k in EMPATI_KELIMELERI  if k in c)
    nl = sum(1 for k in NETLIK_KELIMELERI  if k in c)
    o = sum(1 for k in OTORITE_KELIMELERI  if k in c)
    s = sum(1 for k in STRATEJI_KELIMELERI if k in c)
    b = sum(1 for k in BELIRSIZ_IFADELER   if k in c)

    pe = min(25, e  * 5  + (3 if n > 30 else 0))
    pn = min(25, max(0, nl * 5 - b * 4 + (3 if n > 20 else 0)))
    po = min(25, o  * 6  + (3 if n > 25 else 0))
    ps = min(25, s  * 5  + (5 if n > 40 else 0))

    return {
        "empati": pe, "netlik": pn, "otorite": po, "strateji": ps,
        "toplam": pe + pn + po + ps, "kelime": n, "belirsiz": b,
    }

# ══════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════
def seviye(puan: int) -> str:
    if puan <= 10:   return "kritik"
    elif puan <= 18: return "orta"
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
    alanlar = {"empati": puan["empati"], "netlik": puan["netlik"],
               "otorite": puan["otorite"], "strateji": puan["strateji"]}
    en_dusuk = min(alanlar, key=alanlar.get)

    planlar = {
        "empati":   {"hedef": "Empati kurma becerisini güçlendir",
                     "aksiyon": "Her zor konuşmaya empati kuran bir cümleyle başla.",
                     "olcum": "5 konuşmada uygula ve sonuçları not et.",
                     "ipucu": "💡 'Seni duyuyorum / Seni anlıyorum' ile başla."},
        "netlik":   {"hedef": "Net ve somut iletişim kur",
                     "aksiyon": "Her toplantıyı net bir kapanış cümlesiyle bitir.",
                     "olcum": "5 toplantıda 'Bu toplantıdan çıkan karar: ...' uygula.",
                     "ipucu": "💡 'Yakında', 'biraz' yerine tarih ve sayı kullan."},
        "otorite":  {"hedef": "Sınırlarını kararlılıkla koy",
                     "aksiyon": "En az 2 durumda 'Hayır' veya 'Bu kabul edilemez' de.",
                     "olcum": "Özür dilemeden, sakin ama net söyle.",
                     "ipucu": "💡 Otorite yüksek ses değil, tutarlı bir tutum demektir."},
        "strateji": {"hedef": "Uzun vadeli çerçeve kur",
                     "aksiyon": "Her zor konuşmaya bir 'takip tarihi' belirle.",
                     "olcum": "3 görüşmede sebep-sonuç bağlantısı kur.",
                     "ipucu": "💡 'Bu durumun uzun vadede sana ne kazandıracağını konuşalım' ile başla."},
    }
    return {"alan": en_dusuk, "puan": alanlar[en_dusuk], **planlar[en_dusuk]}

# ══════════════════════════════════════════════
# GRAFİK FONKSİYONLARI
# ══════════════════════════════════════════════
def radar_chart(puan: dict):
    cats = ["Netlik", "Empati", "Otorite", "Strateji", "Netlik"]
    vals = [puan["netlik"], puan["empati"], puan["otorite"], puan["strateji"], puan["netlik"]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[25,25,25,25,25], theta=cats, fill="toself",
        fillcolor="rgba(200,200,200,0.12)", line=dict(color="rgba(180,180,180,0.4)"),
        showlegend=False
    ))
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor="rgba(99,110,250,0.25)",
        line=dict(color="rgba(99,110,250,0.9)", width=2.5),
        marker=dict(size=9, color="rgba(99,110,250,1)"),
        showlegend=False
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,25], tickfont=dict(size=10)),
                   angularaxis=dict(tickfont=dict(size=14))),
        showlegend=False, margin=dict(t=30,b=30,l=40,r=40),
        height=360, paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def trend_chart(gecmis: list):
    if len(gecmis) < 2:
        return None
    idx = list(range(1, len(gecmis)+1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=idx, y=[g["toplam"]//4 for g in gecmis],
        name="Ort. Toplam", line=dict(color="#636EFA", width=3), mode="lines+markers", marker=dict(size=8)))
    for key, color, name in [("empati","#EF553B","Empati"), ("netlik","#00CC96","Netlik"),
                               ("otorite","#AB63FA","Otorite"), ("strateji","#FFA15A","Strateji")]:
        fig.add_trace(go.Scatter(x=idx, y=[g[key] for g in gecmis], name=name,
            line=dict(color=color, width=1.5, dash="dot"), mode="lines+markers"))
    fig.update_layout(
        yaxis=dict(range=[0,25], title="Puan (0-25)"),
        xaxis=dict(title="Deneme #", tickvals=idx),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=300, margin=dict(t=50,b=40,l=40,r=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# ══════════════════════════════════════════════
# ANA UYGULAMA
# ══════════════════════════════════════════════
def main():
    st.set_page_config(page_title="Zor Çalışan Simülatörü", page_icon="💼", layout="wide")

    for key, default in [("senaryo", None), ("degerlendirme", None), ("gecmis_skorlar", [])]:
        if key not in st.session_state:
            st.session_state[key] = default

    tab1, tab2 = st.tabs(["🎮 Simülatör", "📊 Gelişim Dashboard"])

    # ══════════════════════════════════════════
    # SEKME 1 — SİMÜLATÖR
    # ══════════════════════════════════════════
    with tab1:
        st.title("💼 Zor Çalışan Simülatörü")
        st.markdown("_15 farklı senaryo ile liderlik becerilerini test et ve geliştir._")
        st.divider()

        col1, col2 = st.columns([2,1])
        with col1:
            if st.button("🎲 Senaryoyu Başlat", use_container_width=True, type="primary"):
                st.session_state.senaryo = random.choice(SENARYOLAR)
                st.session_state.degerlendirme = None
        with col2:
            if st.session_state.senaryo:
                if st.button("🔄 Yeni Senaryo", use_container_width=True):
                    st.session_state.senaryo = random.choice(SENARYOLAR)
                    st.session_state.degerlendirme = None

        if st.session_state.senaryo:
            senaryo = st.session_state.senaryo
            st.subheader(f"📋 {senaryo['kategori']}")
            st.info(senaryo["metin"])
            st.divider()

            st.subheader("💬 Bu durumda çalışana ne söylersiniz?")
            cevap = st.text_area(
                "Yanıtınızı buraya yazın...", height=160,
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
                    st.session_state.gecmis_skorlar.append(
                        {k: puan[k] for k in ["zaman","toplam","empati","netlik","otorite","strateji","senaryo"]}
                    )

            if st.session_state.degerlendirme:
                d = st.session_state.degerlendirme
                st.divider()
                st.subheader("🎯 Değerlendirme Sonuçları")

                c1,c2,c3,c4 = st.columns(4)
                c1.metric("💬 Netlik",   f"{d['netlik']}/25")
                c2.metric("⚡ Otorite",  f"{d['otorite']}/25")
                c3.metric("❤️ Empati",   f"{d['empati']}/25")
                c4.metric("🧠 Strateji", f"{d['strateji']}/25")

                st.divider()
                toplam = d["toplam"]
                profil, aciklama, stil = liderlik_profili(toplam)
                st.markdown(f"### Toplam Skor: **{toplam}/100**")
                st.progress(toplam / 100)
                getattr(st, stil)(f"**{profil}** — {aciklama}")

                st.divider()
                st.subheader("📈 Alan Bazlı Gelişim Önerileri")

                for alan_key, alan_adi, alan_puani in [
                    ("empati","❤️ Empati",d["empati"]),
                    ("netlik","💬 Netlik",d["netlik"]),
                    ("otorite","⚡ Otorite",d["otorite"]),
                    ("strateji","🧠 Strateji",d["strateji"])
                ]:
                    sev   = seviye(alan_puani)
                    oneri = GELISIM_ONERILERI[alan_key][sev]
                    with st.expander(f"{oneri['baslik']} — {alan_puani}/25", expanded=(sev=="kritik")):
                        st.markdown("**🎯 Somut Davranış Önerileri:**")
                        for i, dav in enumerate(oneri["davranislar"],1):
                            st.markdown(f"{i}. {dav}")
                        st.markdown("**💬 Pratik Cümle Örnekleri:**")
                        for cumle in oneri["cumleler"]:
                            st.markdown(f"- {cumle}")
                        st.info(oneri["egzersiz"])

                st.divider()
                plan = d["plan"]
                alan_label = {"empati":"❤️ Empati","netlik":"💬 Netlik","otorite":"⚡ Otorite","strateji":"🧠 Strateji"}
                st.subheader("📅 Bu Hafta Liderlik Aksiyon Planın")
                st.markdown(f"**Öncelikli alan:** {alan_label[plan['alan']]} ({plan['puan']}/25)")
                colA, colB = st.columns(2)
                with colA:
                    st.markdown(f"**🎯 Haftalık Hedef:**  \n{plan['hedef']}")
                    st.markdown(f"**✅ Aksiyon:**  \n{plan['aksiyon']}")
                with colB:
                    st.markdown(f"**📏 Ölçüm:**  \n{plan['olcum']}")
                    st.info(plan["ipucu"])

                st.divider()
                st.subheader("💡 Örnek Model Yanıt")
                st.success(d["ornek"])
                st.caption("💡 Yanıtınızı düzenleyip tekrar değerlendirebilirsiniz.")

        else:
            st.markdown("""
            ### Nasıl Çalışır?
            1. **"Senaryoyu Başlat"** butonuna bas — 15 farklı senaryo arasından biri gelir
            2. Yönetici olarak yanıtını yaz
            3. **"Cevabı Değerlendir"** ile liderlik skorunu gör
            4. Alan bazlı gelişim önerileri ve haftalık planını incele
            5. **Gelişim Dashboard** sekmesinden ilerlemeni takip et
            """)

    # ══════════════════════════════════════════
    # SEKME 2 — DASHBOARD
    # ══════════════════════════════════════════
    with tab2:
        st.title("📊 Liderlik Gelişim Dashboard")

        if not st.session_state.degerlendirme:
            st.info("ℹ️ Henüz değerlendirme yapılmadı. 🎮 Simülatör sekmesinden başlayın!")
            return

        d = st.session_state.degerlendirme
        toplam = d["toplam"]
        profil, aciklama, stil = liderlik_profili(toplam)

        m1,m2,m3,m4,m5 = st.columns(5)
        m1.metric("🏆 Toplam",   f"{toplam}/100")
        m2.metric("💬 Netlik",   f"{d['netlik']}/25")
        m3.metric("❤️ Empati",   f"{d['empati']}/25")
        m4.metric("⚡ Otorite",  f"{d['otorite']}/25")
        m5.metric("🧠 Strateji", f"{d['strateji']}/25")
        getattr(st, stil)(f"**{profil}** — {aciklama}")

        st.divider()
        col_r, col_a = st.columns([1,1])

        with col_r:
            st.subheader("🕸️ Liderlik Profil Haritası")
            st.plotly_chart(radar_chart(d), use_container_width=True)

        with col_a:
            st.subheader("🔍 Alan Analizi")
            alanlar_sirali = sorted([
                ("❤️ Empati",d["empati"]),("💬 Netlik",d["netlik"]),
                ("⚡ Otorite",d["otorite"]),("🧠 Strateji",d["strateji"])
            ], key=lambda x: x[1])
            for alan_adi, puan_val in alanlar_sirali:
                sev    = seviye(puan_val)
                renk   = {"kritik":"🔴","orta":"🟡","guclu":"🟢"}[sev]
                etiket = {"kritik":"Kritik","orta":"Gelişiyor","guclu":"Güçlü"}[sev]
                st.markdown(f"{renk} **{alan_adi}** — {puan_val}/25  *({etiket})*")
                st.progress(puan_val / 25)
            plan = d["plan"]
            alan_label = {"empati":"❤️ Empati","netlik":"💬 Netlik","otorite":"⚡ Otorite","strateji":"🧠 Strateji"}
            st.divider()
            st.markdown(f"**🎯 Öncelikli Alan:** {alan_label[plan['alan']]}")
            st.markdown(f"*{plan['aksiyon']}*")

        st.divider()
        st.subheader("📈 Gelişim Trendi")
        gecmis = st.session_state.gecmis_skorlar
        if len(gecmis) >= 2:
            fig = trend_chart(gecmis)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"📊 Trend grafiği için {2 - len(gecmis)} değerlendirme daha yap!")

        if gecmis:
            st.divider()
            st.subheader("📋 Tüm Değerlendirmeler")
            for i, g in enumerate(reversed(gecmis), 1):
                no = len(gecmis) - i + 1
                with st.expander(f"#{no} — {g['zaman']} | {g['toplam']}/100 | {g['senaryo']}"):
                    c1,c2,c3,c4 = st.columns(4)
                    c1.metric("Netlik",  g["netlik"])
                    c2.metric("Empati",  g["empati"])
                    c3.metric("Otorite", g["otorite"])
                    c4.metric("Strateji",g["strateji"])
            st.divider()
            if st.button("🗑️ Geçmişi Temizle", type="secondary"):
                st.session_state.gecmis_skorlar = []
                st.session_state.degerlendirme  = None
                st.rerun()


if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────
# ÇALIŞTIRMA KOMUTLARI:
# pip install streamlit plotly
# streamlit run app.py
# ─────────────────────────────────────────────
