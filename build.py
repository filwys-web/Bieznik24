"""Generate the static Bieżnik24 pages from the workshop configuration."""

import json
from html import escape
from pathlib import Path
from urllib.parse import quote_plus
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "docs"
WORKSHOP = json.loads((ROOT / "workshop.json").read_text(encoding="utf-8"))

PAGES = [
    ("index.html", "Strona główna"),
    ("uslugi.html", "Usługi"),
    ("cennik.html", "Cennik"),
    ("o-nas.html", "O nas"),
    ("galeria.html", "Galeria"),
    ("kontakt.html", "Kontakt"),
]

ICONS = {
    "phone": '<path d="M21 16.4v3a2 2 0 0 1-2.2 2A18 18 0 0 1 3 5.2 2 2 0 0 1 5 3h3l1.5 5-2.1 2a13 13 0 0 0 6.6 6.6l2-2.1 5 1.9Z"/>',
    "pin": '<path d="M20 10c0 5-8 11-8 11s-8-6-8-11a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "wheel": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 7v5m-4 3 4-3 4 3"/>',
    "balance": '<circle cx="12" cy="12" r="9"/><path d="M6 12h12m-6-6v12"/><circle cx="12" cy="12" r="2"/>',
    "tool": '<path d="M14 6a5 5 0 0 0-5.9 6.3L3 17.4a2.5 2.5 0 0 0 3.6 3.5l5.1-5.1A5 5 0 0 0 18 10l-3.4 1.5-2.1-2.1L14 6Z"/>',
    "swap": '<path d="M3 8h17l-4-4M21 16H4l4 4"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3Z"/><path d="M9 8h6m-6 4h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "chat": '<path d="M21 11.5A8.5 8.5 0 0 1 12 20a9 9 0 0 1-3.1-.5L4 21l1.5-4.1A8 8 0 0 1 3 11.5 8.5 8.5 0 0 1 12 3a8.5 8.5 0 0 1 9 8.5Z"/><path d="M8 10h8m-8 4h5"/>',
    "expand": '<path d="M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
}

SERVICES = [
    ("wheel", "Sezonowa wymiana opon", "Zdejmujemy opony z felg, zakładamy drugi komplet i wyważamy koła. Przy okazji sprawdzamy bieżnik, stan zaworów i ciśnienie."),
    ("swap", "Wymiana całych kół", "Zakładamy komplet opon już osadzonych na felgach. Sprawdzamy ciśnienie i dokręcamy koła zgodnie z zaleceniami producenta auta."),
    ("balance", "Wyważanie kół", "Na wyważarce wykrywamy niewyważenie i dobieramy odpowiednie ciężarki. To jedna z pierwszych czynności przy drganiach kierownicy podczas jazdy."),
    ("tool", "Naprawa przebicia", "Po zdjęciu opony oceniamy od środka miejsce przebicia i stan karkasu. Naprawę wykonujemy tylko wtedy, gdy uszkodzenie na to pozwala."),
    ("wheel", "Wulkanizacja opon", "Uszczelniamy kwalifikujące się uszkodzenia bieżnika po oględzinach opony. Przy uszkodzeniu boku lub śladach jazdy bez ciśnienia omawiamy wymianę."),
    ("swap", "Montaż i demontaż opon", "Zdejmujemy pojedynczą oponę z felgi lub montujemy nową. Przed założeniem sprawdzamy powierzchnię styku i stan zaworu."),
]

OPTIONAL_SERVICES = [
    ("Prostowanie felg", "Zapytaj o ocenę odkształcenia i możliwość bezpiecznego prostowania felgi."),
    ("Przechowywanie opon", "Zapytaj o wolne miejsce na drugi komplet opon lub kół poza sezonem."),
    ("Czujniki TPMS", "Podaj model i rocznik auta, żeby ustalić dostępność diagnostyki i obsługi czujników ciśnienia."),
]

GALLERY = [
    ("stanowiska", "Stanowiska serwisowe", "Samochody na stanowiskach serwisowych w hali warsztatowej"),
    ("montaz", "Montaż opony", "Mechanik obsługujący montażownicę do opon"),
    ("podnosnik", "Samochód na podnośniku", "Samochód osobowy uniesiony na podnośniku w warsztacie"),
    ("opony", "Opony w warsztacie", "Stos opon samochodowych w warsztacie"),
]

FEATURES = [
    ("receipt", "Cena przed usługą", "Ustalamy zakres i koszt prac."),
    ("balance", "Kontrola po montażu", "Sprawdzamy ciśnienie i dokręcenie."),
    ("phone", "Umawianie telefoniczne", "Dogodny termin bez formularza."),
]

DEMO = WORKSHOP["demo"]
NAME = escape(WORKSHOP["name"])
CITY = escape(WORKSHOP["city"])
DISTRICT = escape(WORKSHOP["district"])
LOCATION = f"{CITY}, {DISTRICT}"
PHONE = escape(WORKSHOP["phone"])
TEL = f'tel:{escape(WORKSHOP["phone_international"])}'
EMAIL = escape(WORKSHOP["email"])
SITE_URL = WORKSHOP["site_url"].rstrip("/")
FIRST_HOURS = " ".join(escape(value) for value in WORKSHOP["hours"][0])
FORM_ENDPOINT = "" if DEMO else WORKSHOP["form_endpoint"]

if not DEMO:
    required = ["street", "postal_code", "administrator", "history", "experience", "site_url"]
    if FORM_ENDPOINT:
        required += ["form_provider", "retention"]
    if any(not WORKSHOP[key].strip() for key in required):
        raise ValueError("Uzupełnij dane warsztatu, adres strony i informacje o przetwarzaniu danych.")
    if WORKSHOP["phone_international"] == "+48000000000" or WORKSHOP["email"].endswith("@example.com"):
        raise ValueError("Zastąp przykładowy telefon i e-mail przed włączeniem trybu produkcyjnego.")
    if not SITE_URL.startswith("https://"):
        raise ValueError("Adres strony musi zaczynać się od https://.")
    if FORM_ENDPOINT and not FORM_ENDPOINT.startswith("https://"):
        raise ValueError("Adres do wysyłki formularza musi zaczynać się od https://.")

ADDRESS = (
    f'{escape(WORKSHOP["street"])}<br>{escape(WORKSHOP["postal_code"])} {CITY}'
    if WORKSHOP["street"]
    else f"{LOCATION}<br><small>Przykładowa lokalizacja</small>"
)
map_location = WORKSHOP["map_query"] if DEMO else (
    WORKSHOP["map_query"] or ", ".join(WORKSHOP[key] for key in ("street", "postal_code", "city"))
)
MAP_QUERY = quote_plus(map_location)
DIRECTIONS = f"https://www.google.com/maps/dir/?api=1&amp;destination={MAP_QUERY}"
MAP_EMBED = escape(WORKSHOP["map_embed_url"] or f"https://maps.google.com/maps?q={MAP_QUERY}&z=14&output=embed")


def icon(name):
    return (
        '<svg class="icon" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


def brand():
    return f"""
      <a class="brand" href="/" aria-label="{NAME} – strona główna">
        <img src="/assets/logo.svg" alt="" width="43" height="43">
        <span><strong>{NAME}</strong><small>Serwis opon</small></span>
      </a>"""


def navigation(page):
    links = "".join(
        f'<a{" aria-current=\"page\"" if path == page else ""} href="{"/" if path == "index.html" else "/" + path}">{label}</a>'
        for path, label in PAGES
    )
    return f"""
    <a class="skip" href="#tresc">Przejdź do treści</a>
    <div class="utility"><div class="container utility-inner">
      <span>{icon("pin")} {LOCATION}</span>
      <span>{icon("clock")} {FIRST_HOURS}</span>
    </div></div>
    <header class="header">
      <div class="container header-inner">
        {brand()}
        <button class="menu-toggle" type="button" aria-label="Otwórz menu" aria-controls="menu" aria-expanded="false" hidden>{icon("menu")}</button>
        <nav id="menu" class="main-nav" aria-label="Menu główne">{links}</nav>
        <a class="button button-dark header-phone" href="{TEL}">{icon("phone")} {PHONE}</a>
      </div>
    </header>"""


def profile_links():
    links = [
        ("Facebook", WORKSHOP["facebook_url"]),
        ("Instagram", WORKSHOP["instagram_url"]),
        ("Wizytówka Google", WORKSHOP["google_profile_url"]),
    ]
    return "".join(f'<a href="{escape(url)}" rel="external">{label}</a>' for label, url in links if url)


def hours():
    rows = "".join(
        f"<div><dt>{escape(day)}</dt><dd>{escape(time)}</dd></div>"
        for day, time in WORKSHOP["hours"]
    )
    return f'<dl class="hours">{rows}</dl>'


def footer():
    badge = '<span>Wersja demonstracyjna</span>' if DEMO else ""
    profiles = profile_links()
    profiles = f'<div class="social-links">{profiles}</div>' if profiles else ""
    return f"""
    <footer class="footer">
      <div class="container footer-main">
        <div>{brand()}<p>Wymiana opon, wyważanie kół i wulkanizacja.<br>{LOCATION}.</p></div>
        <div class="footer-links"><h2>Warsztat</h2><a href="/uslugi.html">Usługi</a><a href="/cennik.html">Cennik</a><a href="/galeria.html">Galeria</a></div>
        <div class="footer-links"><h2>Kontakt</h2><a href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="/kontakt.html">Godziny i dojazd</a>{profiles}</div>
      </div>
      <div class="container footer-bottom"><span>© {NAME}</span>{badge}<a href="/polityka-prywatnosci.html">Polityka prywatności</a></div>
    </footer>
    <div class="mobile-call"><a class="button button-dark" href="{TEL}">{icon("phone")} Zadzwoń i umów wizytę</a></div>"""


def page_head(label, title, intro):
    return f"""
    <section class="page-head">
      <div class="container">
        <nav class="breadcrumb" aria-label="Ścieżka nawigacji"><a href="/">Strona główna</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>
        <h1>{title}</h1><p>{intro}</p>
      </div>
    </section>"""


def service_card(service):
    symbol, title, description = service
    return f'<article class="service-card"><div class="card-icon">{icon(symbol)}</div><h3>{title}</h3><p>{description}</p></article>'


def review_section():
    profile = WORKSHOP["google_profile_url"]
    if profile:
        text = "Przeczytaj opinie klientów o naszym serwisie w wizytówce Google."
        action = f'<a class="button button-outline" href="{escape(profile)}" rel="external">Zobacz opinie w Google</a>'
    else:
        text = "Link do opinii klientów pojawi się po podłączeniu wizytówki warsztatu."
        action = ""
    return f"""
    <section class="section reviews-section" aria-labelledby="opinie">
      <div class="container review-panel">
        <div class="card-icon">{icon("chat")}</div>
        <div><h2 id="opinie">Opinie klientów</h2><p>{text}</p></div>
        {action}
      </div>
    </section>"""


home = f"""
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Wulkanizacja · {LOCATION}</p>
        <h1>Wymiana opon<br>bez komplikacji.</h1>
        <p class="hero-description">Wymieniamy opony i całe koła, wyważamy je i naprawiamy przebicia. Zadzwoń, żeby ustalić dogodny termin.</p>
        <div class="actions">
          <a class="button button-white" href="{TEL}">{icon("phone")} Zadzwoń i umów wizytę</a>
          <a class="button button-light-outline" href="/cennik.html">Sprawdź cennik</a>
        </div>
      </div>
      <div class="hero-media">
        <picture>
          <source media="(max-width: 700px)" srcset="/assets/serwis-kola-720.webp">
          <img src="/assets/serwis-kola.webp" alt="Mechanik pracujący przy kole samochodu w warsztacie" width="1600" height="1100" fetchpriority="high">
        </picture>
      </div>
    </section>
    <section class="features" aria-label="Zalety warsztatu">
      <div class="container feature-list">
        {''.join(f'<div class="feature">{icon(symbol)}<div><strong>{title}</strong><span>{description}</span></div></div>' for symbol, title, description in FEATURES)}
      </div>
    </section>
    <section class="section" aria-labelledby="home-uslugi">
      <div class="container">
        <div class="section-head">
          <div><h2 id="home-uslugi">Usługi wulkanizacyjne</h2><p>Od sezonowej wymiany po naprawę przebitej opony.</p></div>
          <a class="button button-outline" href="/uslugi.html">Wszystkie usługi</a>
        </div>
        <div class="service-grid">{''.join(service_card(SERVICES[i]) for i in (0, 2, 3))}</div>
      </div>
    </section>
    <section class="section section-muted" aria-labelledby="home-godziny">
      <div class="container opening-layout">
        <img class="workshop-photo" src="/assets/stanowiska-560.webp" srcset="/assets/stanowiska-560.webp 560w, /assets/stanowiska.webp 1200w"
             sizes="(max-width: 760px) 100vw, 52vw" alt="Samochody na podnośnikach w warsztacie" width="1200" height="800" loading="lazy" decoding="async">
        <div class="opening-copy">
          <h2 id="home-godziny">Godziny otwarcia</h2>
          <p>{LOCATION}</p>
          {hours()}
          <a class="button button-dark" href="/kontakt.html">Kontakt i dojazd</a>
        </div>
      </div>
    </section>
    {review_section()}
"""

services = f"""
    {page_head("Usługi", "Usługi wulkanizacyjne", "Wymiana opon i kół, wyważanie oraz naprawy po przebiciu.")}
    <section class="section"><div class="container">
      <div class="service-grid">{''.join(service_card(service) for service in SERVICES)}</div>
    </div></section>
    <section class="section section-muted"><div class="container">
      <div class="section-head"><div><h2>Usługi dodatkowe</h2><p>Dostępność ustalamy telefonicznie.</p></div></div>
      <div class="service-grid">
        {''.join(f'<article class="service-card service-compact"><h3>{title}</h3><p>{description}</p></article>' for title, description in OPTIONAL_SERVICES)}
      </div>
    </div></section>
    <section class="section"><div class="container review-panel">
      <div class="card-icon">{icon("receipt")}</div>
      <div><h2>Ile kosztuje serwis?</h2><p>Sprawdź stawki dla rozmiaru i typu Twoich felg.</p></div>
      <a class="button button-dark" href="/cennik.html">Sprawdź cennik</a>
    </div></section>
"""

seasonal_rows = "".join(
    f'<tr><th scope="row">{escape(size)}</th><td>{escape(steel)}</td><td>{escape(alloy)}</td></tr>'
    for size, steel, alloy in WORKSHOP["seasonal_prices"]
)
other_rows = "".join(
    f'<tr><th scope="row">{escape(job)}</th><td>{escape(price)}</td></tr>'
    for job, price in WORKSHOP["other_prices"]
)
price_note = '<p class="notice">Ceny przykładowe. Podane kwoty służą do prezentacji cennika.</p>' if DEMO else ""
prices = f"""
    {page_head("Cennik", "Cennik usług", "Stawki według rozmiaru i typu felgi oraz ceny najczęstszych napraw.")}
    <section class="section"><div class="container narrow">
      {price_note}
      <div class="price-block">
        <h2 id="sezon">Sezonowa wymiana opon</h2>
        <p>Cena za komplet 4 kół. Obejmuje demontaż, montaż i wyważanie.</p>
        <div class="table-card">
          <table aria-labelledby="sezon">
            <thead><tr><th scope="col">Rozmiar felgi</th><th scope="col">Felgi stalowe</th><th scope="col">Felgi aluminiowe</th></tr></thead>
            <tbody>{seasonal_rows}</tbody>
          </table>
        </div>
      </div>
      <div class="price-block">
        <h2 id="pozostale">Pozostałe usługi</h2>
        <div class="table-card">
          <table aria-labelledby="pozostale">
            <thead><tr><th scope="col">Usługa</th><th scope="col">Cena</th></tr></thead>
            <tbody>{other_rows}</tbody>
          </table>
        </div>
      </div>
      <p class="price-disclaimer">Ostateczna cena zależy od rodzaju opony, konstrukcji koła i zakresu pracy. Uszkodzenia wyceniamy po oględzinach. Cenę ustalamy przed rozpoczęciem prac.</p>
      <a class="button button-dark" href="{TEL}">{icon("phone")} Zadzwoń i zapytaj o cenę</a>
    </div></section>
"""

history = (
    '<p>Bieżnik24 to projekt lokalnego serwisu opon na warszawskiej Woli. Oferta skupia się na wymianie opon, wyważaniu i naprawach po przebiciu.</p>'
    if DEMO else f'<p>{escape(WORKSHOP["history"])}</p><p>{escape(WORKSHOP["experience"])}</p>'
)
about = f"""
    {page_head("O nas", "O warsztacie", "Serwis opon i kół samochodów osobowych.")}
    <section class="section"><div class="container about-layout">
      <div class="about-copy">
        <h2>{NAME}</h2>
        {history}
        <h3>Jak wygląda wizyta</h3>
        <p>Na miejscu ustalamy zakres i cenę prac. Przy przebiciu oglądamy oponę od środka i wyjaśniamy, czy można ją bezpiecznie naprawić. Po montażu sprawdzamy ciśnienie i dokręcenie kół.</p>
        <ul class="checklist">
          <li>{icon("check")} Ustalenie ceny przed rozpoczęciem prac</li>
          <li>{icon("check")} Wyważarka i montażownica do opon</li>
          <li>{icon("check")} Krótkie wyjaśnienie wykonanych prac przy odbiorze</li>
        </ul>
      </div>
      <figure class="about-photo">
        <img src="/assets/stanowiska.webp" alt="Stanowiska warsztatu wyposażone w podnośniki samochodowe" width="1200" height="800" decoding="async">
        <figcaption>Zdjęcie poglądowe stanowisk serwisowych</figcaption>
      </figure>
    </div></section>
    <section class="section section-muted"><div class="container review-panel">
      <div class="card-icon">{icon("wheel")}</div><div><h2>Warsztat i wyposażenie</h2><p>Zobacz zdjęcia stanowisk, opon i pracy przy kołach.</p></div>
      <a class="button button-outline" href="/galeria.html">Otwórz galerię</a>
    </div></section>
"""

gallery_cards = "".join(
    f"""
      <figure class="gallery-card">
        <a class="gallery-link" href="/assets/{photo}.webp" aria-label="Powiększ zdjęcie: {caption}">
          <img src="/assets/{photo}-560.webp" alt="{alt}" width="560" height="390" loading="lazy" decoding="async">
          <span class="zoom-icon">{icon("expand")}</span>
        </a>
        <figcaption>{caption}</figcaption>
      </figure>"""
    for photo, caption, alt in GALLERY
)
gallery = f"""
    {page_head("Galeria", "Galeria", "Zdjęcia poglądowe stanowisk, wyposażenia i pracy przy kołach.")}
    <section class="section"><div class="container gallery-grid">{gallery_cards}</div></section>
    <dialog class="lightbox" aria-labelledby="photo-caption">
      <div class="lightbox-inner">
        <button class="lightbox-close" type="button" aria-label="Zamknij zdjęcie" autofocus>{icon("close")}</button>
        <img class="lightbox-photo" src="/assets/stanowiska-560.webp" alt="">
        <div class="lightbox-controls">
          <button class="button button-light-outline" type="button" data-photo-step="-1">Poprzednie</button>
          <p id="photo-caption"></p>
          <button class="button button-light-outline" type="button" data-photo-step="1">Następne</button>
        </div>
      </div>
    </dialog>
"""

if DEMO:
    contact_notice = '<p class="notice">Dane kontaktowe i godziny są przykładowe. Formularz działa w trybie demonstracyjnym.</p>'
    form_help = 'W tej wersji formularz sprawdza pola bez wysyłania wiadomości.'
elif FORM_ENDPOINT:
    contact_notice = ""
    form_help = 'Podane dane wykorzystujemy, żeby odpowiedzieć na Twoje zgłoszenie.'
else:
    contact_notice = ""
    form_help = 'Formularz otworzy wiadomość w Twojej aplikacji pocztowej.'
map_note = "Mapa pokazuje przykładową lokalizację na Woli." if DEMO else "Mapa pokazuje położenie warsztatu."
form_action = f' action="{escape(FORM_ENDPOINT)}"' if FORM_ENDPOINT else ""
form_mode = "demo" if DEMO else "endpoint" if FORM_ENDPOINT else "email"

contact = f"""
    {page_head("Kontakt", "Kontakt i dojazd", "Zadzwoń, żeby zarezerwować termin, lub napisz w sprawie usługi.")}
    <section class="section"><div class="container">
      {contact_notice}
      <div class="contact-grid">
        <div class="contact-card">
          <h2>Dane warsztatu</h2>
          <div class="contact-detail">{icon("phone")}<div><h3>Telefon</h3><a href="{TEL}">{PHONE}</a></div></div>
          <div class="contact-detail">{icon("pin")}<div><h3>Adres</h3><address>{ADDRESS}</address></div></div>
          <div class="contact-detail">{icon("mail")}<div><h3>E-mail</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
          <div class="contact-detail">{icon("clock")}<div><h3>Godziny otwarcia</h3>{hours()}</div></div>
          <div class="social-links">{profile_links()}</div>
        </div>
        <div class="contact-card">
          <h2>Napisz do nas</h2>
          <form class="contact-form" method="post"{form_action} data-mode="{form_mode}" data-email="{EMAIL}">
            <fieldset{" disabled" if not FORM_ENDPOINT else ""}>
              <label for="name">Imię</label><input id="name" name="name" autocomplete="given-name" required maxlength="80">
              <label for="reply">Numer telefonu lub e-mail</label>
              <input id="reply" name="reply" required maxlength="140" aria-describedby="reply-help">
              <small id="reply-help">Podaj jeden sposób kontaktu.</small>
              <label for="message">Treść wiadomości</label><textarea id="message" name="message" required maxlength="2000" rows="5"></textarea>
              <p class="form-help">{form_help} <a href="/polityka-prywatnosci.html">Polityka prywatności</a>.</p>
              <button class="button button-dark" type="submit">Wyślij</button>
            </fieldset>
            <p class="form-status" role="status"></p>
            <noscript><p>Możesz również skorzystać z telefonu lub bezpośredniego adresu e-mail.</p></noscript>
          </form>
        </div>
      </div>
      <section class="map-section" aria-labelledby="map-heading">
        <div class="section-head">
          <div><h2 id="map-heading">Dojazd</h2><p>{map_note}</p></div>
          <a class="button button-outline" href="{DIRECTIONS}" rel="external">{icon("pin")} Wyznacz trasę</a>
        </div>
        <div class="map-shell" data-map-src="{MAP_EMBED}">
          <div class="map-consent">
            <div class="card-icon">{icon("pin")}</div>
            <h3>Mapa Google</h3>
            <p>Po włączeniu mapy przeglądarka połączy się z usługą Google Maps, która może używać plików cookies.</p>
            <button type="button" class="button button-dark map-enable" hidden>Włącz mapę Google</button>
          </div>
          <div class="map-frame"></div>
          <button class="button button-outline map-disable" type="button" hidden>Wyłącz mapę</button>
        </div>
      </section>
    </div></section>
"""

if DEMO:
    privacy_details = f"""
      <h2>Formularz kontaktowy</h2>
      <p>Wersja demonstracyjna sprawdza pola formularza w przeglądarce. Wpisana treść nie jest wysyłana ani zapisywana przez stronę.</p>
      <h2>Hosting</h2>
      <p>Przy otwieraniu strony przeglądarka łączy się z serwerami Vercel. Dostawca hostingu może przetwarzać dane techniczne, takie jak adres IP i informacje o żądaniu, w celu dostarczania i zabezpieczenia usługi.</p>
      <p><a href="https://vercel.com/legal/privacy-policy" rel="external">Polityka prywatności Vercel</a></p>"""
else:
    provider = (
        f' Obsługę formularza zapewnia {escape(WORKSHOP["form_provider"])}.'
        if FORM_ENDPOINT else ""
    )
    retention = escape(WORKSHOP["retention"]) or "do czasu zakończenia sprawy lub upływu okresu potrzebnego do ochrony roszczeń"
    privacy_details = f"""
      <h2>Administrator danych</h2>
      <p>{escape(WORKSHOP["administrator"])}<br>{ADDRESS}<br>Kontakt e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <h2>Kontakt z warsztatem</h2>
      <p>Używamy podanego imienia, danych kontaktowych i treści wiadomości, aby odpowiedzieć na zapytanie. Gdy sprawa dotyczy usługi przed zawarciem umowy, podstawą jest art. 6 ust. 1 lit. b RODO. W pozostałych sprawach podstawą jest uzasadniony interes polegający na obsłudze zapytań (art. 6 ust. 1 lit. f RODO).</p>
      <p>Podanie danych jest dobrowolne i potrzebne, abyśmy mogli odpowiedzieć. Dane przechowujemy {retention}. W obsłudze korespondencji mogą uczestniczyć dostawcy hostingu i poczty.{provider}</p>
      <h2>Twoje prawa</h2>
      <p>Możesz poprosić o dostęp do danych, ich sprostowanie lub usunięcie oraz ograniczenie przetwarzania. W odpowiednich przypadkach możesz złożyć sprzeciw lub skorzystać z prawa do przenoszenia danych. Możesz też wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych.</p>"""

privacy = f"""
    {page_head("Polityka prywatności", "Polityka prywatności", "Informacje o formularzu, hostingu i mapie Google.")}
    <section class="section"><div class="container narrow prose">
      {privacy_details}
      <h2>Cookies i mapa Google</h2>
      <p>Witryna nie używa własnych plików cookies, reklam ani skryptów analitycznych. Po wybraniu „Włącz mapę Google” wczytujemy widżet Google Maps. Google otrzymuje wówczas dane techniczne, takie jak adres IP, i może korzystać z plików cookies. Mapę można w każdej chwili wyłączyć w zakładce Kontakt.</p>
      <p><a href="https://policies.google.com/privacy?hl=pl" rel="external">Polityka prywatności Google</a></p>
    </div></section>
"""

missing = """
    <section class="page-head error-page"><div class="container">
      <p class="eyebrow">Błąd 404</p><h1>Nie znaleziono strony</h1>
      <p>Sprawdź adres albo wróć na stronę główną warsztatu.</p>
      <a class="button button-white" href="/">Wróć na stronę główną</a>
    </div></section>
"""


def metadata(page, title, description):
    tags = [
        f"<title>{escape(title)}</title>",
        f'<meta name="description" content="{escape(description)}">',
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{escape(description)}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:locale" content="pl_PL">',
    ]
    if DEMO or page == "404.html":
        tags.append('<meta name="robots" content="noindex, follow">')
    if SITE_URL and page != "404.html":
        canonical = escape(f'{SITE_URL}/{"" if page == "index.html" else page}')
        tags.extend([
            f'<link rel="canonical" href="{canonical}">',
            f'<meta property="og:url" content="{canonical}">',
            f'<meta property="og:image" content="{escape(SITE_URL)}/assets/serwis-kola.webp">',
        ])
    return "\n  ".join(tags)


def write_page(page, title, description, content):
    document = f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#191919">
  {metadata(page, title, description)}
  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/site.js" defer></script>
</head>
<body>
  {navigation(page)}
  <main id="tresc" tabindex="-1">{content}</main>
  {footer()}
</body>
</html>
"""
    (OUTPUT / page).write_text(document, encoding="utf-8", newline="\n")


def write_sitemap():
    sitemap = OUTPUT / "sitemap.xml"
    hosts = ""
    if not DEMO:
        urls = "\n".join(
            f'<url><loc>{xml_escape(SITE_URL)}/{"" if path == "index.html" else path}</loc></url>'
            for path, _ in PAGES
        )
        sitemap.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
            encoding="utf-8",
        )
        hosts = f"\nSitemap: {SITE_URL}/sitemap.xml\n"
    else:
        sitemap.unlink(missing_ok=True)
    (OUTPUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n{hosts}", encoding="utf-8")


def build():
    name = WORKSHOP["name"]
    location = f'{WORKSHOP["city"]} {WORKSHOP["district"]}'
    pages = [
        ("index.html", f"{name} – Wulkanizacja i wymiana opon | {location}",
         f"Serwis opon {name}, {location}. Wymiana opon, wyważanie kół i wulkanizacja. Zobacz cennik i godziny otwarcia.", home),
        ("uslugi.html", f"Usługi wulkanizacyjne | {name} {location}",
         f"Wymiana opon i kół, wyważanie i naprawa przebić w serwisie {name} w lokalizacji {location}.", services),
        ("cennik.html", f"Cennik wymiany opon i wyważania | {name}",
         f"Cennik wulkanizacji {name}, {location}. Ceny wymiany opon na felgach stalowych i aluminiowych.", prices),
        ("o-nas.html", f"O warsztacie | {name} {location}",
         f"Poznaj serwis opon {name}. Zobacz, jak wygląda wymiana opon, wyważanie i naprawa w warsztacie.", about),
        ("galeria.html", f"Galeria warsztatu | {name}",
         f"Galeria {name}: stanowiska serwisowe, wyposażenie, samochody i montaż opon.", gallery),
        ("kontakt.html", f"Kontakt, godziny i dojazd | {name} {location}",
         f"Sprawdź telefon, e-mail, godziny oraz mapę dojazdu do serwisu opon {name}, {location}.", contact),
        ("polityka-prywatnosci.html", f"Polityka prywatności | {name}",
         "Informacje o danych w formularzu kontaktowym i osadzonej mapie Google.", privacy),
        ("404.html", f"Nie znaleziono strony | {name}",
         f"Wróć na stronę główną serwisu {name}.", missing),
    ]
    for page in pages:
        write_page(*page)
    write_sitemap()


if __name__ == "__main__":
    build()
