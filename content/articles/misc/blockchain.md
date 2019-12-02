Title: Blockchain: Teknologi dibalik Bitcoin
Date: 2017-01-07 22:19
Author: Dhani Setiawan
Category: Misc
Slug: blockchain-bitcoin
Status: Published
Comments: yes


<div class="fimg">
        <img src="//devnull.web.id/images/misc/blockchain/bitcoin.png" alt="bitcoin" title="bitcoin" />
        <p>Gambar: pinterest.com</p>
</div>

Bayangkan sebuah sistem tanpa otoritas. Bayangkan kalau kita bisa transaksi tanpa perlu bank, atau buat kontrak tanpa perlu notaris. Bayangkan kalau ada sistem yang bisa mengganti fungsi pihak ketiga itu, bank atau notaris itu, tanpa ribet dan tanpa mahal.

Bisakah? Mungkin sekarang belum, tapi nanti bisa sangat mungkin. Teknologi atau sistem itu sekarang lagi populer, namanya blockchain, teknologi dibalik kesuksesan _cryptocurrency_ Bitcoin.

Bitcoin ini kurang lebih sama seperti mata uang umunya seperti Rupiah atau Euro, bedanya Bitcoin bentuknya digital. Bedanya lagi, kalau Euro dipakai di negara-negara Eropa atau Rupiah dipakai di Indonesia, Bitcoin dipakai di negara Internet. Perbedaan lainnya, tidak ada otoritas seperti bank yang mengelola Bitcoin. Proses otorisasi, autentikasi, dan verifikasi semuanya ada di sistem blockchain.

Sebelum terlalu jauh tulisannya, buat teman-teman yang mendarat di halaman ini karena pengen tau apa itu Bitcoin, siapa Satoshi Nakamoto, cara transaksi Bitcoin, atau cari tau tentang jual beli Bitcoin, tulisan ini bukan tentang itu, tapi lebih ke masalah teknologinya.

Jadi seperti apa blockchain itu?  
Blockchain itu database. Dalam konteks Bitcoin, database ini isinya record transaksi siapa kirim berapa bitcoin ke siapa. Yang bikin beda sama database umumnya, blockchain ini sistemnya ter-desentralisasi, terbuka, _read only_, _read only_ artinya begitu transaksi sudah tercatat, record itu tidak bisa lagi dirubah. Sebenarnya bukan tidak bisa dirubah, tapi hampir mustahil ada orang bisa memanipulasi data yang tercatat.

Blockchain ini database yang data-datanya ditempatkan di blok-blok. Satu _block_ itu isinya banyak record transaksi. _Block-block_ ini tersusun berdasarkan urutan waktu terus masing-masing _block_ ini punya link ke _block_ sebelumnya, link ini bentuknya hash sha256.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/blockchain.png" alt="blockchain" title="blockchain" />
</div>

Biar bisa paham cara kerja blockchain, kita harus paham dulu pengetahuan dasar tentang _Public Key Encryption_. Jadi kalau ada di antara teman-teman yang belum paham apa itu _Digital Signature_, _Public Key Infrastructure_ sama algoritma _hash_, sebaiknya pelajari dulu. Beberapa waktu lalu saya ada publish post tentang SSL/TLS. Memang tentang SSL/TLS tapi di dalamnya ada pembahasan yang lumayan komprehensif tentang _PKI (Public Key Infrastructure)_, judulnya [Tentang SSL/TLS + sertifikat TLS gratis dari Let's Encrypt](//devnull.web.id/misc/ssl-tls-letsencrypt.html)

<br />

Lanjut, ambil contoh transaksi bitcoin. Alice minum kopi di warung kopi punya Bob, warkopnya Bob ini terima pembayaran Bitcoin. Alice, yang juga punya Bitcoin coba bayar kopi pakai Bitcoin, harganya kalau dalam Rupiah 15 ribu tapi dikonversi ke Bitcoin sekitar 0.001 BTC. Alice buka aplikasi Bitcoin di hapenya, terus transfer 0.001 BTC ke alamat bitcoin Bob.

Supaya bisa transaksi pakai Bitcoin, Alice sama Bob sebelumnya harus punya bitcoin wallet, kita bisa analogikan bitcoin wallet ini seperti rekening bank. Kalau rekening bank ada identitasnya, bitcoin wallet juga ada tapi identitas bitcoin wallet ini bukan nama seperti rekening tapi _key pair_ enkripsi asimetris, ada _public key_ sama _private key_. Terus yang pasti, kalau mau bisa transaksi Bitcoin, di bitcoin wallet itu harus ada nilai bitcoin atau semacam saldo kalau di rekening. Bitcoin ini bisa dibeli di market pakai mata uang tradisional seperti Rupiah. Alice di walletnya sudah punya bitcoin 0.5 BTC yang sebelumnya dia beli dari local market seharga 6 juta.

Alamat bitcoin contohnya seperti ``3HCSJQA3zji58dJmifL5q1DA7p2hX5rGAZ`` yang bisa dibuat gratis di banyak provider bitcoin wallet, salah satunya seperti [Coinbase](https://www.coinbase.com/). Itu alamat bitcoin yang valid, kalau mau coba silahkan transfer bitcoin, itu alamat Bitcoin saya :)  
Panjang alamat bitcoin ini sepanjang 20 byte atau 160 bit yang berarti 2<sup>160</sup>.

        2 ^ 160 = 1461501637330000000000000000000000000000000000000

Kalau alamat bitcoin sebanyak itu, alamat bitcoin ini tidak bakal habis biarpun masing-masing penduduk bumi punya sejuta alamat bitcoin yang berbeda.

Terus dibalik bitcoin ini ada jaringan yang disebut bitcoin network, network ini yang ngatur semua transaksi bitcoin. Jaringan atau bitcoin network ini isinya komputer, sebutannya node. Node ini diinstal software Bitcoin terus mereka ini terhubung satu sama lainnya, node-node ini bisa komputer seperti PC umumnya atau komputer yang didesain khusus buat jalankan software Bitcoin.  
Network ini sistemnya _peer to peer_ yang artinya tidak ada servernya, masing-masing node saling terkoneksi seperti aplikasi Bittorrent. 

Apa yang terjadi waktu Alice transfer bitcoin ke alamat bitcoin Bob? Prosesnya, aplikasi wallet Alice buat dua request transfer seperti ini:

1. Transfer 0.001 BTC dari wallet Alice ke wallet Bob.
2. Transfer 0.498 BTC dari wallet Alice ke wallet Alice.

Dari sisi pengguna, Alice cuma tau kalau saldonya berkurang. Tapi dari sisi network bitcoin transfer itu ada dua, satu transfer ke alamat Bitcoin Bob, satunya ke alamat Alice sendiri.  
Jadi di Bitcoin itu tidak ada namanya saldo, yang ada input sama output. Yang dianggap saldo itu cuma input yang belum jadi output. Input itu bitcoin yang masuk, output bitcoin yang keluar dari wallet. Terus input sama output ini harus balance, bitcoin yang masuk sama yang keluar harus imbang.

Nah di contoh ini, input wallet Alice yang 0.5 BTC dari market. Nah waktu transaksi, input 0.5 BTC ini harus habis jadi output semua. Karena itu dibuat dua output seperti di atas itu, output pertama bayar kopi, output kedua transfer ke wallet sendiri.  
Tapi kalau diperhatikan ``0.001 + 0.0498 = 0.499`` bukan ``0.5``, kemana yang ``0.001``? 0.001 BTC ini jadi fee buat network atas jasa mereka memproses transaksi itu. Jadi fee network itu selisih dari transaksi, kalau misalnya Alice di output kedua transfer 0.497 BTC ke wallet sendiri, berarti fee buat network jumlahnya 0.002 BTC.

Jadi, request wallet Alice ke network kurang lebih seperti ini:

> Halo, saya Alice. Saya punya input 0.5 BTC yang mau dijadikan output.  
> Output 1, 0.001 BTC ke wallet Bob.  
> Output 2, 0.498 BTC ke wallet sendiri.  
> Sisanya yang 0.001 BTC silahkan diambil buat fee.

Fee ini sifatnya opsional, artinya tanpa fee pun transaksi tetap diproses sama network. Cuma fee ini bisa menentukan prioritas, semakin besar fee semakin cepat diproses.

Request Alice di atas itu kemudian ditandatangani secara digital pakai private key Alice terus di-_broadcast_ ke network. Para node di network yang terima pesan broadcast itu mereka coba verifikasi, apa benar Alice yang kirim pesan itu. Verifikasi ini pakai public key Alice, kalau tandatangan atau digital signature yang di-broadcast cocok dengan public key Alice berarti request itu valid.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/sign.png" alt="blockchain digital signature" title="blockchain digital signature" />
</div>

Begitu transaksi itu valid dan berhasil diverifikasi, request itu diproses, record transaksi itu dicatat terus dimasukkan ke _block_ bersama record banyak transaksi lainnya. Block ini kemudian ditempatkan ke database blockchain sebagai _block_ baru.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/new-block.png" alt="blockchain new block" title="blockchain new block" />
</div>
 
<br />

###Struktur block.
Seperti apa bentuknya block itu?

Struktur block kurang lebih seperti di bawah:

- 4 byte        : block size. Berisi informasi berapa besar block ini.
- 80 byte       : header block.
- 1-9 byte      : berisi informasi berapa transaksi yang ada di block ini.
- bervariasi    : berisi list transaksi bitcoin yang tercatat di block ini.

Rincian header block yang 80 byte di atas seperti ini:

- 4 byte        : versi software bitcoin yang dipakai.
- 32 byte       : berisi _hash_ block sebelumnya.
- 32 byte       : hash dari merkle root atau root data structure binary hash tree.
- 4 byte        : berisi timestamp kapan waktu block ini dibuat. Hitungan detik dari _Unix Epoch_ (1 Januari 1970).
- 4 byte        : tingkat kesulitan algoritma proof-of-work.
- 4 byte        : nonce. Atau nilai proof-of-work yang berhasil ditemukan.

_Merkle root_, _Nonce_ sama _proof-of-work_ dibahas nanti.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/block-structure.png" alt="blockchain block structure" title="blockchain block structure" />
</div>

Seperti terlihat, setiap block di headernya ada hash dari block sebelumnya atau bisa dianggap link ke block sebelumnya. Begitu terus dan kalau link ini ditelusuri terus, ujungnya ada di block yang paling pertama dibuat. Block yang paling pertama dibuat ini namanya _Genesis Block_ yang dibuat di tahun 2009. Baca lebih lanjut tentang [Genesis Block](https://en.bitcoin.it/wiki/Genesis_block).

**Merkle root**. Data structure-nya namanya merkle tree atau binary hash tree. Skip.. skip.. tanpa terlalu detail, adanya hash dari merkle root ini dipakai buat membuktikan dengan cepat apakah di block ini transaksi yang dicari ada atau tidak. Satu block, isinya bisa 500 sampai diatas seribu transaksi bitcoin, kalau cari satu-satu diurut dari awal sampai transaksi terakhir tidak efektif, nah adanya _root hash_ ini bisa dipakai buat pembuktian bahwa transaksi yang dicari ada di dalam block tanpa perlu lihat record satu per satu. Wikipedia tentang data structure [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree)

Kembali ke _Network_. Salah satu jenis node di _Network_ ini ada yang kerjanya mem-validasi, verifikasi transaksi, terus kalau transaksi itu valid, mereka catat transaksi itu dalam block, node ini namanya **Miner**. Ada banyak _Miner_ di network bitcoin, ribuan atau mungkin jutaan miner yang saling terkoneksi satu sama lain.

Terus network blockchain ini tidak ter-sentralisasi, artinya tidak ada server yang terpusat. Database blockchain itu tersebar di semua node, masing-masing node punya database yang sama yang saling singkron terus menerus.

Waktu ada pesan broadcast dari Alice, database blockchain pada waktu itu sampai block ke 99 misalnya. Berarti para miner waktu itu semuanya kerja secara independen buat block berikutnya, block ke 100 yang transaksi kopi Alice bakal masuk di block ini.

Di sini muncul problem. Karena masing-masing miner memproses block berikutnya, block ke 100 secara independen, block ini bisa beda-beda isinya antara miner satu sama yang lainnya. Bahkan mungkin ada node miner yang lokasinya jauh dari Alice dia tidak terima pesan broadcast-nya karena misalnya latency jaringan Internetnya tinggi, jadi di miner ini transaksi Alice tidak masuk di block ke 100, tapi di miner lain ada.

Solusinya, ada semacam tantangan buat para miner ini, siapa yang berhasil menang lomba ini, dia yang berhak menempatkan block ke 100 ke chain database blockchain. Bukan cuma itu, miner ini juga dapat reward atau imbalan bitcoin atas hasil usahanya. Selain reward, miner ini juga punya hak ambil fee dari setiap transaksi termasuk fee 0.001 BTC dari Alice, ditambah banyak fee dari ratusan bahkan ribuan transaksi yang masuk di block ke 100.

Tantangan ini yang di blockchain dinamai _Proof-of-work_. Para miner ini beradu cepat menebak angka yang disebut angka _nonce_. Siapa berhasil menemukan _nonce_ paling cepat dia pemenangnya.

<br />
###Bitcoin mining
Reward bitcoin buat miner yang berhasil menang ini satu-satunya cara pembuatan Bitcoin baru. Jadi bitcoin yang beredar sekarang ini awalnya dari para miner itu, karena itu mereka disebut miner atau penambang Bitcoin.  
Berapa banyak coin yang didapat miner kalau berhasil menebak _nonce_? banyak.

Reward buat miner itu 50 BTC. Tapi jumlah ini dikurangi setenganya setiap 210.000 block baru. Setiap kurang lebih 10 menit muncul block baru di blockchain, ini berarti sekitar 4 tahun sekali reward dipotong setengah. _Genesis block_ atau block yang paling pertama dibuat di tahun 2009, reward buat miner 50 BTC. Tahun 2012 jadi setengahnya, 25 BTC dan di tahun 2016 dipotong lagi setengah jadi 12.5 BTC. Jadi sekarang ini reward buat miner yang berhasil menebak _nonce_ reward-nya 12.5 BTC.

Reward ini bakalan dipotong setengahnya terus sampai total bitcoin yang beredar totalnya 21 juta bitcoin. Ini batasan Bitcoin, kalau sudah sampai 21 juta bitcoin tidak ada lagi bitcoin yang bisa dibuat. Reward buat para miner setelah ini cuma dari fee transaksi saja

<br />
###Proof-of-work
Proof-of-work ini data yang jadi syarat supaya block bisa dimasukkan ke blockchain. Data Proof-of-work ini susah sekali buatnya, perlu waktu sama _computing power_ yang besar, tapi gampang buat diverifikasi kebenarannya. Proses pembuatan data ini caranya acak dan tebak-tebakan, terus probabilitas tebakan itu benar kemungkinannya kecil sekali.

Caranya, para miner harus mencari nilai hash SHA256 yang inputnya ``header block + nilai nonce`` yang hasil hash ini nilainya _sama dengan atau lebih kecil_ dari ``target``.

       hash (header block + nonce) <= target

**Nonce** ini panjangnya 4 byte atau 32 bit. Para miner, mereka cari nilai _nonce_ ini, _nonce_ berubah maka hash yang dihasilkan berubah. Mereka tebak nonce terus menerus sampai hasil hash sama atau lebih kecil dari _target_. Tingkat kesulitannya ada di _target_ ini, kalau _target_ nilainya besar berarti kemungkinan hasil hash lebih kecil dari target juga besar. Tapi kalau nilai target ini kecil, probabilitas menemukan nonce yang tepat juga jadi kecil.  
Tingkat kesulitan ini namanya _Difficulty_ dan ini disesuaikan terus menerus. Kalau para miner bisa gampang nebak _nonce_, maka _difficulty_ dinaikkan yang berarti nilai target turun. _Difficulty_ ini dipakai buat menjaga supaya rata-rata _Proof-of-work_ itu bisa dihasilkan setiap 10 menit sekali, yang berarti block baru masuk ke database blockchain setiap sekitar 10 menit.

**Evolusi hardware miner**  
Dulu, awal-awal bitcoin para miner biasa pakai PC biasa yang diinstall software Bitcoin Core terus dijadikan node miner. Kemudian muncul tren pakai GPU atau _Graphical Processing Unit_ buat dijadikan miner. GPU lebih cepat dari CPU biasa, jadi bisa lebih banyak menebak hash per detiknya dibandingkan CPU.

Karena Bitcoin yang tambah lama tambah populer ditambah kompetitifnya persaingan mining, para produsen hardware mereka produksi _Field-programmable gate array_ atau FPGA card buat hardware mining yang tentu saja lebih cepat dibanding GPU. Persaingan tambah sengit, sekarang ini tren mining sudah jadi hardware ASIC (Application Specific Integrated Circuit) yang punya power sekian ratus ribu mega hash per detiknya, jauh kalau dibandingkan sama FPGA yang punya power rata-rata dibawah seribu mega hash per detiknya.

Tentu saja para miner yang awal-awal pakai ASIC bisa kaya mendadak, tapi karena sekarang rata-rata miner semuanya ASIC jadinya ya tetap kompetitif. Dan saking ketatnya persaingan hardware mining ini, sekarang mining biarpun pakai hardware ASIC yang mahal pun tetap susah bersaing. Karena itu rata-rata para miner sekarang mereka buat grup miner yang disebut _mining pool_, pool ini isinya banyak hardware mining yang ngumpul jadi satu terus beban kerja nebak hash dibagi ke anggota pool itu. Kalau pool ini berhasil menghasilkan Proof-of-work, reward bitcoinnya dibagi ke anggota pool berdasarkan kontribusi hardware miner itu.

Karena kemampuan hardware yang tambah hari tambah cepat ini makanya _difficulty_ proof-of-work mengikuti tren ini biar pembuatan block baru bisa tetap di rata-rata sepuluh menit.

<br />
Miner yang berhasil menemukan nilai _nonce_, dia kirim pesan broadcast ke network. Node lain yang terima pesan broadcast ini coba verifikasi apa benar _nonce_ ini menghasilkan data proof-of-work dibawah nilai target. Kalau benar, para node ini mereka ambil block yang dibuat penemu nonce terus block ini dimasukkan ke database blockchain mereka. Mereka para miner ini kemudian mulai lagi kerja nebak nonce buat block berikutnya, begitu seterusnya.

<br />

###Fork
Biarpun kemungkinannya kecil sekali tapi bisa terjadi di waktu yang hampir bersamaan dua node miner atau lebih mereka berhasil menemukan _nonce_. Ini bisa muncul kalau pesan broadcast penemu _nonce_ pertama belum sampai ke node kedua, bisa jadi karena jarak atau latency jaringan.  
Kalau begini, ada dua block baru yang sama-sama valid dimasukkan ke database blockchain, problem ini disebut **fork**.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/blockchain-fork.png" alt="blockchain fork" title="blockchain fork" />
</div>

karena problem fork ini, network jadi terbagi.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/blockchain-network-split.png" alt="blockchain network split" title="blockchain network split" />
</div>

Fork ini tidak boleh dibiarkan, network harus memilih salah satu dari dua block yang sama-sama valid itu. Caranya, para miner harus memprioritaskan salah satu dari dua block, terserah yang mana. Begitu salah satu dari dua block ini dapat block baru, maka block ini yang diambil. Gampangnya, cabang mana yang paling panjang rentetan block-nya, dia yang diambil.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/blockchain-fork2.png" alt="blockchain fork" title="blockchain fork" />
</div>

<br />

###Security
Blockchain ini sistemnya open, semua transaksi bisa dilihat siapa saja yang punya Internet, software-nya pun Open Source. Bagaimana keamanan datanya?

Ada beberapa tipe penggunaan database blockchain yang tidak legal.  
Pertama _Unauthorized transaction_. Setiap akun bitcoin wallet diproteksi pakai sepasang asymetric encryption key. Artinya bitcoin yang tercatat di wallet itu cuma yang punya private key yang bisa transaksi, orang tidak bisa seenaknya pakai bitcoin orang lain buat transaksi karena kalau digital signature mismatch pasti ditolak sama network. Kecuali akun bitcoin wallet jatuh ke orang lain ini lain ceritanya, weak link nya ada di user bukan di sistem.

Kedua _alter data_. Bagaimana kalau ada attacker yang coba merubah data yang tercatat di blockchain?

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/blockchain.png" alt="blockchain" title="blockchain" />
</div>

Misal attacker merubah transaksi yang ada di block 96. Karena transaksi berubah, maka data _merkle root_ di header juga berubah yang berarti hash header juga berubah yang juga berarti _Proof-of-work_ sama _nonce_ jadi invalid. Kalau begini, attacker harus cari nilai _nonce_ sampai benar. Kalau para miner saja harus join pool buat cari proof-of-work, bayangkan bagaimana lamanya attacker yang sendirian itu menebak nonce.

Oke kalau dianggap attacker ini punya hardware yang sangat super cepat yang bisa menebak nonce dalam hitungan menit, dia masih punya tugas lagi. Hash 96 punya attacker ini valid tapi karena data berubah maka hash pun berubah, dan karena setiap block punya link hash ke block sebelumnya, maka block 96 dan 97 jadi terputus karena hash block 96 yang tercatat di block 97 tidak sama lagi.

<div class="aimg">
        <img src="//devnull.web.id/images/misc/blockchain/blockchain-attack.png" alt="blockchain attack" title="blockchain attack" />
</div>

Dengan kondisi begini, attacker mau tidak mau dia harus rubah block 97 juga. Dia harus rubah hash block sebelumnya di block 97 supaya sama dengan hash block 96, akibatnya header block 97 berubah. Kalau header berubah berarti proof-of-work jadinya tidak valid lagi. Artinya, tebak nonce lagi. Ketemu nonce block 97, dia masih punya block 98, 99, sama block 100 yang harus dimodifikasi juga.

Kalaupun attacker ini berhasil, biarpun kemungkinan itu hampir mustahil, dia harus ingat bahwa blockchain ini databasenya tersebar di semua node yang terkoneksi ke network. Artinya, attacker ini harus merubah database di semua node itu, bayangkan bagaimana susahnya itu.

Ketiga _double spending_. Double spending ini, input bitcoin yang sama dipakai di dua ouput transaksi yang berbeda di waktu yang hampir bersamaan. Node yang terima pesan transaksi ini cuma bisa terima satu transaksi saja, transaksi yang lain dianggap tidak valid. Masalahnya tidak semua node bisa sepakat transaksi mana yang valid sama mana yang tidak. Kalau kondisi network normal, double spend ini tidak terlalu jadi masalah karena begitu proof-of-work berhasil dibuat, data di block miner penemu nonce itu yang valid. Karena itu, double spend ini kalau mau berhasil, maka network harus terpecah dan satu-satunya waktu network tidak sepakat itu waktu ada problem _fork_.

Kembali ke fork lagi, fork ini kan cuma bisa muncul kalau ada dua atau lebih miner yang menemukan nonce secara bersamaan. Nah si attacker harus pikirkan bagaimana caranya itu bisa terjadi terus terusan, karena kalau salah satu cabang fork lebih panjang, cabang yang satunya jadi tidak valid lagi.

Sampai sini kita bisa ambil kesimpulan bahwa semakin lama umur block maka semakin solid. Karena itu biasanya kalau transaksi bitcoin yang jumlahnya besar, transaksi ditunggu sampai sekitar satu jam biar block tempat transaksi itu ditumpuk 6 block di depannya. 6 Block atau 6 konfirmasi ini disepakati jadi batas aman block tidak bisa lagi dimanipulasi.

<br />

###Blockchain vulnerablity
Kalau dilihat dari masalah keamanan di atas bisa disimpulkan bahwa keamanan data blockchain ini ada di kerumitan komputasi sama race melawan network miner. Tapi ada cara yang memudahkan attack di atas itu, namanya **51% attack**. 51% attack ini kalau attacker bisa menguasai 51% network miner, maka dia bisa mengontrol network karena kemungkinan menemukan proof-of-work jadi lebih besar kalau sebagian besar network miner dikuasai. Tapi biarpun begitu, cuma _alter data_ sama _double spend_ saja yang mungkin bisa curangi, masalah _unauthorized transaction_ tetap aman karena diproteksi pakai digital signature.

<br />

###Conclusion
Teknologi blockchain ini memang masih belum diadopsi luas, tapi adanya Bitcoin ini blockchain jadi populer.

Bayangkan kemungkinan-kemungkinan apa saja nanti yang bisa muncul karena blockchain. Mungkin kita tidak perlu ICANN buat mengatur nama domain lagi. Mungkin sistem DNS kita tidak lagi diatur sama root server yang 13 itu. Mungkin masalah legal yang selama ini bergantung sama notaris bisa dialihkan ke blockchain.

Kalau saya bayangkan bagaimana kalau semua masyarakat Indonesia masing-masing punya identitas digital yang diproteksi pakai encryption key. Terus kalau ada voting semacam pemilu atau pikada, identitas digital dipakai buat voting terus hasil voting ditempatkan di database blockchain. Voting bisa lewat smartphone atau komputer yang tersambung ke Internet. Tidak ada pilihan yang tidak valid karena semua pilihan ditandatangani pakai digital signature. Tidak ada yang bisa memanipulasi data karena data ada di database blockchain, bukan di KPU.

Itu imajinasi Saya, rekans Linuxer mungkin saja imajinasinya lebih liar lagi dari itu :)

<br />
**Refs:**  
Sumber diambil dari e-book [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook) yang ditulis oleh Andreas M. Antonopoulos.
