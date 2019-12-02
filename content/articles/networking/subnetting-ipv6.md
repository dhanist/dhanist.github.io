Title: Subnetting IPv6 bisa semudah IPv4, bahkan lebih mudah.
Date: 2017-10-18 13:55
Author: Dhani Setiawan
Category: Networking
Tags: IPv6
Slug: subnetting-ipv6-mudah
Status: published
Comments: yes

<div class="fimg">
    <img src="//devnull.web.id/images/networking/ipv6/fimg.jpg" alt="IPv6 Ready" title="IPv6" />
    <p>Image: ipv6forum.com</p>
</div>

Halo teman-teman pembaca, ini revisi tulisan saya sebelumnya tentang subnetting IPv6. Di tulisan sebelumnya ada sedikit kesalahan yang perlu saya koreksi, terima kasih kepada pembaca yang sudah mengoreksi.

Jadi, ini dia.. sebut saja Subnetting IPv6 edisi revisi atau Subnetting IPv6 v2. :)

Di tulisan sebelumnya ada beberapa rumus, tapi di tulisan yang ini saya pakai lebih banyak gambar yang mungkin saja lebih memudahkan.

Saya berasumsi teman-teman yang membaca ini sudah paling tidak sedikit memahami apa itu IPv6, perbedaannya dengan IPv4, penulisannya, dsb. Tapi kalau ternyata belum ngeh apa itu IPv6, jangan belajar subnetting dulu tapi baca artikel yang ini ["Hampir" Semua Tentang IPv6](http://devnull.web.id/networking/pengenalan-ipv6.html)

<br />

Baik, sebelum ke cara subnetting saya tulis lagi apa-apa saja yang perlu diketahui di IPv6.

<br />

## IPv4 dan IPv6
Saya masih menemui ada teknisi jaringan yang beranggapan bahwa IPv4 dan IPv6 sama, hanya saja IPv6 jumlah IP address nya lebih banyak dari IPv4 dan penulisan alamatnya berbeda.  
Tidak benar, IPv4 dan IPv6 tidak sama. IP (Internet Protocol), ada kata protokol di situ. Protokol itu satu set aturan yang sudah dirumuskan dan disepakati bersama.  
Jadi apa pun perangkat jaringannya selama dia perangkat IP di layer 3, entah itu server, router, atau smartphone, mereka berbicara dengan bahasa yang sama, bahasa IP atau protokol IP.  
Nah protokol IP saat ini di ada dua, protokol versi 4 (IPv4) dan protokol versi 6 (IPv6). Keduanya ini biarpun masih sama-sama IP tapi bahasanya sudah berbeda, jadi tidak kompatibel satu sama lain.

Kemudian di IPv4, kita terbiasa subnetting sampai bit terpanjang, misalnya /30 dari IPv4 yang 32 bit.  
Di IPv6, rule nya beda. IPv6 sepanjang 128 bit, tapi subnet terkecil cuma sampai /64. Artinya dari bit ke 65 sampai bit ke 128 jadi alamat host, tidak ada subnetting /72 atau /96.<sup>[1]</sup>  
Jadi IPv6 itu /64 everywhere, biarpun network isinya cuma 10 host, tetap /64 yang dipakai. Tapi ada pengecualian untuk link inter-router, satu network yang isinya dua router. Untuk yang ini dipakai /127.<sup>[2]</sup>

Lagi, di IPv4 biasanya kalau subnetting yang diingat itu alamat pertama network, alamat terakhir broadcast, ditengah-tengah alamat unicast atau alamat untuk host.  
Di IPv6, tidak ada broadcast, jadi alamat terakhir bisa dipakai untuk host.

<br />

## Subnetting IPv6
Saya rasa kita punya masalah yang sama kalau berurusan sama IPv6, bilangan hex. Kita, atau paling tidak saya terbiasa pakai desimal, heksadesimal kelihatannya asing dan sulit.

Tapi sesuai judulnya, subnetting IPv6 bisa lebih mudah dari IPv4. Bagaimana bisa?  
Karena penulisannya pakai hex, itu yang bikin gampang. Iya, jadi hex itu malah mempermudah, karena subnetting itu tidak lepas dari bit bilangan biner, sedangkan satu karakter heksadesimal sama dengan 4 bit biner.  

Saya ulangi lagi, _**Satu karakter heksadesimal sama dengan 4 bit biner**_  

Contoh biner ``11111111`` kalau di desimal ditulis ``255`` tapi di hex ditulis ``ff`` atau ``0xff``

Dengan gambar mungkin bisa lebih dipahami.

**Gambar 1.**
<div class="aimg">
<img src="//devnull.web.id/images/networking/ipv6/ipv6.png" title="IPv6" alt="IPv6" />
</div>

Kita pakai prefix ``2002:db8:abcd:dead::/64`` di contoh ini. Prefix ini, ``2001:db8::/32`` memang dikhususkan untuk dokumentasi, tutorial, dsb. <sup>[3]</sup>

Keterangan gambar di bawah:

- Notasi Hex IPv6: Ini prefix IPv6 yang kita pakai untuk contoh.
- Nomor Hex: Nomor kolom karakter heksadesimal.
- Jumlah bit: Panjang bit di kolom hex ke sekian. Misal hex ``2001``, karena ``2001`` ada 4 kolom, panjang bit nya adalah 16, di notasi biner ditulis seperti ini ``0010 0000 0000 0001``. Paham? Jadi hex ke biner nya seperti ini ``2=0010, 0=0000, 0=0000, 1=0001``, satu hex sama dengan 4 bit biner.

Kalau sudah bisa dipahami, kita ambil contoh.  
Network ``2001:db8::/32``, bagi ke jaringan kecil ``/34``.  
Dari sini ada beberapa istilah di bawah:

- Network: di contoh ini ``2001:db8::/32`` Ini network besarnya, artinya ``/32``, bit dari ``33`` sampai ``128`` punya kita dan bisa diatur semau kita, sedangkan bit ``1`` sampai bit ``32`` bukan punya kita dan tidak bisa kita rubah.
- Sub network atau subnet: subnet ini cabang dari network. Di contoh ini ``/34``

Lebih jelasnya seperti gambar di bawah:

<div class="aimg">
<img src="//devnull.web.id/images/networking/ipv6/ipv6-subnetting.png" title="IPv6 Subnetting" alt="Subnetting IPv6" />
</div>

Jadi subnetting itu membagi network ke sub network atau subnet.  

Nah pertanyaan di subnetting kan biasanya, berapa jumlah subnet, apa saja subnet-nya, berapa jumlah host, dsb.

Baik, saya perkenalkan variabel lagi:

**Jumlah subnet (y):** kita sebut saya jumlah subnet dengan ``y``. Cara menghitungnya, ``2 ^ (subnet - network)``. Di contoh ini network /32 dibagi ke subnet /34. Jadi ``2 ^ 34-32 = 2 ^ 2 = 4``.  
Lihat lagi gambar di atas, network /32 kalau dibagi ke /34, jadinya 4 subnet /34. Jadi ``y = 4``.

**Jumlah host dalam subnet:** Gampang, ``2 ^ 128 - subnet``. Di contoh berarti ``2 ^ 128-34 = 2 ^ 94``. Silakan dihitung berapa hasil 2 pangkat 94.

**Alamat subnet:** Ini yang agak tricky. Untuk menghitung alamat subnetnya, kita perlu beberapa variabel.  
- _Nomor kolom hex (x)_. Kembali ke gambar pertama, ``x`` ini nomor kolom di bit subnet. Di contoh ini bit subnet 34, jadi ``x`` atau nomor kolom di kolom 9.  
Kenapa nomor 9? karena, ingat lagi satu hex = 4 bit biner, dan kolom nomor 9 ada 4 bit dari bit ke 33 sampai 36.

<div class="aimg">
<img src="//devnull.web.id/images/networking/ipv6/ipv6-cols.png" title="IPv6" alt="IPv6" />
</div>

- _Kelipatan subnet (z)_. ``z`` ini dipakai untuk menghitung subnet selanjutnya. Di contoh, /32 dibagi ke /34 dan hasilnya ada 4 subnet /34. Jadi untuk mengetahui subnet /34 pertama, /34 ke dua, ke tiga, dan ke empat, caranya nomor kolom **(x)** ditambah kelipatan subnet **(z)** sama dengan subnet berikutnya.

<div class="aimg">
<img src="//devnull.web.id/images/networking/ipv6/ipv6-inc.png" title="IPv6" alt="IPv6" />
</div>

Perhatikan gambar di atas, jadi setiap kolom ada 4 bit, dan bit ini diberi nomor 1 sampai 4. Kalau bit subnet ada di nomor bit 1, maka kelipatan subnet berikutnya dengan menambahkan 8, _z = 8_, kalau di nomor 2, maka _z = 4_, nomor 3 _z = 2_ dan kalau di nomor 4 maka _z = 1_.  
Jadi untuk menghitung subnet berikutnya nomor kolom **(x)** ditambah **(z)**.

Di contoh ini, network ``2001:db8::/32`` dibagi ke subnet /34, kita bisa terapkan perhitungannya.

- ``x`` nomor kolom. /34 ada di kolom 9.
- ``y`` atau jumlah subnet = 4. ``2 ^ 34-32 = 2 ^ 2 = 4``.
- ``z`` kelipatan. /34 ada di nomor bit ke 2, jadi ``z = 4``.

Jadi, tambahkan nomor kolom ``x (9)`` dengan kelipatan ``z (4)`` sampai jumlah subnet ``y`` sama dengan 4.

    2001:0db8::/32
    - 1. 2001:0db8:0000::/34 atau bisa ditulis 2001:db8::/34
    - 2. 2001:0db8:4000::/34
    - 3. 2001:0db8:8000::/34
    - 4. 2001:0db8:c000::/34

<br />

Kita lanjut dengan contoh lain.


**Contoh 1.**  
Diberikan network 2001:db8::/32, subnetting ke jaringan kecil /36. Berapa jumlah subnet, dan apa saja networknya?  

- ``x`` nomor kolom. /36 ada di kolom 9.
- ``y`` atau jumlah subnet = 16. ``2 ^ 36-32 = 2 ^ 4 = 16``.
- ``z`` kelipatan. /36 ada di nomor bit ke 4, jadi ``z = 1``.

Jadi, tambahkan nomor kolom ``x`` dengan kelipatan ``z`` sampai jumlah subnet ``y`` sama dengan 16.

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

<br />

**Contoh 2.**  
Dari network 2001:db8:c000::/34, bagi ke dalam 3 jaringan kecil.  

Bisa kah?  
Tidak bisa, kita pelu ingat bahwa ``y``, atau jumlah subnet adalah pangkat 2. Yaitu 1, 2, 4, 8, 16, 32, 64, dan seterusnya. Jadi membagi jaringan kedalam 3 jaringan kecil itu tidak bisa. Bisanya, kita ambil yang mendekati tapi tidak lebih kecil. Yang mendekati 3 tapi tidak lebih kecil dari 3 adalah 4, atau 2<sup>2</sup>.

Jadi, kita akan bagi ``2001:db8:c000::/34`` kedalam 4 subnet kecil, atau y = 4.

    network = 34
    subnet  = tidak diketahui
    y       = 4

    Kita cari subnet dengan sedikit aljabar.

                y  = 2 ^ subnet - network
                4  = 2 ^ subnet - 34
     (subnet - 34) = akar 4
     (subnet - 34) = 2
            subnet = 34 + 2
            subnet = 36

    Jadi,
     network = 34
     subnet  = 36
           y = 4

- ``x`` nomor kolom. /36 ada di kolom 9.
- ``y`` atau jumlah subnet = 4. ``2 ^ 36-34 = 2 ^ 2 = 4``.
- ``z`` kelipatan. /36 ada di nomor bit ke 4, jadi ``z = 1``.

<br />

    Hitung dari kiri ke kanan, x atau karakter ke 9 heksadesimal kita tambahkan dengan 1, karena z = 1. Ulangi terus sampai y = 4.
    
    ======================
    y   subnet
    ======================
    1   2001:0db8:c000::/36 atau bisa ditulis 2001:db8:c000::/36
    2   2001:0db8:d000::/36
    3   2001:0db8:e000::/36
    4   2001:0db8:f000::/36

<br /> 

**Contoh 3.**  
Di dalam network 2001:db8:e000::/36, berapa jumlah host yang ada di network tersebut, berapa alamat ip host pertama dan berapa alamat ip host terakhir?  
Karena IPv6 sepanjang 128 bit, maka jumlah host untuk /36 adalah:
    
    2 ^ 128-36
    2 ^ 92
    4.951.760.157.000.000.000.000.000.000

Saya tidak tahu bagaimana menyebut angka diatas.

Dalam network 2001:db8:e000::/36, host awal dan terakhir sbb:

    host pertama  : 2001:db8:e000:0000:0000:0000:0000:0001 atau bisa ditulis 2001:db8::1
    host terakhir : 2001:db8:efff:ffff:ffff:ffff:ffff:ffff

Mengapa host terakhir ``2001:db8:efff:ffff:ffff:ffff:ffff:ffff``?  
Karena alamat ini kalau ditambahkan 1 sudah masuk subnet /36 berikutnya yang alamat subnetnya ``2002:db8:f000::/36``, dan alamat host terakhir ini bukan alamat broadcast karena tidak ada broadcast di IPv6.

<br />

**Contoh terakhir, contoh ke 4.**  
Bagi network 2001:db8:e000::/36 ke subnet /41.

Silahkan dihitung, kemudian bandingkan hasilnya dengan yang di bawah.

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

<br />

Contoh sudah selesai, sekarang **kuis**  
Saya punya network ``2001:db8::/32``. Kemudian saya delegasikan 1 prefix /48 ke teman-teman. Prefix network-nya ``2001:db8:abcd::/48``.
Saya minta teman-teman bagi prefix network ini ke /56.

Pertanyaan saya, berapa jumlah subnet nya, dan apa saja alamat subnet nya.

---

Baik saya rasa cukup, silakan kalau ada yang kurang jelas atau ada yang perlu dikoreksi lagi bisa tuliskan di komen.
Jangan lupa bantu share kalau artikel ini membantu pemahaman subnetting IPv6.

<br />

**Artikel berkaitan:**  
["Hampir" Semua Tentang IPv6](//devnull.web.id/networking/pengenalan-ipv6.html)  
_Pengenalan dan Penjelasan yang berusaha biarpun gagal tapi lumayan komprehensif tentang IPv6, dari sejarah sampai pengalamatannya ditulis dengan Layman's terms_

[Belajar Jaringan Komputer Dasar - Layer OSI 1, 2, dan 3](//devnull.web.id/networking/jaringan-komputer-dasar.html)  
_Teori yang harus diketahui oleh setiap network engineer. Layer OSI 1, 2, dan 3, frame Ethernet dan paket IP, serta proses routing paket IP._

**Refs:**

1. [1] RFC 5375 - Considerations for /64 Prefixes <https://tools.ietf.org/html/rfc5375#section-3.1>
2. [2] RFC 6164 - Using 127-Bit IPv6 Prefixes on Inter-Router Links <https://tools.ietf.org/html/rfc6164>
3. [3] RFC 3849 - IPv6 Address Prefix Reserved for Documentation <https://www.ietf.org/rfc/rfc3849>
