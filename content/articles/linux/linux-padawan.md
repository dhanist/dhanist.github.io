Title: Belajar Linux Dasar - Pengenalan Input & Output
Date: 2016-04-22 13:02
Author: Dhani Setiawan
Category: Linux Padawan
Tags: Linux
Slug: linux-dasar-1
Status: published
Comments: yes

<div class="fimg">
  <img src="/images/term.png" alt="Linux Terminal" title="Linux Terminal" />
  <p>Photo credit: pixabay.com</p>
</div>
GNU/Linux atau sebutan gampangnya Linux, hari ini sudah berbeda jauh sekali dibanding Linux dulu. Linux pada zaman dahulu kala identik dengan sistem operasi yang susah dan cuma orang-orang komputer saja yang pakai Linux. Sekarang Linux sudah gampang, tanpa perlu paham command pun pengguna sudah bisa pakai Linux.  

Dulu waktu pertama belajar Linux, saya bingung waktu masukkan flash disk tapi di layar tidak muncul apa-apa. Putar mp3 tapi tidak ada suara apa-apa yang keluar, mau putar mp3 saja perlu perjuangan.  
Syukurnya sekarang para pengguna baru tidak perlu melalui hal-hal ribet itu, cukup install dan siap pakai.

Tapi ada hal lain, buat pengguna yang berencana menjadi Linux admin atau berencana membuat server dengan Linux, maka belajar command atau perintah-perintah Linux tetap harus dikuasai. Mau tidak mau tetap harus buka terminal dan ketik perintah.  
Karena itu tulisan ini saya kategorikan di Linux Padawan. Padawan kalau di film Star Wars adalah seorang yang sedang belajar menjadi seorang master Jedi.

Entah mengapa saya merasa resource pembelajaran Linux berbahasa Indonesia masih minim, mungkin juga Saya salah tapi lihat saja situs seperti [linux.or.id](http://linux.or.id). Benar atau salah tapi asumsi itu yang membuat Saya menulis artikel ini.

Saya berniat menulis artikel tentang perintah-perintah Linux yang sering dipakai, ada kemungkinan juga akan berkelanjutan. Dimulai dari pengenalan Input dan Output sampai ke program.  
Di Linux, ada package software yang namanya GNU Coreutils. Ini berisi set program-program standar yang pasti ada di setiap distribusi Linux. Tulisan ini akan coba menjelaskan penggunaan program-program Coreutils yang sering dipakai, dan kalau dirasa kurang akan ditambah dengan program-program yang lain.

Sebelum ke program, kita perlu pahami beberapa hal dasar di Linux. Yaitu I/O (Input/Output), pipe, redirection, dan struktur direktori.

&nbsp;

**Input/Output**  
Apa yang kita ketik di terminal termasuk input, dan yang keluar dari terminal namanya output.  
Input tidak harus ada di terminal, begitu juga output. Input dan output bisa berupa file.  
Misal kita mau print isi file /etc/passwd dengan command cat

    cat /etc/passwd

cat adalah programnya, file /etc/passwd inputnya. Outputnya diprint di terminal

Linux punya special device untuk I/O, yaitu standard input atau _**stdin**_, standard ouput disebut _**stdout**_, dan standard error _**stderr**_.  

- stdin: Input yang ditulis atau diprint di terminal.
- stdout: Output normal dari program.
- stderr: Output program untuk pesan error.

Jadi jenis input di Linux ada dua, file dan terminal (stdin). Sedangkan jenis output ada tiga, file, output di terminal (stdout), dan output terminal kalau error (stderr).

&nbsp;

**Pipe**  
Ada fitur menarik di Unix dan Linux, output dari satu program bisa dijadikan input program lain, caranya dengan memakai pipe. Disebut pipe mungkin karena cara kerjanya seperti pipa, menghubungkan output dan input. 
Pipe dilambangkan dengan karakter |.

Contoh, kita mau lihat uid dari nama user nobody. Kita pakai dua program, cat dan grep. Output dari cat dijadikan input program grep dengan pipe.

    cat /etc/passwd | grep "nobody"

    # Output yang terprint di terminal (stdout) seperti dibawah
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin

Maksud dari command di atas, cat /etc/passwd untuk print isi file /etc/passwd ke terminal, sedangkan grep "nobody" untuk filter baris teks yang ada tulisan nobody.  
Ouput dari _cat /etc/passwd_ tidak diprint ke terminal tapi diarahkan ke pipe. Pipe ini kemudian mengambil output dari perintah pertama dan menjadikannya input untuk perintah ke dua _grep "nobody"_.  
Ringkasnya, print isi file /etc/passwd tapi cuma baris yang ada kata nobody saja. Dari output kita tahu uid user nobody adalah 65534, lain sistem hasilnya bisa beda.

Pipe tidak terbatas dua program saja, lebih dari dua juga bisa, misalnya.

    cat /etc/passwd | grep "nobody" | awk -F: '{print $3}'

&nbsp;

**Redirection**  
Fitur lain lagi, namanya redirection.  
Kita bisa me-redirect atau memindahkan output atau input program. Misalnya, program yang outputnya ke stdout atau ke terminal bisa diredirect atau dipindahkan ke file, output dari stderr diredirect ke stdout, dan sebagainya.

- Karakter > untuk redirect output.
- Karakter < untuk redirect input.

Contohnya, command di atas _cat /etc/passwd | grep "nobody"_ outputnya tidak harus terminal, kita bisa redirect atau arahkan output ke file user misalnya.

    cat /etc/passwd | grep "nobody" > user

Command di atas tidak ada output apa-apa di terminal karena output kita redirect atau pindahkan ke file user. Di file user, isinya sama saja dengan output perintah yang pertama. 

    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin

Untuk redirect input, kita gunakan karakter <  

Contoh untuk menghitung jumlah baris file /etc/passwd.

    wc -l /etc/passwd
    
    # Output di stdout
    62 /etc/passwd

62 adalah jumlah baris, /etc/passwd adalah nama file.  
Sekarang dengan redirect input.

    wc -l < /etc/passwd
    
    # Output di stdout
    62

Maksud dari command wc -l yang ke dua, file /etc/passwd diredirect ke stdin dan kemudian dijadikan input perintah wc -l.  
Perhatikan perbedaan output dari kedua perintah. Yang pertama ada file /etc/passwd, yang ke dua tidak ada karena perintah wc -l mengambil input dari stdin, bukan file /etc/passwd.

Ada mode lain di redirect, dengan dua karakter redirection << atau >>.  
Bedanya dengan dua karakter, modenya adalah append.

Langsung saja dengan contoh.

    cat /etc/passwd | grep "nobody" > user

Command ini kalau diulang 5 kali, isi file user tetap sama.
    
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin

Tapi dengan mode append, atau dua karakter redirect

    cat /etc/passwd | grep "nobody" >> user

Isi file user kalau command diulang lima kali.

    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin

Dengan dua karakter redirect, output atau input ditambahkan di bawahnya.

&nbsp;

**Struktur Direktori Linux**  
Di Linux, tidak ada drive C: atau drive D: seperti di Windows.

Di Linux, gambaran struktur direktori seperti di bawah:

    /                           # root
     |
     |-- home                   # Direktori untuk user
     |
     |-- etc                    # /etc: direktori yang berisi konfigurasi
     |   
     |-- tmp                    # /tmp: temporary
     |   
     |-- usr
     |       /
     |
     |       |--  bin           # /usr/bin: Berisi executable program
     |       |    
     |       |--  lib           # /usr/lib: Berisi library program
     |       |
     |       |--  share
     |       |    
     |       |--  local
     |                 /
     |                  | 
     |                  |-- bin
     |                  |
     |                  |-- lib
     |                  | 
     |                  |-- share
     |-- dev                            # /dev: Berisi device node
     |       /
     |       |--  disk
     |
     |-- var
            /
             |
             |-- lib
             |   
             |-- log
             |   
             |-- cache

Seperti terlihat, struktur direktori seperti percabangan pohon. Paling atas disebut root, karakter / dan diikuti cabangnya, misal /usr/local/share.

Kalau di Windows, biasanya program yang terinstall ada di direktori C:\Program Files\. Di Linux berbeda, program yang terinstall filenya tersebar di beberapa direktori.  
Misalnya program Vlc player, program executablenya di /usr/bin/vlc. Library-nya terinstall di /usr/lib/vlc, dokumentasi di /usr/share/vlc.  
Kelebihannya dari Windows, kalau ada beberapa program membutuhkan library yang sama, atau istilahnya shared library, cukup memakai library yang sudah ada di direktori /lib, /usr/lib, atau /usr/local/lib. Satu libarary dipakai bersama-sama, dan hasilnya ukuran program jadi kecil.

Struktur direktori Linux mengikuti standar FHS (Filesystem Hierarchy Standard) [Wikipedia](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard), silahkan dipelajari.

&nbsp;

**Absolute dan relative path**  
Absolute path adalah path yang dimulai dari / (root), misalnya /etc/passwd.  
Relative path, path yang dimulai dari current directory atau working directory. Current directory bisa diketahui dengan command pwd.

    # Dengan absolute path
    cat /etc/passwd

    # Dengan relative path
    $ cd /etc           # cd /etc, pindah working directory ke /etc
    $ cat passwd

Command cat yang ke dua tidak perlu /etc karena working directory adalah /etc.

&nbsp;

**Navigasi**  
Ada beberapa karakter spesial untuk navigasi direktori.

- .  (dot): current directory.
- .. (double dot): naik satu direktori.
- ~  (tilde): home directory.

Contoh:

    $ cd /usr/local/share       # Pindah ke direktori /usr/local/share
    $ cd .                      # Tetap di tempat.
    $ pwd                       # Print working directory
    /usr/local/share
    $ cd ..                     # Naik satu direktori
    $ pwd
    /usr/local
    $ cd ..
    $ pwd
    /usr
    $ cd ~                      # Pindah ke home directory
    $ pwd
    /home/administrator

&nbsp;

Setelah paham hal di atas, maka nantinya tidak akan bingung kalau ketemu command yang ada karakter aneh seperti |, >, .., ~, dan seterusnya.

Di tulisan selanjutnya kita akan mulai bahas program-program dari Coreutils.

Terima kasih.

&nbsp;

[EDIT]  
Artikel selanjutnya: [Belajar Linux Dasar - Manajemen file](//devnull.web.id/linux-padawan/linux-dasar-2.html)
