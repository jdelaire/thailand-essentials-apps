const { test, expect } = require('@playwright/test');
const path = require('path');

test('home page renders core sections', async ({ page }) => {
  const fileUrl = 'file://' + path.resolve(__dirname, '../index.html');
  await page.goto(fileUrl);

  await expect(page).toHaveTitle(/Thailand Essential Apps/i);
  await expect(page.locator('h1')).toContainText('Live like a local faster');
  await expect(page.locator('section#transport')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Transport' })).toBeVisible();
});
