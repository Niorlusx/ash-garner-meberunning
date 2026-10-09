export default async function handler(req, res) {
  // Only allow POST
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Secret check
  const expectedSecret = process.env.FEED_SECRET || process.env.GHL_WEBHOOK_SECRET;
  const providedSecret = req.headers['x-feed-secret'] || req.headers['x-ghl-secret'];

  if (!expectedSecret) {
    console.error('FEED_SECRET / GHL_WEBHOOK_SECRET is not set in Vercel env');
    return res.status(500).json({ error: 'Server misconfigured' });
  }

  if (!providedSecret || providedSecret !== expectedSecret) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;

    // Basic validation for the transaction shape you sent
    const {
      event,
      maskedAccount,
      amount,
      currency,
      merchant,
      date,
      reference
    } = body || {};

    console.log('[ghl-webhook]', {
      event,
      maskedAccount,
      amount,
      currency,
      merchant,
      date,
      reference,
      receivedAt: new Date().toISOString()
    });

    // TODO: persist, forward to Discord/Slack, update spreadsheet, etc.

    return res.status(200).json({
      ok: true,
      received: true,
      event: event || null,
      reference: reference || null
    });
  } catch (err) {
    console.error('[ghl-webhook] parse error', err);
    return res.status(400).json({ error: 'Invalid JSON body' });
  }
}
