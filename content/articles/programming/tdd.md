Title: Test-driven development (TDD) bukan sekedar unit testing
Date: 2018-08-18 07:35
Author: Dhani Setiawan
Category: Programming
Tags: Programming, Python
Slug: test-driven-development
Status: published
Comments: yes

TDD atau Test-driven development?

Yes.., istilah yang lagi ngetrend di dunia software development. Apa dan bagaimana TDD ini? di bawah, saya tuliskan apa itu TDD menurut apa yang saya pahami. Mungkin tidak terlalu akurat tapi paling tidak itulah pemahaman saya tentang metode development ini, silakan dilanjut.

Jadi sebenarnya, istilah Test-driven development ini sudah lama saya baca dan dengar sekilas, tapi kurang menarik minat saya untuk mempelajari lebih lanjut. Alasannya karena satu, karena koding cuma sekedar hobi dan bukan hal serius buat saya waktu itu, saya belum pernah terlibat di project software development yang kompleks. Kedua, karena menurut saya developer yang pakai metode ini seperti kurang kerjaan, siapa yang punya waktu buat nulis kode yang dipakai buat ngetes kodenya sendiri? yang bahkan kode tes ini bisa lebih rumit dan lebih panjang dari kode yang dites.

Dan akhir-akhir ini waktu saya mulai belajar lagi tentang praktek software engineering yang kekinian, termasuk konsep TDD yang saya review lagi. Dan ada sepotong kalimat di Wikipedia, mengatakan bahwa [kode tes ditulis lebih dulu dari kode yang dites](https://en.wikipedia.org/wiki/Test-driven_development#Test-driven_development_cycle) dan ini yang malah yang jadi core idea nya TDD.  
Nah apa maksudnya ini, tulis kode tes buat ngetes kode yang belum ada? jawabannya karena inti dari TDD bukan tentang tes. Ya, setelah baca sana sini, saya berkesimpulan bahwa Test-driven development atau TDD ini bukan tentang **test**, memang ada kata *test* tapi bukan itu intinya.  
Jadi selama ini saya salah karena memahami bahwa TDD dan unit testing itu sama. Ternyata bukan begitu, TDD ini lebih tentang **Spesifikasi dan Implementasi**, TDD lebih ke desain daripada praktek unit testing.

<br />

### Spesifikasi dan Implementasi
Kalau tentang spesifikasi dan implementasi, saya rasa ini tidak asing. Di bahasa pemrograman C misalnya ada C89 dan C99. Bahkan diluar programming pun, banyak contohnya, seperti protokol komunikasi yang spesifikasinya dirumuskan di artikel rfc.

Spesifikasi ini lebih seperti desain dan rule set, sedangkan implementasi seperti.. ya implementasi. Contoh saja begini, dalam komunikasi protokol HTTP misalnya, ada beberapa server http yang kita kenal seperti Apache, Nginx, atau Lighttpd. Ini servernya, sedangkan http client ada web browser yang lebih banyak lagi macamnya, ada Google Chrome atau Mozilla Firefox, dan sebagainya.  
Mereka yang bermacam-macam ini berbicara dengan bahasa yang sama, bahasa http. Prosesnya, client semisal web browser request resource di web, kalau sukses servernya membalas dengan kode 200. Semua web browser paham ini, kalau kode 200 berarti OK. Atau kalau misalnya file yang diminta tidak ditemukan, kode balasannya error 404. Server apa saja kode balasannya sama, dan client apa saja bisa mengerti ini.

Nah dari sini, protokol komunikasi http ini dinamakan spesifikasi, sementara server dan client yang bermacam-macam itu implementasinya, mereka mengimplementasikan spesifikasi http. Tapi biarpun mengimplementasikan spesifikasi yang sama, bisa jadi cara implementasinya tidak sama, karena itu kadang implementasi yang satu lebih baik dari yang lain. Contoh Nginx dan Apache2 yang sama-sama web server populer, Apache dikenal karena full feature sedangkan Nginx dikenal dengan kecepatannya, ini karena cara implementasi yang tidak sama. Begitu juga client http nya, antara Chrome dan Firefox tentu saja ada perbedaan.

Lebih spesifik ke programming, ambil contoh di bahasa C. Bahasa C ini bahasa pemrograman yang terstandar dan library nya ada yang namanya standard library.  
Ambil contoh untuk konversi string ke integer, kita bisa pakai function ``atoi()``. Function ``atoi()`` ini didefinisikan di header *stdlib.h*

Kalau kita baca manualnya ``atoi()``, function ini meng-convert string ke integer, inputnya pointer ke char dan outputnya integer. Char pointer bisa disebut saja dengan string kalau di bahasa lain, di C tidak ada tipe data string tapi anggap saja string.

Jadi spesifikasi ``atoi()`` ini jelas, fungsinya merubah huruf ke angka, inputnya string outputnya angka integer. Nah sedangkan implementasinya, ada beberapa yang umum di instalasi Linux, ada glibc atau GNU C Library ada juga uClibc yang lebih ringan dan biasa dipakai di system embed.  
Dua library ini mengimplementasikan spesifikasi yang sama, entah kita pakai library dari GNU atau uClibc, function ``atoi()`` bisa dipakai dan fungsinya sama, hasilnya juga sama biarpun mungkin yang satu lebih bagus atau lebih cepat dari yang lain.

Di bahasa pemrograman lain, seperti Python pun sama. Python ini sebenarnya spesifikasi bahasa pemrograman yang implementasinya ada lebih dari satu. Ada yang implementasinya pakai bahasa C yang disebut CPython, ada yang pakai Java yang disebut Jython, bahkan ada yang diimplementasikan pakai framework .NET, namanya IronPython.

Sekarang setelah paham tentang spesifikasi dan implementasi, kita kembali ke TDD, Test-driven development. Di TDD, kalau kita mau buat function atau class method, kita tidak langsung koding ngetik kodenya. Tapi, langkah pertama adalah mendefinisikan spesifikasi. Spesifikasi dibuat sejelas mungkin, nama function atau methodnya ini, fungsinya untuk ini, inputnya ini dan outputnya itu. Spesifikasi tidak membahas bagaimana cara implementasinya, karena itu tidak terlalu penting, yang penting adalah apa yang dilakukannya, bukan bagaimana cara melakukannya.

Setelah ada gambaran spesifikasi, kemudian dibuat dokumentasi, ini berguna kalau ada programmer lain yang nantinya pakai function atau method ini. Setelah itu, kita buat kode test. Jadi, kode test disini fungsinya memastikan apakah function atau method yang kita buat itu sesuai dengan spesifikasi yang sudah dibuat diawal atau tidak. Kalau lolos tes, berarti kode kita sesuai dengan spesifikasi kalau tidak berarti ada yang salah dengan implementasinya.

Untuk implementasinya, ada tiga rule yang direkomendasikan. Rule ini tidak strict harus diikuti, tapi saya tulis saja di sini:

1. Make it work.
2. Make it right, dan
3. Make it fast.

Jadi waktu koding implementasi, yang penting lolos uji dulu biarpun kodenya kurang bagus. Setelah lolos tes pertama, baru selanjutnya diperbaiki dan terakhir baru optimasi.

<br />

##TDD dengan Python dan Unittest
Sekarang kita coba pakai contoh TDD pakai bahasa Python, test pakai library unittest.  
Misal kita perlu sebuah function untuk hitung kelipatan dua dari angka yang diinput, misal inputnya 5 hasilnya 10, inputnya 3 hasilnya 6.

Pertama, deskripsikan dengan jelas spesifikasinya.

- Nama function : kali_dua(input)
- Fungsi        : Menghitung kelipatan 2 dari input
- Input         : Integer yang akan dihitung
- Output        : Integer hasil proses

Siapapun yang baca spesifikasi ini pasti paham penggunaannya.

Selanjutnya, buat kode tes di file yang terpisah dari kode yang dites. Misal nama filenya *test_hitung.py* dan nama file kode nya *hitung.py*

    #!/usr/bin/env python

    import unittest
    import hitung

    class TestHitung(unittest.TestCase):
        def test_kali_dua(self):
            self.assertTrue(hitung.kali_dua(5) == 10)

    if __name__ == '__main__':
        unittest.main()


Di kode tes di atas itu kita coba tes dengan input angka 5 dan cek hasilnya apa benar hasilnya 10.  
Dan kalau test ini dijalankan:

    python test_hitung.py

    E
    ======================================================================
    ERROR: test_kali_dua (__main__.TestHitung)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "test_hitung.py", line 8, in test_kali_dua
        self.assertTrue(hitung.kali_dua(5) == 10)
    AttributeError: 'module' object has no attribute 'kali_dua'

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (errors=1)


Error, karena di file hitung.py belum ada function ``kali_dua()``. Berikutnya mulai tulis kode implementasi. Kita buat kode yang sangat simpel saja yang penting lolos tes. Di file hitung.py, kita bisa buat kode seperti di bawah:


    #!/usr/bin/env python

    def kali_dua(input):
        return 10


Kode ini sangat sederhana, return value nya terus 10 berapapun inputnya. Kita buat return value nya 10 karena di kode tes nya kita sudah lihat, tes itu ngecek apa benar hasilnya 10.

Tes lagi.


    python test_hitung.py

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

Hasilnya OK, dari sini kita sudah tahu bahwa kode implementasi itu lolos tes.  
Berikutnya, coba modifikasi kode tes, tes dengan input yang berbeda, 6 misalnya.


    #!/usr/bin/env python

    import unittest
    import hitung

    class TestHitung(unittest.TestCase):
        def test_kali_dua(self):
            self.assertTrue(hitung.kali_dua(5) == 10)
            self.assertTrue(hitung.kali_dua(6) == 12)

    if __name__ == '__main__':
        unittest.main()


Test.

    python test_hitung.py
    F
    ======================================================================
    FAIL: test_kali_dua (__main__.TestHitung)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "test_hitung.py", line 9, in test_kali_dua
        self.assertTrue(hitung.kali_dua(6) == 12)
    AssertionError: False is not true

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (failures=1)


Gagal, karena input 6 hasinya tetap 10, bukan 12. Selanjutnya rule nomor 2, _make it right_. Modifikasi kode supaya berapapun inputnya hasilnya kelipatan duanya.

    #!/usr/bin/env python

    def kali_dua(input):
        return input * 2


Test lagi, hasilnya OK.

    python test_hitung.py

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

Dengan begini, berapapun angka input hasilnya benar.  
Tapi bagaimana kalau nantinya yang manggil function ini kasih input bukan angka tapi huruf? misalnya ``kali_dua("abcd")``. Kita bisa tambahkan verifikasi input, misalnya:

    #!/usr/bin/env python

    def kali_dua(input):
        if not isinstance(input, int):
            raise ValueError("Input not an integer")
        return input * 2

Berikutnya, rule nomor 3 _make it fast_.  
Dari sudut pandang spesifikasi, kode kita sudah benar karena tidak ada error. Tapi kita bisa misalnya, optimasi kode supaya lebih efisien atau lebih cepat tanpa mempengaruhi hasil output, contoh:

    #!/usr/bin/env python

    def kali_dua(input):
        if not isinstance(input, int):
            raise ValueError("Input not an integer")
        return input << 1

Kalau di tes lagi, hasilnya tetap OK, tidak ada yang berubah dari sudut pandang eksternal, biarpun di sisi internal implementasi ada perubahan.

    python test_hitung.py

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

Jadi kita bisa modifikasi implementasi kode supaya lebih bagus dan setelah itu jalankan tes lagi supaya kita yakin bahwa perubahan itu tetap conform atau sesuai dengan spesifikasi dan tidak merusak fungsi program yang lain.

Tentu saja ada saatnya kita pikir bahwa spesifikasi yang sekarang kurang bagus dan perlu diupdate, maka dokumentasi juga perlu diupdate dan juga kode tes nya harus diupdate.

<br />

### Benefits
Sekarang bicara masalah benefit. Dari apa yang saya rasakan pakai metode ini, ada beberapa kelebihannya. Tapi, ini menurut saya pribadi yang tentu saja subjektif dan tidak merepresentasikan TDD.

**Waktu debugging yang berkurang**  
Sebelumnya, biasanya saya koding panjang sambil berharap kode ini nanti bakalan tidak error. Nyatanya, berjam-jam kemudian waktunya untuk debugging cari sumber problem.

Dengan TDD tidak begitu, bukan berarti tidak ada bug, tapi lebih sedikit. Karena dengan TDD, kode dimulai dari sederhana, pastikan tidak ada error, kemudian improve dan improve.

**Design program yang lebih modular**  
Artinya, keterikatan antar modul jadi berkurang. Setiap function atau method bisa dengan gampang diganti kode implementasinya tanpa ada pengaruh ke bagian program yang lain.

Problem ini disebut software regression, ketika satu bagian dimodifikasi, bagian lain jadi rusak, bug ini fix malah muncul bug baru yang lain. Dengan desain yang lebih decoupled atau modular, problem ini bisa diminimalisir.

Satu rule function yang sering dilupakan, bahwa suatu function, method atau subroutine seharusnya cuma melakukan satu hal saja, tapi melakukannya dengan baik. TDD, bisa sedikit memaksa kita berpikir seperti ini.

**Lebih reliable**  
Biasanya, kalau kode program sudah panjang dan kompleks, modifikasi bagian program jadi agak ragu karena bisa jadi bagian yang lain jadi rusak. TDD dengan tes nya bisa buat kita lebih yakin dengan kode yang dibuat atau dirubah, karena tes itu memastikan kode tetap pada jalur.

Paling tidak, beberapa hal di atas ini yang saya rasakan sisi lebihnya. Kalau minusnya, nulis kode jadi lebih lama, selain karena harus nulis tes juga karena berpikir lebih lama diawal.

Terakhir, Test-driven development bukanlah satu-satunya development model, bukan juga senjata yang ampuh disemua keadaan. Tapi menurut saya pribadi, TDD pantas untuk dipelajari.  
Saya yakin tidak semua sepakat dengan saya :)
