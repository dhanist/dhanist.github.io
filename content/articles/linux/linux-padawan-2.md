Title: Belajar Linux Dasar - Manajemen file
Date: 2016-05-02 20:02
Author: Dhani Setiawan
Category: Linux Padawan
Tags: Linux
Slug: linux-dasar-2
Status: published
Comments: yes

<div class="fimg">
  <img src="//devnull.web.id/images/linux/linux-cli.png" alt="Linux CLI" title="Linux CLI" />
</div>

Tulisan ini menyambung artikel sebelumnya, [Belajar Linux Dasar - Pengenalan Input & Ouput](/linux-padawan/linux-dasar-1.html).

Penggunaan program-program di artikel ini dibuat sederhana dengan maksud supaya para pengguna Linux yang baru, atau yang belum familiar dengan terminal bisa langsung ketik perintah tanpa harus membaca manual yang panjang dan <s>boring</s> lengkap itu. Kalau sudah sedikit ngerti baru baca manual lengkapnya, atau istilahnya RTFM (_Read The F[ine] Manual_).

Di artikel ini saya tuliskan tentang manajemen file, bagaimana cara membuat, rename, copy, cut, dan hapus file.

&nbsp;

Beberapa program yang dipakai:

- [**ls**](#ls), Untuk listing file dan direktori.
- [**mkdir**](#mkdir), Dipakai untuk membuat direktori baru.
- [**touch**](#touch), Update timestamp atau buat file baru.
- [**mv**](#mv), Move (cut + paste) dan rename file.
- [**cp**](#cp), Copy file dan direktori.
- [**rm**](#rm), Hapus file dan direktori.
- [**ln**](#ln), Untuk membuat link.

Di penulisan penggunaan program (synopsis), saya mengikuti Linux manual. Jadi argumen program di antara tanda [ dan ] bersifat opsional.

&nbsp;

###<a name="ls"></a>ls
**ls** dipakai untuk me-list nama-nama file dan direktori plus atributnya.  
Synopsis

    ls [OPTION] [FILE]

_ls_ kalau tidak disuplai argumen apa-apa akan me-list nama-nama file di current directory, working atau current directory bisa dilihat dengan perintah _pwd_. File atau folder hidden dengan nama berawalan . (dot) juga tidak di-print kecuali ada argumen -a (all).

**Contoh**  
Untuk me-listing file dan direktori di current directory, ketik ls tanpa argumen apa-apa.

    ls

Output dengan perintah ls di atas semua file terlihat sama, kita tidak bisa bedakan mana file mana folder, berapa besar file-nya, dsb.

Tergantung program terminal dan environmentnya, biasanya output ls ada warna-warna untuk membedakan tipe file, kalau tidak ada warna, coba ini:

    ls --color

Biarpun sudah dibedakan dengan warna, tetap tidak ada informasi kapan file-file itu terahir kali diakses, atau berapa ukurannya, atau siapa pemilik file itu. Supaya ls ada output informasi itu, pakai argumen -l.

    ls -l --color

Untuk list file dan direktori yang bukan di current directory, folder /tmp misalnya

    ls /tmp

Sudah dijelaskan di atas kalau file hidden dengan nama berawalan . (dot) tidak diprint, pakai argumen -a (all) kalau mau print termasuk yang hidden.

    ls -a ~

Dua atau lebih argumen bisa dijadikan satu, misalnya untuk list atribut file termasuk yang hidden.

    ls -la ~/

&nbsp;

###<a name="mkdir"></a>mkdir
**mkdir** dipakai untuk buat file direktori baru. saya sebut file karena memang di Unix dan Linux, direktori itu file, sama seperti file umumnya.  
Cara pakai mkdir:

    mkdir [OPTIONS] DIRECTORY

OPTIONS di sini opsional, boleh tidak dipakai. DIRECTORY adalah nama direktori yang mau dibuat.

**Contoh**  
Membuat direktori _blah_ di current directory:

    mkdir blah

Membuat direktori _blah_ dengan absolute path.

    mkdir /tmp/blah

Kalau kita mau buat direktori baru, sekalian buat juga parent directory-nya kalau belum ada, kita bisa pakai argumen -p (parent).

    mkdir -p blah/blah1/blah2/blah3

Dengan -p, mkdir tidak akan error kalau direktori yang dimaksud sudah ada.  
Perintah di atas itu untuk buat direktori _blah3_, kalau direktori parent-nya _blah2_ belum ada, maka dibuat juga. Begitu juga kalau folder _blah_ dan _blah1_ belum ada, maka akan dibuat juga.

Kalau kita mau buat banyak direktori baru, tidak perlu ketik perintah satu-satu.

    mkdir {blah, blah1, blah2}

Perintah ini untuk buat direktori _blah_, _blah1_, dan _blah2_ di current directory. Sebenarnya tanda { dan } bukan fitur mkdir, tapi Linux shell.

&nbsp;

###<a name="touch"></a>touch
**touch** dipakai untuk modifikasi timestamp, atau buat file baru kalau file yang dimaksud tidak ada. Timestamp adalah waktu terakhir file diakses dan dimodifikasi.

Synopsis

    touch [OPTION] FILE

**Contoh**  


    touch foo

Perintah itu, kalau file _foo_ tidak ada maka dibuat baru, tapi kalau ada maka waktu akses dan modifikasi file yang dirubah. Waktu bisa dilihat dengan perintah ls.

    ls -l foo

Tunggu beberapa menit, ulangi perintah _touch foo_ kemudian _ls -l foo_ dan perhatikan perbedaan outputnya.

&nbsp;

###<a name="mv"></a>mv
**mv** dipakai untuk rename atau move (cut + paste) file.

Synopsis

    mv [OPTION]... [-T] SOURCE DEST

SOURCE adalah file atau direktori asal, dan DEST adalah file atau direktori tujuan.

**Contoh**  
Rename direktori _blah_ ke _blah1_

    mv blah blah1

Pindahkan direktori _blah1_ ke /tmp

    mv blah1 /tmp

Atau misalnya mau pindahkan _blah1_ ke /tmp/ dengan nama berbeda, _blah2_ misalnya

    mv blah1 /tmp/blah2

Sangat simpel.

&nbsp;

###<a name="cp"></a>cp
**cp** dipakai untuk copy file.

Synopsis 

    cp [OPTION]... [-T] SOURCE DEST

Penjelasan SOURCE dan DEST sama dengan mv di atas.

**Contoh**  
Copy file _foo_ ke folder /tmp

    cp foo /tmp

Untuk copy _foo_ ke /tmp dengan nama berbeda, foo1 misalnya.

    cp foo /tmp/foo1

Copy direktori.  
Untuk copy direktori, gunakan argumen -r (recursive)

    cp -r blah /tmp/blah1

Program cp tidak ada output apa-apa kalau sukses, kalau mau print file-file yang dicopy pakai argumen -v (verbose), misalnya:

    cp -rv blah /tmp/blah1

&nbsp;

###<a name="rm"></a>rm
**rm** dipakai untuk menghapus file dan direktori.

Synopis

    rm [OPTION]   FILE

OPTION bersifat opsional, FILE adalah file yang mau dihapus.

**Contoh**  
Hapus file /tmp/foo

    rm /tmp/foo

Hapus direktori dengan option -r (recursive)

    rm -r /tmp/blah

Untuk hapus direktori, selain _rm -r_ juga bisa pakai _rmdir_.

Kadang beberapa file tidak bisa begitu saja dihapus, kita bisa pakai option -f (force) untuk file-file yang susah dihapus.

    rm -rf /tmp/blah

&nbsp;

###<a name="ln"></a>ln
**ln** dipakai untuk membuat file link.  

Di Linux ada file dengan tipe link. Link itu kurang lebih seperti shortcut kalau di Windows.

Jenis link di Linux ada dua, soft link dan hard link. Soft link cara kerjanya kurang lebih seperti shortcut, sedangkan hard link seperti alias.  

Soft link biasanya juga disebut dengan symbolic link atau pendeknya symlink.

Penjelasan untuk hard link agak low level, tapi saya akan coba jelaskan sedikit.

Misal saya buat file dengan nama _foo_, maka file _foo_ ini punya struktur data yang disebut inode, inode ini unik untuk setiap file dan untuk sederhananya inode ini anggap saja nomor.  

Misalnya inode untuk file _foo_ itu 100, nah kalau kita buat hard link ke _foo_ dengan nama _bar_, maka sama saja kita buat file baru  dengan nama _bar_ tapi dengan inode 100.  
Kita edit _foo_ maka _bar_ juga berubah, begitu juga sebaliknya. Tapi kalau kita hapus salah satu nama _foo_ misalnya, maka yang terhapus cuma _foo_, sedangkan inode 100 masih tetap ada, jadinya _bar_ juga masih ada.

<div class="aimg">
        <img src="//devnull.web.id/images/linux/link.png" alt="Linux link" title="Linux link" />
</div>

File di Linux cuma bisa terhapus kalau nama file untuk inode tertentu jumlahnya sama dengan 0, artinya kalau ada 5 hard link ke satu inode maka untuk benar-benar menghapus file, lima link tersebut harus dihapus.  
Terus lagi hard link tidak bisa cross device, artinya target file untuk link tidak bisa beda partisi atau hard disk, harus sama. Sedangkan symlink tidak ada batasan seperti itu.


**Contoh**  
Untuk membuat symlink ke file _foo_ dengan nama _bar_

    ln -s foo bar

Dengan symlink atau soft link, kalau kita hapus file target _foo_, maka _bar_ disebut broken link. _bar_ mengarah ke _foo_ tapi _foo_ tidak ada.

Sedangkan untuk hard link

    ln foo bar

Dengan hard link, _foo_ dan _bar_ mengarah ke satu inode jadi seolah-olah file _foo_ dan _bar_ seperti file kembar yang selalu sinkron. Edit _foo_ maka _bar_ berubah, begitu juga sebaliknya. Hapus _foo_, _bar_ masih bisa diakses.

Demonstrasi penggunaan link dengan hard link.

    [dhani: ~] Endor > touch foo
    [dhani: ~] Endor > echo "abcd" > foo
    [dhani: ~] Endor > cat foo
    abcd
    [dhani: ~] Endor > ln foo bar
    [dhani: ~] Endor > cat bar
    abcd
    [dhani: ~] Endor > echo "1234" > bar
    [dhani: ~] Endor > cat foo
    1234
    [dhani: ~] Endor > rm foo
    rm: remove regular file ‘foo’? y
    [dhani: ~] Endor > cat bar
    1234
    [dhani: ~] Endor > rm -f bar
    [dhani: ~] Endor >

&nbsp;

Saya rasa program-program ini tidak susah dipahami. Dan kalau perlu memahami lebih lagi tentang program-program di atas, langsung saja, ahem... <s>RTFM</s>, maksud saya baca manual masing-masing program dengan ketik perintah _man &lt;program&gt;_.

misalnya untuk program mkdir:

    man mkdir

Kita lanjut lagi di tulisan berikutnya dengan program-program yang lain, Insya Allah.

&nbsp;

[Edit]  
Artikel selanjutnya: [Belajar Linux Dasar - Manipulasi Teks dan Stream](//devnull.web.id/linux-padawan/linux-dasar-3.html)
