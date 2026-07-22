---
id: sim_swap
title: SIM Swap Fraud (सिम स्वैप धोखाधड़ी)
domain: banking
category: cyber_security
subcategory: personal_security
topic: sim_swap
version: 1.0
language: multilingual
difficulty: beginner
keywords: [SIM swap fraud, duplicate SIM card, phone signal loss, OTP theft, phone hijacking, telecom scam, identity theft]
aliases: [sim split fraud, duplicate sim card scam]
related_topics: [banking/cyber_security/phishing.md, banking/cyber_security/reporting_fraud.md, banking/customer_rights.md]
intent: [definition, fraud_help, customer_rights]
last_updated: 2026-07-19
author: Saarthi AI
sources: [Reserve Bank of India (RBI), Department of Telecommunications (DoT)]
---

# SIM Swap Fraud (सिम स्वैप धोखाधड़ी)

## Overview

### English
SIM Swap fraud is a type of identity theft where criminals trick a telecom operator into deactivating a victim's active SIM card and issuing a duplicate SIM card in the victim's name. This allows the fraudster to intercept all SMS-based banking alerts, OTPs, and login codes.

### Hindi
सिम स्वैप धोखाधड़ी (SIM Swap Fraud) एक प्रकार की पहचान की चोरी (identity theft) है जिसमें अपराधी दूरसंचार ऑपरेटर (telecom operator) को धोखा देकर पीड़ित के सक्रिय सिम कार्ड को निष्क्रिय कर देते हैं और पीड़ित के नाम पर एक नया डुप्लिकेट सिम कार्ड जारी करवा लेते हैं। यह जालसाज को बैंक एसएमएस (SMS) अलर्ट, ओटीपी (OTP) और लॉगिन कोड प्राप्त करने की अनुमति देता है।

### Hinglish
SIM Swap fraud ek aisa identity theft scam hai jise duplicate SIM card chori bhi kehte hain. Isme fraudsters telecom company (jaise JIO, Airtel) ko jhooti report karke aapka chal raha SIM block karwa dete hain aur aapke naam par naya duplicate SIM card nikalwa lete hain. Iske baad aapke phone ka signal gayab ho jata hai aur aapke bank transactions ke saare SMS aur OTPs fraudsters ke phone par aane lagte hain, jisse wo aapka account khaali kar dete hain.

---

## Quick Summary
SIM swap fraud is a two-step attack. First, the fraudster gathers the victim's personal details (Aadhaar number, full name, date of birth, and bank account number) through phishing links, fake emails, or data leaks. Once they have this information, they create forged ID proofs with the victim's details but their own photograph.

In the second step, the fraudster visits a telecom retail store, pretending to be the victim, and reports that their phone/SIM is lost. They submit the forged ID and apply for a replacement SIM card. The operator verifies the documents and activates the new SIM card, which automatically deactivates the victim's original SIM. The victim's phone loses all network signals, which they often mistake for a temporary network issue. During this offline period, the fraudster uses the stolen bank credentials and the new SIM to execute transfers and receive the authentication OTPs.

---

## Definition
SIM Swap Fraud is the unauthorized porting or duplicate issuance of a subscriber's mobile identity (IMSI) to a second physical SIM card controlled by an attacker, executed through social engineering of mobile network operators, for the purpose of defeating SMS-based two-factor authentication (2FA).

---

## Why It Matters
Understanding SIM swap fraud is vital because:
- **Bypasses Two-Factor Authentication:** SMS-based OTP is the primary security layer for net banking and UPI in India. A SIM swap bypasses this layer completely, rendering passwords useless.
- **Silent Threat Execution:** The attack is executed when the victim's phone is offline, meaning they receive no SMS alerts about money being debited.
- **Requires telecom vigilance:** Recognizing that sudden, unexplained loss of network coverage is an emergency indicator rather than a casual glitch.

---

## How It Works
The standard execution pathway of a SIM Swap fraud:

Fraudster steals victim's bank details and ID info (via phishing/social engineering)
↓
Fraudster creates forged ID card (e.g., Aadhaar card with victim's data but fraudster's photo)
↓
Fraudster visits a mobile operator shop and requests a replacement SIM card, claiming the old one is lost
↓
Mobile operator activates the new SIM card; victim's SIM card automatically loses connection
↓
Victim's phone displays: "No Service" or "Emergency Calls Only"
↓
Fraudster inserts the new duplicate SIM into their phone
↓
Fraudster initiates fund transfers on victim's bank account online
↓
Transaction OTP is sent by the bank and received directly on the fraudster's phone
↓
Fraudster inputs OTP, completes transaction, and empties the account

---

## Eligibility
- **Targets:** Anyone who uses SMS-based OTPs for validating net banking, mobile banking, UPI, or e-wallets.

---

## Required Documents
- **Not Applicable:** For reporting SIM swap fraud, gather:
  - Last active timestamp of your SIM card.
  - The telecom operator's store visit record or service request ID.
  - Bank account statement showing fraudulent transfers.
  - Cyber Crime complaint copy from cybercrime.gov.in.

---

## Features
- **Identity Forgery:** Creation of replica Aadhaar or Voter IDs.
- **Telecom Mimicry:** Social engineering operator customer care agents to bypass security checks.
- **Automatic Deactivation:** Instantly deactivating the victim's network signal.
- **2FA Interception:** Reading OTP codes for net banking and social media account takeovers.

---

## Benefits of Safety Knowledge
- **Early Glitch Detection:** Prompts customers to check status with telecom providers immediately after losing signal.
- **Immediate Account Lock:** Teaches victims to freeze bank accounts before the duplicate SIM is fully activated.

---

## Risks
- **Total Financial Depletion:** Transfer of large sums from savings, fixed deposits, and linked credit cards.
- **Identity Lockout:** Hijackers can change passwords on email and social media accounts linked to the mobile number, locking you out permanently.
- **Lengthy Resolution Time:** Telecommunication disputes and network audits take time, delaying credit reversals.

---

## Charges & Fees
- **Fraud Reporting & Telecom Complaints:** Nil.

---

## RBI / Government Rules
- **DoT Guidelines on SIM Replacement:** The Department of Telecommunications (DoT) mandates that when a duplicate SIM card is issued, SMS services (incoming and outgoing) must be blocked on the new SIM for 24 hours to prevent immediate financial fraud.
- **Notification Requirement:** Telecom operators must send an automated IVR call or SMS warning to the active SIM card notifying them of a duplicate SIM request before deactivating the connection.
- **Zero Liability Timeline:** Under RBI guidelines, the liability freeze applies once the user contacts the bank to report the compromise.

---

## Step-by-Step Process

### What to do if your mobile signal suddenly vanishes:
1. **Wait and Check:** If the signal is gone for more than 15-20 minutes in a place where you normally get network, do not assume it is a temporary glitch.
2. **Restart Phone:** Restart your phone. If it still shows "No Service" or "SIM not provisioned," try inserting the SIM into another phone.
3. **Contact Telecom Operator:** Call your telecom operator's customer care from another phone, or visit the nearest official outlet immediately. Ask them to verify: *Is my SIM active, or has a duplicate SIM replacement request been processed?*
4. **Request Account Freeze:** If they confirm a replacement was processed without your request, tell them to block the SIM immediately. Next, contact your bank customer care to freeze all net banking, UPI, and card channels.
5. **Report to Cyber Cell:** Dial **1930** or visit **cybercrime.gov.in** to report the SIM swap fraud.
6. **Change Passwords:** Once your network is restored (on a new SIM), log in and change all your online banking passwords.

---

## Safety Tips
- **Monitor Signal Disruptions:** Treat sudden "No Service" alerts on your phone with high urgency.
- **Do not share personal info on social media:** Avoid posting your phone number, date of birth, and email address on public social media platforms.
- **Link Email Alerts:** Always register your active email address with your bank so you receive email receipts for transactions even if your phone is offline.
- **Inquire about SIM lock:** Ask your operator if they support adding a custom PIN/password requirement for any SIM replacement requests.

---

## Common Mistakes
- **Ignoring Signal Loss for Days:** Assuming a "No Service" status over a weekend is just a network issue, allowing fraudsters two full days to execute transfers.
- **Falling for Phishing KYC Calls:** Sharing Aadhaar number and OTP to callers claiming to verify your JIO/Airtel network connection.
- **Not checking email statements:** Neglecting to check email notifications during a phone network blackout.

---

## Frequently Asked Questions
1. **What is SIM swap fraud?** A scam where criminals get a duplicate SIM card issued in your name to receive your bank OTPs.
2. **How does my SIM get deactivated?** Once the telecom company activates the new duplicate SIM requested by scammers, your old SIM loses network automatically.
3. **What are the warning signs of SIM swap fraud?** Sudden, prolonged loss of mobile network signal ("No Service") accompanied by an inability to make calls.
4. **How do scammers get my ID proofs?** Through phishing emails, fake KYC update sites, or databases leaked online.
5. **Does the new SIM card receive my bank alerts immediately?** Yes, once activated, all incoming SMS messages (OTPs, notifications) go to the new SIM.
6. **What is the DoT 24-hour SMS rule?** A rule mandating that telecom operators must block SMS services for 24 hours on newly issued replacement SIM cards to prevent instant fraud.
7. **Can I use UPI if my SIM is swapped?** No, because UPI requires SMS validation from your registered number. Scammers, however, can set up UPI on their devices using the duplicate SIM.
8. **What is the cybercrime helpline number?** 1930.
9. **Can scammers execute transfers without my net banking password?** If they have your SIM, they can click "Forgot Password" on the banking portal and reset it using the OTP sent to the mobile number.
10. **How do I verify if a duplicate SIM was issued?** By calling your mobile network provider's customer support from another phone or visiting their gallery.
11. **Do banks compensate for SIM swap fraud?** If you prove you reported the signal loss and bank compromise quickly, and the bank/telecom failed in security checks, you are covered under RBI's customer protection guidelines.
12. **Is SIM swap different from SIM cloning?** Yes, cloning duplicates the card physically using a writer device; swap uses the operator system to transfer the number to a new card.
13. **Can I lock my SIM card?** Yes, you can set a SIM card PIN in your phone settings, which prevents the SIM from being used if physically stolen.
14. **Why do telecom stores issue duplicate SIMs easily?** Scammers use highly authentic-looking forged documents and exploit weak verification protocols at retail franchise stores.
15. **Does changing my email password help?** Yes, as it stops scammers from accessing email-based transaction alerts.
16. **How long does it take for a new SIM to activate?** Typically 2 to 4 hours after submitting the request at the store.
17. **Can a payments bank account be hacked via SIM swap?** Yes, payments banks are heavily dependent on mobile numbers, making them highly vulnerable to SIM swaps.
18. **Can I report SIM swap fraud online?** Yes, at cybercrime.gov.in.
19. **What is biometric SIM verification?** A system where telecom operators verify your thumbprint before issuing a replacement SIM card.
20. **Should I register a secondary mobile number with my bank?** If your bank supports it, you can add an alternate contact or email for notifications.

---

## Common Myths vs Facts
1. **Myth:** SIM swap can happen without any ID proofs. **Fact:** Telecom operators require ID verification to issue a replacement SIM. Scammers must produce fake or stolen ID copies of the victim.
2. **Myth:** If I lock my phone screen, my SIM is safe from swapping. **Fact:** Swapping happens at the telecom operator level, not on your physical phone device. Locking your phone does not prevent a swap.
3. **Myth:** Scammers need my physical SIM card to swap it. **Fact:** No, they do not need your physical SIM card. They only need to get a new blank SIM card activated with your number.
4. **Myth:** The 24-hour SMS block does not apply to private telecom companies. **Fact:** The 24-hour incoming SMS block on replaced SIM cards is a mandatory rule issued by DoT for all telecom operators in India.
5. **Myth:** Banks cannot track if my SIM was swapped. **Fact:** Many banks check the SIM card IMSI number during mobile banking logins to detect if the SIM has been recently replaced.
6. **Myth:** Scammers can listen to my private phone calls. **Fact:** Once swapped, they receive all calls and messages meant for you, while you receive none.
7. **Myth:** Using WhatsApp is safe during a SIM swap. **Fact:** Scammers can register WhatsApp on their phone using the OTP received on the swapped SIM, taking control of your chat history.
8. **Myth:** SIM swap only happens to high-profile targets. **Fact:** It can happen to any bank customer whose personal data is leaked online.
9. **Myth:** You must pay a fee to telecom operators to report a fraudulent swap. **Fact:** Reporting fraud and blocking services is completely free.
10. **Myth:** A factory reset of my phone will recover the signal. **Fact:** Signal loss is due to network deactivation; formatting the phone will not restore network signal.

---

## Conversation Examples
1. **User:** Mere mobile par 'No Service' likha aa raha hai pichle 2 ghante se. Kya ye normal hai?
   **Assistant:** Ye SIM Swap fraud ka sanket ho sakta hai. Agar restart karne par bhi signal nahi aata, toh turant kisi aur ke phone se apne telecom operator ke customer care ko call karein aur check karein ki kya aapke number par koi duplicate SIM issue toh nahi hui hai.
2. **User:** Scammer ne mere name par duplicate SIM nikalwa li hai, ab main bank accounts ko kaise bachau?
   **Assistant:** Bina ek minute gawaye apne bank ke customer care par call karein aur unhe request karein ki aapke bank accounts aur net banking ko instantly freeze (lock) kar dein taaki koi transfer na ho sake.
3. **User:** SIM swap fraud me fraudsters ko bank details kaise pata chalti hain?
   **Assistant:** Wo pehle se aapko phishing mails, fake KYC calls ya public leaked databases se aapki details (account number, login ID) chura lete hain. SIM swap toh sirf banking OTP pane ke liye kiya jata hai.
4. **User:** Telecom companies duplicate SIM dete waqt verification nahi karti kya?
   **Assistant:** DoT ke rules ke tehat biometric verification ya ID validation zaroori hai. Par fraudsters duplicate ID cards me apni photo laga kar retail stores ko dhoka de dete hain.
5. **User:** Naye SIM card par SMS kab tak band rehta hai?
   **Assistant:** Government guidelines ke mutabik naye replacement SIM card par active hone ke baad pehle 24 ghante tak incoming aur outgoing SMS services blocked rehti hain taaki fraud ko roka ja sake.
6. **User:** Mujhe WhatsApp par message aaya ki aapka SIM card update karein aur details fill karein.
   **Assistant:** Ye fake link hai. Telecom companies WhatsApp par direct links dekar details nahi mangti. Is link par details na fill karein, ye SIM swap fraud ki shuruat ho sakti hai.
7. **User:** SIM swap hone par OTP kiske phone par jayega?
   **Assistant:** Ek baar duplicate SIM active hone par, aapka physical SIM chalu nahi rahega aur saare bank alerts aur OTPs scammer ke pass chalu duplicate SIM par jayenge.
8. **User:** Kya main bank alerts ke liye mobile number ke sath email ID bhi link kar sakta hu?
   **Assistant:** Haan, ye ek bahut safe option hai. Agar mobile signal band bhi ho jaye, toh email par instant transaction messages aane se aapko bank fraud ka turant pata chal jayega.
9. **User:** Cyber cell me SIM swap ki complaint kaise karein?
   **Assistant:** Dial karein **1930** ya visit karein cybercrime.gov.in. Telecommunication department aur bank details ki complain register karwayein.
10. **User:** Kya SIM card par PIN code lagana is fraud ko rok sakta hai?
    **Assistant:** SIM card PIN physically phone chori hone par card ko dusre phone me chalne se rokta hai, par SIM Swap fraud (jo system database se hota hai) par iska koi asar nahi hota.
11. **User:** operator gallery wale bol rahe hain ki naya SIM 4 ghante me chalega. Kya tab tak main safe hu?
    **Assistant:** Haan, active hone tak safe hain par safety ke liye bank ko inform karke rakhein aur alternate email updates check karte rahein.
12. **User:** SIM Swap fraud ke baad bank me shadow credit mila par use use kar sakte hain?
    **Assistant:** Shadow credit temporary refund hota hai. Jaanch poori hone tak aap use withdraw ya transfer na karein, bank investigation close hone ka wait karein.
13. **User:** Kya biometric thumbprint se SIM replacement compulsory hai?
    **Assistant:** DoT regulations ke tehat biometric verification ko badhava diya ja raha hai kyuki isse fake paper ID cards ka use karke duplicate SIM nikalwana mushkil ho jata hai.
14. **User:** Kya credit card ka bill payment direct target ho sakta hai?
    **Assistant:** Haan, fraudsters credit cards se bank funds transfer ya shopping ke liye card details use karke OTP chura sakte hain.
15. **User:** SIM swap fraud me standard compensation rules kya hain?
    **Assistant:** Agar telecom aur bank dono ki galti paayi jati hai aur aapne instant safety block report darj ki hai, toh RBI rules ke tehat customer liability zero hoti hai aur poora refund milta hai.

---

## Government Services
- **Department of Telecommunications (DoT):** dot.gov.in
- **TAFCOP Portal (tafcop.sancharsaathi.gov.in):** To check how many SIM cards are active in your name.
- **National Cyber Crime Helpline:** 1930.

---

## Search Optimization
- **English Keywords:** Prevent SIM swap fraud India, duplicate SIM card replacement scam, phone signal lost bank hack, tafcop portal sanchar saathi check, report duplicate sim fraud, dot rules sim block.
- **Hindi Keywords:** सिम स्वैप धोखाधड़ी, डुप्लीकेट सिम फ्रॉड, मोबाइल सिग्नल गायब बैंक हैक, संचार साथी पोर्टल.
- **Hinglish Keywords:** sim card duplicate nikal gaya kya kare, network signal no service check, sim swap se bank refund.
- **Synonyms:** SIM hijacking, SIM splitting scam, mobile identity theft.
- **Abbreviations:** DoT, IMSI, OTP, PIN, 2FA, RBI, MHA, NCRP, GST.
- **Common Misspellings:** sim swarp fraud, duplicate sim check online, sancharsaathi portal.
- **Regional Search Terms:** SIM Attai Matru Mosam (Tamil), SIM Swapping Donga (Telugu).

---

## Intent Mapping
- `definition`
- `fraud_help`
- `customer_rights`

---

## Retrieval Tags
SIM swap fraud, duplicate SIM card, phone network signal loss, no service bank scam, SMS OTP theft, two factor authentication bypass, DoT 24 hour SMS block, telecom replacement verification, Sanchar Saathi TAFCOP, check registered SIMs, identity theft Aadhaar, forged ID cards, cybercrime helpline 1930, cyber cell complaint, zero liability banking swap, email transaction alerts, mobile operator security check, biometric SIM verification, mule bank accounts, SMS forwarding redirect.

---

## Cross References
- [banking/cyber_security/phishing.md](banking/cyber_security/phishing.md)
- [banking/cyber_security/reporting_fraud.md](banking/cyber_security/reporting_fraud.md)
- [banking/customer_rights.md](banking/customer_rights.md)
- [banking/complaints.md](banking/complaints.md)

---

## See Also
- digital_arrest.md
- upi_fraud.md
- remote_access_scam.md
- zero_balance.md

---

## References
- Department of Telecommunications (DoT) Mandates on SIM Replacement and Verification.
- Reserve Bank of India (RBI) Advisory on SIM Swap and Phishing Vectors.
- Indian Penal Code, 1860 (Section 419 - Punishment for cheating by personation).

---

## Banking Disclaimer
This document is for educational and informational purposes only and does not constitute technical, telecom, or legal advice. SIM card replacement procedures, activation durations, and warning notification systems differ based on telecom operator networks and state regulations. Always contact your telecom provider immediately if your mobile signal behaves abnormally.
