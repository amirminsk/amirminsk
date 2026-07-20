/* Renders collection/product pages from the shared WATCHES inventory
   (../assets/js/watches.js) into markup styled entirely by design-system.css
   classes, which in turn read tokens.css (generated from DESIGN.md). */

const money = (n, currency) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency, maximumFractionDigits: 0 }).format(n);

function watchCard(w) {
  const a = document.createElement("a");
  a.className = "card";
  a.href = `product.html?id=${w.id}`;
  a.innerHTML = `
    <div class="card__media"><img src="${w.photos[0]}" alt="${w.brand} ${w.model}" loading="lazy" /></div>
    <div class="card__body">
      <span class="card__eyebrow">${w.brand}</span>
      <h3 class="card__title">${w.model}</h3>
      <span class="card__meta">${w.ref} · ${w.year} · ${w.case_material}</span>
      ${w.status === "sold" ? `<span class="card__status">Sold</span>` : `<span class="card__price">${money(w.price, w.currency)}</span>`}
    </div>
  `;
  return a;
}

function renderCollection(targetSelector, { limit } = {}) {
  const target = document.querySelector(targetSelector);
  if (!target) return;
  const items = limit ? WATCHES.slice(0, limit) : WATCHES;
  target.append(...items.map(watchCard));
}

function renderProduct(targetSelector) {
  const target = document.querySelector(targetSelector);
  if (!target) return;
  const id = Number(new URLSearchParams(location.search).get("id"));
  const w = WATCHES.find((watch) => watch.id === id) ?? WATCHES[0];

  document.title = `${w.brand} ${w.model} — MAISON`;

  target.innerHTML = `
    <div>
      <div class="product__gallery-main">
        <img id="product-main-img" src="${w.photos[0]}" alt="${w.brand} ${w.model}" />
      </div>
      <div class="product__thumbs">
        ${w.photos
          .map(
            (src, i) =>
              `<img src="${src}" alt="" class="${i === 0 ? "is-active" : ""}" data-src="${src}" />`
          )
          .join("")}
      </div>
    </div>
    <div>
      <span class="product__eyebrow">${w.brand}</span>
      <h1 class="product__title">${w.model}</h1>
      <p class="product__price">${w.status === "sold" ? "Sold" : money(w.price, w.currency)}</p>
      <p class="product__desc">${w.description}</p>
      <table class="spec-table">
        <tbody>
          <tr><td>Reference</td><td>${w.ref}</td></tr>
          <tr><td>Year</td><td>${w.year}</td></tr>
          <tr><td>Case material</td><td>${w.case_material}</td></tr>
          <tr><td>Case size</td><td>${w.case_size}</td></tr>
          <tr><td>Dial</td><td>${w.dial}</td></tr>
          <tr><td>Movement</td><td>${w.movement}</td></tr>
          <tr><td>Condition</td><td>${w.condition}</td></tr>
          <tr><td>Box &amp; papers</td><td>${[w.box && "Box", w.papers && "Papers"].filter(Boolean).join(" · ") || "—"}</td></tr>
        </tbody>
      </table>
      <div class="product__actions">
        <button class="btn btn-primary" ${w.status === "sold" ? "disabled" : ""}>${w.status === "sold" ? "Sold" : "Inquire"}</button>
        <a class="btn btn-secondary" href="collection.html">Back to Collection</a>
      </div>
    </div>
  `;

  target.querySelectorAll(".product__thumbs img").forEach((thumb) => {
    thumb.addEventListener("click", () => {
      document.getElementById("product-main-img").src = thumb.dataset.src;
      target.querySelectorAll(".product__thumbs img").forEach((t) => t.classList.remove("is-active"));
      thumb.classList.add("is-active");
    });
  });
}
