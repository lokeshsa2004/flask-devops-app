/* StackForge Showcase – small client-side enhancements */

function setTheme(next) {
  document.documentElement.dataset.theme = next;
  localStorage.setItem("stackforge-theme", next);
}

function initTheme() {
  const saved = localStorage.getItem("stackforge-theme");
  const prefersLight = window.matchMedia?.("(prefers-color-scheme: light)")?.matches;
  const initial = saved || (prefersLight ? "light" : "dark");
  setTheme(initial);

  const btn = document.getElementById("theme-toggle");
  if (!btn) return;

  const sync = () => {
    const isLight = document.documentElement.dataset.theme === "light";
    btn.setAttribute("aria-pressed", String(isLight));
    btn.textContent = isLight ? "Dark mode" : "Light mode";
  };
  sync();

  btn.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    setTheme(next);
    sync();
  });
}

async function refreshHealth() {
  const pill = document.getElementById("health-pill");
  if (!pill) return;

  try {
    const res = await fetch("/api/health", { headers: { Accept: "application/json" } });
    const data = await res.json();
    if (res.ok && data.ok) {
      pill.textContent = "Database: OK";
      pill.className = "pill pill-ok";
      pill.title = JSON.stringify(data);
      return;
    }
    pill.textContent = "Database: issue";
    pill.className = "pill pill-bad";
    pill.title = JSON.stringify(data);
  } catch (e) {
    pill.textContent = "Database: offline";
    pill.className = "pill pill-bad";
    pill.title = String(e);
  }
}

function cardFromItem(item) {
  const el = document.createElement("article");
  el.className = "card";

  const media = document.createElement("div");
  media.className = "card-media";
  const img = document.createElement("img");
  img.src = item.image_url;
  img.alt = "";
  img.width = 320;
  img.height = 160;
  img.loading = "lazy";
  media.appendChild(img);

  const body = document.createElement("div");
  body.className = "card-body";

  if (item.badge) {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = item.badge;
    body.appendChild(chip);
  }

  const h3 = document.createElement("h3");
  h3.textContent = item.title;
  body.appendChild(h3);

  const p = document.createElement("p");
  p.textContent = item.summary;
  body.appendChild(p);

  el.appendChild(media);
  el.appendChild(body);
  return el;
}

async function refreshItems() {
  const grid = document.getElementById("js-grid");
  const raw = document.getElementById("api-raw");
  if (!grid) return;

  grid.innerHTML = "";
  const res = await fetch("/api/items", { headers: { Accept: "application/json" } });
  const data = await res.json();
  if (raw) {
    raw.hidden = false;
    raw.textContent = JSON.stringify(data, null, 2);
  }
  for (const item of data.items || []) {
    grid.appendChild(cardFromItem(item));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  refreshHealth();
  refreshItems().catch(() => {
    const pill = document.getElementById("health-pill");
    if (pill) pill.textContent = "API: error";
  });

  document.getElementById("refresh-api")?.addEventListener("click", () => {
    refreshItems().catch(() => {});
  });
});
