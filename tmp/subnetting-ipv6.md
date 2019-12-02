Title: Subnetting IPv6 bisa semudah IPv4, bahkan lebih mudah.
Date: 2016-04-07 13:55
Author: Dhani Setiawan
Category: Networking
Tags: IPv6
Slug: subnetting-ipv6-mudah
Status: published
Comments: yes

<br />
**PENTING!!!**  
_Buat teman-teman pembaca, saya mohon maaf di artikel ini ada kesalahan._  
_Setelah ada komen dari agan Ahmad Ajrul Falaah dibawah, saya review lagi artikel ini ternyata ada kesalahan._

_Mudahan dalam waktu dekat saya bisa tulis revisi nya._  

---

IPv6 itu heksadesimal dan 128 bit, identik dengan susah dan ribet. Tapi bagaimana kalau ternyata subnetting IPv6 itu semudah, kalau tidak lebih mudah dari IPv4? Bilangan heksadesimal yang terlihat susah dan mengerikan itu bisa jadi malah memudahkan.

<div class="aimg">
<img src="/images/ipv6.png" width="400" height="250" alt="IPv6" />
</div>

Suka atau tidak, masa kejayaan IPv4 sudah berakhir. 2 ^ 32 atau sejumlah 4 milyar ip address itu tidak akan cukup untuk semua perangkat yang terkoneksi dengan Internet saat ini. Baca artikel APNIC ini <https://www.apnic.net/community/IPv4-exhaustion/>{target="_blank"}, IPv4 pool yang ada di APNIC sudah menipis. Dengan kondisi seperti ini, maka adopsi IPv6 menjadi semakin mendesak.

Baca juga statistik penggunaan IPv6 yang dibuat Google <http://www.google.co.id/intl/en/IPv6/statistics.html>{target="_blank"}, tren adopsi IPv6 semakin tinggi dari tahun ke tahun. Lihat juga di bagian Per-Country IPv6 Adoption, dari jumlah traffic Google yang berasal dari Indonesia, hanya 0.05% yang melalui jaringan IPv6, sisanya yang 99.95% adalah IPv4.

Meskipun Google tidak mewakili semua traffic penggunaan Internet Indonesia, tapi saya rasa traffic Indonesia ke Google sangat besar karena banyaknya pengguna Android, Youtube dan layanan Google lainnya di Indonesia. Data Google tersebut mengatakan bahwa rate adopsi IPv6 di Indonesia berjalan lambat.

Kita tidak perlu studi untuk mengatakan bahwa faktor terbesar lambatnya penerapan IPv6 di Indonesia adalah karena SDM, dan salah satu alasan dari sekian banyak alasan adalah karena IPv6 terlihat mengerikan, paling tidak itu yang saya pikirkan. Subnetting heksadesimal 128 bit itu memang terlihat menakutkan.

Di ISP tempat saya bekerja saat ini sudah menerapkan jaringan dual stack, satu jaringan dengan dua ip network, IPv4 dan IPv6. Ternyata, setelah beberapa waktu dengan IPv6, subnetting IPv6 tidak begitu sulit. Saya menemukan cara gampang subnetting IPv6, paling tidak buat Saya begitu dan akan coba Saya tuliskan dibawah.

## IPv4 vs IPv6
Sebelum subnetting, kita perlu paham perbedaan IPv4 dan IPv6. Pertama, IPv6 tidak kompatibel dengan IPv4, yang artinya jaringan IPv4 tidak bisa berkomunikasi dengan jaringan IPv6. Tidak seperti IPv4, IPv6 tidak ada broadcast address, tidak ada yang namanya ip private dan ip publik. Di IPv6 private address disebut link local sedangkan ip publik disebut global unicast address. Bedanya dengan IPv4, link local tidak bisa untuk akses Internet, cuma bisa lokal.

Kemudian, IPv6 itu /64 everywhere. Subnet terkecil yang direkomendasikan adalah /64 [1], meskipun untuk link inter-router ada RFC yang merekomendasikan menggunakan /127 [2]. Jadi biarpun di satu jaringan cuma ada 10 host, yang dipakai tetap /64.  
Jadi, untuk subnetting kita tidak perlu sampai 128 bit, hanya 64 bit diawal. Bit ke 65 sampai ke 128 adalah host.

Selain yang disebutkan itu, masih banyak perbedaan antara IPv6 dan IPv4 tapi tidak akan dibahas disini.

## Subnetting IPv6
Sebenarnya, penggunaan heksadesimal lebih memudahkan untuk subnetting daripada desimal seperti IPv4. Karena satu karakter heksadesimal itu sama dengan 4 bit bilangan biner. Ini keuntungannya, menghitung subnet heksadesimal jadi lebih gampang.

Di artikel ini kita akan gunakan prefix 2001:db8::/32. Prefix ini, 2001:db8::/32 memang dikhususkan untuk dokumentasi, tutorial, dan sebagainya [3].  
Perhatikan prefix 2001:db8:abcd:dead::/64 di gambar.

**Gambar 1.**
<div class="aimg">
<img src="/images/ipv6-bit.png" title="IPv6" alt="IPv6"/>
</div>

Seperti yang saya sebutkan sebelumnya, satu karakter hex sama dengan 4 bit. Hitungan bit dimulai dari kiri ke kanan. Di prefix _**2001:db8:abcd:dead::/64**_, karakter pertama adalah bilangan hex 2 sepanjang 4 bit, bit 1 sampai bit 4. Karakter kedua angka hex 0, 4 bit, bit ke 5 sampai bit ke 8, begitu seterusnya.

Nah, misalnya untuk melakukan subnetting prefix length /32, maka yang kita ubah adalah dari bit ke 33 sampai 64, sedangkan bit 1 sampai 32 tidak bisa dirubah.

Subnetting adalah membagi jaringan besar /32 misalnya, ke jaringan-jaringan yang lebih kecil /33, /34, dst. Sedangkan sebaliknya, menggabungkan jaringan-jaringan kecil menjadi satu jaringan besar disebut supernetting.

Waktu menghitung subnetting, saya membayangkan subnet itu seperti pohon. Seperti network /32 digambar.

**Gambar 2.**
<div class="aimg">
<img src="/images/prefix-tree.png" title="IPv6 prefix tree" alt="IPv6 prefix tree"/>
</div>

Seperti terlihat, /33 adalah 2 kali dari /32, /34 adalah 2 kali /33 atau 4 kali /32, begitu seterusnya.

Kita ambil contoh, kita diberikan network /32, kemudian diminta untuk memecah network /32 itu ke jaringan yang lebih kecil /36. Dari sini saya akan perkenalkan istilah dan variabel.

- _root_  : /32 kita sebut root, ini adalah network besar kita.
- _child_ : /36 kita sebut child. Anak, atau cabang dari root /32.
- _x_     : Karakter heksadesimal kesekian dari child. Lihat gambar 1, child /36 yang berarti 36 bit, dan bit ke 36 di gambar ada di karakter heksadesimal ke 9. Jadi x sama dengan karakter hex ke 9.
- _y_     : y adalah jumlah subnet. 2 ^ (child - root) = 2 ^ (36 - 32) = 2 ^ 4 = 16. y, atau jumlah subnet sama dengan 16.
- _z_     : z adalah kelipatan network. Kita tambahkan x, atau dalam contoh ini karakter ke 9 dengan z.

Sekarang, perhatikan tabel dibawah:

| **y (Jumlah Subnet)** | **z (Kelipatan Network)** |
|-----------------------|---------------------------|
|           2           |             8             |
|           4           |             4             |
|           8           |             2             |
|           16          |             1             |
|           32          |             8             |
|           64          |             4             |
|          128          |             2             |
|          256          |             1             |
|          512          |             8             |
|          1024         |             4             |
|          2048         |             2             |
|          4096         |             1             |

Cara membaca tabel tersebut:

- kalau kita membagi jaringan besar menjadi 2 jaringan kecil atau y = 2, maka jaringan berikutnya dengan menambahkan 8, z = 8.
- Kalau kita mebagi jaringan besar menjadi 4 jaringan kecil, y = 4 maka jaringan berikutnya adalah kelipatan 4, atau dengan menambahkan 4, z = 4.
- Kalau y sama dengan 8, maka network berikutnya adalah kelipatan 2 atau z = 2.
- Kalau y sama dengan 16 jaringan kecil, maka z sama dengan 1.
- Dan seterusnya.

Tabel tersebut dibatasi cuma sampai 4096, bisa ditambah lagi sampai 2 ^ 64 dan nilai z polanya sama, yaitu 8, 4, 2, 1.

Dalam membagi jaringan, yang biasanya jadi pertanyaan adalah berapa jumlah subnet, apa saja networknya dan berapa jumlah host.  

**Contoh 1.**  
Diberikan network 2001:db8::/32, subnetting ke jaringan kecil /36. Berapa jumlah subnet, dan apa saja networknya?  

    Jumlah subnet adalah y

    y     = 2 ^ (child - root)
          = 2 ^ (36 - 32)
          = 2 ^ 4
          = 16

Selanjutnya kita cari x, atau karakter kesekian dari IPv6 address. Lihat kembali ke gambar 1, /36 atau bit ke 36 ada di karakter ke 9, jadi:

    x = 9

Terakhir yang dicari adalah z. Menurut tabel, karena y = 16, maka z = 1. Maka x akan kita tambahkan dengan 1, x adalah karakter ke 9.

    Hitung dari kiri ke kanan, karakter ke 9 heksadesimal kita tambahkan dengan 1. Ulangi terus sampai jumlah subnet, atau y = 16.
   
    ========================
    y    subnet
    ========================
    1    2001:0db8:0000::/36 atau bisa ditulis 2001:db8::/36
    2    2001:0db8:1000::/36
    3    2001:0db8:2000::/36
    4    2001:0db8:3000::/36
    5    2001:0db8:4000::/36
    6    2001:0db8:5000::/36
    7    2001:0db8:6000::/36
    8    2001:0db8:7000::/36
    9    2001:0db8:8000::/36
    10   2001:0db8:9000::/36
    11   2001:0db8:a000::/36
    12   2001:0db8:b000::/36
    13   2001:0db8:c000::/36
    14   2001:0db8:d000::/36
    15   2001:0db8:e000::/36
    16   2001:0db8:f000::/36

**Contoh 2.**  
Diberikan network 2001:db8::/32, subnetting ke jaringan kecil /34. Berapa jumlah subnet, dan apa saja networknya?  

    Jumlah subnet adalah y

    y     = 2 ^ (child - root)
          = 2 ^ (34 - 32)
          = 2 ^ 2
          = 4

Selanjutnya kita cari x, atau karakter kesekian dari IPv6 address. Lihat kembali ke gambar 1, child 34 atau bit ke 34 ada di karakter ke 9, jadi:

    x = 9

Terakhir yang dicari adalah z. Menurut tabel, karena y = 4, maka z = 4. Maka x akan kita tambahkan dengan 4, x adalah karakter ke 9.

    Hitung dari kiri ke kanan, karakter ke 9 heksadesimal kita tambahkan dengan 4. Ulangi terus sampai y = 4.

    ========================
    y    subnet
    ========================
    1    2001:0db8:0000::/34 atau bisa ditulis 2001:db8::/34
    2    2001:0db8:4000::/34
    3    2001:0db8:8000::/34
    4    2001:0db8:c000::/34


**Contoh 3.**  
Dari network 2001:db8:c000::/34 diatas, bagi lagi kedalam 3 jaringan kecil.  

Kita pelu ingat bahwa y, atau jumlah subnet adalah pangkat 2. Yaitu 1, 2, 4, 8, 16, 32, 64, dan seterusnya. Jadi membagi jaringan kedalam 3 jaringan kecil itu tidak bisa. Bisanya, kita ambil yang mendekati tapi tidak lebih kecil. Yang mendekati 3 tapi tidak lebih kecil dari 3 adalah 4, atau 2 ^ 2. Jadi, kita akan bagi 2001:db8:c000::/34 kedalam 4 subnet kecil, atau y = 4.


    root    = 34
    child   = tidak diketahui
    y       = 4

    Kita cari child dengan sedikit aljabar.

                y = 2 ^ (child - root)
                4 = 2 ^ (child - 34)
     (child - 34) = akar 4
     (child - 34) = 2
            child = 34 + 2
            child = 36

    Jadi,
     root = 34
    child = 36
        y = 4

Menurut tabel, karena y atau jumlah subnet 4,maka z = 4. Karena child = 36, lihat di gambar 1, bit ke 36 ada di karakter ke 9. Jadi x akan kita tambahkan 4. x adalah  karakter ke 9.

    Hitung dari kiri ke kanan, x atau karakter ke 9 heksadesimal kita tambahkan dengan 4, karena z = 4. Ulangi terus sampai y = 4.
    
    ======================
    y   subnet
    ======================
    1   2001:0db8:c000::/36 atau bisa ditulis 2001:db8:c000::/36
    2   2001:0db8:d000::/36
    3   2001:0db8:e000::/36
    4   2001:0db8:f000::/36


**Contoh 4.**  
Di dalam network 2001:db8:e000::/36, berapa jumlah host yang ada di network tersebut, berapa alamat ip host pertama dan berapa alamat ip host terakhir?  
Karena IPv6 sepanjang 128 bit, maka jumlah host untuk /36 adalah:
    
    2 ^ (128 - 36)
    2 ^ 92
    4.951.760.157.000.000.000.000.000.000

Saya tidak tahu bagaimana menyebut angka diatas.

Dalam network 2001:db8:e000::/36, host awal dan terakhir sbb:

    host pertama  : 2001:db8:e000:0000:0000:0000:0000:0001 atau bisa ditulis 2001:db8::1
    host terakhir : 2001:db8:efff:ffff:ffff:ffff:ffff:ffff


**Contoh 5, terakhir.**  
Bagi network 2001:db8:e000::/36 ke subnet /41.

Silahkan dihitung, kalau jawaban sama dengan dibawah, selamat.

    =======================
    y   Subnet
    =======================
    1   2001:0db8:e000::/41
    2   2001:0db8:e080::/41
    3   2001:0db8:e100::/41
    4   2001:0db8:e180::/41
    5   2001:0db8:e200::/41
    6   2001:0db8:e280::/41
    7   2001:0db8:e300::/41
    8   2001:0db8:e380::/41
    9   2001:0db8:e400::/41
    10  2001:0db8:e480::/41
    11  2001:0db8:e500::/41
    12  2001:0db8:e580::/41
    13  2001:0db8:e600::/41
    14  2001:0db8:e680::/41
    15  2001:0db8:e700::/41
    16  2001:0db8:e780::/41
    17  2001:0db8:e800::/41
    18  2001:0db8:e880::/41
    19  2001:0db8:e900::/41
    20  2001:0db8:e980::/41
    21  2001:0db8:ea00::/41
    22  2001:0db8:ea80::/41
    23  2001:0db8:eb00::/41
    24  2001:0db8:eb80::/41
    25  2001:0db8:ec00::/41
    26  2001:0db8:ec80::/41
    27  2001:0db8:ed00::/41
    28  2001:0db8:ed80::/41
    29  2001:0db8:ee00::/41
    30  2001:0db8:ee80::/41
    31  2001:0db8:ef00::/41
    32  2001:0db8:ef80::/41

Sampai di sini saya rasa cukup, untuk basic understanding bagaimana cara subnetting IPv6.  
IPv6 menawarkan banyak fitur yang tidak ada di IPv4, seperti fitur security contohnya. Jadi, migrasi jaringan ke IPv6 harusnya jadi prioritas.

Saya punya harapan penerapan IPv6 di Indonesia rate-nya bisa lebih tinggi lagi. Dimulai dari provider Internet atau content provider yang menerapkan jaringan IPv6, programmer network bisa menambahkan AF_INET6 disamping AF_INET, IPv6 diajarkan di Sekolah IT, dan seterusnya.

Dan terakhir kalau artikel ini dirasa membantu problem subnetting IPv6, silahkan di-share dan diteruskan ke mereka yang belajar dan baru mengenal IPv6.

**Artikel berkaitan:**  
["Hampir" Semua Tentang IPv6](//devnull.web.id/networking/pengenalan-ipv6.html)  
_Pengenalan dan Penjelasan IPv6, dari sejarah sampai pengalamatannya_

[Belajar Jaringan Komputer Dasar - Layer OSI 1, 2, dan 3](//devnull.web.id/networking/jaringan-komputer-dasar.html)  
_Teori yang harus diketahui oleh setiap network engineer. Layer OSI 1, 2, dan 3, paket Ethernet dan paket IP, serta proses routing paket IP._

**Refs:**

1. [1] RFC 5375 - Considerations for /64 Prefixes <https://tools.ietf.org/html/rfc5375#section-3.1>
2. [2] RFC 6164 - Using 127-Bit IPv6 Prefixes on Inter-Router Links <https://tools.ietf.org/html/rfc6164>
3. [3] RFC 3849 - IPv6 Address Prefix Reserved for Documentation <https://www.ietf.org/rfc/rfc3849>
