# Stripe setup — Ash Garner / Meberunning

Create three recurring monthly AUD products in Stripe: Runner $9, 3630 $19, and Label $49. Create Payment Links, collect email, and redirect success to the deployed landing page with `#thanks`.

Paste the resulting `https://buy.stripe.com/...` URLs into `js/config.js` under `stripePaymentLinks.runner`, `tier3630`, and `label`, then redeploy.

Test with Stripe test mode first, verify AUD pricing, and switch to live links only after checkout and redirect work.