/* ── MAISON — Cart ──────────────────────────────────────────────────────
   A tiny client-side shopping cart persisted to localStorage. It joins the
   stored {id, qty} lines against the shared WATCHES inventory
   (../assets/js/watches.js) and self-mounts a cart button into the nav plus
   a slide-out drawer — so every page becomes shoppable without editing its
   markup. All rendered chrome uses the .btn/.icon-btn/etc. classes from
   design-system.css, which read tokens generated from DESIGN.md. */

const Cart = (() => {
  const KEY = "maison.cart.v1";
  const subs = [];
  let lines = read();

  function read() {
    try {
      const parsed = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(parsed) ? parsed.filter((l) => l && l.id) : [];
    } catch {
      return [];
    }
  }

  function write() {
    localStorage.setItem(KEY, JSON.stringify(lines));
    emit();
  }

  const inventory = (id) =>
    (typeof WATCHES !== "undefined" ? WATCHES : []).find((w) => w.id === id);

  function detailed() {
    return lines
      .map((l) => {
        const w = inventory(l.id);
        return w ? { ...w, qty: l.qty, lineTotal: w.price * l.qty } : null;
      })
      .filter(Boolean);
  }

  const count = () => lines.reduce((n, l) => n + l.qty, 0);
  const subtotal = () => detailed().reduce((n, l) => n + l.lineTotal, 0);

  function state() {
    return { lines: detailed(), count: count(), subtotal: subtotal() };
  }

  function emit() {
    subs.forEach((fn) => fn(state()));
  }

  function add(id, qty = 1) {
    const w = inventory(id);
    if (!w || w.status === "sold") return false;
    const existing = lines.find((l) => l.id === id);
    if (existing) existing.qty += qty;
    else lines.push({ id, qty });
    write();
    return true;
  }

  function setQty(id, qty) {
    qty = Math.max(0, Math.floor(qty));
    if (qty === 0) return remove(id);
    const line = lines.find((l) => l.id === id);
    if (line) {
      line.qty = qty;
      write();
    }
  }

  function remove(id) {
    lines = lines.filter((l) => l.id !== id);
    write();
  }

  function clear() {
    lines = [];
    write();
  }

  function onChange(fn) {
    subs.push(fn);
    fn(state());
    return fn;
  }

  return { add, setQty, remove, clear, onChange, state, count, subtotal };
})();

const formatMoney = (n, currency = "USD") =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(n);

/* ── UI: nav button + drawer, mounted on every page ─────────────────────── */

function mountCartUI() {
  const nav = document.querySelector(".site-nav");
  if (nav && !nav.querySelector(".cart-btn")) {
    const btn = document.createElement("button");
    btn.className = "cart-btn icon-btn";
    btn.type = "button";
    btn.setAttribute("aria-label", "Open cart");
    btn.innerHTML = `<span aria-hidden="true">BAG</span><span class="cart-btn__count" hidden>0</span>`;
    btn.addEventListener("click", openDrawer);
    nav.appendChild(btn);
  }

  if (!document.querySelector(".cart-drawer")) {
    const wrap = document.createElement("div");
    wrap.innerHTML = `
      <div class="cart-scrim" hidden></div>
      <aside class="cart-drawer" aria-label="Shopping cart" aria-hidden="true">
        <header class="cart-drawer__head">
          <h2 class="cart-drawer__title">Your Bag</h2>
          <button class="icon-btn cart-drawer__close" type="button" aria-label="Close cart">✕</button>
        </header>
        <div class="cart-drawer__body"></div>
        <footer class="cart-drawer__foot" hidden>
          <div class="cart-drawer__subtotal">
            <span class="text-label-lg">Subtotal</span>
            <span class="cart-drawer__subtotal-val"></span>
          </div>
          <p class="cart-drawer__note text-body-sm">Shipping &amp; duties calculated at checkout.</p>
          <a class="btn btn-primary cart-drawer__checkout" href="checkout.html">Checkout</a>
          <button class="btn btn-secondary cart-drawer__continue" type="button">Continue Shopping</button>
        </footer>
      </aside>
      <div class="cart-toast" role="status" aria-live="polite" hidden></div>`;
    document.body.appendChild(wrap);

    wrap.querySelector(".cart-scrim").addEventListener("click", closeDrawer);
    wrap.querySelector(".cart-drawer__close").addEventListener("click", closeDrawer);
    wrap.querySelector(".cart-drawer__continue").addEventListener("click", closeDrawer);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeDrawer();
    });
  }

  // Keep nav badge + drawer contents in sync with cart state.
  Cart.onChange(renderCartUI);
}

function renderCartUI({ lines, count, subtotal }) {
  const badge = document.querySelector(".cart-btn__count");
  if (badge) {
    badge.textContent = count;
    badge.hidden = count === 0;
  }

  const body = document.querySelector(".cart-drawer__body");
  const foot = document.querySelector(".cart-drawer__foot");
  if (!body) return;

  if (lines.length === 0) {
    body.innerHTML = `
      <div class="cart-empty">
        <p class="cart-empty__title">Your bag is empty</p>
        <p class="text-body-sm">Every piece is authenticated and sold with full provenance.</p>
        <a class="btn btn-secondary" href="collection.html">Browse the Collection</a>
      </div>`;
    if (foot) foot.hidden = true;
    return;
  }

  body.innerHTML = lines
    .map(
      (l) => `
      <div class="cart-line" data-line="${l.id}">
        <a class="cart-line__media" href="product.html?id=${l.id}">
          <img src="${l.photos[0]}" alt="${l.brand} ${l.model}" loading="lazy" />
        </a>
        <div class="cart-line__info">
          <span class="cart-line__brand">${l.brand}</span>
          <a class="cart-line__title" href="product.html?id=${l.id}">${l.model}</a>
          <span class="cart-line__price">${formatMoney(l.price, l.currency)}</span>
          <div class="cart-line__controls">
            <div class="qty-stepper" aria-label="Quantity">
              <button class="qty-stepper__btn" data-dec="${l.id}" aria-label="Decrease quantity">−</button>
              <span class="qty-stepper__val">${l.qty}</span>
              <button class="qty-stepper__btn" data-inc="${l.id}" aria-label="Increase quantity">+</button>
            </div>
            <button class="cart-line__remove" data-remove="${l.id}">Remove</button>
          </div>
        </div>
      </div>`
    )
    .join("");

  if (foot) {
    foot.hidden = false;
    foot.querySelector(".cart-drawer__subtotal-val").textContent = formatMoney(subtotal);
  }
}

function openDrawer() {
  document.querySelector(".cart-drawer")?.classList.add("is-open");
  document.querySelector(".cart-drawer")?.setAttribute("aria-hidden", "false");
  const scrim = document.querySelector(".cart-scrim");
  if (scrim) scrim.hidden = false;
  requestAnimationFrame(() => scrim?.classList.add("is-open"));
  document.body.style.overflow = "hidden";
}

function closeDrawer() {
  document.querySelector(".cart-drawer")?.classList.remove("is-open");
  document.querySelector(".cart-drawer")?.setAttribute("aria-hidden", "true");
  const scrim = document.querySelector(".cart-scrim");
  scrim?.classList.remove("is-open");
  if (scrim) setTimeout(() => (scrim.hidden = true), 300);
  document.body.style.overflow = "";
}

let toastTimer;
function cartToast(message) {
  const el = document.querySelector(".cart-toast");
  if (!el) return;
  el.textContent = message;
  el.hidden = false;
  requestAnimationFrame(() => el.classList.add("is-show"));
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    el.classList.remove("is-show");
    setTimeout(() => (el.hidden = true), 300);
  }, 1800);
}

/* Global delegation: any [data-add] button (product cards) adds to the cart.
   Quantity-aware adds on the product page are handled in app.js. */
document.addEventListener("click", (e) => {
  const addBtn = e.target.closest("[data-add]");
  if (addBtn && !addBtn.disabled) {
    const id = Number(addBtn.dataset.add);
    if (Cart.add(id)) cartToast("Added to your bag");
    return;
  }
  const inc = e.target.closest("[data-inc]");
  if (inc) return Cart.setQty(Number(inc.dataset.inc), lineQty(inc.dataset.inc) + 1);
  const dec = e.target.closest("[data-dec]");
  if (dec) return Cart.setQty(Number(dec.dataset.dec), lineQty(dec.dataset.dec) - 1);
  const rm = e.target.closest("[data-remove]");
  if (rm) return Cart.remove(Number(rm.dataset.remove));
});

function lineQty(id) {
  return Cart.state().lines.find((l) => l.id === Number(id))?.qty ?? 0;
}

document.addEventListener("DOMContentLoaded", mountCartUI);
