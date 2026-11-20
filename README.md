# Bieżnik24

Polskojęzyczna strona demonstracyjna serwisu opon. Gotowe pliki statyczne znajdują się w katalogu **docs/**. Vercel publikuje ten katalog bez instalacji zależności.

## Podgląd lokalny

W katalogu projektu uruchom:

~~~sh
python -m http.server 8080 --directory docs
~~~

Otwórz **http://localhost:8080**. Plik **docs/404.html** zawiera wygląd strony błędu. Vercel zwraca go z kodem 404 dla nieznanych adresów.

## Konfiguracja warsztatu

Dane i stawki znajdują się w **workshop.json**. Tryb demonstracyjny zawiera przykładowe dane kontaktowe, lokalizację na warszawskiej Woli oraz orientacyjny cennik. Formularz sprawdza dane lokalnie. Profil Google i odnośniki społecznościowe pojawiają się po wpisaniu prawdziwych adresów w konfiguracji.

Przed przełączeniem na tryb produkcyjny uzupełnij:

- Dane kontaktowe, pełny adres, godziny, cennik, historię i doświadczenie. Wpisz własne zapytanie w **map_query** lub pozostaw je puste, aby użyć pełnego adresu warsztatu. W **map_embed_url** możesz podać adres z funkcji „Umieść mapę” w Google Maps.
- Adres HTTPS witryny w **site_url** oraz adresy wizytówki Google i profili firmowych. Dane SEO i mapa witryny są generowane przy zmianie konfiguracji.
- Dane administratora, zasady i okres przechowywania danych oraz dostawcę obsługi formularza, jeśli z takiego korzystasz. Zaktualizuj treść polityki, jeżeli Twój sposób przetwarzania danych wymaga dodatkowych informacji.
- **form_endpoint** przy wysyłce przez usługę formularzy. Endpoint powinien przyjmować żądania POST z danymi formularza (**name**, **reply**, **message**), zwracać status 2xx po przyjęciu wiadomości i zezwalać domenie witryny na odczyt odpowiedzi przez CORS. Skonfiguruj ograniczenia antyspamowe u dostawcy. Puste pole otwiera wiadomość w aplikacji pocztowej w trybie produkcyjnym.

Po wyłączeniu **demo** i zmianie danych zbuduj HTML przy pomocy Pythona 3.12 lub nowszego:

~~~sh
python build.py
~~~

Zapisz w Git zmienioną konfigurację oraz wygenerowane strony. Przy włączonej integracji Vercel z GitHub kolejne zmiany na **main** uruchamiają wdrożenie.

## Zdjęcia stockowe

Zdjęcia pokazują przykładowe stanowiska i prace serwisowe. Zapisano je lokalnie w formacie WebP, w dwóch rozmiarach. Źródła objęte są [licencją Pexels](https://www.pexels.com/license/).

- [Mechanik wymieniający koło](https://www.pexels.com/photo/mechanic-changing-car-wheel-17600886/)
- [Samochody w warsztacie](https://www.pexels.com/photo/cars-in-car-repair-shop-4756887/)
- [Obsługa montażownicy](https://www.pexels.com/photo/person-holding-a-tire-5260115/)
- [Samochód na podnośniku](https://www.pexels.com/photo/car-on-a-lifter-inside-a-garage-8985514/)
- [Opony w warsztacie](https://www.pexels.com/photo/stack-of-car-tires-in-an-automotive-garage-34357287/)
