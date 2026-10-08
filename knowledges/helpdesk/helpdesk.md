# Katalog Layanan UPA TIK

Dokumen ini merepresentasikan katalog layanan Helpdesk UPA TIK ITK, diambil dari `database/seeders/ServiceSeeder.php`.

## Struktur

- Layanan tersusun **hierarkis**: kategori induk (A–J) berperan sebagai kelompok, dan layanan anak adalah layanan yang benar-benar dapat diajukan beserta target SLA-nya.
- Semua layanan bertipe `helpdesk`.

## Keterangan Kolom

- **Kode** — kode unik layanan.
- **Nama Layanan** — nama layanan (Bahasa Indonesia).
- **Prioritas SLA** — diturunkan dari waktu resolution: Critical (≤240 mnt), High (≤480 mnt), Medium (≤1440 mnt), Low (>1440 mnt).

---

## A. Layanan Akun & Identitas Digital

**Kode kategori:** `CAT-A` · **PIC TI:** UPA TIK - Helpdesk
Layanan terkait pengelolaan akun, identitas digital, dan akses sistem.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| A-01 | Permohonan reset password akun kampus | Critical |
| A-03 | Permohonan perubahan data akun pengguna | High |
| A-05 | Permohonan akses VPN kampus | High |
| A-06 | Permohonan akses WiFi kampus | Critical |
| A-07 | Permohonan whitelist perangkat jaringan | High |
| A-08 | Permohonan akses sistem informasi kampus | High |
| A-09 | Permohonan penonaktifan akun pengguna | Critical |
| A-10 | Permohonan migrasi akun email | Medium |

---

## B. Layanan Infrastruktur Server & Data Center

**Kode kategori:** `CAT-B` · **PIC TI:** UPA TIK - Infrastruktur
Layanan terkait pengelolaan server, hosting, dan data center.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| B-01 | Permohonan pembuatan VPS | Medium |
| B-02 | Permohonan peningkatan resource server | Medium |
| B-03 | Permohonan backup data server | High |
| B-04 | Permohonan restore data server | High |
| B-05 | Permohonan monitoring server | Medium |
| B-06 | Permohonan maintenance server | Medium |
| B-07 | Permohonan migrasi server | Medium |
| B-08 | Permohonan instalasi SSL Certificate | High |
| B-09 | Permohonan pembukaan port server | Critical |
| B-10 | Permohonan DNS management | High |
| B-11 | Permohonan reverse proxy configuration | High |
| B-13 | Permohonan database hosting | Medium |
| B-14 | Permohonan database maintenance | High |
| B-15 | Permohonan disaster recovery assistance | High |

---

## C. Layanan Website & Aplikasi

**Kode kategori:** `CAT-C` · **PIC TI:** UPA TIK - Pengembang
Layanan terkait pengembangan, pemeliharaan, dan pengelolaan website dan aplikasi.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| C-01 | Permohonan pembuatan website unit kerja | Low |
| C-02 | Permohonan redesign website | Low |
| C-03 | Permohonan maintenance website | Medium |
| C-04 | Permohonan upload/update konten website | High |
| C-05 | Permohonan integrasi API | Medium |
| C-06 | Permohonan subdomain baru | High |
| C-07 | Permohonan migrasi website | Medium |
| C-09 | Permohonan audit keamanan aplikasi | Low |
| C-10 | Permohonan deployment aplikasi | High |
| C-11 | Permohonan staging/testing server | Medium |
| C-12 | Permohonan penanganan bug aplikasi | High |
| C-13 | Permohonan konsultasi pengembangan aplikasi | High |
| C-14 | Permohonan integrasi SSO aplikasi | Medium |
| C-15 | Permohonan hosting repository Git internal | Medium |

---

## D. Layanan Jaringan & Internet

**Kode kategori:** `CAT-D` · **PIC TI:** UPA TIK - Jaringan
Layanan terkait jaringan, konektivitas, dan internet kampus.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| D-01 | Penanganan jaringan internet lambat | Critical |
| D-02 | Penanganan akses internet terputus | Critical |
| D-03 | Permohonan pemasangan titik LAN | Medium |
| D-04 | Permohonan pemasangan access point | Medium |
| D-05 | Permohonan konfigurasi VLAN | High |
| D-06 | Permohonan bandwidth management | High |
| D-07 | Permohonan monitoring jaringan | Medium |
| D-08 | Permohonan IP publik | High |
| D-09 | Permohonan IP statis | Critical |
| D-11 | Permohonan blokir akses website tertentu | Critical |
| D-12 | Permohonan captive portal WiFi | Medium |
| D-13 | Permohonan troubleshooting jaringan | High |

---

## E. Layanan Keamanan Informasi

**Kode kategori:** `CAT-E` · **PIC TI:** UPA TIK - Keamanan
Layanan terkait keamanan siber, audit, dan perlindungan data.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| E-01 | Pelaporan insiden keamanan siber | Critical |
| E-02 | Permohonan vulnerability assessment | Low |
| E-03 | Permohonan penetration testing | Low |
| E-04 | Permohonan scanning malware | High |
| E-05 | Permohonan audit log akses | Medium |
| E-06 | Permohonan recovery data | Medium |
| E-07 | Permohonan backup email | High |
| E-08 | Permohonan konsultasi keamanan informasi | High |
| E-09 | Permohonan digital signature/tanda tangan elektronik | Medium |
| E-10 | Permohonan enkripsi data | Medium |

---

## F. Layanan Multimedia & Pembelajaran Digital

**Kode kategori:** `CAT-F` · **PIC TI:** UPA TIK - Multimedia
Layanan terkait multimedia, e-learning, dan dukungan pembelajaran digital.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| F-01 | Permohonan dukungan hybrid meeting | Critical |
| F-02 | Permohonan live streaming kegiatan | Medium |
| F-03 | Permohonan perekaman kegiatan | High |
| F-05 | Permohonan peminjaman perangkat multimedia | Critical |
| F-06 | Permohonan setup konferensi video | Critical |
| F-07 | Permohonan akun LMS | Critical |
| F-10 | Permohonan pelatihan penggunaan aplikasi pembelajaran | Medium |

---

## G. Layanan Dukungan Perangkat TI

**Kode kategori:** `CAT-G` · **PIC TI:** UPA TIK - Infrastruktur
Layanan terkait pemeliharaan, perbaikan, dan pengelolaan perangkat TI.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| G-01 | Permohonan maintenance komputer | Medium |
| G-02 | Permohonan upgrade perangkat komputer | Medium |
| G-03 | Permohonan troubleshooting printer | High |
| G-04 | Permohonan instalasi printer jaringan | High |
| G-07 | Permohonan inventarisasi perangkat TI | Medium |
| G-08 | Permohonan disposal/peremajaan perangkat TI | Low |
| G-09 | Permohonan pengecekan perangkat laboratorium | Medium |
| G-10 | Permohonan konfigurasi perangkat biometrik/fingerprint | High |

---

## H. Layanan Administrasi & Konsultasi TI

**Kode kategori:** `CAT-H` · **PIC TI:** UPA TIK
Layanan terkait konsultasi, pelatihan, dan administrasi TI.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| H-01 | Permohonan konsultasi transformasi digital | Medium |
| H-02 | Permohonan konsultasi pemilihan perangkat TI | High |
| H-03 | Permohonan konsultasi pengadaan software | High |
| H-04 | Permohonan pelatihan keamanan siber | Low |
| H-05 | Permohonan pelatihan aplikasi perkantoran | Low |
| H-06 | Permohonan pelatihan sistem informasi kampus | Low |
| H-08 | Permohonan dokumentasi teknis sistem | Medium |
| H-09 | Permohonan surat dukungan teknis TI | High |
| H-10 | Permohonan rekomendasi spesifikasi perangkat TI | High |

---

## J. Kategori Insiden & Permasalahan Umum

**Kode kategori:** `CAT-J` · **PIC TI:** UPA TIK - Helpdesk
Pelaporan insiden dan permasalahan umum terkait layanan TI.

| Kode | Nama Layanan | Prioritas SLA |
|------|--------------|---------------|
| J-01 | Pelaporan website tidak dapat diakses | Critical |
| J-02 | Pelaporan akun diretas | Critical |
| J-03 | Pelaporan spam email | High |
| J-04 | Pelaporan perangkat rusak | Medium |
| J-05 | Pelaporan jaringan down | Critical |
| J-06 | Pelaporan server overload | Critical |
| J-07 | Pelaporan kehilangan data | High |
| J-08 | Pelaporan kegagalan backup | High |
| J-09 | Pelaporan printer bermasalah | High |
| J-10 | Pelaporan akses sistem gagal | Critical |

---

## Ringkasan

| Kategori | Kode | Jumlah Layanan | Fokus |
|----------|------|----------------|-------|
| A | CAT-A | 8 | Akun & Identitas Digital |
| B | CAT-B | 14 | Infrastruktur Server & Data Center |
| C | CAT-C | 14 | Website & Aplikasi |
| D | CAT-D | 12 | Jaringan & Internet |
| E | CAT-E | 10 | Keamanan Informasi |
| F | CAT-F | 7 | Multimedia & Pembelajaran Digital |
| G | CAT-G | 8 | Dukungan Perangkat TI |
| H | CAT-H | 9 | Administrasi & Konsultasi TI |
| J | CAT-J | 10 | Insiden & Permasalahan Umum |
| **Total** | | **92** | **9 kategori** |

> Sumber data: `helpdesk-backend/database/seeders/ServiceSeeder.php`. Perubahan pada seeder perlu disinkronkan ke dokumen ini.
