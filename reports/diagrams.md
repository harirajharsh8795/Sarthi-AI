# 📊 Saarthi AI Diagrams for Presentation

Here are the visual diagrams you can use for your presentation. You can take a screenshot of these rendered diagrams and paste them directly into your PDF, or copy the mermaid code if you are using a markdown-to-pdf tool.

## 1. System Architecture (For Page 6)

```mermaid
flowchart LR
    %% Colors and Styles
    classDef input fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#000
    classDef ui fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000
    classDef slm fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#000
    classDef data fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000
    classDef deploy fill:#ffebee,stroke:#d32f2f,stroke-width:2px,color:#000
    classDef output fill:#e0f7fa,stroke:#0097a7,stroke-width:2px,color:#000

    %% User Input
    subgraph Input ["User Input"]
        A1("Text Chat")
        A2("Hindi/Eng Voice")
        A3("Camera / Upload")
    end
    Input:::input

    %% App UI
    B("App / UI\n(React + Vite, SSE Stream)"):::ui

    %% Agent Logic
    subgraph AgentLogic ["SLM / Agent Logic (11-Stage RAG)"]
        direction TB
        C1("1. Prompt Guard & PII Redaction")
        C2("2. Intent & Query Rewrite")
        C3("3. Hybrid Retrieval")
        C4("4. Reranking & Context Compress")
        C5("5. Adaptive Prompt Build")
    end
    AgentLogic:::slm

    %% Tools / DB
    subgraph Database ["Tools / RAG / Database"]
        D1[("ChromaDB Vector Store")]
        D2[("BM25 Index")]
        D3[("Knowledge Graph")]
        D4("OCR & Whisper STT")
    end
    Database:::data

    %% Deployment
    E{"Jetson Deployment\n(Orin Nano, Ollama Llama 3.2 1B)"}:::deploy

    %% Output
    F("Output\n(Cited Response, Confidence Badge, Audio)"):::output

    %% Flow
    Input --> B
    B --> AgentLogic
    AgentLogic <--> Database
    AgentLogic --> E
    E --> F
```

---

## 2. Input → Processing → Output Workflow (For Page 5)

```mermaid
flowchart TD
    classDef process fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
    classDef startend fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#000

    Start(["📥 INPUT\nUser asks query (Text/Voice/Image)"]):::startend
    
    Start --> P1
    
    subgraph Processing ["⚙️ 11-Stage Processing Pipeline"]
        direction TB
        P1("Security & Privacy Check\n(Prompt Guard + PII Redaction)"):::process
        P2("Query Understanding\n(Intent, Domain, Language Detect)"):::process
        P3("Context Retrieval\n(Hybrid Vector+BM25 Search)"):::process
        P4("Evaluation\n(Reranking, KG Extraction)"):::process
        P5("Generation\n(Local Llama 3.2 1B Inference)"):::process
        
        P1 --> P2 --> P3 --> P4 --> P5
    end

    P5 --> End(["📤 OUTPUT\nGrounded Markdown Answer with Page Citations\n+ Confidence Badge + Voice Audio"]):::startend
```

---

## 3. Upload & OCR Processing Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Frontend UI
    participant Q as Background Job Queue
    participant OCR as Multi-Tier OCR
    participant VDB as ChromaDB

    U->>UI: Uploads Document / Scans Photo
    UI->>Q: Queues document for processing
    Q->>OCR: Attempts Native Text Extraction
    alt Scanned Image/PDF
        OCR->>OCR: Upscales & Auto-contrasts image
        OCR->>OCR: Runs Tesseract (Eng+Hin)
        alt Low Confidence
            OCR->>OCR: Fallback to EasyOCR
        end
    end
    OCR->>VDB: Chunks Text & Calculates Embeddings
    VDB-->>UI: Sends 'Indexing Complete' status
    UI-->>U: Document Ready for Querying
```
