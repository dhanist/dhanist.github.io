Title: Belajar Linux Dasar - File Permission
Author: Dhani Setiawan
Date: 07-24-2016
Status: Published
Comment: Yes
Slug: linux-dasar-4
Category: Linux Padawan
Tags: Linux

Selamat pagi, siang, atau malam teman-teman Linuxers. Tulisan ini yang keempat seri pembelajaran Linux dasar, buat teman-teman yang belum baca tulisan sebelumnya, ini link-nya:

1. [Belajar Linux Dasar - Pengenalan Input & Output](//devnull.web.id/linux-padawan/linux-dasar-1.html)
2. [Belajar Linux Dasar - Manajemen file](//devnull.web.id/linux-padawan/linux-dasar-2.html)
3. [Belajar Linux Dasar - Manipulasi Teks dan Stream](//devnull.web.id/linux-padawan/linux-dasar-3.html)

Yang keempat ini kita bakal belajar tentang permissions. Permission ini kurang lebih seperti cara mengatur siapa yang bisa berbuat apa di file tertentu. Satu orang cuma bisa baca saja, orang lainnya bisa baca sama edit file, dan sebagainya. 

Buat memahami permission, paling tidak ada dua hal yang perlu kita pahami, yaitu pengelompokan user sama mode akses nya. Cara manipulasi permission dan penjelasan tentang SUID, SGID, dan Sticky bit juga ada di tulisan ini.

&nbsp;

## User, Group, dan Other.
Ada tiga jenis user di Unix dan Linux yang berhubungan dengan file permission; mereka itu _User_, _Group_, dan _Other_. Seperti apakah mereka? di bawah:

**User**  
Ini user yang punya file atau pemilik file. Kalau misalnya saya buat file bernama "blah" pakai command `touch blah`, maka file `blah` ini punya Saya, kecuali kepemilikan atau ownership file ini dialihkan ke user lain pakai command `chown`.

Di Linux masing-masing user punya id yang unik. Kalau kita mau cek nama user kita yang lagi login, pakai command `whoami`.

    whoami

Kalau mau cek nomor id user kita yang lagi login:

    id -u $(whoami)

Untuk nama-nama user yang lain bisa dilihat di file `/etc/passwd`.

**Group**  
Beberapa user bisa digabungkan ke dalam satu grup. Sama seperti _User_, _Group_ ini masing-masing juga punya nama dan nomor id yang unik.

Nama-nama grup bisa dilihat di file `/etc/group`. Kalau kita mau lihat user yang kita pakai sekarang tergabung di grup mana saja, ketik command `id`.

**Other**  
Kalau yang ini berlaku buat semua user yang bukan pemilik file, juga tidak tergabung dalam grup pemilik file.

&nbsp;

## Mode akses.
Berikutnya mode akses. Mode akses, atau permission ini yang menentukan hak akses masing-masing user yang sudah dijelaskan sebelumnya.  
Setiap file, termasuk file direktori punya tiga mode akses seperti di bawah:

1. **read**. User yang punya akses **read** dia bisa melihat isi file atau melihat atribut file.
2. **write**. User yang punya akses **write** berarti dia bisa update, edit, rename, move dan hapus file.
3. **execute**. Mode akses yang ini biasanya cuma diterapkan ke file program atau script, file program atau script tidak bisa dieksekusi kalau tidak punya mode **execute**. Jadi user yang punya akses **execute** ke file, dia bisa mengeksekusi file program atau script itu.

&nbsp;

Berikutnya coba kita lihat contoh output command `ls -l`

    ls -l blah 
    -rwxr-xr-- 1 administrator admins 0 Jul 19 13:45 blah

File `blah` di atas itu kepunyaan user `administrator` sama grup `admins`.  
Permission-nya ada di kolom yang pertama, itu yang `-rwxr-xr--`.  
bagaimana cara bacanya ini?

<div class="aimg">
  <img src="//devnull.web.id/images/linux/lp/perm.png" />
</div>

Keterangannya seperti ini:

**1) File type**  
Karakter yang pertama itu menunjukkan jenis file, ada beberapa tipe seperti list di bawah:

- `-` : Regular file atau gampangnya file biasa.
- `d` : File direktori atau folder, seperti yang dibuat pakai command `mkdir`.
- `l` : Menunjukkan file jenis link seperti yang dibuat pakai command `ln -s`.
- `b` : Block device, seperti flash disk, partisi hard drive, dsb.
- `c` : File character class seperti serial console.
- `s` : File socket jenis Unix.

**2) User permission**  
Permission ini berlaku buat pemilik file. Dalam contoh ini `rwx` yang berarti si user pemilik file bisa **baca (r)**, **edit, rename, move dan hapus (w)**, dan **execute (x)**.

**3) Group Permission**  
Permission yang ini berlaku buat grup pemilik file, grup ini isinya bisa nol user atau lebih. Di contoh, permission untuk grup `r-x` yang berarti para user yang tergabung di grup ini, mereka bisa **baca (r)** dan **execute (x)** tapi tidak bisa edit, rename, move atau hapus file karena grup ini tidak punya permission **write (w)**.

**4) Other Permission**  
Triad permission yang terakhir ini berlaku buat semua user selain nomor 2 dan nomor 3 di atas. Di contoh ini, para user yang tergolong **other** cuma bisa baca file karena cuma ada permission baca atau **read (r)**.

&nbsp;

## Manipulasi Permission
Hak akses atau permission untuk ketiga jenis user; user, group, dan other itu tidak statik yang artinya permission ini bisa dirubah. Untuk merubah permission kita pakai command `chmod`.

Kalau mau rubah permission, kita bisa pilih salah satu dari dua mode `chmod`, mode text sama numeric.  
Kita lihat satu-satu.

**Mode text**  
Mode chmod yang ini pakai karakter huruf untuk masing-masing jenis user:

- `u` : yang berarti user pemilik file.
- `g` : grup pemilik file.
- `o` : other.
- `a` : semua user `u`, `g`, dan `o`. Kita bisa pakai `a` ini daripada harus ketik `ugo`.


Contoh untuk set permission grup supaya bisa baca, edit dan hapus file:

    # chmod g=rw blah
    # ls -l blah 
    -rwxrw-r-- 1 administrator admins 0 Jul 19 13:45 blah

Supaya `other` tidak punya permission apa-apa, tidak bisa baca, edit dan execute:

    # chmod o= blah
    # ls -l blah 
    -rwxrw---- 1 administrator admins 0 Jul 19 13:45 blah

User pemilik file dengan akses penuh:

    # chmod u=rwx blah
    # ls -l blah 
    -rwxrw---- 1 administrator admins 0 Jul 19 13:45 blah

Semua user punya akses penuh:

    # chmod ugo=rwx blah
    # ls -l blah 
    -rwxrwxrwx 1 administrator admins 0 Jul 19 13:45 blah

Selain `ugo` bisa juga pakai `a` untuk semua user.

    # chmod a=rwx blah

Di mode ini, selain pakai tanda sama dengan `(=)`, kita juga bisa pakai tanda minus `(-)` atau plus `(+)`.  
Misalnya kalau `g=rwx` itu berarti berikan hak akses penuh ke grup, `g-w` berarti hilangkan permission `w` dari grup. `g+w` berarti tambahkan permission `write (w)` ke grup.

Contoh, kita hilangkan permission `w` dan `x` dari _group_ dan _other_.

    # chmod go-wx blah
    # ls -l blah
    -rwxr--r-- 1 administrator admins 0 Jul 19 13:45 blah

&nbsp;

**Mode Numeric**  
Kalau mode yang ini kita tidak pakai huruf-huruf seperti `u`, `g`, atau `o`, tapi pakai angka oktal. Oktal? Bilangan yang angkanya cuma 8, dari 0 sampai 7.

Caranya begini, tiga permission `r`, `w`, dan `x` anggap saja seperti tiga kolom terus masing-masing kolom ini punya switch atau saklar on/off pakai bilangan biner yang bersifat boolean. Bilangan biner angkanya cuma `1` sama `0`, `1` berarti hidup dan `0` berarti mati.

Contoh **`r-x`** berarti **`101`**, **`rwx`** berarti **`111`**, **`r--`** berarti **`100`**.  
Angka **`101`** yang mewakili **`r-x`** itu bilangan biner, jadi angka **`101`** bukan berarti seratus satu, tapi **`5`** kalau dalam oktal.

`chmod` mode numeric pakai tiga angka oktal; angka pertama mewakili permission untuk user, angka kedua mewakili group, dan angka ketiga mewakili permission other.

Contoh untuk set permission jadi `rwxr-xr--` :

    # chmod 754 blah

command di atas kalau dalam mode text seperti ini :

    # chmod u=rwx,g=rx,o=r blah

Saya rasa gambar lebih bisa menjelaskan mode numeric ini.

<div class="aimg">
  <img src="//devnull.web.id/images/linux/lp/754.png" />
</div>

Gampangnya bisa kita ingat mode-mode permission-nya seperti ini :

- `r` = 4, atau dalam biner ditulis `100`.
- `w` = 2, dalam biner ditulis `010`.
- `x` = 1, dalam biner ditulis `001`.

Jadi `rwx` sama dengan `421` yang kalau angka-angka ini dijumlahkan sama dengan 7.  
`r-x` berarti `401`, dijumlahkan jadi 5.
`r--` berarti `400`, ketiga angka ini dijumlahkan hasilnya 4.

Itulah kenapa `754` sama dengan `rwxr-xr--`

Contoh lain, mode `644` :

    # chmod 644 blah
    # ls -l blah
    -rw-r--r-- 1 administrator admins 0 Jul 19 13:45 blah

Mode `644` dengan gambar.

<div class="aimg">
  <img src="//devnull.web.id/images/linux/lp/644.png" />
</div>

Mode `777`

    # chmod 777 blah
    # ls -l blah
    -rwxrwxrwx 1 administrator admins 0 Jul 19 13:45 blah

<div class="aimg">
  <img src="//devnull.web.id/images/linux/lp/777.png" />
</div>

Biar lebih gampang lagi, kita bisa lihat tabel di bawah:

| **chmod numeric** | **Oktal** | **Biner** | **Teks** |
|:-----------------:|:---------:|:---------:|:--------:|
|        `0`        |  `0+0+0`  |   `000`   |  ` ---`  |
|        `1`        |  `0+0+1`  |   `001`   |   `--x`  |
|        `2`        |  `0+2+0`  |   `010`   |   `-w-`  |
|        `3`        |  `0+2+1`  |   `011`   |   `-wx`  |
|        `4`        |  `4+0+0`  |   `100`   |   `r--`  |
|        `5`        |  `4+0+1`  |   `101`   |   `r-x`  |
|        `6`        |  `4+2+0`  |   `110`   |   `rw-`  |
|        `7`        |  `4+2+1`  |   `111`   |   `rwx`  |

Buat Saya, pakai numeric ini lebih ringkas daripada harus pakai `u`, `g`, atau `o`.

&nbsp;

## SUID, SGID, Sticky bit.
Pernah pakai command `sudo`? Ya, pakai command `sudo` kita bisa jalankan program pakai user lain, root misalnya.

**SUID** atau _Set User ID_ ini kurang lebih seperti `sudo` tapi tanpa perlu pakai perintah `sudo`. SUID ini cuma bisa dipakai di file executable seperti file program. Artinya file program executable yang ada flag _suid_ kalau dieksekusi, maka sistem Linux menjalankan prosesnya dengan user pemilik file, bukan user yang mengeksekusinya.

Contoh file `/usr/bin/passwd`.

    ls -l /usr/bin/passwd
    -rwsr-xr-x 1 root root 53112 Nov 20  2014 /usr/bin/passwd

Coba kita perhatikan di permission yang pertama `(rws)`, karakter `s` menandakan SUID.  
File itu punya user root dan dengan suid, siapapun bisa mengeksekusi file itu dan sistem akan menjalankannya dengan user `root`. Karena itu user reguler bisa mengganti passwordnya sendiri biarpun tidak punya akses `write` ke file `/etc/passwd`.

**SGID** atau _Set Group ID_ kurang lebih seperti `SUID` hanya saja untuk `group`. Jadi program dengan sgid yang dijalankan oleh siapapun dianggap `group` yang mengeksekusinya.

    ls -l /usr/bin/bsd-write 
    -rwxr-sr-x 1 root tty 9680 Oct 18  2014 /usr/bin/bsd-write

Sama seperti SUID, karakter `s` menandakan sgid tapi di permission triad yang tengah.

**Sticky bit** ini berguna buat mencegah file dihapus oleh user yang bukan pemilik file, biarpun di dalam direktori publik yang open access.

Contohnya direktori `/tmp`. Direktori ini punya mode `777` yang artinya siapa saja punya akses penuh ke file-file yang ada di direktori ini, siapa saja bisa buat dan hapus file. Tapi kalau ada **Sticky bit**, file tidak bisa dihapus, move, atau rename begitu saja oleh sembarang user, cuma user pemilik dan user `root` saja yang bisa hapus, move, atau rename.

    ls -ld /tmp
    drwxrwxrwt 16 root root 4096 Jul 20 15:15 /tmp

Karakter pertama `(d)` menandakan file `/tmp` itu file direktori. Tiga karakter berikutnya `(rwx)` artinya user pemilik folder `/tmp` punya akses penuh. Tiga karakter berikutnya untuk group `(rwx)` yang juga berarti akses penuh. Terakhir `(rwt)` untuk _Other_ yang berarti _read_, _write_, dan _sticky bit_. Jadi karakter `t` itu menandakan _sticky bit_.

&nbsp;

### Bagaimana set SUID, SGID atau Sticky bit?
Sama seperti setting permission hanya saja kita pakai 4 angka, angka pertama untuk suid, sgid, dan sticky bit, tiga angka berikutnya permission untuk user, group, dan other.

Angka oktal kurang lebih sama seperti permission `rwx`.

- SUID : 4 atau dalam biner 100.
- SGID : 2 atau dalam biner 010, dan.
- Sticky bit : 1 atau 001 dalam angka biner.

Contoh untuk set suid dan permission 755 di file `blah` :

    # chmod 4755 blah
    # ls -l blah
    -rwsr-xr-x 1 administrator admins 0 Jul 19 13:45 blah

Set SGID:

    # chmod 2755 blah
    # ls -l blah
    -rwxr-sr-x 1 administrator admins 0 Jul 19 13:45 blah

Untuk Sticky bit:

    # chmod 1755 blah
    # ls -l blah
    -rwxr-xr-t 1 administrator admins 0 Jul 19 13:45 blah

Kita bisa set dua flag atau lebih, misal `suid + sgid` yang berarti `4 + 2 = 6`.

    # chmod 6755 blah
    # ls -l blah
    -rwsr-sr-x 1 administrator admins 0 Jul 19 13:45 blah

Atau `suid + sticky bit` yang berarti `4 + 1 = 5`.


    # chmod 5755 blah
    # ls -l blah
    -rwsr-xr-t 1 administrator admins 0 Jul 19 13:45 blah

Selain mode numeric, kita juga bisa pakai mode text:

- SUID : s.
- SGID : s.
- Sticky bit : t.

`chmod u+s` untuk set suid, `chmod g+s` untuk set sgid, dan `chmod o+t` untuk set sticky bit.

&nbsp;

## Merubah Ownership
Ownership, atau kepemilikan file baik _user_ atau _group_ bisa diganti atau dialihkan ke user atau group lain.

Untuk merubah user ownership pakai command `chown`. Contoh merubah kepemilikan file `blah` yang awalnya punya user `administrator` dialihkan ke user `root`.

    # ls -l blah
    rwx-r-xr-x 1 administrator admins 0 Jul 19 13:45 blah
    # chown root blah
    # ls -l blah
    rwx-r-xr-x 1 root admins 0 Jul 19 13:45 blah

Untuk mengganti _group_ kita pakai command `chgrp`. Contoh rubah group admins ke group root.

    # chgrp root blah
    # ls -l blah
    rwx-r-xr-x 1 root root 0 Jul 19 13:45 blah

Kita juga bisa rubah user sama grupnya pakai satu command `chown`. Di bawah contoh buat rubah user ke `administrator` dan grup ke `admins`.

    # chown administrator:admins blah
    # ls -l blah
    rwx-r-xr-x 1 administrator admins 0 Jul 19 13:45 blah

Jadi, user dan grup dipisahkan dengan titik dua `(:)`.

Semua command di atas; `chmod`, `chown`, dan `chgrp` bisa juga dipakai di direktori secara recursive. Artinya kalau kita rubah satu direktori, semua file sama direktori yang ada di dalamnya semua ikut berubah tanpa perlu eksekusi command ke file satu per satu.

Untuk recursive pakai argumen `-R`. Contoh, supaya tidak ada yang bisa baca isi folder `Documents` selain yang punya.

    chmod -R 600 Documents

Dengan `-R` semua file dan folder termasuk isinya semua permission-nya berubah.

&nbsp;

Baik, semoga tulisan tentang Linux file permission ini bisa dipahami dengan mudah.  
Silahkan dikomentari, kritik, share, atau abaikan.

&nbsp;

Terima kasih.
