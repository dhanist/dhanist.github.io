Title: Belajar Linux Dasar - Manipulasi Teks dan Stream
Date: 2016-05-20 02:47
Author: Dhani Setiawan
Category: Linux Padawan
Tags: Linux
Slug: linux-dasar-3
Status: published
Comments: yes


<div class="fimg">
  <img src="//devnull.web.id/images/linux/regex.png" alt="regex" title="Regular Expression" />
  <p>Image source: www.linuxnix.com</p>
</div>

Selamat pagi, siang, atau malam. Selamat datang kembali di seri pembelajaran Linux Dasar. Kalau Anda baru bergabung, Anda bisa lihat tulisan sebelumnya lewat link di bawah:

1\. [Belajar Linux Dasar - Pengenalan Input & Output](//devnull.web.id/linux-padawan/linux-dasar-1.html)  
2\. [Belajar Linux Dasar - Manajemen file](//devnull.web.id/linux-padawan/linux-dasar-2.html)

Di artikel ini saya tuliskan tentang manipulasi teks dan stream. Teks sudah jelas, tapi stream?  
Stream itu stdin, stdout, dan stderr yang sudah dibahas di tulisan yang pertama, proses manipulasi stream ada di I/O itu.

Jadi misalnya input program dari stdin itu ``A``, keluar di stdout berubah jadi ``B``, nah proses merubah ``A`` ke ``B`` ini disebut manipulasi stream.

Tahukan Anda? bahwa salah satu the greatest strength, atau kekuatan terbesar Unix dan Linux itu ada di kemampuannya memanipulasi teks dan stream.  
Saya paham itu, karena dulu sekali saya juga pengguna Windows, dan tidak ada hal yang seperti ini di Windows. 

Karena itu sebagai Linux Engineer, hal yang satu ini wajib dikuasai. Sejenak kita tinggalkan GUI, pakai command dan rasakan kekuatan Linux sebenarnya.

Benar GUI sudah maju, tapi sehebat-hebatnya GUI tidak bisa menandingi fitur teks dan stream manipulation ini. Pelajari dan buktikan sendiri.

Baik, kita lihat apa saja program yang dibahas kali ini:

1. [Wildcard & Regular Expression](#wildcard-n-regex)
2. [cut](#cut)
3. [head & tail](#head-n-tail)
4. [tr](#tr)
5. [sort](#sort)
6. [uniq](#uniq)

Selain program di atas, saya juga tambahkan beberapa program yang bukan dari Coreutils. Program-program ini krusial dan penting.

1. [more & less](#more-n-less)
2. [awk](#awk)
3. [grep](#grep)
4. [sed](#sed)

&nbsp;

## <a name="wildcard-n-regex"></a>Wildcard & Regular Expression
Pernah lihat command yang mirip seperti ini?

    grep '^[0-9]{1,3}.*$' data.txt

Karakter-karakter aneh itu namanya karakter Regular Expression atau regex atau regexp.

Wildcard dan regex itu karakter-karakter spesial yang diartikan secara berbeda oleh shell atau program.

Mungkin Anda bertanya, apa pentingnya saya memahami ini?  
Sebenarnya tanpa paham wildcard atau regex, kita sudah bisa pakai command di shell Linux. Tapi dengan sedikit memahami ini, banyak task yang ribet
bisa jadi mudah.

Menurut saya tidak ada ruginya pelajari wildcard sama regex.

Wildcard sama regex ini fungsinya kurang lebih sama, mencari pola karakter dalam string. Bedanya, karakter wildcard diproses di Linux Shell seperti
bash, dash, dan lainnya. Regex diproses oleh program, contoh di atas itu pakai program ``grep``.

### Wildcard 
Wildcard ini karakter-karakter spesial di shell Linux. Pakai wildcard kita bisa beroperasi di banyak file sekaligus.

Masing-masing karakter wildcard artinya beda-beda, saya list dan jelaskan satu-satu.

- **\***: Asterisk atau tanda bintang.
- **?**: Question mark atau tanda tanya.
- **[]**: Square bracket atau kurung siku.
- **[!]**: Exclamation mark, tanda seru dalam kurung siku.
- **{}**: curly bracket atau kurung kurawal, dan.
- **\\**: Backslash.

**Asterisk (\*)**  
Tanda bintang atau asterisk mewakili karakter apa saja, jumlahnya bisa berapa saja termasuk nol.

Jadi ``mp*`` bisa berarti ``mp``, ``mp3``, ``mp4``, atau ``mp`` apa saja.

Misalnya saja kita punya tiga file dengan nama berbeda:

    touch a.txt
    touch ab.txt
    touch abc.txt

Kita punya tiga file ``a.txt``, ``ab.txt``, dan ``abc.txt``.  
Kita bisa filter output ls pakai bintang

    ls a*.txt
    abc.txt  ab.txt  a.txt

Jadi, tanda bintang itu mewakili karakter apa saja, dengan jumlah berapapun.  
``a*.txt`` artinya huruf ``a`` diikuti karakter apa saja, jumlahnya berapa saja diikuti dengan ``.txt``.

**Tanda tanya (?)**  
Karakter ini (?) mewakili karakter apa saja, tapi jumlahnya satu.

Contohnya kalau kita mau filter command ``ls`` untuk tipe file ``mp3``, ``mp4`` misalnya:

    ls *mp?

``*mp?`` artinya, karakter apa saja dengan jumlah berapa saja, diikuti karakter ``mp``, dan diikuti satu karakter apa saja.

Jadi ``ls *mp?`` akan match file dengan ekstensi ``mp3``, ``mp4``, ``mpg``, ``mp2``, dan ``mp apa saja``.

**Square bracket ([])**  
Karakter yang ada di dalam kurung siku adalah satu set karakter. Gampangnya kita bisa baca set karakter di kurung siku ini dengan _``atau``_.

Contoh, ``[abc]`` bisa dibaca ``a`` atau ``b`` atau ``c``.

Misalnya kita mau filter output command ``ls`` untuk tipe file ``jpg`` dan ``mpg``

    ls *.[mj]pg

Jadi, ``*.[mj]pg`` bisa dibaca karakter apa saja dengan jumlah berapa saja, diikuti ``tanda titik (.)``, terus diikuti karakter ``m`` atau ``j``, dan diikuti karakter ``pg``.

**Tanda seru dalam kurung siku ([!])**  
Ini sama dengan yang sebelumnya, hanya saja kebalikannya. Kalau ``[mj]`` berarti ``m`` atau ``j``, ``[!mj]`` berarti apa saja selain ``m`` dan ``j``.

**Curly backets atau kurung kurawal ({})**  
Kalau kurung siku bisa dibaca _``atau``_, kurung kurawal ini bisa dibaca _``dan``_. Bedanya juga, di kurung kurawal masing-masing pattern dipisah pakai koma.

Jadi ``{o,p}df`` berarti ``odf`` dan ``pdf``.

Contoh saja, dari pada kita hapus satu-satu file ``pdf`` dan ``odf``, kita bisa pakai satu command.

    rm *.{o,p}df

**Backslash (\)**  
Ini untuk escape karakter spesial. Kalau tanda tanya ``?`` berarti satu karakter apa saja, tapi kalau ditempatkan backslash didepannya ``\?``, tanda tanya itu jadi hilang arti spesialnya, dan cuma berarti tanda tanya.

&nbsp;

### Regular Expression
Regex ini karakternya sedikit lebih kompleks dari wildcard. Oke, bukan sedikit, tapi jauh lebih kompleks.

Perhatikan set karakter regex dibawah.

    ^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$

Biarpun terlihat rumit, arti regex di contoh itu cuma email address. Cuma gambaran saja bahwa Regular Expression karakternya lebih banyak dibanding wildcard.

Seperti yang saya sebutkan di atas, regex ini prosesnya bukan di shell, tapi di program. Jadi command seperti di bawah ini tidak valid.

    ls ^[abc]

Tidak valid karena penggunaan regex di shell.

Apa saja karakter Regular Expression?

**Dot atau tanda titik (.)**  
    Artinya satu karakter apa saja. Sama seperti tanda tanya kalau di wildcard. Jadi ``mp.`` bisa berarti ``mp3`` atau ``mp4``.

**Backslash (\\)**  
    Artinya sama dengan backslash di wildcard, dipakai buat escape karakter spesial.

**Asterisk (\*)**  
    Berarti match nol atau lebih untuk karakter seblumnya. ``a*`` berarti ``a``, ``aa``, ``aaa``, dan seterusnya. 
        Sedangkan ``.* (dot dan asterisk)`` berarti karakter apa saja dengan jumlah nol atau lebih. Ini karena ``. (dot)`` berarti karakter apa saja di regex.

**Plus (+)**  
    Berarti satu atau lebih untuk karakter sebelumnya. ``a+`` berarti ``aa``,  ``aaa``, ``aaaa``, dan seterusnya.

**{min,max}**  
    ``min`` dan ``max`` itu angka misalnya ``{1,2}``. Artinya jumlah karakter sebelumnya minimal ``1`` dan maksimal ``2``.  
    Jadi ``a{2,3}`` bisa jadi ``aa`` dan ``aaa``, tapi tidak ``aaaa`` karena melebihi nilai max.

**Caret (^)**  
    Artinya karakter pertama di baris teks. ``^a`` berarti baris teks yang karakter pertamanya ``a``.

**Tanda dolar ($)**  
    Ini kebalikan dari ``^``, yang berarti karakter terakhir. ``a$`` berarti baris teks yang karakter terakhirnya adalah ``a``.

**Kurung siku ([])**  
    Artinya sama dengan kurung siku di wildcard. ``[ab]`` berarti ``a`` atau ``b``.

**[^]**  
    Sama seperti ``[!]`` di wildcard. ``[^ab]`` berarti bukan ``a`` dan bukan ``b``.

**|**  
    Berarti salah satu dari pattern. ``(a|b|c)`` berarti salah satu saja antara ``a`` atau ``b`` atau ``c``.

&nbsp;

Di atas itu karakter-karakter Regular Expression. Regex ini dipakai di program seperti ``grep``, ``awk``, dan ``sed`` yang juga ada di tulisan ini.

Pusing?  
Ingat, Anda membaca ini atas kemauan sendiri dan tanpa paksaan dari pihak manapun.

Kita lanjut ke program.

&nbsp;

## <a name="cut" ></a>cut
**cut** dipakai buat filter output berdasarkan ``delimiter`` dan ``field``, input program ``cut`` bisa dari stdin atau file.

    cut OPTION... [FILE]...

Lebih gampang dijelaskan pakai contoh, misal kita punya file dengan nama ``data.txt`` yang isinya seperti di bawah

    satu    dua     tiga    empat

Masing-masing kata itu dipisahkan dengan delimiter tab, jadi ``satu<tab>dua<tab>tiga<tab>empat``. Nah yang disebut field itu kata ``satu``, ``dua``, ``tiga``, dan ``empat``.  
Field ini dihitung ``field 1``, ``field 2``, dan seterusnya, dihitung dari kiri. Jadi ``field 1`` itu kata ``satu``, ``field 4`` itu kata ``empat``.

Sekarang, kita lihat penggunaan ``cut`` yang umum.  
Misalnya kita mau filter output file ``data.txt`` untuk ``field 3`` saja:

    $ cut -f3 data.txt
    tiga

Kalau kita mau print ``field 2`` sampai field terakhir, pakai ``dash (-)``.

    $ cut -f2- data.txt
    dua    tiga    empat

Bagaimana kalau ``field 1`` sama ``field 3``?

    $ cut -f1,3 data.txt
    satu   tiga

``cut`` juga bisa pakai ``stdin`` selain file. Jadi kita bisa pakai ``pipe``, misalnya:

    $ cat data.txt | cut -f1,3
    satu   tiga

``cut`` secara default pakai ``delimiter tab``, jadi bagaimana kalau isi file ``data.txt`` seperti ini?

    satu,dua,tiga,empat

Kata-kata di file itu dipisah pakai koma, bukan tab. Jadi kita harus secara spesifik instruksikan ``cut`` supaya pakai delimiter koma, caranya dengan argumen ``-d`` diikuti karakter delimiter-nya.

    $ cat data.txt | cut -d, -f3
    tiga

&nbsp;

### <a name="head-n-tail" ></a>head & tail
command ``head`` dan ``tail`` dipakai untuk membatasi jumlah baris yang diprint ke stdout.

     tail [OPTION]... [FILE]...
     head [OPTION]... [FILE]...

Bedanya ``head`` sama ``tail``, ``head`` dihitung dari baris pertama, kalau ``tail`` dihitung dari baris terakhir.  

Misal kita punya file ``data.txt`` yang isinya ada 11 baris teks.

    $ cat > data.txt << EOF
    > satu
    > dua
    > tiga
    > empat
    > lima
    > enam
    > tujuh
    > delapan
    > sembilan
    > sepuluh
    > sebelas
    > EOF

Tes command ``head``

    $ head data.txt
    satu
    dua
    tiga
    empat
    lima
    enam
    tujuh
    delapan
    sembilan
    sepuluh

Kalau command ``tail``

    $ tail data.txt
    dua
    tiga
    empat
    lima
    enam
    tujuh
    delapan
    sembilan
    sepuluh
    sebelas

Kelihatan bedanya?  
Ya, jadi secara default ``head`` menampilkan 10 baris teks dihitung dari baris pertama. ``tail`` menampilkan 10 baris dihitung dari baris terakhir.

Kalau kita mau kurang atau lebih dari 10, bisa pakai argumen ``-n``

    $ head -n2 data.txt
    satu
    dua
    $
    $ tail -n2 data.txt
    sepuluh
    sebelas

Tentu saja kita juga bisa pakai stdin lewat ``pipe`` selain ``file``.

    $ cat data.txt | tail -n2
    sepuluh
    sebelas

&nbsp;

### <a name="tr" ></a>tr
**tr** dipakai untuk translasi atau hapus set karakter.

    tr [OPTION]... SET1 [SET2]

``tr`` ini inputnya dari ``stdin`` dan print output ke ``stdout``. saya biasanya pakai ``tr`` buat konversi karakter atau hapus karakter.

Misal kita mau convert huruf kecil ke besar

    $ echo "abcd" | tr [:lower:] [:upper:]
    ABCD

Kalau mau sebaliknya, tinggal dibalik saja ``tr [:upper:] [:lower:]``

``tr`` ini berguna buat misalnya merubah ``newline`` jadi ``tab``. Contoh kita buat file ``data.txt`` yang isinya seperti ini:

    $ cat > data.txt << EOF
    > abcd
    > efgh
    > EOF

File ``data.txt`` yang isinya dua baris. Kita bisa rubah ``newline (\n)`` ke ``tab (\t)``.

    $ cat data.txt | tr '\n' '\t'
    abcd   efgh

Atau ``newline`` ke ``spasi``

    $ cat data.txt | tr '\n' ' '
    abcd efgh

Atau jadi ``dash (-)``.

    $ cat data.txt | tr '\n' '-'
    abcd-efgh-

Kita juga bisa pakai ``tr`` buat hapus karakter tertentu pakai argumen ``-d``. Contoh, hapus huruf ``c`` dari stream.

    $ cat data.txt | tr -d 'c'
    abd
    efgh

&nbsp;

### <a name="sort" ></a>sort
**sort**, seperti namanya dipakai buat sorting baris teks dari stdin atau file.

    sort [OPTION]... [FILE]...

Mari kita coba dengan file ``data.txt`` yang tidak berurutan.

    $ cat > data.txt << EOF
    > zebra
    > charlie
    > bravo
    > kilo
    > 456
    > 123
    > EOF

Sort file ``data.txt``

    $ sort data.txt
    123
    456
    bravo
    charlie
    kilo
    zebra

Jadi, sort mengurutkan dari 0-9 kemudian a-z. Kalau mau sebaliknya, pakai argumen ``-r (reverse)``.

Sort mode ``reverse`` dari ``stdin``

    $ cat data.txt | sort -r
    zebra
    kilo
    charlie
    bravo
    456
    123

&nbsp;

### <a name="uniq" ></a>uniq
**uniq** ini dipakai buat print file atau stdin ke ``stdout`` tapi skip baris yang sama dan berdekatan.

    uniq [OPTION]... [INPUT [OUTPUT]]

Coba dengan file ``data.txt``

    $ cat > data.txt << EOF
    > satu
    > satu
    > dua
    > dua
    > tiga
    > tiga
    > EOF

Kalau kita print file itu pakai ``uniq``,

    $ uniq data.txt
    satu
    dua
    tiga

Jadi kalau ada line atau baris berdekatan yang sama, ``uniq`` print satu saja. Tapi bagaimana kalau misalnya baris yang sama itu tidak berdekatan?

    $ cat > data.txt << EOF
    > satu
    > tiga
    > dua
    > tiga
    > satu
    > dua
    > EOF

Isi file yang seperti itu, kalau kita pakai ``uniq``

    $ uniq data.txt
    satu
    tiga
    dua
    tiga
    satu
    dua

Tidak ada yang berubah.

Triknya, kalau kita mau print baris pakai ``uniq`` tapi line-nya tidak berdekatan, kita bisa pakai ``sort``.  
Misalnya

    $ cat data.txt | sort | uniq
    dua
    satu
    tiga
    
Kita print dulu ``data.txt``, kemudian di sorting pakai command ``sort``, baru pakai ``uniq``.

&nbsp;

Itu program-program Coreutils untuk manipulasi output. Selanjutnya kita ke program-program selain Coreutils.

&nbsp; 

### <a name="more-n-less" ></a>more & less
Command ``more`` dan ``less`` fungsinya sama. Kalau kita print file yang isinya banyak baris dan tidak fit di layar, ``more`` dan ``less`` bisa dipakai buat scroll.  
Jadi sama seperti kalau kita baca artikel di web yang panjang, kita bisa scroll halamannya kebawah.

Program ``more`` sebenarnya termasuk Coreutils, kalau ``less`` bukan. Kelemahan program ``more``, dia tidak bisa scroll ke atas, cuma scroll ke bawah. Nah para hacker yang kurang suka limitasi ini buat program sendiri seperti ``more`` tapi yang bisa scroll ke atas, lucunya program itu malah dinamakan ``less``.

Contoh penggunaan ``less`` misalnya kalau kita baca file syslog yang panjang itu.

    less /var/log/syslog

Tekan ``<Enter>`` atau panah ke bawah untuk scroll ke bawah, panah atas untuk scroll ke atas. Program ``less`` dan ``more`` juga bisa baca dari stdin selain dari file.

    cat /var/log/syslog | less

Sama saja.

&nbsp;

Tiga program selanjutnya, ``awk``, ``grep``, dan ``sed`` perlu ``Regular Expression`` yang sudah ditulis di atas. Di contoh ini saya tidak akan pakai karakter regex yang aneh-aneh, yang simpel saja.

&nbsp;

### <a name="awk" ></a>awk
Sama seperti program-program yang lain, ``awk`` ini juga dipakai buat manipulasi stream. Bedanya, ``awk`` ini lebih programmable atau seperti scripting. Input ``awk`` bisa dari ``file`` atau ``stdin``.

Secara umum penggunaan ``awk`` seperti ini

    awk '/pattern_regex/ {action1;}' file

Salah satu dari ``/pattern_regex/`` atau ``{action;}`` boleh tidak dipakai, tapi tidak dua-duanya. Kalau ``{action;}`` tidak ada, maka action dianggap ``{print}``. ``{print}`` ini action default di ``awk``.

Proses ``awk`` kalau dirinci seperti ini:

1. ``awk`` baca input dari file atau stdin baris per baris.
2. Kalau ada ``/pattern_regex/``, di setiap baris teks, periksa pattern regex. Kalau match eksekusi action yang ada di kurung kurawal. Kalau tidak, baris teks dilompati dan action tidak dieksekusi.
3. Kalau tidak ada ``/pattern_regex/``, eksekusi ``{action;}`` di setiap baris teks.
4. Kalau tidak ada ``{action;}`` print baris teks yang match dengan ``/pattern_regex/``.

Contoh umum penggunaan awk sama seperti ``cut``.  
Masih ingat program ``cut`` di atas?

Sama seperti ``cut``, ``awk`` juga ada delimiter dan default delimiter di program ``awk`` ini bisa ``spasi`` atau ``tab``. Sama seperti ``cut`` juga, delimiter bisa disesuaikan.

Langsung saja dengan contoh file ``data.txt``

    $ cat > data.txt << EOF
    > satu dua tiga empat
    > EOF

Sama seperti ``cut``, kalau kita mau print field 3 pakai ``awk``, caranya:

    $ awk '{print $3;}' data.txt
    tiga

Untuk field 1 dan 3

    $ awk '{print $1,$3;}' data.txt
    satu tiga

Sekarang kita coba dengan ``data.txt`` yang berisi dua baris.

    $ cat > data.txt << EOF
    > satu dua tiga empat
    > lima enam tujuh delapan
    > EOF

Coba print field ke 3.

    $ awk '{print $3;}' data.txt
    tiga
    tujuh

Kalau misalnya kita mau ``awk`` eksekusi action di baris tertentu saja, kita bisa filter baris itu. Misalnya untuk eksekusi action print di baris yang diawali ``lima`` saja.

    $ awk '/^lima.*/ {print $3;}' data.txt
    tujuh

Line yang pertama di-skip karena tidak ada pattern ``lima``.

Seperti yang lain, ``awk`` juga bisa baca dari stdin.

    $ cat data.txt | awk '/^lima.*/ {print $3;}'

Bagaimana untuk delimiter yang bukan ``spasi`` atau ``tab``?  
Ambil contoh seperti file ``/etc/passwd`` yang seperti ini:

    root:x:0:0:root:/root:/bin/bash

Kita bisa pakai argumen ``-F`` diikuti karakter delimiternya.

    $ awk -F: '/^root/ {print $7;}' /etc/passwd
    /bin/bash

&nbsp;

### <a name="grep" ></a>grep
**grep** dipakai buat filter baris teks yang ada berisi pattern Regular Expression yang dicari.

    grep [OPTIONS] PATTERN [FILE...]

Misalnya file ``data.txt`` isinya dua baris seperti di bawah:
        
    $ cat > data.txt << EOF
    > satu dua tiga empat
    > lima enam tujuh delapan
    > EOF

Nah pakai ``grep``, kita bisa filter baris teks yang ada pattern ``"enam"`` misalnya.

    $ grep "enam" data.txt
    lima enam tujuh delapan

``grep`` ini case sensitive, jadi ``ABCD`` beda sama ``abcd``. Kalau mau pakai pattern yang case insensitive atau besar kecil huruf bukan masalah, pakai argumen ``-i``.

    $ grep -i "ENAM" data.txt
    lima enam tujuh delapan

Kadang kita perlu tahu di baris ke berapa pattern ``regex`` itu match. Terutama teks yang isinya ratusan atau ribuan baris seperti source code.

kita bisa instruksikan ``grep`` supaya print nomor baris itu, caranya pakai argumen ``-n``.

    $ grep -ni "ENAM" data.txt
    2:lima enam tujuh delapan

``2``, itu nomor barisnya.

Selain ``file``, ``grep`` juga bisa terima input dari ``stdin``.

    $ cat data.txt | grep "enam"

Untuk pattern yang lebih kompleks misalnya.

    $ cat data.txt | grep "^s.*t$"
    satu dua tiga empat

Maksudnya ``"^s.*t$"`` baris yang dimulai huruf ``s (^s)``, diikuti karakter apa saja dengan jumlah berapa saja ``(.*)`` dan diakhiri huruf ``t (t$)``.

&nbsp;

### <a name="sed" ></a>sed
**sed** ini stream editor, program yang powerful dan keren sekali di Linux. Pakai ``sed`` ini kita bisa edit file teks tanpa perlu buka file itu di editor seperti ``Vim`` atau ``Emacs``.

Anda juga bisa bayangkan ``sed`` ini seperti ``pipe``, terima input dari ujung yang satu dan keluar dari ujung yang lain. Bedanya, ``sed`` ada proses manipulasi stream, jadi outputnya beda sama input karena sudah dimanipulasi.

Proses ``sed`` kurang lebih seperti di bawah:

1. Terima input dari ``file`` atau ``stdin``, baca baris per baris.
2. Di setiap baris, tempatkan baris teks itu di ``buffer``.
3. Edit teks yang ada di ``buffer``.
4. Print teks yang sudah diedit ke ``output``.
5. Lanjut ke baris berikutnya, eksekusi nomor 1 sampai 4 sampai tidak ada lagi input atau eof (end of file).

``sed`` ini punya banyak mode untuk manipulasi stream. Di sini kita pelajari tiga saja yang umum dipakai.

- ``print``. Print baris teks tanpa ada modifikasi teks.
- ``delete``. Delete baris teks.
- ``subtitute``. Cari pola karakter berdasarkan regex dan subtitusi karakter itu dengan karakter lain.

**Print**  
Mode print dipakai buat print baris teks tanpa ada manipulasi teks.

Contoh dengan file ``data.txt`` yang seperti ini.

    $ cat data.txt
    1. satu
    2. dua
    3. tiga
    4. empat
    5. lima
    6. enam
    7. tujuh
    8. delapan
    9. sembilan
    10. sepuluh

Format mode print: **``sed -n '<nomor baris>'p file``**.  

Contoh print baris ke 7.

    $ sed -n '7'p data.txt
    7. tujuh

Print baris terakhir pakai tanda ``$ (dolar)``.

    $ sed -n '$'p data.txt
    10. sepuluh

Print baris ke dua sampai 5.

    $ sed -n '2,5'p data.txt
    2. dua
    3. tiga
    4. empat
    5. lima

Print baris ke delapan sampai baris terakhir.

    $ sed -n '8,$'p data.txt
    8. delapan
    9. sembilan
    10. sepuluh

&nbsp;    

**Delete**  
Format untuk mode delete: **``sed '<nomor baris>'d file``**.

Mode delete ini bisa dianggap kebalikan dari mode ``print``.

Contoh delete baris ke 7.

    $ sed '7'd data.txt
    1. satu
    2. dua
    3. tiga
    4. empat
    5. lima
    6. enam
    8. delapan
    9. sembilan
    10. sepuluh

Delete baris terakhir pakai tanda ``$ (dolar)``.

    $ sed '$'d data.txt
    1. satu
    2. dua
    3. tiga
    4. empat
    5. lima
    6. enam
    7. tujuh
    8. delapan
    9. sembilan

Delete baris ke dua sampai 5.

    $ sed '2,5'd data.txt
    1. satu
    6. enam
    7. tujuh
    8. delapan
    9. sembilan
    10. sepuluh

Delete baris ke delapan sampai baris terakhir.

    $ sed -n '8,$'d data.txt
    1. satu
    2. dua
    3. tiga
    4. empat
    5. lima
    6. enam
    7. tujuh

&nbsp;    

**Subtitusi**  
Mode subtitusi ini bisa dibilang _search and replace_, cari karakter pakai regex, kalau ketemu replace.

Saya suka pakai sed mode ini, lebih cepat daripada harus lewat teks editor.

Format mode subtitusi: **``sed 's/regex/replace/' file``**

Dengan contoh file ``data.txt`` seperti di bawah,

    $ cat > data.txt << EOF
    > 123 abc
    > EOF

Coba subtitusi karakter ``123`` dengan ``456``.

    $ sed 's/123/456/' data.txt
    456 abc

``sed`` ini kalau kita instruksikan buat subtitusi karakter, cuma pattern yang pertama match saja yang dirubah.
        
    $ cat > data.txt << EOF
    > 123 abc 123
    > EOF
    $
    $ sed 's/123/456/' data.txt
    456 abc 123

Pattern ``123`` yang kedua tidak berubah. Kalau kita mau rubah semuanya, pakai ``g (global)`` setelah delimiter terakhir.

    $ sed 's/123/456/g' data.txt
    456 abc 456

Tentu saja ``sed`` ini juga bisa ambil input dari ``stdin`` selain ``file``.

    $ cat data.txt | sed 's/123/456/g'
    456 abc 456

Dari semua contoh di atas itu, output semuanya di print ke stdout. Kadang kita perlu juga output bukan stdout tapi langsung ke file.  
``sed`` punya satu fitur untuk ini namanya in-place. Pakai in-place, input dan output adalah file yang sama. Gampangnya, edit file tanpa perlu buka di editor.

    $ cat > data.txt << EOF
    > 123 abc 123
    > EOF

Merubah file secara in-place pakai argumen ``-i``.

    $ sed -i 's/123/456/' data.txt
    $ cat data.txt
    456 abc 123

&nbsp;

Sampai sini topik kali ini, manipulasi teks dan stream.  
Contoh-contoh yang ditulis di atas itu sedikit, cuma buat pengenalan. Kalau kurang, "Man page is your friend", dan tentu saja Google.

Saya terbuka, jadi silahkan disampaikan kalau di tulisan ini ada yang perlu dikoreksi, perlu ditambah atau dikurangi, asal bukan untuk dihapus.

Sampai jumpa di tulisan selanjutnya, Insya Allah.
