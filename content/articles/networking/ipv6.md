title: "Hampir" Semua Tentang IPv6
Author: Dhani Setiawan
Date: 2016-05-27 00:00
Category: Networking
Tags: networking, ipv6
Status: Published
Slug: pengenalan-ipv6


<div class="fimg">
    <img src="//devnull.web.id/images/networking/ipv6-logo.png" alt="World IPv6 Launch" title="World IPv6 Launch" />
    <p>Image: www.worldipv6launch.org</p>
</div>

Jaringan komputer awalnya dulu lahir di ARPANET (Advanced Research Projects Agency Network), ARPANET ini organisasi networking yang dibiayai sama Departemen Pertahanan Amerika Serikat <sup>[1]</sup> waktu itu.

Di ARPANET waktu itu, protokol komunikasi perangkat jaringan pakai protokol yang namanya NCP (Network Control Program). Terus di tanggal 1 Januari 1983, NCP ini dirubah ke protokol yang baru, namanya TCP/IP, Protokol baru pengganti NCP yang lebih baik. Transisi ini dikenal dengan "Flag Day" <sup>[2]</sup>.

Lahirnya protokol IP ini mulainya era Internet modern, protokol IP ini juga yang kita pakai sampai sekarang.

Awal-awal tahun 90-an waktu Internet mulai dipakai publik dan bukan lagi proyek militer, disini kelihatan kalau IPv4 address yang 4 milyar itu bakalan tidak cukup buat semua perangkat yang terhubung ke Internet nantinya.

&nbsp;

### Internet kehabisan IP Address
Begitu Internet ini dilepas ke publik, jaringan Internet ini jadi booming. Salah satu aplikasi Internet yang populer waktu itu yang sampai sekarang juga masih populer, seperti WWW (World Wide Web). Boomingnya Internet ini jadi masalah sendiri, IP address yang 4 milyar yang awalnya untuk militer itu begitu dipakai publik jadi kelihatan kalau ini nanti bakalan kurang.

Selain karena populernya Internet, ada satu hal lagi yang bikin Internet cepat sekali kehabisan IP address. Pada waktu itu, IP address dibagi menurut kelas-kelas, atau istilahnya Classful Network.

Kenapa ini jadi masalah? Mari kita lihat gambar ini.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/classful-network.png" alt="Classful Network" title="Classful Network" />
</div>

- Class A: 2<sup>24</sup> = 16.777.216 alamat.
- Class B: 2<sup>16</sup> = 65.536 alamat.
- Class C: 2<sup>8</sup> = 256 alamat.

Jadi di Classful Network, subnet bit kelipatan 8.

Ini masalahnya, kalau misalnya ada satu organisasi yang perlu 200 IP address, maka dia dialokasikan IP address kelas C yang isinya 256 IP address. Tapi kalau perlunya 500, dia dialokasikan address kelas B yang isinya 65 ribu ip address. Artinya? Itu berarti lebih dari 60 ribu IP address sia-sia tidak terpakai.

Tentu saja para engineer tidak tinggal diam melihat ini. Supaya borosnya IP address ini bisa direm sedikit, ada dua metode yang efektif dipakai; _Classless Inter-Domain Routing_ (CIDR) sama _Network Address Translation_ (NAT).

&nbsp;

##CIDR##
_Classless Inter-Domain Routing_ (CIDR), dibaca _"sidr"_ atau _"saidr"_. CIDR ini muncul di tahun 1993 menggantikan pembagian kelas-kelas IP address atau Classful Network di atas.<sup>[3]</sup> Jadi, seharusnya pembagian IP address berdasarkan kelas-kelas A, B, C, D, dan E itu sudah tidak dipakai dan diajarkan lagi. Kalau Anda ketemu tutorial yang mengajarkan kelas-kelas IP address, abaikan saja karena kemungkinan itu ditulis sebelum tahun 1993.

Lalu apa bedanya CIDR sama Classful Network?  
Kalau Classful Network subnet bit di kelipatan 8, CIDR subnet bitnya bisa di bit ke berapa saja.

Penulisan CIDR dengan menambahkan tanda ``slash (/)`` diikuti network bit, misalnya 192.168.0.1/24. 192.168.0.1/24 berarti 24 bit diawal adalah network, sisanya yang 8 bit host nya.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/cidr-24.png" alt="CIDR 24" title="CIDR 24" />
</div>

Nah kalau misalnya perlu IP address lebih dari 256, 300 misalnya; tidak perlu langsung ke bit 16 seperti class B, tapi cukup di bit ke 23, penulisannya 192.168.0.1/23.  
/23 menyisakan 9 bit untuk host, 9 bit ini maksimal bisa 510 host.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/cidr-23.png" alt="CIDR 23" title="CIDR 23" />
</div>

Atau /22 yang menyisakan 10 bit buat host. 10 bit berarti maksimal 1022 host.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/cidr-22.png" alt="CIDR 22" title="CIDR 22" />
</div>

Bahkan untuk subnet yang lebih kecil yang cuma perlu 10 IP address, kita bisa pakai /28 yang maksimal 14 IP address.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/cidr-28.png" alt="CIDR 28" title="CIDR 28" />
</div>

Jadi bedanya CIDR ini sama Classful Network, pakai CIDR subnet bisa di bit ke berapa saja tergantung kebutuhan, jadinya lebih hemat.

&nbsp;

##NAT
_Network Address Translation_ (NAT) ini juga salah satu cara penghematan IP address. Pakai NAT, satu IP address bisa dibagi ke banyak host.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/nat.png" alt="Network Address Translation" title="Network Address Translation" />
</div>

Di gambar itu ada 10 host tapi IP address yang dipakai buat koneksi Internet cukup dua saja, 1.1.1.1 dan 2.2.2.2. Dua IP address ini dipakai bersama oleh para host yang ada di belakang NAT.  
Host yang ada di belakang NAT, kita bebas pakai IP address private berapa saja karena IP address private tidak terlihat dari Internet. Di gambar itu juga ada host yang sama-sama punya IP address 192.168.0.2, tapi tidak masalah karena mereka ada di belakang NAT.

Kelemahan kalau pakai NAT, host yang ada di belakang NAT itu tersembunyi dari Internet. Jadi dari sudut pandang Internet, mereka ini tidak ada. Internet cuma bisa lihat IP address 1.1.1.1 dan 2.2.2.2 saja.

Ini biasanya bukan masalah kalau para host itu cuma perlu akses email atau browsing web. Tapi kalau seperti server yang IP addressnya harus terlihat dari Internet, NAT tidak bisa dipakai. Biarpun sekarang sudah ada cara-cara supaya NAT bisa dipakai buat server, tapi tetap saja caranya ribet dibanding tanpa NAT.

--
&nbsp;

Dua metode di atas, CIDR dan NAT sedikit bisa membantu mengurangi pemborosan IP address. Sedikit artinya IP address exhaustion tetap tidak bisa dihindari, cepat atau lambat IP address ini nantinya bakal habis juga.

Mereka para engineer di _Internet Engineering Task Force_ (IETF) sudah menyadari ini dari lama. Mereka kemudian merumuskan tipe IP baru yang jumlahnya banyak, IP baru ini namanya _Internet Protocol Next Generation_ (IPng) yang kemudian menjadi IPv6 yang kita kenal sekarang.

IPv6 adalah _Internet Protocol_ (IP) jenis baru penerus versi 4 yang hampir habis itu. Jadi sekarang Internet punya dua IP, IP yang lama disebut IPv4 dan IP yang baru disebut IPv6.

Tapi biarpun IPv4 sama IPv6 ini sama-sama IP, ternyata mereka ini berbicara dengan bahasa berbeda. IPv6 yang baru ini tidak bisa berkomunikasi dengan IPv4 yang lama.

&nbsp;

## Internet menjadi IPv6
Mengapa Internet perlu beralih ke IPv6?

1. IPv4 address cuma 32 bit atau 4 milyar, ini tidak cukup buat semua perangkat di dunia.
2. IPv6 lebih secure.
3. Metode routing IPv6 lebih efisien.
4. Tidak perlu alasan lagi.

IPv6 sepanjang 128 bit, jumlahnya 3,4x10<sup>38</sup>. Jumlah ini lebih dari cukup untuk semua bintang yang ada di langit, mungkin saja.  
Buat Anda yang tidak terbiasa dengan notasi ilmiah 3,4x10<sup>38</sup>, jumlah 2<sup>128</sup> adalah:

    340.282.366.920.938.463.463.374.607.431.768.211.456

Saya bahkan tidak tahu bagaimana cara membaca angka itu.

Jaringan IP adalah jaringan yang sangat tidak aman. Kalau kita akses Internet pakai protokol yang tidak terenkripsi, bisa jadi paket IP yang kita kirim dan terima itu dilihat, dimonitor, bahkan sampai level yang ekstrem paket IP itu dimodifikasi tanpa kita sadar. _Virtual Private Network_ (VPN) muncul karena adanya problem ini, VPN dipakai buat enkripsi paket IP.

Protokol IPSec<sup>[4]</sup> banyak dipakai buat VPN yang biasanya buat komunikasi kantor pusat dan cabangnya, atau buat komunikasi data yang sifatnya sensitif. Di IPv4, kalau mau pakai IPSec ini kita perlu konfigurasi tambahan di router atau host dan biasanya tidak gampang.

Di IPv6 IPsec ini bagian dari protokol, jadi kalau kita pakai IPv6 secara otomatis sudah pakai IPSec tanpa perlu konfigurasi apa-apa. Ini karena memang dari awalnya IPSec ini didesain untuk IPv6.

IPSec memastikan enkripsi paket IP secara end-to-end. Artinya paket itu dienkripsi oleh host pengirim, terus di-decrypt oleh penerima. Siapa saja diantara pengirim dan penerima tidak ada yang bisa melihat, merubah, atau mengacaukan paket IP itu.

Dari segi routing, IPv6 juga lebih efisien dibanding IPv4. Karena itu, routing IPv6 jadi lebih cepat.  
Di IPv4, setiap router yang melakukan forward paket IP harus menghitung IP checksum untuk memastikan paket yang diterima itu utuh dan tidak rusak. Di IPv6 tidak ada IP checksum, IPv6 mengatakan bahwa kewajiban pemeriksaan paket ada di layer di atasnya, bukan di IP.

Di protokol IP juga ada yang namanya packet fragmentation. Ini terjadi kalau paket yang akan dikirim lebih besar dari _Maximum Transmission Unit_ (MTU) di network interface. Jadi paket IP harus dipotong-potong jadi kecil supaya muat di MTU, terus potongan-potongan ini dikirim berulang-ulang sampai habis.  
Si penerima yang menerima paket yang terpotong-potong ini harus menunggu sampai semua potongan terkumpul, terus potongan-potongan itu digabungkan lagi jadi satu paket IP yang utuh.

Di IPv4, tugas memotong-motong paket dan menggabungkan paket ada di host dan router. Jadi, router sebelum meneruskan paket itu menunggu sampai semua potongan terkumpul terus menggabungkannya. Proses itu dilakukan semua router yang dilewati paket IP itu kalau MTU tidak cukup besar buat paket.

Kelebihan IPv6, IPv6 menangani packet fragmentation ini dengan lebih cerdas, router tidak ikut-ikutan memotong-motong paket IP. Misalnya router menerima potongan paket IPv6, router tidak menunggu tapi dia langsung teruskan potongan paket itu ke hop berikutnya. Begitu seterusnya sampai potongan paket itu diterima di host terakhir.

Host penerima yang terakhir inilah yang bertugas mengumpulkan potongan-potongan paket dan menggabungkannya jadi satu paket IPv6 yang utuh. Jadi proses fragmentasi itu ada di ujung-ujungnya saja. Dengan begini, proses routing lebih cepat dan efisien.

&nbsp;

## IPv6 Address
IPv6 address sepanjang 128 bit, ditulis dengan karakter Heksadesimal.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/ipv6.png" alt="IPv6 Address" title="IPv6 Address" />
</div>

Satu karakter heksadesimal itu sama dengan 4 bit biner, dan setiap 16 bit dipisahkan dengan titik dua.

Angka ``nol`` yang berdekatan bisa diringkas pakai dua titik dua ``(::)``, Misalnya ``2001:db8:0:0:82c1:6eff:fe59:2e43`` menjadi ``2001:db8::82c1:6eff:fe59:2e43``.  
Tapi kalau ada dua grup angka ``nol``, penulisan ringkas cuma bisa di salah satunya saja. Misalnya ``2001:db8:0:0:82c1:0:0:2e43`` bisa ditulis ``2001:db8::82c1:0:0:2e43`` atau ``2001:db8:0:0:82c1::2e43`` tapi tidak ``2001:db8::82c1::2e43``.


Seperti di gambar itu, IPv6 yang 128 bit itu dibagi 2. 64 bit yang awal adalah bit untuk network, 64 bit yang terakhir untuk host.

Penggunaan 64 bit untuk host ini diatur di RFC 5375<sup>[5]</sup>. Jadi di IPv6, tidak ada subnet lebih kecil dari /64. Misalnya di satu jaringan cuma ada 10 host, network yang dipakai tetap /64.

Ada satu pengecualian penggunaan network yang lebih kecil dari /64. Untuk link inter-router, link yang isinya cuma ada dua router dianjurkan pakai /127. Penggunaan /127 untuk link inter-router ditulis di RFC 6164<sup>[6]</sup>.

&nbsp;

**EUI-64**  
EUI-64<sup>[7]</sup> dipakai buat generate 64 bit host atau 64 bit terakhir IPv6 address berdasarkan MAC address. Cara penomoran alamat host bisa saja kita atur berurutan seperti waktu IPv4, alamat host 1, 2, 3 dan seterusnya, atau bisa acak diambilkan dari alamat MAC. Metode yang terakhir inilah yang namanya EUI-64.

Tapi ada problemnya, alamat MAC itu cuma 48 bit, host IPv6 64 bit. Supaya bisa jadi 64 bit, ditambahkan 16 bit angka hex ``0xfffe`` di tengah-tengah MAC address.

Selain itu, bit ke tujuh juga harus dirubah ke 1 supaya menandakan bahwa EUI-64 ini diatur secara lokal.

Saya pakai contoh buat EUI-64 dari MAC ``80:c1:6e:59:2e:43``. Step untuk membuat EUI-64 kurang lebih seperti di bawah:

**1) Ambil MAC address dan bagi dua.**  
MAC address dibagi jadi dua bagian, 24 bit _Organizationally Unique Identifier_ (OIU) dan 24 bit _Network Interface Card_ ID (NIC).

<div class="aimg">
    <img src="//devnull.web.id/images/networking/mac-addr.png" alt="MAC Address" title="MAC Address" />
</div>

**2) Tempatkan 16 bit hex ``0xfffe`` di tengah-tengah MAC address.**  

<div class="aimg">
    <img src="//devnull.web.id/images/networking/fffe.png" alt="eui-64" title="eui-64" />
</div>

**3) Rubah bit ke 7 ke angka 1 untuk menandakan universal atau local.**  
Setiap MAC address yang terdaftar dan di-assign oleh _Institute of Electrical and Electronics Engineers_ (IEEE), bit ke 7 pasti ``0`` yang menandakan bahwa ini alamat yang universal. Di EUI-64, bit ke 7 ini harus dirubah ke ``1`` yang menandakan bahwa alamat ini diadministrasi secara lokal.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/ul.png" alt="eui-64" title="eui-64" />
</div>

Jadinya, 64 bit host EUI-64 dari MAC address ``80:c1:6e:59:2e:43`` adalah ``82c1:6eff:fe59:2e43``. Tinggal digabungkan dengan 64 bit networknya, untuk link-local misalnya ``fe80::82c1:6eff:fe59:2e43``.

Sebenarnya EUI-64 ini kerjaannya software, bukan orang. Di OS router misalnya, kalau kita set EUI-64 software yang bakal hitung sama setting itu. Di OS modern seperti Linux juga, EUI-64 ini juga otomatis ter-set tanpa ada campur tangan user.

Tapi biarpun begitu, saya rasa tidak ada salahnya kan memahami teori dibalik EUI-64 ini?

&nbsp;

## Tipe IPv6 address
Sama seperti IPv4, IPv6 address juga dibagi ke beberapa tipe <sup>[8]</sup> di bawah:

1. Unicast.
2. Multicast.
3. Anycast.

### Unicast
IPv6 Unicast address adalah tipe IPv6 address yang dipakai buat komunikasi satu lawan satu. Misalnya Anda ngobrol berdua dengan teman Anda secara privat, jenis obrolan seperti ini kalau di protokol IP namanya unicast.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/unicast.png" alt="IPv6 Unicast" title="IPv6 Unicast" />
</div>

Dalam obrolan unicast, pihak yang tidak berkepentingan tidak bisa mendengar obrolan itu, apalagi ikut menjawab.

Di IPv6, unicast address ini dibagi lagi jadi tiga, _Global Unicast Address_, _Link-local Address_, sama _Unique Local Address_.

**A) Global Unicast Address**  
Global Unicast Address ini jenis IPv6 unicast yang dipakai buat komunikasi di Internet, kalau di IPv4 namanya ip address publik. Ini jenis IP address yang diatur sama _Regional Internet Registry_ (RIR). Kalau kita di Indonesia, yang kelola IP address jenis ini ada di APNIC, RIR untuk wilayah Asia Pasifik.

APNIC alokasikan alamat IPv6 tipe ini ke organisasi sama ISP, terus para ISP ini mendistribusikan IPv6 address ini ke pelanggan-pelanggan mereka.  
Untuk di awal, biasanya alokasi IPv6 address untuk ISP sebanyak /32.

**B) Link-local Address**  
Link-local address dipakai buat komunikasi unicast yang sifatnya lokal dan cuma sebatas link, jadi link-local ini tidak bisa melewati router. Block alamat IPv6 address yang dialokasikan untuk jenis ini adalah ``fe80::/10``.

Beda sama IPv4, kalau di IPv6 link-local ini wajib ada di setiap interface, IPv6 bakalan tidak berfungsi kalau jenis link-local ini tidak ada.  
IPv6 address jenis ini biasanya di-set secara otomatis oleh OS pakai EUI-64, jadi user tidak perlu konfigurasi apa-apa.

Kalau Anda punya mesin Linux yang modern, bisa dicek pakai command ``ip``.

    # ip addr show wlan0
    3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
        link/ether 18:4f:32:59:88:33 brd ff:ff:ff:ff:ff:ff
        inet 10.10.10.11/28 brd 10.10.10.15 scope global wlan0
            valid_lft forever preferred_lft forever
        inet6 2xxx:exxx:0:a:1a4f:32ff:fe59:8833/64 scope global mngtmpaddr dynamic 
            valid_lft 7180sec preferred_lft 1780sec
        inet6 fe80::1a4f:32ff:fe59:8833/64 scope link 
            valid_lft forever preferred_lft forever

IPv6 yang paling bawah ``fe80::1a4f:32ff:fe59:8833/64`` dengan scope link itu alamat link-local.

IPv6 address jenis ini dipakai buat neighbor discovery, buat cari tahu ada router atau tidak, kalau ada router dimana alamat IPv6 nya. IPv6 address jenis ini juga dipakai protokol dynamic routing OSPFv3. Jadi IPv6 address unicast yang jenis ini penting sekali.

**C) Unique Local Address**  
Kalau di IPv4 kita punya blok private IP address, salah satunya seperti ``192.168.0.0/16`` yang kita bebas pakai di mana saja, di IPv6 juga ada. Alokasi IPv6 address untuk unicast jenis ini adalah ``fc00::/7``. Jadi buat jaringan yang sifatnya lokal, kita bisa pakai IP address jenis ini.

Tapi ada bedanya sama IPv4, IPv6 address jenis ini tidak bisa dipakai buat Internet, cuma bisa lokal saja. Jadinya router kalau terima paket dari IPv6 address jenis ini, dia tidak mau meneruskan paket kalau tujuannya jenis Global Unicast, tapi paket diforward kalau tujuannya juga jenis Unique Local.

Dulu ada satu lagi jenis unicast address, namanya site-local dengan blok address ``fec0::/10``. Tapi jenis yang ini tidak lagi dipakai dan digantikan Unique Local.

&nbsp;

### Multicast
Multicast adalah metode komunikasi one-to-many dan many-to-many, multicast ini ada grup-grup. Misalnya kalau Anda ngobrol sama sekelompok orang di satu ruangan, komunikasi ini namanya multicast. Mungkin di ruangan itu juga ada kelompok yang lain lagi, tapi karena Anda tidak bicara sama mereka, grup itu juga tidak akan merespon Anda. Jadi cuma grup yang dituju saja yang merespon.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/multicast.png" alt="IPv6 Multicast" title="IPv6 Multicast" />
</div>

Jenis komunikasi multicast ini banyak dipakai buat tv broadcasting atau streaming. Pakai multicast, server tidak perlu buat banyak koneksi secara bersamaan, cukup satu koneksi saja.

Di IPv6, blok untuk alamat multicast adalah ``ff00::/8``.

&nbsp;

### Anycast  
Kalau multicast ke satu grup, anycast ke salah satu member dari grup.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/anycast.png" alt="IPv6 Anycast" title="IPv6 Anycast" />
</div>

Paket IP yang ditujukan ke alamat anycast akan dikirim ke salah satu member dari grup anycast itu, tidak semua.

Contoh penggunaan anycast misalnya di DNS root server. Root server ini di dunia ada 13 alamat IP nya, tapi jumlah fisiknya lebih dari itu.

Misalnya kita query dns ke salah satu root server ``a.root-servers.net`` yang IPv6 address-nya ``2001:503:ba3e::2:30``. User di belahan dunia lain yang juga query ke alamat IPv6 ``2001:503:ba3e::2:30 `` bisa jadi servernya tidak sama dengan kita biarpun IPv6 address-nya sama-sama ``2001:503:ba3e::2:30``.

Jadi, IP address anycast ini adalah IP address yang sama tapi ditempatkan di node yang berbeda. Paket IP yang ditujukan ke alamat anycast akan dikirim ke salah satu saja dari grup anycast dan biasanya yang paling dekat.

IPv6 anycast ini juga bisa dipakai buat failover kalau misalnya salah satu node down, bisa digantikan yang lain secara otomatis.

&nbsp;

## Apa yang tidak ada di IPv6?
Bukan cuma ada penambahan, di IPv6 juga ada pengurangan.

**Broadcast**  
Tidak ada lagi komunikasi broadcast di IPv6, begitu juga tidak ada IPv6 address jenis broadcast. Broadcast ini komunikasi satu ke banyak. Kalau unicast Anda ambil ponsel dan telepon ke orang yang dituju, tapi kalau broadcast Anda ambil speaker supaya orang satu RT bisa dengar semua.

Di IPv6, broadcast tidak ada tapi diganti sama multicast.

**NAT**  
Dengan jumlah IP address sebanyak 3,4x10<sup>38</sup>, apakah kita masih perlu NAT? tentu saja tidak.

Setiap perangkat yang terhubung ke Internet, apakah itu server, desktop, laptop sampai smartphone kalau terhubung lewat IPv6 semua terekspos ke Internet.

Mungkin juga ada yang berpendapat dengan tidak adanya NAT, perangkat yang ber-IPv6 itu jadi tidak aman karena terekspos ke Internet.  
Ini mungkin betul tapi juga salah. NAT, biarpun bisa menyembunyikan host di belakangnya tapi NAT ini bukanlah firewall, jadi jangan dianggap NAT ini seperti firewall.

Jadi biarpun perangkat yang pakai IPv6 terekspos ke Internet, ini tanggung jawab administrator bagaimana mengatur firewall IPv6 supaya bisa secure.

&nbsp;

## Conclusion

Mungkin, mungkin saja IPv6 ini terlihat lebih horor daripada IPv4. Ini juga yang dulu saya pikirkan, dan Saya yakin banyak yang sependapat. Alasannya mungkin saja karena:

1. 128 bit, ini panjang sekali.
2. Ditulis pakai heksadesimal, angka yang saya tidak pernah diajarkan waktu di SD.
3. Karena bukan IPv4.

Tapi apakah benar IPv6 ini susah?  
Coba kita lihat kenapa Luke Skywalker gagal mengangkat pesawat X-wing.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/yoda.png" alt="Yoda" />
    <p style="font-size:13px;color:#a4a4a4;">Image source: picturequotes.com</p>
</div>

Karena menurutnya, X-wing itu terlalu besar.

&nbsp;

**Refs:**

1. [Wikipedia - ARPANET](https://en.wikipedia.org/wiki/ARPANET)
2. [Wikipedia - Network Control Program - Transition to TCP/IP](https://en.wikipedia.org/wiki/Network_Control_Program#Transition_to_TCP.2FIP)
3. [Wikipedia - Classful Network - Replacement of classes](https://en.wikipedia.org/wiki/Classful_network#Replacement_of_classes)
4. [IETF - IPSec](https://www.ietf.org/rfc/rfc2401.txt)
5. [IETF - RFC5375](https://tools.ietf.org/html/rfc5375#section-3.1)
6. [IETF - RFC6164](https://tools.ietf.org/html/rfc6164)
7. [IETF - RFC4291  Appendix A - EUI-64](http://tools.ietf.org/html/rfc4291#appendix-A)
8. [CIDR Report - Reserved IPv6 Address](http://www.cidr-report.org/v6/as2.0/reserved-ipv6.html)

&nbsp;

**Artikel Berkaitan:**  
[Subnetting IPv6 bisa semudah IPv4, bahkan lebih mudah.](//devnull.web.id/networking/subnetting-ipv6-mudah.html)  
_Cara menghitung subnetting IPv6 dengan mudah._
