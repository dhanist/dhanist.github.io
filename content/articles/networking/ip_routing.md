Title: Jaringan Layer 3, IP routing
Date: 2019-12-1 09:45
Author: Dhani Setiawan
Category: Networking
Slug: jaringan-layer-3
Status: published
Comments: yes


Selamat datang teman-teman pembaca. Saya meneruskan tulisan yang lama tentang
jaringan layer 1, 2, dan 3. Saya lihat demand tulisan itu lumayan bagus, jadi
saya terpikir buat sedikit lebih dalam membahas apa yang terjadi di layer 3.

Layer 3 ini di standar OSI dinamakan network layer dan di layer ini ada beberapa
protokol yang berjalan, salah satunya yang paling populer dan hanya
itu yang akan saya bahas, yaitu IP atau Internet Protocol. IP ini yang sekarang
kita pakai buat akses web, sosial media, email, dll.

Sebelum kita bahas IP dan proses routing-nya, saya mau kita samakan persepsi
dulu tentang IP supaya tidak membingungkan. Jadi kalau saya sebut IP, yang saya
maksud bukan seperti 192.168.1.1, ini bukan IP, tapi ini alamat IP atau IP address.

Jadi apa itu IP?  
IP atau Internet Protocol bisa kita bayangkan seperti Bahasa
Indonesia, satu bahasa yang dimengerti semua suku di Indonesia, kecuali mungkin
yang di pedalaman. Itulah IP, satu bahasa atau protokol yang dimengerti semua
perangkat layer 3 apapun jenis dan merek nya. Smartphone, PC, Laptop, server dan
router yang jenis dan mereknya berbeda-beda itu, tapi mereka semua mengerti satu
bahasa, bahasa IP.

Kemudian di dalam IP ini ada yang namanya alamat IP dan paket IP. Alamat IP,
sama seperti alamat pada umumnya, ini informasi di mana perangkat IP
ini lokasinya, tidak ditulis dengan nama jalan tapi pakai notasi
192.168.1.100 misalnya.

Paket IP, sama seperti paket umumnya, ada
alamat IP pengirim, ada alamat IP penerima, ada isi paket yang dalam
bahasa IP disebut Payload. Payload ini bisa berisi data TCP misalnya,
yang kalau kita akses web atau email kita pakai TCP.
Payload bisa juga berisi UDP yang kalau kita request DNS pakai UDP.
Bisa juga berisi ICMP yang biasanya kita kirim pakai program PING.
Atau bahkan IP payload ini bisa berisi paket IP, IP dalam IP yang biasa disebut
IP tunnel.

&nbsp;

##Proses routing IP

Nah sekarang, setelah paham apa itu IP, kita bahas masalah routing IP.  Apa itu?
proses routing IP ini, cara bagaimana satu paket IP dari alamat pengirim bisa
sampai di alamat IP penerima, melewati beberapa atau banyak IP forwarder yang
disebut router.

Router-router ini bertugas menerima paket dari pengirim atau
dari router lainnya, kemudian meneruskan ke router lain atau menyerahkan paket
IP tersebut ke penerima kalau dia yang terhubung ke alamat penerima atau dia router
yang terakhir. Bayangkan pengiriman paket lewat jasa ekspedisi yang melewati
beberapa pos transit sebelum sampai ke penerima, pos-pos ini fungsinya sama
dengan router.

Kemudian bagaimana cara sebuah router menentukan jalur yang harus dilewati
paket IP? seperti sebuah rumah yang punya beberapa pintu, paket IP ke tujuan
tertentu harus lewat pintu mana? salah jalur maka paket tidak bisa sampai
tujuan.

Di sinilah peran routing protocol, routing protocol menentukan jalur A
untuk tujuan alamat IP A, dan jalur B untuk tujuan B, dst. Dan setelah
diputuskan jalurnya, informasi ini dicatat di sebuah database yang disebut
routing table atau _routing information base (RIB)_. Ya, jadi masing-masing router
punya data informasi routing table, jadi waktu ada paket masuk, dilihat
tujuannya dan alamat tujuan ini dicari di data routing table dan setelah didapat
jalurnya, paket IP diteruskan lewat jalur itu.

&nbsp;

##Routing Protocol

Secara garis besar, routing protocol dibagi jadi tiga. _Link_ atau _Connected_,
_static routing_, dan _dynamic routing_. Kita bahas satu-satu.

####Connected / Link.

Link atau juga disebut connected routing, ini informasi router dalam satu
broadcast domain.
Informasi routing yang otomatis terbuat kalau kita assign ip address di
interface router. Misal router A punya 2 interface, eth0 dan eth1. Kita
set ip address 192.168.1.1/24 di eth0, maka secara otomatis router akan
membuat informasi routing bahwa network 192.168.1.0/24 lewat eth0.
Informasi ini kemudian disimpan di data routing table.

    :::console
    [root: ~] Endor # ip route
    default via 10.10.10.28 dev eth0
    10.10.10.0/24 dev eth0 proto kernel scope link src 10.10.10.96
    [root: ~] Endor # ip addr add 192.168.1.1/24 dev eth0
    [root: ~] Endor # ip route
    default via 10.10.10.28 dev eth0
    10.10.10.0/24 dev eth0 proto kernel scope link src 10.10.10.96
    192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.1
    [root: ~] Endor #

Seperti terlihat di atas, routing 192.168.1.0/24 otomatis terbuat waktu saya set
ip address 192.168.1.1/24 di interface eth0.

&nbsp;

####Static routing protocol

Static routing protocol. Protokol ini diset secara manual oleh administrator
jaringan. Jadi misal saya mau informasikan ke router A di atas bahwa tujuan
alamat 172.16.1.0/24 lewat 192.168.1.100, maka saya harus secara manual inputkan
data ini ke router, baru kemudian router tulis data ini ke routing table. Maka
ketika ada paket masuk router A dengan tujuan 172.16.1.1 misalnya, router A cek
routing table dan ternyata 172.16.1.1 masuk ke network 172.16.1.0/24.

Berdasarkan informasi routing table bahwa 172.16.1.0/24 harus lewat
192.168.1.100, maka paket ini akan diteruskan ke 192.168.1.100.<br />
Tapi di mana router 192.168.1.100 ini? sekali lagi router A cek routing
table dan didapat bahwa 192.168.1.100 masuk network 192.168.1.0/24 dan
192.168.1.0/24 lewat interface eth0.

Dan itulah yang terjadi, paket dengan
tujuan 172.16.1.1 diteruskan ke 192.168.1.100 lewat interface eth0.

    :::console
    [root: ~] Endor # ip route show
    default via 10.10.10.28 dev eth0
    10.10.10.0/24 dev eth0 proto kernel scope link src 10.10.10.96
    192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.1
    [root: ~] Endor #
    [root: ~] Endor # ip route add 172.16.1.0/24 via 192.168.1.100
    [root: ~] Endor #
    [root: ~] Endor # ip route show
    default via 10.10.10.28 dev eth0
    10.10.10.0/24 dev eth0 proto kernel scope link src 10.10.10.96
    172.16.1.0/24 via 192.168.1.100 dev eth0
    192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.1
    [root: ~] Endor #

Satu, dua, atau sepuluh informasi routing masih oke, tapi bagaimana kalau saya
punya ratusan atau bahkan ribuan network yang melibatkan banyak sekali router?
di sinilah peran dynamic routing protocol.

&nbsp;

####Dynamic Routing Protocol

Dynamic routing ini protokol routing yang kita tidak perlu input satu-satu
entri routing secara manual. Misal saya punya 100 router yang saling
terhubung, saya input routing di router ke 100, maka secara otomatis 99 router
yang lainnya akan meng-update data routing table mereka tanpa intervensi manual.

Di sini saya bahas 2 saja untuk dynamic routing, **Border gateway protocol (BGP)**
dan **Open Shortest Path First (OSPF)**. Dua protokol ini yang paling banyak
dipakai di jaringan yang besar. BGP dan OSPF akan kita bahas nanti.

Dynamic routing protocol, seperti yang sudah disebutkan, dia didesain buat
memudahkan administrasi routing. Pakai dynamic protocol, admin jaringan bisa
me-manage banyak sekali router tanpa takut looping.

Routing loop ini misalnya router A mengatakan tujuan C harus lewat router B,
sementara router B mengatakan tujuan C harus lewat router A. Jadinya paket IP
ke C cuma bolak balik antara router A sama B, tidak bisa sampai C.

Looping ini sangat mungkin dan umum terjadi di jaringan yang pakai static routing, karena
admin yang salah setting static route. Nah dynamic routing menjamin routing
yang bebas loop, biarpun banyak sekali router yang terlibat di jaringan.

&nbsp;

##Administrative Distance (AD)

Di satu router, bisa saja ada beberapa routing protocol yang jalan, tapi entri
di routing table cuma ada satu yang bisa aktif dan inilah yang jadi rujukan
router buat memproses pengiriman paket IP. Maksudnya begini, kalau misalnya ada
dua atau lebih routing protokol menulis ke routing table untuk tujuan yang sama,
misal saja ada connected untuk tujuan 10.10.10.0/24 lewat eth0, ada juga routing
yang sama dari protokol static untuk route 10.10.10.0/24.

Nah di routing table bakal ada dua entri untuk route yang sama, 10.10.10.0/24.
Tapi yang aktif cuma bisa satu, dan penentuan jalur ini berdasarkan rangking
yang disebut _administrative distance_, semakin kecil nilai distance, dia yang
akan dipilih.

Pengecualian buat _Equal Cost Multipath_ atau **ECMP** dimana beberapa jalur bisa aktif
bersamaan, tapi ini teknik yang agak advance.

Secara default distance untuk masing-masing protokol:

- **Connected / Link  : 0**
- **Static            : 1** dan bisa diset di angka lain sesuka hati admin. Misal
                        supaya routing table memprioritaskan ospf daripada yang static ini, nilai
                        distance harus lebih besar dari ospf yang angkanya 110.
- **OSPF              : 110**
- **BGP               : 200** untuk internal bgp (ibgp) dan **20** untuk external bgp
(ebgp)


<div class="aimg">
    <img src="//devnull.web.id/images/networking/ip_route/rib.png" alt="Routing table" title="Routing Table" />
</div>

&nbsp;

Baik teman-teman, di atas tadi gambaran tentang bagaimana proses routing dan
routing protocol.

Di bawah saya coba bahas dua routing protokol yang termasuk dynamic routing,
BGP sama OSPF.

&nbsp;

###BGP (Border Gateway Protocol)

BGP ini protokol yang sekarang dipakai backbone Internet, jadi penyedia jasa
semacam isp atau nap, termasuk juga institusi seperti kampus yang berbeda-beda
semua terhubung lewat bgp. Masing-masing bgp dari router yang berbeda
saling bertukar informasi tentang jaringan masing-masing.

Silakan coba cek looking glass OpenIXP di <http://lg.mohonmaaf.com>, pilih show ip
bgp summary dan submit.

Ada ratusan bgp dari perusahaan dan institusi yang bermacam-macam saling
terkoneksi di sini.

Dari output looking glass ini ada beberapa informasi yang perlu dicatat; _Neighbor_,
_AS_, sama _State/Pfx_. Satu-satu dijelaskan di bawah:

**Neighbor.** Ini alamat IP router bgp yang ada di satu broadcast domain.
Misal Indosat di OpenIXP beralamat IP di 218.100.36.110 dan
Telkom di 218.100.36.59.

Jadi misal dari Indosat menuju Telkom kalau di OpenIXP berarti lewat
218.100.36.59, begitu juga sebaliknya menuju Indosat lewat 218.100.36.110.

**AS (Autonomous System)** AS ini representasi perusahaan, institusi atau organisasi.
Jadi ada AS Telkom, AS Indosat, AS Telkomsel, dan seterusnya.
Nah masing masing AS ini punya nomor yang disebut **ASN** atau _Autonomous System Number_.

Nomor AS atau ASN ini sifatnya publik juga unik, tidak ada nomor ASN yang sama.
Pengalokasian ASN ini di bawah IANA atau Internet Assigned Numbers Authority.
Artinya setiap perusahaan atau institusi harus daftar kalau mau punya nomor AS.

Karena AS ini informasi publik, siapa saja bisa lihat. Kalau teman-teman mau cek
misalnya BGP Telkom, Telkom punya ASN salah satunya 7713, silakan cek BGP Telkom
terkoneksi kemana saja, bisa lewat <https://bgp.he.net/AS7713>

Peering bgp ini bisa antar AS artinya ASN nya beda nomor, bisa juga dalam satu
autonomous system atau nomor AS nya sama. Peer bgp antar AS disebut _external bgp_
atau **ebgp**, sementara peer bgp dalam satu AS namanya _internal bgp_ atau
**ibgp**.

**State/Pfx.** Ada dua informasi di sini, state sama Prefix.
State ini kondisi koneksi bgp, dia bisa open, connect, atau established.

Prefix, ini jumlah prefix yang diterima dari neighbor.<br />
Terus prefix ini apa? Prefix ini alamat network, seperti 192.168.0.0/24 misalnya.
Nah berarti jumlah prefix yang diterima dari neighbor ini berarti jumlah
network yang diumumkan oleh neighbor atau peer itu.

Misalkan Telkom yang punya ASN 7713 mengumumkan ke OpenIXP lewat
routernya 218.100.36.59 kalau ada sebanyak 2000 network yang kalau mau menuju
network ini bisa lewat router Telkom.

Kalau mau tau networknya apa saja, bisa cek di <http://lg.mohonmaaf.com> pilih
``show ip bgp neighbor 218.100.x.x received-routes``, isikan neighbor Telkom
218.100.36.59 di kolom isian, klik submit.

Prefix ini yang ada di bgp semuanya publik, kalau kita cari prefix private
seperti 192.168.1.0/24 tidak ada di sini. Juga netmask yang lebih besar dari 24
juga tidak ada, tidak ada /25, /26 dst. Seperti ASN yang publik dan unik,
prefix IP address juga diatur IANA.

Kembali ke hasil looking glass sebelumnya yang received-routes. Di belakang itu
ada informasi path, oke artinya? Ini artinya kalau mau menuju prefix tertentu
jalurnya lewat AS ini.

Dari sini kita tau ternyata yang diumumkan Telkom ke OpenIXP atau dalam
istilah bgp namanya advertise, bukan cuma perfix Telkom, ternyata ada prefix
dari AS lain.

Kenapa begitu? Ini mungkin pelanggan Telkom yang ada di daerah yang mereka tidak
terkoneksi langsung ke OpenIXP karena OpenIXP adanya di gedung IDC Jakarta.
Jadi para member OpenIXP kalau mau menuju alamat ini bisa lewat Telkom.

Terus bagaimana misalnya pelanggan Telkom ini juga jadi pelanggan Indosat, yang
Indosat juga ada di OpenIXP, terus masing-masing Indosat sama Telkom advertise
prefix pelanggan ini ke OpenIXP.

Maka di OpenIXP bakal ada dua jalur menuju prefix yang sama, tapi cuma satu
yang bisa aktif.
Yang mana yang jadi aktif kalau begitu? Em.. di bgp ada flag namanya localpref
yang bisa diset secara manual oleh admin bgp, semakin tinggi nilai localpref
maka dia yang bakal dipilih.

Tapi secara default localpref untuk bgp sama semua bobotnya, kalau begitu bgp bakal pilih
yang jalur AS path nya yang paling pendek. Artinya kalau misalnya lewat Telkom
lewat 3 AS sementara Indosat cuma 2 AS, maka Indosat yang aktif.

Coba sekarang kita cek untuk prefix 175.184.248.0/24 di OpenIXP. Buka lagi
<http://lg.mohonmaaf.com>, pilih show ip bgp, isikan 175.184.248.0, klik submit,
hasilnya ada di paling bawah.

Dari sini ternyata ada 3 jalur menuju prefix 175.184.248.0/24.
kita juga tau prefix ini terdaftar untuk AS 46028.
Dari 3 jalur yang ada ini yang aktif yang ada kata Best, dan jalur ini dipilih karena
jalur AS atau AS Path nya yang paling pendek, ini karena nilai localpref untuk
tiga path ini semuanya sama.

Ada yang menarik dari salah satu hasil AS path, waktu ini ditulis dan kalau
belum berubah, ada yang AS path nya 17922 46028 46028 46028, AS 17922 AS nya
Indosat.

Apa ini, kenapa AS 46028 diulang tiga kali? Ini artinya kalau mau
menuju prefix 175.184.248.0/22 harus melalui pertama AS Indosat, kemudian 46028,
46028 lagi, baru terakhir 46028 juga.

Sebenarnya AS path nya cuma dua saja, 17922 sama 46028.
Metode ini di BGP namanya AS path prepending, path prepending ini cara membuat
bagaimana seolah-olah jalur as path nya kelihatan panjang ada empat AS,
padahal cuma dua.

Kemudian as path prepend ini yang set dari admin bgp nya AS 46028,
bukan Indosat bukan juga OpenIXP. Nah Karena as path nya kelihatan
panjang di OpenIXP, jalur ini tidak terpilih.

Jadi misalnya kita punya dua atau lebih koneksi bgp, dalam istilah bgp namanya
_multihoming_, kita bisa misalnya atur bagaimana caranya salah satu jalur kelihatan
panjang pakai as path prepend, yang harapannya jalur yang di prepend ini nanti
tidak terpilih di bgp.

Kita cuma berharap karena panjang as path ini pertimbangan kedua
setelah localpref, jadi kalau kita sudah prepend sampai panjang sepuluh
AS tapi ternyata tetangga bgp kita set localpref maka as path prepend ini
tidak ada gunanya. Tapi dalam kasus OpenIXP ini as path prepend berhasil
karena nilai localpref sama bobotnya.

Terakhir masalah BGP, semua yang dibahas di atas itu bgp publik.
BGP juga ada private bgp, yang bisa dipakai siapa saja
tanpa harus punya nomor AS. ASN atau nomor AS private yang dialokasikan IANA
dari 64512 sampai 65534. ASN ini bisa dipakai siapa saja di jaringan internal,
tidak ada batasan prefix harus publik, juga tidak ada batasan netmask harus
24 atau di bawahnya, bebas.

&nbsp;

###Konfigurasi BGP
Baik sekarang setelah sedikit paham tentang gambaran BGP, kita coba detail
teknisnya.

Ada tiga mode konfigurasi BGP yang bisa dipakai, _full mesh_, _route reflect_, sama
_route server_.

Anggap sekarang ini kita punya tiga router yang terkoneksi di satu broadcast
domain, router A, B, dan C.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/ip_route/full_mesh.png" alt="BGP Full mesh" title="BGP Full mesh" />
</div>

**Full mesh.** Pakai full mesh, setiap router peering bgp ke semua router, misal A
peer ke B sama C. Router B peering ke A sama C, C peering ke B sama A.

Dengan begini, kalau misalnya link dari A ke B terputus, maka A ke B bisa lewat
router C.
Mode full mesh ini ada kelamahannya, apa itu? Ribet. Bagaimana kalau ada sepuluh
router? masing-masing router punya sembilan peer, dan kalau ada nambah satu
router lagi, kita harus tambah konfigurasi di sepuluh router yang eksisting.

**Route reflector.** Mode ini menyederhanakan problem full mesh di atas. Kalau kita
punya banyak router di satu broadcast domain, kita bisa pilih salah satu router
jadi route reflector. Router yang lainnya, semuanya peering ke route reflector.
Jadi di masing-masing route reflector client cuma ada satu peer bgp, ke route
reflector.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/ip_route/route_reflect.png" alt="BGP Route reflector" title="BGP Route reflector" />
</div>

Anggap router yang dijadikan route reflector ini seperti cermin, jadi prefix
yang di advertise dari client akan di reflect atau dipantulkan ke client yang
lain.

Kelemahannya, route reflector jadi **spof** atau _single point of failure_. Route
reflector mati, maka semua peer bgp mati. Untuk meminimalisir ini, kita bisa
misalnya buat dua route reflector sebagai backup kalau yang utama bermasalah.
Route reflector ini ekstensi iBGP atau internal BGP.

**Route server.** Route server sama seperti route reflector, jadi ada satu atau
lebih yang jadi bgp server, semua router peering ke route server. Bedanya sama
route reflector, route server beroperasi di external bgp dan biasa dipakai di
exchange point.

Route server ini tugasnya cuma jadi server, tidak mem-forward traffic IP seperti
router lainnya. Bahkan biasanya hardware yang dipakai juga server Linux yang
diinstall software BGP semacam BIRD atau Quagga.

Banyak route server publik yang bisa teman-teman coba akses di luar sana,
biasanya dipakai buat troubleshooting masalah inbound route, coba cek
<http://www.routeservers.org>

&nbsp;

Oke, kita coba config bgp. Apa yang diperlukan buat setting BGP? kita harus punya:

1. IP address, IP address harus dalam satu broadcast domain.
   Di contoh ini address kita 172.16.3.2/30 sementara address peer kita 172.16.3.1.
2. AS number kita yang disebut local AS. Di sini kita pakai 64512, private ASN.
3. AS number peer atau neighbor yang disebut remote AS. Remote AS, atau AS
   tetangga BGP kita 65000 yang juga private.
4. Prefix apa saja yang mau kita umumkan atau advertise ke peer. Kita punya dua
   prefix, 10.10.10.0/24 sama 192.168.1.0/24. Dua prefix ini yang nantinya kita
   advertise ke neighbor dan dua prefix ini tipenya connected. Masih ingat
   protokol connected di atas?
5. Prefix yang kita terima dari neighboor atau peer, yang ini optional.

Command konfigurasi yang dipakai di sini pakai VyOS, sistem operasi
router yang Open Source. Kompatibel sama Vyatta, atau mungkin juga Juniper
JunOS.

    :::console
    vyos@ROUTER2:~$ # masuk mode konfiugrasi pakai command configure
    vyos@ROUTER2:~$ configure
    [edit]
    vyos@ROUTER2# ## set IP address, contoh saja di eth0
    [edit]
    vyos@ROUTER2# set interfaces ethernet eth0 address 172.16.3.2/30
    [edit]
    vyos@ROUTER2# ## commit dulu supaya ip address terset di eth0
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2# ## kemudian set local AS 64512
    [edit]
    vyos@ROUTER2# set protocols bgp 64512
    [edit]
    vyos@ROUTER2# ## kemudian set alamat neighbor
    [edit]
    vyos@ROUTER2# set protocols bgp 64512 neighbor 172.16.3.1
    [edit]
    vyos@ROUTER2# ## set remote as buat neighbor
    [edit]
    vyos@ROUTER2# set protocols bgp 64512 neighbor 172.16.3.1 remote-as 65000
    [edit]
    vyos@ROUTER2# ## ini konfigurasi minimal buat peering bgp, kita commit dan seharunya bgp bisa running
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2# exit
    vyos@ROUTER2:~$

Di router peer nya, kalau belum di set, konfigurasinya sama dengan konfig di
atas, tinggal disesuaikan address, as number sama neighbor nya.

Di router VyOS, Vyatta dan keluarganya, cek status bgp bisa pakai `show ip bgp summary` atau bisa
juga cek neighbor `show ip bgp neigh 172.16.3.1`

    :::console
    vyos@ROUTER2:~$ show ip bgp neighbors 172.16.3.1
    BGP neighbor is 172.16.3.1, remote AS 65000, local AS 64512, external link
      BGP version 4, remote router ID 172.16.3.1
      BGP state = Established, up for 00:02:05
      Last read 00:00:09, hold time is 180, keepalive interval is 60 seconds
      Neighbor capabilities:
        4 Byte AS: advertised and received
        Route refresh: advertised and received(old & new)
        Address family IPv4 Unicast: advertised and received
        Graceful Restart Capabilty: received
          Remote Restart timer is 120 seconds
          Address families by peer:
            IPv4 Unicast(not preserved)
      Graceful restart informations:
        End-of-RIB send: IPv4 Unicast
        End-of-RIB received: IPv4 Unicast
      Message statistics:
        Inq depth is 0
        Outq depth is 0

``BGP state = Established``, berarti bgp sudah running.

&nbsp;

####BGP Advertisement

Setelah bgp peering bisa established, konfigurasi belum selesai. Kita advertise
atau umumkan ke tetangga bgp kita kalau kita punya prefix sekian dan sekian.

Secara default, bgp cuma meng-advertise prefix yang juga bgp. Artinya kalau
misal kita punya beberapa peering bgp, prefix yang kita terima dari peer A
misalnya, prefix-prefix ini bakal di-advertise ke peer lain. Sedangkan tipe
routing lain seperti ospf, connected, dan static tidak di distribusikan ke bgp.

Praktek umumnya, kita juga perlu meng-advertise prefix yang bukan bgp ke bgp.
Contoh saja misalnya kita punya static route di router kita yang kita mau prefix
static ini dimasukkan ke bgp buat di-advertise. Dan di protokol dynamic routing,
yang seperti ini disebut _route redistribution_.

Di contoh ini kita punya dua prefix, yang dua-duanya connected. Connected
artinya salah satu interface di router ini terhubung ke network prefix. Dua
prefix yang kita punya, 10.10.10.0/24 sama 192.168.1.0/24.

Bagaimana cara kita meng-advertise dua prefix connected di atas? di VyOS kita
cuma perlu set bgp dengan redistribute connected.

    :::console
    vyos@ROUTER2:~$ # cek prefix yang termasuk connected
    vyos@ROUTER2:~$ show ip route connected
    Codes: K - kernel route, C - connected, S - static, R - RIP, O - OSPF,
           I - ISIS, B - BGP, > - selected route, * - FIB route

    C>* 10.10.10.0/24 is directly connected, lo
    C>* 127.0.0.0/8 is directly connected, lo
    C>* 172.16.3.0/30 is directly connected, eth0
    C>* 192.168.1.0/24 is directly connected, lo
    vyos@ROUTER2:~$
    vyos@ROUTER2:~$ # cek advertise prefix awalnya kosong karena tidak ada
    vyos@ROUTER2:~$ # bgp lain, juga tidak ada protocol lain yang di redistribute
    vyos@ROUTER2:~$
    vyos@ROUTER2:~$ show ip bgp neighbors 172.16.3.1 advertised-routes
    vyos@ROUTER2:~$
    vyos@ROUTER2:~$ configure
    vyos@ROUTER2# set protocols bgp 64512 redistribute connected
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2# save
    Saving configuration to '/config/config.boot'...
    Done
    [edit]
    vyos@ROUTER2# exit
    vyos@ROUTER2:~$ # kita perlu refresh bgp advertisement
    vyos@ROUTER2:~$
    vyos@ROUTER2:~$ reset ip bgp 172.16.3.1 out
    vyos@ROUTER2:~$ show ip bgp neighbors 172.16.3.1 advertised-routes
    BGP table version is 0, local router ID is 172.16.3.2
    Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                  r RIB-failure, S Stale, R Removed
    Origin codes: i - IGP, e - EGP, ? - incomplete

       Network          Next Hop            Metric LocPrf Weight Path
    *> 10.10.10.0/24    172.16.3.2               1         32768 ?
    *> 172.16.3.0/30    172.16.3.2               1         32768 ?
    *> 192.168.1.0/24   172.16.3.2               1         32768 ?

    Total number of prefixes 3
    vyos@ROUTER2:~$

Begitu kita distribusikan protokol connected, maka prefix yang masuk tipe
connected di-import ke bgp kemudian di-advertise ke peer 172.16.3.1

&nbsp;

####Prefix filter

Seperti terlihat di atas, ada tiga prefix connected yang di advertise ke peer
bgp 172.16.3.1.
Umumnya kita tidak mau advertise semua prefix yang kita punya, contoh di atas
itu ada prefix 172.16.3.0/30, prefix ini dipakai buat koneksi inter-router antar
peer bgp, kita tidak mau prefix ini ikut di-advertise ke bgp neighbor.

Di VyOS, ada dua cara filter prefix yang nantinya di-advertise ke peer. Pertama,
kita bisa filter waktu import prefix dari protokol lain, connected misalnya.
Kedua, kita filter di bgp advertisement.

Maksudnya begini, jadi di kasus ini kita punya dua prefix connected yang mau
kita advertise ke peer bgp 172.16.3.1. Nah, prosesnya pertama dua prefix ini
diimport dari connected ke bgp, setelah itu baru di advertise ke peer bgp.
Nah kita bisa filter waktu import dari connected, atau filter prefix waktu
advertise ke peer bgp.
Kita bisa filter waktu prefix ini masuk bgp, jadi di internal bgp prefix sudah
tersaring. Atau kita bisa import prefix semuanya ke bgp tanpa filter, kemudian
waktu advertise ke peer baru difilter.

Saya secara pribadi prefer filter di advertisement. Karena filter import kita
perlu filter masing-masing protokol non bgp, misalnya ada filter untuk
connected, filter buat static, filter buat ospf, dst.
Kalau filter advertisement, maka cukup satu rule filter saja.

Kemudian filter prefix ke peer bgp ini harus ada supaya tidak ada route leak.
Misal saja kalau di bgp multihoming antar isp, biasanya bgp punya peer ke banyak
upstream, misal saja Indosat sama Telkom.

Seperti yang saya sebutkan di atas, bgp secara default meng-advertise semua
prefix yang diterima dari bgp lain. Nah kita tidak mau misalnya prefix yang
kita terima dari Indosat kita advertise lagi ke Telkom, begitu juga sebaliknya.
Kecuali kalau kita jadi penyedia jasa ip transit, tapi bukan itu yang kita bahas
di sini.

Di sini kita coba filter prefix 172.16.3.0/30 supaya tidak di-advertise ke peer
172.16.3.1.

Langkah-langkah nya ada tiga:

- Buat prefix list, kita kasih nama ``LIST-ALLOW-PREFIX``. List ini isinya semua
  prefix yang nantinya di-advertise ke peer bgp
- Buat route-map, nama route-map nya ``BGP-EXPORT``. Di route-map ini rule nya,
  pertama kita allow yang di prefix-list ``LIST-ALLOW-PREFIX``, kemudian prefix
  lainnya yang tidak ada di list di drop.
- Ketiga, route-map yang sudah dibuat di set ke peer 172.16.3.1 untuk export.
  route-map export dipakai buat filter prefix yang kita advertise ke peer, kalau
  route-map import dipakai buat filter prefix yang diterima dari 172.16.3.1.


Pertama, buat prefix list yang isinya prefix yang mau di-advertise. Ada dua
prefix-nya 192.168.1.0/24 sama 10.10.10.0/24

    :::console
    vyos@ROUTER2:~$ configure
    [edit]
    vyos@ROUTER2# set policy prefix-list LIST-ALLOW-PREFIX rule 10 action permit
    [edit]
    vyos@ROUTER2# set policy prefix-list LIST-ALLOW-PREFIX rule 10 prefix 192.168.1.0/24
    [edit]
    vyos@ROUTER2# set policy prefix-list LIST-ALLOW-PREFIX rule 11 action permit
    [edit]
    vyos@ROUTER2# set policy prefix-list LIST-ALLOW-PREFIX rule 11 prefix 10.10.10.0/24
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2# show policy prefix-list LIST-ALLOW-PREFIX
     rule 10 {
         action permit
         prefix 192.168.1.0/24
     }
     rule 11 {
         action permit
         prefix 10.10.10.0/24
     }
    [edit]
    vyos@ROUTER2#


Kedua, buat route-map yang isinya rule terima prefix dari prefix-list di atas,
kemudian drop prefix yang tidak ada di list.

    :::console
    vyos@ROUTER2# set policy route-map BGP-EXPORT rule 10 action permit
    [edit]
    vyos@ROUTER2# set policy route-map BGP-EXPORT rule 10 match ip address prefix-list LIST-ALLOW-PREFIX
    [edit]
    vyos@ROUTER2# set policy route-map BGP-EXPORT rule 50 action deny
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2# show policy route-map
     route-map BGP-EXPORT {
         rule 10 {
             action permit
             match {
                 ip {
                     address {
                         prefix-list LIST-ALLOW-PREFIX
                     }
                 }
             }
         }
         rule 50 {
             action deny
         }
     }
    [edit]
    vyos@ROUTER2#

Ketiga, setelah rule di route-map BGP-EXPORT kita set ke peer

    :::console
    vyos@ROUTER2# set protocols bgp 64512 neighbor 172.16.3.1 route-map export BGP-EXPORT
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2# save
    Saving configuration to '/config/config.boot'...
    Done
    [edit]
    vyos@ROUTER2# ## refresh bgp untuk out advertisement supaya pakai rule baru
    [edit]
    vyos@ROUTER2# run reset ip bgp 172.16.3.1 out
    [edit]
    vyos@ROUTER2# ## cek prefix yang di advertise
    [edit]
    vyos@ROUTER2# run sh ip bgp neigh 172.16.3.1 adv
    BGP table version is 0, local router ID is 172.16.3.2
    Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                  r RIB-failure, S Stale, R Removed
    Origin codes: i - IGP, e - EGP, ? - incomplete

       Network          Next Hop            Metric LocPrf Weight Path
    *> 10.10.10.0/24    172.16.3.2               1         32768 ?
    *> 192.168.1.0/24   172.16.3.2               1         32768 ?

    Total number of prefixes 2
    [edit]
    vyos@ROUTER2#

Berhasil, cuma prefix yang ada di list LIST-ALLOW-PREFIX yang di advertise ke
172.16.3.1

Bagaimana dengan _route-map import?_ _route-map import_ kita pakai kalau kita perlu
filter atau modifikasi atribut routing yang kita terima dari peer bgp.

Ada banyak yang bisa kita buat di route-map. Di bgp multihoming misalnya, contoh
saja kita punya dua peer bgp, dua-duanya meng-advertise ke bgp kita prefix yang
sama, anggap saja prefix Google 8.8.8.0/24.

Kita mau traffic ke network Google ini lewat peer A, kita bisa buat prefix-list
yang isinya 8.8.8.0/24, kemudian kita buat rule di route-map buat modifikasi
atribut localpref ke angka yang lebih besar dari default, kemudian route-map
ini kita set ke neighbor A untuk import.

Jadi fungsi route-map bukan cuma buat filter prefix, tapi juga bisa buat
modifikasi atribut routing bgp. Silakan bereksperimen dengan route-map.

&nbsp;

###OSPF (Open Shortest Path First)

Dynamic protocol berikutnya, OSPF. OSPF masuk dalam kategori _Interior Gateway
Protocol_ atau **IGP**, kategori lainnya **EGP** atau _Exterior Gateway Protocol_, BGP di
atas masuk kategori EGP. IGP artinya protokol ini cuma hidup dan berjalan di
satu lingkup AS saja, bukan seperti BGP di atas yang bisa nyeberang antar AS.
Karena itu OSPF cuma dipakai internal saja dalam satu Autonous System.

Kemudian OSPF ini tipe protokolnya link-state routing protocol. Yang artinya,
apa yang diumumkan atau di advertise ke tetangga ospf bukan routing
tapi kondisi terkini link router.

Jadi cara kerjanya ospf seperti ini, masing-masing router ospf punya database
yang namanya link state database.
Kondisi link interface, berapa bandwidth link itu, ada yang
100 Mbps ada yang 1 Gbps, network nya di link itu apa saja, semuanya
disimpan di link state database atau **lsdb**. Nah, kondisi terkini link
router ini di advertise ke semua tetangga ospf, proses pengumuman atau
advertising ini di ospf namanya _Link State Advertisement_ atau **LSA**. Jadi
setiap router yang terkoneksi ospf saling kirim LSA yang pada akhirnya,
masing-masing router ospf punya database LSDB yang identik, dan LSDB
inilah gambaran topologi jaringan OSPF.

Misal ada 10 router ospf yang saling terhubung, kesepuluh router ini punya
gambaran lsdb yang sama. Waktu ada salah satu router mengalami perubahan kondisi
link, anggap saja link nya down, maka perubahan ini di-broadcast ke semua
neighbor atau tetangga ospf. Jadi kalau router pertama ada link yang down,
router kesepuluh bakal tau.

Selanjutnya dari gambaran topologi yang ada di LSDB ini, masing-masing router
secara independen malakukan kalkulasi jalur routing.

Buat memperjelas gambaran Link-State protocol ini dengan yang lain seperti
distance vector, bayangkan teman-teman ada di sebuah kota yang belum pernah
ke situ sebelumnya, jadi jalan-jalan di situ asing. Anggap sekarang ada di titik
A mau menuju ke titik B. Untuk yang non link-state, maka teman-teman tinggal
jalan saja ikuti petujuk jalan, kalau ketemu simpangan terus ada tanda ke arah B
belok kanan, maka belok kanan, tandanya ke kiri maka ikuti ke kiri. Kalau ikuti
terus petunjuk jalan ini, nanti pada akhirnya sampai di titik B.

Kalau untuk link-state protocol, beda. Link state protocol kita pegang map atau
peta, jadi dari awal kita sudah tau gambaran jalan-jalannya, di mana posisi kita
sekarang dan di mana posisi titik B. Dari map ini kita bisa hitung lewat mana
sih jalan yang tercepat kalau mau ke titik B, jadi tidak perlu ikuti petunjuk
jalan. Kalau ada gang-gang kecil tapi lewat situ lebih cepat, bisa lewat situ.

Kira-kira seperti itu apa yang dilihat oleh router ospf, jadi masing-masing
punya map di lsdb yang setiap router map nya sama, dari map ini masing-masing
router secara independen menghitung jarak terpendek menuju tujuan. Pakai map
lsdb ini maka jaringan bebas loop, ingat looping di atas yang cuma bolak-balik
tidak bisa sampai tujuan, kondisi looping ini tidak bisa terjadi di ospf karena
jalurnya sudah dihitung berdasarkan gambaran topologi lsdb.

Bayangkan kalau pakai non link-state seperti di atas yang kita cuma ikuti
petunjuk jalan. Kita cuma tau belok kiri, belok kanan atau lurus. Kemudian setelah
beberapa belokan ternyata kita sampai di simpangan yang sebelumnya sudah
dilewati, akhirnya cuma berputar-putar di situ-situ saja tidak bisa sampai
tujuan. Karena setelah diperiksa ternyata petunjuk jalannya salah pasang, dan di
dunia routing hal itu juga bisa saja terjadi.

Sampai sini kita sudah paham bahwa OSPF masuk kategori IGP yang cuma beroperasi
dalam satu lingkup Autonomous System. Kemudian OSPF adalah salah satu tipe link
state routing protocol.

Sebelum kita lanjut, saya informasikan kalau ospf ini detail teknisnya agak rumit
dan saya tidak bahas ospf sampai detail karena sepertinya butuh bab sendiri buat
ospf dan bakal panjang dan membosankan.

Di sini saya cuma usahakan bagaimana ospf bisa up dan running tanpa tau detail
bagaimana ospf itu kerjanya. Anggap seperti orang yang belajar nyetir mobil, dia
tidak perlu tau detail bagaimana cara kerja mesin.

Minimalnya kalau mau buat jaringan OSPF, paling tidak ada dua informasi yang
perlu kita tau; Area sama Network.

**Area**. Area di ospf fungsinya segmentasi logis router. Jadi ada sekelompok
router di area A, ada lagi sekelompok router di area B, dan seterusnya.

Bayangkan kalau misalnya kita punya 100 router yang terkoneksi ospf di satu
area, ukuran lsdb pasti bengkak, terus kalau salah satu router mengalami perubahan
link state, maka LSA akan membanjiri jaringan.

Di sini fungsi area, kita bisa secara logis mengelompokkan router-router ke
beberapa area terpisah. Dengan pengelompokan area ini, router ospf cuma
me-maintain lsdb di area yang sama. Artinya router-router ini cuma tau topologi
di areanya saja, topologi di area lain tidak kelihatan.

Ada beberapa tipe area di ospf, di sini dua saja yang akan saya bahas. Pertama
standard area, dan kedua stub area. Area di ospf ditulis seperti format ip
address, misal 0.0.0.0 atau 192.168.1.0, dst.

Ada satu standard area yang wajib ada di ospf, namanya area backbone atau area 0.
Area backbone bisa ditulis pakai 0.0.0.0 atau cukup 0. Semua area selain
backbone harus terkoneksi ke area ini.

Area yang satu lagi namanya stub area. Tipe area ini area tertutup, artinya
jalan keluar masuk area ini cuma lewat satu pintu saja, satu router.
Jadi di area stub ini ada satu router yang fungsinya jadi gateway ke network di
luar area, router ini disebut ABR atau Area Border Router.

Fungsi router ABR ini meng-inject default route ke area stub, jadi nantinya
semua router di area stub ini punya entri routing default route 0.0.0.0/0 yang
gateway-nya router ABR.

Jadi di area stub ini tidak semua routing ospf ada, cuma ada routing intra-area
atau routing di area stub ini saja, plus satu routing untuk default gateway
lewat router ABR. Karena itu traffic LSA di area ini tidak besar, jadinya ukuran
lsdb juga kecil.

Karena ukuran lsdb-nya yang kecil, tipe area ini cocok buat router-router kecil
yang tidak punya memori besar.

<div class="aimg">
    <img src="//devnull.web.id/images/networking/ip_route/ospf_area.png" alt="OSPF Area" title="OSPF Area" />
</div>

Jadi kapan kita pakai area stub? Pertimbangannya, kalau area ini area jalan
buntu, keluar masuk area cuma ada satu jalan saja, lewat router ABR. Kedua,
kalau router-router di area ini router kecil yang cuma perlu default route.

**Network**. Di dalam area ospf, apakah itu standard area atau stub area, di
dalam area ini ada network nya, misal network 10.10.10.0/24 masuk area backbone,
dan network 192.168.1.0/24 masuk area 192.168.1.0 yang tipe areanya stub. Di
dalam satu area bisa ada lebih dari satu network.

Misal kalau kita set network 10.10.10.0/24 ke area backbone, maka ospf bakal cek
interface router yang mana saja yang masuk ke network 10.10.10.0/24. Kalau
misalnya interface eth0 ada ip address 10.10.10.1 maka eth0 dimasukkan ke ospf
dan ospf mulai mem-broadcast LSA lewat eth0.

Ospf membentuk adjacency kalau router ada deteksi router ospf lain yang punya
network sama dan ada di area yang sama.
Jadi kalau ada dua atau lebih router ospf di satu broadcast domain, punya
network yang sama dan network ini ada di area yang sama maka bakal terbentuk
adjcency antar router ospf yang saling bertetangga. Kalau sudah terbentuk
adjacency, router bisa saling broadcast LSA masing-masing.

&nbsp;

####Route redistribution
Seperti juga bgp di atas, kita juga bisa import routing dari protokol lain ke
ospf supaya router yang lain tau jalur ke prefix ini.

&nbsp;

####Konfigurasi OSPF
Kita pakai lagi router untuk setting bgp di atas buat ospf. Jadi router1 ip
addressnya 172.16.3.1/30 dan router router2 172.16.3.2/30.
Router2 punya dua prefix connected, 10.10.10.0/24 sama 192.168.1.0/24 yang dua
prefix connected ini nantinya kita inject ke ospf.

Router1 dan router2 terkoneksi satu broadcast domain di network 172.16.3.0/30.
Network ini yang kita pakai dan set ke area 0 atau area backbone.

    :::console
    vyos@ROUTER1:~$ configure
    [edit]
    vyos@ROUTER1# set protocols ospf area 0 network 172.16.3.0/30
    [edit]
    vyos@ROUTER1# show protocols ospf
    +area 0 {
    +    network 172.16.3.0/30
    +}
    [edit]
    vyos@ROUTER1# commit
    [edit]
    vyos@ROUTER1# save
    Saving configuration to '/config/config.boot'...
    Done
    [edit]
    vyos@ROUTER1#

Router1 sudah terset, tinggal router2.

    :::console
    vyos@ROUTER2:~$ configure
    [edit]
    vyos@ROUTER2# set protocols ospf area 0 network 172.16.3.0/30
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2#

Kalau sudah berhasil terbentuk adjacency, kita bisa lihat detail tetangga ospf
kita.

    :::console
    vyos@ROUTER2# run show ip ospf neighbor

        Neighbor ID Pri State           Dead Time Address         Interface            RXmtL RqstL DBsmL
    172.16.3.1        1 2-Way/DROther     34.366s 172.16.3.1      eth0:172.16.3.2          0     0     0
    [edit]
    vyos@ROUTER2#

Berhasil, neighbor 172.16.3.1 terbaca dari router2.
Di salah satu router ospf kita bisa cek routing ospf pakai command `show ip
route ospf`

    :::console
    vyos@ROUTER1:~$ show ip route ospf
    Codes: K - kernel route, C - connected, S - static, R - RIP, O - OSPF,
           I - ISIS, B - BGP, > - selected route, * - FIB route

    O   172.16.3.0/30 [110/10] is directly connected, eth1, 00:08:32
    vyos@ROUTER1:~$

Cuma ada satu prefix 172.16.3.0/30.
Berikutnya di router2 kita coba import prefix connected ke ospf.

    :::console
    vyos@ROUTER2# set protocols ospf redistribute connected
    [edit]
    vyos@ROUTER2# commit
    [edit]
    vyos@ROUTER2#

Cek lagi di router1, apa sudah ada prefix yang diimport.

    :::console
    vyos@ROUTER1:~$ show ip route ospf
    Codes: K - kernel route, C - connected, S - static, R - RIP, O - OSPF,
           I - ISIS, B - BGP, > - selected route, * - FIB route

    O   10.10.10.0/24 [110/20] via 172.16.3.2, 00:00:03
    O   172.16.3.0/30 [110/10] is directly connected, eth1, 00:11:09
    O   192.168.1.0/24 [110/20] via 172.16.3.2, 00:00:03
    vyos@ROUTER1:~$
    vyos@ROUTER1:~$ ping 10.10.10.1
    PING 10.10.10.1 (10.10.10.1) 56(84) bytes of data.
    64 bytes from 10.10.10.1: icmp_req=1 ttl=64 time=0.677 ms
    64 bytes from 10.10.10.1: icmp_req=2 ttl=64 time=1.13 ms
    ^C
    --- 10.10.10.1 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1001ms
    rtt min/avg/max/mdev = 0.677/0.905/1.133/0.228 ms

Prefix 10.10.10.0/24 sama 192.168.1.0/24 terbaca dari router1 dan gatewaynya
router2 yang address nya 172.16.3.2.

&nbsp;

Baik, saya rasa sudah cukup panjang dan saya cuma sampai di sini. Selanjutnya
silakan teman-teman lanjutkan sendiri eksperimen nya.

Kalau ada koreksi, saran, kritik atau komentar silakan disampaikan.

Terima kasih dan semoga bermanfaat.
