// usage: node render_pdf.js in.html out.pdf   -> prints page count
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage();
  await pg.goto('file://' + path.resolve(inp));
  await pg.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
  const buf = fs.readFileSync(out).toString('latin1');
  console.log(out, 'pages:', (buf.match(/\/Type\s*\/Page[^s]/g) || []).length);
})();
