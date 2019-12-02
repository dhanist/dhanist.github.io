Title: Tentang SSL/TLS + sertifikat TLS gratis dari Let's Encrypt
Date: 2016-12-19 14:35
Author: Dhani Setiawan
Category: Misc
Slug: ssl-tls-letsencrypt
Status: Published
Comments: yes


Kalau teman-teman lihat di address bar blog ini, protokolnya pakai https yang berarti koneksi ke blog ini pakai secure connection.  
Atau coba cek pakai command

    openssl s_client -connect devnull.web.id:443

Aman tidak harus mahal. Sertifikat ssl yang dipakai blog ini gratis dari Let's Encrypt. 
Beda sama sertifikat gratis lainnya yang mensyaratkan harus langganan hosting di provider tertentu, 
Let's Encrypt tidak, kita cuma perlu membuktikan kalau kita owner website tersebut.

Sebelum ke free certificate dari Let's Encrypt, kita pelajari dulu apa itu **Public Key Infrastructure (PKI)** dan **SSL/TLS**. 
Buat teman-teman pembaca yang mau langsung lompat ke cara install sertifikat, silahkan langsung ke bagian [**Let's Encrypt**](#letsencrypt).

<br />
**Pentingkah security?**  
Kalau mau jawab pertanyaan ini, kita bisa bayangkan jaringan Internet itu seperti komunikasi yang sifatnya terbuka. 
Bayangkan kita bicara satu lawan satu tapi di tengah-tengah kerumunan banyak orang, mereka bisa dengar apa yang kita bicarakan.   
Kalau di jaringan, komunikasi satu lawan satu ini disebut unicast, beda sama broadcast yang komunikasinya satu ke banyak. 
Jenis-jenis komunikasi ini ada saya bahas sedikit di artikel tentang IPv6, ["Hampir" Semua Tentang IPv6](//devnull.web.id/networking/pengenalan-ipv6.html).

Tapi ceritanya jadi lain kalau pembicaraan ini sifatnya harus privat, yang tidak boleh ada yang tahu kecuali dua pihak unicast itu. 
Dan di era Internet sekarang ini ada yang namanya e-commerce, Internet banking, dan lainnya yang sifat komunikasinya harus aman.

Internet kita ini berjalan di atas protokol IP dan routing yang ada di layer 3 OSI. Routing artinya untuk bisa berkomunikasi secara unicast, kita tidak bisa 
langsung bicara ke pihak yang dituju. Pesan kita itu dirouting seperti kalau kirim paket lewat jasa ekspedisi, pesan kita itu diserahkan secara 
estafet dari hop ke hop sampai ke tujuan.

Masalahnya adalah, di setiap hop itu siapapun yang berwenang bisa melihat isi pesan kita, bahkan bukan tidak mungkin mereka bisa merubah isinya. 
Siapa mereka itu? Mereka itu adalah provider Internet kita, Telkom, Indosat, dll. saya juga bekerja di provider Internet dan paham sekali yang seperti ini, jadi jangan 
percaya mereka.

Praktik mendengarkan percakapan (eavesdropping) dan merubah pesan yang dikirim ini dalam bahasa security disebut _MITM_ atau _Man-in-the-middle_ attack.

<br />

###Public Key Infrastructure (PKI)
PKI ini seperti satu set aturan buat me-manage digital certificate. PKI memverifikasi identitas baik itu server atau client, 
mengasosiasikan public key ke identitas tertentu. Gampangnya, PKI itu seperti password. Password itu cara sederhana buat memastikan identitas user, 
artinya identitas user diproteksi dengan password yang password ini cuma user tersebut yang tahu.

PKI juga kurang lebih seperti itu, memproteksi identitas, bukan pakai password tapi pakai encryption key.  
Lebih dari itu, PKI menyelesaikan tiga problem komunikasi sekaligus:

1. **Confidentiality.**
2. **Authentication.**
3. **Integrity.**

Kita bahas satu-satu.

**1) Confidentiality**  
Confidentiality atau kerahasiaan data diatur dalam PKI. Bagaimana caranya kita berkomunikasi satu lawan satu secara rahasia? sementara Internet itu kan 
jaringan publik, siapa saja bisa _eavesdropping_ atau mendengarkan pembicaraan itu. Caranya, komunikasinya pakai kode atau bahasa yang cuma bisa dimengerti 
dua pihak ini, yang lain bisa dengar tapi tidak paham maksudnya.

Cara ini disebut encryption atau encipherment, istilah yang awal lebih umum dan sering dipakai. Encryption atau enkripsi ini caranya mengacak pesan digital, 
bit-bit digital diacak dan dibuat jadi seolah-olah tidak beraturan. Data digital ini bisa dikembalikan lagi seperti aslinya sebelum diacak, prosesnya disebut decrypt. Proses decrypt ini 
pakai kunci yang disebut encryption key. Jadi, cuma pemegang kunci saja yang bisa decrypt pesan itu.

Ada dua metode enkripsi yang ada saat ini, metode simetris atau _symmetric encryption_ sama metode asimetris atau _asymmetric encryption_.

**Symmetric encryption** menggunakan kunci atau key yang sama untuk encrypt atau decrypt. Jadi antara kedua pihak yang bertukar informasi key-nya sama. 
Pesan di-_encrypt_ pakai key itu, di-_decrypt_ pakai key itu juga.

Kelebihan enkripsi metode ini, lebih cepat dibanding asymmetric encryption. Enkripsi ini juga biasanya lebih secure. Key yang dipakai untuk enkripsi ini biasanya pendek, 
cuma 128 bit atau 256 bit. Biarpun pendek tapi bisa lebih secure dari key asymmetric yang lebih panjang.  
Algoritma enkripsi untuk tipe ini semisal **AES (Advanced Encryption Standard)** dan **DES (Data Encryption Standard)**.

Kekurangannya, karena pihak yang berkomunikasi pakai key yang sama, distribusi key ini jadi problem sendiri. Karena kalau tidak hati-hati, key bisa jatuh ke tangan yang salah. 
Supaya aman, distribusi key ini bisa pakai cara tradisional, misalnya key disimpan ke flash disk untuk kemudian dikirim fisiknya. Kalau key ditransfer lewat jaringan Internet, 
ada kemungkinan key tersebut di hijack dan diterima orang yang salah.

**Asymmetric encryption** pakai key yang berbeda antara yang buat encrypt sama yang buat decrypt. Satu key bersifat publik yang disebut _public key_ terus satunya lagi 
disebut _private key_ yang cuma owner nya saja yang bisa akses. Siapapun yang punya public key bisa meng-encrypt data pakai public key tersebut dan yang bisa decrypt cuma 
pemilik private key nya.

Kelebihan metode ini, tidak ada problem distribusi key karena cuma public key saja yang di distribusikan sedangkan private key tetap aman.

Kekurangannya, biasanya metode enkripsi ini lebih lambat dari yang symmetric. Key nya juga biasanya panjang dari 1024 bit sampai 4096 bit. 
Algoritma enkripsi untuk metode _asymmetric encryption_ ini seperti **RSA (Rivest-Shamir-Adleman)** dan **DSA (Digital Signature Algorithm)**.

Contoh penggunaan _asymmetric encryption_ yang populer seperti **PGP**, **OpenPGP**, dan **GPG**. Siapa saja bisa download _public key_ dari keyserver terus pakai key ini buat encrypt file. 
File yang sudah terenkripsi ini kemudian bisa dikirim secara aman, seseorang bisa saja membajak file itu tapi karena dia tidak punya file _private key_-nya, file tidak bisa di-_decrypt_.

Ini contoh _public key_ GPG punya saya dengan id ``0x2d6783968595c582`` yang ada di keyserver <https://sks-keyservers.net/pks/lookup?op=vindex&search=0x2d6783968595c582>.

<br />

**2) Authentication**  
Problem komunikasi berikutnya masalah autentikasi. Autentikasi ini buat memastikan bahwa lawan bicara kita adalah benar dia, bukan orang yang berpura-pura. 
Dalam komunikasi IP begitu juga, user atau client yang berkomunikasi dengan situs online banking misalnya, 
harus memastikan bahwa yang diaksesnya itu benar-benar situs bank yang dimaksud dan bukannya situs tiruan buatan pencuri.

Teknik kejahatan cyber yang seperti ini, misalnya membuat halaman situs yang mirip situs resmi online banking supaya si user tidak sadar masuk 
jebakan disebut teknik _phising_. Salah satu tujuan PKI untuk mencegah hal ini dengan cara memastikan identitas server dengan encryption key.

Caranya, kembali ke asymmetric encryption. Selain untuk encrypt dan decrypt, metode asymmetric juga bisa buat tanda tangan digital atau istilahnya digital signature.  
Kalau untuk encrypt dan decrypt, data digital di encrypt pakai public key kemudian pemilik private key yang bisa decrypt data itu. Untuk signing berlaku sebaliknya, 
pemilik private key menandatangani atau sign data pakai private key, kemudian siapa saja yang punya public key bisa verifikasi tanda tangan tersebut dan memastikan
keasliannya.

Contoh saja, kita akses halaman situs https://www.google.com. Pertama, browser kita yang bertindak sebagai client download digital certificate dari website tersebut. 
Di dalam digital certificate itu ada public key dengan identitas www.google.com. Dengan begitu, client bisa encrypt data pakai public key yang sudah didownload, terus 
server yang bisa decrypt. Begitu juga server bisa tandatangani data digital dengan private key-nya dan client yang sudah punya public key bisa verifikasi signature tersebut.

Nah, sampai sini timbul masalah. Bagaimana kita bisa memastikan bahwa digital certificate yang didownload tadi benar-benar dari Google dan bukan server yang mengaku sebagai Google?  
Kita tidak bisa memastikan, karena siapa saja bisa mengaku sebagai Google dengan membuat certificate dengan identitas www.google.com.

Terus solusinya bagaimana?  
Setidaknya ada dua metode yang mengatasi problem ini, **Certificate Authority (CA)** dan **Web of trust**.

**Certificate Authority** atau **CA** ini berfungsi seperti organisasi yang punya otoritas menandatangani digital certificate. 
Ada banyak organisasi CA, contoh saja seperti Comodo, GeoTrust, DigiCert, dan Symantec yang dulu namanya VeriSign. Digital certificate dari para CA ini secara default sudah dimasukkan di database 
client, misal browser seperti Google Chrome atau Firefox. Certificate dari CA ini dianggap trusted atau terpercaya karena reputasi organisasi yang bagus dan mereka ini diaudit secara berkala.

Para CA ini yang memastikan nama identitas di digital certificate itu valid atau tidak. Misalnya Google membuat digital certificate untuk domain www.google.com, kemudian Google 
membuat file _Certificate Signing Request (CSR)_ ke CA GeoTrust supaya GeoTrust menandatangani digital certificate-nya Google. Di sini GeoTrust melakukan verifikasi apakah request 
itu benar-benar dari Google atau tidak. Caranya bisa bermacam-macam, mulai dari verifikasi website, telepon, sampai penggunaan legal dokumen buat membuktikan identitas.  
Kemudian setelah GeoTrust memastikan validitas request tersebut, CA ini signing atau secara digital menandatangani digital certificate Google, certificate ini kemudian dipakai di 
server Google.

Nah waktu kita browsing Google misalnya, browser melihat bahwa digital certificate punya Google ini ditandatangani oleh GeoTrust. Karena certificate GeoTrust ada di database dan 
dianggap terpercaya, maka digital certificate Google ini juga secara otomatis dipercaya oleh client atau browser.

Tapi biarpun begitu, CA ini jadi _The weakest link_ di PKI. Karena kalau misalnya private key punya CA berhasil dicuri, maka pencuri tersebut bisa seenaknya menandatangani atau signing certificate apa saja, 
termasuk situs phising. Atau misalnya organisasi CA ini secara diam-diam bekerjasama atau berbagi private key dengan organisasi rahasia untuk memata-matai pengguna Internet, kita tidak akan tahu bedanya.

**Web of trust**. Ini alternatif lain selain CA. Web of trust ini dipakai di PGP/OpenPGP/GPG. Bedanya, tidak ada satupun otoritas di sini. Web of trust ini seperti jaring, misalnya 
kita set public key teman kita si B sebagai trusted, dan si B juga mempercayai public key si C, maka public key punya si C juga dianggap trusted. Begitu seterusnya sampai membentuk jaringan kepercayaan.

<br />

**3) Integrity**  
Satu lagi masalah data integrity. Bagaimana PKI meyakinkan dua pihak yang berkomunikasi secara digital bahwa data atau pesan yang dikirim dan diterima itu tidak mengalami perubahan di tengah jalan, 
bahwa data yang diterima itu benar data yang dikirim.

Ada beberapa cara buat mengecek integritas data.

- **Digital Signature.**
- **Message digest atau Hash.**
- **Message Authentication code (MAC).**

**Digital Signature** seperti yang sudah dibahas di atas tentang autentikasi. Digital signing ini caranya si pengirim menggunakan private key-nya untuk sign data digital, tandatangan digital sama datanya 
kemudian dikirim bersama. Si penerima yang sudah punya public key memeriksa validitas signature tersebut. Kalau misalnya di tengah jalan data ini mengalami perubahan, maka signature tersebut jadi tidak 
valid dan si penerima tahu bahwa data ini tidak sama dengan data yang dikirim.

Mari dicoba.  
Misal saya buat file ``text`` yang isinya _"abcde"_, kemudian file tersebut Saya sign. File signature terpisah dengan nama ``text.signature``

    [dhani: ~] Endor > echo "abcde" > text
    [dhani: ~] Endor > gpg -u dhani.stx@gmail.com --armor --output text.signature --detach-sig text
    
    You need a passphrase to unlock the secret key for
    user: "Dhani Setiawan <dhani.stx@gmail.com>"
    2048-bit RSA key, ID 8595C582, created 2016-08-27

Hasil signature seperti di bawah:

    [dhani: ~] Endor > cat text.signature 
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1
    
    iQEcBAABAgAGBQJYU5YtAAoJEC1ng5aFlcWCrA8H/3vZI0+CBAW0NwrewslSDmFi
    WKvUiCV1JQQtZcjT6ljCFLIk7MvtN5s00aEgySTLKRbnOWeL4HO2oNaI0LgjCfB9
    b46LO74Z+2DSBattr5dWG+fusAcOQDblakSItHUG3BpeFQOaPhdjctk4hEm2FKmj
    JVkbSqLWf6VOZe2+F0Zz81tYuJkVlIO7oxW6rzZCYucO98/piyoJQzrrupOio8jr
    N9uxTeNJBuAKMprU9rEHf0VSwMw4baPKzgf/wGht7E/EQgkz9RVuN8zWNxpFgdDI
    fbfCGgMvxxuC2+dzUASz6Ca2jZMOM6k8r8OXdtTpSd5erf1FI88U9df4oh2kDjs=
    =K/SY
    -----END PGP SIGNATURE-----

Coba diverifikasi signature itu.

    [dhani: ~] Endor > gpg --verify text.signature text
    gpg: Signature made Fri 16 Dec 2016 03:22:21 PM WITA using RSA key ID 8595C582
    gpg: Good signature from "Dhani Setiawan <dhani@deltatux.com>"
    gpg:                 aka "Dhani Setiawan <dhani.stx@gmail.com>"

Apa yang terjadi kalau isi file ``text`` dirubah, misalnya rubah huruf terakhir jadi huruf besar, kemudian verifikasi signature-nya.

    [dhani: ~] Endor > echo "abcdE" > text
    [dhani: ~] Endor > gpg --verify text.signature text
    gpg: Signature made Fri 16 Dec 2016 03:22:21 PM WITA using RSA key ID 8595C582
    gpg: BAD signature from "Dhani Setiawan <dhani@deltatux.com>"
    [dhani: ~] Endor >

Kalihatan antara file dengan signaturenya tidak cocok.

Kelemahan metode ini, karena pakai public dan private key yang berarti asymmetric, maka prosesnya lebih lambat dibanding cara yang lain.

<br />

**Message digest atau Hash**. Hampir sama dengan digital signing, hanya saja tidak pakai encryption key apapun, cuma algoritma hashing. Data digital yang dikirim terlebih dulu di hash, kemudian data 
sama hash-nya dikirm. Si penerima data juga kalkulasi hash data itu, terus membandingkan apa hash yang dihasilkan sama atau tidak. Kalau sama berarti data itu valid kalau tidak berarti data itu sudah 
dimodifikasi.

Beberapa algoritma hashing misalnya MD5, SHA1 dan SHA256. hash MD5 panjangnya 128 bit, SHA1 160 bit, dan SHA256 sepanjang 256 bit.

Perhatikan hasil hash text "abcde" di bawah:

    [dhani: ~] Endor > echo "abcde" | md5sum
    9b9af6945c95f1aa302a61acf75c9bd6  -
    [dhani: ~] Endor > echo "abcde" | sha1sum
    ec11312386ad561674f724b8cca7cf1796e26d1d  -
    [dhani: ~] Endor > echo "abcde" | sha256sum
    0283da60063abfb3a87f1aed845d17fe2d9ba8c780b478dc4ae048f5ee97a6d5  -
    [dhani: ~] Endor >

Hash MD5 dan SHA1, sekarang ini sudah dianggap tidak lagi secure karena pendek. Artinya kemungkinan dua data yang berbeda menghasilkan hash yang sama lebih besar dibanding hash yang panjang.

Kita ambil contoh hash SHA256, data "abcde" dirubah ke "abcdE", cuma berubah di karakter terakhir.

    [dhani: ~] Endor > echo "abcde" | sha256sum
    0283da60063abfb3a87f1aed845d17fe2d9ba8c780b478dc4ae048f5ee97a6d5  -
    [dhani: ~] Endor > echo "abcdE" | sha256sum
    98f2c74c952a79ac39fffc5c6beb301c267cfeaeb898d840b1482350fc4e9b91  -
    [dhani: ~] Endor >

Biarpun perbedaan itu cuma antara huruf kecil dan besar, hasil hash berbeda.

Perlu diingat bahwa hash cuma berguna buat memastikan integritas data, tidak bisa memastikan identitas pengirim data.

<br />

**Message Authentication Code (MAC)**. Kurang lebih seperti digital signature, hanya saja key yang dipakai di sini shared key yang berarti symmetric encryption. Kalau hash inputnya cuma satu, data saja, 
MAC inputnya dua, data sama key. MAC fungsinya hampir sama dengan digital signature, selain buat memastikan integritas data juga sebagai autentikasi bahwa data yang dikirim itu berasal dari pengirim 
yang memegang key-nya. Penerima data digital menerima data bersamaan dengan kode MAC-nya, kalau data ini dibuat dari key yang berbeda maka kode MAC itu jadi tidak valid. Begitu juga kalau data 
dimodifikasi di tengah jalan, kode MAC juga akan berbeda.

Kelebihan MAC, karena pakai symmetric encryption jadinya lebih cepat proses generate kode sama proses verifikasinya dibanding digital signature. Kelemahannya juga sama seperti symmetric encryption, 
tidak bisa memastikan dari siapa data itu dikirim karena siapa saja yang punya enryption key bisa mengirim data yang valid.

<br />

###X.509
Baik, setelah membahas tentang _Public Key Infrastructure_ atau _PKI_ di atas, sekarang kita lihat seperti apa digital certificate itu.

Salah satu standar format digital certificate PKI adalah **X.509**. Digital certificate standar X.509 ini yang dipakai di SSL dan TLS.

Digital certificate yang pakai standard X.509 berisi informasi-informasi atau struktur seperti di bawah:

- **Version** atau versi X.509. Ada X.509 versi 1, 2 dan 3.
- **Serial Number**. Serial dari pembuat digital certificate yang membedakan dari certificate lainnya.
- **Algorithm**. Informasi tentang algoritma yang dipakai untuk membuat digital certificate. Algoritma seperti yang sudah dibahas sebelumnya tentang 
confidentiality PKI.
- **Issuer** atau organisasi _Certificate Authority_ (CA) yang mengeluarkan digital certificate.
- **Validity** berisi informasi tentang mulai kapan sampai kapan certificate ini validnya, tanggal expire nya.
- **Subject DN**. Isinya tentang identitas pemilik digital certificate ini, dari nama sampai alamat email.
- **Public key**. Public key asymmetric encryption seperti yang sudah dibahas sebelumnya.

Selain yang di atas itu, ada beberapa informasi yang sifatnya opsional seperti extension X.509.

Sebagai contoh, di bawah ini digital certificate X.509 yang dipakai blog DevNull ini.

    openssl x509 -noout -text -in devnull.web.id/fullchain.pem 
    Certificate:
        Data:
            Version: 3 (0x2)
            Serial Number:
                03:ac:ba:ea:90:d4:7c:b6:17:76:d7:23:75:af:f8:1a:73:89
        Signature Algorithm: sha256WithRSAEncryption
            Issuer: C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
            Validity
                Not Before: Dec  9 14:42:00 2016 GMT
                Not After : Mar  9 14:42:00 2017 GMT
            Subject: CN=devnull.web.id
            Subject Public Key Info:
                Public Key Algorithm: rsaEncryption
                    Public-Key: (2048 bit)
                    Modulus:
                        00:d7:03:8f:1b:50:43:04:bf:f4:bc:bc:ed:77:5c:
                        1c:12:e0:ec:14:14:2e:92:3b:eb:05:54:77:ec:99:
                        01:02:5d:62:ea:cb:79:af:1a:53:d0:49:2b:65:f9:
                        97:be:11:8d:99:bf:2a:2d:e7:63:2e:dc:0b:ff:2f:
                        21:89:17:2f:64:42:37:fc:e9:ef:95:d2:38:77:20:
                        7d:19:ba:ea:35:43:96:2c:70:23:13:97:55:2d:da:
                        78:50:51:66:0f:3f:5c:6e:46:62:20:4a:f4:e0:b9:
                        54:35:94:1d:b7:43:19:51:9f:4c:18:13:9f:f8:a6:
                        e7:b0:64:06:d0:a6:ba:b5:be:cd:e8:35:bc:44:2a:
                        85:9a:6b:00:8e:d3:e7:73:ff:23:a3:fd:4e:3c:e0:
                        f9:9e:3c:be:6e:e7:64:b6:b2:eb:06:20:eb:32:53:
                        a9:10:ea:c1:1f:90:eb:ca:23:8a:14:1a:88:3b:90:
                        ea:f1:e8:41:e4:41:63:99:01:3b:bd:5a:78:61:23:
                        3b:b8:78:5a:e3:22:e7:7a:d9:f1:81:b8:59:91:4a:
                        b5:ec:5e:3b:e1:53:17:23:d1:74:75:77:c4:be:e1:
                        4a:cd:8d:e3:fa:f1:2b:5f:93:87:e4:0c:42:0b:f6:
                        28:69:86:31:97:b8:a5:b1:48:b4:ea:03:07:4b:41:
                        ea:99
                    Exponent: 65537 (0x10001)
            X509v3 extensions:
                X509v3 Key Usage: critical
                    Digital Signature, Key Encipherment
                X509v3 Extended Key Usage: 
                    TLS Web Server Authentication, TLS Web Client Authentication
                X509v3 Basic Constraints: critical
                    CA:FALSE
                X509v3 Subject Key Identifier: 
                    8F:A5:A9:96:A7:D0:1A:53:3E:D9:B2:16:18:29:A0:06:31:CD:6F:9E
                X509v3 Authority Key Identifier: 
                    keyid:A8:4A:6A:63:04:7D:DD:BA:E6:D1:39:B7:A6:45:65:EF:F3:A8:EC:A1
    
                Authority Information Access: 
                    OCSP - URI:http://ocsp.int-x3.letsencrypt.org/
                    CA Issuers - URI:http://cert.int-x3.letsencrypt.org/
    
                X509v3 Subject Alternative Name: 
                    DNS:devnull.web.id
                X509v3 Certificate Policies: 
                    Policy: 2.23.140.1.2.1
                    Policy: 1.3.6.1.4.1.44947.1.1.1
                    CPS: http://cps.letsencrypt.org
                    User Notice:
                        Explicit Text: This Certificate may only be relied upon by Relying Parties and only in accordance with the Certificate Policy found at https://letsencrypt.org/repository/
    
        Signature Algorithm: sha256WithRSAEncryption
            2c:ee:d4:c4:c1:30:d4:4c:60:42:f8:6d:8e:db:cf:86:f3:ae:
            b7:d9:3a:7b:8c:60:31:29:be:7b:a0:9d:f7:49:1c:53:e2:34:
            8e:9b:68:d3:72:b0:97:7c:7f:56:29:fa:80:ab:a9:40:a4:99:
            39:47:9e:9d:af:ea:c6:61:17:f3:18:a5:c9:1e:73:cc:9e:8b:
            25:7d:76:16:54:ea:f8:ec:e0:27:41:43:61:1a:54:9a:14:ba:
            c8:a4:a2:20:64:84:6d:b4:ac:d7:48:e0:d1:e4:a3:2a:92:ae:
            a1:d4:c8:86:2c:8a:f4:7a:0c:27:d3:ac:7f:51:11:a7:38:a8:
            a7:4a:c8:3c:4a:11:b3:81:e7:25:bc:59:15:b0:51:88:2e:b7:
            73:a4:73:bb:1a:f3:78:36:60:18:75:a1:a4:eb:b7:08:0d:6c:
            20:26:bd:e1:76:fc:bc:77:ca:52:c5:43:bb:46:ab:5b:67:4f:
            c8:7b:20:b4:1f:7b:b2:52:13:35:e3:80:ea:9f:55:4d:c1:04:
            59:69:44:55:d6:fb:ba:ae:97:fa:fc:73:fa:94:47:cd:30:8e:
            93:cd:a7:1c:1a:1d:45:9a:e6:d0:2e:94:c6:84:c9:38:a0:5b:
            35:e4:8a:8e:fe:d8:49:d7:a0:71:9f:c3:c8:02:23:ab:95:ca:
            eb:72:8e:b6

Jadi, kata "sertifikat SSL" yang sering kita dengar itu sebenarnya istilah marketing, istilah teknis yang benar adalah sertifikat X.509. Cuma karena sertifikat ini sering dipakai di SSL, makanya 
jadi lebih terkenal sebagai "sertifikat SSL", padahal TLS juga pakai standar sertifikat X.509 yang sama.

<br />

###SSL/TLS
**SSL (Secure Socket Layer)** dan **TLS (Transport Layer Security)**, dua kata yang kadang membingungkan, paling tidak buat saya begitu. Maksudnya begini, kadang SSL dan TLS ini dua hal yang berbeda yang tidak bisa ketemu. Tapi kadang SSL dan TLS 
ini adalah hal yang sama. SSL ya TLS, TLS ya SSL, karena itu biasanya ditulis SSL/TLS. saya rasa ini penting untuk dipahami bahwa ada maksud yang ambigu di dua kata ini.

SSL/TLS ini sama-sama implementasi security _PKI_ dan pakai digital certificate X.509.

Kita bahas dulu perbedaannya, bahwa SSL dan TLS ini dua hal yang berbeda yang tidak bisa ketemu.  
Kalau membahas perbedaannya, yang dimaksud dengan SSL dan TLS adalah protokolnya. Mereka ini SSL dan TLS 
berbicara dengan bahasa yang berbeda, karena itu tidak bisa ketemu.  
TLS ini seperti evolusi dari SSL, SSL awalnya didevelop dari Netscape. saya ambil dari [Wikipedia](https://en.wikipedia.org/wiki/Transport_Layer_Security#SSL_1.0.2C_2.0_and_3.0), 
bahwa versi pertama SSL yaitu versi 1.0 tidak pernah dirilis karena banyak celah keamanan. 
Begitu juga SSL 2.0 yang masih banyak kekurangan, yang akhirnya melahirkan versi ketiga SSL 3.0 yang merupakan hasil design ulang protokol sebelumnya.

Terus kemudian muncul TLS 1.0 sebagai successor dari SSL 3.0. Bedanya, TLS ini standar dari _Internet Engineering Task Force_ atau IETF dan bukan dari Netscape lagi yang berarti bahwa TLS ini standar terbuka. 
Tapi biarpun TLS 1.0 ini penerus SSL 3.0, dua protokol ini tidak kompatibel. saya tidak memahami detailnya, tapi salah satu perbedaan mendasar adalah di _Message Authentication Code_ atau _MAC_ yang sudah 
dibahas di atas. MAC di SSL pakai block cipher sedangkan di TLS pakai hash yang lebih dikenal dengan HMAC.

Setelah TLS 1.0, disusul TLS 1.1 dan yang sekarang adalah TLS 1.2. Versi TLS yang selanjutnya TLS 1.3 yang sekarang masih berbentuk draft di IETF.

Waktu komunikasi secure antara server sama client, terlebih dulu ada proses _handshake_ atau negosiasi parameter antara TLS di server dan client. Client akan meng-_advertise_ ke server bahwa 
dia support SSL 3.0, TLS 1.0, TLS 1.1, dan TLS 1.2 misalnya. Berdasarkan informasi ini, server akan memilih protokol yang cocok dan secara default akan memilih yang paling baru. Misalnya 
si server cuma bisa sampai TLS 1.1 maka ini yang dipilih.

Sekarang ini SSL 3.0 dianggap sudah tidak lagi aman, karena itu kebanyakan server tidak menyertakan protokol ini waktu proses _handshake_. Salah satu penyebab SSL 3.0 ditolak server 
karena ada vulnerability yang dikenal dengan POODLE, baca lebih lanjut tentang POODLE di <https://en.wikipedia.org/wiki/POODLE>

<br />

Kemudian kita bahas persamaan dua kata ini SSL dan TLS. Kalau sebelumnya, perbedaan mereka ini ada di protokol atau bahasa yang dipakai, persamaan ini lebih ke pembedaan saja antara komunikasi yang aman 
sama yang tidak.

Contohnya begini, _Hypertext Transfer Protocol_ atau _HTTP_ itu berjalan di atas protokol TCP di port 80 yang sifatnya terbuka dan tidak aman. Ada HTTP yang sifatnya secure yang disebut _HTTPS_, dan ini 
berjalan di atas protokol TCP port 443. Jadi ada dua _HTTP_, yang aman di port 443 dan yang tidak terenkripsi di port 80. Kalau di address bar browser, url untuk SSL/TLS diawali ``https://`` sedangkan non 
SSL/TLS ``http://``

Contoh yang lain seperti protokol email:

**SMTP**. SMTP di port 25 dan SMTP SSL/TLS di port 465, umumnya disebut smtps.  
**POP3**. POP3 di port 110 dan POP3 SSL/TLS di port 995, disebut pop3s.  
**IMAP**. IMAP di port 143 dan IMAP SSL/TLS di port 993, atau imaps.

Secara teknis, port yang secure itu pakai protokol TLS. Tapi mengapa masih disebut juga SSL itu saya kurang paham, mengapa tidak disebut saja HTTP TLS atau SMTP TLS.

Dari sini, kita jadi paham bahwa maksud penulisan SSL/TLS ini adalah bahwa SSL dan TLS ini hal yang sama.

Terus kalau diperhatikan, masing-masing komunikasi itu ada di dua port yang berbeda. Sekarang ini yang seperti itu dianggap wasted atau buang-buang resource, karena itu sekarang ini 
ada lagi yang namanya **STARTTLS**.  
Apa bedanya? bedanya kalau SSL/TLS pakai port yang berbeda untuk komunikasi yang secure, STARTTLS pakai port yang sama. Jadi SMTP tetap di port 25, komunikasi dimulai dari tidak terenkripsi 
kemudian diswitch atau dirubah ke komunikasi terenkripsi yang aman tapi tetap di port yang sama.

<br />

###SSL/TLS Handshake
Sebelum bisa bertukar data secara secure, antara client dan server perlu negosiasi dulu, proses ini namanya _handshake_. Proses ini diperlukan karena implementasi dan support algoritma enkripsi 
antara client dan server bisa beda, jadi perlu adanya kesepakatan.

Proses SSL/TLS Handshake kurang lebih seperti di bawah:

1. Client mengirim _"client hello"_ ke server. "client hello" ini berisi informasi CipherSuite atau algoritma apa saja yang disupport oleh client, versi SSL atau TLS juga diinformasikan di sini.
2. Server membalas _"client hello"_ itu dengan _"server hello"_ yang berisi CipherSuite yang dipilih server. Bersamaan "server hello" ini dikirim juga digital certificate server.
3. Client memeriksa validitas digital certificate yang dikirm server. Kalau digital certificate itu tidak valid entah karena alasan apapun, misalnya sudah expired atau digital certificate itu tidak dipercayai 
oleh client, maka proses handshake berhenti.
4. Sebaliknya, kalau digital certificate itu valid dan trusted, maka client membuat semacam password yang disebut pre-master secret yang diambil dari byte string yang acak. Pre-master secret ini kemudian dienkripsi 
dengan public key server, public key ini ada di dalam certificate. Kemudian pre-master secret yang sudah terenkripsi dikirim ke server.
5. Server kemudian men-_decrypt_ pre-master secret itu dengan private key-nya.
6. Sampai di sini, client dan server yang sudah punya pre-master secret yang sama. Kemudian mereka berdua membuat symmetric encryption key berdasarkan pre-master secret tadi. Key ini yang nantinya dipakai buat encrypt dan decrypt data.
7. Client mengirim pesan _"finished"_.
8. Server mengirim pesan _"finished"_.

Setelah proses _handshake_ di atas selesai, masing-masing client dan server bisa kirim dan terima data dengan terenkripsi pakai symmetric key. Perlu diingat bahwa symmetric encryption key yang dibuat tadi cuma berlaku 
di session itu, session lain lagi key-nya baru lagi.

Kelihatan dari sini bahwa SSL/TLS ini pakai dua metode enkripsi yang berbeda, asymmetric dan symmetric. Asymmetric encryption dipakai waktu handshake supaya symmetric key bisa dibuat dengan aman, sedangkan symmetric key 
dipakai untuk komunikasi data.  

Kita ingat lagi di atas, kelebihan symmetric encryption adalah kecepatannya. Sedangkan kelemahannya adalah distribusi key, dan penggunaan asymmetric encryption dipakai menutupi kekurangan itu. Di proses _handshake_ di 
atas tidak ada distribusi key, tapi masing-masing client dan server membuat key berdasarkan pre-master secret yang dienkripsi pakai public key server.

<br />

###<a name="letsencrypt"></a>Free digital certificate dari Let's Encrypt
Baik, pertama saya kutip dulu dari situs <https://letsencrypt.org>

> Let’s Encrypt is a free, automated, and open certificate authority (CA), run for the public’s benefit. It is a service provided by the Internet Security Research Group (ISRG).

> We give people the digital certificates they need in order to enable HTTPS (SSL/TLS) for websites, for free, in the most user-friendly way we can. We do this because we want to create a more secure and privacy-respecting Web.

Sebelum Let's Encrypt, sudah ada beberapa CA yang punya certificate gratis. Kebanyakan mereka itu provider hosting, yang kalau kita langganan hosting di situ kita dapat free SSL/TLS certificate. Ada juga StartSSL, CA dari 
perusahaan StartCom yang berbasis di.. <s>batuk..</s> Israel.  

Ada juga CAcert, oraganisi CA non profit. saya sendiri sudah lama pakai certificate dari CA ini, kekurangannya CA ini adopsinya kurang luas. Debian sendiri yang dulu defaultnya ada certificate dari CA ini sekarang sudah tidak 
di-include-kan lagi.

Certificate authority atau CA ada yang namanya **Root CA** sama **Intermediate CA**. Jadi CA aslinya yang root, hanya saja untuk keamanan root CA ini tidak langsung mengeluarkan SSL/TLS certificate. Root CA ini mengeluarkan atau 
secara digital menandatangani certificate untuk CA lain yang disebut Intermediate CA. Intermediate CA ini yang kemudian melayani permintaan certificate atas nama root CA.  
Root CA bisa saja punya lebih dari satu Intermediate CA, dan karena proses penandatanganan certificate sudah didelegasikan ke Intermediate CA, private key dari root CA bisa disimpan secara offline di tempat yang aman, aman 
dari pencurian termasuk juga aman dari force majeure seperti kebakaran.

Nah, Let's Encrypt di sini perannya adalah sebagai Intermediate CA, sedangkan root CA nya adalah DST Root CA X3 yang secara default sudah ada di browser atau SSL/TLS client.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/crt-chain.png" alt="certificate chain" title="Certificate Chain" />
</div>

<br />

###Instalasi

Untuk instalasinya, Let's Encrypt perlu memastikan bahwa kita adalah benar sebagai pemilik domain dan website. Salah satu dari tiga cara bisa diambil buat verifikasi ini.

1. Memanfaatkan web server yang sudah running, misal Apache2 atau Nginx.
2. Standalone web server dari Let's Encrypt client.
3. Manual, cara terakhir yang agak ribet. Cara ini diambil kalau kita tidak punya akses ke web server, misalnya website kita ada di shared hosting yang tidak punya fasilitas install Let's Encrypt.

Karena system yang saya pakai Debian Jessie, mungkin saja cara di bawah ini tidak bisa diaplikasikan ke system lain.

Pertama, install Let's Encrypt client yang bernama certbot pakai user root.

    apt-get update && apt-get install -y certbot

Kalau kita mau pakai web server yang sudah running, mungkin karena alasan traffic website yang tinggi sehingga web server tidak bisa di shutdown, kita perlu install plugin buat web server itu.  
Untuk plugin Apache2

    apt-get install python-certbot-apache

Untuk Nginx, ganti saja ``apache`` dengan ``nginx``.

Yang perlu kita input ke program certbot adalah nama domain dan email untuk keperluan registrasi dan recovery. Kalau di server yang sama ada lebih dari satu domain, kita bisa buat satu sertifikat saja untuk semua domain tersebut.

**Cara pertama**, pakai existing web server, Apache2 misalnya:

    certbot certonly --apache --agree-tos --email hostmaster@example.com --domain example.com

- ``certonly`` di sini kita maksudkan bahwa kita cuma perlu certificate saja.
- ``--agree-tos`` Term of service dari protokol komunikasi _Automated Certificate Management Environment_ (ACME).
- ``--email`` Sesuaikan email yang valid.
- ``--domain`` nama domain sebagai identitas di certificate.

Untuk domain yang lebih dari satu, bisa seperti di bawah:

    certbot certonly --apache --agree-tos --email hostmaster@example.com --domain example.com --domain example2.com

**Cara kedua** pakai builtin web server certbot.  
kalau web server masih running, kill dulu.

    killall apache2

Saya pakai command ``killall apache2`` karena entah alasan apa command ``systemctl stop apache2`` tidak bisa shutdown service apache2.

    certbot certonly --standalone --agree-tos --email hostmaster@example.com --domain example.com
    
Setelah proses selesai, hidupkan lagi web server.

    systemctl start apache2

**Cara ketiga**, manual. Ini dipakai kalau misalnya kita langganan shared hosting yang kita tidak punya akses ssh ke server, web hosting tersebut tidak ada fitur install Let's Encrypt, dan support mereka tidak bisa membantu 
instalasi Let's Encrypt atau bahkan tidak tahu apa itu Let's Encrypt.

Caranya adalah, ``certbot`` kita install di laptop atau pc desktop misalnya, kemudian dari laptop itu eksekusi command ``certbot`` seperti dibawah:

    certbot certonly --manual --agree-tos --email hostmaster@example.com --domain example.com

Untuk cara manual, akan muncul warning dari ``certbot`` bahwa ip address kita dilog di server Let's Encrypt.  
Lewat cara ini, Let's Encrypt akan menginformasikan bahwa kita perlu upload file ke website, file ini berisi string sesuai instruksi ``certbot``. Cara verifikasi ini mirip seperti verifikasi Google, yang kita perlu upload 
file tertentu ke website kita.

<br />

Begitu sukses instalasi, digital certificate ada di ``/etc/letsencrypt/live/example.com/`` example.com cuma contoh saja. Ada 4 file yang keterangannya seperti di bawah:

- ``chain.pem`` Ini adalah file digital certificate Let's Encrypt, Intermediate CA kita.
- ``cert.pem`` Ini digital certificate kita yang sudah ditandatangani Let's Encrypt.
- ``fullchain.pem`` Gabungan antara ``chain.pem`` dan ``cert.pem``. File ini yang nantinya dipakai di web server karena kebanyakan browser tidak ada certificate Lets's Encrypt, maka certificate dari Intermediate CA kita 
perlu disertakan supaya membentuk chain lengkap dari kita ke Let's Encrypt sampai ke Digital Signature Trust (DST Root CA) yang root CA ini sudah ada di browser client.
- ``privkey.pem`` Ini adalah private key kita seperti yang sudah dibahas sebelumnya tentang asymmetric encryption. File ini yang harus kita jaga kerahasiannya.

Setelah itu, tinggal kita pakai file-file ini di konfigurasi web server, contoh untuk Apache2.

    SSLEngine               on
	SSLCertificateFile      /etc/letsencrypt/live/example.com/fullchain.pem
	SSLCertificateKeyFile   /etc/letsencrypt/live/example.com/privekey.pem

<br />

###Renewal
Untuk renewal, caranya sama dengan instalasi, hanya saja ``certonly`` diganti ``renew``. Kemudian ``renew`` juga tidak perlu parameter ``--email`` dan ``--domain``.  
Misalnya:

    certbot renew --standalone --agree-tos

Atau

    certbot renew --apache --agree-tos

Untuk yang manual.

    certbot renew --manual --agree-tos

Terkecuali untuk yang ``manual``, ``renew`` bisa dieksekusi lewat ``cron`` supaya bisa renew certificate secara otomatis kalau sudah mendekati masa expire. Dan tidak seperti digital certificate yang mahal, certificate 
dari Let's Encrypt ini umurnya pendek, cuma tiga bulan saja. Tapi karena renewal bisa diproses secara otomatis lewat ``cron`` saya rasa tidak ada bedanya.

<br />
Baik, sampai sini semoga tulisan ini bisa dipahami. Silahkan di-share, dikomentari dan dikoreksi kalau ada yang salah atau kurang.

Terima kasih.
