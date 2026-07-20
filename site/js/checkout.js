/* ── MAISON — Checkout ──────────────────────────────────────────────────
   Renders the order summary from the Cart and a (demo, client-side) payment
   form. Placing an order clears the cart and shows a confirmation. No real
   payment is processed. Markup uses design-system.css classes only. */

function renderCheckout(selector) {
  const root = document.querySelector(selector);
  if (!root) return;

  const { lines, subtotal } = Cart.state();

  if (lines.length === 0) {
    root.innerHTML = `
      <section class="checkout-empty">
        <h1 class="section__title">Your bag is empty</h1>
        <p class="text-body-md">Add a piece to your bag before checking out.</p>
        <a class="btn btn-primary" href="collection.html">Browse the Collection</a>
      </section>`;
    return;
  }

  root.innerHTML = `
    <div class="checkout">
      <section class="checkout__form-col">
        <h1 class="checkout__title">Checkout</h1>
        <form class="checkout-form" id="checkout-form" novalidate>
          <fieldset class="checkout-form__group">
            <legend class="checkout-form__legend text-label-lg">Contact</legend>
            <label class="field"><span>Full name</span><input name="name" required autocomplete="name" /></label>
            <label class="field"><span>Email</span><input name="email" type="email" required autocomplete="email" /></label>
          </fieldset>

          <fieldset class="checkout-form__group">
            <legend class="checkout-form__legend text-label-lg">Shipping</legend>
            <label class="field"><span>Address</span><input name="address" required autocomplete="street-address" /></label>
            <div class="field-row">
              <label class="field"><span>City</span><input name="city" required autocomplete="address-level2" /></label>
              <label class="field"><span>Postal code</span><input name="zip" required autocomplete="postal-code" /></label>
            </div>
            <label class="field"><span>Country</span><input name="country" required autocomplete="country-name" value="United States" /></label>
          </fieldset>

          <fieldset class="checkout-form__group">
            <legend class="checkout-form__legend text-label-lg">Payment</legend>
            <label class="field"><span>Card number</span><input name="card" inputmode="numeric" placeholder="4242 4242 4242 4242" required /></label>
            <div class="field-row">
              <label class="field"><span>Expiry</span><input name="exp" placeholder="MM / YY" required /></label>
              <label class="field"><span>CVC</span><input name="cvc" inputmode="numeric" placeholder="123" required /></label>
            </div>
            <p class="checkout-form__disclaimer text-body-sm">Demo storefront — no real payment is processed.</p>
          </fieldset>

          <button class="btn btn-primary checkout-form__submit" type="submit">Place Order</button>
        </form>
      </section>

      <aside class="checkout__summary">
        <h2 class="checkout-summary__title text-label-lg">Order Summary</h2>
        <div class="checkout-summary__lines">
          ${lines
            .map(
              (l) => `
            <div class="checkout-summary__line">
              <div class="checkout-summary__media">
                <img src="${l.photos[0]}" alt="${l.brand} ${l.model}" loading="lazy" />
                <span class="checkout-summary__qty">${l.qty}</span>
              </div>
              <div class="checkout-summary__meta">
                <span class="checkout-summary__brand">${l.brand}</span>
                <span class="checkout-summary__name">${l.model}</span>
              </div>
              <span class="checkout-summary__price">${formatMoney(l.lineTotal, l.currency)}</span>
            </div>`
            )
            .join("")}
        </div>
        <dl class="checkout-summary__totals">
          <div><dt>Subtotal</dt><dd>${formatMoney(subtotal)}</dd></div>
          <div><dt>Shipping — insured</dt><dd>Complimentary</dd></div>
          <div class="checkout-summary__grand"><dt>Total</dt><dd>${formatMoney(subtotal)}</dd></div>
        </dl>
      </aside>
    </div>`;

  const form = root.querySelector("#checkout-form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form).entries());
    const order = {
      number: "MSN-" + Math.random().toString(36).slice(2, 8).toUpperCase(),
      email: data.email,
      total: subtotal,
    };
    Cart.clear();
    root.innerHTML = `
      <section class="order-confirm">
        <span class="order-confirm__mark">✓</span>
        <h1 class="section__title">Thank you</h1>
        <p class="text-body-md order-confirm__lede">Your order is confirmed.</p>
        <dl class="order-confirm__meta">
          <div><dt>Order</dt><dd>${order.number}</dd></div>
          <div><dt>Total</dt><dd>${formatMoney(order.total)}</dd></div>
          <div><dt>Confirmation sent to</dt><dd>${order.email}</dd></div>
        </dl>
        <p class="text-body-sm">A MAISON specialist will contact you to arrange insured delivery and authentication handover.</p>
        <a class="btn btn-primary" href="collection.html">Continue Shopping</a>
      </section>`;
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}
