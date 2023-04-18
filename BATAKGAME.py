import random
import pandas as pd

A = [ '♠', '♣', '♥', '♦' ]
B = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

deste = []
for i in A:
    for j in B:
        deste.append(i + j)

oyuncular = {}
oyuncu_sira = []
oyuncu_el_sayisi = []
oyuncu_bahis = {}
kart_tipi = ''

print("OYUNCULARIN İSİMLERİNİ GİRİN")
for i in range(4):
    oyuncular.setdefault(input("Oyuncu " + str(i + 1) + ": "), {}.fromkeys(A))

tur_sayisi = int(input("Kaç tur oynayacağınızı giriniz : "))
for tur in range(tur_sayisi):

    for oyuncu in oyuncular:
        oyuncu_sira.append(oyuncu)
        for i in A:
            oyuncular[oyuncu][i] = []
        for i in range(13):
            kart = random.choice(deste)
            oyuncular[oyuncu][kart[0]].append(kart[1:])
            deste.remove(kart)

    print("\nDAĞITILAN KARTLAR:")
    for oyuncu in oyuncular:
        print(oyuncu + ":")
        for karttip in oyuncular[oyuncu]:
            oyuncular[oyuncu][karttip].sort(key=B.index)  # kartlar B listesindeki sıraya göre dizilir
            print(karttip, oyuncular[oyuncu][karttip])

    for name in oyuncular.keys():
        oyuncu_bahis[name] = int(input(f"{name}, kaç el kazanacağını tahmin ediyorsun: "))


    print("\nOYUN BAŞLADI...")  # Oyun seçilen tur sayısı kadar her turda 13 el oynanacak şekildedir.

    print("\n" , tur,".Tur\n")

    oyun_skor = dict()
    macaAtildi = False
    sira = random.randrange(4)  # oyuna başlayacak oyuncu rastgele belirleniyor
    for el in range(13):
        print(str(el + 1) + ". el:")
        oynayan = 0
        oynanan_kartlar = []  # bu liste içine kimin hangi kartı attığı yazılacak
        while oynayan < 4:
            oyuncu = oyuncu_sira[sira]
            if oynayan == 0:  # ilk kart atacak oyuncu ise kart tipi belirlenecek (rastgele)
                while True:
                    if macaAtildi:  # Maça önceki bir elde koz olarak kullanıldı ise oyuncu Maça ile başlayabilir
                        kart_tipi = random.choice(A)
                    else:  # Maça önceki bir elde koz olarak kullanılmadı ise diğer üç kart tipinden atabilir
                        kart_tipi = random.choice(A[1:])
                    if len(oyuncular[oyuncu_sira[sira]][kart_tipi]):  # o tipte kartı yoksa döngü devam edecek
                        break
                oyuncu_kart = (
                    oyuncu, kart_tipi, oyuncular[oyuncu][kart_tipi].pop())  # o tipteki en büyük kartı atıyor !!!!

            else:  # diğer oyuncular ilk oyuncunun belirlediği kart tipinde kart atacak
                if len(oyuncular[oyuncu][kart_tipi]):  # o kart tipinde kartı varsa en büyük olanı atacak
                    oyuncu_kart = (oyuncu, kart_tipi, oyuncular[oyuncu][kart_tipi].pop())
                elif len(oyuncular[oyuncu]['♠']):  # o kart tipinde kartı yoksa en küçük maça kartını atacak
                    oyuncu_kart = (oyuncu, '♠', oyuncular[oyuncu]['♠'].pop(0))
                    macaAtildi = True  # Maça koz olarak oynandığı için sonraki ellerde doğrudan Maça atılabilecek
                else:  # maça kartı da yoksa, diğer 2 tipin hangisinde daha çok kart varsa en küçük kartı atacak
                    kart_tipleri = A[1:].copy()  # maça hariç diğer 3 kart tipi kopyalandı
                    if kart_tipi != '♠':  # oynanan kart tipi maça değilse
                        kart_tipleri.remove(kart_tipi)  # oynanan kart tipi de oyuncuda olmadığı için silindi
                    if len(oyuncular[oyuncu][kart_tipleri[0]]) > len(oyuncular[oyuncu][kart_tipleri[1]]):
                        oyuncu_kart = (oyuncu, kart_tipleri[0], oyuncular[oyuncu][kart_tipleri[0]].pop(0))
                    else:
                        oyuncu_kart = (oyuncu, kart_tipleri[1], oyuncular[oyuncu][kart_tipleri[1]].pop(0))
            print(oyuncu_kart[0], oyuncu_kart[1] + oyuncu_kart[2])
            oynanan_kartlar.append(oyuncu_kart)
            oynayan += 1
            sira += 1
            if sira >= 4:
                sira -= 4

        # atılan 4 karta göre eli kazananı bulma:
        en_buyuk = oynanan_kartlar[0]  # ilk atılanı en büyük kart kabul ettim
        for kart in oynanan_kartlar[1:]:
            if kart[1] == en_buyuk[1] and B.index(kart[2]) > B.index(en_buyuk[2]):
                en_buyuk = kart  # en büyük ile aynı kart tipinde daha büyük atıldı ise en büyük kart kabul et
            elif en_buyuk[1] != '♠' and kart[1] == '♠':
                en_buyuk = kart  # en büyük maça değilken maça atıldı ise en büyük kart kabul et
        print("eli kazanan:", en_buyuk[0])
        sira = oyuncu_sira.index(en_buyuk[0])
        oyun_skor[en_buyuk[0]] = oyun_skor.setdefault(en_buyuk[0], 0) + 1

        for i in range(4):
            bahis = oyuncu_bahis.values()
            bahis_list = list(bahis)
            fark = oyun_skor[en_buyuk[0]] - bahis_list[0]
            if fark == 0:
                oyun_skor[en_buyuk[0]] *= 10
            elif fark > 0:
                oyun_skor[en_buyuk[0]] = oyun_skor[en_buyuk[0]] * 10 + fark*2
            else:
                oyun_skor[en_buyuk[0]] -= oyun_skor[en_buyuk[0]] * 10

    print("SKOR:", oyun_skor)

    data_frame = pd.DataFrame(list(oyun_skor.items()), columns=["İsim", "Puan"])

    data_frame = data_frame.sort_values(by=["Puan"], ascending=False)

    print(data_frame)