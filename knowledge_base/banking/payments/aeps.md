---
id: aeps-001
title: Aadhaar Enabled Payment System (AePS)
domain: banking
category: digital-payments
subcategory: biometric-payments
topic: Aadhaar Enabled Payment System
version: 1.0
language: multilingual
difficulty: beginner/intermediate
keywords:
  - AePS
  - Aadhaar Pay
  - Micro ATM
  - Biometric payment
  - NPCI AePS
  - CSC Banking
  - Aadhaar Withdrawal
aliases:
  - Aadhaar Payment
  - APBS
  - Micro-ATM transaction
related_topics:
  - Unified Payments Interface (UPI)
  - Direct Benefit Transfer (DBT)
  - Micro-ATMs
intent:
  - Understand AePS transactions
  - Learn how to withdraw cash using Aadhaar
  - Resolve AePS transaction failures
last_updated: "2026-07-19"
author: Saarthi AI
sources:
  - National Payments Corporation of India (NPCI)
  - Unique Identification Authority of India (UIDAI)
  - Reserve Bank of India (RBI) Circulars on AePS
---

# Aadhaar Enabled Payment System (AePS)

## Overview

**English:**
The Aadhaar Enabled Payment System (AePS) is a bank-led model which allows online interoperable financial transactions at Point of Sale (PoS) or Micro-ATMs through the Business Correspondent (BC) of any bank using the Aadhaar authentication. It empowers marginalized and unbanked populations to perform basic banking functions without needing a debit card, smartphone, or bank branch access, relying entirely on their Aadhaar number and biometric verification.

**Hindi (Unicode):**
आधार सक्षम भुगतान प्रणाली (AePS) एक बैंक-आधारित मॉडल है जो किसी भी बैंक के बिजनेस कॉरेस्पोंडेंट (BC) के माध्यम से प्वाइंट ऑफ सेल (PoS) या माइक्रो-एटीएम पर आधार प्रमाणीकरण का उपयोग करके ऑनलाइन इंटरऑपरेबल वित्तीय लेनदेन की अनुमति देता है। यह हाशिए पर रहने वाली और बिना बैंक वाली आबादी को डेबिट कार्ड, स्मार्टफोन या बैंक शाखा तक पहुंच के बिना बुनियादी बैंकिंग कार्य करने का अधिकार देता है, जो पूरी तरह से उनके आधार नंबर और बायोमेट्रिक सत्यापन पर निर्भर करता है।

**Hinglish:**
Aadhaar Enabled Payment System (AePS) ek bank-led model hai jo kisi bhi bank ke Business Correspondent (BC) ke through Micro-ATMs ya PoS par Aadhaar authentication use karke online financial transactions allow karta hai. Yeh un logo ko basic banking functions karne ki suvidha deta hai jinke paas debit card ya smartphone nahi hai, sirf unke Aadhaar number aur fingerprint/iris scan (biometric) ki madad se.

---

## Quick Summary
* **Launch Body:** National Payments Corporation of India (NPCI) in collaboration with UIDAI.
* **Core Requirement:** Bank account linked with Aadhaar.
* **Transaction Medium:** Micro-ATM / PoS terminals operated by Business Correspondents (Bank Mitras).
* **Key Services:** Cash withdrawal, balance enquiry, mini statement, Aadhaar-to-Aadhaar fund transfer, and BHIM Aadhaar Pay.
* **Daily Limit:** Typically ₹10,000 per transaction (varies by bank).
* **Authentication:** Biometric (Fingerprint, Iris, or Face authentication in newer devices).

---

## Definition
AePS (Aadhaar Enabled Payment System) is a digital payment system developed by the National Payments Corporation of India (NPCI). It enables individuals to carry out financial transactions on a Micro-ATM provided by a Banking Correspondent (BC) simply by furnishing their Aadhaar number and verifying it via biometrics (fingerprint or iris scan) mapped to their Aadhaar profile. It effectively makes the Aadhaar identity a ubiquitous financial address and biometric credential, removing the physical boundaries of traditional banking.

---

## Why It Matters
AePS plays a foundational role in India’s financial inclusion strategy (Jan Dhan-Aadhaar-Mobile or JAM trinity). 
1. **Financial Inclusion:** Reaches rural and remote areas where establishing physical bank branches or full-scale ATMs is economically unviable.
2. **Doorstep Banking:** Enables elderly, differently-abled, and highly isolated individuals to receive cash at their doorsteps through roaming Bank Mitras.
3. **Cardless & PIN-less:** Eliminates the need to carry physical ATM cards or remember PINs, heavily reducing cognitive load for less-literate populations.
4. **DBT Access:** Critical for cashing out Direct Benefit Transfers (DBT) like PM-KISAN, NREGA wages, and pensions directly in the village.

---

## How It Works

```text
=============================================================================
                          AePS TRANSACTION FLOW
=============================================================================

       [Customer] 
           | (1) Provides Aadhaar Number, Bank Name, and Biometric 
           v
 [Business Correspondent (BC) / Micro-ATM]
           | (2) Formats transaction request & sends securely
           v
     [Acquiring Bank] (Bank of the BC)
           | (3) Forwards request for interoperability
           v
        [NPCI (AePS Switch)] 
           |---------------------------------------------\
           | (4) Sends Auth Request                      | (5) Routes Financial Request
           v                                             v
       [UIDAI]                                     [Issuer Bank] (Customer's Bank)
           |                                             |
           | (Validates Fingerprint/Iris)                | (Checks Balance & Approves/Declines)
           | (Returns Yes/No)                            | (Returns Status)
           |---------------------------------------------/
           v
        [NPCI] 
           | (6) Combines Auth & Financial Status
           v
     [Acquiring Bank]
           | (7) Notifies Terminal
           v
  [Micro-ATM / PoS Terminal]
           | (8) Displays Success/Failure. Dispenses Cash (if withdrawal)
           v
       [Customer] 
=============================================================================
```

---

## Eligibility
* **Aadhaar Linking:** The customer MUST have their Aadhaar number linked to their active bank account.
* **Biometric Profile:** The customer’s biometric data (fingerprints/iris) must be updated and readable in the UIDAI database.
* **Single Account Priority:** If multiple accounts are linked to the same Aadhaar in the SAME bank, the primary account designated by the bank is used.
* **Exceptions:** "Not Applicable" for Non-Resident Indians (NRIs) without Aadhaar, or unlinked accounts.

---

## Required Documents
* **Physical Documents:** Not Applicable. No physical Aadhaar card, passbook, or debit card is required at the time of transaction.
* **Information Needed:** The 12-digit Aadhaar number (or Virtual ID) and the name of the bank where the account is held.
* **Authentication:** Live biometric scan on an authorized device.

---

## Features & Benefits

1. **Interoperability Across Banks:** A customer of State Bank of India can go to a Business Correspondent of Punjab National Bank and successfully withdraw money or check their balance. The NPCI switch seamlessly routes the transaction between the acquiring and issuing banks.
2. **Multiple Banking Services:** 
   * **Cash Withdrawal:** Taking out physical cash.
   * **Cash Deposit:** Depositing money (supported by select banks).
   * **Balance Enquiry:** Checking the current account balance.
   * **Mini Statement:** Retrieving the last few transactions.
   * **Aadhaar to Aadhaar Fund Transfer:** Sending money to another person using just their Aadhaar number (if linked to their bank).
3. **No Smartphones Required:** The entire technology stack resides with the Business Correspondent. The customer only needs to present themselves. This completely bridges the digital divide for end-users.
4. **Instant Settlements:** Transactions are processed in real-time, and customers receive immediate printed or SMS receipts (if mobile is linked) from the BC.
5. **Government Subsidy Utilization:** Immediate realization of Direct Benefit Transfers (DBT) like MNREGA, PM-Kisan, and old-age pensions without traveling long distances to the nearest town.

---

## Risks

### Financial Risks
* **Unauthorized Deductions (Failed Transactions):** Sometimes the amount is debited from the customer's account, but the BC's Micro-ATM shows a "Transaction Failed" status due to network timeout. The BC does not hand over the cash, leaving the customer temporarily out of pocket until the auto-reversal happens (usually T+5 days).
* **Overcharging by BCs:** Unscrupulous BCs might manually demand an extra "commission" or "convenience fee" for handing over the cash, which is strictly prohibited.

### Technical Risks
* **Biometric Mismatch:** Manual laborers or elderly customers often face biometric failures due to worn-out fingerprints or cataracts (for iris), rendering them unable to access their own funds.
* **Downtime and Latency:** AePS relies on multiple nodes (BC, Acquiring Bank, NPCI, UIDAI, Issuer Bank). If any single node faces server downtime, the transaction fails.

### Legal & Regulatory Risks
* **KYC Compliance:** If the underlying bank account is frozen due to incomplete KYC or e-KYC anomalies, AePS transactions will be instantly declined, leading to severe inconvenience.
* **Dispute Resolution:** Lodging a formal complaint for an AePS failure requires going to the home bank branch, which contradicts the "doorstep banking" premise if rural users have to travel to resolve it.

### Cyber & Fraud Risks
* **Silicone Fingerprint Cloning:** Scammers have historically cloned fingerprints onto silicone pads (often sourced from public registry documents) and used stolen Aadhaar numbers to drain accounts using compromised Micro-ATMs.
* **Rogue BCs:** A fraudulent BC might execute a withdrawal while telling the customer they are checking the balance, pocketing the cash and exploiting the customer's illiteracy.

---

## Charges & Fees
* **Cash Withdrawal for Customers:** Generally **FREE** of charge for the customer. The RBI mandates that BCs cannot charge customers directly.
* **Balance Enquiry / Mini Statement:** Free of charge.
* **Interchange Fee:** The Issuer bank pays an interchange fee to the Acquiring bank (usually around 0.5% of the transaction amount, capped at ₹15) to compensate the BC network.
* **Limits:** Most banks limit free AePS transactions to 4 or 5 per month, after which a fee (e.g., ₹15 - ₹20 + GST) may be applied depending on the bank's specific schedule of charges.

---

## RBI / Government Rules
* **L1 Device Mandate (UIDAI):** To combat fingerprint cloning, UIDAI has mandated the phase-out of L0 devices (which encrypt data at the software level). All AePS transactions must now happen on **L1 devices** that feature Trusted Execution Environments (TEE) and hardware-level encryption with liveness detection.
* **Standardized Limits:** NPCI allows a maximum of ₹10,000 per AePS transaction. However, individual banks can set lower limits for fraud prevention.
* **Two-Factor Authentication for BCs:** NPCI guidelines mandate that the BC must authenticate themselves via biometrics at least once a day (or for every transaction in high-risk zones) before facilitating customer transactions.
* **Turn Around Time (TAT) for Reversals:** RBI mandates that failed transactions (account debited but cash not dispensed) must be auto-reversed within **T+5 days** (Transaction date + 5 working days). If delayed, the bank must pay a penalty of ₹100 per day of delay to the customer.

---

## Step-by-Step Process

**For Cash Withdrawal:**
1. **Visit a BC / Bank Mitra:** The customer visits a local Business Correspondent equipped with a Micro-ATM/PoS.
2. **Provide Details:** The customer tells the BC their Aadhaar Number and the Name of their Bank.
3. **Select Transaction:** The BC selects "Cash Withdrawal" and enters the requested amount (e.g., ₹2,000).
4. **Provide Biometrics:** The BC prompts the customer to place their finger on the biometric scanner or look into the iris scanner.
5. **Authentication & Processing:** The device securely transmits the data to UIDAI and NPCI.
6. **Approval & Dispensation:** Upon successful authentication and balance check, the machine prints a receipt.
7. **Cash Handover:** The BC hands the physical cash (₹2,000) to the customer along with the receipt.

---

## Safety Tips
1. **Never Share OTPs:** AePS doesn't require OTPs for standard biometric withdrawals. If a BC asks for an OTP, they might be initiating a different, fraudulent transaction.
2. **Lock Biometrics:** Use the mAadhaar app or UIDAI website to lock your Aadhaar biometrics when not in use. Unlock it temporarily just before visiting a BC.
3. **Check the Receipt:** Always insist on a printed physical receipt or check your bank SMS immediately to verify the exact amount debited.
4. **Masked Aadhaar:** You only need your Aadhaar number. Do not hand over photocopies of your Aadhaar card to unknown BCs for basic withdrawals.
5. **Report Immediate Fraud:** If unauthorized AePS withdrawals occur, immediately call 1930 (Cyber Crime Helpline) and your bank's toll-free number.

---

## Common Mistakes
1. **Repeated Failed Attempts:** Attempting a transaction multiple times when the bank's server is down. This can lead to multiple debits that get stuck in the reversal pipeline.
2. **Using Unverified Agents:** Transacting at random, unbranded shops claiming to be BCs without verifying their official Bank Mitra ID or credentials.
3. **Not Linking Aadhaar Correctly:** Assuming an account is Aadhaar-enabled just because Aadhaar was given as ID. You must explicitly submit a mandate to the bank for "DBT and AePS enablement".
4. **Ignoring SMS Alerts:** Not having a registered mobile number linked to the bank account, leaving the customer blind to silent unauthorized withdrawals.
5. **Sharing Full Aadhaar Details online:** Uploading Aadhaar PDFs on public platforms, which scammers use alongside property registries to clone fingerprints.

---

## Frequently Asked Questions

**1. What is the maximum amount I can withdraw in a day via AePS?**
NPCI permits a maximum of ₹10,000 per transaction. However, most issuer banks set a daily limit of ₹10,000 for AePS withdrawals to mitigate fraud risk.

**2. Can I use AePS if I do not have a debit card?**
Yes. AePS is specifically designed for cardless transactions. You only need your Aadhaar number linked to your bank account and your physical biometric presence.

**3. Is there any fee for using AePS for cash withdrawal?**
Generally, there are no charges levied on the customer for a reasonable number of transactions (usually up to 4-5 per month). Excessive usage may attract nominal bank charges.

**4. My transaction failed, but the money was deducted. What should I do?**
Do not panic. This is a common network timeout issue. As per RBI guidelines, the amount should automatically be reversed to your account within T+5 working days.

**5. What if the money is not refunded after 5 days?**
You should raise a formal chargeback/complaint with your home bank branch. You are entitled to a compensation of ₹100 per day for delays beyond the T+5 window.

**6. Do I need to carry my physical Aadhaar card?**
No, you do not need the physical card. You only need to remember your 12-digit Aadhaar number or Virtual ID (VID).

**7. Can I deposit cash using AePS?**
Yes, cash deposit is an available feature in AePS, but it is currently supported by a limited number of banks and BC networks. 

**8. Can I transfer money to my friend using AePS?**
Yes, if your friend also has their Aadhaar linked to their bank account, you can use the 'Aadhaar to Aadhaar Fund Transfer' feature at a BC point.

**9. Why is the BC's machine not recognizing my fingerprint?**
Biometric failures occur due to worn-out fingerprints (common among manual laborers), dirt, or moisture. You can wash and dry your hands, or request the BC to use an Iris scanner if available.

**10. How can I protect my bank account from AePS fraud?**
The most effective way is to use the UIDAI portal or mAadhaar app to 'Lock' your biometric data. Unlock it only when you genuinely need to perform a transaction.

**11. Does AePS work on Sundays and public holidays?**
Yes, AePS operates 24x7x365. You can transact on holidays, provided you find an active Business Correspondent or Micro-ATM.

**12. What is an L1 device in AePS?**
An L1 device is a highly secure biometric scanner mandated by UIDAI. It checks for 'liveness' (ensuring a real human finger is placed, not a silicone clone) and encrypts data at the hardware level.

**13. The BC is asking for a ₹20 convenience fee for withdrawing ₹1000. Is this legal?**
No. BCs are paid a commission directly by the banks. Demanding an extra fee directly from the customer for AePS cash withdrawal is strictly against RBI and NPCI rules.

**14. I have multiple accounts in the same bank linked to my Aadhaar. Which one will be debited?**
The bank marks one account as the "Primary" account for Aadhaar/DBT purposes. The AePS transaction will automatically route to and debit that primary account.

**15. Can I choose which account to debit if I have accounts in different banks?**
Yes. While transacting, the BC will ask for the name of the bank. If you specify "Bank of Baroda," your BoB account will be queried. If you say "State Bank of India," your SBI account will be used.

**16. Are NRIs eligible for AePS?**
No. AePS requires an Aadhaar number, and since Aadhaar is generally for Indian residents, NRIs typically do not use AePS for their NRE/NRO accounts.

**17. Can I check my account balance without withdrawing cash?**
Yes. Balance Enquiry and Mini Statement are standalone services available on AePS without needing to perform a financial withdrawal.

**18. What is BHIM Aadhaar Pay?**
It is a merchant version of AePS. Merchants can receive payments from customers using the customer's Aadhaar and biometrics for purchasing goods, similar to a PoS machine.

**19. How do I complain against a corrupt Business Correspondent?**
You should report the BC's ID and location to the Acquiring Bank (the bank whose branding is on the micro-ATM), your home bank, and file a grievance with the Banking Ombudsman.

**20. Will AePS work if my bank account is frozen for KYC?**
No. If your bank account is inactive, frozen, or suspended due to pending KYC, all AePS transactions will be declined by your issuer bank.

---

## Common Myths vs Facts

**Myth 1:** If I tell someone my Aadhaar number, they can drain my bank account.
**Fact:** An Aadhaar number alone is useless for AePS. Live biometric authentication (fingerprint/iris) is strictly required to authorize any transaction.

**Myth 2:** AePS transactions can only be done at my home branch.
**Fact:** AePS is fully interoperable. You can perform transactions at ANY bank's Business Correspondent across India.

**Myth 3:** I need a smartphone with internet to withdraw cash via AePS.
**Fact:** You need absolutely no technology. The BC provides the internet-connected PoS device; you only provide your finger and Aadhaar number.

**Myth 4:** The BC can save my fingerprint and use it later.
**Fact:** Certified biometric scanners encrypt the fingerprint data immediately. The BC cannot save, store, or reuse your biometrics for a later transaction.

**Myth 5:** Failed AePS transactions mean my money is permanently lost.
**Fact:** The RBI guarantees auto-reversal of failed transactions within T+5 days, backed by financial penalties against the bank for delays.

**Myth 6:** AePS charges ₹50 per transaction as tax.
**Fact:** Basic cash withdrawals and balance enquiries are mostly free. No such statutory tax applies directly to the consumer.

**Myth 7:** Only rural people can use AePS.
**Fact:** Anyone with an Aadhaar-linked bank account can use AePS anywhere in India, rural or urban.

**Myth 8:** If I update my Aadhaar address, my AePS stops working.
**Fact:** Demographic updates (like address) do not affect AePS. Only biometric data and the bank linkage status matter.

**Myth 9:** AePS relies on OTPs.
**Fact:** AePS relies purely on Biometric authentication. OTPs are not part of the standard AePS cash withdrawal flow.

**Myth 10:** I must link my PAN card to use AePS.
**Fact:** PAN is not required for basic micro-transactions on AePS. Only Aadhaar-bank linkage is necessary.

---

## Conversation Examples

### Example 1: Transaction Failed but Money Deducted (English)
**Customer:** I tried to withdraw ₹3000 at the CSC center. The machine said 'failed', but I just got an SMS that ₹3000 is debited.
**Agent:** I understand your concern. In AePS, this happens due to network timeouts between the NPCI and the bank. Please do not worry. As per RBI guidelines, the amount will be automatically reversed to your account within 5 working days. 

### Example 2: BC Demanding Extra Fee (Hindi)
**Customer:** बैंक मित्र 2000 रुपये निकालने के लिए 20 रुपये अलग से मांग रहा है। क्या यह सही है?
**Agent:** नहीं, यह पूरी तरह से गलत है। आरबीआई और एनपीसीआई के नियमों के अनुसार, बिजनेस कॉरेस्पोंडेंट (BC) को ग्राहक से AePS नकद निकासी के लिए कोई भी अतिरिक्त शुल्क या कमीशन नहीं मांगना चाहिए। आप इसकी शिकायत अपने बैंक या बैंकिंग लोकपाल से कर सकते हैं।

### Example 3: Account Linking Query (Hinglish)
**Customer:** Mera account HDFC me hai, kya main gaon me PNB ke agent se paise nikal sakta hu?
**Agent:** Haan, bilkul. AePS puri tarah se interoperable hai. Agar aapka HDFC account Aadhaar se linked hai, toh aap kisi bhi bank (jaise PNB) ke Bank Mitra ya BC ke paas jakar apna Aadhaar number aur fingerprint dekar paise nikal sakte hain.

### Example 4: Daily Limits (English)
**Customer:** I need to withdraw ₹25,000 using my Aadhaar today for a medical emergency. Can I?
**Agent:** I'm afraid the standard limit for AePS cash withdrawal set by NPCI is ₹10,000 per transaction, and most banks allow only ₹10,000 per day for security reasons. For ₹25,000, you will need to use a standard ATM with a debit card, issue a cheque, or visit a bank branch.

### Example 5: Biometric Failure (Hinglish)
**Customer:** Main apna fingerprint laga raha hu par 'Biometric Mismatch' error aa raha hai.
**Agent:** Yeh kabhi-kabhi rough skin, dhool ya machine ke sensor par gandagi ki wajah se hota hai. Aap apne hath dho kar ya saaf karke dobara try kar sakte hain. Agar phir bhi na ho, toh aap BC se Iris (aankh) scanner use karne ki request kar sakte hain, agar unke paas available ho.

### Example 6: Aadhaar Lock (Hindi)
**Customer:** मैंने खबरों में आधार धोखाधड़ी के बारे में सुना है। मैं अपने खाते को कैसे सुरक्षित रखूं?
**Agent:** सबसे अच्छा तरीका है कि आप mAadhaar ऐप या UIDAI की वेबसाइट पर जाकर अपने 'बायोमेट्रिक' को लॉक कर दें। जब आपका बायोमेट्रिक लॉक होता है, तो कोई भी आपके फिंगरप्रिंट का इस्तेमाल करके AePS से पैसे नहीं निकाल सकता। जब आपको पैसे निकालने हों, तो आप इसे कुछ मिनटों के लिए अनलॉक कर सकते हैं।

### Example 7: Deposit Cash (English)
**Customer:** Can I deposit ₹5000 cash into my father's account using the Micro-ATM?
**Agent:** While AePS supports cash deposits technically, this facility is only enabled by select banks and specific BC networks right now. You will need to ask the local BC if their terminal and your father's bank support the AePS Cash Deposit feature.

### Example 8: No SMS Received (Hinglish)
**Customer:** Maine paise nikale AePS se, BC ne cash bhi diya, par bank ka message nahi aaya.
**Agent:** Agar aapko cash aur printed receipt mil gayi hai, toh transaction successful hai. SMS na aane ka kaaran bank ka SMS server delay ho sakta hai, ya shayad aapka mobile number bank account me properly updated na ho. Aap passbook print karwa ke confirm kar sakte hain.

### Example 9: Meaning of L1 Device (English)
**Customer:** The bank sent a message saying 'Use only L1 devices for AePS'. What does this mean?
**Agent:** An L1 device is a new, highly secure fingerprint scanner mandated by the government. It checks if the fingerprint belongs to a live human being and prevents scammers from using fake silicone fingerprints. It ensures your transaction is much safer.

### Example 10: Using PAN instead of Aadhaar (Hindi)
**Customer:** मेरे पास आधार कार्ड नहीं है, क्या मैं अपने पैन कार्ड का इस्तेमाल करके माइक्रो-एटीएम से पैसे निकाल सकता हूँ?
**Agent:** नहीं, AePS (आधार सक्षम भुगतान प्रणाली) पूरी तरह से आधार नंबर और आपके फिंगरप्रिंट पर आधारित है। बिना आधार और बायोमेट्रिक प्रमाणीकरण के आप इस सेवा का उपयोग नहीं कर सकते। पैन कार्ड का उपयोग इसमें नहीं किया जा सकता।

### Example 11: NRI Account (English)
**Customer:** I am an NRI and my NRE account is active. Can my parents in India withdraw money from it using AePS?
**Agent:** No, AePS operates strictly on the biometric authentication of the account holder whose Aadhaar is linked. Since you are the account holder, your parents cannot use their biometrics, and NRIs generally do not link Aadhaar to NRE accounts for such purposes.

### Example 12: Locked Account (Hinglish)
**Customer:** Mera Aadhaar verify ho raha hai, par machine par 'Account Inactive' aa raha hai.
**Agent:** Yeh tab hota hai jab aapka bank account dormant (nishkriy) ho gaya ho, ya bank ne KYC update na hone ki wajah se account freeze kar diya ho. Aapko apni bank branch jakar KYC documents submit karne honge account active karne ke liye.

### Example 13: Multiple Accounts (English)
**Customer:** Both my saving and current accounts in SBI are linked to my Aadhaar. Which will be debited?
**Agent:** By default, the bank maps one specific account (usually the primary savings account) to the NPCI mapper for Direct Benefit Transfers and AePS. That primary account will be automatically debited when you perform an AePS withdrawal.

### Example 14: Checking Pension (Hindi)
**Customer:** मुझे अपनी वृद्धावस्था पेंशन चेक करनी है, क्या मुझे बैंक जाना पड़ेगा?
**Agent:** बिल्कुल नहीं। आप अपने गाँव के किसी भी बैंक मित्र (BC) के पास जाकर, अपना आधार नंबर देकर AePS के माध्यम से 'बैलेंस पूछताछ (Balance Enquiry)' कर सकते हैं। इससे आपको पता चल जाएगा कि पेंशन आपके खाते में आई है या नहीं।

### Example 15: Overriding Daily Limit (Hinglish)
**Customer:** Maine subah ₹10,000 nikale the, kya main dopahar me ₹5,000 aur nikal sakta hu AePS se?
**Agent:** Zyadatar banks ne fraud rokne ke liye ek din me maximum ₹10,000 ki limit set ki hui hai AePS ke liye. Agar aapki bank ki limit ₹10,000 per day hai, toh aapka dusra transaction decline ho jayega aur aapko agle din try karna padega.

---

## Government Services
* **Direct Benefit Transfer (DBT):** AePS is the primary withdrawal vehicle for rural beneficiaries receiving funds via PM-KISAN, MGNREGA wages, LPG subsidies (PAHAL), and state-level social security pensions. The government deposits money via the Aadhaar Payment Bridge (APB), and citizens withdraw it via AePS.
* **CSC (Common Service Centres):** The Ministry of Electronics and IT uses the vast network of CSCs equipped with DigiPay (an AePS application) to provide banking services to the last mile.
* **IPPB (India Post Payments Bank):** Postmen act as mobile Business Correspondents, using AePS to provide doorstep banking to any bank's customer using handheld micro-ATMs.

---

## Search Optimization
**Keywords:** AePS, Aadhaar Pay, Micro ATM, biometric withdrawal, NPCI AePS limit, CSC Banking, Aadhaar withdrawal, failed AePS transaction, L1 biometric device.
**Regional/Colloquial Terms:** Angutha lagakar paise nikalna (अंगूठा लगाकर पैसे निकालना), Bank Mitra cash, Grahak Seva Kendra (ग्राहक सेवा केंद्र), Aadhaar ATM.
**Abbreviations:** AePS (Aadhaar Enabled Payment System), BC (Business Correspondent), NPCI (National Payments Corporation of India), UIDAI (Unique Identification Authority of India), PoS (Point of Sale), TEE (Trusted Execution Environment).

---

## Intent Mapping
* **"How to withdraw money without ATM card"** -> Route to AePS Process & Features.
* **"Fingerprint transaction failed but money deducted"** -> Route to FAQs / Risks (T+5 days reversal).
* **"What is the limit for Aadhaar withdrawal"** -> Route to RBI Rules / FAQs (₹10,000 limit).
* **"Bank Mitra asking for commission"** -> Route to Charges & Fees / Safety Tips.
* **"How to lock Aadhaar biometrics"** -> Route to Safety Tips / Risks.

---

## Retrieval Tags
AePS, Aadhaar Enabled Payment System, NPCI, UIDAI, Micro-ATM, Business Correspondent, Bank Mitra, Biometric payment, Fingerprint withdrawal, Iris scan, Interoperable banking, Cardless withdrawal, PIN-less transaction, DBT withdrawal, PM-KISAN, NREGA wages, Financial inclusion, JAM trinity, L1 device, L0 device, Silicone fingerprint fraud, Biometric lock, mAadhaar, Transaction failure, T+5 reversal, Auto-reversal, RBI guidelines, Chargeback, Banking ombudsman, Balance enquiry, Mini statement, Cash withdrawal, Cash deposit, Aadhaar to Aadhaar transfer, BHIM Aadhaar Pay, Point of Sale, PoS, CSC, Common Service Centre, DigiPay, IPPB, India Post Payments Bank, Doorstep banking, Rural banking, Unbanked population, Financial literacy, Aadhaar Payment Bridge, APBS, Interchange fee, MDR, Two-factor authentication, KYC compliance, Cyber crime 1930, Grievance redressal, Daily limits, Transaction limits, National Payments Corporation, Unique Identification, Aadhaar linkage, Bank mapper, Primary account, Demographic update, Virtual ID, VID, Suspended account, Frozen account, OTP fraud, Social security pension, Elderly banking, Differently-abled banking, Marginalized banking, Financial empowerment, Subsidies, PAHAL, Direct Benefit Transfer, Real-time settlement, Digital India, MEITY, Trusted Execution Environment, Liveness detection, Spoofing, Cloning, Biometric mismatch, Network timeout, Acquirer bank, Issuer bank, Switch network, Financial network, India stack, Payment settlement, Retail payments, Micro-transactions.

---

## Cross-References
* [Understanding Savings Accounts](../accounts/savings-account.md)
* [Unified Payments Interface (UPI)](upi.md)
* [Direct Benefit Transfer (DBT)](../government-schemes/dbt.md)
* [Micro-ATMs and BC Networks](../infrastructure/micro-atms.md)
* [Aadhaar Payment Bridge System (APBS)](apbs.md)

---

## See Also & References
* **NPCI Official AePS Portal:** Information on limits and technical architecture.
* **UIDAI Authentication Framework:** Guidelines on L1 devices and biometric locking.
* **RBI Circulars on Financial Inclusion:** Mandates regarding BC operations and transaction reversal TAT.

---

## Banking Disclaimer
*The information provided in this document is for educational and informational purposes only. AePS transaction limits, bank charges, and reversal timelines are subject to change as per RBI and NPCI notifications. Users are advised to verify details with their respective issuing banks. Never share OTPs or hand over unmasked Aadhaar documents to unverified agents. Report any suspicious transactions immediately to 1930 or your bank's official helpline.*
