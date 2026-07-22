# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: app.spec.js >> Saarthi AI E2E Suite >> App Tests >> Can send a message and receive response
- Location: tests\app.spec.js:33:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.message-bubble:not(.user-role), .message:not(.user)').first()
Expected: visible
Timeout: 15000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 15000ms
  - waiting for locator('.message-bubble:not(.user-role), .message:not(.user)').first()

```

```yaml
- complementary:
  - text: Saarthi AI Offline
  - button "New Chat"
  - textbox "Search conversations, messages, or documents..."
  - button "Conversations"
  - button "Messages"
  - button "Documents"
  - button "Welcome Thread"
  - button "Welcome Thread"
  - heading "Today" [level=4]
  - button "Welcome Thread":
    - text: Welcome Thread
    - button "Rename"
    - button "Delete"
  - button "Welcome Thread":
    - text: Welcome Thread
    - button "Rename"
    - button "Delete"
  - button "Documents Manager ▲"
  - text: No documents uploaded yet.
  - button "System ▼"
  - button "EN"
  - button "हिं"
  - button "Light Mode"
- main:
  - text: SAARTHI AI >
  - heading "Welcome Thread" [level=2]
  - button "Rename"
  - paragraph: Hello from Playwright!
  - button "Edit message"
  - button "Delete message"
  - paragraph: I could not find reliable information about this topic in my document library. You can upload a relevant document and ask me questions about it.
  - text: Not found
  - button "Listen to answer"
  - button "Copy Markdown"
  - button "Export to Markdown"
  - button "Helpful"
  - button "Not helpful"
  - text: ~34 tokens
  - button "Delete message"
  - button "Regenerate"
  - button "Add attachment"
  - textbox "Ask about your uploaded document, or ask about legal, banking & medical topics..."
  - button "Record voice input"
  - button [disabled]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Saarthi AI E2E Suite', () => {
  4  | 
  5  |   test('Page loads properly', async ({ page }) => {
  6  |     await page.goto('/');
  7  |     await expect(page).toHaveTitle(/Saarthi/);
  8  |     await expect(page.locator('text=Launch Saarthi').first()).toBeVisible();
  9  |   });
  10 | 
  11 |   test.describe('App Tests', () => {
  12 |     test.beforeEach(async ({ page }) => {
  13 |       await page.goto('/');
  14 |       // Wait for app to load by checking for the chat input or upload button
  15 |       await expect(page.getByRole('button', { name: /attach|upload|paperclip/i }).first()).toBeVisible({ timeout: 10000 });
  16 |     });
  17 | 
  18 |     test('Sidebar navigation works', async ({ page }) => {
  19 |       const featuresBtn = page.getByRole('button', { name: /features/i });
  20 |       if (await featuresBtn.isVisible()) {
  21 |         await featuresBtn.click();
  22 |         await expect(page.locator('text=OCR')).toBeVisible();
  23 |       }
  24 |     });
  25 | 
  26 |     test('Theme toggle works', async ({ page }) => {
  27 |       const themeBtn = page.getByRole('button', { name: /toggle theme|dark mode|light mode/i }).first();
  28 |       if (await themeBtn.isVisible()) {
  29 |         await themeBtn.click();
  30 |       }
  31 |     });
  32 | 
  33 |     test('Can send a message and receive response', async ({ page }) => {
  34 |       const chatInput = page.getByPlaceholder(/Ask about/i);
  35 |       await expect(chatInput).toBeVisible();
  36 |       
  37 |       await chatInput.fill('Hello from Playwright!');
  38 |       await chatInput.press('Enter');
  39 |       
  40 |       await expect(page.locator('text=Hello from Playwright!')).toBeVisible();
  41 |       
  42 |       const aiBubble = page.locator('.message-bubble:not(.user-role), .message:not(.user)').first();
> 43 |       await expect(aiBubble).toBeVisible({ timeout: 15000 });
     |                              ^ Error: expect(locator).toBeVisible() failed
  44 |     });
  45 |     
  46 |     test('Camera access (mocked) and Upload modal', async ({ page }) => {
  47 |       const attachBtn = page.getByRole('button', { name: /attach|upload|paperclip/i }).first();
  48 |       if (await attachBtn.isVisible()) {
  49 |         await attachBtn.click();
  50 |         await expect(page.getByText(/upload/i).first()).toBeVisible();
  51 |       }
  52 |     });
  53 |   });
  54 | 
  55 | });
  56 | 
```