---
id: neft-001
title: "National Electronic Funds Transfer (NEFT)"
domain: banking
category: payments
subcategory: fund_transfer
topic: neft
version: 1.0
language: multilingual
difficulty: beginner/intermediate
keywords: [NEFT, National Electronic Funds Transfer, RBI, online transfer, fund transfer, bank transfer, batch processing, UTR, NEFT timings, NEFT limit, NEFT charges]
aliases: [NEFT transfer, NEFT payment, National Electronic Funds Transfer]
related_topics: [rtgs, upi, imps]
intent: understand_neft, transfer_money_neft, check_neft_status, resolve_neft_failure
last_updated: 2026-07-19
author: Saarthi AI
sources: [RBI Official Guidelines, NPCI, Indian Banking Association]
---

# National Electronic Funds Transfer (NEFT) Comprehensive Guide

## Overview
**English**: The National Electronic Funds Transfer (NEFT) is a nation-wide centralized payment system owned and operated by the Reserve Bank of India (RBI). It enables bank customers in India to transfer funds securely and efficiently between bank accounts on a one-to-one basis. Unlike Real-Time Gross Settlement (RTGS), NEFT operates on a deferred net settlement (DNS) basis, where transactions are settled in half-hourly batches rather than continuously.
**Hindi Unicode**: नेशनल इलेक्ट्रॉनिक फंड ट्रांसफर (NEFT) भारतीय रिज़र्व बैंक (RBI) के स्वामित्व और संचालन वाली एक राष्ट्रव्यापी केंद्रीकृत भुगतान प्रणाली है। यह भारत में बैंक ग्राहकों को एक बैंक खाते से दूसरे बैंक खाते में सुरक्षित और कुशलतापूर्वक धन हस्तांतरित करने में सक्षम बनाता है। आरटीजीएस (RTGS) के विपरीत, एनईएफटी आस्थगित शुद्ध निपटान (DNS) के आधार पर संचालित होता है, जहां लेनदेन निरंतर आधार के बजाय आधे घंटे के बैचों में निपटाए जाते हैं।
**Hinglish**: NEFT ek nation-wide payment system hai jo Reserve Bank of India (RBI) manage karta hai. Iske through aap ek bank account se dusre bank account mein easily aur securely paise bhej sakte hain. RTGS ke alag, NEFT mein paise turant nahi jaate, balki half-hourly batches mein clear hote hain. Yeh 24x7 available hota hai aur isme transfer ki koi lower ya upper limit nahi hai.

## Quick Summary
* **Managed By**: Reserve Bank of India (RBI)
* **Availability**: 24x7x365 (including holidays and weekends)
* **Settlement**: Half-hourly batches (48 batches a day)
* **Minimum Limit**: ₹1 (No minimum limit)
* **Maximum Limit**: No upper limit (banks may apply limits based on customer profiles)
* **Cash Transfer Limit**: Up to ₹50,000 per transaction for walk-in customers without an account.
* **Nepal Remittance**: Allowed under the Indo-Nepal Remittance Facility Scheme.
* **Processing Time**: Usually within 2 hours of batch clearance.

## Definition
The National Electronic Funds Transfer (NEFT) system is an electronic payment system that facilitates the direct, seamless, and secure transfer of funds across the country. Any individual, firm, or corporate maintaining an account with a participating bank can transfer funds to any other individual, firm, or corporate having an account with any other NEFT-enabled bank branch in India. The system operates entirely electronically, substituting the traditional paper-based clearing mechanism and minimizing the time taken for fund remittance.

## Why It Matters
NEFT forms the backbone of non-urgent, high-volume retail electronic payments in India. Its transition to a 24x7x365 system drastically changed the financial landscape, empowering businesses to clear payrolls on weekends and allowing ordinary citizens to execute safe, traceable money transfers at any hour without worrying about banking holidays. It ensures financial inclusion by permitting cash-based remittances for individuals who do not possess a bank account, bridging the gap between the unbanked sector and the formal financial infrastructure.

## How It Works

```text
[Sender/Remitter] 
       │
       ▼ (Initiates Transfer via NetBanking / Branch)
[Originating Bank Branch]
       │
       ▼ (Validates & Forwards to NEFT Service Centre)
[NEFT Clearing Centre (RBI)]
       │
       ▼ (Consolidates & Settles in Half-Hourly Batches)
[Destination Bank Branch]
       │
       ▼ (Credits Funds to Beneficiary's Account)
[Beneficiary/Receiver]
```
1. **Initiation**: The customer initiates the transaction by adding a beneficiary using their account number and IFSC code.
2. **Batching**: The originating bank sends the transaction details to the centralized NEFT clearing house.
3. **Clearing**: RBI's NEFT system groups these requests into batches every half-hour.
4. **Settlement**: Funds are deducted from the sender's bank's pool and credited to the receiving bank's pool.
5. **Crediting**: The receiving bank deposits the amount into the beneficiary's specific account.

## Eligibility
* **Individuals**: Any Indian resident with a savings or current account in an NEFT-enabled bank. Walk-in individuals without a bank account can deposit cash up to ₹50,000 for an NEFT transfer by providing basic KYC details.
* **Corporates & Firms**: Businesses with corporate accounts can use NEFT for bulk payments like salaries, vendor payouts, and utility bill settlements without any upper limit.
* **Non-Resident Indians (NRIs)**: NRIs can use NEFT for transferring funds from their NRE/NRO accounts to other accounts within India, subject to FEMA regulations.
* **Not Applicable**: Foreign bank accounts outside of India (excluding Nepal under specific schemes) cannot be directly credited via domestic NEFT.

## Required Documents
* **For Account Holders**: No physical documents are required if using mobile or internet banking. Only the beneficiary's Account Number, Name, and IFSC Code are needed.
* **For Branch Walk-ins (Cash Deposits under ₹50,000)**: 
  - Valid ID Proof (Aadhaar, PAN, Voter ID)
  - Proof of Address (if ID doesn't contain address)
  - A completely filled out NEFT mandate/challan form at the bank branch.
* **For Corporates**: Bulk NEFT mandate files with valid authorization matrices (Digital Signatures or authorized signatories).

## Features & Benefits
1. **24x7x365 Availability**: RBI has made NEFT available round the clock on all days of the year, including weekends and public holidays. This unprecedented access means you never have to wait for the next working day to clear an essential payment.
2. **No Value Restrictions**: The RBI places no minimum or maximum limits on the amount of funds that can be transferred using NEFT. This makes it highly versatile—suitable for transferring a single rupee or several crores (though banks may enforce risk-based daily limits).
3. **Batch Processing System**: Operating on a Deferred Net Settlement (DNS) basis with 48 half-hourly batches ensures systemic stability. It processes massive volumes of transactions efficiently without overloading the immediate gross settlement infrastructure.
4. **Positive Confirmation (SMS/Email)**: Both the remitter and the beneficiary receive positive confirmation via SMS or email once the account is credited. This reduces anxiety and ensures transactional transparency.
5. **Indo-Nepal Remittance**: NEFT accommodates cross-border remittances to Nepal under a specialized scheme, easing the burden on migrant workers wishing to send money home to their families safely.

## Risks
* **Financial Risks**: While NEFT itself is secure, inputting the wrong beneficiary account number can lead to funds being transferred to an unintended recipient. The reversal process is entirely dependent on the recipient's consent, which can lead to permanent financial loss.
* **Technical Risks**: During high-traffic periods or scheduled bank maintenance, the connection to the NEFT clearing house may timeout, resulting in transactions pending in a 'Processing' state for several hours, causing distress.
* **Legal Risks**: Using NEFT for unverified or illegal transactions (e.g., hawala, illicit gambling) leaves a permanent digital trail, making the user liable for prosecution under the Prevention of Money Laundering Act (PMLA).
* **Cyber Risks**: Phishing, vishing, and malware attacks can compromise internet banking credentials. Fraudsters often trick users into adding them as a beneficiary and authorizing unauthorized NEFT mandates.

## Charges & Fees
* **Inward NEFT**: Completely FREE. Beneficiaries are not charged for receiving funds.
* **Outward NEFT (Online)**: Since 2020, RBI has mandated that no charges will be levied on NEFT transactions initiated online (via Internet Banking or Mobile Apps) by savings bank account customers.
* **Outward NEFT (Branch/Offline)**: Banks may levy minor charges for transactions initiated at the branch:
  - Up to ₹10,000: ₹2.50 + GST
  - ₹10,001 to ₹1 Lakh: ₹5 + GST
  - ₹1 Lakh to ₹2 Lakhs: ₹15 + GST
  - Above ₹2 Lakhs: ₹25 + GST

## RBI / Government Rules
* **Mandatory Credit**: RBI regulations stipulate that the receiving bank must credit the beneficiary's account within two hours of the batch settlement.
* **Penalty for Delay**: If the receiving bank fails to credit the account or return the uncredited funds to the remitter within the stipulated time, they are liable to pay penal interest to the affected customer at the current RBI LAF Repo Rate plus two percent.
* **Digital Free Rules**: To promote digital transactions, the RBI mandated the waiver of all NEFT charges for savings account holders when executed via digital channels (Circular: DPSS.CO.PD No.629/02.01.014/2019-20).

## Step-by-Step Process
**Online Process (NetBanking/Mobile App):**
1. Log in to your Internet/Mobile Banking application using your User ID and PIN/Password.
2. Navigate to 'Fund Transfers' or 'Payments' and select 'NEFT'.
3. If it's a new beneficiary, click on 'Add Beneficiary'. Enter their Name, Account Number, and IFSC Code. (Adding a beneficiary may require an OTP and a cooling period of 30 minutes to 4 hours).
4. Select the beneficiary from the list, enter the transfer amount, and add a remark (optional).
5. Verify the details and authorize the payment using a transaction password, OTP, or biometric authentication.
6. A success message displaying the UTR (Unique Transaction Reference) number will be generated.

**Offline Process (Bank Branch):**
1. Visit your home bank branch.
2. Request an NEFT transfer form.
3. Fill in your account details, beneficiary's account details, IFSC code, and the amount to be transferred.
4. Sign the form and hand it over along with a cheque (or cash if under ₹50,000) to the teller.
5. Collect the acknowledgment slip containing the UTR number for tracking.

## Safety Tips
* **Double Check IFSC & Account Number**: Always verify the account number twice before confirming. Bank systems use the account number primarily for routing; the beneficiary name is secondary and often not validated against the account number during automated processing.
* **Never Share Credentials**: Do not share your banking passwords, ATM PINs, or OTPs with anyone. Bank officials will never ask for these details over a phone call.
* **Use Official Apps Only**: Ensure you are using the official mobile banking application downloaded from verified sources like the Google Play Store or Apple App Store. Avoid clicking on links received via SMS/WhatsApp claiming to 'update your KYC'.
* **Beware of Screen-Sharing Apps**: Never install screen-sharing applications (like AnyDesk, TeamViewer) on your phone if guided by an unknown caller claiming to assist with a NEFT transfer or refund.

## Common Mistakes
1. **Wrong IFSC Code**: Using an incorrect branch IFSC code can result in a failed transaction or delays, as the funds might be routed to the wrong clearing destination before bouncing back.
2. **Incorrect Account Number**: Typographical errors in the beneficiary's account number can lead to money being deposited into an unknown person's account. Reversing this is a complex, manual legal process.
3. **Ignoring the Cooling Period**: New users often try to send large sums immediately after adding a beneficiary, unaware that banks impose a mandatory 'cooling period' (usually up to ₹50,000 for the first 24 hours) to prevent fraud.
4. **Expecting Instant Transfer**: Treating NEFT like IMPS or UPI. Users often panic when funds aren't credited instantly, forgetting that NEFT operates in half-hourly batches and can take up to two hours.
5. **Not Saving the UTR Number**: Dismissing the final screen without saving the UTR (Unique Transaction Reference) number, making it difficult to trace the transaction if a dispute arises.

## Frequently Asked Questions
1. **What is NEFT?**
   NEFT is an electronic funds transfer system operated by the RBI that settles transactions in batches. It provides a secure way to transfer money between accounts across the country.
2. **Is NEFT available 24x7?**
   Yes, since December 2019, NEFT is available 24 hours a day, 7 days a week, including all public holidays and weekends.
3. **What is the minimum amount I can transfer via NEFT?**
   There is no minimum limit for NEFT transactions. You can transfer an amount as low as ₹1.
4. **Is there a maximum limit for NEFT?**
   The RBI does not impose an upper limit for NEFT transfers. However, individual banks may set transaction limits based on their own risk management policies.
5. **How long does an NEFT transfer take?**
   Transactions are processed in half-hourly batches. Once a batch is settled, the beneficiary's account is typically credited within 2 hours.
6. **Can I send money to an overseas account using NEFT?**
   No, NEFT is restricted to domestic transactions within India, with the singular exception of remittances to Nepal under the Indo-Nepal Remittance Facility.
7. **What happens if an NEFT transaction fails?**
   If the destination bank cannot credit the beneficiary for any reason (e.g., account frozen, invalid account), the funds are returned to the originating bank within two hours, and credited back to the sender.
8. **Do I need a bank account to use NEFT?**
   Not necessarily. Walk-in customers without an account can deposit cash up to ₹50,000 at a bank branch and instruct them to transfer the funds via NEFT.
9. **What are the charges for NEFT?**
   Inward NEFT is free. Outward NEFT initiated via internet or mobile banking is entirely free for savings account holders. Offline branch transactions may incur nominal charges ranging from ₹2.50 to ₹25 plus GST.
10. **What is an IFSC code and why is it needed?**
    IFSC stands for Indian Financial System Code. It is an 11-digit alphanumeric code that uniquely identifies a bank branch participating in the NEFT network.
11. **How is NEFT different from RTGS?**
    NEFT operates on a Deferred Net Settlement (DNS) basis in batches, while RTGS settles transactions on a continuous, Real-Time Gross Settlement basis. RTGS also has a minimum limit of ₹2 Lakhs.
12. **Can an NEFT transaction be cancelled or reversed?**
    No, once an NEFT transaction is initiated and the batch is sent to the clearing center, it cannot be stopped or cancelled by the remitter.
13. **How can I track the status of my NEFT?**
    You can track the status using the 16 or 22-digit UTR (Unique Transaction Reference) number provided upon successful initiation of the transfer through your bank's customer service or online portal.
14. **Are NEFT transfers subject to tax?**
    The transfer mechanism itself is not taxed, but the amount transferred may be subject to income tax depending on the nature of the transaction (e.g., business income, gift).
15. **What is a UTR number?**
    A UTR (Unique Transaction Reference) number is a unique alphanumeric string used to identify a specific transaction in the banking system, essential for tracking and resolving disputes.
16. **Why is my NEFT transaction pending?**
    Transactions can be pending due to technical glitches at the originating bank, RBI clearing house, or the destination bank. They usually resolve within the next few batches.
17. **Can corporate customers use NEFT?**
    Yes, corporates heavily rely on NEFT for bulk payments like salary disbursements, vendor settlements, and tax payments.
18. **Does NEFT work on bank holidays?**
    Yes, NEFT operates normally on all bank holidays, national holidays, and weekends.
19. **What if the bank delays the credit?**
    If the bank delays crediting the beneficiary beyond the stipulated time, they are liable to pay a penal interest at the RBI LAF Repo Rate plus 2% for the period of delay.
20. **Can I use NEFT through a UPI app?**
    UPI uses the IMPS infrastructure, not NEFT. However, some banking apps integrate NEFT as a standard option alongside UPI for large transfers.

## Common Myths vs Facts
1. **Myth**: NEFT only works during bank working hours.
   **Fact**: NEFT is available 24x7x365. You can transfer money at midnight or on a Sunday.
2. **Myth**: NEFT is strictly for businesses and corporate users.
   **Fact**: Anyone with a bank account (or even cash up to ₹50,000) can use NEFT for personal transfers.
3. **Myth**: It takes 2 to 3 business days for an NEFT to clear.
   **Fact**: NEFT clears in half-hourly batches; funds usually reach the beneficiary within 2 hours of initiation.
4. **Myth**: You have to pay high fees for online NEFT transfers.
   **Fact**: Online NEFT transfers for savings account holders are completely free of charge as mandated by the RBI.
5. **Myth**: You can cancel an NEFT transfer if you change your mind.
   **Fact**: Once authorized and transmitted to the clearing house, NEFT transactions are irrevocable.
6. **Myth**: NEFT requires you to have a smartphone.
   **Fact**: NEFT can be initiated via basic internet banking on a computer or by visiting a physical bank branch.
7. **Myth**: If an NEFT fails, you lose your money forever.
   **Fact**: Failed transactions are automatically reversed to the sender's account, usually on the same day.
8. **Myth**: The bank verifies the recipient's name before sending the money.
   **Fact**: Transactions are processed primarily based on the Account Number and IFSC. Name mismatches are often ignored by automated systems.
9. **Myth**: You cannot do NEFT to Gramin (Rural) banks.
   **Fact**: Most Regional Rural Banks (RRBs) and Cooperative Banks are integrated into the RBI's NEFT network.
10. **Myth**: NEFT and IMPS are exactly the same thing.
    **Fact**: They use entirely different clearing infrastructures. IMPS settles instantly and individually, while NEFT settles in batches.

## Conversation Examples
**Example 1: Timing & Availability**
*Customer*: "Mujhe Sunday ko rent pay karna hai, kya NEFT chalega?"
*Agent*: "Haan sir, NEFT 24x7 aur 365 days available rehta hai. Aap Sunday ko bhi aaram se rent transfer kar sakte hain. Batch clear hote hi 2 ghante mein amount credit ho jayega."

**Example 2: Transaction Charges**
*Customer*: "Are there any hidden charges if I transfer 5 Lakhs using NEFT online?"
*Agent*: "No, absolutely not. As per RBI guidelines, online NEFT transfers from a savings account are completely free of charge, regardless of the amount."

**Example 3: Wrong Account Number**
*Customer*: "Mene galti se galat account number daal diya aur NEFT success ho gaya! Kya karu?"
*Agent*: "Sir, ghabraye nahi. Sabse pehle apni bank branch se sampark karein aur ek formal complaint darj karein with UTR number. Bank us branch se contact karegi jahan paisa gaya hai. Agar recipient agree karta hai, toh paisa reverse ho jayega."

**Example 4: Tracking a Transfer**
*Customer*: "I sent the money 3 hours ago, but my friend hasn't received it yet."
*Agent*: "I understand your concern. Could you please check your SMS or banking app for the 16-digit UTR number? You can provide this UTR to your friend so they can ask their bank to track the exact status of the incoming NEFT."

**Example 5: Minimum Limit Inquiry**
*Customer*: "Kya main 100 rupaye ka NEFT kar sakta hu? Ya koi limit hai?"
*Agent*: "Beshak! NEFT mein koi minimum limit nahi hoti. Aap ₹1 se lekar kitna bhi amount transfer kar sakte hain."

**Example 6: Cash Transfer via NEFT**
*Customer*: "Mera bank account nahi hai, par mujhe kisi ko 30,000 rupaye bhejne hain. Kya main NEFT kar sakta hu?"
*Agent*: "Ji bilkul. Aap kisi bhi NEFT-enabled bank branch mein jaakar cash de sakte hain (maximum ₹50,000 tak). Aapko ek challan bharna hoga aur apna ID proof dikhana hoga."

**Example 7: Failed Transfer Refund**
*Customer*: "My NEFT was reversed back to my account today. Why did this happen?"
*Agent*: "This usually happens if the beneficiary's account is inactive, frozen, or if the IFSC/Account combination was invalid. The receiving bank automatically returns the funds."

**Example 8: NEFT vs RTGS**
*Customer*: "Should I use NEFT or RTGS for a 3 Lakh transfer?"
*Agent*: "You can use either! RTGS will settle the funds in real-time immediately, whereas NEFT will settle in the next half-hourly batch. Both are free if done online."

**Example 9: Cooling Period Explanation**
*Customer*: "I just added a beneficiary but I can only transfer ₹50,000 today. Why?"
*Agent*: "That is a security feature called a 'cooling period'. Most banks restrict the transfer limit for the first 24 hours after adding a new beneficiary to protect your account from fraudulent, large unauthorized transfers."

**Example 10: NRI Accounts**
*Customer*: "Can I use my NRE account to send an NEFT to my family in India?"
*Agent*: "Yes, you can easily use your NRE or NRO accounts to initiate an NEFT transfer to any regular savings account within India."

**Example 11: UTR Explanation**
*Customer*: "Bank waale mujhse UTR number maang rahe hain, ye kahan milega?"
*Agent*: "UTR number aapko us SMS ya email mein milega jo transaction success hone ke baad aaya tha. Aap apni net banking ki 'Transaction History' mein bhi UTR dekh sakte hain."

**Example 12: Credit Confirmation**
*Customer*: "How will I know if the other person got the money?"
*Agent*: "Once the beneficiary's bank credits the funds to their account, you will automatically receive a positive confirmation SMS and email from the RBI's clearing system."

**Example 13: Technical Glitch**
*Customer*: "Paise kat gaye par NEFT 'Processing' dikha raha hai 1 ghante se."
*Agent*: "Kabhi-kabhi network issues ki wajah se delay hota hai. NEFT batches har aadhe ghante mein run hote hain. Kripya 2 ghante tak wait karein, status automatically update ho jayega."

**Example 14: Difference from UPI**
*Customer*: "NEFT aur UPI mein kya better hai?"
*Agent*: "Dono ke apne fayde hain. UPI chote aur instant transfers ke liye best hai kyunki ye mobile number se chal jata hai. NEFT bade amounts, business payments aur bulk transfers ke liye zyada secure aur suitable hai."

**Example 15: Cross-Border Restrictions**
*Customer*: "Can I NEFT money to my son studying in the USA?"
*Agent*: "No, NEFT cannot be used for international transfers to the USA. You will need to use a Foreign Outward Remittance via SWIFT for that purpose. NEFT is strictly for domestic transfers."

## Government Services
NEFT is deeply integrated with state and central government machineries. It is heavily utilized for Direct Benefit Transfers (DBT) where welfare schemes, subsidies (like LPG subsidy, PM-KISAN), and tax refunds (Income Tax Returns) are processed in massive bulk batches. Furthermore, services like the Jan Dhan Yojana rely on the robustness of NEFT to ensure zero-delay distribution of government aid directly to the poorest citizens' bank accounts without middle-man interference. 

## Search Optimization
* **Keywords**: NEFT transfer, National Electronic Funds Transfer, RBI payment systems, UTR tracking, NEFT batch timings, NEFT limit, offline NEFT, NEFT charges, IFSC code lookup, fund transfer delay, NEFT vs RTGS.
* **Regional/Hinglish**: NEFT kaise karein, paisa transfer bank, NEFT fail ho gaya, NEFT ka time kya hai, NEFT me kitna time lagta hai, khata number se paise bhejna.
* **Abbreviations**: NEFT, RBI, UTR, IFSC, DNS, NPCI.

## Intent Mapping
* `understand_neft`: Explains the concept, definition, and working of NEFT.
* `transfer_money_neft`: Guides the user on steps to initiate online or offline NEFT.
* `check_neft_status`: Helps users locate their UTR and track transaction status.
* `resolve_neft_failure`: Provides troubleshooting for pending, reversed, or wrong account transfers.

## Retrieval Tags
#neft #fundtransfer #rbi #banking #payments #utr #ifsc #nefttimings #neftcharges #digitalbanking #national_electronic_funds_transfer #rtgs_vs_neft #neft_status #batch_processing #onlinebanking #mobilebanking #neft_limit #cash_neft #neft_refund #neft_cooling_period #neft_tracking #indian_banking #saarthi_ai #knowledge_base #dbt #government_subsidies #banking_awareness #financial_literacy #secure_payments

## Cross-References
* [Real-Time Gross Settlement (RTGS)](./rtgs.md)
* [Immediate Payment Service (IMPS)](./imps.md)
* [Unified Payments Interface (UPI)](./upi.md)
* [Understanding IFSC Codes](../basics/ifsc_codes.md)
* [Direct Benefit Transfer (DBT)](../government_schemes/dbt.md)
* [How to Handle Wrong Transfers](../support/wrong_account_transfer.md)

## See Also & References
* **RBI NEFT FAQs**: Official guidelines published by the Reserve Bank of India on NEFT policies.
* **Indian Banks' Association (IBA)**: Circulars on standardized charges and timings.
* **FEMA Guidelines**: For non-resident accounts and cross-border limitations.

## Banking Disclaimer
> [!WARNING]
> This document is strictly for informational and educational purposes as part of the Saarthi AI Banking Knowledge Base. NEFT guidelines, limits, and charges are subject to modifications by the Reserve Bank of India (RBI) and individual banks. Users are advised to verify details from their respective home bank branches or official banking portals before executing high-value financial transactions. Saarthi AI accepts no liability for transactions sent to incorrect accounts. Never share your OTP, PIN, or banking passwords with anyone.
