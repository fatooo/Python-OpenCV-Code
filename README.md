# Istaka tanımlama, bilardo masası; dış havuz, iç havuz ve bilardo topunun yarıçapı kadar içeride bir çerçeve tanımı.


Çalıştırmak için

python final.py -v videos/fixed.mp4

alternatif video için hsv değerleri kodun içerisindeki alternatifleriyle değiştirilmeli.

 # Undistortion çalıştırmak için
 
 python v_corner.py -v fisheye1.mp4


# Önemli notlar

* Fisheye correction anlık olarak düşük fps verse de, video olarak kaynak ile aynı fpsde kayıt edilebiliyor. Yani programımız atış tekrarını izleme amacıyla kullanılırsa herhangi bir fps sorunu yaşamayız.

* Fisheye correction tam olarak doğru çalışmıyor, ek olarak perpective correction gerekebilir çünkü kamera dikey hiza olarak masanın tam ortasında durmayabiliyor. Ayrıca test3.mp4 isimli videodaki görüntünün nasıl bu kadar kusursuz olduğu araştırılabilir. Buna göre fisheye correctiona gerek olmadan sorun direk kameradan çözülebilir. (bu ihtimalde bile perspective correction gerekebilir)


