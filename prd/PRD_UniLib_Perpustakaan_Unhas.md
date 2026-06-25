# Product Requirements Document (PRD)
# UniLib — Perpustakaan Digital Universitas Hasanuddin

| Field | Detail |
|---|---|
| Nama Produk | UniLib (Perpustakaan Digital Unhas) |
| Versi Dokumen | 1.0 |
| Tanggal | 25 Juni 2026 |
| Stack Teknologi | Python, Flask, MySQL |
| Status | Draft untuk pengembangan |

---

## 1. Latar Belakang & Tujuan

### 1.1 Latar Belakang
Perpustakaan universitas membutuhkan portal digital yang tidak hanya menampilkan informasi statis, tapi juga mudah dikelola oleh staf non-teknis (pustakawan/admin konten) tanpa harus mengubah kode setiap kali ada perubahan informasi — seperti berita terbaru, link jurnal elektronik, atau perubahan visi-misi.

### 1.2 Tujuan Produk
1. Menyediakan landing page modern (Liquid Glass UI) yang menjadi pusat informasi perpustakaan: profil, repository, e-journal, dan layanan.
2. Menyediakan **Admin Panel/CMS** agar konten (berita, profil, link navigasi, menu layanan) dapat diubah tanpa coding.
3. Menyediakan sistem **manajemen pengguna berbasis peran (role-based)**: Admin dan Staff, dengan hak akses berbeda.
4. Menjamin keamanan akses (autentikasi, otorisasi per-role, audit log aktivitas).

### 1.3 Referensi Desain
Desain visual mengacu pada mockup yang diberikan (gaya **Liquid Glass UI** — frosted glass panel, rounded corner 24–32px, gradasi biru lembut, shadow halus), dengan struktur halaman:
- Navbar pill mengambang (Beranda, Profil, Repository, E-Journal, Layanan)
- Hero section dengan headline besar + 2 CTA button
- Statistik (counter) 4 kolom
- Section "Berita & Acara Terkini" (card berita)
- Section tambahan: Repository Highlight, Digital Journal (ScienceDirect/EBSCOhost), Services, Facilities, Location, Footer

> Catatan implementasi: Efek glassmorphism (`backdrop-filter: blur()`) dibuat dengan Tailwind CSS / CSS custom di sisi front-end (Jinja2 templates), bukan oleh Flask. PRD ini fokus pada fungsionalitas dan data, sementara detail UI mengikuti spesifikasi desain Stitch yang sudah ada.

---

## 2. Target Pengguna

| Aktor | Deskripsi | Akses |
|---|---|---|
| **Pengunjung (Visitor)** | Mahasiswa, dosen, umum — tidak login | Read-only: lihat beranda, profil, daftar repository, e-journal, layanan, berita |
| **Staff** | Pustakawan / staf konten perpustakaan | Login ke dashboard; CRUD berita, edit profil (visi-misi, struktur organisasi, jam layanan, fasilitas), kelola link repository (navbar), kelola link e-journal, kelola menu layanan |
| **Admin** | Pengelola sistem (kepala perpustakaan / IT) | Semua akses Staff **+** CRUD akun user (Admin/Staff), monitoring aktivitas user, manajemen statistik counter di beranda |

---

## 3. Lingkup Proyek (Scope)

### 3.1 In-Scope
- Landing page publik (multi-section sesuai desain)
- Sistem autentikasi & otorisasi (login, logout, role-based access control)
- Modul **CMS Berita** (create, read, update, delete, publish/draft)
- Modul **CMS Profil** (Profil Perpustakaan, Visi & Misi, Struktur Organisasi, Jam Pelayanan, Fasilitas)
- Modul **Manajemen Link Navigasi**: Repository (dropdown navbar) & E-Journal (dropdown navbar, mis. ScienceDirect, EBSCOhost)
- Modul **Manajemen Menu Layanan** (Membership, Borrowing, Repository, Reference, Library Clearance, dst — dinamis)
- Modul **Manajemen Statistik** (4 counter di beranda: Koleksi Repository, Buku Digital, Jurnal Internasional, Pengunjung Harian)
- Modul **Manajemen User** (khusus Admin): CRUD akun, reset password, aktif/nonaktifkan akun
- **Activity Log** untuk audit (siapa mengubah apa, kapan)
- Upload gambar (untuk berita, fasilitas, thumbnail) tersimpan di server/cloud storage
- Dashboard admin/staff yang ringkas dan mobile-responsive

### 3.2 Out of Scope (Fase 1 / MVP)
- Sistem peminjaman buku fisik (OPAC katalog katalog lengkap)
- Integrasi pembayaran/denda
- Single Sign-On (SSO) dengan akun kampus (SIAKAD/SSO Unhas) — dipertimbangkan di fase berikutnya
- Live chat / chatbot AI search (disebut di mockup berita "Peluncuran Sistem AI Search" hanya sebagai *konten berita*, bukan fitur nyata di fase ini)
- Aplikasi mobile native

---

## 4. Arsitektur & Tech Stack

| Layer | Teknologi |
|---|---|
| Backend Framework | Flask (Python 3.11+) |
| ORM | Flask-SQLAlchemy |
| Database | MySQL 8.x |
| Migrasi DB | Flask-Migrate (Alembic) |
| Autentikasi | Flask-Login + Werkzeug (password hashing) |
| Form & CSRF Protection | Flask-WTF |
| Template Engine | Jinja2 |
| Styling | Tailwind CSS (untuk efek glassmorphism) |
| Interaktivitas Frontend | Vanilla JS / Alpine.js (animasi counter, scroll reveal, navbar shrink) |
| File/Image Storage | Local `/static/uploads` (fase 1) → opsi migrasi ke object storage (S3-compatible) di fase 2 |
| Deployment | Gunicorn + Nginx (production), dapat dikemas dengan Docker |
| Environment Config | `.env` (python-dotenv) untuk kredensial DB, secret key |

### 4.1 Struktur Proyek (usulan)
```
unilib/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/               # SQLAlchemy models
│   ├── routes/
│   │   ├── public.py         # Beranda, profil, repository, ejournal, layanan, detail berita
│   │   ├── auth.py           # Login/logout
│   │   ├── admin.py          # CRUD user, monitoring
│   │   └── staff.py          # CRUD berita, profil, link, layanan, statistik
│   ├── forms/                # Flask-WTF forms
│   ├── templates/
│   │   ├── public/
│   │   └── dashboard/
│   ├── static/
│   └── utils/                # decorators (role_required), helper upload gambar
├── migrations/
├── config.py
├── requirements.txt
└── run.py
```

---

## 5. Functional Requirements

### 5.1 Modul Publik (Tanpa Login)

| ID | Requirement |
|---|---|
| PUB-01 | Sistem menampilkan halaman Beranda sesuai desain (hero, statistik, berita terkini) |
| PUB-02 | Sistem menampilkan submenu Profil: Profil Perpustakaan, Visi & Misi, Struktur Organisasi, Jam Pelayanan, Fasilitas — konten diambil dari database (dapat diedit Staff/Admin) |
| PUB-03 | Sistem menampilkan dropdown Repository di navbar berisi daftar link yang dikelola Staff/Admin (bisa link internal atau eksternal) |
| PUB-04 | Sistem menampilkan dropdown E-Journal di navbar (mis. ScienceDirect, EBSCOhost) sesuai data dari database |
| PUB-05 | Sistem menampilkan menu Layanan dengan daftar item dinamis (judul, deskripsi, ikon, link) |
| PUB-06 | Sistem menampilkan daftar berita (card) dengan kategori badge, tanggal publikasi, ringkasan, dan tautan "Baca Selengkapnya" ke halaman detail |
| PUB-07 | Sistem menampilkan halaman detail berita lengkap (judul, gambar, isi, tanggal, penulis) |
| PUB-08 | Statistik counter (Koleksi Repository, Buku Digital, Jurnal Internasional, Pengunjung Harian) ditampilkan dengan animasi number-counter, nilai diambil dari database |
| PUB-09 | Halaman bersifat responsif (desktop, tablet, mobile) |

### 5.2 Modul Autentikasi

| ID | Requirement |
|---|---|
| AUTH-01 | Form login (username/email + password) dengan validasi dan pesan error yang jelas |
| AUTH-02 | Password disimpan dengan hashing (Werkzeug `generate_password_hash`) |
| AUTH-03 | Sesi login dikelola dengan Flask-Login; redirect otomatis ke dashboard sesuai role setelah login |
| AUTH-04 | Logout menghapus sesi pengguna |
| AUTH-05 | Rute dashboard dilindungi `@login_required` dan decorator `@role_required(...)` |
| AUTH-06 | Pembatasan percobaan login (rate limiting) untuk mencegah brute force |
| AUTH-07 | Fitur "lupa password" (reset via token email) — opsional fase 2 |

### 5.3 Modul Staff (Akses: Staff & Admin)

**a) CRUD Berita**
| ID | Requirement |
|---|---|
| NEWS-01 | Staff dapat membuat berita baru (judul, kategori, gambar cover, isi konten rich-text, status draft/publish) |
| NEWS-02 | Staff dapat mengedit & menghapus berita yang ada |
| NEWS-03 | Staff dapat mengatur status publish/draft dan tanggal publikasi |
| NEWS-04 | Sistem otomatis membuat slug URL ramah-SEO dari judul berita |
| NEWS-05 | Upload gambar berita divalidasi (tipe file, ukuran maksimum) dan dikompresi/resize otomatis |

**b) Edit Profil (Konten Statis)**
| ID | Requirement |
|---|---|
| PROF-01 | Staff dapat mengedit konten section: Profil Perpustakaan, Visi & Misi, Struktur Organisasi, Jam Pelayanan, Fasilitas |
| PROF-02 | Setiap section mendukung rich-text editor (WYSIWYG, mis. CKEditor/TinyMCE) dan upload gambar pendukung |
| PROF-03 | Sistem menyimpan riwayat siapa & kapan terakhir mengubah tiap section (updated_by, updated_at) |

**c) Manajemen Link Repository (Navbar)**
| ID | Requirement |
|---|---|
| REPO-01 | Staff dapat menambah/edit/hapus item link Repository yang muncul di dropdown navbar |
| REPO-02 | Setiap item memiliki: nama tampilan, URL tujuan, urutan tampil (order), status aktif/nonaktif |
| REPO-03 | Perubahan langsung tercermin di navbar publik tanpa perlu deploy ulang |

**d) Manajemen Link E-Journal (Navbar)**
| ID | Requirement |
|---|---|
| EJOUR-01 | Staff dapat menambah/edit/hapus item E-Journal (nama, logo, deskripsi singkat, URL akses, urutan, status aktif) |
| EJOUR-02 | Tampilan section "Digital Journal" di beranda (kartu ScienceDirect, EBSCOhost, dst) mengambil data dari tabel yang sama |

**e) Manajemen Menu Layanan**
| ID | Requirement |
|---|---|
| SERV-01 | Staff dapat menambah/edit/hapus item Layanan (judul, deskripsi, ikon, link/halaman tujuan, urutan, status aktif) |
| SERV-02 | Item layanan ditampilkan otomatis di section "Services" beranda |

**f) Manajemen Statistik Counter**
| ID | Requirement |
|---|---|
| STAT-01 | Staff/Admin dapat mengubah nilai angka statistik (Koleksi Repository, Buku Digital, Jurnal Internasional, Pengunjung Harian) atau menambah kartu statistik baru |

### 5.4 Modul Admin (Akses: Admin saja)

| ID | Requirement |
|---|---|
| ADM-01 | Admin dapat melihat daftar seluruh user (Admin & Staff) dengan informasi nama, email, role, status aktif, login terakhir |
| ADM-02 | Admin dapat membuat akun user baru (set nama, email/username, password awal, role) |
| ADM-03 | Admin dapat mengedit data user (nama, email, role) dan mereset password user |
| ADM-04 | Admin dapat menonaktifkan (suspend) atau menghapus akun user |
| ADM-05 | Admin dapat melihat log aktivitas user (mis. "Staff X menambahkan berita Y pada tanggal Z") untuk keperluan monitoring/audit |
| ADM-06 | Admin memiliki akses penuh ke seluruh modul Staff (berita, profil, link, layanan, statistik) |
| ADM-07 | Sistem mencegah Admin menghapus akunnya sendiri jika itu satu-satunya akun Admin aktif (safety guard) |

---

## 6. Desain Skema Database (MySQL)

### 6.1 Tabel Utama

**`users`**
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| full_name | VARCHAR(150) | |
| email | VARCHAR(150), UNIQUE | |
| username | VARCHAR(80), UNIQUE | |
| password_hash | VARCHAR(255) | |
| role | ENUM('admin','staff') | |
| is_active | BOOLEAN, default TRUE | |
| last_login_at | DATETIME, nullable | |
| created_at | DATETIME | |
| updated_at | DATETIME | |

**`news`** (Berita)
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| title | VARCHAR(255) | |
| slug | VARCHAR(255), UNIQUE | |
| category | VARCHAR(50) | mis. Riset, Event, Akademik |
| cover_image | VARCHAR(255) | path/URL gambar |
| excerpt | TEXT | ringkasan untuk card |
| content | LONGTEXT | isi rich-text |
| status | ENUM('draft','published') | |
| published_at | DATETIME, nullable | |
| author_id | INT, FK → users.id | |
| created_at | DATETIME | |
| updated_at | DATETIME | |

**`profile_sections`** (Profil Perpustakaan, Visi-Misi, dll — konten statis editable)
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| section_key | VARCHAR(50), UNIQUE | `profil_perpustakaan`, `visi_misi`, `struktur_organisasi`, `jam_pelayanan`, `fasilitas` |
| title | VARCHAR(150) | |
| content | LONGTEXT | rich-text HTML |
| image_url | VARCHAR(255), nullable | |
| updated_by | INT, FK → users.id | |
| updated_at | DATETIME | |

**`nav_links`** (menggabungkan Repository & E-Journal dengan kolom `type`)
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| type | ENUM('repository','ejournal') | |
| name | VARCHAR(150) | mis. "ScienceDirect" |
| description | TEXT, nullable | khusus e-journal |
| logo_url | VARCHAR(255), nullable | |
| url | VARCHAR(255) | |
| sort_order | INT, default 0 | |
| is_active | BOOLEAN, default TRUE | |
| created_at | DATETIME | |

**`services`** (Menu Layanan)
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| title | VARCHAR(150) | |
| description | TEXT | |
| icon | VARCHAR(100) | nama icon (mis. dari icon set) |
| link_url | VARCHAR(255), nullable | |
| sort_order | INT, default 0 | |
| is_active | BOOLEAN, default TRUE | |

**`statistics`** (Counter di beranda)
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| label | VARCHAR(100) | mis. "KOLEKSI REPOSITORY" |
| value | INT | mis. 15420 |
| icon | VARCHAR(100), nullable | |
| sort_order | INT, default 0 | |

**`activity_logs`**
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT, PK, AI | |
| user_id | INT, FK → users.id | |
| action | VARCHAR(255) | mis. "create_news", "delete_user" |
| target_type | VARCHAR(50), nullable | mis. "news", "user" |
| target_id | INT, nullable | |
| description | TEXT, nullable | |
| created_at | DATETIME | |

### 6.2 Diagram Relasi (ringkas)
```
users (1) ───< (banyak) news            [author_id]
users (1) ───< (banyak) profile_sections [updated_by]
users (1) ───< (banyak) activity_logs    [user_id]
```
Tabel `nav_links`, `services`, `statistics` berdiri independen (tidak butuh relasi langsung ke users selain log perubahan via `activity_logs`).

---

## 7. Hak Akses (Permission Matrix)

| Fitur | Visitor | Staff | Admin |
|---|:---:|:---:|:---:|
| Lihat halaman publik | ✅ | ✅ | ✅ |
| Login dashboard | ❌ | ✅ | ✅ |
| CRUD Berita | ❌ | ✅ | ✅ |
| Edit Profil/Visi-Misi/dll | ❌ | ✅ | ✅ |
| Kelola Link Repository | ❌ | ✅ | ✅ |
| Kelola Link E-Journal | ❌ | ✅ | ✅ |
| Kelola Menu Layanan | ❌ | ✅ | ✅ |
| Kelola Statistik Counter | ❌ | ✅ | ✅ |
| CRUD Akun User | ❌ | ❌ | ✅ |
| Lihat Log Aktivitas | ❌ | ❌ | ✅ |

---

## 8. Non-Functional Requirements

| Kategori | Requirement |
|---|---|
| **Keamanan** | CSRF protection (Flask-WTF) di semua form; sanitasi input rich-text untuk mencegah XSS (mis. `bleach`); validasi tipe & ukuran file upload; password hashing; HTTPS di production |
| **Performa** | Lazy-load gambar; caching halaman publik (Flask-Caching) untuk konten yang jarang berubah; optimasi query dengan index pada kolom slug, email, status |
| **Skalabilitas** | Struktur kode modular (blueprint Flask) agar mudah menambah modul baru (mis. OPAC di fase berikutnya) |
| **Usability** | Dashboard admin/staff sederhana, mobile-friendly, feedback jelas (flash messages) saat CRUD berhasil/gagal |
| **Maintainability** | Migrasi DB terversi (Flask-Migrate); environment config terpisah (dev/staging/prod) |
| **Aksesibilitas** | Kontras warna memenuhi standar dasar WCAG AA pada teks di atas glass panel; alt text pada gambar |
| **SEO** | Slug URL ramah-SEO untuk berita; meta title/description per halaman |

---

## 9. Alur Pengguna Utama (User Flow)

### 9.1 Staff menambahkan berita
1. Staff login → diarahkan ke Dashboard Staff
2. Klik "Berita" → "Tambah Berita Baru"
3. Isi judul, kategori, upload gambar cover, tulis isi konten
4. Pilih status: Draft (simpan tanpa tayang) atau Publish (tayang langsung)
5. Sistem menyimpan, mencatat di `activity_logs`, redirect ke daftar berita dengan notifikasi sukses

### 9.2 Admin membuat akun Staff baru
1. Admin login → Dashboard Admin → "Manajemen User"
2. Klik "Tambah User" → isi nama, email/username, role = Staff, set password awal
3. Sistem membuat akun, mengirim notifikasi (opsional via email), mencatat log
4. Staff baru dapat login dengan kredensial tersebut

### 9.3 Pengunjung menjelajah Repository via Navbar
1. Pengunjung hover/klik menu "Repository" di navbar
2. Dropdown menampilkan daftar link yang dikelola Staff (real-time dari database)
3. Klik salah satu → diarahkan ke URL tujuan (internal/eksternal)

---

## 10. Roadmap Pengembangan

| Fase | Lingkup | Estimasi |
|---|---|---|
| **Fase 0** | Setup project (Flask app factory, koneksi MySQL, struktur folder, auth dasar) | 1 minggu |
| **Fase 1 — MVP** | Halaman publik statis sesuai desain + Auth + CRUD Berita + Edit Profil sections | 2–3 minggu |
| **Fase 2** | Manajemen Link Repository/E-Journal, Manajemen Layanan, Manajemen Statistik | 1–2 minggu |
| **Fase 3** | Modul Admin: CRUD User, Activity Log, Permission guard menyeluruh | 1–2 minggu |
| **Fase 4** | Polish UI (animasi Liquid Glass, responsif penuh), testing, deployment | 1–2 minggu |

---

## 11. Asumsi & Risiko

| Jenis | Catatan |
|---|---|
| Asumsi | Tidak ada integrasi SSO kampus di fase awal; jumlah staff/admin relatif kecil (puluhan, bukan ribuan) |
| Risiko | Konten rich-text dari Staff berpotensi XSS jika tidak disanitasi — mitigasi: gunakan `bleach`/whitelist tag HTML |
| Risiko | Upload gambar besar memperlambat halaman — mitigasi: resize/compress otomatis saat upload (Pillow) |
| Risiko | Hak akses yang salah konfigurasi bisa membocorkan akses dashboard — mitigasi: testing menyeluruh pada decorator `role_required` |

---

## 12. Metrik Keberhasilan (Success Metrics)

- Staff dapat menerbitkan berita baru dalam < 3 menit tanpa bantuan developer
- Perubahan link Repository/E-Journal/Layanan langsung tampil di frontend tanpa deploy ulang
- 0 insiden akses tidak sah ke dashboard oleh non-staff/non-admin (diverifikasi via activity log)
- Waktu muat halaman beranda < 2.5 detik (di koneksi standar)

---

*Dokumen ini adalah baseline requirement; detail UI (warna, spacing, animasi) tetap mengikuti referensi desain Stitch yang sudah dibuat dan dapat disesuaikan saat implementasi front-end.*
