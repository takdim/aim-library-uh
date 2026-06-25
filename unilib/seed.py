"""
seed.py — Initial data seeder for UniLib
Run: python seed.py
"""
import os
from datetime import datetime, timezone
from app import create_app, db
from app.models.user import User
from app.models.news import News
from app.models.profile import ProfileSection
from app.models.nav_link import NavLink
from app.models.service import Service
from app.models.statistic import Statistic

app = create_app(os.environ.get('FLASK_ENV', 'development'))


def seed():
    with app.app_context():
        db.create_all()

        # ── Admin user ──────────────────────────────────────────
        if not User.query.filter_by(username='admin').first():
            admin = User(
                full_name='Administrator Perpustakaan',
                email='admin@lib.unhas.ac.id',
                username='admin',
                role='admin',
                is_active=True,
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print('✓ Admin user dibuat (admin / admin123)')
        else:
            print('  Admin user sudah ada')

        # ── Staff user ──────────────────────────────────────────
        if not User.query.filter_by(username='staff1').first():
            staff = User(
                full_name='Pustakawan Contoh',
                email='staff@lib.unhas.ac.id',
                username='staff1',
                role='staff',
                is_active=True,
            )
            staff.set_password('staff123')
            db.session.add(staff)
            print('✓ Staff user dibuat (staff1 / staff123)')

        db.session.flush()

        admin = User.query.filter_by(username='admin').first()

        # ── Profile sections ────────────────────────────────────
        default_profiles = [
            ('profil_perpustakaan', 'Profil Perpustakaan',
             '<p>Perpustakaan Universitas Hasanuddin (Unhas) merupakan salah satu unit pelayanan akademik yang berperan penting dalam mendukung kegiatan pendidikan, penelitian, dan pengabdian kepada masyarakat di lingkungan Universitas Hasanuddin.</p>'
             '<p>Didirikan sejak Universitas Hasanuddin berdiri, perpustakaan terus berkembang menjadi pusat sumber daya informasi modern yang mengintegrasikan koleksi tercetak dan digital untuk memenuhi kebutuhan sivitas akademika.</p>'),
            ('visi_misi', 'Visi & Misi',
             '<h3>Visi</h3><p>Menjadi perpustakaan perguruan tinggi terkemuka di kawasan timur Indonesia yang mendukung pengembangan ilmu pengetahuan dan teknologi berbasis riset.</p>'
             '<h3>Misi</h3><ul><li>Menyediakan layanan informasi yang berkualitas dan mudah diakses oleh sivitas akademika Unhas.</li>'
             '<li>Mengembangkan koleksi yang relevan, komprehensif, dan mutakhir.</li>'
             '<li>Mendukung kegiatan penelitian melalui akses ke sumber informasi global.</li>'
             '<li>Menyelenggarakan layanan yang berorientasi pada kepuasan pengguna.</li></ul>'),
            ('struktur_organisasi', 'Struktur Organisasi',
             '<p>Perpustakaan Universitas Hasanuddin dipimpin oleh seorang Kepala Perpustakaan yang membawahi beberapa bidang layanan dan dukungan teknis.</p>'
             '<ul><li><strong>Kepala Perpustakaan</strong></li><li>Bidang Layanan Teknis</li><li>Bidang Layanan Pemustaka</li><li>Bidang Pengembangan Koleksi</li><li>Bidang Teknologi Informasi</li></ul>'),
            ('jam_pelayanan', 'Jam Pelayanan',
             '<table><thead><tr><th>Hari</th><th>Jam</th></tr></thead><tbody>'
             '<tr><td>Senin – Kamis</td><td>08.00 – 16.00 WITA</td></tr>'
             '<tr><td>Jumat</td><td>08.00 – 11.30 WITA (Istirahat), 13.30 – 16.00 WITA</td></tr>'
             '<tr><td>Sabtu – Minggu</td><td>Tutup</td></tr>'
             '</tbody></table>'),
            ('fasilitas', 'Fasilitas',
             '<p>Perpustakaan Universitas Hasanuddin menyediakan berbagai fasilitas modern untuk mendukung kenyamanan belajar:</p>'
             '<ul><li>Ruang baca ber-AC yang nyaman dengan kapasitas 500 orang</li>'
             '<li>Komputer akses internet berkecepatan tinggi (100+ unit)</li>'
             '<li>Ruang diskusi dan ruang belajar mandiri</li>'
             '<li>Loker penyimpanan barang</li>'
             '<li>Akses Wi-Fi di seluruh area perpustakaan</li>'
             '<li>Ruang multimedia dan audio-visual</li>'
             '<li>Mesin fotokopi dan print mandiri</li></ul>'),
        ]

        for key, title, content in default_profiles:
            if not ProfileSection.query.filter_by(section_key=key).first():
                section = ProfileSection(
                    section_key=key,
                    title=title,
                    content=content,
                    updated_by=admin.id,
                    updated_at=datetime.now(timezone.utc),
                )
                db.session.add(section)
        print('✓ Profile sections dibuat')

        # ── Statistics ──────────────────────────────────────────
        stats_data = [
            ('Koleksi Repository', 15420, 'folder_open', 0),
            ('Buku Digital', 8500, 'menu_book', 1),
            ('Jurnal Internasional', 25000, 'article', 2),
            ('Pengunjung Harian', 1200, 'group', 3),
        ]
        for label, value, icon, order in stats_data:
            if not Statistic.query.filter_by(label=label).first():
                db.session.add(Statistic(label=label, value=value, icon=icon, sort_order=order))
        print('✓ Statistik dibuat')

        # ── Nav Links — Repository ──────────────────────────────
        repos = [
            ('Repository Unhas', 'http://repository.unhas.ac.id', 0),
            ('Institutional Repository', 'http://eprints.unhas.ac.id', 1),
            ('Karya Ilmiah Mahasiswa', 'http://repository.unhas.ac.id/karya', 2),
        ]
        for name, url, order in repos:
            if not NavLink.query.filter_by(name=name, type='repository').first():
                db.session.add(NavLink(
                    type='repository', name=name, url=url, sort_order=order, is_active=True
                ))
        print('✓ Repository links dibuat')

        # ── Nav Links — E-Journal ───────────────────────────────
        ejournals = [
            ('ScienceDirect', 'https://www.sciencedirect.com', 'Akses jutaan artikel ilmiah dari Elsevier', 0),
            ('EBSCOhost', 'https://www.ebsco.com', 'Database multidisiplin terbesar di dunia', 1),
            ('ProQuest', 'https://www.proquest.com', 'Sumber tesis, disertasi, dan jurnal global', 2),
            ('Springer Link', 'https://link.springer.com', 'Jurnal dan buku teks dari Springer Nature', 3),
        ]
        for name, url, desc, order in ejournals:
            if not NavLink.query.filter_by(name=name, type='ejournal').first():
                db.session.add(NavLink(
                    type='ejournal', name=name, url=url,
                    description=desc, sort_order=order, is_active=True
                ))
        print('✓ E-Journal links dibuat')

        # ── Services ────────────────────────────────────────────
        services_data = [
            ('Keanggotaan', 'Daftar sebagai anggota perpustakaan untuk akses penuh ke semua layanan.', 'badge', '#', 0),
            ('Peminjaman Buku', 'Pinjam koleksi buku fisik dengan prosedur mudah dan cepat.', 'book_2', '#', 1),
            ('Akses Repository', 'Akses karya ilmiah, skripsi, tesis, dan disertasi civitas akademika.', 'folder_open', '#', 2),
            ('Referensi', 'Konsultasi dengan pustakawan untuk penelusuran literatur dan sumber informasi.', 'support_agent', '#', 3),
            ('Library Clearance', 'Pengurusan bebas pustaka untuk wisudawan dan pegawai yang akan pindah.', 'verified', '#', 4),
            ('Inter-Library Loan', 'Pinjam koleksi dari perpustakaan universitas lain dalam jaringan.', 'share', '#', 5),
        ]
        for title, desc, icon, link, order in services_data:
            if not Service.query.filter_by(title=title).first():
                db.session.add(Service(
                    title=title, description=desc, icon=icon,
                    link_url=link, sort_order=order, is_active=True
                ))
        print('✓ Layanan dibuat')

        # ── Sample News ─────────────────────────────────────────
        news_data = [
            (
                'Peluncuran Sistem Pencarian Digital Terbaru Perpustakaan Unhas',
                'Riset',
                'news/news_sample1.png',
                'Perpustakaan Unhas meluncurkan sistem pencarian digital generasi baru yang memudahkan penelusuran literatur ilmiah.',
                '<p>Perpustakaan Universitas Hasanuddin dengan bangga meluncurkan sistem pencarian digital terbaru yang dirancang untuk mempermudah akses sivitas akademika ke sumber daya informasi ilmiah.</p>'
                '<p>Sistem baru ini mengintegrasikan berbagai database jurnal internasional seperti ScienceDirect, EBSCOhost, dan ProQuest dalam satu antarmuka yang intuitif dan responsif.</p>'
                '<p>"Kami berkomitmen untuk terus berinovasi dalam menyediakan layanan perpustakaan yang modern dan memenuhi kebutuhan penelitian warga Unhas," kata Kepala Perpustakaan dalam acara peluncuran.</p>',
            ),
            (
                'Seminar Literasi Digital 2026: Membangun Budaya Membaca di Era Digital',
                'Event',
                'news/news_sample2.png',
                'Perpustakaan Unhas menyelenggarakan seminar literasi digital untuk meningkatkan kesadaran pentingnya membaca di era informasi.',
                '<p>Dalam rangka memperingati Hari Perpustakaan Nasional, Perpustakaan Universitas Hasanuddin menyelenggarakan Seminar Literasi Digital 2026 yang menghadirkan narasumber dari berbagai institusi pendidikan terkemuka.</p>'
                '<p>Seminar ini membahas tantangan dan peluang dalam membangun budaya literasi di tengah arus informasi digital yang semakin deras.</p>'
                '<p>Para peserta yang terdiri dari mahasiswa, dosen, dan tenaga kependidikan mendapat wawasan baru tentang strategi efektif membaca kritis dan evaluasi sumber informasi.</p>',
            ),
            (
                'Penambahan 5.000 Koleksi Jurnal Internasional Terindeks Scopus',
                'Akademik',
                'news/news_sample3.png',
                'Perpustakaan Unhas menambah 5.000 judul jurnal internasional terindeks Scopus untuk mendukung kegiatan penelitian.',
                '<p>Merespons kebutuhan penelitian yang terus meningkat, Perpustakaan Universitas Hasanuddin resmi menambahkan 5.000 judul jurnal internasional terindeks Scopus ke dalam koleksi digitalnya.</p>'
                '<p>Penambahan koleksi ini mencakup berbagai bidang ilmu mulai dari teknik, kedokteran, ilmu sosial, hingga humaniora, sehingga semakin melengkapi kebutuhan referensi seluruh fakultas di Unhas.</p>'
                '<p>Dengan penambahan ini, total koleksi jurnal digital yang dapat diakses sivitas akademika Unhas kini mencapai lebih dari 25.000 judul dari berbagai penerbit internasional ternama.</p>',
            ),
        ]

        for title, category, cover, excerpt, content in news_data:
            if not News.query.filter_by(title=title).first():
                article = News(
                    title=title,
                    category=category,
                    cover_image=cover,
                    excerpt=excerpt,
                    content=content,
                    status='published',
                    published_at=datetime.now(timezone.utc),
                    author_id=admin.id,
                )
                article.generate_slug()
                db.session.add(article)
        print('✓ Berita sampel dibuat')

        db.session.commit()
        print('\n🎉 Seed selesai! Login dengan: admin / admin123')


if __name__ == '__main__':
    seed()
