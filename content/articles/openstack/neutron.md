Title: Memahami OpenStack Neutron lebih dalam
Date: 2016-04-26 18:58
Author: Dhani Setiawan
Category: OpenStack
Tags: OpenStack, Linux
Slug: memahami-networking-openstack-neutron
Status: published
Comments: yes

<div class="fimg">
  <img src="//devnull.web.id/images/openstack/openstack-logo.png" alt="OpenStack" title="OpenStack" />
</div>

Beberapa waktu lalu, salah satu node server OpenStack kami mengalami system failure karena NIC Gigabit di server itu hang dan reset terus-menerus. Node yang fail ini service-nya networking atau di OpenStack disebut Neutron, dan akibatnya beberapa guest vm unreachable karena sistem failure ini.

Meskipun pada akhirnya saya berhasil mengembalikan guest os beroperasi lagi, tapi Saya perlu waktu yang lama sampai akhirnya sistem up dan running. Kendalanya waktu itu status OpenStack out of sync, status di OpenStack sistem running padahal yang sebenarnya dalam keadaan failed.

Parahnya lagi waktu problem itu, saya belum benar-benar mengerti cara kerja networking di OpenStack, jadinya Saya sedikit kebingungan dan perlu waktu lama sampai akhirnya kembali normal.  
Saya tahu cara mengadministrasi jaringan OpenStack, tapi saya tidak benar-banar tahu bagaimana sebenarnya OpenStack Neutron itu di belakang layar.  
Karena problem itu kemudian saya coba memahami OpenStack Neutron lebih dalam lagi.

Di artikel ini saya akan gambarkan apa yang sudah Saya pelajari, bagaimana OpenStack Neutron itu membuat jaringan virtual di Linux. Bagaimana interkoneksi antar vm dibuat, dan seterusnya.  
Saya tidak membahas bagaimana membuat port di OpenStack, cara assign floating ip, dan sebagainya. Yang mau saya jelaskan lebih ke low level bagaimana sebenarnya networking di OpenStack itu beroperasi.

&nbsp;

### Setup
Saya jelaskan dulu deployment OpenStack yang saya pakai. Di setup ini Saya gunakan vlan untuk komunikasi antar vm.  
Ada beberapa mode di OpenStack Neutron untuk komunikasi antar vm:

- flat : Ini mode routing biasa, antar tenant OpenStack tidak ada segmentasi jaringan.
- vlan : Antar tenant OpenStack masing-masing tersegmentasi dengan vlan, beda tenant beda vlan id.
- vxlan: Segmentasi jaringan menggunakan vxlan.
- gre : Segmentasi jaringan antar tenant menggunakan tunneling generic routing encapsulation.

Dalam setup ini saya gunakan vlan dengan range vlan id untuk tenant dari 1000 - 1100.

Di setup ini ada tujuh guest os yang berjalan di OpenStack, tapi di contoh ini saya ambil tiga saja. Tiga vm itu anggap saja VM1, VM2, dan VM3. Tiga vm ini berjalan di dua server compute atau di OpenStack disebut Nova.

Saya gambarkan kurang lebih tiga vm itu seperti di bawah:

<div class="aimg">
  <img src="//devnull.web.id/images/openstack/neutron.png" alt="OpenStack Neutron" title="OpenStack Neutron" />
</div>

**Keterangan:**

- **A, E, W** : Guest OS.
- **B, F, X** : Linux bridge
- **C, Y** : Openvswitch bridge dengan nama br-int (default OpenStack).
- **D, Z** : Openvswitch bridge dengan nama br-vm.

Kalau Anda merasa tidak familiar dengan gambar di atas, maka ada beberapa komponen penting yang harus dipelajari dulu sebelumnya, yaitu:

- Tap device : Interface virtual yang berjalan di layer 2.
- Linux Bridge: ini bridge yang dibuat dengan brctl.
- Linux virtual ethernet : Linux veth, Linux veth adalah virtual interface yang berpasang-pasangan. Anggap pasangan veth A dan B, seperti pipa, apa yang masuk ke A akan keluar lewat B, yang masuk lewat B keluar lewat A.
- Openvswitch: Software switching, seperti switch fisik tapi di lingkungan virtualisasi.

Di OpenStack Neutron, Openvswitch juga diatur dengan OpenFlow. saya jelaskan singkat saja, di dalam switch ada yang namanya control plane dan data plane. Control plane fungsinya untuk mengatur flow paket, sedangkan data plane mengeksekusi flow tersebut. Biasanya dalam switch umum, control plane dan data plane jadi satu. Dengan OpenFlow, control plane dipisah dari data plane dan control plane diatur lewat OpenFlow.

Keuntungannya, switch yang berbeda-beda dari vendor apapun kalau pakai OpenFlow maka bisa diatur dari software yang sama. Cisco tidak harus dengan Cisco IOS, Juniper tidak harus dengan JunOS. Istilah untuk ini namanya SDN (Software Defined Networking).

Empat hal di atas itu yang harus dipelajari dulu kalau memang masih asing, karena OpenStack Neutron menggunakan 4 komponen di atas untuk membentuk jaringan.

Melihat gambar di atas, mungkin Anda punya pertanyaan mengapa harus ada Linux bridge di situ. Ini juga pertanyaan saya pertama kali karena seperti tidak masuk akal menempatkan Linux bridge di antara vm dan Openvswitch br-int. Lebih logis kalau tap device langsung ke Openvswitch bridge br-int dari pada ke Linux bridge.

Kemudian saya tahu dari hasil baca sana-sini bahwa bridge itu memang diperlukan. Fitur security di OpenStack memerlukan bridge itu karena firewall tidak akan berfungsi kalau interface tap dijadikan port Openvswitch. Jadi, anggap saja bridge B, F, dan X adalah firewall bridge.

&nbsp;

### OpenStack Networking
Dilihat dari gambaran besarnya, OpenStack Neutron membagi network jadi tiga kategori:

1. Management Network: Jaringan yang digunakan untuk memanage server OpenStack.
2. External: Jaringan yang digunakan guest OS untuk berkomunikasi dengan jaringan luar, Internet misalnya.
3. Internal: Jaringan yang digunakan untuk komunikasi antar virtual machine.

Di setup ini, saya jadikan management dan external network jadi satu jaringan. Di gambar itu interface untuk management dan external menggunakan interface eth0, sedangkan interface untuk internal eth1.

Di tulisan ini saya fokuskan untuk jaringan internal saja, jaringan external dan management tidak karena Saya rasa dua network itu cukup jelas fungsinya.

Penjelasan masing-masing komponen network internal seperti di bawah:

- br-vm: Bridge Openvswitch untuk jaringan internal vm saya namakan br-vm. Pengaturan vlan untuk tenant ada di bridge ini.
- br-int: Ini bridge Openvswitch internal OpenStack. Bridge ini tidak diatur oleh user atau konfigurasi, tapi OpenStack yang mengatur. Fungsi bridge ini semacam patch panel fisik, jalur-jalur ke vm diatur di bridge ini.
- Linux bridge: Seperti saya terangkan di atas, bridge ini fungsi utamanya untuk security. Setiap vm mempunyai bridge sendiri-sendiri.

Antara br-int dengan br-vm terkoneksi dengan Linux veth. Ujung Linux veth yang satu namanya int-br-vm, ujung satunya phy-br-vm. int-br-vm ditempatkan di bridge br-int, sedangkan phy-br-vm ditempatkan di br-vm.

<div class="aimg">
  <img src="//devnull.web.id/images/openstack/br-int.png" alt="OpenStack Openvswitch" title="OpenStack Openvswitch" />
</div>

&nbsp;

###Proses networking OpenStack
Untuk setiap vm baru yang dibuat, OpenStack neutron membuat satu tap interface, satu Linux bridge, dan satu pasang Linux veth.  
Tap interface untuk di-attach ke vm dan vm mapping tap itu ke eth0.  
Satu Linux bridge untuk keperluan firewall. Member bridge ini ada dua, tap yang mengarah ke vm dan salah satu interface virtual Linux veth. Sedangkan Linux veth yang satunya lagi jadi member bridge br-int.

OpenStack membuat prefix nama interface yang konsisten, prefix yang dimaksud seperti di bawah:

- tap : Interface dengan prefix tap adalah tap device.
- qbr : Interface dengan prefix qbr menandakan Linux bridge.
- qvb : qvb adalah salah satu dari pasangan Linux veth yang jadi member bridge qbr.
- qvo : Ini pasangan Linux veth qvb. Jadi qvo dan qvb itu sepasang veth. qvo jadi member bridge Ovs (Openvswitch) br-int.

Jadi untuk satu vm, prefix interface beda-beda cuma suffixnya sama. Misal suffix interface abcd-01, maka tap nya **tapabcd-01**, bridge-nya **qbrabcd-01**, veth yang di Linux bridge **qvbabcd-01**, veth yang di Ovs bridge **qvoabcd-01**.


Contoh di bawah ini saya ambilkan dari salah satu server compute dengan salah satu guest OS yang Saya beri nama alderaan:

**Guest interface**  
Dari guest, nama interface eth0 dengan mac address fa:16:3e:0c:24:82

    administrator@alderaan:~$ ip link show eth0
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:0c:24:82 brd ff:ff:ff:ff:ff:ff
    administrator@alderaan:~$

**Tap device**  
Dari compute server kita cari tap device dengan mac address yang 40 bit di belakangnya sama dengan yang terbaca di guest OS, yaitu 16:3e:0c:24:82. _ip link show_ untuk print interface.

    root@nova2:~# ip link show tapdd0ae56d-5f
    50: tapdd0ae56d-5f: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master qbrdd0ae56d-5f state UNKNOWN mode DEFAULT group default qlen 500
    link/ether fe:16:3e:0c:24:82 brd ff:ff:ff:ff:ff:ff
    root@nova2:~#

Dari sini diketahui nama interface tap **tapdd0ae56d-5f**, berarti suffix-nya **dd0ae56d-5f**.

**Linux bridge**  
Karena sudah tahu suffix interface **dd0ae56d-5f**, tinggal tambah prefix qbr jadi **qbrdd0ae56d-5f**.

    root@nova2:~# brctl show qbrdd0ae56d-5f
    bridge name	bridge id		STP enabled	interfaces
    qbrdd0ae56d-5f		8000.fad1404dbac4	no		qvbdd0ae56d-5f
							tapdd0ae56d-5f
    root@nova2:~#

**Linux veth**  
Dari suffix itu, berarti pasangan veth nya **qvodd0ae56d-5f** dan **qvbdd0ae56d-5f**.  
**qvbdd0ae56d-5f** jadi member Linux bride **qbrdd0ae56d-5f**, seperti terlihat di command brctl di atas.  
**qvodd0ae56d-5f** jadi member Ovs bridge br-int.

    root@nova2:~# ovs-vsctl show
    da610347-b798-4520-b5a1-4f8899b3e1a4
        
        Bridge br-int
            fail_mode: secure
            Port br-int
                Interface br-int
                    type: internal
            Port "qvodd0ae56d-5f"
                tag: 3
                Interface "qvodd0ae56d-5f"
            Port int-br-vm
                Interface int-br-vm
        ovs_version: "2.3.0"
    root@nova2:~#

Interface yang tidak berhubungan saya hilangkan dari output.

Menurut saya yang buat susah itu nama interface yang aneh dan tidak deskriptif itu. Kalau misalnya nama interface dibuat seperti qbralderaan, qvoalderaan, atau qvbalderaan mungkin lebih gampang buat diingat.

&nbsp;

###Packet Flow
Di bagian ini saya bahas bagaimana aliran paket di Openvswitch dengan setup di atas.  
Di setup ini tenant menggunakan range vlan id dari 1000 - 1100. Karena tenant cuma ada satu, vlan yang terpakai baru vlan id 1000.

Vlan ini di tag di br-vm untuk vlan tenant, kemudian di Ovs br-int vlan tersebut di rewrite dengan vlan yang diatur sendiri oleh OpenStack dan diarahkan ke port yang jadi member vlan tersebut.

Dalam setup ini, vlan tenant adalah vlan 1000 sedangkan vlan internal OpenStack Neutron vlan 3. Vlan 3 ini sepenuhnya OpenStack yang mengatur, tidak ada campur tangan user dan sebaiknya tidak dirubah secara langsung.

    root@nova2:~# ovs-vsctl show
    da610347-b798-4520-b5a1-4f8899b3e1a4
        
        Bridge br-int
            fail_mode: secure
            Port br-int
                Interface br-int
                    type: internal
            Port "qvodd0ae56d-5f"
                tag: 3
                Interface "qvodd0ae56d-5f"
            Port int-br-vm
                Interface int-br-vm
        ovs_version: "2.3.0"
    root@nova2:~#

Terlihat dari output, vlan internal OpenStack vlan 3 (tag: 3). Mungkin counter-intuitive, yang dimaksud _tag: 3_ di output itu sebenarnya mode port access, bukan trunk. Jadi port qvodd0ae56d-5f itu port vlan 3 mode access.

Untuk memperjelas flow paket, gambarannya seperti di gambar.

<div class="aimg">
  <img src="//devnull.web.id/images/openstack/flow.png" alt="OpenStack Packet flows" title="OpenStack Packet flows" />
</div>

Seperti saya jelaskan sebelumnya, packet flow di Openvswitch itu tidak diatur langsung dari Openvswitch, tapi dari OpenFlow.  
Mari kita lihat flow nya:

    root@nova2:~# ovs-ofctl dump-flows br-int
    NXST_FLOW reply (xid=0x4):
     cookie=0x0, duration=417414.623s, table=0, n_packets=11149297, n_bytes=1952040247, idle_age=0, hard_age=65534, priority=1 actions=NORMAL
     cookie=0x0, duration=410729.710s, table=0, n_packets=13337809, n_bytes=6907864027, idle_age=0, hard_age=65534, priority=3,in_port=7,dl_vlan=1000 actions=mod_vlan_vid:3,NORMAL
     cookie=0x0, duration=417413.441s, table=0, n_packets=4617, n_bytes=295786, idle_age=65534, hard_age=65534, priority=2,in_port=7 actions=drop
     cookie=0x0, duration=417411.202s, table=0, n_packets=0, n_bytes=0, idle_age=65534, hard_age=65534, priority=2,in_port=6 actions=drop
     cookie=0x0, duration=417414.582s, table=22, n_packets=0, n_bytes=0, idle_age=65534, hard_age=65534, priority=0 actions=drop
    root@nova2:~#

Di output line ke dua 
     
    in_port=7,dl_vlan=1000 actions=mod_vlan_vid:3,NORMAL
    
Maksudnya paket yang masuk lewat port 7, port 7 ini int-br-vm, kalau paket tersebut ada vlan header dengan vlan id 1000 maka vlan itu direwrite ke vlan 3. Vlan 3 ini kemudian di untag di port qvodd0ae56d-5f.

Untuk memahami kenapa ada dua vlan berbeda ini, anggap saja ada dua versi vlan untuk tenant yang sama, vlan 1000 dan vlan 3. Vlan 1000 versi saya (user) vlan 3 versi OpenStack.  
Nah karena saya dan OpenStack tidak sepakat nomor id vlan-nya, maka perlu pemetaan vlan. Vlan 1000 versi user diterjemahkan ke vlan 3 versi OpenStack.

Kalau saya ditanya kenapa OpenStack tidak pakai vlan yang dipilih user saja, Saya tidak bisa jawab karena memang Saya tidak tahu kenapa desainnya seperti itu. Padahal logis saja kalau pakai vlan 1000 tanpa perlu translasi vlan.

Kita lanjut lihat flow di bridge br-vm:

    root@nova2:~# ovs-ofctl dump-flows br-vm
    NXST_FLOW reply (xid=0x4):
     cookie=0x0, duration=417699.483s, table=0, n_packets=13597383, n_bytes=6938457305, idle_age=0, hard_age=65534, priority=1 actions=NORMAL
     cookie=0x0, duration=411015.347s, table=0, n_packets=10778277, n_bytes=1641396036, idle_age=0, hard_age=65534, priority=4,in_port=3,dl_vlan=3 actions=mod_vlan_vid:1000,NORMAL
     cookie=0x0, duration=417698.995s, table=0, n_packets=48, n_bytes=3976, idle_age=65534, hard_age=65534, priority=2,in_port=3 actions=drop
    root@nova2:~#

Output line ke dua:

     in_port=3,dl_vlan=3 actions=mod_vlan_vid:1000,NORMAL
    
Paket dengan header vlan 3 dan masuk dari port 3 (phy-br-vm) akan dipetakan ke vlan user vlan 1000. Vlan 1000 ini yang dipakai untuk komunikasi antar vm yang beda server compute.

Saya harap penjelasan saya tentang internal network OpenStack ini bisa dipahami dan bisa memberikan gambaran bagaimana OpenStack networking itu beroperasi.

Sebenarnya belum semua tentang internal network dibahas karena masih ada virtual router OpenStack dengan network namespace yang belum dijelaskan. Tapi saya batasi sampai di sini saja karena terlalu panjang kalau virtual router dan network namespace ditulis juga.

Mungkin lain kali, mungkin.

&nbsp;

**Artikel Berkaitan:**  
[Membumikan OpenStack](//devnull.web.id/openstack/pengenalan-openstack.html)  
_Pengenalan yang "ramah" tentang OpenStack, ditulis dengan bahasa yang sederhana dan gampang dipahami_

[Cara Kerja OpenStack Networking - Memahami Network Namespace](//devnull.web.id/openstack/openstack-network-namespace.html)  
_Pembahasan tentang Linux Network Namespace dan bagaimana OpenStack menggunakan Network Namespace untuk membuat jaringan virtual._
