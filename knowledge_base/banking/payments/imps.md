---
id: kb-pay-imps-001
title: Immediate Payment Service (IMPS)
domain: banking
category: Payments
subcategory: Digital Fund Transfers
topic: IMPS
version: 1.0
language: multilingual
difficulty: beginner/intermediate
keywords: IMPS, Immediate Payment Service, instant money transfer, MMID, fund transfer, NPCI, interbank transfer, instant bank transfer, 24x7 payment, electronic funds transfer
aliases: Instant Transfer, Mobile Money Transfer, IMPS Transfer, Immediate Payment
related_topics: NEFT, RTGS, UPI, MMID
intent: Provide complete, exhaustive, and actionable information on IMPS, its transaction limits, charges, technical architecture, and grievance redressal mechanisms.
last_updated: 2026-07-19
author: Saarthi AI
sources: NPCI Official Guidelines, RBI Circulars on Payment Systems, Standard Commercial Banking Handbooks
---

# Immediate Payment Service (IMPS) - The 24x7 Interbank Electronic Fund Transfer System

## Overview

**English:**
Immediate Payment Service (IMPS) is a real-time, 24x7 interbank electronic fund transfer system operated by the National Payments Corporation of India (NPCI). Introduced in 2010, it revolutionized the Indian banking sector by allowing instant money transfers between bank accounts through mobile devices, internet banking, and ATMs. Unlike traditional NEFT and RTGS, which previously operated within fixed banking hours, IMPS ensures that funds are credited to the beneficiary's account instantly, on a 24x7x365 basis, including Sundays and public holidays. It is highly secure, multichannel, and utilizes MMID (Mobile Money Identifier) or account number and IFSC for routing transactions.

**Hindi Unicode:**
इमीडिएट पेमेंट सर्विस (IMPS) नेशनल पेमेंट्स कॉरपोरेशन ऑफ इंडिया (NPCI) द्वारा संचालित एक रीयल-टाइम, 24x7 इंटरबैंक इलेक्ट्रॉनिक फंड ट्रांसफर सिस्टम है। 2010 में शुरू की गई इस सेवा ने भारतीय बैंकिंग क्षेत्र में क्रांति ला दी, जिससे मोबाइल फोन, इंटरनेट बैंकिंग और एटीएम के माध्यम से बैंक खातों के बीच तुरंत पैसे ट्रांसफर किए जा सकते हैं। पारंपरिक NEFT और RTGS (जो पहले निश्चित बैंकिंग घंटों में काम करते थे) के विपरीत, IMPS यह सुनिश्चित करता है कि लाभार्थी के खाते में पैसा तुरंत जमा हो, वो भी 24x7x365, जिसमें रविवार और सार्वजनिक अवकाश शामिल हैं। यह अत्यधिक सुरक्षित, मल्टीचैनल है और लेनदेन को रूट करने के लिए MMID (मोबाइल मनी आइडेंटिफ़ायर) या खाता संख्या और IFSC का उपयोग करता है।

**Hinglish:**
IMPS (Immediate Payment Service) NPCI dwara chalaaya jaane wala ek real-time, 24x7 interbank electronic fund transfer system hai. 2010 mein launch hone ke baad isne Indian banking system ko puri tarah badal diya, jisse aap mobile, internet banking aur ATMs ke through turant paise transfer kar sakte hain. Purane NEFT aur RTGS system ke mukable, IMPS 24x7x365 kaam karta hai, chahe Sunday ho ya bank holiday. Ye fund transfer bilkul instant hota hai aur beneficiary ke account mein turant credit ho jata hai. Aap isme MMID aur mobile number ya phir Account number aur IFSC code ka use karke highly secure tarike se paise bhej sakte hain.

## Quick Summary
* **Launch Year:** 2010
* **Managed By:** National Payments Corporation of India (NPCI)
* **Availability:** 24x7x365 (including bank holidays and Sundays)
* **Transfer Speed:** Real-time / Instantaneous
* **Maximum Limit:** Up to ₹5,000,000 (₹5 Lakhs) per transaction (limit increased by RBI recently). Note: Individual banks may set lower limits for their customers.
* **Minimum Limit:** ₹1
* **Channels Supported:** Mobile Banking, Internet Banking, ATMs, SMS, Branches
* **Primary Modes:** Account Number + IFSC, Mobile Number + MMID

## Definition
Immediate Payment Service (IMPS) is an instant payment inter-bank electronic funds transfer system in India. Built on the National Financial Switch (NFS) network, it facilitates customers to use mobile instruments as a channel for accessing their bank accounts and remitting funds seamlessly. The core objective of IMPS is to enable bank customers to transfer money instantly and securely without being constrained by clearing cycles or banking hours. By providing immediate confirmation to both the sender and the receiver, IMPS mitigates the uncertainty associated with delayed batch-processing fund transfers.

## Why It Matters
Before the advent of IMPS, electronic fund transfers in India heavily relied on NEFT (National Electronic Funds Transfer) and RTGS (Real-Time Gross Settlement). These systems were bound by specific operational timings and were unavailable on holidays and non-working Saturdays. IMPS filled this massive void by introducing a truly ubiquitous, round-the-clock payment infrastructure. It matters fundamentally because:
1. **Emergency Utility:** In medical or logistical emergencies, money can be transferred and accessed within seconds.
2. **Economic Velocity:** It increases the velocity of money in the retail sector by settling trades and personal transactions instantaneously.
3. **Foundation for UPI:** The architectural success of IMPS laid the technical and regulatory groundwork for the Unified Payments Interface (UPI).
4. **Financial Inclusion:** By utilizing mobile phones and SMS channels (via MMID), it enabled non-smartphone users and rural populations to execute digital transactions seamlessly.

## How It Works

The technical flow of an IMPS transaction involves multiple nodes communicating instantaneously over the NFS network.

```text
[Sender's App/Portal] --> Enters Beneficiary Details & Amount
          |
          V
[Remitting Bank Core Banking System] --> Deducts Funds & Validates Request
          |
          V (via NFS Network)
[NPCI Central IMPS Switch] --> Routes the transaction & logs metadata
          |
          V
[Beneficiary Bank Core Banking System] --> Validates Account & Credits Funds
          |
          V (Success Acknowledgement sent back up the chain)
[Beneficiary Account] --> Receiver Gets SMS Alert of Instant Credit
```

1. **Initiation:** The sender logs into their banking application and selects IMPS. They enter the beneficiary's Mobile Number + MMID or Account Number + IFSC.
2. **Validation:** The sender's bank validates the user's credentials, checks the available balance, and debits the amount.
3. **Transmission:** The sender's bank forwards the transaction request to NPCI's IMPS switch.
4. **Routing:** NPCI reads the IFSC/MMID, identifies the beneficiary's bank, and routes the encrypted transaction packet.
5. **Credit & Confirmation:** The beneficiary bank receives the packet, verifies the destination account, credits the amount, and sends a positive confirmation back to NPCI, which notifies the remitting bank. Both parties receive an SMS notification.

## Eligibility
To use IMPS, the following eligibility criteria must be met:
* **Account Type:** The user must have a valid savings, current, or overdraft account with a bank that is a member of the IMPS network.
* **Mobile Banking Registration:** For using the Mobile Number + MMID method, the user must be registered for mobile banking services with their respective bank.
* **Active Status:** The bank account must not be dormant, frozen, or suspended.
* **KYC Compliance:** The account must be fully KYC compliant. Minimum KYC accounts (like small accounts) may have restrictive outward transfer limits (often capped at ₹10,000 per month).
* **Beneficiary Eligibility:** The receiving bank must also be live on the IMPS network.

## Required Documents
Unlike loan processing, IMPS does not require a physical document suite per transaction, but the underlying setup requires:
* **Active Bank Account:** With a physical debit card (often needed to set up mobile banking/internet banking passwords).
* **Registered Mobile Number:** An active SIM card registered with the bank to receive OTPs (One Time Passwords) and transaction alerts.
* **MMID (Mobile Money Identifier):** A 7-digit code provided by the bank (optional, if using Account+IFSC).
* **Valid Beneficiary Details:** Accurate Account Number and 11-digit IFSC code of the receiver.

## Features & Benefits
* **Instantaneous Processing:** Funds are transferred and credited in real-time, generally within 5 to 10 seconds, regardless of the time of day. This immediate settlement eliminates counterparty credit risk for retail transactions.
* **24x7x365 Availability:** Unlike branch banking which is restricted to 10 AM - 4 PM on weekdays, IMPS is operational continuously. It works seamlessly at 3 AM on a Sunday or a National Holiday.
* **Multiple Channel Access:** Users are not restricted to one platform. IMPS can be accessed via Internet Banking web portals, Mobile Banking smartphone applications, Bank Branches (during working hours), and ATMs.
* **Dual Routing Mechanisms:** It supports Person-to-Person (P2P) transfers using just a Mobile Number and MMID (enhancing privacy by hiding account numbers) and Person-to-Account (P2A) transfers using standard Account Number and IFSC.
* **High Transaction Limits:** With the RBI increasing the maximum IMPS transaction limit from ₹2 Lakh to ₹5 Lakh per transaction, it now caters to high-value retail payments, property token advances, and large business invoice settlements.

## Risks
* **Financial Risk (Wrong Transfer):** Because IMPS is instantaneous, if a user inputs the wrong Account Number or IFSC, the funds are credited to an unintended recipient immediately. Reversing an IMPS transaction is extremely difficult and requires the cooperation of the unintended beneficiary and both banks.
* **Technical Risk (Timeouts & Pending Status):** Sometimes, due to network congestion at the beneficiary bank or NPCI switch, the transaction status may show as "Pending" or "Timeout". In such cases, funds are debited but not credited immediately. Reconciliation (auto-refund) typically takes T+1 or T+2 working days.
* **Legal Risk (Dispute Resolution):** Fraudulent transactions executed via IMPS (where the user was tricked into sending money) fall under complex cyber-legal jurisdictions. If the user authorized the transaction via OTP, the bank usually waives its liability, placing the burden on the user.
* **Cyber Security Risk (Phishing/Vishing):** Scammers often use social engineering (vishing calls) to extract mobile banking passwords, UPI PINs, or OTPs from unsuspecting users to authorize unauthorized IMPS transfers to mule accounts.

## Charges & Fees
While NEFT is largely mandated to be free for savings account holders initiating transfers online, IMPS often attracts nominal charges designed by individual banks based on transaction slabs. These charges cover the infrastructure costs of real-time processing.
* **Up to ₹1,000:** Often free or extremely nominal (e.g., ₹2.50 + GST).
* **₹1,001 to ₹10,000:** Generally ₹2.50 to ₹5.00 + GST.
* **₹10,001 to ₹1,00,000:** Generally ₹5.00 to ₹10.00 + GST.
* **₹1,00,001 to ₹5,00,000:** Generally ₹15.00 to ₹25.00 + GST.
* *Note: Charges are dynamically set by the remitter's bank. Beneficiary banks do not charge for receiving an IMPS inward remittance. GST is applicable at 18% on the fee.*

## RBI / Government Rules
* **Transaction Limits:** In October 2021, the Reserve Bank of India (RBI) enhanced the daily transaction limit of IMPS from ₹2 Lakh to ₹5 Lakh to promote digital transactions. However, banks are permitted to set their own risk-based sub-limits (e.g., ₹50,000 for new payees for the first 24 hours).
* **Cooling Period Restrictions:** As per RBI cybersecurity guidelines, when a user adds a new beneficiary, banks must enforce a "cooling period" (usually 30 minutes to 24 hours) during which only limited funds (typically ₹50,000) can be transferred via IMPS.
* **Turn Around Time (TAT) & Auto Reversal:** RBI mandates that if an IMPS transaction fails (debit successful, credit failed), the remitting bank must reverse the funds to the customer's account by T+1 working day. Failure to do so requires the bank to pay a penalty of ₹100 per day of delay to the customer.
* **Grievance Redressal:** If a dispute is not resolved by the bank within 30 days, customers are legally entitled to escalate the issue to the RBI Banking Ombudsman under the Integrated Ombudsman Scheme, 2021.

## Step-by-Step Process

### Method 1: Using Account Number and IFSC (P2A)
1. **Login:** Open your bank's Mobile App or Internet Banking portal.
2. **Navigate:** Go to the 'Fund Transfer' or 'Payments' section.
3. **Select IMPS:** Choose the 'IMPS' (Immediate Payment Service) option.
4. **Add Beneficiary:** If not already added, input the receiver's Name, exact Bank Account Number, and 11-character IFSC Code. Wait for the cooling period if applicable.
5. **Enter Amount:** Enter the transfer amount and an optional remark/narration.
6. **Authenticate:** Proceed to pay and authorize the transaction using an OTP, Transaction Password, or MPIN.
7. **Confirmation:** Wait for the success screen and SMS notification. The receiver gets the money instantly.

### Method 2: Using Mobile Number and MMID (P2P)
1. **Retrieve MMID:** The receiver must generate their 7-digit MMID via their bank's mobile app or SMS banking.
2. **Login:** The sender logs into their mobile banking app.
3. **Select IMPS (P2P):** Choose the option to transfer via Mobile Number + MMID.
4. **Enter Details:** Input the receiver's Registered Mobile Number and their 7-digit MMID.
5. **Execute:** Enter the amount, authorize with your security PIN/OTP, and complete the transfer.

## Safety Tips
* **Verify Beneficiary Details:** Always double-check the account number and IFSC before hitting 'Send'. For large amounts, perform a ₹1 test transfer first.
* **Never Share Credentials:** Never share your Internet Banking Password, MPIN, or OTP with anyone. Bank employees or customer care agents will never ask for these.
* **Avoid Public Wi-Fi:** Do not execute high-value IMPS transfers while connected to open, unsecured public Wi-Fi networks (e.g., at airports or cafes) to prevent packet sniffing.
* **Enable SMS/Email Alerts:** Ensure your bank account has active SMS and Email alerts so you are notified immediately of any unauthorized debit.
* **Check the 'Cooling Period':** Respect the bank's cooling period for new beneficiaries; it is designed to prevent massive fraud if your account is compromised.

## Common Mistakes
1. **Typographical Errors in Account Number:** Entering a wrong digit in the account number is the most common and devastating mistake, as IMPS is irreversible. Funds may be credited to a stranger.
2. **Selecting Wrong Transfer Mode:** Sometimes users intending to schedule a payment select IMPS instead of NEFT. IMPS processes immediately and cannot be scheduled or cancelled.
3. **Ignoring Network Warnings:** Proceeding with an IMPS transfer when the banking app flashes a "Network Congestion / Slow Processing" warning, leading to pending transactions and locked funds.
4. **Trusting Unverified Callers:** Making IMPS transfers to "customer care" numbers found on Google search results who ask for a small transfer to "verify your account". This is a classic phishing scam.
5. **Misunderstanding MMID:** Assuming MMID is just the ATM PIN or UPI PIN. MMID is a specific 7-digit routing code strictly used for IMPS P2P transfers.

## Frequently Asked Questions

**Q1: What are the working hours for IMPS?**
A1: IMPS operates 24 hours a day, 7 days a week, and 365 days a year. Unlike branch banking or earlier clearing systems, it does not stop for weekends, national holidays, or bank strikes. You can transfer funds at midnight, and they will be credited instantly.

**Q2: What is the maximum amount I can transfer via IMPS?**
A2: The Reserve Bank of India (RBI) allows a maximum transfer limit of ₹5 Lakh per transaction via IMPS. However, your specific bank might have lower daily limits depending on your account type and risk profile. You should check your bank’s specific limit section in your net banking profile.

**Q3: Can I transfer money via IMPS on a Sunday?**
A3: Yes, absolutely. IMPS is designed specifically to function without interruption on Sundays and all public holidays. The transaction processing is fully automated via the NPCI switch and does not require manual intervention by bank staff.

**Q4: My IMPS transaction is showing as "Pending". What should I do?**
A4: Do not initiate another transfer immediately, as this might result in a double debit. Wait for the bank's reconciliation process. In most cases, pending transactions are either successfully credited to the beneficiary or refunded to your account by the end of the next working day (T+1).

**Q5: Is there any minimum amount limit for IMPS?**
A5: The minimum amount you can transfer using IMPS is just ₹1. This makes it highly flexible for both micro-payments and large retail fund transfers, though you should be mindful of any flat transaction fees your bank might charge.

**Q6: I transferred money to the wrong account number via IMPS. How can I get it back?**
A6: Reversing an IMPS transfer is exceptionally difficult because it is real-time. You must immediately contact your bank's customer support and branch manager to raise a chargeback/wrong transfer complaint. Your bank will contact the beneficiary's bank, but the reversal ultimately requires the consent of the unintended recipient.

**Q7: Does the beneficiary need an MMID for me to send them money via Account Number + IFSC?**
A7: No. If you are using the Account Number and IFSC method (P2A), the beneficiary does not need an MMID. MMID is only required if you are transferring money using the recipient's Mobile Number (P2P).

**Q8: What is the difference between IMPS and NEFT?**
A8: IMPS processes transactions instantly on a 24x7 basis with a limit of ₹5 Lakh per transaction. NEFT processes transactions in half-hourly batches, operates 24x7, but does not have a strict maximum limit. IMPS generally incurs a small fee, whereas online NEFT is largely free for savings accounts.

**Q9: Can NRIs use IMPS for transferring funds?**
A9: Yes, Non-Resident Indians (NRIs) can use IMPS to transfer funds from their NRE/NRO accounts to other resident bank accounts in India. However, outward remittances from India to foreign banks using IMPS are not supported.

**Q10: Are there any hidden charges in IMPS?**
A10: There are no "hidden" charges, but banks do levy a transaction fee based on the amount slab, plus 18% GST on that fee. These charges must be explicitly displayed on the bank's website and are usually shown on the confirmation screen before you authorize the payment.

**Q11: How long does it take for a new payee/beneficiary to be activated for IMPS?**
A11: This depends on the bank's security policy. Typically, a cooling period lasts anywhere from 30 minutes to 24 hours. During this period, you may either be blocked from sending money to the new payee or restricted to a lower limit (e.g., ₹50,000).

**Q12: Can I use IMPS to pay my credit card bill?**
A12: Yes, many banks allow you to pay credit card bills via IMPS by adding the credit card number as the account number and using a specific IFSC code provided by the credit card issuing bank. The credit is usually reflected instantly.

**Q13: Is IMPS safe to use?**
A13: Yes, IMPS is highly secure. It uses two-factor authentication (password/biometric to log in, and OTP/MPIN to authorize the transaction). The network traffic is heavily encrypted by bank grade security and routed through NPCI's secured National Financial Switch.

**Q14: What happens if the beneficiary's bank server is down?**
A14: If the beneficiary bank's server is down, the NPCI switch will not be able to complete the transaction. The IMPS request will fail, and any debited amount will automatically be reversed to your account. This reversal usually happens immediately or within a few hours.

**Q15: Can I cancel an IMPS transaction once initiated?**
A15: No. Because IMPS is an immediate payment system, the transaction is executed and settled in real-time. Once the OTP or MPIN is entered and the request is sent, there is no window of time to cancel or stop the payment.

**Q16: Do I need a smartphone to use IMPS?**
A16: No, a smartphone is not strictly necessary. You can use IMPS via SMS banking (using Mobile Number and MMID) on a feature phone, or you can access IMPS through a bank's ATM using your debit card.

**Q17: Is it mandatory to add a beneficiary to do an IMPS transfer?**
A17: Most banks require you to add and activate a beneficiary for large amounts. However, many banks offer a "Quick Transfer" feature that allows you to send smaller amounts (usually up to ₹10,000 or ₹25,000) instantly without adding a formal beneficiary.

**Q18: What is MMID and how do I get it?**
A18: MMID (Mobile Money Identifier) is a 7-digit code issued by your bank. It links your bank account to your registered mobile number for IMPS P2P transfers. You can generate or retrieve your MMID through your mobile banking app, net banking portal, or by sending a specific SMS code to your bank.

**Q19: If my IMPS fails but money is debited, will I get compensation?**
A19: According to RBI guidelines, if a failed IMPS transaction is not reversed to your account within T+1 working days (T being the transaction date), the bank is liable to pay you a penalty of ₹100 per day of delay until the funds are credited back.

**Q20: Can I use IMPS for business accounts (Current Accounts)?**
A20: Yes, current accounts and corporate banking portals fully support IMPS. It is widely used by businesses for instant vendor payments, salary disbursements, and urgent invoice settlements within the ₹5 Lakh per transaction limit.

## Common Myths vs Facts

1. **Myth:** IMPS transfers do not work on Sundays or National Holidays.
   **Fact:** IMPS operates 24x7x365. It is completely independent of branch working days and works perfectly on Sundays, festivals, and public holidays.

2. **Myth:** If I send money to the wrong account via IMPS, the bank will automatically pull it back if I complain within 24 hours.
   **Fact:** The bank cannot automatically reverse an IMPS transaction. Once credited, the money belongs to the receiving account. Reversal strictly requires the permission of the unintended recipient.

3. **Myth:** IMPS is exactly the same as UPI.
   **Fact:** While both offer instant transfers, they are different platforms. UPI operates primarily via Virtual Payment Addresses (VPAs/UPI IDs) and mobile apps, while IMPS is the underlying architecture traditionally accessed via net banking/mobile banking using Account+IFSC or MMID.

4. **Myth:** I can transfer up to ₹50 Lakhs using IMPS.
   **Fact:** The maximum limit per IMPS transaction set by the RBI is ₹5 Lakhs. For transferring amounts larger than ₹5 Lakhs in a single transaction, you must use RTGS.

5. **Myth:** Receiving money via IMPS incurs a charge for the beneficiary.
   **Fact:** Only the remitter (the person sending the money) pays the IMPS transaction fee. The beneficiary receives the exact transferred amount with zero deductions.

6. **Myth:** IMPS cannot be used without adding a beneficiary and waiting 24 hours.
   **Fact:** Most banks offer a "Quick Transfer" feature allowing immediate IMPS transfers for smaller amounts (e.g., ₹10,000) without adding a beneficiary.

7. **Myth:** If an IMPS transaction shows "Pending", my money is lost forever.
   **Fact:** A "Pending" status just means a network timeout occurred. The systems will reconcile automatically. The money will either reach the beneficiary or be refunded to you, typically within 24 to 48 hours.

8. **Myth:** IMPS is managed by individual private banks, so my money is at risk.
   **Fact:** IMPS is built, maintained, and operated by the National Payments Corporation of India (NPCI), a highly secure, RBI-regulated entity.

9. **Myth:** I need an active internet connection on my phone to receive an IMPS transfer.
   **Fact:** Receiving funds requires no action or internet connection on the receiver's part. The funds hit the core bank account directly. You only need a basic cellular signal to receive the SMS alert.

10. **Myth:** MMID is the same as my ATM PIN and should be kept secret.
    **Fact:** MMID is a public routing identifier, not a password. It is perfectly safe to share your MMID along with your mobile number with someone who needs to send you money.

## Conversation Examples

**Scenario 1: Customer asking about IMPS timings.**
*Customer (English):* Can I use IMPS to send money to my landlord right now? It's 11 PM on a Sunday.
*Agent (English):* Yes, absolutely! IMPS is available 24x7x365. You can transfer funds at any time, including Sundays and public holidays, and the money will be credited instantly to your landlord's account.

**Scenario 2: Customer worried about a pending transaction.**
*Customer (Hindi):* Maine ₹10,000 transfer kiye the IMPS se, par status pending dikha raha hai aur mere paise kat gaye hain.
*Agent (Hindi):* Ghabraye nahi. Kabhi-kabhi network issue ki wajah se IMPS status 'Pending' ho jata hai. Aapka paisa bilkul surakshit hai. Ye aam taur par 24 se 48 ghante ke bheetar ya toh beneficiary ke account mein jama ho jayega, ya aapke account mein refund ho jayega.

**Scenario 3: Customer asking about transfer limits.**
*Customer (Hinglish):* Mujhe apne bhai ko 6 lakh rupaye bhejne hain, kya main IMPS use kar sakta hu?
*Agent (Hinglish):* RBI ki guidelines ke anusar, IMPS ki maximum limit per transaction ₹5 Lakh hai. Agar aapko ₹6 Lakh bhejne hain, toh aap ya toh RTGS ka use kar sakte hain, ya phir IMPS se multiple transactions (jaise 5 lakh aur 1 lakh) kar sakte hain.

**Scenario 4: Customer confused between NEFT and IMPS.**
*Customer (English):* Should I choose NEFT or IMPS to pay my vendor? I need the money to reach him immediately.
*Agent (English):* If you need the funds to reach the vendor immediately, you must choose IMPS. IMPS transfers money in real-time, whereas NEFT processes in batches every half hour and might take a little longer depending on the clearing cycle.

**Scenario 5: Customer sent money to the wrong account.**
*Customer (Hinglish):* Oho! Maine galti se wrong account number par IMPS kar diya hai. Paise wapas kaise aayenge?
*Agent (Hinglish):* IMPS transactions instant hote hain, isliye inhe cancel nahi kiya ja sakta. Aapko turant apni branch se contact karke 'wrong credit chargeback' request raise karni hogi. Bank receiver ki branch se contact karega, par refund receiver ki sehmati par nirbhar karta hai.

**Scenario 6: Customer asking about charges.**
*Customer (Hindi):* Kya IMPS se paise bhejne par koi charge lagta hai?
*Agent (Hindi):* Haan, IMPS ke dwara paise bhejne par bank ek chhota shulk (fee) lagata hai, jo transfer kiye gaye amount par nirbhar karta hai. Sath hi us shulk par 18% GST bhi lagta hai. Paise prapt karne wale (beneficiary) ko koi charge nahi dena padta.

**Scenario 7: Clarifying MMID usage.**
*Customer (English):* My friend asked for my MMID to send money. What is it and is it safe to share?
*Agent (English):* MMID stands for Mobile Money Identifier. It is a 7-digit code linked to your bank account used specifically for IMPS mobile transfers. Yes, it is completely safe to share your MMID and mobile number with your friend so they can send you the funds.

**Scenario 8: Failed transaction penalty.**
*Customer (Hinglish):* Mera IMPS fail ho gaya tha 4 din pehle, par abhi tak refund nahi aaya!
*Agent (Hinglish):* RBI ke niyam anusar, agar failed IMPS transaction T+1 working day me refund nahi hota, toh bank ko ₹100 per day ke hisab se penalty deni hoti hai. Kripya apne bank ke grievance portal par turant complain darj karein, aapko aapka paisa aur penalty dono milenge.

**Scenario 9: Adding a new beneficiary.**
*Customer (Hindi):* Maine naya beneficiary add kiya hai, par main IMPS se sirf 50,000 hi bhej pa raha hu. Kyu?
*Agent (Hindi):* Suraksha karno se, naya beneficiary add karne par bank 'Cooling Period' lagate hain. Aam taur par pehle 24 ghanto ke liye transfer limit ₹50,000 tak seemit hoti hai. 24 ghante pure hone ke baad aap full limit (₹5 Lakh tak) transfer kar payenge.

**Scenario 10: NRI wanting to use IMPS.**
*Customer (English):* I am an NRI. Can I use IMPS from my NRE account to send money to my mother's savings account in India?
*Agent (English):* Yes, you can! NRIs are allowed to use IMPS to transfer funds from their NRE or NRO accounts to any resident bank account within India instantly.

**Scenario 11: Customer without smartphone.**
*Customer (Hinglish):* Mere paas smartphone aur net banking nahi hai. Kya main ATM se IMPS transfer kar sakta hu?
*Agent (Hinglish):* Ji haan, aap apne debit card ka use karke kisi bhi supported bank ke ATM se IMPS fund transfer kar sakte hain. Aapko sirf receiver ka account number aur IFSC code, ya unka mobile number aur MMID chaiye hoga.

**Scenario 12: Credit card bill payment via IMPS.**
*Customer (English):* Can I pay my HDFC credit card bill instantly using IMPS from my SBI account?
*Agent (English):* Yes, you can. You need to add your 16-digit credit card number as the payee account number and use the specific IFSC code provided by HDFC Bank for credit card payments. The payment will be credited instantly.

**Scenario 13: Customer receiving spam calls.**
*Customer (Hindi):* Mujhe ek call aayi hai bol rahe hain bank se hain, aur IMPS verify karne ke liye OTP maang rahe hain.
*Agent (Hindi):* Kripya apna OTP kabhi kisi ke sath share na karein! Bank kabhi bhi aapko call karke IMPS ya koi aur OTP nahi maangta. Ye ek fraud call (phishing scam) hai. Turant call kaat dein aur us number ko block kar dein.

**Scenario 14: Difference between UPI and IMPS limits.**
*Customer (Hinglish):* UPI aur IMPS mein maximum kitna paisa bhej sakte hain ek baar mein?
*Agent (Hinglish):* Standard UPI ki limit aam taur par ₹1 Lakh per day hoti hai (kuch specific transactions chhod kar), jabki IMPS ke zariye aap ek transaction mein ₹5 Lakh tak instant bhej sakte hain. Bade amounts ke liye IMPS behtar vikalp hai.

**Scenario 15: Corporate/Business use.**
*Customer (English):* I run a small business. Can I use IMPS to disburse salaries to my employees instantly?
*Agent (English):* Yes, you can use IMPS through your corporate or current account internet banking portal. It is highly effective for instant salary disbursements or vendor payouts, provided each transfer is within the ₹5 Lakh limit.

## Government Services
* **Direct Benefit Transfer (DBT):** While the government primarily relies on Aadhaar Enabled Payment System (AePS) and NACH for mass subsidies (like PM-KISAN or LPG subsidies), IMPS architecture acts as a robust underlying framework and fallback routing mechanism for critical instant financial reliefs.
* **Jan Dhan Accounts:** PMJDY (Pradhan Mantri Jan Dhan Yojana) accounts are fully integrated into the IMPS network. Account holders can receive funds instantly from their relatives working in urban areas, deeply promoting rural financial inclusion.

## Search Optimization
* **Keywords:** IMPS, Immediate Payment Service, instant fund transfer, send money instantly, 24x7 transfer, MMID transfer, IFSC transfer, NPCI payment, NEFT vs IMPS, maximum limit IMPS, wrong IMPS transfer.
* **Regional Search Terms:** turant paise bhejna (Hindi), instant paise transfer, rat me paise bhejna, bank chutti paise transfer.
* **Abbreviations:** IMPS, NPCI, MMID, IFSC, P2P, P2A.
* **Common Typos:** IMPA, INPS, IPMS, instant transfer.

## Intent Mapping
* **Transfer Setup:** User wants to know how to set up and execute an IMPS transfer.
* **Limit Checking:** User wants to know the maximum amount they can send via IMPS.
* **Troubleshooting:** User's transaction is pending, failed, or sent to the wrong account, seeking redressal.
* **Comparison:** User is confused between NEFT, RTGS, and IMPS.
* **Charges Enquiry:** User wants to know how much the bank will deduct for an IMPS transfer.

## Retrieval Tags
`imps`, `immediate-payment-service`, `fund-transfer`, `instant-transfer`, `npci`, `mmid`, `ifsc`, `24x7-payment`, `holiday-transfer`, `electronic-funds-transfer`, `mobile-banking`, `net-banking`, `imps-limits`, `imps-charges`, `wrong-transfer`, `transaction-pending`, `rbi-guidelines`, `imps-vs-neft`, `digital-banking`, `p2p-transfer`, `p2a-transfer`, `nfs-network`.

## Cross-References
* [National Electronic Funds Transfer (NEFT)](../neft.md)
* [Real-Time Gross Settlement (RTGS)](../rtgs.md)
* [Unified Payments Interface (UPI)](upi.md)
* [Mobile Money Identifier (MMID)](../../glossary/mmid.md)
* [Indian Financial System Code (IFSC)](../../glossary/ifsc.md)

## See Also & References
* **NPCI Official IMPS Portal:** For technical routing guidelines and institutional FAQs.
* **RBI Circulars on Payment Systems (2021 update):** Regarding the enhancement of IMPS limit from ₹2 Lakhs to ₹5 Lakhs.
* **Integrated Ombudsman Scheme, 2021:** For digital transaction grievance redressal.

## Banking Disclaimer
> **Disclaimer:** The information provided in this document is for educational and informational purposes only and aligns with the standard guidelines issued by the Reserve Bank of India (RBI) and the National Payments Corporation of India (NPCI) as of 2026. Individual banks may impose different limits, cooling periods, and service charges based on their internal risk policies and account variants. Customers should always verify specific transaction limits, fees, and network statuses directly with their respective bank's official portal or customer service before initiating high-value transfers. Saarthi AI is not responsible for any financial loss resulting from typographical errors, network timeouts, or phishing scams during the execution of transactions.
