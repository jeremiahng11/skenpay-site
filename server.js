const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const FRONTEND = path.join(__dirname, 'frontend');

// Clean URL routes — serve .html files without the extension
app.get('/', (req, res) => {
  res.sendFile(path.join(FRONTEND, 'index.html'));
});

app.get('/home', (req, res) => {
  res.sendFile(path.join(FRONTEND, 'index.html'));
});

app.get('/signup', (req, res) => {
  res.sendFile(path.join(FRONTEND, 'signup.html'));
});

// Serve static assets (CSS, JS, images, etc.)
app.use(express.static(FRONTEND));

// Catch-all fallback — return index.html for any unmatched route (SPA-style)
app.get('*', (req, res) => {
  res.sendFile(path.join(FRONTEND, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`SkenPay site running on port ${PORT}`);
});
