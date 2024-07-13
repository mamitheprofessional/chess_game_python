import pygame
import os

pygame.init()

genislik = 800
yukseklik = 800
pencere = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("MamiTheProfessional")

dosya_yolu = os.path.dirname(__file__)

png_dosya_yolu = os.path.join(dosya_yolu, 'pngler')

arkaplan = pygame.image.load(os.path.join(png_dosya_yolu, 'board2.png'))
arkaplan = pygame.transform.scale(arkaplan, (800, 800))

resimler = {
    'b_kale': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 'b_kale.png')), (100, 100)),
    'b_at': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 'b_at.png')), (100, 100)),
    'b_fil': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 'b_fil.png')), (100, 100)),
    'b_vezir': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 'b_vezir.png')), (100, 100)),
    'b_sah': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 'b_sah.png')), (100, 100)),
    'b_piyon': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 'b_piyon.png')), (100, 100)),
    's_kale': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 's_kale.png')), (100, 100)),
    's_at': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 's_at.png')), (100, 100)),
    's_fil': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 's_fil.png')), (100, 100)),
    's_vezir': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 's_vezir.png')), (100, 100)),
    's_sah': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 's_sah.png')), (100, 100)),
    's_piyon': pygame.transform.scale(pygame.image.load(os.path.join(png_dosya_yolu, 's_piyon.png')), (100, 100)),
}


secili_tas = None


tahta = [ # 2 boyutlu dinamik listemiz
    ['b_kale', 'b_at', 'b_fil', 'b_vezir', 'b_sah', 'b_fil', 'b_at', 'b_kale'               ],
    ['b_piyon', 'b_piyon', 'b_piyon', 'b_piyon', 'b_piyon', 'b_piyon', 'b_piyon', 'b_piyon' ],
    ['--', '--', '--', '--', '--', '--', '--', '--'                                         ],
    ['--', '--', '--', '--', '--', '--', '--', '--'                                         ],
    ['--', '--', '--', '--', '--', '--', '--', '--'                                         ],
    ['--', '--', '--', '--', '--', '--', '--', '--'                                         ],
    ['s_piyon', 's_piyon', 's_piyon', 's_piyon', 's_piyon', 's_piyon', 's_piyon', 's_piyon' ],
    ['s_kale', 's_at', 's_fil', 's_vezir', 's_sah', 's_fil', 's_at', 's_kale'               ]
]


def tas_rengi(tas): # taşın türünü belirleyeceğiz ana döngüdeki tas değişkeni tıklanan seçili taşın koordinatlarını alıyor buradan rengine bakıyor
    if tas.startswith("b_"): #beyazla taşlar
        return "b"
    elif tas.startswith("s_"): #siyah taşlar
        return "s"
    else:
        return None
    
    



def tahta_konumlar(pencere, tahta):
    pencere.blit(arkaplan, (0, 0))
    for i in range(len(tahta)):
        for j in range(len(tahta[i])):
            if tahta[i][j] != '--':
                pencere.blit(resimler[tahta[i][j]], (j * 100, i * 100)) # taşın konumu her seferinde yeniden ayarlanacak
    if secili_tas is not None:
        pygame.draw.rect(pencere, (0, 255, 0), (secili_tas[1] * 100, secili_tas[0] * 100, 100, 100), 3)  # seçili kare belirgin olsun diye yeşil bir çerçeve çiziyoruz





def piyon_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    if tas == 'b_piyon':  
        if secilen_y == 1: # beyaz piyon başlangıç konumu
            if (hedef_y - secilen_y == 1) and (secilen_x - hedef_x == 0): # başlangıçta sadece y ekseninde 1 x te 0 adım atabilir
                return True    
            elif (hedef_y - secilen_y == 2) and (secilen_x - hedef_x == 0) and tahta[hedef_y][hedef_x] == '--': # veya y2 x0 atabilir
                return True
            elif (hedef_y - secilen_y == 1) and (abs(secilen_x - hedef_x) == 1) and tahta[hedef_y][hedef_x] != '--': #veya çaprazda düşman taş varsa y1 x1 atabilir
                return True
        else: # başlangıç konumda değilse sadece 1 adım atar ve yine sadece çapraz yiyebilir
            if (hedef_y - secilen_y == 1) and (secilen_x - hedef_x == 0) and tahta[hedef_y][hedef_x] == '--': 
                return True
            elif (hedef_y - secilen_y == 1) and (abs(secilen_x - hedef_x) == 1) and tahta[hedef_y][hedef_x] != '--':
                return True
    elif tas == 's_piyon':  # siyahlarda benzer şekilde y=6 noktasından başlar
        if secilen_y == 6:
            if (secilen_y - hedef_y == 1) and (secilen_x - hedef_x == 0):
                return True    
            elif (secilen_y - hedef_y == 2) and (secilen_x - hedef_x == 0) and tahta[hedef_y][hedef_x] == '--':
                return True
            elif (secilen_y - hedef_y == 1) and (abs(secilen_x - hedef_x) == 1) and tahta[hedef_y][hedef_x] != '--':
                return True
        else:
            if (secilen_y - hedef_y == 1) and (secilen_x - hedef_x == 0) and tahta[hedef_y][hedef_x] == '--':
                return True
            elif (secilen_y - hedef_y == 1) and (abs(secilen_x - hedef_x) == 1) and tahta[hedef_y][hedef_x] != '--':
                return True
        if tahta[7][hedef_x] or tahta[0][hedef_x]:
            for y in range(len(tahta)):
                for x in range(len(tahta[y])):
                    tas = tahta[y][x]
                    if tas == 'b_piyon' and y == 7:
                        tahta[y][x] = 'b_vezir'
                    elif tas == 's_piyon' and y == 0:
                        tahta[y][x] = 's_vezir'
    return False






def at_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    if tas == 'b_at' or tas == 's_at':
        # ya 2y ve 1x                               yada                     2x ve 1y hareket edecek
        if (abs(hedef_y - secilen_y) == 2 and abs(hedef_x - secilen_x) == 1) or (abs(hedef_y - secilen_y) == 1 and abs(hedef_x - secilen_x) == 2): 
            if tahta[hedef_y][hedef_x] == '--' or tas_rengi(tahta[hedef_y][hedef_x]) != tas_rengi(tas):
                return True
    return False

def kale_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    if tas == "b_kale" or tas == "s_kale":
        if secilen_x == hedef_x or secilen_y == hedef_y: #mesela x=0 da 0,2 den 0,4 e gidecekse seçilen_x ile hedef_x değeri 0 olur böylece kale sadece y ekseninde hareket eder

            if secilen_x == hedef_x: # kale y koordinatlarında hareket ederken önünde kendi renginde taş varsa hareket edemesin diye ekledim

                #aşağıdaki for döngüsünde y ekseninde harekete bakarken eğer aşağıdan yukarıya gidilecekse min = seçilen olur max = hedef olur
                #yukarıdan aşağı gidileceksede min = hedef olur max = seçilen olur böylece aradaki tüm taşları hem siyah hem beyaz için sayaca sokabiliriz
                for i in range(min(secilen_y, hedef_y) + 1, max(secilen_y, hedef_y)):
                    if tahta[i][secilen_x] != '--': # aynı sabit x koordinatında tüm y koordinatlarını tara eğer boş kare yoksa false dön
                        return False
                    
            elif secilen_y == hedef_y: # yukarıdakiler gibi
                for j in range(min(secilen_x, hedef_x) + 1, max(secilen_x, hedef_x)):
                    if tahta[secilen_y][j] != '--':
                        return False
            # hedef boş ise veya farklı renkte düşman taş varsa kale onu yiyebilir
            if tahta[hedef_y][hedef_x] == '--' or tas_rengi(tahta[hedef_y][hedef_x]) != tas_rengi(tas):
                return True
    return False 


def fil_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    if tas == 'b_fil' or tas == 's_fil':
        if abs(hedef_y - secilen_y) == abs(hedef_x - secilen_x):  # y de gittiği kadar x tede giderse çapraz hareket olur
            # y ekseni için
            temp_y = 1 if hedef_y > secilen_y else -1 #mesela yukarıdaki fil aşağıya gidecekse hedef_y>başlangıç_y olur =1 değeri atanır
                                                      #aşağıdan yukarı çıkacaksada tam tersi koşul sağlanır -1 değeri atanır
            # x ekseni için
            temp_x = 1 if hedef_x > secilen_x else -1 #benzer durum geçerli
#mesela bir senaryo yazalım fil 2,0 konumundan 5,3 konumuna gelmek istesin
#temp_y ve temp_x işlemlerinden gerekli değerlerini alacak hedef_y(3)>seçilen_y(0) ---> temp_y=1 değeri aldı 
#hedef_x(5)>secilen_x(2) ---> temp_x = 1 değerini aldı
#y = secilen_y + temp_y  --> y = 0 + 1 = 1       x = secilen_x + temp_x --> x = 2 + 1 = 3 değerlerini alır

            y = secilen_y + temp_y
            x = secilen_x + temp_x

            while y != hedef_y and x != hedef_x: #y ve x değerleri eşitleninceye kadar aşağıdaki işlemleri yapıcaz
                if tahta[y][x] != '--': # döngüdeki her hareketi inceliyor filin hedef konumunda önünde taş varsa false dönecek
                    return False
                y += temp_y
                x += temp_x
# ilk döngüde y(1) ve x(3) tahta[1][3] kontrol ediliyor boş ise true olmuş gibi döngüden çıkılmıyor ve x,y değerleri birer arttırılıyor
# ikinci döngüde y(2) ve x(4) yine boş ise true ve y(3) x(5) oluyor böylece x,y değerleri hedeflerle eşitleniyor ve döngüden çıkılıyor

#aşağıdaki if kısmı denetleniyor sorun yoksa fil hareket etmek için main kodlarına dönüyor

            #hedef konumda taş yoksa veya rakip renkte bir taş varsa fil o konuma ulaşur
            if tahta[hedef_y][hedef_x] == '--' or tas_rengi(tahta[hedef_y][hedef_x]) != tas_rengi(tas): 
                return True
    return False


def vezir_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    # kale hareketi fonksiyonunun aynısını ekledim
    if secilen_x == hedef_x or secilen_y == hedef_y:
        if secilen_x == hedef_x:
            for i in range(min(secilen_y, hedef_y) + 1, max(secilen_y, hedef_y)):
                if tahta[i][secilen_x] != '--':
                    return False
        elif secilen_y == hedef_y:
            for j in range(min(secilen_x, hedef_x) + 1, max(secilen_x, hedef_x)):
                if tahta[secilen_y][j] != '--':
                    return False
        if tahta[hedef_y][hedef_x] == '--' or tas_rengi(tahta[hedef_y][hedef_x]) != tas_rengi(tas):
            return True
        
    # fil hareketi fonksiyonunun aynısını ekledim
    if abs(hedef_y - secilen_y) == abs(hedef_x - secilen_x):
        temp_y = 1 if hedef_y > secilen_y else -1
        temp_x = 1 if hedef_x > secilen_x else -1
        y = secilen_y + temp_y
        x = secilen_x + temp_x
        while y != hedef_y and x != hedef_x:
            if tahta[y][x] != '--':
                return False
            y += temp_y
            x += temp_x
        if tahta[hedef_y][hedef_x] == '--' or tas_rengi(tahta[hedef_y][hedef_x]) != tas_rengi(tas):
            return True

    return False



def sah_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    if tas == "s_sah" or tas == "b_sah":
        # piyondan gibi hareketten farkı <= 1 kullanmam çünkü mesela düz ileri hareket ederse x değeri 0 olur y değeri 1 olur
        # yan hareket edersem busefer y değeri 0 olur     çapraz hareket edersemde x1 y1 olur ve koşul sağlanır
        if abs(hedef_y - secilen_y) <= 1 and abs(hedef_x - secilen_x) <= 1:
            if tahta[hedef_y][hedef_x] == '--' or tas_rengi(tahta[hedef_y][hedef_x]) != tas_rengi(tas):
                if not sah_tehdit_kontrol(tas, hedef_y, hedef_x, tahta): #eğerki tehdit altında değilse hareket etmesine izin ver
                    return True
        return False




def sah_tehdit_kontrol(tas, y, x, tahta):
    sah_rengi = tas_rengi(tas) #şahı seçiyoruz
#    print(f"şah: {tas}, renk: {sah_rengi}")  # kontrol
    # kabaca tüm taşları tarıyor zıt rengi görünce tehdit durumu algılıyor
    for i in range(len(tahta)): 
        for j in range(len(tahta[i])):
            if tahta[i][j] != '--' and tas_rengi(tahta[i][j]) != sah_rengi:
                if tas_hareketi(i, j, y, x, tahta): # bilgileri fonksiyona yollayıp düşman taşın hedefi benim şahın gideceği yere return edebiliyormu diye kontrollüyor
                    return True # ediyorsa sıkıntı
#                print(f"taş: {tahta[i][j]}, renk: {tas_rengi(tahta[i][j])}") # döngüyü daha iyi görmek için

#                print(f"şah rengi: {sah_rengi}")
    return False



def sahmat_kontrol(sah_rengi, tahta):
    sah_y, sah_x = None, None #başlangıç için none değer atadık

    for y in range(len(tahta)): #satır
        for x in range(len(tahta[y])): #sütun
            if (sah_rengi + "_sah") in tahta[y][x]: #tahtada şahı görürsen
                sah_y, sah_x = y, x #koordinatları tut
                break #iç döngüyü kır
        if sah_y is not None: #dış döngüyü kır
            break

    if sah_tehdit_kontrol(tahta[sah_y][sah_x], sah_y, sah_x, tahta) == False: 
        return False  # eğer şah mevcut konumunda tehdit altında değilse false döner

    # Şahın etrafındaki tüm kareleri kontrol et
    for delta_y in [-1, 0, 1]:
        for delta_x in [-1, 0, 1]:
            if delta_y == 0 and delta_x == 0:
                continue  # şahın başlangıç değerini 0,0 kabul ediyoruz yani delta_y ve delta_x 0,0 olursa bu iterasyonu atla
            yeni_y = sah_y + delta_y # örnek sah_y , sah_x 0,4 olsun delta_y delta_x -1,0 olsun yeni_y yeni_x -1,4 olur
            yeni_x = sah_x + delta_x
            #aşağıda tahtanın sınırları içindemi diye kontrol ediyoruz eğerki senaryo yeni_y,yeni_x=-1,4 olursa ilk koşul 0<-1<8(yanlış) olup tahtanın dışında olduğu anlaşılır
            if 0 <= yeni_y < 8 and 0 <= yeni_x < 8:
                #eğerki şahın gidebileceği bir alan varsa yani boş kare veya yiyebileceği düşman taş varsa
                if tahta[yeni_y][yeni_x] == '--' or tas_rengi(tahta[yeni_y][yeni_x]) != sah_rengi:
                    # şahı geçici olarak o bölgeye taşır
                    temp = tahta[yeni_y][yeni_x]
                    tahta[yeni_y][yeni_x] = tahta[sah_y][sah_x]
                    tahta[sah_y][sah_x] = '--'
                    
                    # sonra taşıdığı bölgede sah_Tehdit_kontrol fonksiyonuna bakar buraya taşınabilirmi diye eğer orası false dönerse demekki şahın belirtilern koordinata gitmesinde sorun yok 
                    if sah_tehdit_kontrol(tahta[yeni_y][yeni_x], yeni_y, yeni_x, tahta) == False: 
                        tahta[sah_y][sah_x] = tahta[yeni_y][yeni_x] # şahı eski konuma taşıyoruz
                        tahta[yeni_y][yeni_x] = temp
                        return False  # şah yeni konumunda tehdit altında değilse false döner
                    #yani önce şahın mevcut konumunu kontrol ettik sonra şahı geçici olarak çevresindeki karelere koyup oralarda tehdit varmı test edip tekrar eski konumuna koyduk
                    
                    # her halükarda tahtayı eski haline getir
                    tahta[sah_y][sah_x] = tahta[yeni_y][yeni_x]
                    tahta[yeni_y][yeni_x] = temp

    return True #şah hareket edemez vede tehdit altındaysa true dönüp ana fonksiyonda döngüyü sonlandıracak







def rok_hamlesi(secilen_y, secilen_x, hedef_x, tahta):
    tas = tahta[secilen_y][secilen_x] # şahı seçince koordinatlar taşa aktarılacak (işlemler ana döngüde)
    
    if tas == 'b_sah':
        baslangic_x, baslangic_y = 4, 0 
        kisa_rok_kale_x, uzun_rok_kale_x = 7, 0
    elif tas == 's_sah':
        baslangic_x, baslangic_y = 4, 7
        kisa_rok_kale_x, uzun_rok_kale_x = 7, 0
    else:
        return False  # seçilen taş şah değilse false dön diğerleriyle işimiz yok

    # burası ileride değişecek çünkü şah yer değiştirip eski konumuna gelirse rok yapabiliyor
    sah_baslangic_konumunda = (secilen_x == baslangic_x and secilen_y == baslangic_y)
    if not sah_baslangic_konumunda:
        return False


    # kısa rok için
    if hedef_x == baslangic_x + 2: #şah başlangıç konumundan 2 birim sağa kaydırmayı hedeflersek
        kale_x = kisa_rok_kale_x # başlangıç koordinatı
        ara_x = [5, 6] # aşağıda döngüsü var 5 ve 6 boş olmalı
    # uzun rok için
    elif hedef_x == baslangic_x - 3:
        kale_x = uzun_rok_kale_x
        ara_x = [1, 2, 3]
    else:
        return False  # hedef geçersiz ise

    # Kale kontrolü
    kale = 'b_kale' if tas[0] == 'b' else 's_kale'
    if tahta[secilen_y][kale_x] != kale:
        return False  # kale oynatılmışsa false

    # Aradaki karelerin boş olması gerekir
    for x in ara_x:
        if tahta[secilen_y][x] != '--':
            return False



    # herşey hazırsa artık roku bu aşağıdaki kodlar yapacak bunlar tahtanın son hali
    if hedef_x > secilen_x:  # sağ taraf kısa rok için
        tahta[secilen_y][6] = tas # şah
        tahta[secilen_y][5] = kale
        tahta[secilen_y][4] = '--'
        tahta[secilen_y][7] = '--'
    else: # uzun rok kısmı
        tahta[secilen_y][1] = tas  # Şah 1. sütuna gidiyor
        tahta[secilen_y][2] = kale  # Kale 2. sütuna gidiyor
        tahta[secilen_y][4] = '--'
        tahta[secilen_y][0] = '--'

    print("çalışıyor------------------")
    return True



def tas_hareketi(secilen_y, secilen_x, hedef_y, hedef_x, tahta):
    tas = tahta[secilen_y][secilen_x]

    if (tas == 'b_sah' or tas == 's_sah') and (abs(hedef_x - secilen_x) == 2 or abs(hedef_x - secilen_x) == 3): #rok isteniyorsa şahı x ekseninde 2 yada 3 kare oynat
        return rok_hamlesi(secilen_y, secilen_x, hedef_x, tahta)



    if tas == "b_piyon":
        return piyon_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "s_piyon":
        return piyon_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "b_at":
        return at_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "b_fil":
        return fil_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "b_kale":
        return kale_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "b_vezir":
        return vezir_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "b_sah":
        return sah_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "s_at":
        return at_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "s_fil":
        return fil_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "s_kale":
        return kale_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "s_vezir":
        return vezir_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    elif tas == "s_sah":
        return sah_hareketi(tas, secilen_y, secilen_x, hedef_y, hedef_x, tahta)
    
    
    else:
        return False


beyaz_tas_sirasi = True

durum = True
while durum:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            durum = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x_degeri = event.pos[0] // 100  # fare x değeri pozisyonunu ver
            mouse_y_degeri = event.pos[1] // 100  # fare y değeri pozisyonunu ver
#            print(f"x eksen değeri: {mouse_x_degeri}, y eksen değeri: {mouse_y_degeri}")

            if secili_tas is None:
                if tahta[mouse_y_degeri][mouse_x_degeri] != '--': # boş alana değilde taşa tıklanmışsa çalış
                    if (beyaz_tas_sirasi and tas_rengi(tahta[mouse_y_degeri][mouse_x_degeri]) == 'b') or (not beyaz_tas_sirasi and tas_rengi(tahta[mouse_y_degeri][mouse_x_degeri]) == 's'): #siyah yada beyaz taş kararı
                        secili_tas = (mouse_y_degeri, mouse_x_degeri) # none olan seçili taşa koordinatları ata böylece ikinci tıklamada else bloğuna git
#                        print(tahta)  # kontrol amaçlı tahtanın durumu
#                        print("şuan bir taş seçili")
            else:
                secili_tas_rengi = tas_rengi(tahta[secili_tas[0]][secili_tas[1]])   # seçili taşın koordinatı tahtaya gidiyor ve tahtada karşılık gelen anahtarı görüyor sonra (devamı altta)
                hedef_tas_rengi = tas_rengi(tahta[mouse_y_degeri][mouse_x_degeri])  #o isimdeki anahtar tas_rengi fonksiyonuna gidiyor ve b yada s değerini dönüyor
                if secili_tas_rengi != hedef_tas_rengi: # seçilen taşla hedef taş farklı veya hedef kare boş ise programı çalıştırıyorum
                    tas = tahta[secili_tas[0]][secili_tas[1]] #secili_Tas[0] = satır = y koordinat, [1] ise sütun yani x koordinatını tutar ve bilgileri taş değişkenine atar

                    if tas_hareketi(secili_tas[0], secili_tas[1], mouse_y_degeri, mouse_x_degeri, tahta): # bilgileri tas_hareketi fonksiyonuna yolluyor oradanda onay gelince çalışıyor
#                        print("@@@@@@@@ karar yapısı çalışıyor @@@@@@@@@@@")  # kontrol amaçlı
                        tahta[secili_tas[0]][secili_tas[1]] = '--' # aşağıdakiyle birlikte boş kareyi taşla yer değiştirme işlemi
                        tahta[mouse_y_degeri][mouse_x_degeri] = tas
                        secili_tas = None # hamleler bitince herşeyi sil baştan yapmak için

#                        print(f"taş sırası beyazdamı: {beyaz_tas_sirasi}")
                        beyaz_tas_sirasi = not beyaz_tas_sirasi  # boolean değeri tersiyle değiştiriyoruz
#                        print(f"taş sırası beyazdamı: {beyaz_tas_sirasi}")

                        if sahmat_kontrol("b", tahta):
#                            print(beyaz_tas_sirasi)
                            print("oyun bitti şah mat.")
                            durum = False # tüm döngüyü sonlandır
                        elif sahmat_kontrol("s", tahta):
                            durum = False
                            print("oyun bitti şah mat.")

                    else:
                        secili_tas = None # geçersiz hamle olursa none dön
                else: #seçili taş rengi ile hedef taş rengi aynı ise yani kısaca beyaz taş beyazı yemesin diye tekrar koordinat ataması yapıyoruz
                    secili_tas = (mouse_y_degeri, mouse_x_degeri)



    tahta_konumlar(pencere, tahta)



    pygame.display.update()



pygame.quit()   