---
id: upi-knowledge-base-001
title: "Unified Payments Interface (UPI): Complete Banking Guide"
domain: banking
category: payments
subcategory: digital-payments
topic: upi
version: 1.0
language: multilingual
difficulty: beginner/intermediate
keywords: [UPI, Unified Payments Interface, NPCI, Digital Payments, BHIM, PhonePe, Google Pay, Paytm, UPI PIN, VPA, UPI AutoPay, e-RUPI, UPI Lite, UPI 123Pay]
aliases: [UPI Payment, BHIM UPI, UPI Transfer, Digital Payment UPI]
related_topics: [banking/payments/imps.md, banking/payments/neft.md, banking/payments/rtgs.md, banking/mobile_banking/overview.md]
intent: [understand UPI, how to use UPI, UPI safety, UPI limit, UPI charges, resolve UPI pending, reset UPI PIN]
last_updated: 2026-07-19
author: Saarthi AI
sources: [NPCI Official Documentation, RBI Guidelines on Digital Payments]
---

# Unified Payments Interface (UPI): Complete Banking Guide

## Overview
**English:** The Unified Payments Interface (UPI) is a real-time instant payment system developed by the National Payments Corporation of India (NPCI) facilitating inter-bank peer-to-peer (P2P) and person-to-merchant (P2M) transactions. It consolidates multiple banking services, seamless fund routing, and merchant payments into a single mobile application, operating 24x7x365. With UPI, users can link multiple bank accounts to a single smartphone app and make instant transfers without needing to enter complex bank details like IFSC codes or account numbers every time, instead relying on a Virtual Payment Address (VPA) or UPI ID.

**Hindi Unicode:** यूनिफाइड पेमेंट्स इंटरफेस (UPI) नेशनल पेमेंट्स कॉरपोरेशन ऑफ इंडिया (NPCI) द्वारा विकसित एक रीयल-टाइम इंस्टेंट पेमेंट सिस्टम है जो अंतर-बैंक पीयर-टू-पीयर (P2P) और पर्सन-टू-मर्चेंट (P2M) लेनदेन की सुविधा प्रदान करता है। यह एक ही मोबाइल एप्लिकेशन में कई बैंकिंग सेवाओं, फंड रूटिंग और मर्चेंट भुगतानों को समेकित करता है, जो 24x7x365 संचालित होता है। UPI के साथ, उपयोगकर्ता कई बैंक खातों को एक ही स्मार्टफोन ऐप से जोड़ सकते हैं और हर बार IFSC कोड या खाता संख्या जैसे जटिल बैंक विवरण दर्ज किए बिना त्वरित स्थानान्तरण कर सकते हैं, इसके बजाय वर्चुअल पेमेंट एड्रेस (VPA) या UPI ID पर निर्भर रह सकते हैं।

**Hinglish:** Unified Payments Interface (UPI) ek real-time instant payment system hai jise National Payments Corporation of India (NPCI) ne banaya hai. Yeh inter-bank P2P aur P2M transactions ko aasan banata hai. Iske through aap ek hi mobile app mein apne multiple bank accounts link kar sakte hain aur bina IFSC code ya account number enter kiye, sirf ek Virtual Payment Address (VPA) ya UPI ID ka use karke 24x7 fund transfer kar sakte hain. Yeh digital payments ke liye India ka sabse popular aur reliable method ban chuka hai.

## Quick Summary
UPI is a revolutionary digital payment architecture that simplifies bank-to-bank money transfers. By leveraging two-factor authentication (device binding and UPI PIN) and the Immediate Payment Service (IMPS) infrastructure, it allows users to push and pull funds instantly using a simple UPI ID (e.g., name@bankname), mobile number, or QR code. It eliminates the need for maintaining mobile wallets by debiting and crediting funds directly from and to the user's primary bank account.

## Definition
The **Unified Payments Interface (UPI)** is a standardized API architecture and a set of standard specifications engineered by the NPCI to facilitate the seamless integration of various payment service providers (PSPs), banks, and third-party application providers (TPAPs) to execute instant real-time financial and non-financial transactions. It abstracts the underlying complexities of banking channels and presents a unified, user-friendly interface for the end consumer.

## Why It Matters
UPI has fundamentally transformed the Indian economic landscape by democratizing digital payments. It matters immensely because it reduces the dependency on physical cash, thereby increasing transparency and accountability in the financial ecosystem. It enables micro-transactions (as low as ₹1) without any prohibitive transaction costs, which empowers small merchants, street vendors, and individuals. By integrating directly with bank accounts, it ensures that users continue to earn interest on their balances until the exact moment a transaction occurs, unlike prepaid wallets where funds are locked. Furthermore, it drives financial inclusion and digital literacy at the grassroots level.

## How It Works

```text
+-------------------+       +-------------------+       +-------------------+
|   Payer (User)    | ----> |   PSP App (TPAP)  | ----> |  Payer's Bank     |
| (Enters UPI PIN)  |       | (GPay, PhonePe)   |       | (Debits Account)  |
+-------------------+       +-------------------+       +-------------------+
                                      |                           |
                                      v                           v
                            +-------------------------------------------+
                            |     National Payments Corp. (NPCI)        |
                            |       (Central Routing Engine)            |
                            +-------------------------------------------+
                                      |                           |
                                      v                           v
+-------------------+       +-------------------+       +-------------------+
| Beneficiary(Payee)| <---- |  Payee's PSP App  | <---- | Beneficiary Bank  |
| (Receives Funds)  |       |  (Notification)   |       | (Credits Account) |
+-------------------+       +-------------------+       +-------------------+
```
1. **Initiation:** The Payer opens a UPI-enabled app and enters the Payee's UPI ID or scans a QR code.
2. **Authentication:** The Payer enters the transaction amount and authenticates the payment using their secure 4 or 6-digit UPI PIN.
3. **Routing:** The Third-Party App Provider (TPAP) sends the request to the NPCI switch.
4. **Validation:** NPCI routes the request to the Payer's bank to verify the PIN and check for sufficient balance.
5. **Execution:** If valid, the Payer's bank debits the amount and sends a success response to NPCI.
6. **Settlement:** NPCI then instructs the Beneficiary's bank to credit the specified amount. Both parties receive an instant SMS notification from their respective banks.

## Eligibility
To use UPI services, individuals must meet the following detailed criteria:
- **Active Bank Account:** The user must have a savings or current account with a UPI-member bank.
- **Registered Mobile Number:** The mobile number used in the smartphone must be exactly the same as the one registered with the bank account for SMS alerts.
- **Valid Debit Card:** A valid, active debit card linked to the bank account is required for the initial setup to generate the UPI PIN (though newer updates allow Aadhaar-based OTP verification in certain banks).
- **Smartphone & Internet:** A compatible smartphone (Android or iOS) with an active internet connection (Mobile Data or Wi-Fi). Feature phone users can use *99# (USSD) or UPI 123Pay.
- **Age Requirement:** Typically, users must be 18 years or older to independently operate a full KYC bank account with debit card privileges, though minors above 10 can use UPI with restricted accounts under guardian supervision depending on bank policies.

## Required Documents
- **Not Applicable** in the traditional sense of submitting physical forms.
- **Functional Requirements:** 
  1. Bank Account Number.
  2. Debit Card Details (Last 6 digits and Expiry Date) for PIN setup.
  3. Linked Mobile Number SIM present in the device (for device binding SMS validation).
  4. Aadhaar Card (Optional, for Aadhaar-based UPI PIN setup if the bank supports it).

## Features & Benefits
- **Instant Real-Time Transfers:** UPI operates 24x7x365, including weekends and public holidays. Funds are transferred and settled instantly in the beneficiary's bank account, unlike NEFT which operates in batches. This ensures immediate liquidity for merchants and individuals alike.
- **Single App, Multiple Accounts:** Users do not need to download separate apps for different bank accounts. A single TPAP (like BHIM, PhonePe, or Google Pay) can link accounts from SBI, HDFC, ICICI, etc., providing a consolidated financial dashboard.
- **Virtual Payment Address (VPA):** UPI eliminates the risk of sharing sensitive banking information. Instead of sharing an account number and IFSC, users share a VPA (e.g., rahul@sbi), keeping their underlying banking details completely private and secure.
- **Two-Factor Authentication (2FA):** Every transaction requires device binding (the physical phone with the registered SIM) and a confidential UPI PIN known only to the user. This robust security framework significantly reduces the chances of unauthorized transactions.
- **Collect Requests (Pull Feature):** Unlike traditional payment systems that only allow 'pushing' money, UPI allows users to send 'collect requests' to others. The payer simply receives a notification, reviews the request, and approves it by entering their UPI PIN.

## Risks
- **Financial Risks:** Exposing your UPI PIN to fraudsters can lead to unauthorized debits and complete drainage of bank balances. Fraudsters often disguise themselves as bank officials or customer support executives to trick users into entering their PIN for a "refund" or "lottery win."
- **Technical Risks:** Network congestion at the NPCI switch or core banking server downtime can lead to "pending" transactions. In such cases, the amount may be debited from the sender but not credited to the receiver, causing temporary financial distress until the automatic reconciliation process reverses the transaction (usually within T+1 to T+3 days).
- **Legal & Compliance Risks:** Using UPI for illegal activities, such as unregulated betting, gambling, or money laundering, can result in immediate freezing of the linked bank accounts and legal action under the Prevention of Money Laundering Act (PMLA) and RBI regulations.
- **Cyber Risks:** Screen-sharing applications (like AnyDesk or TeamViewer), malicious links distributed via SMS (smishing), and fake QR codes pasted over legitimate merchant codes can compromise the user's mobile device, leading to account takeovers and financial loss.

## Charges & Fees
- **For Customers (P2P):** Currently, standard peer-to-peer (P2P) transfers and peer-to-merchant (P2M) payments are completely **free of cost** for everyday retail customers as per government mandates to promote digital transactions.
- **PPI Interoperability Charges:** Transactions made using Prepaid Payment Instruments (PPIs like wallets) on the UPI network above ₹2000 may incur an interchange fee of up to 1.1%, but this fee is borne by the merchant, not the retail customer.
- **Merchant Discount Rate (MDR):** The government has mandated a zero MDR policy on UPI transactions for RuPay debit cards and standard UPI to encourage adoption among small businesses.
- **Bank Specific Charges:** Some banks reserve the right to charge for transactions exceeding a certain monthly limit (e.g., beyond 20 P2P transactions per month), though most major public and private banks currently do not levy such fees.
- **Pre-payment Penalty & Taxes:** Not applicable for standard UPI transactions.

## RBI / Government Rules
- **Transaction Limits:** The RBI and NPCI have capped standard UPI transactions at ₹1 Lakh per transaction and per day. For specific categories like Capital Markets, Collections, Insurance, and Foreign Inward Remittances, the limit is extended up to ₹2 Lakh. For IPO subscriptions and Retail Direct Schemes, the limit is ₹5 Lakh.
- **Zero Liability Protection:** As per RBI guidelines on unauthorized electronic banking transactions, if a customer reports a fraudulent UPI transaction within 3 working days, they have zero liability, and the bank must credit the amount back within 10 working days.
- **Cooling Period:** To prevent frauds, a cooling period of 24 hours is enforced when a user changes their device or registers for UPI for the first time, restricting transaction limits to a maximum of ₹5,000 during this window.
- **Dispute Resolution Mechanism:** NPCI mandates that all UPI apps must have an in-app Online Dispute Resolution (ODR) system to allow users to raise complaints regarding failed or pending transactions directly within the application.

## Step-by-Step Process
**Setting Up UPI for the First Time:**
1. Download a certified UPI application (BHIM, Google Pay, PhonePe, Paytm, etc.) from the official Google Play Store or Apple App Store.
2. Open the app and grant the necessary permissions (SMS, Phone) to allow device binding.
3. Select the mobile number that is linked to your bank account to send a background verification SMS.
4. Once verified, select your bank from the list of UPI-enabled banks. The app will fetch your account details automatically.
5. Create a Virtual Payment Address (VPA) or use the default one generated by the app.
6. To set the UPI PIN, enter the last 6 digits of your debit card and its expiry date (or choose the Aadhaar verification option).
7. Enter the OTP received from your bank, then set and confirm your new 4 or 6-digit secure UPI PIN.
8. Your UPI setup is complete. You can now send and receive money.

**Making a Payment:**
1. Open the UPI app.
2. Choose "Scan QR", "Send to Contacts", or "Enter UPI ID / Bank Details".
3. Enter the amount and add an optional remark.
4. Click "Pay" and enter your UPI PIN on the secure NPCI page.
5. Wait for the success confirmation screen.

## Safety Tips
- **NEVER share your UPI PIN:** Your UPI PIN is only required to *send* money or check your balance. You NEVER need to enter your UPI PIN to *receive* money.
- **Beware of Collect Requests:** Fraudsters send collect requests with deceptive messages like "Enter PIN to receive ₹5000 cashback." Always decline unknown requests.
- **Verify the Receiver's Name:** Before entering your PIN, double-check the registered name of the beneficiary displayed on the payment screen.
- **Avoid Screen Sharing Apps:** Never install apps like AnyDesk, TeamViewer, or QuickSupport on the instruction of unknown callers claiming to be bank or customer care executives.
- **Use Screen Locks:** Secure your mobile device and the UPI app itself with a strong password, pattern, or biometric lock (fingerprint/FaceID).

## Common Mistakes
1. **Entering PIN to Receive Money:** The most common and devastating mistake. Users are tricked into believing that entering their PIN will credit money to their account, whereas it actually debits their account.
2. **Ignoring the VPA Name:** Failing to cross-check the official registered name associated with the UPI ID before transferring large sums, resulting in money sent to the wrong person due to a typo.
3. **Sharing OTPs and Device Access:** Forwarding bank SMSs containing device binding strings or OTPs to unknown numbers, which allows hackers to clone the UPI setup on another device.
4. **Panicking on Pending Transactions:** Initiating multiple duplicate transactions when the first one shows as "Pending" or "Processing". Users often end up paying the merchant twice. The correct approach is to wait for the final status or check the bank statement.
5. **Using Public Wi-Fi:** Making large or sensitive UPI transactions while connected to unsecured, open public Wi-Fi networks, which can be susceptible to packet sniffing or man-in-the-middle attacks.

## Frequently Asked Questions

**Q1: What is UPI and how is it different from NEFT/RTGS?**
A: UPI is an instant real-time payment system that works 24x7x365 via mobile apps using a Virtual Payment Address (VPA). Unlike NEFT or RTGS, it does not require you to add beneficiaries with IFSC codes and wait for activation. It is designed for quick, everyday transactions.

**Q2: Do I need to enter my UPI PIN to receive money?**
A: No, absolutely not. You only need to enter your UPI PIN when you want to send money from your account to someone else or when you are checking your bank balance. If an app asks for your PIN to receive money, it is a scam.

**Q3: What should I do if my transaction fails but the amount is debited?**
A: Do not panic. In most cases, the system identifies the failure during reconciliation and the debited amount is automatically refunded to your bank account within 3 to 5 working days. You can also raise a dispute using the in-app help section.

**Q4: Can I link multiple bank accounts to one UPI app?**
A: Yes, you can link multiple accounts from different banks within a single UPI application. You can choose which account to set as your primary or default account for receiving funds, and you can select any linked account while sending money.

**Q5: Is there a limit on how much money I can send via UPI?**
A: Yes, standard UPI transactions have a maximum limit of ₹1 Lakh per day per bank account. However, for specific use cases like initial public offerings (IPOs), the limit is increased to ₹5 Lakhs.

**Q6: What happens if I forget my UPI PIN?**
A: You can easily reset your UPI PIN within your UPI app. You will need to select the bank account, click on "Reset UPI PIN", and verify your identity using the last 6 digits and expiry date of your linked debit card, followed by an OTP.

**Q7: Can I use UPI without internet access?**
A: Yes, you can use UPI offline by dialing *99# from your registered mobile number on any phone, including feature phones. This USSD-based service allows you to send money, check balance, and manage your UPI settings without an internet connection.

**Q8: Are there any charges for using UPI?**
A: For general retail users, peer-to-peer (P2P) and person-to-merchant (P2M) UPI transactions are completely free of charge. The government has waived off the Merchant Discount Rate (MDR) to encourage digital payments.

**Q9: What is a VPA?**
A: VPA stands for Virtual Payment Address. It is an identifier (like yourname@bank) that maps to your underlying bank account details. This allows you to receive money without exposing your actual account number and IFSC code.

**Q10: Is it safe to link my bank account to third-party apps like Google Pay or PhonePe?**
A: Yes, it is safe. These Third-Party Application Providers (TPAPs) operate under the strict guidelines of NPCI and RBI. They do not store your bank account passwords or your UPI PIN. The transaction routing is securely handled by NPCI.

**Q11: Can NRI accounts (NRE/NRO) use UPI?**
A: Yes, NPCI has enabled UPI for Non-Resident External (NRE) and Non-Resident Ordinary (NRO) accounts having international mobile numbers from select countries (like USA, UK, UAE, Singapore, etc.), provided the member banks support it.

**Q12: What is UPI AutoPay?**
A: UPI AutoPay is a feature that allows users to set up recurring e-mandates for regular payments like utility bills, OTT subscriptions, and mutual fund SIPs. Once authorized with your UPI PIN, subsequent payments up to a certain limit are deducted automatically.

**Q13: Why is my UPI account blocked?**
A: Your UPI account may be blocked due to multiple incorrect UPI PIN attempts, suspicious transaction patterns detected by your bank's fraud monitoring system, or if you have recently changed your device/SIM and are in a mandatory cooling period.

**Q14: How is UPI Lite different from regular UPI?**
A: UPI Lite is an 'on-device wallet' designed for small-value transactions (up to ₹500). It allows you to make payments without entering your UPI PIN, ensuring faster checkouts and decluttering your main bank statement, as only the wallet load is recorded.

**Q15: Can I transfer money to an account number using UPI?**
A: Yes, if the recipient does not have a UPI ID, you can choose the "Bank Transfer" option in your UPI app, enter their exact Account Number and IFSC code, and transfer funds instantly using the UPI infrastructure.

**Q16: What is the maximum number of transactions allowed per day?**
A: Besides the monetary limit of ₹1 Lakh, NPCI has capped the number of peer-to-peer UPI transactions at 20 per day per bank account to curb misuse. Person-to-merchant transactions typically do not count towards this limit.

**Q17: Will UPI work if I change my mobile handset?**
A: When you change your mobile handset, you must reinstall your UPI app, insert your registered SIM card into the new device, and complete the device binding SMS verification process again to restore access.

**Q18: What if I send money to the wrong UPI ID by mistake?**
A: UPI transactions are instantaneous and irreversible. If you send money to the wrong person, your bank cannot automatically reverse it. You must contact the recipient directly and request a refund, or raise a formal complaint with your bank immediately.

**Q19: How do I deregister or delete my UPI profile?**
A: You can deregister by opening your UPI app, navigating to the bank accounts section, and selecting "Unlink" or "Remove Account". Additionally, you can delete your entire UPI profile from the app's profile settings before uninstalling the app.

**Q20: Do I need a debit card to create a UPI PIN?**
A: Traditionally, a debit card was mandatory. However, NPCI has rolled out Aadhaar-based OTP verification, allowing users to set their UPI PIN using their Aadhaar card (provided the Aadhaar is linked to the bank account and the same mobile number).

## Common Myths vs Facts

**Myth 1:** You need to enter your UPI PIN to receive cashback or money from someone.
**Fact 1:** Absolutely false. Your UPI PIN is essentially your secret password for withdrawal. You never ever need to enter it to receive money.

**Myth 2:** Third-party apps like PhonePe or GPay store your money.
**Fact 2:** False. These apps are merely interfaces. Your money always remains safe in your actual bank account. The apps just instruct your bank to transfer funds.

**Myth 3:** UPI is not secure because it doesn't use passwords for login.
**Fact 3:** False. UPI employs robust Two-Factor Authentication. It requires device binding (something you have - the phone with SIM) and the UPI PIN (something you know).

**Myth 4:** If a UPI transaction fails, the money is lost forever.
**Fact 4:** False. Failed transactions where money is debited are automatically reconciled by the banking network. The money is refunded to the source account within 3-5 working days.

**Myth 5:** You can only use UPI on a smartphone with high-speed internet.
**Fact 5:** False. The *99# USSD service and the UPI 123Pay framework allow users of basic feature phones to use UPI services without an active internet connection.

**Myth 6:** Changing the UPI app will change your bank balance.
**Fact 6:** False. The UPI app is just a window to your bank account. Whether you use BHIM, Paytm, or GPay, the balance reflects your actual bank database, which remains unchanged.

**Myth 7:** UPI charges high fees for transactions.
**Fact 7:** False. Standard P2P and retail P2M UPI transactions are completely free of charge for the consumer. There are no hidden processing fees.

**Myth 8:** You cannot use UPI for large investments like Mutual Funds or IPOs.
**Fact 8:** False. UPI is widely accepted for Mutual Fund SIPs through AutoPay, and the transaction limit has been raised to ₹5 Lakh specifically for IPO subscriptions and government securities.

**Myth 9:** Once a VPA is created, it can never be deleted or changed.
**Fact 9:** False. You can delete or deactivate your virtual payment addresses through your UPI application settings at any time and create new ones.

**Myth 10:** UPI is only a private sector initiative.
**Fact 10:** False. UPI is developed by the National Payments Corporation of India (NPCI), an umbrella organization created by the RBI and the Indian Banks' Association (IBA).

## Conversation Examples

**Conversation 1: Basic Understanding**
*Customer (Hindi):* "Mujhe ye UPI samajh nahi aa raha. Kya hai ye?"
*Agent (Hinglish):* "Namaste! UPI (Unified Payments Interface) ek digital payment system hai. Isse aap apne mobile phone se kisi ko bhi turant paise bhej sakte hain, bina bank account number ya IFSC code yaad rakhe. Bas ek UPI ID (jaise rahul@sbi) se kaam ho jata hai."

**Conversation 2: Pending Transaction Panic**
*Customer (English):* "I just paid a merchant ₹2000. The money left my account but the app says 'Pending'. The merchant is demanding cash!"
*Agent (English):* "I understand your concern. Please do not pay cash immediately if possible. A 'Pending' status means the banking server is processing it. It will either be successful and reach the merchant shortly, or fail and automatically refund to your account within 3-5 working days. You can show the merchant the transaction reference number (UTR) for their records."

**Conversation 3: Receiving Money Scam**
*Customer (Hinglish):* "Mujhe OLX buyer ne ek request bheji hai. Keh raha hai UPI PIN dalo toh paise milenge. Kya karu?"
*Agent (Hinglish):* "Kripya apna UPI PIN bilkul mat daliye! Yeh ek fraud hai. UPI mein paise *receive* karne ke liye PIN ki kabhi zaroorat nahi hoti. PIN sirf paise *bhejne* ke liye use hota hai. Us request ko turant decline ya block kar dein."

**Conversation 4: Changing Devices**
*Customer (Hindi):* "Maine naya phone kharida hai. Purane phone mein GPay chalta tha. Naye phone me kaise chalu karu?"
*Agent (Hinglish):* "Naye phone mein apna wahi purana SIM card daaliye jo bank me registered hai. Phir app download karke mobile number verify karein. App automatic ek SMS bhej kar verification kar lega aur aapka purana account link ho jayega."

**Conversation 5: Resetting Forgotten PIN**
*Customer (English):* "I forgot my 6-digit UPI PIN. How do I recover it?"
*Agent (English):* "You can reset it easily. Open your UPI app, go to your bank account settings, and select 'Reset UPI PIN'. You will need your linked debit card. Enter the last 6 digits of the card and the expiry date. You will receive an OTP via SMS. After entering the OTP, you can set a new PIN."

**Conversation 6: Offline Transactions**
*Customer (Hinglish):* "Mera internet kaam nahi kar raha aur mujhe urgent payment karna hai. Kya karu?"
*Agent (Hinglish):* "Aap bina internet ke bhi payment kar sakte hain. Apne phone ke dialer se *99# dial karein. Ek menu aayega jismein aap 'Send Money' select karke samne wale ka mobile number aur amount daalkar, apna UPI PIN enter karke payment kar sakte hain."

**Conversation 7: Linking Multiple Accounts**
*Customer (Hindi):* "Mere paas SBI aur HDFC dono ke accounts hain. Kya mujhe 2 apps rakhne padenge?"
*Agent (Hinglish):* "Nahi, bilkul nahi. Aap ek hi app (jaise BHIM ya PhonePe) mein dono bank accounts link kar sakte hain. Payment karte samay aap select kar sakte hain ki kis bank se paise katne hain."

**Conversation 8: UPI AutoPay Cancellation**
*Customer (English):* "I set up a UPI AutoPay for Netflix, but I canceled my subscription. Will money still be deducted?"
*Agent (English):* "To be safe, you should also cancel the mandate from your end. Open your UPI app, navigate to the 'AutoPay' or 'Mandates' section, find the active Netflix mandate, and select 'Pause' or 'Revoke/Cancel'. You will need to enter your UPI PIN to confirm the cancellation."

**Conversation 9: Sending Money to Non-UPI Users**
*Customer (Hinglish):* "Jisko mujhe paise bhejne hain uske paas UPI nahi hai, sirf normal bank account hai. Kaise bheju?"
*Agent (Hinglish):* "Aap UPI app se direct bank account me bhi paise bhej sakte hain. App mein 'Bank Transfer' ya 'To Bank/UPI ID' ka option chunein. Phir unka Account Number aur IFSC code daalein, amount likhein aur pay kar dein."

**Conversation 10: Wrong Transfer Issue**
*Customer (Hindi):* "Bhaiya, maine galti se kisi aur ke number par 5000 rupaye bhej diye hain. Refund kaise hoga?"
*Agent (Hinglish):* "UPI payments turant hote hain, isliye bank automatically refund nahi kar sakta. Aapko us number par call karke unse request karni padegi ki woh paise wapas bhej dein. Agar woh mana karte hain, toh apne bank ki branch mein jakar 'Wrong Transfer' ki complaint turant darj karayein."

**Conversation 11: Transaction Limits**
*Customer (English):* "I need to send ₹2,50,000 for a medical emergency today via UPI. Is it possible?"
*Agent (English):* "I'm sorry, but the standard UPI transfer limit is ₹1,00,000 per day per bank account. For an amount of ₹2,50,000, you will need to use NEFT or RTGS through your mobile banking app or by visiting the bank branch."

**Conversation 12: Aadhaar Based PIN Setup**
*Customer (Hinglish):* "Mera debit card expire ho gaya hai aur mujhe naya UPI PIN set karna hai. Kya karu?"
*Agent (Hinglish):* "Agar aapka bank Aadhaar-based UPI support karta hai, toh aapko debit card ki zaroorat nahi hai. PIN reset karte waqt 'Aadhaar' option select karein, apne Aadhaar ke shuruwati 6 digits daalein, aur Aadhaar OTP verify karke naya PIN set kar lein."

**Conversation 13: Using UPI Lite**
*Customer (Hindi):* "Main choti choti payments karta hu 20-30 rupaye ki. Mera bank statement bahut bada ho jata hai. Koi solution hai?"
*Agent (Hinglish):* "Ji haan! Aap 'UPI Lite' activate kar sakte hain. Isme aap ek baar mein wallet me paise add kar lein. Phir 500 rupaye tak ki choti payments bina UPI PIN ke jaldi ho jayengi, aur bank statement mein sirf wallet load ki ek hi entry aayegi, har payment ki alag-alag nahi."

**Conversation 14: Daily Transaction Count Limit**
*Customer (English):* "My transaction is failing with an error saying 'Transaction limit exceeded', but I have only sent ₹10,000 today."
*Agent (English):* "Even if you haven't crossed the ₹1 Lakh limit, banks have a cap on the *number* of UPI transactions you can make in a day, which is usually 10 to 20 transactions. You might have exceeded this count. You will have to wait for 24 hours to make another P2P payment."

**Conversation 15: Disputing a Fraudulent Transaction**
*Customer (Hinglish):* "Kisi ne mere account se UPI ke through fraud karke 50,000 nikal liye. Mujhe abhi pata chala!"
*Agent (Hinglish):* "Kripya ghabrayein nahi. Sabse pehle apne bank ke customer care par call karke apna account debit freeze karwayein taki aur paise na katein. Phir 1930 (National Cyber Crime Helpline) par call karein. RBI rules ke anusar 3 din ke andar report karne par customer ko zero liability milti hai."

## Government Services
UPI serves as the backbone for various government and national-level digital infrastructure projects. It is tightly integrated with the Direct Benefit Transfer (DBT) scheme, ensuring subsidies reach citizens directly. It powers e-RUPI, a contactless, purpose-specific digital voucher system used for healthcare and government welfare. Furthermore, UPI is accepted across all Government-to-Citizen (G2C) portals, enabling swift payment of utility bills on Bharat BillPay (BBPS), traffic challans, municipal taxes, and FASTag recharges for national highways.

## Search Optimization
- **Multilingual Keywords:** UPI Payment, Unified Payments Interface, NPCI, Online Payment, PhonePe kaise chalaye, GPay, Paytm UPI, UPI PIN reset, Payment Pending, Paise fas gaye, Digital India.
- **Regional Search Terms:** "UPI account kaise banaye", "UPI limit kya hai", "UPI fraud complaint", "Bina ATM UPI kaise banaye", "Paise galat number pe gaye".
- **Abbreviations:** UPI, VPA, NPCI, PSP, TPAP, PIN, OTP, P2P, P2M, USSD.

## Intent Mapping
- **"How do I use UPI?"** -> Route to Step-by-Step Process (Setting Up).
- **"My transaction is pending"** -> Route to Risks (Technical) & FAQs (Q3).
- **"Can someone hack my UPI?"** -> Route to Risks (Cyber) & Safety Tips.
- **"I don't have an ATM card"** -> Route to FAQs (Q20) / Conversation 12.
- **"App is asking for PIN to get cashback"** -> Route to Safety Tips & Myths (Myth 1).

## Retrieval Tags
UPI, Unified Payments Interface, NPCI, Digital Payments, BHIM, PhonePe, Google Pay, Paytm, UPI PIN, VPA, Virtual Payment Address, P2P, P2M, IMPS, RTGS, NEFT, Real-time transfer, Digital wallet, UPI Lite, UPI AutoPay, 123Pay, USSD *99#, OTP, Device binding, Two-factor authentication, 2FA, Transaction limit, 1 Lakh limit, NPCI switch, Pending transaction, Failed transaction, UPI dispute, ODR, Zero liability, Cyber crime 1930, Fraud prevention, Collect request, Screen sharing fraud, Smishing, Aadhaar UPI, NRE UPI, NRO UPI, IPO UPI mandate, Debit card required, IFSC code bypass, Bank transfer, e-RUPI, FASTag, BBPS, Mobile banking, Internet banking, Payment gateway, QR code scanner, BharatQR, Merchant Discount Rate, MDR zero, PPI interoperability, Wallet to bank transfer, Payment settlement, Cooling period, Change UPI PIN, Forgot UPI PIN, Block UPI, Unlink bank account, Deregister UPI, Daily transaction count limit, Wrong transfer recovery, Reversal policy, Cashless economy, Financial inclusion, DBT integration.

## Cross-References
- [IMPS Overview](banking/payments/imps.md)
- [NEFT Guidelines](banking/payments/neft.md)
- [RTGS Transfers](banking/payments/rtgs.md)
- [Mobile Banking Basics](banking/mobile_banking/overview.md)

## See Also & References
- **National Payments Corporation of India (NPCI) Official Website:** Provides detailed API specifications, live transaction statistics, and technical guidelines for PSPs.
- **Reserve Bank of India (RBI) Circulars:** Regulatory framework for digital payment systems, limits, and customer liability guidelines.
- **Cyber Swachhta Kendra:** Ministry of Electronics and Information Technology's center for botnet cleaning and malware analysis, providing insights on mobile banking security.

## Banking Disclaimer
> **Disclaimer:** The information provided in this document is for general informational and educational purposes only and does not constitute financial, legal, or professional advice. While every effort has been made to ensure accuracy based on current NPCI and RBI guidelines, policies and limits (such as transaction caps and fees) are subject to change without prior notice. Saarthi AI is not liable for any direct, indirect, incidental, or consequential damages resulting from the use or inability to use the UPI services based on this guide. Users must never share their UPI PIN, OTP, or passwords with anyone, including individuals claiming to be bank employees or customer support agents. In case of fraudulent activity, report immediately to your bank and the National Cyber Crime Reporting Portal at 1930.
