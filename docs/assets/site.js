const menuToggle = document.querySelector(".menu-toggle");
const menu = document.querySelector("#menu");
const mobileMenu = window.matchMedia("(max-width: 800px)");

function setMenu(open) {
  menu.classList.toggle("is-open", open);
  menuToggle.setAttribute("aria-expanded", String(open));
  menuToggle.setAttribute("aria-label", open ? "Zamknij menu" : "Otwórz menu");
}

function syncMenu() {
  menuToggle.hidden = !mobileMenu.matches;
  setMenu(false);
}

document.documentElement.classList.add("js");
syncMenu();
mobileMenu.addEventListener("change", syncMenu);

menuToggle.addEventListener("click", () => {
  setMenu(menuToggle.getAttribute("aria-expanded") !== "true");
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menu.classList.contains("is-open")) {
    setMenu(false);
    menuToggle.focus();
  }
});

menu.addEventListener("click", (event) => {
  if (event.target.closest("a")) setMenu(false);
});

const gallery = document.querySelector(".lightbox");
if (gallery && typeof gallery.showModal === "function") {
  const entries = [...document.querySelectorAll(".gallery-link")];
  const photo = gallery.querySelector(".lightbox-photo");
  const caption = gallery.querySelector("#photo-caption");
  let current = 0;
  let opener;

  function showPhoto(index) {
    current = (index + entries.length) % entries.length;
    const selected = entries[current];
    const image = selected.querySelector("img");
    photo.src = selected.href;
    photo.alt = image.alt;
    caption.textContent = selected.closest("figure").querySelector("figcaption").textContent;
  }

  entries.forEach((entry, index) => {
    entry.addEventListener("click", (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = entry;
      showPhoto(index);
      gallery.showModal();
    });
  });

  gallery.querySelector(".lightbox-close").addEventListener("click", () => gallery.close());
  gallery.querySelectorAll("[data-photo-step]").forEach((control) => {
    control.addEventListener("click", () => showPhoto(current + Number(control.dataset.photoStep)));
  });
  gallery.addEventListener("click", (event) => {
    if (event.target === gallery) gallery.close();
  });
  gallery.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      showPhoto(current + (event.key === "ArrowLeft" ? -1 : 1));
    }
  });
  gallery.addEventListener("close", () => opener?.focus());
}

const form = document.querySelector(".contact-form");
if (form) {
  const fields = form.querySelector("fieldset");
  const submit = form.querySelector('button[type="submit"]');
  const status = form.querySelector(".form-status");
  const replyField = form.elements.namedItem("reply");

  fields.disabled = false;
  form.addEventListener("input", (event) => {
    event.target.setCustomValidity?.("");
    status.textContent = "";
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);

    for (const field of ["name", "reply", "message"]) {
      const value = data.get(field).trim();
      if (!value) {
        const input = form.elements.namedItem(field);
        input.setCustomValidity("Uzupełnij to pole.");
        input.reportValidity();
        return;
      }
      data.set(field, value);
    }

    const reply = data.get("reply");
    const emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(reply);
    const phoneIsValid = /^\+?[\d\s().-]+$/.test(reply) && /^\+?\d{9,15}$/.test(reply.replace(/[\s().-]/g, ""));
    if (!emailIsValid && !phoneIsValid) {
      replyField.setCustomValidity("Podaj poprawny adres e-mail lub numer telefonu.");
      replyField.reportValidity();
      return;
    }

    if (form.dataset.mode === "demo") {
      status.textContent = "Formularz przeszedł sprawdzenie. W trybie demonstracyjnym wiadomość nie została wysłana.";
      form.reset();
      return;
    }

    if (form.dataset.mode === "email") {
      const subject = encodeURIComponent("Zapytanie do warsztatu Bieżnik24");
      const body = encodeURIComponent(
        "Imię: " + data.get("name") + "\r\nKontakt: " + reply + "\r\n\r\n" + data.get("message")
      );
      window.location.href = "mailto:" + form.dataset.email + "?subject=" + subject + "&body=" + body;
      status.textContent = "Dokończ wysyłkę w swojej aplikacji pocztowej.";
      return;
    }

    submit.disabled = true;
    status.textContent = "Wysyłanie wiadomości…";
    try {
      const result = await fetch(form.action, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
        signal: AbortSignal.timeout(15000),
      });
      if (!result.ok) throw new Error("Wysyłka nie powiodła się");
      form.reset();
      status.textContent = "Wiadomość została wysłana. Odpowiemy na podany kontakt.";
    } catch {
      status.textContent = "Nie udało się potwierdzić wysłania wiadomości. Możesz skontaktować się z nami telefonicznie lub e-mailem.";
    } finally {
      submit.disabled = false;
    }
  });
}

const map = document.querySelector(".map-shell");
if (map) {
  const notice = map.querySelector(".map-consent");
  const frameSlot = map.querySelector(".map-frame");
  const enable = map.querySelector(".map-enable");
  const disable = map.querySelector(".map-disable");
  enable.hidden = false;

  enable.addEventListener("click", () => {
    const iframe = document.createElement("iframe");
    iframe.title = "Interaktywna mapa dojazdu Google";
    iframe.referrerPolicy = "no-referrer-when-downgrade";
    iframe.src = map.dataset.mapSrc;
    iframe.allowFullscreen = true;
    frameSlot.replaceChildren(iframe);
    notice.hidden = true;
    disable.hidden = false;
    disable.focus({ preventScroll: true });
  });

  disable.addEventListener("click", () => {
    frameSlot.replaceChildren();
    notice.hidden = false;
    disable.hidden = true;
    enable.focus({ preventScroll: true });
  });
}
