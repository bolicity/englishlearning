const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function verify() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  const context = await browser.newContext({ viewport: { width: 1400, height: 950 } });
  const page = await context.newPage();

  const resultsDir = path.join(__dirname, '../test-results');
  if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
  }

  console.log('--- 1. Testing Branch 1 (rulinwaishi-p1-V1.html) ---');
  const p1Path = 'file://' + path.join(__dirname, '../chinese/rulinwaishi-p1-V1.html');
  await page.goto(p1Path, { waitUntil: 'load' });
  await page.waitForSelector('img[alt="儒林外史核心考点第一页"]');
  await page.screenshot({ path: path.join(resultsDir, 'branch1_p1.png') });
  console.log('✓ Branch 1 loaded successfully and screenshot saved.');

  // Test Lightbox in Branch 1
  await page.click('.img-box');
  await page.waitForSelector('.lightbox-modal.active');
  await page.screenshot({ path: path.join(resultsDir, 'branch1_lightbox.png') });
  await page.click('.lightbox-close');
  console.log('✓ Branch 1 lightbox verified.');

  console.log('--- 2. Testing Branch 2 (rulinwaishi-p2-V1.html) ---');
  const p2Path = 'file://' + path.join(__dirname, '../chinese/rulinwaishi-p2-V1.html');
  await page.goto(p2Path, { waitUntil: 'load' });
  await page.waitForSelector('img[alt="儒林外史核心考点第二页"]');
  await page.screenshot({ path: path.join(resultsDir, 'branch2_p2.png') });
  console.log('✓ Branch 2 loaded successfully.');

  console.log('--- 3. Testing Branch 3 (rulinwaishi-p3-V1.html) ---');
  const p3Path = 'file://' + path.join(__dirname, '../chinese/rulinwaishi-p3-V1.html');
  await page.goto(p3Path, { waitUntil: 'load' });
  await page.waitForSelector('img[alt="儒林外史核心考点第三页"]');
  await page.screenshot({ path: path.join(resultsDir, 'branch3_p3.png') });
  console.log('✓ Branch 3 loaded successfully.');

  console.log('--- 4. Testing Branch 4 (rulinwaishi-p4-V1.html) ---');
  const p4Path = 'file://' + path.join(__dirname, '../chinese/rulinwaishi-p4-V1.html');
  await page.goto(p4Path, { waitUntil: 'load' });
  await page.waitForSelector('#matrixTable');
  await page.click('button:has-text("一、正统典范 (5人)")');
  await page.screenshot({ path: path.join(resultsDir, 'branch4_p4_filtered.png') });
  console.log('✓ Branch 4 matrix and filter tabs verified.');

  console.log('--- 5. Testing Character Cards Panorama (rulinwaishi-cards-V1.html) ---');
  const cardsPath = 'file://' + path.join(__dirname, '../chinese/rulinwaishi-cards-V1.html');
  await page.goto(cardsPath, { waitUntil: 'load' });
  await page.waitForSelector('.pair-card-box');
  await page.screenshot({ path: path.join(resultsDir, 'cards_panorama_pair.png') });
  
  // Switch to 9 cards single view
  await page.click('button:has-text("九大人物独立切图图鉴")');
  await page.waitForSelector('.single-card');
  await page.screenshot({ path: path.join(resultsDir, 'cards_panorama_single9.png') });
  console.log('✓ Character cards panorama (pair & single 9 cards) verified.');

  console.log('--- 6. Testing Branches Navigation Hub (rulinwaishi-nav-V1.html) ---');
  const navPath = 'file://' + path.join(__dirname, '../chinese/rulinwaishi-nav-V1.html');
  await page.goto(navPath, { waitUntil: 'load' });
  await page.waitForSelector('.branch-card');
  await page.screenshot({ path: path.join(resultsDir, 'rulinwaishi_nav_hub.png') });
  console.log('✓ Navigation hub loaded successfully.');

  console.log('--- 7. Testing Chinese Home Entrance (chinese.html) ---');
  const chinesePath = 'file://' + path.join(__dirname, '../chinese/chinese.html');
  await page.goto(chinesePath, { waitUntil: 'load' });
  await page.waitForSelector('#card-rulinwaishi-nav');
  await page.screenshot({ path: path.join(resultsDir, 'chinese_entrance.png') });
  console.log('✓ Chinese home entrance verified.');

  await browser.close();
  console.log('🎉 ALL PLAYWRIGHT TESTS PASSED SUCCESSFULLY!');
}

verify().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
