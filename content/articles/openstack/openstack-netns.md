Title: Cara Kerja OpenStack Networking - Memahami Network Namespace
Date: 2016-05-09 20:02
Author: Dhani Setiawan
Category: OpenStack
Tags: Linux, OpenStack, Networking
Slug: openstack-network-namespace
Status: published
Comments: yes

<div class="fimg">
  <img src="//devnull.web.id/images/openstack/netns.png" alt="OpenStack" title="OpenStack" />
</div>

Melanjutkan tentang OpenStack Networking di tulisan yang lalu dengan judul [Memahami OpenStack Neutron lebih dalam](//devnull.web.id/openstack/memahami-networking-openstack-neutron.html), ada salah satu fitur Linux yang dipakai OpenStack Networking dan belum dibahas, fitur Linux itu namanya network namespace.

Mungkin di antara Anda para pembaca ada yang punya background networking. Di dunia networking ada istilah yang dikenal dengan VRF (_Virtual Routing and Forwarding_). VRF ini memungkinkan lebih dari satu routing table coexist dalam satu router fisik, artinya dalam satu router ada banyak router virtual dengan routing table yang independen dan terpisah dari yang lain. Nah di Linux, fitur ini dinamakan network namespace.

Masing-masing network namespace di Linux punya routing table sendiri-sendiri, interface sendiri-sendiri dan juga firewall yang terpisah. Fitur ini yang dipakai OpenStack untuk membuat virtual network dan virtual router.

Seperti router dan network pada umumnya, di network namespace juga ada interface, routing table, firewall, dan ip address. Bedanya, di network namespace kita tidak bisa pakai interface fisik, kita cuma bisa pakai interface virtual. Jadi tidak ada eth0 atau eth1 atau wlan0 di network namespace.  

Karena tidak bisa pakai interface fisik, maka network virtual ini secara default juga tidak bisa berkomunikasi dengan jaringan fisik, seperti Internet misalnya. Dan untuk mengatasi batasan itu, biasanya digunakan bridge untuk menjembatani antara jaringan fisik dan jaringan virtual.  
OpenStack Neutron atau networking juga menggunakan bridge Open vSwitch untuk menjembatani dua jaringan ini.

&nbsp;

###Command-command namespace

Di contoh ini saya pakai banyak command _ip_. Kalau Anda masih sering pakai command _ifconfig_ dan command _route_, saran Saya segera saja tinggalkan karena dua command itu dari zaman batu. Gantinya, pelajari command _ip_ dari package _iproute2_ karena yang ini lebih modern.

Karena network namespace sama seperti network biasa, maka command ip juga bisa dipakai di namespace.

Menambahkan network namespace:

    ip netns add test-netns

Command ini untuk membuat network namespace baru dengan nama _test-netns_.

Untuk melihat semua netns

    root@DEATH-STAR:~# ip netns show
    test-netns
    root@DEATH-STAR:~#

Untuk mengeksekusi command dalam netns, pakai _ip netns exec &lt;nama netns&gt; &lt;command&gt;_.
Contoh untuk eksekusi command _ip link show_ di netns _test-netns_

    root@DEATH-STAR:~# ip netns exec test-netns ip link show
    1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    root@DEATH-STAR:~#

Kalau command di atas dibagi jadi tiga bagian, maka seperti ini:

1. **ip netns exec** : Ini dipakai untuk eksekusi command dalam network namespace.
2. **test-netns** : _test-netns_ adalah nama network namespace.
3. **ip link show** : Ini command yang dieksekusi di dalam netns.

Seperti terlihat di output, waktu kita buat namespace atau netns baru, di netns baru itu langsung ada interface loopback (lo) tapi dengan status down, jadi tidak bisa kita ping.

    root@DEATH-STAR:~# ip netns exec test-netns ping localhost
    PING localhost (127.0.0.1) 56(84) bytes of data.
    ^C
    --- localhost ping statistics ---
    4 packets transmitted, 0 received, 100% packet loss, time 3024ms

Kita harus up-kan dulu interface loopback _lo_ baru kemudian loopback tersebut bisa berfungsi.  
Supaya interface lo bisa up, pakai command _ip link set lo up_. Di dalam netns tentu saja.

    root@DEATH-STAR:~# ip netns exec test-netns ip link set lo up
    root@DEATH-STAR:~# ip netns exec test-netns ping localhost
    PING localhost (127.0.0.1) 56(84) bytes of data.
    64 bytes from localhost (127.0.0.1): icmp_req=1 ttl=64 time=0.126 ms
    64 bytes from localhost (127.0.0.1): icmp_req=2 ttl=64 time=0.066 ms
    64 bytes from localhost (127.0.0.1): icmp_req=3 ttl=64 time=0.057 ms
    ^C
    --- localhost ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 1998ms
    rtt min/avg/max/mdev = 0.057/0.083/0.126/0.030 m

Netns ini belum bisa berkomunikasi dengan dunia luar. Supaya bisa maka harus kita buat bridge untuk menjembatani itu.

Di Debian yang saya pakai untuk percobaan ini nama interface-nya _eth0_. Kemudian Saya akan coba buat sepasang Linux Veth, salah satu veth di assign ke netns _test-netns_, satunya lagi dijadikan member bridge _br0_ bersama _eth0_. _eth0_ ini tersambung dengan kabel ke jaringan fisik external termasuk jaringan Internet.

Buat bridge _br0_ dengan member _eth0_, request ip address ke server DHCP dan test ping ke Google dns.

    root@DEATH-STAR:~# brctl addbr br0
    root@DEATH-STAR:~# brctl addif br0 eth0
    root@DEATH-STAR:~# brctl show br0
    bridge name bridge id               STP enabled     interfaces
    br0         8000.80c16e592e43       no              eth0
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# dhclient br0
    Restarting ntp (via systemctl): ntp.service.
    root@DEATH-STAR:~# ip addr show br0
    4: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
        link/ether 80:c1:6e:59:2e:43 brd ff:ff:ff:ff:ff:ff
        inet 10.10.10.10/27 brd 10.10.10.31 scope global br0
                valid_lft forever preferred_lft forever
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# ping 8.8.8.8
    PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
    64 bytes from 8.8.8.8: icmp_req=1 ttl=55 time=47.2 ms
    64 bytes from 8.8.8.8: icmp_req=2 ttl=55 time=48.5 ms
    64 bytes from 8.8.8.8: icmp_req=3 ttl=55 time=44.0 ms
    ^C
    --- 8.8.8.8 ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2003ms
    rtt min/avg/max/mdev = 44.051/46.605/48.540/1.900 ms
    root@DEATH-STAR:~#


Selanjutnya buat sepasang Linux Veth dengan nama veth1 dan veth2

    root@DEATH-STAR:~# ip link add veth1 type veth peer name veth2
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# ip link show | grep veth
    5: veth2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    6: veth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    root@DEATH-STAR:~#

Seperti yang sudah dijelaskan di artikel sebelumnya, Linux Virtual Ethernet (Veth) adalah sepasang interface yang kalau ada paket masuk lewat salah satu interface maka paket itu akan keluar lewat interface lainnya.

Berikutnya, assign interface veth1 ke namespace _test-netns_ dan veth2 ke bridge _br0_.

    root@DEATH-STAR:~# brctl addif br0 veth2
    root@DEATH-STAR:~# brctl show br0
    bridge name bridge id               STP enabled     interfaces
    br0         8000.80c16e592e43       no              eth0
                                                        veth2
    root@DEATH-STAR:~# ip link set veth1 netns test-netns

Kalau kita cek lagi dengan _ip link show_, veth1 sudah hilang karena sudah ada di namespace _test-netns_

    root@DEATH-STAR:~# ip link show | grep veth
    5: veth2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000

Cek _ip link show_ di _test-netns_

    root@DEATH-STAR:~# ip netns exec test-netns ip link show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    6: veth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
        link/ether 26:e1:4d:ee:33:ef brd ff:ff:ff:ff:ff:ff
    root@DEATH-STAR:~#

Perlu juga diperhatikan bahwa nomor index interface tidak berubah biarpun interface ada di netns. Di namespace _test-netns_ nomor interface 1 untuk _lo_ dan 6 untuk _veth1_ karena nomor index interface _veth1_ adalah 6.

Coba dihidupkan interface veth1 dan veth2 kemudian request ip address ke DHCP server di _test-netns_ dan coba ping ke Google.

    root@DEATH-STAR:~# ip link set veth2 up
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# ip netns exec test-netns ip link set veth1 up
    root@DEATH-STAR:~# ip netns exec test-netns dhclient veth1 >/dev/null
    root@DEATH-STAR:~#
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# ip netns exec test-netns ip addr show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
            valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host 
            valid_lft forever preferred_lft forever
    6: veth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
        link/ether 26:e1:4d:ee:33:ef brd ff:ff:ff:ff:ff:ff
        inet 10.10.10.25/27 brd 10.10.10.31 scope global veth1
            valid_lft forever preferred_lft forever
        inet6 fe80::24e1:4dff:feee:33ef/64 scope link 
            valid_lft forever preferred_lft forever
    
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# ### Cek routing table di netns test-netns
    root@DEATH-STAR:~# ip netns exec test-netns ip route show
    default via 10.10.10.28 dev veth1 
    10.10.10.0/27 dev veth1  proto kernel  scope link  src 10.10.10.25 
    root@DEATH-STAR:~#
    root@DEATH-STAR:~#
    root@DEATH-STAR:~# ip netns exec test-netns ping 8.8.8.8
    PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
    64 bytes from 8.8.8.8: icmp_req=1 ttl=55 time=40.8 ms
    64 bytes from 8.8.8.8: icmp_req=2 ttl=55 time=40.8 ms
    64 bytes from 8.8.8.8: icmp_req=3 ttl=55 time=42.3 ms
    ^C
    --- 8.8.8.8 ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2003ms
    rtt min/avg/max/mdev = 40.817/41.328/42.347/0.720 ms
    root@DEATH-STAR:~#

Network namespace _test-netns_ sudah berhasil terkoneksi dengan Internet.

Untuk menghapus namespace, pakai perintah _ip netns del &lt;nama netns&gt;_

    ip netns del test-netns

&nbsp;

###OpenStack & jaringan virtual

Setelah memahami sedikit tentang network namespace, kita akan lihat bagaimana OpenStack membangun jaringan virtual dengan network namespace.

<div class="aimg">
    <img src="//devnull.web.id/images/openstack/openstack-network-namespace.png" alt="OpenStack Network Namespace" title="OpenStack network Namespace" />
</div>

Gambar di atas adalah perbandingan antara netns dan Open vSwitch.  
Bagian gambar di sebelah kanan adalah network namespace, bagaimana masing-masing tenant OpenStack melihat jaringannya sebagai jaringan yang independen dan terpisah dengan jaringan tenant lainnya.  

Di Open vSwitch, bagian jaringan di gambar yang sebelah kiri itu jaringan sebenarnya, tidak terpisah secara fisik. Jaringan masing-masing tenant jadi satu hanya saja dipisahkan dengan apapun mode yang dipilih oleh administrator, vlan contohnya. Silahkan lihat kembali artikel sebelumnya untuk mode-mode yang lain.

Kalau di tulisan yang lalu kita tahu OpenStack membuat penamaan interface dengan prefix **qbr**, **qvo**, **qvb** dengan masing-masing penggunaannya, di sini juga ada tiga lagi yaitu **qg**, **qrouter**, dan **qr**.  
Mari kita lihat masing-masing nama prefix ini.

- **qrouter** : Ini adalah prefix untuk network namespace
- **qg** : Ini nama interface di namespace untuk interface yang terhubung ke jaringan luar, gampangnya kita sebut gateway.
- **qr** : Ini adalah nama interface yang terhubung ke jaringan internal vm.

Di instalasi OpenStack di contoh ini, saya ambil salah satu namespace bernama qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d

    ip netns show
    qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d

Sedangkan untuk interface di netns tersebut:

    root@Controller:~# ip netns exec qrouter-3b71f8b1-4f6f-4647-abd3-bac4b1aebe7d ip link show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    7: qg-25efe5e5-07: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:84:ca:5c brd ff:ff:ff:ff:ff:ff
    9: qr-6d6d8407-22: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:7f:a5:23 brd ff:ff:ff:ff:ff:ff
    12: qr-c5ad4b75-f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 
        link/ether fa:16:3e:69:23:ee brd ff:ff:ff:ff:ff:ff
    root@Controller:~#

Seperti terlihat, saya punya satu interface gateway qg-25efe5e5-07 dan 2 interface ke jaringan internal dengan prefix qr.

&nbsp;

Saya harap tulisan ini bisa memberikan gambaran untuk para administrator bagaimana OpenStack networking itu dibangun.  
Salah satu hal yang kompleks di OpenStack menurut saya adalah networking ini, rumit dan banyak sekali komponennya.

&nbsp;

**Artikel Berkaitan:**  
[Membumikan OpenStack](//devnull.web.id/openstack/pengenalan-openstack.html)  
_Pengenalan yang "ramah" tentang OpenStack, ditulis dengan bahasa yang sederhana dan gampang dipahami_

[Memahami OpenStack Neutron lebih dalam](//devnull.web.id/openstack/memahami-networking-openstack-neutron.html)  
_Memahami bagaimana OpenStack menggunakan Open vSwitch, bridge, dan mengatur flow packet_

[Convert Database OpenStack Cinder dari Sqlite3 ke MySQL - Debian Jessie](//devnull.web.id/openstack/convert-database-openstack-cinder-dari-sqlite3-ke-mysql.html)  
_Kesalahan konfigurasi default OpenStack Cinder di Debian 8, dan bagaimana cara konversi database dari Sqlite3 ke MySQL_
