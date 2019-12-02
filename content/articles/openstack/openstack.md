Title: Membumikan OpenStack
Date: 2016-05-14 00:13
Author: Dhani Setiawan
Category: OpenStack
Tags: Linux, OpenStack, Debian
Slug: pengenalan-openstack
Status: published
Comments: yes

<div class="fimg">
  <img src="//devnull.web.id/images/openstack/openstack-logo.png" alt="OpenStack" title="OpenStack" />
</div>
Hari itu tanggal 13 Februari 2016, bunyi notifikasi di hape tanda ada email masuk. Subject email itu bunyinya _"Debian 6.0 Long Term Support reaching end-of-life"_, email announcement dari tim Debian.

Semua Linux admin paham apa maksudnya ini. Ya, itu berarti upgrade sistem, sebuah task yang njlimet.

Tapi tetap saja, sistem harus diupgrade. Debian 6 dengan nama Squeeze itu sudah lima tahun dari lahirnya di tahun 2011 lalu.

Februari 2016, Debian stable yang paling baru namanya Debian Jessie, versi 8.  
Itu artinya, prosesnya pasti semakin rumit karena proses upgrade tidak bisa lompat dari 6 langsung ke 8, harus upgrade ke versi 7 dulu atau Debian Wheezy.

Dengan pertimbangan proses yang njlimet itu, juga karena lingkungan virtualisasi Xen, ditambah lagi karena banyaknya jumlah server yang harus diupgrade, saya putuskan tidak upgrade.

Sistem tidak diupgrade, tapi saya lebih milih buat fresh install Debian Jessie.

Nyatanya pilihan ini juga tidak lebih mudah, saya harus pikirkan juga bagaimana caranya migrasi sistem dengan waktu downtime yang minim.

Strategi yang muncul di pikiran saya waktu itu, pakai satu mesin untuk host virtualisasi, terus buat guest OS Debian 8 di situ, kemudian migrasi konfigurasi.

Nah di sinilah perkenalan saya dengan OpenStack dimulai.

Saya tidak tinggal di goa, jadi kata seperti cloud computing, big data, dan OpenStack sering sekali saya dengar. Kata-kata itu biasanya cuma lewat begitu saja, tapi karena momen upgrade ini Saya jadi punya niat buat memahami apa itu OpenStack.

Saya buka Google, cari tentang OpenStack berbahasa Indonesia belum ada yang bisa memuaskan keingintahuan Saya. Kebanyakan tulisan terlalu advance, banyak juga yang pengenalan OpenStack tapi tidak terlalu ramah buat yang belum ngerti OpenStack seperti saya waktu itu.

Dari hasil baca sana-sini saya masih juga kesulitan memahami konsep OpenStack. Tapi akhirnya biarpun berbekal sedikit pengetahuan, Saya tetap install OpenStack. Setup OpenStack Saya waktu itu, satu controller dan dua compute node biar bisa redundant maksudnya.

Setelah proses deploy dan testing yang sangat singkat itu, hasilnya saya berani putuskan bahwa setup OpenStack ini siap beroperasi.

Dan sekarang saya pikir, Saya juga perlu menulis pengenalan OpenStack berdasarkan pemahaman Saya.

&nbsp;

## Tentang OpenStack

Saya yakin banyak pengguna <s>Linux</s> GNU/Linux, mungkin juga Anda salah satunya yang sering dengar kata OpenStack, atau mau belajar OpenStack tapi masih geleng-geleng belum ngeh apa itu OpenStack.

Kabar baiknya, di artikel ini saya mau coba kasih gambaran tentang pengertian OpenStack termasuk komponennya. Kabar buruknya, karena Saya juga termasuk baru kenal OpenStack, jadi tidak semua hal tentang OpenStack ada di tulisan ini.

Kalau kita bahas tentang OpenStack pasti tidak bisa lepas dari yang namanya buzzword "Cloud". Ya, jadi kata _Cloud_ itu cuma buzzword. Artinya, _Cloud_ itu bukan terminologi teknis, jadi arti kata _Cloud_ itu bisa beda masing-masing orang.

Tapi coba kita lihat definisi _Cloud Computing_ yang lumayan bikin bingung dari [Wikipedia](https://en.wikipedia.org/wiki/Cloud_computing) ini:  

>"_**Cloud computing**, also **on-demand computing**, is a kind of Internet-based computing that provides shared processing resources and data to computers and other devices on demand. It is a model for enabling ubiquitous, on-demand access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications and services)_"

Jadi, secara umum yang mereka-mereka maksud dengan _Cloud Computing_ itu, layanan komputasi yang resource komputasinya seperti jaringan, hard disk, dan server, itu tidak perlu dikelola sendiri dan resource itu sifatnya on-demand.

Seperti Saya, atau Anda juga yang punya email Gmail misalnya. Kita tidak perlu punya server, tidak perlu sewa jaringan sama public ip address kalau mau bisa pakai email. Cukup buka browser, atau pakai smartphone sudah bisa baca sama kirim email.  
Resourcenya seperti server, storage, sama jaringannya kita tidak perlu ikut mikir, biarkan itu Google saja yang mikir.  
Sama seperti kalau kita perlu listrik, kita tidak perlu punya pltd sendiri kan? kita tinggal sewa saja dari PLN, beres.

Nah, dengan pemahaman _Cloud_ yang seperti itu, terus di mana tempat dan fungsinya OpenStack?

Jadi OpenStack adalah software suite, atau kumpulan banyak software yang fungsinya untuk mengatur resource komputasi itu. OpenStack fungsinya mengatur server, hard disk, network, dan sebagainya. Karena itu OpenStack menyebut dirinya sebagai _**Cloud Software**_.

Sebenarnya OpenStack itu adalah project Open Source yang lahirnya belakangan. Jadi sebelum OpenStack sudah ada project yang kurang lebih sama, seperti OpenNebula contohnya.

OpenStack disebut software suite karena memang ada lebih dari satu software cloud di OpenStack itu. Beda sama software cloud yang spesifik, software cloud buat storage misalnya seperti ownCloud atau Seafile.  
Kalau untuk storage-nya, OpenStack punya software yang namanya Swift sama Cinder.

Masing-masing software atau service di OpenStack ini bisa jalan sendiri-sendiri atau independen. Jadi kalau misalnya kita cuma perlu software cloud buat storage, kita bisa install OpenStack Swift saja, yang lain tidak perlu.

Sudah paham kalau OpenStack adalah software suite untuk cloud? Sekarang coba kita lihat apa saja software atau service di OpenStack.

OpenStack punya nama-nama untuk masing-masing software nya.

1. **Keystone:** Identity service
2. **Nova:** Compute service
3. **Glance:** Image service
4. **Swift:** Object storage service
5. **Cinder:** Block storage service
6. **Neutron:** Networking service

Enam software di atas itu yang termasuk inti atau core service di OpenStack, cuma enam ini juga yang mau saya tuliskan.

Saya tidak bahas service yang lain karena saya juga tidak pernah pakai service itu kecuali Horizon. Horizon ini buat manajemen Cloud lewat interface web.

Service selain enam core di atas:

* **Horizon:** Dashboard Web management
* **Trove:** Database
* **Zaqar:** Messaging
* **Barbican:** Key Management
* **Congress:** Governance
* **Ceilometer:** Telemetry
* **Sahara:** Elastic Map Reduce
* **Manila:** Shared Filesystems
* **Magnum:** Containers
* **Heat:** Orchestration
* **Ironic:** Bare-Metal Provisioning
* **Designate:** Domain Name Service
* **Murano:** Application Catalog

&nbsp;

### Keystone
Keystone adalah identity service. Mungkin service Keystone ini yang wajib ada di tiap-tiap instalasi OpenStack. Jadi semua service sama tenant di OpenStack harus terdaftar di Keystone ini.

Misalnya kita nambah service baru, seperti Nova contohnya, Nova ini harus di daftarkan di Keystone. User sama tenant begitu juga, harus terdaftar di Keystone.

Istilah Tenant di OpenStack itu seperti grup resource. Jadi setiap tenant itu punya user sama kapasitas resource-nya masing-masing. Kita bisa batasi resource storage buat tenant A maksimal 100 GB misalnya.

Itu Keystone. Jadi Keystone itu service OpenStack yang berhubungan dengan Tenant, User, sama service yang lain.


### Nova
Nova adalah compute service, atau virtualisasi, atau service virtual machine. Nova tugasnya membuat guest OS atau virtual machine, restart, shutdown, destroy guest OS, itu semuanya dari Nova.

Nova ini frontend, artinya Nova bukan teknologi hypervisor seperti KVM, Xen dan teman-temannya. Untuk hypervisor-nya Nova bisa pakai backend Qemu, bisa juga pakai KVM, Xen, bahkan VMware vSphere.

Itu Nova. Jadi jelas ya, bahwa fungsi Nova ini lebih ke Virtual Machine.

### Glance
Glance fungsinya buat manage disk image. Disk image ini yang nantinya diattach ke vm lewat Nova, terus dipakai buat hard disk virtual.  
Glance ini seperti repositori disk image, user bisa upload disk image, terus instruksikan Nova supaya boot pakai disk image ini.

Jadi gambarannya kurang lebih seperti itu. Glance itu fungsinya berhubungan dengan image, disk image.

### Swift
Swift adalah service object storage di OpenStack.

Sudah pernah dengar object storage? ini salah satu dari beberapa jenis storage, yang lain misalnya seperti file-level storage sama block-level storage.

Di object storage, kalau misalnya kita simpan file di storage dengan tipe ini, data yang disimpan di storage ini disebut object.

Object ini masing-masing punya metadata, metadata ini berisi informasi tentang object, misalnya tipe filenya, besarnya berapa, dibuat kapan, dan sebagainya. Terus setiap object ini juga punya id masing-masing yang unik.

Kita ambil contoh, kita sudah tidak asing sama layanan cloud storage semacam Google Drive atau Amazon S3.  
Bisa kita bayangkan dari semua pengguna Google Drive itu, kalau dihitung semua kapasitas storage-nya pasti bukan hitungan terabyte lagi, anggap saja sekian exabyte atau jutaan terabyte.

Nah, problemnya adalah, bagaimana mengatur data sebesar itu? itu pasti jadi persoalan sendiri.

Di sinilah keunggulan storage tipe object storage. Kapasitas storage dengan tipe ini bisa scaling atau bisa membesar kapasitasnya sampai skala unlimited. Terus kerennya lagi, letak geografis bukan masalah buat object storage.

Jadi storage yang terpisah-pisah secara geografis, data center yang beda lokasi bukan masalah karena object storage melihatnya sebagai satu entity.  

Karena itu, karena kelebihan ini makanya layanan seperti Amazon S3 sama Google Drive pakai object storage buat nyimpan data.

### Cinder
OpenStack Cinder adalah service block storage. Block storage ini beda sama Swift yang object storage di atas.  
Block storage ini nyimpan data di disk dalam bentuk block, block ini biasanya disebut volume.

Block storage itu kebanyakan dipakai di _Storage Area Network_ atau SAN. Data yang bentuknya block itu bisa dipakai buat hard disk virtual, karena itu tipe storage ini banyak dipakai buat filesystem di Guest OS.

Block yang tersimpan di disk itu bisa didistribusikan sebagai hard disk virtual ke server-server lewat protokol iSCSI atau Fibre Channel (FC), ini bukan typo tapi memang betul fibre bukan fiber.  
Fibre Channel ini protokol, kalau fiber optic itu medianya. 

Terus OS yang pakai FC atau iSCSI ini nantinya bisa memperlakukan block yang dari SAN itu, sama seperti hard disk fisik. Block ini bisa diformat ke filesystem tertentu seperti ext4, ntfs, atau fat dan diisi data.

Tipe storage yang ini lebih cepat kalau dibanding object storage, itu kelebihannya, karena itu tipe block ini lebih cocok buat database sama filesystem untuk OS.  
Kelemahannya, tipe block ini kurang bisa scaling seperti object storage. Jadi kalau object storage bisa scaling bahkan sampai beda lokasi, block storage tidak.

### Neutron
OpenStack Neutron ini adalah layanan Networking as a Service atau NaaS. saya sendiri juga belum ngeh konsep NaaS ini sampai Saya pakai OpenStack, padahal Saya punya background jaringan.

Neutron ini tugasnya me-manage jaringan virtual, alokasikan ip address, termasuk juga security firewall.  
Pakai Neutron ini, user tenant bisa buat jaringan virtual untuk tenant-nya, dia juga bisa buat router virtual termasuk port-nya, atur firewall, ip address, dan lainnya.

Dari semua service core di OpenStack, menurut saya Neutron ini yang paling susah, paling susah dimengerti. Karena ketika dipelajari lagi ternyata Neutron ini banyak komponen program Linux yang membentuk jadi Neutron. Dari Linux bridge, Open vSwitch, OpenFlow, Linux virtual ethernet, sampai Linux network namespace.

Kalau Anda mau pelajari OpenStack Neutron lebih dalam lagi, silahkan baca tulisan saya yang lain tentang Neutron, [Memahami OpenStack Neutron lebih dalam](//devnull.web.id/openstack/memahami-networking-openstack-neutron.html) sama lanjutannya juga, [Cara Kerja OpenStack Networking - Memahami Network Namespace](http://devnull.web.id/openstack/openstack-network-namespace.html).  

Dua artikel ini saya rasa cukup buat memahami gambaran bagaimana OpenStack Neutron itu sebenarnya.

&nbsp;

## Manajemen OpenStack
Untuk manajemen service-nya, OpenStack punya tiga fasilitas. Dashboard web GUI lewat service Horizon, bisa juga pakai Command Line Interface atau CLI, atau Application Programming Interface atau API.  

Dua yang awal tidak perlu banyak penjelasan, tinggal yang terakhir API. API ini interface buat pemrograman, pakai API ini developer atau programmer bisa buat program sendiri buat me-manage service OpenStack.  
Terus program itu berkomunikasi dengan OpenStack lewat API ini. Jadi API ini semacam perantara antara program yang dibuat programmer sama OpenStack.

&nbsp;

## Conclusion
Kalau Anda pengguna Linux yang bukan end user atau sekedar pengguna, atau Anda berada di industri IT, terutama Linux, menurut saya OpenStack layak untuk dipelajari. Kita lihat saja tren komputasi sekarang, data yang besar, masif, dan terpusat. 

Kalau dulu developer jualan software, sekarang software ditaruh di cloud terus dibuat layanan atau istilah kerennya sekarang Software as a Service (SaaS), Google Apps contohnya.

Google Apps ambil contoh saja seperti aplikasi perkantoran Google Docs. Kalau seperti Microsoft Office programnya dijual, tapi kalau Google Docs programnya tidak dijual tapi ditempatkan di cloud terus dijadikan layanan.  
User tinggal buka browser, kapan saja dari mana saja dan dari perangkat apa saja bisa pakai service program Google Docs.

Kalau misalnya perlu update software, atau ada problem sama programnya, itu juga bukan tanggung jawab user tapi Google.

Nah OpenStack bisa menjawab tren computing itu, OpenStack ini juga sebuah project Open Source yang besar karena sebagian besar leader di industri IT berkontribusi di OpenStack. Sebut saja seperti Rackspace, Red Hat, Ubuntu, Google, Intel, Cisco, dan masih banyak lagi yang terlibat di project ini.

Saya sendiri begitu sudah sedikit ngeh dengan OpenStack ini, saya merasa kagum sama sistem ini, dan seharusnya Anda juga.

Terakhir, saya minta bantuan Anda untuk share tulisan ini kalau menurut Anda tulisan ini bisa membantu buat pemula OpenStack.

&nbsp;

Terima kasih.

&nbsp;

**Artikel Berkaitan:**  
[Convert Database OpenStack Cinder dari Sqlite3 ke MySQL - Debian Jessie](//devnull.web.id/openstack/convert-database-openstack-cinder-dari-sqlite3-ke-mysql.html)  
_Kesalahan konfigurasi default OpenStack Cinder di Debian 8, dan bagaimana cara konversi database dari Sqlite3 ke MySQL_
