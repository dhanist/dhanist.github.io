Title: Solusi IPv6 di OpenStack Icehouse
Date: 2016-06-02 10:13
Author: Dhani Setiawan
Category: OpenStack
Tags: Linux, OpenStack, Debian, IPv6, Networking
Slug: ipv6-openstack-icehouse
Status: Published
Comments: yes

OpenStack yang pertama kali saya install pakai Debian 8, dan seperti anak kecil yang dapat mainan baru, Saya begitu excited sama OpenStack ini.  
Icehouse, ini versi OpenStack yang default di Debian Jessie, versi OpenStack yang sebenarnya dirilis tahun 2014 lalu dan sekarang sudah masuk masa EOL atau _End of Life_.

Budaya di Debian Stable memang begitu, lebih mengutamakan kestabilan daripada keterbaruan. saya yang pertama kalinya menginstall OpenStack Icehouse di Debian 8 merasakan itu, Saya tidak banyak menemui masalah waktu instalasi.

Semua komponen OpenStack sudah running; Keystone, Nova, Cinder, Glance, dan Neutron semuanya sudah jalan. Kemudian saya buat vm, install OS Debian di vm itu terus migrasi konfigurasi dari server yang lama. Selanjutnya, Saya buat virtual router dan setup networking IPv4 buat guest OS, semuanya lancar jaya tidak ada masalah.

Lalu problem itu muncul waktu saya coba setting koneksi IPv6, OpenStack Neutron tidak bisa buat external network pakai IPv6 padahal untuk internal network tidak ada masalah.  
Berikutnya saya menghabiskan berjam-jam buat Googling dan berujung satu kesimpulan, OpenStack versi Icehouse ini belum sepenuhnya mendukung IPv6.

Saya seperti nabrak dinding dan sedikit frustasi. Penyebabnya karena pertama, proses instalasi ini sudah terlanjur jauh dan tinggal satu potongan puzzle saja yang tidak bisa, IPv6 itu. Kedua, koneksi IPv6 ini penting karena sebelumnya para server ini juga sudah pakai IPv6 waktu masih pakai Xen. Jadi bagaimanapun caranya, para server itu harus punya koneksi IPv6.

Saya punya tiga pilihan. Pertama uninstall OpenStack dan kembali ke Xen, yang ini tidak saya ambil. Kedua, baca kode Python OpenStack Neutron, cari tahu masalahnya di mana dan perbaiki. Cara kedua ini berat, Saya terlalu hebat kalau bisa memahami kode Neutron dalam satu atau dua hari. Tinggal pilihan ketiga, pelajari bagaimana cara kerja OpenStack Neutron dan lihat barangkali ada workaround yang bisa diambil.

Pilihan ketiga saya ambil dan dua hari berikutnya Saya habiskan buat baca dokumentasi, Googling, sama utak-atik OpenStack. Begitu sudah paham cara kerja OpenStack Neutron, solusinya ternyata simpel, gampang dan agak konyol. Cuma tinggal tambah IP address sama tambah route ke routing table, sudah beres.

&nbsp;

Karena saya belum paham kode OpenStack Neutron jadi Saya juga tidak paham penyebab masalah IPv6 ini, tapi mungkin saja karena desain networking yang dipakai.

OpenStack punya istilah-istilah yang menurut saya aneh untuk IP addressing, ada yang namanya floating IP sama fixed IP. Floating IP ini IP address yang dipakai buat komunikasi guest OS dengan external network seperti Internet misalnya, floating IP ini bisa berubah-ubah dan biasanya floating IP ini IP address publik.

Kalau fixed IP, ini IP address yang fix dipakai di guest OS, IP address yang ini tidak bakal berubah dan biasanya ini jenis IP address private.

<div class="aimg">
        <img src="//devnull.web.id/images/openstack/openstack-router.png" alt="OpenStack Virtual Router" title="OpenStack Virtual Router" />
</div>

Dengan setup seperti di gambar itu, satu floating IP dipetakan ke satu fixed IP pakai NAT. Jadi untuk akses ke guest OS dari network luar, yang diakses floating IP-nya bukan yang fixed IP. NAT yang kemudian meneruskan paket IP ke fixed IP yang dipakai guest OS.

Begitu juga kalau guest OS ke external network seperti Internet misalnya, IP address yang fixed IP itu diterjemahkan ke floating IP oleh NAT, jadi yang kelihatan dari Internet bukan yang fixed IP tapi yang floating IP.

Dengan desain network yang seperti itu, kelihatan sekali kalau network itu buat IPv4. Kalau desain seperti ini dibuat IPv6 bakalan tidak bisa, karena di IPv6 tidak ada lagi yang namanya NAT. Di IPv6 kita punya 3,4x10<sup>38</sup> IP address, jadi kita tidak perlu lagi NAT.

Kalau IPv6 dan NAT ini masih asing buat Anda, saya sudah tulis artikel tentang IPv6 dengan judul ["Hampir" Semua Tentang IPv6](//devnull.web.id/networking/pengenalan-ipv6.html). Silahkan dibaca, artikel ini mungkin saja bisa sedikit mencerahkan tentang IPv6.

&nbsp;

### Sudah cukup, sekarang solusinya bagaimana?
Salah satu dari dua opsi bisa diambil.  
**Pertama**, dengan mengeliminasi virtual router dan menggantikannya pakai router fisik.

<div class="aimg">
        <img src="//devnull.web.id/images/openstack/openstack-ext.png" alt="OpenStack External Network" title="OpenStack External Network" />
</div>

Dengan begini, external network langsung di-attach ke guest OS dan IP address public bisa langsung di-set di guest OS. Dengan cara ini, kemungkinan juga firewall perlu disesuaikan.

Buat saya sayangnya, Saya sudah terlanjur pakai virtual router untuk IPv4 dan merubah topologi itu ke cara pertama berarti Saya harus setup networking dari awal lagi. Saya cari cara yang lain saja.

**Cara kedua**, ugly workaround.

Cara yang kedua ini tetap pakai virtual router seperti di gambar yang pertama, hanya saja saya menambahkan IPv6 address termasuk route nya ke virtual router.

Kalau Anda belum ngeh apa itu Linux namespace, ada baiknya baca ini dulu [Cara Kerja OpenStack Networking - Memahami Network Namespace](//devnull.web.id/openstack/openstack-network-namespace.html) karena virtual router OpenStack pakai Linux namespace.

Lanjut, karena koneksi IPv4 di OpenStack ini sudah jalan, berarti saya sudah punya virtual router termasuk interface-nya.

    root@Controller:~# ip netns show
    qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d
    root@Controller:~# ip netns exec qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d ip link show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    7: qg-25efe5e5-07: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:84:ca:5c brd ff:ff:ff:ff:ff:ff
    9: qr-6d6d8407-22: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:7f:a5:23 brd ff:ff:ff:ff:ff:ff
    10: qr-cadd47a6-a2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:c9:b5:47 brd ff:ff:ff:ff:ff:ff
    12: qr-c5ad4b75-f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:69:23:ee brd ff:ff:ff:ff:ff:ff
    root@Controller:~#

Keterangan namespace dan port seperti di bawah:

1. ``qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d``. Ini nama namespace untuk virtual router yang dipakai. Kalau ada lebih dari satu router, namespace juga lebih dari satu.
2. ``lo``. Interface loopback di virtual router.
3. ``qg-25efe5e5-07``. Interface yang terkoneksi ke external network, sebut saja WAN.
4. ``qr-6d6d8407-22``. Interface yang terkoneksi ke internal network 1, atau LAN 1 untuk IPv4.
5. ``qr-cadd47a6-a2``. Interface internal network 2, LAN 2 buat IPv4.
6. ``qr-c5ad4b75-f0``. Interface internal network buat IPv6.

<div class="aimg">
        <img src="//devnull.web.id/images/openstack/openstack-virtual-router.png" alt="OpenStack Virtual Router" title="OpenStack Virtual Router" />
</div>

Cara buat dual-stack IPv4 dan IPv6 di virtual router itu gampang saja.

1. Tambahkan IPv6 address di interface ``qg-25efe5e5-07``.
2. Tambahkan default route IPv6 di router ``qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d``.
3. Tambahkan route di router fisik, entah dynamic atau static route terserah saja.

Untuk network IPv6 IP address-nya saya rubah, kita anggap saja untuk link inter-router pakai prefix ``2001:db8:dead::/64`` dengan ``2001:db8:dead::1`` di router fisik dan ``2001:db8:dead::2`` di ``qg-25efe5e5-07``.

Untuk network guest OS, prefix anggap saja ``2001:db8:cafe::/64``, IPv6 address di interface ``qr-c5ad4b75-f0`` kita pakai ``2001:db8:cafe::1``.

Gambarannya seperti di bawah:

<div class="aimg">
        <img src="//devnull.web.id/images/openstack/openstack-dual-stack.png" alt="OpenStack Dual-stack" title="OpenStack Dual-stack" />
</div>

Langkah-langkahnya seperti ini,  
**Pertama**, Tambahkan IPv6 address di port ``qg-25efe5e5-07``.

    root@Controller:~# ip netns \
    > exec qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d \
    > ip -6 addr add 2001:db8:dead::2/64 dev qg-25efe5e5-07
    root@Controller:~#

**Kedua**, default route di virtual router.

    root@Controller:~# ip netns \
    > exec qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d \
    > ip -6 route add default via 2001:db8:dead::1
    root@Controller:~#
    root@Controller:~# ip netns \
    > exec qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d \
    > ip -6 route show
    2001:db8:dead::/64 dev qg-25efe5e5-07  proto kernel  metric 256 
    2001:db8:cafe::/64 dev qr-c5ad4b75-f0  proto kernel  metric 256 
    fe80::/64 dev qr-6d6d8407-22  proto kernel  metric 256 
    fe80::/64 dev qr-c5ad4b75-f0  proto kernel  metric 256 
    fe80::/64 dev qr-cadd47a6-a2  proto kernel  metric 256 
    fe80::/64 dev qg-25efe5e5-07  proto kernel  metric 256 
    default via 2001:db8:dead::1 dev qg-25efe5e5-07  metric 1024
    root@Controller:~#

**Ketiga**, tambahkan route ``2002:db8:cafe::/64`` di router fisik .  
Ini tergantung OS routernya, misalnya untuk router yang pakai OS Linux.

    ip -6 route add 2001:db8:cafe::/64 via 2001:db8:dead::2

Vyatta dan VyOS.

    user@ROUTER:~$ configure
    user@ROUTER:~# set protocols static route6 2001:db8:cafe::/64 next-hop 2001:db8:dead::2
    user@ROUTER:~# commit

MikroTik RouterOS.

    /ipv6 route add dst-address=2001:db8:cafe::/64 gateway=2001:db8:dead::2

Cisco IOS dan Quagga.

    ipv6 route 2001:db8:cafe::/64 2001:db8:dead::2

Setelah selesai ini kemudian saya coba koneksi IPv6 dari server guest OS.

IPv6 berhasil..! saya terselamatkan.

&nbsp;

### Dengan script, hidup jadi lebih mudah
Kalau misalnya saja nantinya server perlu reboot, saya tidak harus mengulang command-command di atas. Jadi Saya ketik sedikit Shell script buat sedikit mengurangi beban hidup.

Waktu itu saya belum tahu apa nantinya nama namespace sama nama interfacenya ini bisa berubah atau tidak kalau reboot, jadi namespace sama nama interfacenya Saya buat dinamis. Kemudian setelah benar-benar reboot baru Saya tahu nama-namanya tidak ada yang berubah, tapi karena sudah terlanjur diketik jadi Saya _paste_ saja di sini.

IPv6 address-nya juga saya rubah jadi ``2001:db8:dead::/64`` sama ``2001:db8:cafe::/64`` sesuai gambar yang di atas.

Script ini perlu MAC address router gateway buat menentukan mana interface yang mengarah ke external network.

    #!/bin/sh

    ROUTER="00:1e:67:9d:c1:9d"
    GATEWAY="2001:db8:dead::1"
    IP6_REGEX="2001"
    IP6_WAN="2001:db8:dead::2/64"

    for ns in $(/sbin/ip netns show)
    do
            IFACE_WAN=$(/sbin/ip netns exec $ns ip neigh show \
                            | grep "$ROUTER" | head -n1 | awk '{print $3}')
        
            IP6_WAN_TMP=$(/sbin/ip netns exec $ns ip -6 addr show $IFACE_WAN | \
                grep "$IP6_REGEX" | head -n1 | \
                            awk '{print $2}')
        
            echo "$IP6_WAN_TMP" | grep "$IP6_REGEX" >/dev/null 2>&1
            if [ "$?" = "0" ]
            then
                    continue
            else
                    /sbin/ip netns exec $ns ip -6 addr add $IP6_WAN dev $IFACE_WAN
                    /sbin/ip netns exec $ns ip -6 route replace default via $GATEWAY
            fi
    
    done


Supaya script ini bisa jalan waktu sistem boot, script ini bisa dieksekusi dari ``/etc/rc.local``.

&nbsp;

**Artikel Berkaitan:**  
["Hampir" Semua Tentang IPv6](//devnull.web.id/networking/pengenalan-ipv6.html)  
_Tulisan tentang IPv6 yang berusaha komprehensif tapi ternyata gagal membahas semua hal tentang IPv6. "Hampir" Semua Tentang IPv6, dari sejarah, kelebihan IPv6, sampai pengalamatannya._

[Membumikan OpenStack](//devnull.web.id/openstack/pengenalan-openstack.html)  
_Pengenalan yang "ramah" tentang OpenStack ditulis dengan Layman's terms._
