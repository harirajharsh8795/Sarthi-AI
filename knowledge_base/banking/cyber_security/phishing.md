---
id: phishing
title: Phishing (फ़िशिंग / नकली वेबसाइट घोटाला)
domain: banking
category: cyber_security
subcategory: personal_security
topic: phishing
version: 1.0
language: multilingual
difficulty: beginner
keywords: [phishing, fake website, fake email, link scam, banking fraud, steal password, secure browsing]
aliases: [email phishing, credential harvesting]
related_topics: [banking/cyber_security/smishing.md, banking/cyber_security/vishing.md, banking/cyber_security/reporting_fraud.md]
intent: [definition, fraud_help, customer_rights]
last_updated: 2026-07-19
author: Saarthi AI
sources: [Reserve Bank of India (RBI), Indian Computer Emergency Response Team (CERT-In)]
---

# Phishing (फ़िशिंग / नकली वेबसाइट घोटाला)

## Overview

### English
Phishing is a cyber-attack method where fraudsters use deceptive emails, messages, and fake websites that resemble legitimate organizations (such as banks, government portals, or utility companies) to trick users into revealing sensitive credentials like passwords, PINs, and card numbers.

### Hindi
फ़िशिंग (Phishing / नकली वेबसाइट घोटाला) एक साइबर-हमले की पद्धति है जिसमें जालसाज धोखाधड़ी वाले ईमेल, संदेशों और नकली वेबसाइटों का उपयोग करते हैं जो वैध संगठनों (जैसे बैंक, सरकारी पोर्टल या उपयोगिता कंपनियों) से मिलती-जुलती हैं, ताकि उपयोगकर्ताओं को पासवर्ड, पिन और कार्ड नंबर जैसे संवेदनशील क्रेडेंशियल प्रकट करने के लिए धोखा दिया जा सके।

### Hinglish
Phishing ek aisa cyber-attack hota hai jisme thag log aapko aisi fake emails, message links ya websites bhejte hain jo dikhne me bilkul asli bank ya company ki tarah lagti hain. Inka maqsad aapko dhoke me rakhkar aapka net banking password, debit card details ya login credentials churaana hota hai.

---

## Quick Summary
Phishing is one of the oldest and most effective forms of cyber theft. A typical phishing attack starts with an email or chat message containing a sense of urgency—for example, warning that your bank account will be blocked unless you click a link to verify your KYC details immediately.

When you click the link, it directs you to a fake login page that looks identical to your bank's official website. Any information you type there (customer ID, password, OTP) is captured by the attacker in real-time. Once they have these credentials, they log into your actual bank account and transfer your funds. Under RBI safety guidelines, checking the browser address bar for the correct domain spelling (e.g., matching the exact bank URL) and avoiding unsolicited links is the best protection.

---

## Definition
Phishing is a social engineering attack vector that utilizes electronic communication mediums to spoof trusted identities, misleading targets into executing malicious payloads or submitting sensitive account data on attacker-controlled landing pages.

---

## Why It Matters
Preventing phishing is essential for all internet banking users because:
- **Major Gateway to Cyber Theft:** Over 80% of banking security incidents start with a phishing link.
- **Protects Identity:** Stolen credentials can be used not just to steal money, but also to commit identity fraud or borrow loans in your name.
- **Bypasses Technical Barriers:** Phishing targets human psychology (fear, greed) rather than hacking the bank's highly secure core servers, making awareness the only real shield.

---

## How It Works
The standard execution flow of a Net Banking Phishing attack:

Fraudster sends email pretending to be the Bank: "Urgent: Update KYC or account gets suspended."
↓
Email contains a link: "Click here to login and update KYC."
↓
Customer clicks link; browser opens a spoofed website (e.g., www.sbi-kycupdate.com instead of official portal)
↓
Customer inputs Customer ID and Net Banking Password on the fake login page
↓
Fake page captures details and displays: "Enter OTP sent to your mobile to complete update."
↓
Simultaneously, the fraudster logs into the real bank website using the stolen ID and password, triggering a real transaction OTP
↓
Customer enters the OTP on the fake website
↓
Fraudster captures the OTP, enters it on the real bank website, and completes the theft

---

## Eligibility
- **Targets:** Any individual using digital banking channels, net banking portals, e-wallets, or online payment applications.

---

## Required Documents
- **Not Applicable:** For reporting phishing attempts, you should gather:
  - Screenshot of the phishing email showing the sender's email address.
  - The exact URL link of the fake website.
  - Screenshots of transactions (if money was stolen).
  - Copy of the complaint filed on the cybercrime portal.

---

## Features
- **Email Spoofing:** Altering the email header to make the message appear as if sent by the bank.
- **Domain Name Spoofing:** Registering website domains with minor spelling variations (e.g., 'hdfcbankk' or 'icicicb').
- **Urgent Call-to-Actions:** Messages demanding immediate updates to prevent account suspension, tax penalties, or credit card blocks.

---

## Benefits of Safety Knowledge
- **Early Detection:** Recognizing spelling errors in domains and sender email IDs instantly.
- **Data Protection:** Preventing credential loss by using dedicated mobile apps instead of browser links for transactions.

---

## Risks
- **Account Takeover:** Criminals gaining complete control of your bank accounts, modifying registered contact details, and locking you out.
- **Unauthorized Loans:** Fraudsters using your compromised credentials to apply for pre-approved personal loans, withdrawing the cash instantly.
- **Malware Infection:** Clicking phishing links can download spyware/keyloggers onto your computer, recording all future keystrokes.

---

## Charges & Fees
- **Fraud Reporting:** Nil.

---

## RBI / Government Rules
- **Mandatory Safe Browsing Guidelines:** Banks are required to display clear warnings on their login pages, cautioning users about phishing scams.
- **Zero Liability Protection:** If a phishing incident occurs due to bank system breaches, the customer faces zero liability. However, if the customer voluntarily enters details on a phishing link, they may have to bear the loss until they report the incident and block the account.
- **Immediate Website Take-downs:** Indian cybersecurity agencies (like CERT-In) coordinate with domain registrars to block and take down reported phishing links rapidly.

---

## Step-by-Step Process

### How to Identify a Phishing Website:
1. **Check the Domain Name:** Look closely at the browser address bar. Banks use clear, simple domains (e.g., `onlinesbi.sbi` or `hdfcbank.com`). Watch out for additions like `-verify`, `-update`, or extension changes like `.org`/`.net` instead of `.com`.
2. **Check for HTTPS:** Look for the lock icon in the address bar. However, be aware that modern phishing sites also use HTTPS to look secure. The domain name spelling remains the most critical check.
3. **Verify Sender Email ID:** Do not trust the sender name (e.g., "ICICI Bank"). Hover over or tap the sender name to see the actual email address (e.g., `support@icici-kycdepartment-india.com` is fake; official emails come from domains ending in `@icicibank.com`).
4. **Use Bookmarks:** Never click links in emails or search engine results to open net banking. Always type the URL manually or use saved browser bookmarks.
5. **Report Immediately:** If you spot a fake bank page, email the details to the bank's abuse desk (e.g., `abuse@bankname.com`) and cyber crime cell.

---

## Safety Tips
- **Use Multi-Factor Authentication (MFA):** Enable token/OTP or biometric logins for all banking services.
- **Never click KYC Links:** Banks never ask you to update KYC, personal info, or pan cards through email/SMS links. KYC updates are done inside branch offices or through secure video KYC on official bank apps.
- **Keep Browser Updated:** Keep your internet browser (Chrome, Firefox, Edge) updated, as they contain built-in protection databases that block known phishing sites.

---

## Common Mistakes
- **Trusting Search Engine Ads:** Clicking on the top sponsored search results on Google for your bank's login page. Scammers often run ads to place phishing sites at the top of search listings.
- **Entering OTP without Reading Message:** Entering the OTP received on your phone onto a website without reading the SMS text, which may say "OTP for transfer of ₹10,000" instead of "OTP for login."
- **Replying to Deceptive Mails:** Sending password details via email response to "customer care" representatives claiming they need it to reset your account.

---

## Frequently Asked Questions
1. **What is phishing?** A cyber attack where scammers use fake emails or websites to steal your bank passwords and card details.
2. **What is the difference between phishing and smishing?** Phishing uses emails or websites; Smishing uses SMS messages containing fraud links.
3. **How do I know if an email is really from my bank?** Check the sender's actual email domain (after the '@' symbol). Official bank emails only come from official bank domains.
4. **Can a phishing website steal my money without an OTP?** If you enter your card details, scammers can use them on international websites that do not require OTP verification.
5. **What should I do if I clicked a phishing link but didn't enter details?** You are generally safe, but perform a full antivirus scan on your device to check for malware downloads.
6. **What if I entered my net banking password on a fake site?** Log into the official bank website immediately and change your password. If you cannot log in, contact customer care to freeze your account.
7. **Do banks ask for passwords via email?** No, banks never ask for passwords, PINs, or CVVs via email or phone call.
8. **Why do phishing sites look exactly like bank sites?** Scammers copy the HTML code and logos of real bank websites to make their fake versions look identical.
9. **Is HTTPS in the address bar a guarantee of a safe site?** No, scammers can get free SSL certificates for their fake domains. Always verify the domain spelling.
10. **Where do I report a phishing email?** Send it to your bank's official security/abuse email ID (e.g., abuse@hdfcbank.com) and register a complaint at cybercrime.gov.in.
11. **What is spear phishing?** A targeted phishing attack directed at a specific individual or company, using customized personal details to sound authentic.
12. **Can phishing happen on WhatsApp?** Yes, scammers send fake lottery or job offer links on WhatsApp to steal credentials.
13. **Are zero-balance account holders targets for phishing?** Yes, scammers target all bank account holders.
14. **What is a look-alike domain?** A website name that has minor spelling mistakes to trick users (e.g., paytmm.com instead of paytm.com).
15. **Does antivirus software protect against phishing?** Yes, many antivirus programs have web shields that block known phishing pages.
16. **Why did the bank block my access after a phishing report?** For security, to prevent fraudsters from taking out money while they investigate.
17. **What is the Cyber Cell helpline number?** 1930.
18. **Can I recover my money if lost through phishing?** Yes, if you block your account and report the transaction to the bank and Cyber Cell (1930) immediately (within 2-3 hours).
19. **What is social engineering?** The psychological manipulation of people into performing actions or divesting confidential information.
20. **How do banks secure online logins?** By using virtual keyboards, secure login captchas, and OTPs.

---

## Common Myths vs Facts
1. **Myth:** Phishing only happens to uneducated people. **Fact:** Phishing attacks are highly sophisticated; even IT professionals and bank employees fall victim to smart scams.
2. **Myth:** If I don't click on any link, I can't get phished. **Fact:** True, but you can also get phished by downloading attachments (like fake bills) that contain keyloggers.
3. **Myth:** Google search results are always safe. **Fact:** Scammers run paid search ads that appear above organic results, linking directly to phishing sites.
4. **Myth:** Banks send emails asking you to check account security links. **Fact:** Banks will only advise you to visit their official app or website; they never include direct login links in emails.
5. **Myth:** A site is safe if it has the bank's logo. **Fact:** Logos are easily copied. Trust only the domain URL in the browser address bar.
6. **Myth:** I can check the fake site's ownership on WHOIS. **Fact:** You can, but it is faster to check the domain spelling; fake sites are registered recently under private names.
7. **Myth:** Phishing links only steal banking data. **Fact:** Phishing is also used to steal social media logins, official corporate emails, and government IDs.
8. **Myth:** If I close the page quickly, my details are safe. **Fact:** If you already typed your details and clicked 'submit', the data was sent to the hackers.
9. **Myth:** Once a phishing site is blocked, the scam stops. **Fact:** Scammers instantly launch the same fake page on a different domain. Vigilance is key.
10. **Myth:** Banks cover all phishing losses under insurance. **Fact:** Banks only cover losses due to their own technical failures. Customer negligence (entering OTP/passwords on links) is generally not covered unless reported under zero liability timelines.

---

## Conversation Examples
1. **User:** Mujhe HDFC Bank ke naam par ek mail aaya hai ki mera account block hone wala hai, isme KYC update karne ka link hai. Kya karu?
   **Assistant:** Ye ek phishing email hai. Bank kabhi bhi account block karne ki dhamki dekar email par KYC link nahi bhejte. Is link par click na karein, ise block karein aur bank ke abuse desk par report karein.
2. **User:** Maine galti se ek website par apna customer ID aur password daal diya. Ab mujhe darr lag raha hai.
   **Assistant:** Turant bank ki official website par login karein aur apna password badal (change) dein. Agar aap login nahi kar paa rahe hain, toh customer care ko phone karke apna account instantly freeze/block karwayein.
3. **User:** Website safe hai ya nahi, ye kaise check karein?
   **Assistant:** Browser ke address bar me check karein ki spelling bilkul sahi hai ya nahi (jaise online.sbi na ki online-sbi-update.com). Sath hi bank ki website ka address hamesha khud type karein, Google search ads par click na karein.
4. **User:** OTP SMS me likha tha 'Transaction of 5000' par maine bina padhe website par daal diya. Refund kaise milega?
   **Assistant:** Ghabraiye nahi, sabse pehle 1930 Cyber Helpline par call karke fraud report karein aur bank se contact karke card block karein. Kyunki aapne OTP khud enter kiya, ye customer negligence me aata hai, par jaldi report karne par transaction hold ho sakta hai.
5. **User:** Spear phishing kya hoti hai?
   **Assistant:** Spear phishing me scammers kisi specific vyakti ko target karte hain. Wo aapka naam, company ya family details churaakar aisi customized mail bhejte hain jisse aapko lage ki ye bilkul asli hai.
6. **User:** Bank ka security warning message aane laga hai browser par.
   **Assistant:** Iska matlab hai ki aapke browser ne us website ko phishing page detect kar liya hai. Turant us tab ko close karein aur wahan koi details na dalein.
7. **User:** Net banking password kitne din me badalna chahiye?
   **Assistant:** Har 3 se 6 mahine me aapko apna net banking password badalna chahiye aur use bilkul random banana chahiye (jaise numbers, characters aur symbols ka use karke).
8. **User:** Kya WhatsApp par aane wale job offers phishing hote hain?
   **Assistant:** Haan, aamtaur par aisi links jo bade salaries ka lalach deti hain aur registration ke liye card details maangti hain, phishing scams hoti hain.
9. **User:** KYC update karne ke liye bank kab link bhejta hai?
   **Assistant:** Bank kabhi bhi sms/email me direct link dekar KYC update karne ko nahi kehta. KYC update bank app ke andar secure portal par ya bank branch jaakar hi hota hai.
10. **User:** Mujhe lagta hai mera email hack ho gaya hai, kya mera bank account safe hai?
    **Assistant:** Agar aapka email banking account se linked hai, toh fraudsters password change kar sakte hain. Bank me phone karke email and mobile verification channels check karein aur email ka password turant badlein.
11. **User:** Mobile app par phishing ho sakti hai?
    **Assistant:** Mobile app stores par kuch fake clone apps ho sakti hain jo asli banking app jaisi dikhti hain. Hamesha verified developer (bank official developer) ka app hi download karein.
12. **User:** Browser me auto-save passwords rakhna safe hai?
    **Assistant:** Banking passwords ko browser me auto-save na karein. Agar aapka device kisi ke hath lag gaya, toh wo asani se net banking open kar sakta hai.
13. **User:** Income tax department ke naam par refund mail aayi hai.
    **Assistant:** Ye bhi ek common phishing attack hai. Tax refunds direct aapke registered bank account me aate hain; department kisi link par card details fill karne ko nahi kehta. official portal (incometax.gov.in) par login karke check karein.
14. **User:** Phishing complaints ke liye kya cyber police station jana padega?
    **Assistant:** Pehli report aap 1930 call karke ya cybercrime.gov.in par online de sakte hain. Agar nuksan bada hai, toh cyber cell police station me copy submit karna behtar hoga.
15. **User:** Kya transaction fee lagti hai agar bank dispute investigate karein?
    **Assistant:** Nahi, dispute registration aur investigation process completely free hai.

---

## Government Services
- **CERT-In (cert-in.org.in):** Cyber emergency response portal for reporting phishing sites.
- **National Cyber Crime Portal:** For lodging official complaints.
- **Telecom Regulatory Authority of India (TRAI):** For reporting spam messages.

---

## Search Optimization
- **English Keywords:** Net banking phishing scam, fake bank login website, identify phishing email address, recover account from phishing hack, cybercrime complaint online, rbi customer protection rules.
- **Hindi Keywords:** फ़िशिंग घोटाला, फर्जी बैंक वेबसाइट पहचान, ऑनलाइन धोखाधड़ी शिकायत, पासवर्ड चोरी समाधान.
- **Hinglish Keywords:** phishing link click ho gaya kya kare, bank name spelling mistake website, otp safety rules.
- **Synonyms:** Email spoofing, web page cloning, digital identity theft.
- **Abbreviations:** CERT, TRAI, MFA, OTP, PIN, CVV, SSL, HTTPS, RBI, GST.
- **Common Misspellings:** phising mail, fake bank log in, hdfc kyc link.
- **Regional Search Terms:** Vala Veesi Pidithal (Tamil), Phishing Vala (Telugu).

---

## Intent Mapping
- `definition`
- `fraud_help`
- `customer_rights`

---

## Retrieval Tags
phishing scam, fake bank website, email spoofing, fake email alert, KYC update scam link, net banking credential theft, domain name spoofing, check domain spelling, browser secure lock icon, look alike domain, CERT In reporting, cybercrime portal, cyber cell helpline 1930, zero liability customer protection, shadow reversal credit, multi factor authentication, browser safety updates, spear phishing, WhatsApp link scam, online password security.

---

## Cross References
- [banking/cyber_security/smishing.md](banking/cyber_security/smishing.md)
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
- Indian Computer Emergency Response Team (CERT-In) Advisory on Phishing Attacks.
- Reserve Bank of India (RBI) Cyber Security Framework for Banks.
- Information Technology Act, 2000 (Section 66D - Punishment for cheating by personation by using computer resource).

---

## Banking Disclaimer
This document is for educational and informational purposes only and does not constitute technical or legal advice. Online portal designs, abuse reporting mailboxes, and security architectures vary by bank. Always log into your banking accounts by manually typing the official domain address directly in the browser address bar.
