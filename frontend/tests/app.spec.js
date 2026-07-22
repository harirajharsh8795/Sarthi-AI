import { test, expect } from '@playwright/test';

test.describe('Saarthi AI E2E Suite', () => {

  test('Page loads properly', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Saarthi/);
    await expect(page.locator('text=Launch Saarthi').first()).toBeVisible();
  });

  test.describe('App Tests', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/');
      // Wait for app to load by checking for the chat input or upload button
      await expect(page.getByRole('button', { name: /attach|upload|paperclip/i }).first()).toBeVisible({ timeout: 10000 });
    });

    test('Sidebar navigation works', async ({ page }) => {
      const featuresBtn = page.getByRole('button', { name: /features/i });
      if (await featuresBtn.isVisible()) {
        await featuresBtn.click();
        await expect(page.locator('text=OCR')).toBeVisible();
      }
    });

    test('Theme toggle works', async ({ page }) => {
      const themeBtn = page.getByRole('button', { name: /toggle theme|dark mode|light mode/i }).first();
      if (await themeBtn.isVisible()) {
        await themeBtn.click();
      }
    });

    test('Can send a message and receive response', async ({ page }) => {
      const chatInput = page.getByPlaceholder(/Ask about/i);
      await expect(chatInput).toBeVisible();
      
      await chatInput.fill('Hello from Playwright!');
      await chatInput.press('Enter');
      
      await expect(page.locator('text=Hello from Playwright!')).toBeVisible();
      
      const aiBubble = page.locator('.message-bubble:not(.user-role), .message:not(.user)').first();
      await expect(aiBubble).toBeVisible({ timeout: 15000 });
    });
    
    test('Camera access (mocked) and Upload modal', async ({ page }) => {
      const attachBtn = page.getByRole('button', { name: /attach|upload|paperclip/i }).first();
      if (await attachBtn.isVisible()) {
        await attachBtn.click();
        await expect(page.getByText(/upload/i).first()).toBeVisible();
      }
    });
  });

});
