import puppeteer from 'puppeteer'; // Ensure you're using ES Modules if you're using `import`

import fs from 'fs/promises'; // Use the promise-based `fs` API
import path from 'path';

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename)

async function generateImages(folderPath) {
  const browser = await puppeteer.launch(); // Launch Puppeteer
  const page = await browser.newPage(); // Create a new page

  try {
    const files = await fs.readdir(folderPath); // Read folder contents

    for (const file of files) {
      const fullPath = path.join(folderPath, file);

      // Ensure the file is HTML before attempting to render it
      if (path.extname(file).toLowerCase() === '.html') {
        console.log(`Rendering ${fullPath}...`);
        await page.goto(`file://${__dirname}/${fullPath}`); // Load the file in the browser
        await page.setViewport({ width: 1080, height: 1024 });
        const outputPath = path.join(folderPath, `${path.basename(file, '.html')}.png`);
        await page.screenshot({ path: outputPath , fullPage: true});
        console.log(`Image saved at ${outputPath}`);
      }
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
  } finally {
    await browser.close(); // Close the browser
  }
}

const subfolderPath = 'generated_outputs'; // Path to your folder

(async () => {
  await generateImages(subfolderPath); // Call the async function
})();