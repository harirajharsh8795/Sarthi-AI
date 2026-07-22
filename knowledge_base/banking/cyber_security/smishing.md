---
id: smishing
title: Smishing (एसएमएस फ़िशिंग / संदेश घोटाला)
domain: banking
category: cyber_security
subcategory: personal_security
topic: smishing
version: 1.0
language: multilingual
difficulty: beginner
keywords: [smishing, SMS phishing, spam SMS, SMS link fraud, pan card link sms, account block sms, cyber security]
aliases: [sms link scam, text message fraud]
related_topics: [banking/cyber_security/phishing.md, banking/cyber_security/vishing.md, banking/cyber_security/reporting_fraud.md]
intent: [definition, fraud_help, customer_rights]
last_updated: 2026-07-19
author: Saarthi AI
sources: [Reserve Bank of India (RBI), Telecom Regulatory Authority of India (TRAI)]
---

# Smishing (एसएमएस फ़िशिंग / संदेश घोटाला)

## Overview

### English
Smishing (short for SMS Phishing) is a cyber-attack method that uses deceptive text messages (SMS or instant chats) to trick recipients into clicking malicious links or calling fraudulent helpline numbers, with the intent of stealing banking passwords, card numbers, or installing malware.

### Hindi
स्मीशिंग (Smishing / एसएमएस फ़िशिंग) एक साइबर-हमले की पद्धति है जो प्राप्तकर्ताओं को दुर्भावनापूर्ण लिंक (malicious links) पर क्लिक करने या धोखेबाज हेल्पलाइन नंबरों पर कॉल करने के लिए प्रेरित करने के लिए कपटपूर्ण टेक्स्ट संदेशों (SMS) का उपयोग करती है, जिसका उद्देश्य बैंकिंग पासवर्ड, कार्ड नंबर चोरी करना या वायरस इंस्टॉल करना है।

### Hinglish
Smishing (yaani SMS Phishing) ek aisa cyber fraud hai jisme thag log aapke mobile par dhoke se bhare SMS ya WhatsApp messages bhejte hain. In messages me aamtaur par aisi links hoti hain jo aapko apna bank account active karne, PAN card link karne, ya lottery claim karne ke liye click karne ko kehti hain. Link par click karte hi aap aisi fake websites par chale jate hain jahan aapke passwords aur card details chori ho jate hain.

---

## Quick Summary
Smishing is phishing conducted via text messaging. It has a higher success rate for scammers because people generally trust text messages on their mobile phones more than emails. Smishing messages are designed to cause panic or excite the target. Common formats include fake alerts claiming: "Dear Customer, your bank account has been blocked due to pending KYC. Click here to verify: [fake link]" or claiming a electricity power cut unless an unpaid bill is paid immediately via a phone number.

When the victim clicks the link, they are directed to a spoofed bank login page where they are asked to enter their customer ID, net banking password, and the subsequent transaction OTP. Under TRAI regulations in India, all banking and utility messages must use registered headers (like VM-HDFCBK or AD-KOTAKB) instead of standard 10-digit mobile numbers. Messages from personal numbers claiming to be banks are almost always scams.

---

## Definition
Smishing is a social engineering attack mechanism executed over Short Message Service (SMS) protocols or messaging applications, leveraging spoofed sender headers or bulk SMS gateways to deliver phishing URLs or fraudulent contact numbers to retail consumers.

---

## Why It Matters
Understanding smishing is crucial because:
- **High Penetration Rate:** Mobile phones are always active and accessible, making SMS the easiest way for scammers to reach remote and rural populations.
- **Urgency Exploitation:** Scammers use terms like "Immediate action required" or "Electricity disconnect tonight" to trigger panic, leading victims to click links without thinking.
- **Bypasses Email Filters:** Phishing emails are often caught by smart email spam filters, but text messages go directly to the user's primary SMS inbox.

---

## How It Works
The standard execution flow of an electricity bill smishing scam:

Scammer sends bulk SMS to random numbers: "Electricity bill unpaid. Power cut at 9:30 PM. Call officer at 9xxxxxxxxx."
↓
Worried customer calls the listed mobile number in panic
↓
Scammer answers: "I am from the electricity board. Pay ₹10 immediately online to update records."
↓
Scammer sends a SMS link: "Click here to pay ₹10."
↓
Customer clicks link; a fake payment page opens demanding debit card number, expiry, and CVV
↓
Customer inputs card details to pay the ₹10
↓
Scammer initiates an unauthorized transfer of ₹50,000 on the card backend
↓
Customer receives OTP SMS: "OTP for transaction of ₹50,000"
↓
In panic, customer types the OTP on the website, thinking it is for the ₹10 payment
↓
Transaction completes; ₹50,000 is debited, and scammer disconnects

---

## Eligibility
- **Targets:** Any mobile user with SMS access, especially those linked to mobile banking and UPI.

---

## Required Documents
- **Not Applicable:** For reporting smishing scams:
  - Copy of the received SMS text and the sender's header/number.
  - Screenshot of the fake website/link.
  - Bank transaction statement showing the debit (if defrauded).
  - Cyber Crime complaint printout.

---

## Features
- **Sender Header Spoofing:** Creating fake headers that look like banks, although modern blockchain-based SMS portals have restricted this in India.
- **Malicious Short URLs:** Using URL shorteners (like bit.ly, tinyurl, or custom short links) to hide the real destination of the fake website.
- **Coercive Content:** Threats of immediate SIM blocking, account suspension, or court cases.

---

## Benefits of Safety Knowledge
- **Header Identification:** Knowing how to distinguish between official banking headers and regular 10-digit mobile numbers.
- **URL Verification:** Identifying suspicious extensions (.in-update, .xyz, .top) before clicking.

---

## Risks
- **Financial Fraud:** Rapid siphoning of bank balances via online portals.
- **Malware Download:** Clicking the link may download silent Android Trojan apps (APKs) that record keystrokes and forward SMS messages automatically.
- **Identity Exploitation:** Leakage of Aadhaar and PAN card photo copies uploaded on fake sites.

---

## Charges & Fees
- **Spam Reporting:** Free (via DND apps or calling 1909).

---

## RBI / Government Rules
- **TRAI Header Registration Mandate:** TRAI mandates that all telemarketers and banks must use registered alpha-headers (like HDFCBK, SBIIN) for sending transactional SMS. SMS from personal 10-digit mobile numbers claiming to be banks are illegal.
- **NCRP Fraud Interception:** Reporting the fraudulent phone number quickly on the cyber portal helps the Home Ministry block the scammer's handset IMEI number national-wide.
- **Zero Liability Rules:** Customer liability is evaluated under RBI guidelines based on reporting timelines.

---

## Step-by-Step Process

### How to Identify and Handle a Smishing Message:
1. **Analyze the Sender:** Look at the sender ID. If it is a standard 10-digit number (e.g., +91-9xxxxxxxxx), it is fake. Official bank messages never come from personal mobile numbers.
2. **Examine the Link:** Look at the web link in the text. If it does not end with the official bank domain (like `.sbi` or `.com` with correct spelling), do not touch it. Watch out for domains like `sbi-update-kyc.net`.
3. **Read SMS carefully:** If you receive an OTP SMS, read the text description first. Verify if it says "OTP for transaction of [Amount]" instead of "Verification Code".
4. **Do Not Call numbers listed in SMS:** If the text says "Call officer at 98xxxxxxx," do not call that number. Call the official bank customer support number listed on your debit card or the bank's official website.
5. **Block and Report:** Block the sender on your phone. Report the SMS to TRAI by forwarding the message to **1909** or using the DND App.

---

## Safety Tips
- **Keep DND (Do Not Disturb) Active:** Register for full DND on your SIM to block unregistered telemarketers.
- **Never click links to update KYC:** No bank or telecom operator sends direct SMS links to update PAN cards, Aadhaar cards, or bank records. KYC updates always happen inside official banking portals or physical branches.
- **Use Official Apps for Bill Payments:** Pay electricity, water, and gas bills only through official apps (like Paytm, GPay, PhonePe, or the official utility portal) instead of clicking SMS payment links.

---

## Common Mistakes
- **Clicking Links to Check "Free Prizes":** Clicking on lottery wins, job offers, or free gift card links received from random SMS.
- **Believing "Account Blocked" Alerts:** Panic-clicking links in messages that threaten instant account deactivation.
- **Entering card details for verification:** Inputting sensitive card PINs or CVVs on websites reached through text links.

---

## Frequently Asked Questions
1. **What is smishing?** Phishing conducted via SMS text messages to steal bank and card details.
2. **How does smishing differ from email phishing?** Smishing uses SMS or chat apps; phishing uses email messages.
3. **Are messages from 10-digit numbers claiming to be banks real?** No, banks in India are required to use registered alphabetic headers, not 10-digit personal numbers.
4. **What is a header?** The sender name displayed at the top of an SMS (e.g., AX-AXISBK).
5. **Can clicking a link in an SMS download a virus?** Yes, it can trigger automatic downloads of malicious APK files on Android phones.
6. **How do I report spam SMS?** Forward the SMS to **1909** in the format: "Spam text, Sender ID, Date" or use the TRAI DND app.
7. **What is the 1930 helpline?** The national cyber crime helpline for reporting financial frauds.
8. **Why do scammers send fake electricity bill alerts?** Because it causes instant panic, making the victim call the fake officer's number immediately.
9. **Can scammers steal money if I only click the link but don't enter anything?** Usually no, but they can identify that your number is active and download adware/spyware.
10. **Do banks send WhatsApp messages for KYC?** No, banks do not conduct KYC verifications or ask for documents on WhatsApp chats.
11. **What is a short URL?** A compressed link (like bit.ly) used to hide the destination of a fake website.
12. **Can I block SMS from unknown senders?** Yes, you can enable spam protection settings in your phone's default messaging app.
13. **Is it safe to reply to a smishing SMS?** No, do not reply, as it confirms to the scammer that your number is active and monitored.
14. **What is TAFCOP?** A government portal to check how many mobile connections are active in your name.
15. **Does the bank compensate for losses due to smishing links?** If the user voluntarily entered their password and OTP on the link, it is evaluated as customer negligence. Report immediately to 1930 to freeze the money.
16. **Why do I receive SMS alerts for cash debit when my card is at home?** Your card details were compromised online, or your card has been cloned. Block the card instantly.
17. **Can a smishing link hack my WhatsApp?** Yes, if the link tricks you into entering a WhatsApp verification code or downloading spyware.
18. **Do telecom operators block fake SMS headers?** Yes, TRAI uses blockchain-based systems (DLT) to filter unauthorized headers, though scammers bypass this using personal numbers.
19. **What is the penalty for SMS fraud in India?** Imprisonment and fines under the IT Act (Section 66D).
20. **Should I delete the smishing SMS after blocking?** Keep a screenshot of the message for reporting to the Cyber Cell, then delete it.

---

## Common Myths vs Facts
1. **Myth:** If the SMS is in my default inbox, it must be from a verified bank. **Fact:** Scammers can bypass default filters using bulk SMS gateways; keep check on headers.
2. **Myth:** Official banks use WhatsApp to update user details. **Fact:** Banks only use WhatsApp for automated updates (balance checks, statements) but never for updating passwords or KYC details.
3. **Myth:** Clicking a link requires entering a PIN to deduct money. **Fact:** Malicious links can trigger silent malware installs that read future OTPs automatically.
4. **Myth:** Scammers cannot spoof bank headers anymore. **Fact:** While blockchain filters are strict, scammers find loopholes or use headers that look similar (e.g., AD-HDFCBK vs AD-HDFCBP).
5. **Myth:** I won a lottery because the SMS came from a government number. **Fact:** Government departments never run lottery contests via SMS. All such alerts are fake.
6. **Myth:** Forwarding spam to 1909 blocks the scammer's bank account. **Fact:** 1909 blocks the telemarketer's SMS capabilities. Freezing bank accounts requires calling 1930.
7. **Myth:** Standard BSBDA/Jan Dhan accounts do not receive spam. **Fact:** Scammers send bulk messages blindly; they do not know your account type initially.
8. **Myth:** If a text link begins with https://, it is 100% safe. **Fact:** Scammers easily get free security certificates for their fake sites, showing the https logo.
9. **Myth:** Banks send links to download mobile banking apps in SMS. **Fact:** It is safer to search and download banking apps directly from the official Google Play Store or Apple App Store.
10. **Myth:** The cyber cell cannot trace SMS senders. **Fact:** Senders can be traced through SMS gateway logs and tower locations.

---

## Conversation Examples
1. **User:** Mujhe SMS aaya hai ki 'SBI Account suspended. Click link to update Aadhaar'. Kya ye asli hai?
   **Assistant:** Ye bilkul fake smishing message hai. SBI ya koi bhi bank email/sms me direct link dekar Aadhaar update karne ko nahi kehta. Is link par click na karein aur message delete kar dein.
2. **User:** Dukandar bol raha hai ki SMS me aayi link se payment karein, kya ye safe hai?
   **Assistant:** Agar link kisi trusted payment gateway (jaise Razorpay, BillDesk) ki hai toh verify karke pay kar sakte hain. Par verify karein ki amount aur merchant name sahi dikh raha hai. Random text links se bachein.
3. **User:** Bijli vibhag (Electricity Board) ke naam par message aaya hai ki bill nahi bhara toh aaj raat light kat jayegi. Kya main call karu?
   **Assistant:** Ye ek bahut common fraud SMS hai. Bijli vibhag ke messages kabhi bhi 10-digit personal number se nahi aate aur na hi direct number par call karne ko kehte hain. Apne electricity bill ka status official app (jaise GPay, Paytm) par check karein.
4. **User:** Maine SMS link par click kiya par koi detail fill nahi ki. Kya mera bank account khali ho sakta hai?
   **Assistant:** Agar aapne login details, password ya OTP enter nahi kiya hai, toh aap safe hain. Phir bhi, security ke liye ek baar antivirus scanner run karein taaki check ho sake koi fake app background me install toh nahi hui.
5. **User:** TRAI 1909 kya hai?
   **Assistant:** 1909 ek national helpline hai jahan aap spam messages aur calls ki DND (Do Not Disturb) complaint file kar sakte hain. Aap is number par SMS bhejkar telemarketer ko block karwa sakte hain.
6. **User:** WhatsApp par 'KBC Lottery' ka message mila hai jisme check ki photo hai.
   **Assistant:** Ye poori tarah se fake lottery scam hai. KBC ya koi bhi government body aise lottery messages nahi bhejti. Ye aapse process fee ke naam par paise thagne ki koshish hai. Number block karein.
7. **User:** OTP message me 'debit' likha tha par maine socha registration code hai, kya karu?
   **Assistant:** Agar paise kat gaye hain, toh turant bank customer care ko call karke card block karein aur 1930 Cyber Fraud Helpline par shikayat darj karwayein taaki paisa freeze kiya ja sake.
8. **User:** SMS header 'AD-SBIIN' aur number '+91-98xxxxxxx' me kya difference hai?
   **Assistant:** 'AD-SBIIN' ek registered corporate header hai jo bank ka hai, jabki '+91-98xxxxxxx' ek normal mobile number hai jiska use scammers bank ke naam par SMS bhejne ke liye karte hain.
9. **User:** Kya minor accounts par bhi spam SMS aate hain?
   **Assistant:** Haan, spam messages randomly bulk numbers par bheje jate hain. Bacchon ko sikhaayein ki kisi bhi SMS link par click na karein.
10. **User:** Telemarketer mere block karne ke baad bhi dusre ID se SMS bhej raha hai.
    **Assistant:** Aap TRAI ke DND App par iski shikayat register karein. DDLT system block rates badhne par telecom operators us operator portal ko suspend kar dete hain.
11. **User:** SMS link click karne par phone automatic hang ho gaya.
    **Assistant:** Phone ko restart karein aur settings me jaakar check karein koi anjan app (jaise AnyDesk, keylogger) install toh nahi ho gayi. Aise apps ko instantly delete karein.
12. **User:** Kya post office ke parcal delivery hold ka message real hota hai?
    **Assistant:** India Post aisi links nahi bhejta jahan update address ke liye debit card details maangi jayein. Ye smishing scam hai.
13. **User:** Income tax refund SMS me direct link diya hai, kya wahan details bharu?
    **Assistant:** Income tax department links ke zariye refunds process nahi karta. Refund status sirf official portal (incometax.gov.in) par login karke hi check kiya ja sakta hai.
14. **User:** UPI PIN register link aaya hai SMS me.
    **Assistant:** UPI PIN registration sirf aapke phone me trusted UPI apps ke andar hota hai, kisi web link par nahi. Link block karein.
15. **User:** DND portal registration kaise hota hai?
    **Assistant:** Aap apne phone se SMS type karein "START 0" aur use 1909 par send kar dein. Isse sabhi categories ke spam messages block ho jayenge.

---

## Government Services
- **TRAI DND App:** For managing and reporting spam SMS.
- **National Cyber Crime portal:** cybercrime.gov.in
- **Sanchar Saathi Portal:** sancharsaathi.gov.in

---

## Search Optimization
- **English Keywords:** Smishing SMS fraud prevention, fake electricity bill message safety, report spam sms 1909, block text message links, bank kyc update sms link, national cyber helpline 1930.
- **Hindi Keywords:** एसएमएस फ़िशिंग, फर्जी मैसेज लिंक, बिजली बिल भुगतान घोटाला, मोबाइल धोखाधड़ी शिकायत.
- **Hinglish Keywords:** kyc update link sms fake ya real, bank block sms alert check, spam message block kaise kare.
- **Synonyms:** Text phishing, SMS spam fraud, mobile link scam.
- **Abbreviations:** SMS, DND, TRAI, NCRP, UPI, KYC, RBI, GST, IVR, OTP.
- **Common Misspellings:** smising message, bank kyc link, electricity bill cut sms.
- **Regional Search Terms:** Kuru Seydhi Mosam (Tamil), SMS Donga (Telugu).

---

## Intent Mapping
- `definition`
- `fraud_help`
- `customer_rights`

---

## Retrieval Tags
smishing, SMS phishing, spam SMS, text message fraud, fake KYC SMS, account blocked alert link, electricity power cut scam, bit ly short URLs, TRAI header registration, alphabetic headers, 1909 DND complaints, cybercrime helpline 1930, National Cyber Crime portal, zero liability banking, transaction OTP check, PAN card link SMS, India Post parcel scam, TAFCOP portal, Sanchar Saathi check, SMS redirect virus, Android Trojan APK link.

---

## Cross References
- [banking/cyber_security/phishing.md](banking/cyber_security/phishing.md)
- [banking/cyber_security/vishing.md](banking/cyber_security/vishing.md)
- [banking/cyber_security/reporting_fraud.md](banking/cyber_security/reporting_fraud.md)
- [banking/customer_rights.md](banking/customer_rights.md)

---

## See Also
- digital_arrest.md
- upi_fraud.md
- remote_access_scam.md
- complaints.md

---

## References
- Telecom Regulatory Authority of India (TRAI) Directions on Blockchain-based DLT SMS systems.
- Reserve Bank of India (RBI) Safety Alerts on Smishing Schemes.
- Information Technology Act, 2000 (Section 66D - Punishment for cheating by personation).

---

## Banking Disclaimer
This document is for educational and informational purposes only and does not constitute technical or legal advice. SMS templates, notification frequencies, and telecom regulations are subject to change by TRAI and DoT. Always verify banking transaction alerts and contact official bank channels directly before acting on text messages.
