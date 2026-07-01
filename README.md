# Hermes

AI Helpdesk Agent untuk UPA TIK Institut Teknologi Kalimantan.

## Deskripsi

Hermes adalah agen AI berbasis Docker yang berfungsi sebagai helpdesk otomatis untuk UPA TIK (Unit Pelaksana Akademik Teknologi Informasi dan Komunikasi) ITK. Hermes menjawab pertanyaan civitas akademika seputar layanan IT kampus melalui tiga kanal komunikasi: WhatsApp, Telegram, dan Email.

Hermes menggunakan image `nousresearch/hermes-agent:latest` dengan model Gemini 2.5 Flash sebagai backend AI, dilengkapi knowledge base yang dapat disesuaikan dengan informasi layanan UPA TIK.

## Arsitektur

```
┌─────────────────────────────────────────────────┐
│  Debian 13 VPS (2 cores, 2GB RAM, 20GB disk)    │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │  Docker Engine                             │  │
│  │                                            │  │
│  │  ┌──────────────────────────────────────┐  │  │
│  │  │  hermes container (1.5GB / 1.5 CPU)  │  │  │
│  │  │  nousresearch/hermes-agent:latest     │  │  │
│  │  │                                      │  │  │
│  │  │  /opt/config    ← ./config/:ro       │  │  │
│  │  │  /opt/prompts   ← ./prompts/:ro      │  │  │
│  │  │  /opt/automations ← ./automations/:ro│  │  │
│  │  │  /opt/knowledges ← ./knowledges/:ro  │  │  │
│  │  │  /opt/logs      ← ./logs/           │  │  │
│  │  │  /opt/data      ← /root/.hermes     │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  │                                            │  │
│  │  Network: ai-network (external)            │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Port 127.0.0.1:8642 → container:8642           │
└─────────────────────────────────────────────────┘
```

## Prasyarat

| Komponen | Minimum |
|----------|---------|
| OS | Debian 13 |
| CPU | 2 cores |
| RAM | 2 GB |
| Storage | 20 GB |
| Docker | >= 20.10 |
| Docker Compose | >= 2.0 |

## Quick Start

```bash
# 1. Clone repository
git clone <repository-url> hermes
cd hermes

# 2. Salin template environment
cp .env.example .env.production

# 3. Edit konfigurasi (isi API key dan kredensial)
nano .env.production

# 4. Buat Docker network
docker network create ai-network

# 5. Jalankan
docker-compose up -d
```

## Konfigurasi

Salin `.env.example` ke `.env.production` lalu isi nilai yang sesuai. Berikut referensi variabel yang tersedia:

### AI

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `MODEL_PROVIDER` | Provider model AI | `gemini` |
| `MODEL_NAME` | Nama/identifier model | `gemini-2.5-flash` |
| `GOOGLE_API_KEY` | API key Google AI (Gemini) | — |
| `OPENROUTER_API_KEY` | API key OpenRouter (alternatif) | — |

### Timezone

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `TZ` | Timezone container (format IANA) | `Asia/Makassar` |

### Dashboard

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `HERMES_DASHBOARD` | Aktifkan (1) atau nonaktifkan (0) dashboard | `0` |

### WhatsApp

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `WHATSAPP_ENABLED` | Aktifkan integrasi WhatsApp | `true` |
| `WHATSAPP_MODE` | Mode operasi: `bot` atau `self-chat` | `bot` |
| `WHATSAPP_ALLOWED_USERS` | Filter pengguna (`*` untuk semua) | `*` |

### Telegram

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `TELEGRAM_ENABLED` | Aktifkan integrasi Telegram | `true` |
| `TELEGRAM_BOT_TOKEN` | Token bot dari @BotFather | — |
| `TELEGRAM_ALLOWED_USERS` | Filter user ID (kosongkan untuk semua) | — |

### Email

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `EMAIL_ENABLED` | Aktifkan integrasi Email | `true` |
| `EMAIL_PROVIDER` | Tipe provider email | `imap` |
| `EMAIL_POLL_INTERVAL` | Interval polling dalam detik | `60` |
| `EMAIL_ADDRESS` | Alamat email yang dimonitor | — |
| `EMAIL_PASSWORD` | Password atau app-specific password | — |
| `EMAIL_IMAP_HOST` | Hostname server IMAP | `imap.gmail.com` |
| `EMAIL_SMTP_HOST` | Hostname server SMTP | `smtp.gmail.com` |
| `EMAIL_ALLOWED_USERS` | Filter pengirim email | — |

### Logging

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `LOG_LEVEL` | Level verbositas log | `INFO` |

### Knowledge API

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `KNOWLEDGE_API_URL` | URL endpoint knowledge API eksternal | — |
| `KNOWLEDGE_API_TOKEN` | Token autentikasi knowledge API | — |

## Channels

Hermes mendukung tiga kanal komunikasi:

### WhatsApp

- **Mode bot**: Menggunakan nomor telepon dedicated untuk agen
- **Interaksi**: Direct message atau tag/reply di grup
- **Konfigurasi**: Set `WHATSAPP_ENABLED=true` dan `WHATSAPP_MODE=bot`
- **Pengaturan grup**: Lihat `automations/whatsapp.yaml` untuk atur `require_mention` dan aturan AI per grup

### Telegram

- **Interaksi**: Kirim pesan ke bot atau tambahkan bot ke grup
- **Konfigurasi**: Set `TELEGRAM_ENABLED=true` dan isi `TELEGRAM_BOT_TOKEN` dari @BotFather
- **Pengaturan grup**: Lihat `automations/telegram.yaml` untuk daftar grup yang dimonitor

### Email

- **Interaksi**: Kirim email ke alamat yang dimonitor, Hermes akan membalas secara otomatis
- **Konfigurasi**: Set `EMAIL_ENABLED=true`, isi kredensial IMAP/SMTP
- **Multi-akun**: Konfigurasikan akun tambahan di `automations/email.yaml`
- **Polling**: Hermes mengecek email baru setiap `EMAIL_POLL_INTERVAL` detik (default: 60)

## Knowledge Base

Knowledge base adalah kumpulan file markdown di direktori `knowledges/` yang menjadi sumber informasi utama Hermes. Agent akan memprioritaskan informasi dari knowledge base dibanding jawaban yang di-generate.

### Struktur

```
knowledges/
├── networking/
│   ├── wifi.md          # WiFi Kampus
│   └── lan.md           # Jaringan LAN
├── regulation/
│   └── sop.md           # SOP Layanan
├── domain/
│   └── domain.md        # Domain ITK
├── email/
│   └── email.md         # Email Institusi
├── helpdesk/
│   └── helpdesk.md      # Helpdesk UPA TIK
├── hosting/
│   └── hosting.md       # Hosting
└── web-apps/
    └── web-apps.md      # Aplikasi Web (OJS, OMP, ITK Press, Repository, SSO, VPN)
```

### Mengedit Knowledge Base

Setiap file knowledge mengikuti struktur berikut:

```markdown
# [Nama Domain]

## Deskripsi Layanan
<!-- Jelaskan layanan ini secara singkat -->

## Cara Akses
<!-- Langkah-langkah untuk mengakses layanan -->

## Troubleshooting
<!-- Masalah umum dan solusinya -->

## FAQ
<!-- Pertanyaan yang sering ditanyakan -->

## Kontak
<!-- Siapa yang dihubungi jika masalah tidak terselesaikan -->
```

Untuk menambah atau mengedit knowledge:

1. Buka file markdown yang sesuai di direktori `knowledges/`
2. Isi atau perbarui konten sesuai template di atas
3. Restart container agar perubahan diterapkan: `docker-compose restart`

Untuk menambah domain baru:

1. Buat direktori baru di `knowledges/` (misal: `knowledges/vpn/`)
2. Buat file markdown di dalamnya (misal: `vpn.md`)
3. Ikuti struktur template yang sama
4. Restart container

## Development

Untuk pengembangan lokal, gunakan `docker-compose.override.yml` yang secara otomatis di-merge dengan `docker-compose.yaml`:

```bash
# Salin template environment untuk development
cp .env.example .env.development

# Edit konfigurasi development
nano .env.development

# Jalankan (override otomatis diterapkan)
docker-compose up -d
```

Override file melakukan:
- Menggunakan `.env.development` sebagai sumber environment
- Mengaktifkan dashboard (`HERMES_DASHBOARD=1`)
- Set log level ke `DEBUG`
- Menaikkan batas memori ke 2GB dan shared memory ke 1GB

Untuk menjalankan tanpa override (simulasi production):

```bash
docker-compose -f docker-compose.yaml up -d
```

## Deployment

Langkah deployment ke production VPS (Debian 13):

### 1. Instalasi Docker

```bash
# Install Docker dan Docker Compose
curl -fsSL https://get.docker.com | sh
```

### 2. Buat Docker Network

```bash
docker network create ai-network
```

### 3. Clone dan Konfigurasi

```bash
git clone <repository-url> /opt/hermes
cd /opt/hermes

# Salin dan edit environment production
cp .env.example .env.production
nano .env.production
```

### 4. Jalankan

```bash
docker-compose up -d
```

### 5. Verifikasi

```bash
# Cek status container
docker-compose ps

# Cek health
curl http://127.0.0.1:8642/health

# Lihat log
docker-compose logs -f --tail=50
```

### Maintenance

```bash
# Restart setelah perubahan konfigurasi
docker-compose restart

# Update image
docker-compose pull && docker-compose up -d

# Lihat resource usage
docker stats hermes
```

## Roadmap

Fitur yang direncanakan untuk pengembangan selanjutnya:

- [ ] Dashboard monitoring
- [ ] Analytics dan reporting
- [ ] Dukungan multi-bahasa
- [ ] Integrasi dengan SIAKAD (Sistem Informasi Akademik)
- [ ] Pembuatan tiket otomatis dari percakapan
- [ ] Dukungan pesan suara (voice message)

## Kontribusi

1. Fork repository ini
2. Buat branch fitur (`git checkout -b fitur/nama-fitur`)
3. Commit perubahan (`git commit -m "Tambah fitur X"`)
4. Push ke branch (`git push origin fitur/nama-fitur`)
5. Buat Pull Request

### Panduan Kontribusi

- Gunakan bahasa Indonesia untuk dokumentasi dan knowledge base
- Ikuti struktur template yang sudah ada untuk knowledge base
- Jangan commit file `.env`, `.env.development`, atau `.env.production`
- Test perubahan secara lokal menggunakan `docker-compose.override.yml`
