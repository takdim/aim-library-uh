"""
Translation dictionary for ID/EN language toggle.
Usage in templates: {{ t('key') }}
"""

TRANSLATIONS = {
    # ── Navbar
    'nav_home':             {'id': 'Beranda',     'en': 'Home'},
    'nav_profile':          {'id': 'Profil',      'en': 'About'},
    'nav_services':         {'id': 'Layanan',     'en': 'Services'},
    'nav_news':             {'id': 'Berita',      'en': 'News'},
    'no_links':             {'id': 'Belum ada link', 'en': 'No links yet'},

    # ── Profil dropdown keys (match section_key values)
    'profil_perpustakaan':  {'id': 'Profil Perpustakaan',  'en': 'Library Profile'},
    'visi_misi':            {'id': 'Visi & Misi',          'en': 'Vision & Mission'},
    'struktur_organisasi':  {'id': 'Struktur Organisasi',  'en': 'Organizational Structure'},
    'jam_pelayanan':        {'id': 'Jam Pelayanan',        'en': 'Service Hours'},
    'fasilitas':            {'id': 'Fasilitas',            'en': 'Facilities'},

    # ── Hero
    'hero_badge':   {'id': 'Akses Terbuka 24/7', 'en': 'Open Access 24/7'},
    'hero_title1':  {'id': 'Membangun Masa Depan', 'en': 'Building the Future'},
    'hero_title2':  {'id': 'Melalui Pengetahuan',  'en': 'Through Knowledge'},
    'hero_desc':    {
        'id': 'Perpustakaan digital modern Universitas Hasanuddin — menghubungkan sivitas akademika dengan repository, jurnal internasional, dan layanan akademik.',
        'en': 'The modern digital library of Hasanuddin University — connecting the academic community with repositories, international journals, and academic services.',
    },
    'cta_repo':     {'id': 'Jelajahi Repository', 'en': 'Explore Repository'},
    'cta_services': {'id': 'Lihat Layanan',       'en': 'View Services'},

    # ── Berita
    'news_section_title': {'id': 'Berita',   'en': 'News'},
    'events_and':         {'id': '& Acara',  'en': '& Events'},
    'latest':             {'id': 'Terkini',  'en': 'Latest'},
    'news_desc': {
        'id': 'Informasi terbaru seputar kegiatan, pembaruan sistem, dan koleksi perpustakaan.',
        'en': 'Latest updates on events, system improvements, and library collections.',
    },
    'read_more':    {'id': 'Baca Selengkapnya', 'en': 'Read More'},
    'no_news':      {'id': 'Belum ada berita yang dipublikasikan.', 'en': 'No news published yet.'},

    # ── Repository
    'repo_desc': {
        'id': 'Akses koleksi karya ilmiah, skripsi, tesis, dan disertasi sivitas akademika Universitas Hasanuddin.',
        'en': 'Access scientific works, theses, and dissertations from Hasanuddin University academics.',
    },
    'no_repo': {'id': 'Belum ada repository yang ditambahkan.', 'en': 'No repositories added yet.'},

    # ── E-Journal
    'ej_section_title':  {'id': 'Jurnal',   'en': 'Digital'},
    'ej_section_title2': {'id': 'Digital',  'en': 'Journals'},
    'ej_desc': {
        'id': 'Akses ribuan jurnal internasional terindeks dari database bereputasi global.',
        'en': 'Access thousands of indexed international journals from globally reputed databases.',
    },
    'access_now': {'id': 'Akses Sekarang', 'en': 'Access Now'},
    'no_ej':      {'id': 'Belum ada e-journal yang ditambahkan.', 'en': 'No e-journals added yet.'},

    # ── Layanan / Services
    'services_title1': {'id': 'Layanan', 'en': 'Our'},
    'services_title2': {'id': 'Kami',    'en': 'Services'},
    'services_desc': {
        'id': 'Berbagai layanan perpustakaan untuk mendukung kebutuhan akademik Anda.',
        'en': 'Various library services to support your academic needs.',
    },
    'learn_more':   {'id': 'Selengkapnya',    'en': 'Learn More'},
    'visit_page':   {'id': 'Kunjungi Halaman','en': 'Visit Page'},
    'no_services':  {'id': 'Belum ada layanan yang ditambahkan.', 'en': 'No services added yet.'},
    'no_desc':      {'id': 'Tidak ada deskripsi tersedia.', 'en': 'No description available.'},

    # ── Lokasi
    'find_us':    {'id': 'Temukan Kami', 'en': 'Find Us'},
    'address':    {'id': 'Alamat',       'en': 'Address'},
    'hours':      {'id': 'Jam Layanan',  'en': 'Service Hours'},
    'contact':    {'id': 'Kontak',       'en': 'Contact'},
    'hours_text': {'id': 'Senin – Jumat: 08.00 – 16.00 WITA', 'en': 'Monday – Friday: 08:00 – 16:00 WITA'},

    # ── news_detail
    'back':           {'id': 'Kembali',          'en': 'Back'},
    'home':           {'id': 'Beranda',           'en': 'Home'},
    'news_breadcrumb':{'id': 'Berita',            'en': 'News'},
    'by':             {'id': 'oleh',              'en': 'by'},
    'view_all_news':  {'id': 'Lihat Semua Berita','en': 'View All News'},

    # ── Profil page
    'content_unavailable': {'id': 'Konten belum tersedia.', 'en': 'Content not yet available.'},
}


def get_t(lang: str = 'id'):
    """Returns a translation callable for the given language code."""
    def t(key: str) -> str:
        entry = TRANSLATIONS.get(key)
        if entry is None:
            return key
        return entry.get(lang, entry.get('id', key))
    return t
