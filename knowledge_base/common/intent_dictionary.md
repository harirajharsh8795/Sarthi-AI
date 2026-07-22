---
id: saarthi_common_intent_dictionary_001
title: Saarthi AI Master Intent Dictionary
domain: common
category: NLU Framework
subcategory: Intent Mapping
topic: Master Intent Dictionary
version: 1.0
language: multilingual
difficulty: intermediate
keywords: [intent mapping, nlp dictionary, saarthi ai intents, conversational ai, user intent, dialogue management, banking intents, legal intents, medical intents, public administration]
aliases: [Master Intent Tracker, NLU Intent Glossary, Saarthi Intent Guide]
related_topics: [Entity Recognition, Dialogue Management, Natural Language Understanding]
intent: check_intent_dictionary
last_updated: 2026-07-21
author: Saarthi AI
sources: [Saarthi AI Internal NLU Guidelines, Conversational AI Standards]
---

# Saarthi AI Master Intent Dictionary

## Overview
**English**: The Master Intent Dictionary serves as the foundational Natural Language Understanding (NLU) framework for Saarthi AI. It defines, categorizes, and maps user queries across Banking, Legal, Medical, and Public Administration domains into actionable intents, allowing the offline AI assistant to trigger the correct workflows, fetch accurate knowledge, and provide localized multilingual responses.
**Hindi**: मास्टर इंटेंट डिक्शनरी (Master Intent Dictionary) सारथी AI के लिए एक बुनियादी प्राकृतिक भाषा समझ (NLU) ढांचे के रूप में कार्य करती है। यह बैंकिंग, कानूनी, चिकित्सा और सार्वजनिक प्रशासन डोमेन में उपयोगकर्ता के प्रश्नों को परिभाषित, वर्गीकृत और मैप करती है, जिससे ऑफ़लाइन AI सहायक सही वर्कफ़्लो को ट्रिगर करने और स्थानीय बहुभाषी प्रतिक्रियाएं प्रदान करने में सक्षम होता है।
**Hinglish**: Master Intent Dictionary Saarthi AI ke liye ek foundational NLU framework ka kaam karti hai. Ye Banking, Legal, Medical, aur Public Administration domains ke user queries ko define aur categorize karti hai, jisse offline AI assistant sahi workflow trigger karke accurate aur multilingual response de sake.

## Quick Summary
**English**: This document outlines all primary intents recognized by Saarthi AI, mapping user inputs to system actions. It includes domain-specific classifications, handling rules, and fallback mechanisms.
**Hindi**: यह दस्तावेज़ सारथी AI द्वारा मान्यता प्राप्त सभी प्राथमिक इंटेंट्स की रूपरेखा तैयार करता है, जो उपयोगकर्ता इनपुट को सिस्टम क्रियाओं से जोड़ता है।
**Hinglish**: Ye document Saarthi AI dwara recognize kiye gaye sabhi primary intents ko outline karta hai, jo user input ko system actions se map karta hai.

## Definition
**English**: An "Intent" represents the underlying goal or purpose of a user's input. The Intent Dictionary is a structured registry cataloging these goals (e.g., checking a bank balance, filing a police complaint) alongside their respective training utterances and domain categories.
**Hindi**: "इंटेंट" उपयोगकर्ता के इनपुट के अंतर्निहित लक्ष्य या उद्देश्य को दर्शाता है। इंटेंट डिक्शनरी एक संरचित रजिस्ट्री है जो इन लक्ष्यों को सूचीबद्ध करती है।
**Hinglish**: "Intent" user input ke main goal ya purpose ko darshata hai. Intent Dictionary ek structured registry hai jo in goals ko categorize karti hai.

## Why It Matters
**English**: Accurate intent classification is critical for Saarthi AI because it operates offline. Without cloud-based large language models, the local NLU engine must rely on a meticulously crafted intent dictionary to quickly route queries to the correct static knowledge bases or local APIs.
**Hindi**: सटीक इंटेंट वर्गीकरण सारथी AI के लिए महत्वपूर्ण है क्योंकि यह ऑफ़लाइन संचालित होता है। स्थानीय NLU इंजन को प्रश्नों को सही ज्ञान आधार तक पहुंचाने के लिए इस डिक्शनरी पर निर्भर रहना पड़ता है।
**Hinglish**: Accurate intent classification Saarthi AI ke liye bahut zaroori hai kyunki ye offline chalta hai. Local NLU engine ko queries sahi jagah route karne ke liye is dictionary par depend hona padta hai.

## Detailed Framework / Content Structure

| Domain | Intent Name | Description | Example Utterances (En/Hi/Hinglish) | System Action |
| :--- | :--- | :--- | :--- | :--- |
| Banking | `bank_check_balance` | Inquire about account balance | "Check balance", "खाता शेष", "Balance dikhao" | Trigger Balance API |
| Banking | `bank_apply_loan` | Initiate a loan application | "Apply for loan", "ऋण आवेदन", "Loan apply karna hai" | Trigger Loan Workflow |
| Banking | `bank_block_card` | Request to block a lost debit/credit card | "Block my card", "कार्ड ब्लॉक करें", "Mera card block kar do" | Trigger Card Block Protocol |
| Banking | `bank_check_interest_rate` | Ask for current FD/RD/Loan interest rates | "What is the FD rate?", "एफडी दर क्या है?", "FD ka rate kya hai?" | Fetch Rate Knowledge Base |
| Banking | `bank_open_account` | Open a new savings or current account | "Open new account", "नया खाता खोलें", "Naya account kholna hai" | Trigger Account Opening Guide |
| Legal | `legal_file_fir` | Understand process to file an FIR | "How to file FIR?", "एफआईआर कैसे दर्ज करें?", "FIR kaise file karein?" | Fetch FIR Legal Guide |
| Legal | `legal_know_rights` | Ask about fundamental or legal rights | "What are my rights?", "मेरे अधिकार क्या हैं?", "Mere rights kya hain?" | Fetch Citizen Rights Base |
| Legal | `legal_check_case_status` | Check the status of a pending court case | "Check case status", "केस की स्थिति जांचें", "Case ka status batao" | Trigger eCourts Lookup API |
| Legal | `legal_property_registration` | Ask about registering a property or land | "Property registration process", "संपत्ति पंजीकरण", "Property register karni hai" | Fetch Property Law KB |
| Legal | `legal_consumer_complaint` | File a complaint in consumer court | "Consumer forum complaint", "उपभोक्ता शिकायत", "Consumer court me complaint karni hai" | Trigger Consumer Workflow |
| Medical | `medical_book_appointment` | Schedule a doctor appointment | "Book doctor", "डॉक्टर अपॉइंटमेंट बुक करें", "Doctor ki appointment chahiye" | Trigger Healthcare Scheduler |
| Medical | `medical_symptom_check` | Preliminary symptom analysis | "I have a fever", "मुझे बुखार है", "Mujhe bukhar aa raha hai" | Fetch Symptom Checker |
| Medical | `medical_find_hospital` | Locate nearby hospitals or clinics | "Hospitals near me", "मेरे पास के अस्पताल", "Aas paas hospital kahan hai?" | Trigger Geo-Location API |
| Medical | `medical_insurance_claim` | How to file a health insurance claim | "Health insurance claim", "स्वास्थ्य बीमा दावा", "Health insurance claim karna hai" | Fetch Insurance Guide |
| Medical | `medical_first_aid_info` | Ask for emergency first-aid instructions | "How to treat a burn", "जलने का प्राथमिक उपचार", "Jalne par kya karein?" | Fetch Emergency Medical KB |
| Public Admin | `admin_apply_passport` | Passport application and renewal queries | "Apply for passport", "पासपोर्ट के लिए आवेदन करें", "Passport apply karna hai" | Fetch Passport Seva Guide |
| Public Admin | `admin_download_aadhar` | Aadhaar card related queries | "Download Aadhaar", "आधार डाउनलोड", "Aadhaar card download karna hai" | Trigger UIDAI Workflow |
| Public Admin | `admin_pay_taxes` | Income tax or property tax payments | "Pay income tax", "आयकर का भुगतान करें", "Income tax pay karna hai" | Fetch Taxation Guide |
| Public Admin | `admin_voter_id_reg` | Voter ID registration and updates | "Apply for voter ID", "वोटर आईडी पंजीकरण", "Voter ID banwana hai" | Fetch Election Comm. Guide |
| Public Admin | `admin_ration_card` | Ration card application and status | "Ration card status", "राशन कार्ड की स्थिति", "Ration card check karna hai" | Fetch PDS Information |
| Common | `common_greeting` | User greets the assistant | "Hello", "नमस्ते", "Hi Saarthi" | Greeting Response |
| Common | `common_fallback` | Out of domain or unrecognized query | "Tell me a joke", "मुझे चुटकुला सुनाओ", "Joke sunao" | Fallback / Clarification Protocol |
| Common | `common_change_language` | Request to switch assistant language | "Speak in Hindi", "हिंदी में बात करें", "Hindi me bolo" | Trigger Language Switch |

## Applicability
**English**: This intent dictionary applies to all modules of the Saarthi AI offline assistant. It covers interactions originating from text inputs, voice transcriptions, and local API requests. Exemptions include pure OS-level hardware commands which are handled directly by the device OS.
**Hindi**: यह इंटेंट डिक्शनरी सारथी AI ऑफ़लाइन सहायक के सभी मॉड्यूल पर लागू होती है।
**Hinglish**: Ye intent dictionary Saarthi AI offline assistant ke sabhi modules par apply hoti hai.

## Rights of Citizens
**English**: Citizens have the right to privacy; their intents are processed entirely offline without sending personal data to cloud servers.
**Hindi**: नागरिकों को निजता का अधिकार है; उनके इंटेंट्स को क्लाउड सर्वर पर व्यक्तिगत डेटा भेजे बिना पूरी तरह से ऑफ़लाइन संसाधित किया जाता है।
**Hinglish**: Citizens ko privacy ka right hai; unke intents bina cloud par data bheje offline process hote hain.

## Duties & Responsibilities
**English**: Users should attempt to provide clear utterances to help the local NLU engine accurately classify the intent. Developers must regularly update this dictionary.
**Hindi**: स्थानीय NLU इंजन को इंटेंट को सटीक रूप से वर्गीकृत करने में मदद करने के लिए उपयोगकर्ताओं को स्पष्ट बातें प्रदान करने का प्रयास करना चाहिए।
**Hinglish**: Users ko clear utterances deni chahiye taaki local NLU engine intent ko sahi se classify kar sake.

## Step-by-Step Procedure / Usage Guide
**English**:
1. User provides input via voice or text.
2. The local Speech-to-Text engine (if voice) converts it to text.
3. The NLU module tokenizes the text and matches it against the Master Intent Dictionary.
4. The system identifies the highest confidence intent.
5. If confidence is >80%, the mapped System Action is triggered.
6. If confidence is <80%, the `common_fallback` intent is triggered to ask for clarification.

**Hindi**:
1. उपयोगकर्ता आवाज़ या टेक्स्ट के माध्यम से इनपुट प्रदान करता है।
2. स्थानीय NLU मॉड्यूल टेक्स्ट को टोकन करता है और इसका मिलान मास्टर इंटेंट डिक्शनरी से करता है।
3. सिस्टम उच्चतम विश्वास वाले इंटेंट की पहचान करता है और कार्रवाई करता है।

**Hinglish**:
1. User voice ya text ke through input deta hai.
2. NLU module text ko check karta hai aur Master Intent Dictionary se match karta hai.
3. System highest confidence wale intent ko identify karke action leta hai.

## Required Documents / Reference Tables
- Saarthi AI NLU Architecture Document
- Domain-specific Knowledge Bases (Banking, Legal, Medical, Public Admin)
- Multilingual Synonym Library (common/glossary.md)

## Authorities / Helplines / Organizations
- Saarthi AI Core Engineering Team
- Saarthi AI Linguistic Data Team
- India Offline AI Standards Board

## Common Errors & Misconceptions
- **Error**: Misclassifying `bank_apply_loan` as `bank_check_interest_rate`.
- **Misconception**: Believing the intent dictionary requires an internet connection to update live. (Updates are done via batch offline syncs).

## Safety & Verification Tips
**English**: Always verify the triggered intent in the debug console during development. Ensure sensitive intents like `bank_block_card` have secondary confirmation prompts.
**Hindi**: विकास के दौरान हमेशा डीबग कंसोल में ट्रिगर किए गए इंटेंट को सत्यापित करें। सुनिश्चित करें कि संवेदनशील इंटेंट में द्वितीयक पुष्टिकरण संकेत हैं।
**Hinglish**: Development ke time hamesha debug console me triggered intent verify karein. Sensitive intents ke liye double confirmation zaroori hai.

## Frequently Asked Questions

1. **What is an intent in Saarthi AI?**
   **English**: An intent is the user's goal when they interact with the assistant. It tells the system what action needs to be taken. This is fundamental to NLU.
   **Hindi**: सारथी AI में इंटेंट उपयोगकर्ता का लक्ष्य है जब वे सहायक के साथ बातचीत करते हैं। यह सिस्टम को बताता है कि क्या कार्रवाई की जानी है। यह NLU के लिए मौलिक है।
   **Hinglish**: Saarthi AI me intent user ka goal hota hai jab wo assistant se baat karta hai. Ye system ko batata hai ki kya action lena hai. Ye NLU ka basic part hai.

2. **How does the intent dictionary work offline?**
   **English**: The dictionary is pre-compiled into a local database on the device. It uses lightweight, optimized models to match text to intents without internet access. This ensures speed and privacy.
   **Hindi**: डिक्शनरी को डिवाइस पर एक स्थानीय डेटाबेस में पूर्व-संकलित किया जाता है। यह इंटरनेट एक्सेस के बिना टेक्स्ट का इंटेंट से मिलान करने के लिए हल्के, अनुकूलित मॉडल का उपयोग करता है। यह गति और गोपनीयता सुनिश्चित करता है।
   **Hinglish**: Dictionary device par local database me pre-compiled hoti hai. Ye bina internet ke text ko intents se match karne ke liye optimized models use karti hai. Isse speed aur privacy milti hai.

3. **What happens if an intent is not recognized?**
   **English**: If the system confidence is too low, it triggers a fallback intent. The assistant will then ask the user to rephrase their request. It logs the unrecognized query for future learning.
   **Hindi**: यदि सिस्टम का विश्वास बहुत कम है, तो यह फ़ॉलबैक इंटेंट को ट्रिगर करता है। सहायक तब उपयोगकर्ता से अपने अनुरोध को फिर से कहने के लिए कहेगा। यह भविष्य की सीख के लिए अज्ञात क्वेरी को लॉग करता है।
   **Hinglish**: Agar system confidence low hai, to fallback intent trigger hota hai. Assistant user se apna question dobara poochne ko kahega. Ye future learning ke liye query log kar leta hai.

4. **Can intents handle multiple languages in one sentence?**
   **English**: Yes, the NLU engine is trained on code-mixed data (like Hinglish). The intent dictionary maps cross-lingual synonyms to a single master intent. This is vital for the Indian context.
   **Hindi**: हाँ, NLU इंजन को कोड-मिश्रित डेटा (जैसे हिंग्लिश) पर प्रशिक्षित किया जाता है। इंटेंट डिक्शनरी क्रॉस-लिंगुअल समानार्थी शब्दों को एक मास्टर इंटेंट में मैप करती है। यह भारतीय संदर्भ के लिए महत्वपूर्ण है।
   **Hinglish**: Haan, NLU engine code-mixed data par trained hai. Intent dictionary alag-alag languages ke synonyms ko ek master intent par map karti hai. Ye Indian context ke liye zaroori hai.

5. **How are banking intents secured?**
   **English**: Banking intents require secondary authentication. Identifying the intent is just step one; executing it requires PIN or biometric validation. Data is kept locally secure.
   **Hindi**: बैंकिंग इंटेंट के लिए द्वितीयक प्रमाणीकरण की आवश्यकता होती है। इंटेंट की पहचान करना सिर्फ पहला कदम है; इसे निष्पादित करने के लिए पिन या बायोमेट्रिक सत्यापन की आवश्यकता होती है। डेटा स्थानीय रूप से सुरक्षित रखा जाता है।
   **Hinglish**: Banking intents ke liye secondary authentication chahiye. Intent identify karna pehla step hai; execute karne ke liye PIN ya biometric validation lagta hai. Data locally safe rehta hai.

6. **What is a fallback intent?**
   **English**: A fallback intent is the safety net of the NLU system. It catches inputs that do not match any known intent in the dictionary. It prevents the system from crashing.
   **Hindi**: फ़ॉलबैक इंटेंट NLU सिस्टम का सुरक्षा जाल है। यह उन इनपुट को पकड़ता है जो डिक्शनरी में किसी भी ज्ञात इंटेंट से मेल नहीं खाते हैं। यह सिस्टम को क्रैश होने से रोकता है।
   **Hinglish**: Fallback intent NLU system ka safety net hai. Ye un inputs ko catch karta hai jo dictionary me kisi known intent se match nahi karte. Ye system ko crash hone se bachata hai.

7. **How frequently is the intent dictionary updated?**
   **English**: The dictionary is updated through periodic local software patches. When the user syncs their device, new intents are downloaded. It is updated quarterly by the Saarthi team.
   **Hindi**: डिक्शनरी को आवधिक स्थानीय सॉफ़्टवेयर पैच के माध्यम से अपडेट किया जाता है। जब उपयोगकर्ता अपने डिवाइस को सिंक करता है, तो नए इंटेंट डाउनलोड होते हैं। इसे सारथी टीम द्वारा त्रैमासिक रूप से अपडेट किया जाता है।
   **Hinglish**: Dictionary periodic local software patches ke through update hoti hai. Jab user device sync karta hai, naye intents download hote hain. Ise Saarthi team quarterly update karti hai.

8. **Are medical intents meant for diagnostics?**
   **English**: No, medical intents route to information and first-aid guides, not definitive diagnoses. They are for informational support only. Users are advised to see a doctor.
   **Hindi**: नहीं, चिकित्सा इंटेंट जानकारी और प्राथमिक चिकित्सा गाइड को रूट करते हैं, न कि निश्चित निदान को। वे केवल सूचनात्मक सहायता के लिए हैं। उपयोगकर्ताओं को डॉक्टर से मिलने की सलाह दी जाती है।
   **Hinglish**: Nahi, medical intents sirf information aur first-aid guides ke liye hain, final diagnosis ke liye nahi. Ye sirf info support ke liye hain. Users ko doctor ko dikhane ki salah di jati hai.

9. **Can the user customize their own intents?**
   **English**: Currently, users cannot add custom intents to the core dictionary. The core intents are strictly managed to maintain offline stability and accuracy. Customization is limited to quick actions.
   **Hindi**: वर्तमान में, उपयोगकर्ता कोर डिक्शनरी में कस्टम इंटेंट नहीं जोड़ सकते हैं। ऑफ़लाइन स्थिरता और सटीकता बनाए रखने के लिए मुख्य इंटेंट को सख्ती से प्रबंधित किया जाता है। अनुकूलन त्वरित क्रियाओं तक सीमित है।
   **Hinglish**: Abhi users core dictionary me custom intents nahi add kar sakte. Offline stability banaye rakhne ke liye core intents strictly manage kiye jate hain. Customization sirf quick actions tak limited hai.

10. **How does the system differentiate between similar legal and administrative intents?**
    **English**: It uses contextual tokens and entity extraction. For example, "court" vs "government office" helps differentiate legal cases from administrative tasks. Advanced embedding distances resolve ties.
    **Hindi**: यह प्रासंगिक टोकन और इकाई निष्कर्षण का उपयोग करता है। उदाहरण के लिए, "अदालत" बनाम "सरकारी कार्यालय" कानूनी मामलों को प्रशासनिक कार्यों से अलग करने में मदद करता है।
    **Hinglish**: Ye contextual tokens aur entity extraction use karta hai. Jaise "court" aur "government office" me difference legal aur admin tasks ko alag karne me madad karta hai.

11. **Is the intent dictionary identical across all Saarthi devices?**
    **English**: Yes, the base master dictionary is identical across all core offline devices. This standardizes the AI's behavior everywhere. Local language packs modify the mapping, not the intents.
    **Hindi**: हाँ, बेस मास्टर डिक्शनरी सभी कोर ऑफ़लाइन उपकरणों में समान है। यह हर जगह AI के व्यवहार को मानकीकृत करता है। स्थानीय भाषा पैक मैपिंग को संशोधित करते हैं, इंटेंट को नहीं।
    **Hinglish**: Haan, base master dictionary sabhi core offline devices par same hoti hai. Ye AI ke behavior ko standardize karti hai. Local language packs sirf mapping change karte hain.

12. **What role do entities play alongside intents?**
    **English**: Entities provide the specific parameters for an intent. If the intent is `bank_check_balance`, the entity might be "savings account". Intents define the action; entities define the target.
    **Hindi**: इकाइयां एक इंटेंट के लिए विशिष्ट पैरामीटर प्रदान करती हैं। यदि इंटेंट बैंक बैलेंस चेक करना है, तो इकाई "बचत खाता" हो सकती है। इंटेंट कार्रवाई को परिभाषित करते हैं; इकाइयां लक्ष्य को परिभाषित करती हैं।
    **Hinglish**: Entities ek intent ke liye specific parameters deti hain. Agar intent balance check karna hai, to entity "savings account" ho sakti hai. Intents action define karte hain, entities target.

13. **Why do we need a separate Master Intent Dictionary file?**
    **English**: It acts as the central source of truth for the engineering and localization teams. Having a single master file prevents duplication of intents. It ensures consistent architecture.
    **Hindi**: यह इंजीनियरिंग और स्थानीयकरण टीमों के लिए सत्य के केंद्रीय स्रोत के रूप में कार्य करता है। एक ही मास्टर फ़ाइल होने से इंटेंट के दोहराव को रोका जा सकता है। यह सुसंगत वास्तुकला सुनिश्चित करता है।
    **Hinglish**: Ye engineering aur localization teams ke liye central source of truth hai. Ek master file hone se intents duplicate nahi hote. Ye consistent architecture banaye rakhta hai.

14. **How are greetings and chitchat handled?**
    **English**: Greetings are categorized under `common_greeting` and simple chitchat falls under small talk intents. Since Saarthi is a task-oriented offline assistant, chitchat is kept minimal to save processing power.
    **Hindi**: अभिवादन को सामान्य अभिवादन के तहत वर्गीकृत किया गया है और साधारण बातचीत छोटी बात के अंतर्गत आती है। चूंकि सारथी एक कार्य-उन्मुख ऑफ़लाइन सहायक है, इसलिए प्रसंस्करण शक्ति को बचाने के लिए बातचीत को न्यूनतम रखा जाता है।
    **Hinglish**: Greetings ko common_greeting me rakha gaya hai aur chitchat small talk intents me aata hai. Saarthi ek task-oriented assistant hai, isliye chitchat minimal rakha gaya hai.

15. **Does intent mapping depend on grammar?**
    **English**: No, the offline NLU is trained to be robust against grammatical errors. It focuses on keywords and semantic meaning rather than strict syntax. This is highly effective for varied regional dialects.
    **Hindi**: नहीं, ऑफ़लाइन NLU को व्याकरणिक त्रुटियों के प्रति मजबूत होने के लिए प्रशिक्षित किया जाता है। यह सख्त वाक्य रचना के बजाय कीवर्ड और अर्थ संबंधी अर्थ पर केंद्रित है।
    **Hinglish**: Nahi, offline NLU grammatical mistakes ke khilaf robust hai. Ye strict syntax ke bajaye keywords aur meaning par focus karta hai.

16. **Can an intent trigger multiple workflows?**
    **English**: Generally, one intent triggers one primary workflow. However, that workflow may have sub-routines. For complex requests, the system handles it sequentially through dialogue management.
    **Hindi**: आम तौर पर, एक इंटेंट एक प्राथमिक वर्कफ़्लो को ट्रिगर करता है। हालाँकि, उस वर्कफ़्लो में उप-दिनचर्या हो सकती है। जटिल अनुरोधों के लिए, सिस्टम इसे संवाद प्रबंधन के माध्यम से क्रमिक रूप से संभालता है।
    **Hinglish**: Generally, ek intent ek primary workflow trigger karta hai. Par us workflow ke sub-routines ho sakte hain. Complex requests ke liye system sequence me kaam karta hai.

17. **What is the maximum number of intents supported offline?**
    **English**: The current local NLU engine can comfortably support up to 500 distinct intents without degrading offline performance. The Master Dictionary currently tracks around 150 core intents.
    **Hindi**: वर्तमान स्थानीय NLU इंजन ऑफ़लाइन प्रदर्शन को कम किए बिना 500 अलग-अलग इंटेंट तक का आराम से समर्थन कर सकता है। मास्टर डिक्शनरी वर्तमान में लगभग 150 कोर इंटेंट को ट्रैक करती है।
    **Hinglish**: Current local NLU engine bina performance gire 500 distinct intents support kar sakta hai. Master dictionary me abhi kareeb 150 core intents hain.

18. **How does Saarthi AI update its dictionary for new government schemes?**
    **English**: When a major scheme is launched, an NLU patch is generated. Once the user connects to a local sync point or Wi-Fi temporarily, the new intents are added to the offline dictionary.
    **Hindi**: जब कोई बड़ी योजना शुरू की जाती है, तो एक NLU पैच उत्पन्न होता है। एक बार जब उपयोगकर्ता अस्थायी रूप से वाई-फाई से जुड़ जाता है, तो ऑफ़लाइन डिक्शनरी में नए इंटेंट जोड़े जाते हैं।
    **Hinglish**: Jab koi nayi scheme aati hai, to ek NLU patch banta hai. Jaise hi user Wi-Fi se connect hota hai, naye intents offline dictionary me add ho jate hain.

19. **Why use explicit intent mapping instead of generative AI?**
    **English**: Generative AI requires massive compute and cloud access, which compromises offline capability and privacy. Explicit intent mapping is deterministic, fast, runs locally, and guarantees accuracy without hallucinations.
    **Hindi**: जनरेटिव AI को बड़े पैमाने पर कंप्यूट और क्लाउड एक्सेस की आवश्यकता होती है, जो ऑफ़लाइन क्षमता और गोपनीयता से समझौता करता है। स्पष्ट इंटेंट मैपिंग नियतात्मक, तेज़ है, और स्थानीय रूप से चलती है।
    **Hinglish**: Generative AI ko jyada compute aur cloud chahiye jo offline privacy ke khilaf hai. Explicit intent mapping fast hai, locally chalta hai aur bina hallucinations ke accurate result deta hai.

20. **Can users request a log of their triggered intents?**
    **English**: Yes, users can view their interaction history directly on the device. Since everything is processed offline, the logs are strictly local and fully transparent to the user.
    **Hindi**: हां, उपयोगकर्ता अपना इंटरेक्शन इतिहास सीधे डिवाइस पर देख सकते हैं। चूंकि सब कुछ ऑफ़लाइन संसाधित होता है, लॉग पूरी तरह से स्थानीय और उपयोगकर्ता के लिए पारदर्शी होते हैं।
    **Hinglish**: Haan, users apna interaction history device par dekh sakte hain. Kyunki sab offline hota hai, logs strictly local aur transparent hote hain.

## Common Myths vs Facts
1. **Myth**: Intent dictionaries require cloud processing.
   **Fact**: Saarthi's intent dictionary is embedded entirely within the device's local offline engine.
2. **Myth**: It only understands perfect English.
   **Fact**: The dictionary maps colloquial Hinglish, Hindi, and regional dialects to master intents perfectly.
3. **Myth**: More intents always mean a smarter AI.
   **Fact**: Too many overlapping intents confuse the NLU; a focused, distinct dictionary yields higher accuracy.
4. **Myth**: Fallback intent means the system crashed.
   **Fact**: Fallback intent is a controlled safety mechanism to ask the user for clarification.
5. **Myth**: The intent dictionary stores my personal voice data.
   **Fact**: It only stores abstract mappings and structural definitions, zero personal data.
6. **Myth**: You cannot update an offline intent dictionary.
   **Fact**: It can be updated via secure, tiny periodic patch downloads.
7. **Myth**: Medical intents can replace real doctors.
   **Fact**: Medical intents only provide standard first-aid and directory information.
8. **Myth**: Intents and Entities are the exact same thing.
   **Fact**: Intents are actions (e.g., book ticket), entities are variables (e.g., to Delhi).
9. **Myth**: Hinglish intents are separated from Hindi intents.
   **Fact**: They point to the same unified Master Intent ID to ensure consistent workflow triggering.
10. **Myth**: It takes seconds to match an intent offline.
    **Fact**: Local intent mapping happens in less than 50 milliseconds.

## Conversation Examples

**Example 1: Banking Balance Inquiry**
*Citizen (En)*: How much money is in my account?
*Assistant (En)*: Your account balance is ₹15,000. Is there anything else you need?
*Citizen (Hi)*: मेरे खाते में कितने पैसे हैं?
*Assistant (Hi)*: आपके खाते की शेष राशि ₹15,000 है। क्या आपको कुछ और चाहिए?
*Citizen (Hinglish)*: Mere account me kitne paise hain?
*Assistant (Hinglish)*: Aapke account ka balance ₹15,000 hai. Kya main aur kuch madad kar sakti hu?

**Example 2: FIR Filing**
*Citizen (En)*: I want to file a police complaint.
*Assistant (En)*: To file an FIR, you can visit the nearest police station or use the state police online portal. Shall I show you the steps?
*Citizen (Hi)*: मैं पुलिस में शिकायत दर्ज करना चाहता हूँ।
*Assistant (Hi)*: एफआईआर दर्ज करने के लिए, आप नजदीकी पुलिस स्टेशन जा सकते हैं या राज्य पुलिस के ऑनलाइन पोर्टल का उपयोग कर सकते हैं। क्या मैं आपको चरण दिखाऊं?
*Citizen (Hinglish)*: Mujhe police complaint karni hai.
*Assistant (Hinglish)*: FIR file karne ke liye aap nearest police station ja sakte hain ya online portal use kar sakte hain. Kya main steps dikhau?

**Example 3: Medical Appointment**
*Citizen (En)*: Book a doctor appointment.
*Assistant (En)*: Sure, I can help you book an appointment. Which specialty or doctor are you looking for?
*Citizen (Hi)*: डॉक्टर का अपॉइंटमेंट बुक करें।
*Assistant (Hi)*: ज़रूर, मैं अपॉइंटमेंट बुक करने में आपकी मदद कर सकता हूँ। आप किस विशेषता या डॉक्टर की तलाश कर रहे हैं?
*Citizen (Hinglish)*: Doctor ki appointment book karni hai.
*Assistant (Hinglish)*: Zaroor, main appointment book karne me madad kar sakti hu. Aap kis doctor ko dikhana chahte hain?

**Example 4: Aadhaar Download**
*Citizen (En)*: How do I get my e-Aadhaar?
*Assistant (En)*: You can download your e-Aadhaar from the official UIDAI website using your Aadhaar number and OTP.
*Citizen (Hi)*: मुझे अपना ई-आधार कैसे मिलेगा?
*Assistant (Hi)*: आप अपने आधार नंबर और ओटीपी का उपयोग करके आधिकारिक यूआईडीएआई वेबसाइट से अपना ई-आधार डाउनलोड कर सकते हैं।
*Citizen (Hinglish)*: e-Aadhaar kaise milega?
*Assistant (Hinglish)*: Aap UIDAI website se Aadhaar number aur OTP use karke e-Aadhaar download kar sakte hain.

**Example 5: Fallback Trigger**
*Citizen (En)*: When will the aliens attack?
*Assistant (En)*: I am sorry, I am a public assistance AI and I do not have information on that topic. How can I help you with banking, legal, or public services?
*Citizen (Hi)*: एलियंस कब हमला करेंगे?
*Assistant (Hi)*: मुझे खेद है, मैं एक सार्वजनिक सहायता एआई हूं और मेरे पास उस विषय पर जानकारी नहीं है। मैं आपकी कैसे मदद कर सकता हूँ?
*Citizen (Hinglish)*: Aliens kab aayenge?
*Assistant (Hinglish)*: Sorry, main public assistance AI hu aur is topic par jankari nahi hai. Main banking ya legal me kaise madad karu?

**Example 6: Property Registration**
*Citizen (En)*: I need to register a new property.
*Assistant (En)*: Property registration requires the sale deed, identity proof, and stamp duty payment. Shall I open the state registry guide?
*Citizen (Hi)*: मुझे एक नई संपत्ति पंजीकृत करनी है।
*Assistant (Hi)*: संपत्ति पंजीकरण के लिए बिक्री विलेख, पहचान प्रमाण और स्टाम्प शुल्क भुगतान की आवश्यकता होती है। क्या मैं राज्य रजिस्ट्री गाइड खोलूं?
*Citizen (Hinglish)*: Nayi property register karni hai.
*Assistant (Hinglish)*: Property registration ke liye sale deed aur stamp duty chahiye. Kya main state registry guide open karu?

**Example 7: Loan Application**
*Citizen (En)*: Apply for a personal loan.
*Assistant (En)*: To apply for a personal loan, I will need to guide you through your bank's application workflow. Proceed?
*Citizen (Hi)*: व्यक्तिगत ऋण के लिए आवेदन करें।
*Assistant (Hi)*: व्यक्तिगत ऋण के लिए आवेदन करने के लिए, मुझे आपके बैंक के वर्कफ़्लो के माध्यम से आपका मार्गदर्शन करना होगा। आगे बढ़ें?
*Citizen (Hinglish)*: Personal loan apply karna hai.
*Assistant (Hinglish)*: Personal loan apply karne ke liye mujhe bank workflow open karna hoga. Aage badhein?

**Example 8: Ration Card Status**
*Citizen (En)*: Check my ration card status.
*Assistant (En)*: Please provide your ration card application number to check the current status on the PDS portal.
*Citizen (Hi)*: मेरे राशन कार्ड की स्थिति जांचें।
*Assistant (Hi)*: पीडीएस पोर्टल पर वर्तमान स्थिति की जांच करने के लिए कृपया अपना राशन कार्ड आवेदन संख्या प्रदान करें।
*Citizen (Hinglish)*: Ration card status check karna hai.
*Assistant (Hinglish)*: PDS portal par status check karne ke liye apna application number batayein.

**Example 9: Block Debit Card**
*Citizen (En)*: I lost my debit card, please block it.
*Assistant (En)*: This is urgent. I am initiating the card blocking protocol. Please enter your secure PIN to confirm.
*Citizen (Hi)*: मैंने अपना डेबिट कार्ड खो दिया है, कृपया इसे ब्लॉक करें।
*Assistant (Hi)*: यह जरूरी है। मैं कार्ड ब्लॉकिंग प्रोटोकॉल शुरू कर रहा हूँ। पुष्टि करने के लिए कृपया अपना सुरक्षित पिन दर्ज करें।
*Citizen (Hinglish)*: Mera debit card kho gaya hai, block kar do.
*Assistant (Hinglish)*: Ye urgent hai. Main card block protocol start kar rahi hu. Confirm karne ke liye PIN enter karein.

**Example 10: First Aid**
*Citizen (En)*: I cut my finger badly.
*Assistant (En)*: Wash the cut with clean water, apply gentle pressure with a clean cloth to stop bleeding, and seek medical help if it is deep.
*Citizen (Hi)*: मेरी उंगली बुरी तरह कट गई।
*Assistant (Hi)*: कट को साफ पानी से धो लें, खून बहने से रोकने के लिए साफ कपड़े से हल्का दबाव डालें, और गहरा होने पर चिकित्सा सहायता लें।
*Citizen (Hinglish)*: Meri ungli kat gayi hai.
*Assistant (Hinglish)*: Cut ko saaf paani se dho lein, khoon rokne ke liye saaf kapde se dabayein. Agar gehra hai to doctor ke paas jayein.

**Example 11: Tax Payment**
*Citizen (En)*: How do I pay property tax?
*Assistant (En)*: Property tax can be paid at your local municipal office or through their official online portal using your property ID.
*Citizen (Hi)*: मैं संपत्ति कर का भुगतान कैसे करूं?
*Assistant (Hi)*: संपत्ति कर का भुगतान आपके स्थानीय नगर निगम कार्यालय में या आपकी संपत्ति आईडी का उपयोग करके उनके आधिकारिक ऑनलाइन पोर्टल के माध्यम से किया जा सकता है।
*Citizen (Hinglish)*: Property tax kaise pay karu?
*Assistant (Hinglish)*: Property tax aap local municipal office ya unke online portal par property ID se pay kar sakte hain.

**Example 12: Change Language**
*Citizen (En)*: Talk to me in Hindi.
*Assistant (En)*: Switching language to Hindi. नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?
*Citizen (Hi)*: मुझसे हिंदी में बात करो।
*Assistant (Hi)*: भाषा को हिंदी में बदल रहा हूँ। नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?
*Citizen (Hinglish)*: Hindi me baat karo.
*Assistant (Hinglish)*: Language Hindi me switch kar rahi hu. Namaste, main aapki kaise madad kar sakti hu?

**Example 13: Case Status**
*Citizen (En)*: What is the status of my court case?
*Assistant (En)*: I can look that up on the eCourts offline database sync. Please provide your CNR number.
*Citizen (Hi)*: मेरे अदालती मामले की स्थिति क्या है?
*Assistant (Hi)*: मैं eCourts ऑफ़लाइन डेटाबेस सिंक पर इसे देख सकता हूँ। कृपया अपना CNR नंबर प्रदान करें।
*Citizen (Hinglish)*: Mere court case ka status kya hai?
*Assistant (Hinglish)*: Main eCourts offline database me check kar sakti hu. Apna CNR number bataiye.

**Example 14: Hospital Search**
*Citizen (En)*: Is there a hospital nearby?
*Assistant (En)*: Based on your offline location data, there is a district hospital 2 kilometers away. Shall I provide directions?
*Citizen (Hi)*: क्या आस-पास कोई अस्पताल है?
*Assistant (Hi)*: आपके ऑफ़लाइन स्थान डेटा के आधार पर, 2 किलोमीटर दूर एक जिला अस्पताल है। क्या मैं दिशा-निर्देश प्रदान करूँ?
*Citizen (Hinglish)*: Aas paas koi hospital hai kya?
*Assistant (Hinglish)*: Aapki offline location ke hisaab se 2 km door ek district hospital hai. Kya main directions du?

**Example 15: Voter ID**
*Citizen (En)*: Apply for a new Voter ID.
*Assistant (En)*: You can apply for a Voter ID using Form 6. Do you have your age and address proof ready?
*Citizen (Hi)*: नए वोटर आईडी के लिए आवेदन करें।
*Assistant (Hi)*: आप फॉर्म 6 का उपयोग करके वोटर आईडी के लिए आवेदन कर सकते हैं। क्या आपके पास अपनी आयु और पते का प्रमाण तैयार है?
*Citizen (Hinglish)*: Naya voter ID banwana hai.
*Assistant (Hinglish)*: Aap Form 6 use karke Voter ID apply kar sakte hain. Kya aapke paas age aur address proof ready hai?

## Government Services & National Portals
- **Banking**: RBI Guidelines Portal
- **Legal**: eCourts India Services
- **Medical**: eSanjeevani, Ayushman Bharat
- **Public Admin**: UIDAI (Aadhaar), Passport Seva, Election Commission of India

## Search Optimization
**English Keywords**: Intent dictionary, Saarthi AI intents, NLU mapping, offline AI understanding, banking intents, legal intents, medical intents, public admin intents, citizen queries, user intent recognition.
**Hindi Keywords**: इंटेंट डिक्शनरी, सारथी एआई इंटेंट, NLU मैपिंग, ऑफ़लाइन एआई समझ, बैंकिंग इंटेंट, कानूनी इंटेंट, चिकित्सा इंटेंट, सार्वजनिक प्रशासन इंटेंट, उपयोगकर्ता इरादा।
**Hinglish Keywords**: Intent map, Saarthi intents, user kya chahta hai, NLU intents, query routing, offline AI keywords.
**Abbreviations**: NLU, NLP, Intent Map, KB, UIDAI.
**Synonyms**: User Goal Registry, Action Map, Intent Database.

## Intent Mapping
- `common_greeting` -> Routes to Greeting Module
- `common_fallback` -> Routes to Clarification Module
- `bank_*` -> Routes to Local Banking APIs
- `legal_*` -> Routes to Local Legal KB
- `medical_*` -> Routes to Local Medical KB
- `admin_*` -> Routes to Local Public Admin KB

## Retrieval Tags
`intent_mapping`, `saarthi_core`, `nlp_dictionary`, `banking_intents`, `legal_intents`, `medical_intents`, `public_admin_intents`, `user_goal`, `dialogue_management`, `offline_ai`, `hindi_nlu`, `hinglish_nlu`, `multilingual_intents`, `intent_classification`, `utterances`, `fallback_intent`, `greeting_intent`, `bank_check_balance`, `bank_apply_loan`, `bank_block_card`, `legal_file_fir`, `legal_know_rights`, `medical_book_appointment`, `medical_first_aid`, `admin_apply_passport`, `admin_download_aadhar`, `intent_confidence`, `nlu_engine`, `saarthi_assistant`, `query_understanding`, `text_classification`, `intent_registry`, `master_dictionary`, `intent_id`, `entity_extraction`, `system_action`, `workflow_trigger`, `api_trigger`, `knowledge_base_fetch`, `offline_processing`, `data_privacy`, `local_ai`, `edge_ai`, `intent_training`, `code_mixed_data`, `hindi_nlp`, `indian_languages`, `bharat_ai`, `voice_assistant`, `text_assistant`, `intent_architecture`, `nlu_framework`, `intent_logs`, `debug_intent`, `intent_verification`, `secondary_auth`, `secure_intents`, `health_info`, `civic_services`, `e_governance`, `digital_india`, `smart_assistant`, `conversational_ai`, `bot_framework`, `virtual_agent`, `intent_resolution`, `intent_disambiguation`, `intent_hierarchy`, `primary_intent`, `sub_intent`, `cross_lingual`, `language_switch`, `intent_update`, `offline_patch`, `sync_point`, `intent_accuracy`, `intent_testing`, `utterance_corpus`, `training_data`, `intent_model`, `lightweight_ai`, `embedded_ai`, `mobile_ai`, `intent_routing`, `action_mapping`, `intent_parameters`, `intent_slots`, `slot_filling`, `intent_context`, `context_management`, `dialogue_state`, `state_tracker`, `intent_policy`, `rule_based_intent`, `ml_intent`, `hybrid_nlu`, `intent_confidence_score`, `threshold_tuning`, `intent_overlap`, `intent_collision`, `intent_metrics`.

## Cross-References
- [Multilingual Synonym Glossary](common/glossary.md)
- [Banking Knowledge Base](banking/overview.md)
- [Legal Knowledge Base](legal/overview.md)
- [Medical Knowledge Base](medical/overview.md)
- [Public Administration Knowledge Base](public_admin/overview.md)

## See Also
- Saarthi NLU Training Guide
- Offline Dialogue Management Best Practices
- Entity Resolution Framework

## References
1. Saarthi AI Internal Documentation (2026). NLU Intent Design Guidelines.
2. India AI Stack Standards for Offline Processing.
3. Conversational AI Best Practices for Multilingual Contexts.

## Disclaimer
This Master Intent Dictionary is proprietary to Saarthi AI and is strictly meant for the internal NLU processing engine of the offline AI assistant. The mapping definitions provided here are subject to quarterly updates and are designed exclusively to provide informational and administrative assistance to citizens. The system does not replace professional medical diagnoses, legal counsel, or direct banking verification.
---
