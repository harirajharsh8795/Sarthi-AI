---
id: chq_101
title: "Cheque (चेक): Complete Guide"
domain: banking
category: payments
subcategory: offline_payments
topic: cheque
version: 1.0
language: multilingual
difficulty: beginner/intermediate
keywords: [Cheque, CTS, Cheque Truncation System, Cheque bounce, Section 138, NI Act 1881, Bearer Cheque, Crossed Cheque, Account Payee, PDC, Positive Pay System]
aliases: [Check, Bank Cheque, Paper Cheque, Cheque Book]
related_topics: [NEFT, RTGS, Demand Draft, UPI]
intent: understand_cheque_system
last_updated: 2026-07-19
author: Saarthi AI
sources: [RBI Guidelines, NI Act 1881, CTS-2010 Standards]
---

# Cheque (चेक) - Comprehensive Banking Guide

## Overview

**English**: A cheque is a negotiable instrument instructing a financial institution to pay a specific amount of currency from a specified transactional account held in the drawer's name with that institution. It serves as a secure, traceable, and widely accepted mode of offline payment, historically central to banking and trade, now heavily digitized via the Cheque Truncation System (CTS) and enhanced with the Positive Pay System to prevent fraud.

**Hindi Unicode**: चेक एक परक्राम्य लिखत (negotiable instrument) है जो किसी वित्तीय संस्थान को निर्देश देता है कि वह ड्रॉअर (खाताधारक) के खाते से एक विशिष्ट राशि का भुगतान करे। यह ऑफलाइन भुगतान का एक सुरक्षित, पता लगाने योग्य और व्यापक रूप से स्वीकृत तरीका है। वर्तमान में, इसे चेक ट्रंकेशन सिस्टम (CTS) के माध्यम से डिजिटल कर दिया गया है और धोखाधड़ी को रोकने के लिए पॉजिटिव पे सिस्टम (PPS) के साथ सुरक्षित किया गया है।

**Hinglish**: Cheque ek negotiable instrument hai jo bank ko instruction deta hai ki account holder ke account se ek specific amount pay kiya jaye. Ye offline payment ka ek secure aur traceable method hai jise ab CTS (Cheque Truncation System) ke through digital kar diya gaya hai. Fraud se bachne ke liye RBI ne Positive Pay System (PPS) bhi introduce kiya hai.

---

## Quick Summary

A cheque enables account holders to make payments to individuals or organizations without the need to exchange hard cash. Despite the surge in digital payments like UPI, NEFT, and RTGS, cheques remain crucial for high-value corporate transactions, post-dated loan EMIs, legal settlements, and escrow accounts. Key modern advancements include the CTS-2010 standard which eliminated the physical movement of cheques between banks, substituting it with secure electronic images, thereby drastically reducing clearance times from weeks to just a day or two.

---

## Definition

According to Section 6 of the Negotiable Instruments Act, 1881, a "cheque" is a bill of exchange drawn on a specified banker and not expressed to be payable otherwise than on demand. This includes the electronic image of a truncated cheque and a cheque in the electronic form. Essentially, it comprises three parties:
1. **Drawer**: The person who makes the cheque (account holder).
2. **Drawee**: The bank on which the cheque is drawn.
3. **Payee**: The person named in the cheque to whom the money is to be paid.

---

## Why It Matters

Cheques hold immense legal validity. Unlike basic cash transactions, a cheque leaves a concrete paper and electronic trail. Bouncing a cheque due to insufficient funds is a criminal offense in India under Section 138 of the Negotiable Instruments Act, 1881, acting as a strong deterrent against financial default. Furthermore, post-dated cheques (PDCs) act as security for loans, rental agreements, and business supply chains, providing a structured mechanism for deferred payments that electronic payments cannot fully emulate without complex mandates.

---

## How It Works

```text
[ Drawer writes Cheque ] --> [ Hands over to Payee ] 
                                      |
                                      v
[ Payee deposits Cheque in their Bank (Presenting Bank) ]
                                      |
                                      v
[ Presenting Bank scans Cheque & creates electronic image (CTS) ]
                                      |
                                      v
[ Image sent to Clearing House (NPCI / RBI) ]
                                      |
                                      v
[ Clearing House forwards image to Drawer's Bank (Drawee Bank) ]
                                      |
                                      v
[ Drawee Bank verifies Signature, Funds, and PPS Data ]
               |                                      |
       (If Approved)                             (If Rejected)
               |                                      |
               v                                      v
[ Funds Debited from Drawer ]             [ Cheque Bounced (Return Memo Generated) ]
               |                                      |
               v                                      v
[ Funds Credited to Payee ]               [ Payee notified of Dishonour ]
```

---

## Eligibility

- **Who can get a cheque book**: Any individual or entity holding a Savings Bank Account, Current Account, Overdraft Account, or Cash Credit Account with a recognized bank.
- **Minors**: Minors above 10 years of age can operate accounts independently and may be issued cheque books subject to bank-specific limits and RBI guidelines.
- **Illiterate persons**: Typically, illiterate account holders are not issued cheque books due to the inability to verify dynamic signatures, though thumb impressions are used for cash withdrawals.
- **Not Applicable**: Fixed Deposit, Recurring Deposit, and basic PPF accounts do not have cheque book facilities.

---

## Required Documents

To request a new cheque book or activate cheque facilities:
- Duly filled requisition slip (if applying via a branch for subsequent books).
- Valid government-issued ID (Aadhaar, PAN, Passport) if applying for the first time in person.
- Mobile banking / Net banking application credentials (no physical documents needed if applying online).
- For Corporate Accounts: Board resolution or authorized signatory mandate.

---

## Features & Benefits

1. **Security and Traceability**: Cheques, especially account payee crossed cheques, ensure that the money is credited solely to the intended recipient's bank account. This eliminates the risk of cash theft and provides a permanent, auditable paper trail for both personal accounting and corporate tax purposes.
2. **Deferred Payments via PDCs**: Post-Dated Cheques allow individuals and businesses to commit to a payment at a future date. This is heavily utilized in EMIs, lease agreements, and B2B credit cycles, offering liquidity management without immediate cash outflow.
3. **Legal Recourse and Protection**: Under Section 138 of the NI Act, a dishonoured cheque gives the payee the statutory right to issue a legal notice and subsequently file a criminal case against the drawer. This legal backing makes cheques a trusted instrument for large settlements and contracts.
4. **No Upper Limit**: Unlike UPI (which is capped at ₹1 lakh to ₹5 lakh depending on the category) or IMPS, there is technically no upper limit on the amount that can be written on a cheque, making it the preferred mode for real-estate purchases, corporate acquisitions, and high-value bulk transfers.
5. **Universal Acceptance**: Despite the digital boom, cheques are universally understood and accepted by all demographics, government departments, and courts across India. They do not require the payee to have a smartphone, internet connectivity, or digital literacy.

---

## Risks

**Financial Risks**:
If a cheque bounces due to insufficient funds, the drawer faces immediate penalty charges from their bank. Furthermore, frequent bouncing can severely impact the drawer's CIBIL score and relationship with the bank, potentially leading to account closure.

**Technical Risks**:
Under the CTS, if a cheque is mutilated, folded across the MICR band, or poorly scanned, the electronic clearance may fail. Overwriting, using non-standard ink, or mismatching the date format can result in technical rejection (Return Code: 35 or 88).

**Legal Risks**:
Issuing a cheque without adequate funds invites criminal prosecution under Section 138 of the NI Act. This can lead to imprisonment for up to two years, a fine extending to twice the amount of the cheque, or both. The legal battle is often time-consuming and expensive.

**Cyber and Fraud Risks**:
Cheque fraud includes forging signatures, altering the payee name or amount (chemical washing), or counterfeiting the cheque leaf itself. If a fraudster steals a bearer cheque, they can encash it over the counter. Positive Pay System (PPS) mitigates some of this by cross-verifying details for high-value cheques.

---

## Charges & Fees

- **Issuance of Cheque Book**: Banks usually offer 10 to 25 cheque leaves free per financial year for savings accounts. Beyond this, a fee of ₹2 to ₹5 per leaf is charged, plus 18% GST. Current accounts may have different tariffs.
- **Cheque Bounce Charges (Inward/Outward)**: 
  - If a cheque you issued bounces (Inward Return): ₹250 to ₹750 + GST per instance.
  - If a cheque deposited by you bounces (Outward Return): ₹100 to ₹300 + GST.
- **Stop Payment Charges**: Requesting a stop payment on an issued cheque usually incurs a fee of ₹100 to ₹200 + GST per instrument.
- **Outstation Cheque Collection**: For non-CTS clearing (rare now), banks may charge a percentage of the value (e.g., ₹50 per ₹10,000) for collection.

---

## RBI / Government Rules

- **CTS-2010 Standards**: RBI mandates that all cheques must follow the CTS-2010 standard, which includes security features like void pantograph, bank logo in invisible ink, standard paper quality, and specific field placements.
- **Validity Period**: Cheques and bank drafts are valid for exactly 3 months from the date of issue (reduced from the earlier 6 months mandate by RBI in 2012).
- **Positive Pay System (PPS)**: Effective Jan 1, 2021, RBI introduced PPS for cheques of ₹50,000 and above. While optional at ₹50k, banks may make it mandatory for cheques above ₹5,00,000. The drawer must reconfirm key details (date, name, amount) electronically to the bank before clearance.
- **Section 138 NI Act, 1881**: Governs the dishonour of cheques for insufficiency of funds, establishing it as a criminal offense punishable by imprisonment and fines.
- **MICR Band**: Magnetic Ink Character Recognition band at the bottom contains the cheque number, city/bank/branch code, account type, and transaction code. It must not be signed over or folded.

---

## Step-by-Step Process

**How to Write and Issue a Cheque Safely**:
1. **Date**: Write the current date in DD/MM/YYYY format on the top right.
2. **Payee Name**: Write the exact name of the person or company on the "Pay" line. Draw a line through any empty space after the name to prevent additions.
3. **Amount in Words**: Write the amount in words clearly on the "Rupees" line. Always add "Only" at the end (e.g., "Fifty Thousand Only") and strike through any remaining blank space.
4. **Amount in Figures**: Write the numeric amount in the right-hand box. Ensure the first digit touches the "₹" symbol so nothing can be added before it. Put a slash and hyphen at the end (e.g., ₹50,000/-).
5. **Crossing (Crucial)**: Draw two parallel lines at the top left corner and write "A/c Payee" between them. This ensures the money only goes into a bank account and cannot be encashed over the counter.
6. **Signature**: Sign clearly *above* the authorized signatory line at the bottom right. Do not sign on or below the MICR band.
7. **Record Keeping**: Note the cheque number, date, amount, and payee on the record slip provided at the beginning of the cheque book.

**How to Stop a Cheque Payment**:
1. Log in to Net Banking or the Mobile Banking app.
2. Navigate to "Services" > "Cheque Book Services" > "Stop Payment of Cheque".
3. Enter the Cheque Number and the reason for stopping it.
4. Confirm with OTP or MPIN. The bank will register the mandate instantly.

---

## Safety Tips

- **Never pre-sign blank cheques**: Always fill in the payee name, date, and amount before signing.
- **Use your own pen**: Always use your own pen to write a cheque to prevent the use of erasable or "magic" ink by fraudsters.
- **Cross your cheques**: Always make it an "A/c Payee" cheque unless you specifically want the person to withdraw cash.
- **Cancel properly**: If a cheque has an error, write "CANCELLED" in large letters across the entire face of the cheque. Do not just tear it up and throw it away; destroy the MICR band.
- **Update PPS**: Always use the bank's app to submit Positive Pay details for high-value cheques to ensure smooth clearance and prevent alteration fraud.
- **Keep it safe**: Treat your cheque book like cash. Keep it in a locked drawer.

---

## Common Mistakes

1. **Overwriting and Alterations**: Under CTS rules, no changes or corrections are allowed on cheques (except for date validation in some extremely rare, older exceptions). Any overwriting on the payee name or amount will cause instant rejection. If you make a mistake, cancel the cheque and write a new one.
2. **Signing on the MICR Band**: The bottom white strip containing magnetic ink codes is read by scanning machines. Signing over it or writing anything in that zone prevents the machine from reading the cheque, leading to rejection.
3. **Mismatched Signatures**: Our signatures evolve over time. If the signature on the cheque does not perfectly match the one scanned and stored in the bank's database, the cheque will be returned.
4. **Forgetting to Cross the Cheque**: Leaving a cheque uncrossed (a bearer cheque) means whoever holds the physical piece of paper can go to the bank branch and demand cash. This is highly risky if the cheque is lost or stolen.
5. **Post-dating incorrectly**: Writing a future year by mistake (e.g., writing 2025 instead of 2026 in January) makes the cheque a PDC for a whole year, rendering it un-clearable until that date arrives.

---

## Frequently Asked Questions

**Q1: What happens if I misplace my cheque book?**
A: You must immediately contact your bank's customer care or use mobile banking to block the entire cheque book or specific unissued cheque leaves to prevent fraudulent usage.

**Q2: Can I write a cheque in Hindi or my regional language?**
A: Yes, cheques can be written in English, Hindi, or the regional language of the state where the bank branch is located, provided the details are clear and legible.

**Q3: How long does a cheque take to clear?**
A: Under the Cheque Truncation System (CTS), local and outstation cheques usually clear within 1 to 2 working days.

**Q4: What is a stale cheque?**
A: A cheque becomes "stale" and invalid if it is not presented to the bank for payment within 3 months from the date written on it.

**Q5: What is a post-dated cheque (PDC)?**
A: A PDC bears a date in the future. The bank will not process or clear the cheque until that specified date arrives.

**Q6: Why did my cheque bounce with the reason 'Funds Insufficient'?**
A: It means the account from which the cheque was drawn did not have enough balance to cover the cheque amount at the time of presentation.

**Q7: Can a stopped cheque bounce?**
A: If you issue a 'Stop Payment' instruction, the cheque will be returned unpaid with the reason 'Payment stopped by drawer'. However, if this is done to maliciously avoid a legitimate debt, you can still face legal action under Section 138.

**Q8: What is an 'Account Payee' cheque?**
A: By drawing two parallel lines on the top left and writing "A/c Payee", you instruct the bank to deposit the funds only into the bank account of the person named on the cheque, preventing cash withdrawal.

**Q9: What is a bearer cheque?**
A: A cheque that is not crossed and is payable to the person holding or carrying the cheque (the bearer). Anyone possessing it can encash it at the counter.

**Q10: What is the Positive Pay System (PPS)?**
A: PPS is a fraud prevention system where the issuer of a high-value cheque (₹50,000+) must separately confirm the cheque details (date, payee, amount) via net banking or app to the bank before it is cleared.

**Q11: Are there charges if my cheque bounces?**
A: Yes, banks levy bounce charges on both the drawer (the one who issued it) and the payee (the one who deposited it) to cover processing and penalize default.

**Q12: Can I use different colored inks to write a cheque?**
A: It is strongly recommended to use standard blue or black ink. Red, green, or gel pens that can easily smudge or fade should be avoided, as scanners may fail to read them.

**Q13: What should I do with a cancelled cheque?**
A: A cancelled cheque is often required for KYC, EPF withdrawal, or ECS mandates to verify your bank details. Write "CANCELLED" largely across it without covering the account number or MICR code. Do not sign it.

**Q14: Can an NRI issue a cheque from an NRE account?**
A: Yes, NRIs are provided with NRE/NRO cheque books which can be used to make payments in India.

**Q15: What is a self-cheque?**
A: A cheque where the drawer writes "Self" in the payee column to withdraw cash from their own account at their home branch.

**Q16: How do I know if my cheque has cleared?**
A: You will receive an SMS alert from your bank once the amount is debited from your account. You can also check your account statement via mobile banking.

**Q17: What does the MICR code represent?**
A: MICR (Magnetic Ink Character Recognition) is a 9-digit code. The first 3 digits represent the city, the next 3 the bank, and the last 3 the specific branch.

**Q18: Can a company issue a bearer cheque?**
A: Generally, companies issue crossed Account Payee cheques for security and audit purposes. Bearer cheques by companies are highly discouraged and often restricted by banks.

**Q19: Is there a maximum limit on a cheque amount?**
A: There is no legal maximum limit for the amount that can be written on a cheque, provided the account has sufficient funds.

**Q20: Can I get my money back if I lost a bearer cheque and someone else encashed it?**
A: It is highly unlikely. Since a bearer cheque is payable to whoever holds it, the bank is legally discharged of liability once they pay the bearer over the counter in good faith. This is why crossing cheques is critical.

---

## Common Myths vs Facts

**Myth 1:** A cheque is valid for 6 months.
**Fact:** RBI reduced the validity of cheques and demand drafts to 3 months effective April 1, 2012, to curb the misuse of banking instruments.

**Myth 2:** You can correct a mistake on a cheque by signing next to it.
**Fact:** Under CTS-2010 rules, no alterations or overwriting are allowed on cheques. Any correction on the payee name or amount will lead to instant rejection. You must write a new cheque.

**Myth 3:** A post-dated cheque guarantees payment.
**Fact:** A PDC does not guarantee funds will be available on that future date. If the account is empty when presented, the PDC will bounce just like a regular cheque.

**Myth 4:** If I stop payment, I cannot be sued for a bounced cheque.
**Fact:** Stopping payment to escape a legal debt liability still attracts criminal proceedings under Section 138 of the NI Act, along with civil recovery suits.

**Myth 5:** Bearer cheques are just as safe as Account Payee cheques.
**Fact:** Bearer cheques are extremely risky. If lost, anyone can encash them at the bank counter, just like losing a ₹2000 currency note.

**Myth 6:** You must have a physical branch in your city to clear an outstation cheque.
**Fact:** CTS has eliminated the physical movement of cheques. A cheque from any bank branch in India can be cleared electronically at any other branch nationwide.

**Myth 7:** Banks verify the signature manually on every single cheque.
**Fact:** While high-value cheques are scrutinized carefully, automated systems compare digital signature mappings. Positive Pay adds a secondary layer of electronic verification.

**Myth 8:** You can write a cheque for ₹10.
**Fact:** While technically legal, banks discourage ultra-low value cheques as the processing cost (and potential bounce charges) far exceeds the cheque value. Digital payments are for micro-transactions.

**Myth 9:** A cheque bouncing is purely a civil matter between two parties.
**Fact:** Dishonour of a cheque for insufficiency of funds is a criminal offense in India, carrying a potential jail term of up to 2 years.

**Myth 10:** If the amount in words and figures differ, the cheque is automatically bounced.
**Fact:** As per Section 18 of the NI Act, if there is a discrepancy, the amount written in words is legally considered the correct amount to be paid, though practically, banks often reject them to avoid disputes.

---

## Conversation Examples

**Conversation 1 (Hindi - Overwriting Mistake)**
*Customer:* मैंने चेक पर नाम लिखते समय गलती से ओवरराइट कर दिया है और बगल में साइन कर दिया है। क्या ये चल जाएगा?
*Agent:* नमस्ते! नहीं सर, CTS-2010 की गाइडलाइंस के अनुसार चेक पर किसी भी प्रकार की ओवरराइटिंग या कटिंग मान्य नहीं है। आपका चेक रिजेक्ट हो जाएगा। कृपया इस चेक को 'CANCEL' कर दें और एक नया चेक जारी करें।

**Conversation 2 (Hinglish - Cheque Validity)**
*Customer:* Maine apne landlord ko ek cheque diya tha 4 mahine pehle, usne abhi tak deposit nahi kiya. Kya wo abhi clear ho jayega?
*Agent:* Hello! Nahi, RBI rules ke anusar ek cheque sirf 3 mahine (90 days) ke liye valid hota hai issue date se. Ab wo cheque 'stale' ho chuka hai aur bank use reject kar dega. Aapko unhe naya cheque dena hoga.

**Conversation 3 (English - Stopping Payment)**
*Customer:* I lost a cheque I had written for my supplier. How can I ensure no one else encashes it?
*Agent:* Please don't worry. You can immediately stop the payment by logging into your mobile banking app, going to the 'Cheque Services' section, and entering the cheque number to place a 'Stop Payment' request. Alternatively, I can assist you in blocking that specific cheque number right now.

**Conversation 4 (Hindi - Positive Pay System)**
*Customer:* मुझे 2 लाख रुपये का चेक देना है, क्या मुझे बैंक को पहले से बताना होगा?
*Agent:* जी बिल्कुल, 50,000 रुपये से अधिक के चेक के लिए सुरक्षा के नजरिए से 'पॉजिटिव पे सिस्टम (PPS)' का उपयोग करना अनिवार्य है। आप अपने नेट बैंकिंग या मोबाइल ऐप के माध्यम से चेक नंबर, तारीख, प्राप्तकर्ता का नाम और राशि बैंक को सबमिट कर दें, ताकि चेक आसानी से क्लियर हो सके।

**Conversation 5 (Hinglish - Crossed Cheque)**
*Customer:* Mujhe ek company ko payment karni hai par main chahta hu cash koi na nikal sake. Kaise likhu cheque?
*Agent:* Bahut aasan hai. Cheque ke top-left corner par do cross (parallel) lines draw karein aur unke beech mein "A/c Payee Only" likh dein. Isse ye ensure hoga ki paisa sirf us company ke bank account mein hi credit hoga, koi cash nahi nikal payega.

**Conversation 6 (English - Insufficient Funds Bounce)**
*Customer:* I received an SMS saying a cheque I issued bounced due to insufficient funds, but I deposited money today morning!
*Agent:* I understand your concern. The cheque clearing process happens in the evening/night. The funds must be available in your account at the exact moment the clearing house presents the cheque to your bank. Since the funds were added later, the cheque bounced. You will face a bounce penalty, and you should request the payee to present the cheque again.

**Conversation 7 (Hindi - Apply for New Book)**
*Customer:* मेरी चेकबुक खत्म हो गई है, नई कैसे मिलेगी?
*Agent:* आप अपनी नई चेकबुक कई तरीकों से मंगा सकते हैं। आप मोबाइल बैंकिंग ऐप में 'Request Cheque Book' विकल्प चुन सकते हैं, एटीएम से रिक्वेस्ट कर सकते हैं, या अपनी होम ब्रांच में एक रिक्वेस्ट स्लिप भरकर जमा कर सकते हैं। चेकबुक 5-7 कार्य दिवसों में आपके रजिस्टर्ड पते पर डाक द्वारा आ जाएगी।

**Conversation 8 (Hinglish - MICR Band)**
*Customer:* Mere cheque par niche jo safed patti hoti hai, uspe maine galti se sign kar diya hai.
*Agent:* Oh, wo MICR band hota hai jise scanner read karta hai. Agar us par sign ya koi daag hai, toh machine use scan nahi kar payegi aur cheque reject ho jayega. Aapko us cheque ko cancel karke naya cheque banake dena padega.

**Conversation 9 (English - Outstation Cheque)**
*Customer:* I have an account in Delhi but someone gave me a cheque from a Chennai branch. Will it take weeks to clear?
*Agent:* Not at all! Thanks to the Cheque Truncation System (CTS), physical cheques don't travel anymore. It will be scanned at your Delhi branch and cleared electronically. It should take the standard 1 to 2 working days.

**Conversation 10 (Hindi - Cancelled Cheque for Loan)**
*Customer:* मुझे कार लोन के लिए एक 'कैंसल्ड चेक' देना है। ये क्या होता है?
*Agent:* कैंसल्ड चेक आपके खाते का प्रमाण होता है। आप अपनी चेकबुक से एक खाली चेक लें और उस पर बड़े अक्षरों में "CANCELLED" लिख दें। इस पर आपको हस्ताक्षर नहीं करने हैं और न ही कोई राशि लिखनी है। यह सिर्फ आपका अकाउंट नंबर और IFSC कोड वेरिफाई करने के लिए लिया जाता है।

**Conversation 11 (Hinglish - Post Dated Cheque)**
*Customer:* Maine aaj ki date daal di hai par main chahta hu banda agle mahine paise nikale.
*Agent:* Agar aapne aaj ki date daali hai toh wo aaj hi bank mein laga sakta hai. Agar aap chahte hain ki wo agle mahine clear ho, toh aapko cheque par agle mahine ki date (Post-Dated Cheque) likhni chahiye thi. Ab aapko unse request karni padegi ki wo cheque agle mahine lagaye, ya phir is cheque ko cancel karke naya PDC dein.

**Conversation 12 (English - Cheque Charges)**
*Customer:* Why was ₹295 deducted from my account for 'Cheque Book Issuance'?
*Agent:* As per the bank's tariff, the first 25 cheque leaves in a financial year are free. Since this was your second cheque book request of 25 leaves, a standard charge of ₹250 plus 18% GST (₹45) was levied, totaling ₹295.

**Conversation 13 (Hindi - Signature Mismatch)**
*Customer:* मेरा चेक 'Signature Mismatch' की वजह से वापस आ गया है। अब क्या करूँ?
*Agent:* इसका अर्थ है कि चेक पर किए गए आपके हस्ताक्षर बैंक के रिकॉर्ड में मौजूद हस्ताक्षर से मेल नहीं खा रहे हैं। आपको या तो सही हस्ताक्षर के साथ एक नया चेक देना होगा, या अपनी होम ब्रांच में जाकर एक फॉर्म भरकर अपने नए हस्ताक्षर बैंक रिकॉर्ड में अपडेट कराने होंगे।

**Conversation 14 (Hinglish - Minor Account Cheque Book)**
*Customer:* Mera beta 12 saal ka hai aur uska account hai. Kya usko cheque book mil sakti hai?
*Agent:* Haan, RBI guidelines ke anusar 10 saal se upar ke minors jo apna account khud operate karte hain, unhe cheque book facility di ja sakti hai. Halaanki, banks minors ke accounts par ek limit set karte hain taaki risk kam rahe. Aap branch mein apply kar sakte hain.

**Conversation 15 (English - Difference between NEFT and Cheque)**
*Customer:* Should I give a cheque of 5 lakhs to my interior designer or do NEFT? What's better?
*Agent:* NEFT is faster, entirely digital, and the funds will reflect in their account within a few hours without any risk of signature mismatch or bouncing. However, if the designer needs a physical instrument for their accounting records or if you want to delay the payment by post-dating it, a cheque is the way to go. Otherwise, NEFT is highly recommended.

---

## Government Services

- **EPFO & Pensions**: Providing a cancelled cheque is a mandatory requirement for withdrawing Employees' Provident Fund (EPF) to ensure the funds are routed to a verified bank account belonging to the employee.
- **Direct Benefit Transfer (DBT)**: While DBT schemes (like PM-KISAN, LPG subsidy) use Aadhaar Payments Bridge System (APBS) directly to accounts, local level government disbursements (municipal contractor payouts, land acquisition compensations) still heavily utilize government treasuries issuing cheques to citizens.
- **Tax Refunds**: Historically Income Tax refunds were sent via physical cheques by speed post; however, this has almost entirely transitioned to direct bank transfers (ECS) based on bank account pre-validation on the e-filing portal.

---

## Search Optimization

- **Multilingual Keywords**: Cheque book, चेक बुक, Bank Check, Cheque Bounce, Section 138, CTS clearing, PPS, Positive Pay, Cancelled Cheque, Account Payee, Bearer Cheque, PDCs, cheque clearing time, crossed cheque meaning.
- **Regional Search Terms**: "Cheque kaise bhare", "Cheque bounce case kya hai", "Cancelled cheque ka use", "Cheque kitne din me clear hota hai", "Cheque par date ki validity".
- **Abbreviations**: CTS (Cheque Truncation System), PPS (Positive Pay System), PDC (Post Dated Cheque), NI Act (Negotiable Instruments Act), MICR (Magnetic Ink Character Recognition).

---

## Intent Mapping

- `how_to_write_cheque`: Route to Step-by-Step Process & Safety Tips.
- `cheque_bounced_reason`: Route to Risks & Charges.
- `what_is_cancelled_cheque`: Route to FAQ 13 & Step-by-Step Process.
- `cheque_validity_time`: Route to RBI Rules & FAQ 4.
- `stop_cheque_payment`: Route to Step-by-Step Process.

---

## Retrieval Tags

#Cheque, #BankCheck, #CTS, #ChequeTruncationSystem, #ChequeBounce, #Section138, #NIAct, #PositivePaySystem, #PPS, #AccountPayee, #BearerCheque, #CrossedCheque, #PostDatedCheque, #PDC, #CancelledCheque, #MICR, #ClearingHouse, #ChequeValidity, #StaleCheque, #StopPayment, #ChequeBook, #SignatureMismatch, #BankingSafety, #OfflinePayment, #NegotiableInstrument, #Drawer, #Drawee, #Payee, #ChequeCharges, #ReturnMemo, #FraudPrevention, #BankGuidelines, #RBI, #FinancialLiteracy, #HindiBanking, #HinglishSupport

---

## Cross-References

- To learn about digital alternatives, see: [NEFT Overview](neft.md)
- For instant high-value transfers, refer to: [RTGS Guidelines](rtgs.md)
- For mobile-based payments, check: [UPI Guide](upi.md)
- For other paper-based banking instruments: [Demand Draft (DD)](demand_draft.md)

---

## See Also & References

- *The Negotiable Instruments Act, 1881 (Bare Act)*
- *RBI Master Circular - Mobile Banking & Cheque Clearing (CTS-2010)*
- *NPCI Guidelines on Cheque Truncation System*

---

> **Banking Disclaimer**: The information provided regarding cheque rules, validity, bounce charges, and penal sections is based on prevailing RBI guidelines and the Negotiable Instruments Act as of 2026. Bank-specific charges (issuance, bounce penalties) may vary and are subject to change. For legal disputes under Section 138, consulting a legal professional is strictly advised.
