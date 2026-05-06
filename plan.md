# Insurance RAG Assistant — Product Requirements

This document defines the requirements for a web-based Retrieval-Augmented Generation (RAG) tool designed to help Indian users navigate complex insurance policy manuals (Health, Life, Motor) and IRDAI regulations.

## Product Vision

An AI-powered assistant that translates dense Indian insurance jargon into plain English/Hinglish. The tool allows users to query pre-loaded Indian policy sets or upload their own specific policy manuals to get cited, legally-grounded answers regarding claims, exclusions, and coverage.

## Core User Experience

The application presents a three-column layout:

-   **Source Vault (Left):** Management of active documents. Shows pre-loaded Indian policy standards (e.g., LIC, HDFC Ergo, Star Health) and user-uploaded PDFs. Displays "Indexing" status for new files.
    
-   **Query Console (Center):** The primary chat interface. Users input questions (e.g., "Is robotic surgery covered?"). It displays the "Retrieval Chain" (what clauses were found) before showing the final answer.
    
-   **Insight & Verification (Right):** Real-time display of specific PDF snippets used to generate the answer, with page numbers and a  that explains IRDAI-specific terms found in the text.
- ## 1. Document & Knowledge Management

**Source Types:**

    
-   **User Uploads:** Custom PDF manuals provided by the user.
    
-   **IRDAI Regulatory Feed:** Master circulars regarding claim settlement ratios and standardized exclusions fetch from web using tavily api .
    

**Document Properties:**

-   **Insurer Name:** (e.g., "ICICI Lombard")
    
-   **Policy Category:** (Health, Term, Life, Motor, Travel)
    
-   **Effective Date:** Critical for Indian policies due to changing IRDAI norms.

    

**Operations:**

-   Upload PDF (triggers background TaskIQ).
-   Delete custom manuals.
- ## 2. Query & Retrieval Logic

**Query Categories:**

-   **Eligibility:** "Am I covered for pre-existing diseases after 2 years?"
    
-   **Claim Process:** "What documents are needed for a cashless claim?"
    
-   **Exclusions:** "Does this policy cover sports injuries?"
    
-   **Limit Check:** "What is the sub-limit for room rent?"
    

**The Retrieval Loop:**

-   **Semantic Search:** Finds top-$k$ relevant chunks using embeddings 
    
-   **Reranking:** Re-orders chunks to ensure Indian-specific nuances (like "Waiting Periods") are prioritized.
    
-   **Context Assembly:** Bundles the top 3–5 chunks with the user's query.
- ## 3. Answer Generation & Citations

**AI Answer Engine:**

-   Generates a concise response using LLMs (Groq Api).
    
-   **Tone:** Empathetic yet factual (Peer-to-peer style).
    
    

**Citation System:**

-   **Direct Links:** Clicking a citation opens the Right Column to the exact page/paragraph.
    
    
-   **Hallucination Guard:** If the answer is not in the manual, the system must state: "This information is not present in the provided policy documents."
- ## 5. Data Model

**Manuals Table (`policy_manuals`):**

-   `id`: Primary key.
    
-   `file_hash`: To prevent duplicate processing.
    
-   `insurer`: String.
    
-   `category`: Enum (Health, Life, etc.).
    
-   `vector_collection_id`: Reference to Qdrant
    

**Chat History Table (`query_logs`):**

-   `id`: Primary key.
    
-   `query_text`: User input.
    
-   `response_text`: AI output.
    
-   `sources_used`: JSON array of document IDs and page numbers.
    
-   `feedback`: Thumb up/down for RAG accuracy.
- ## 6. Technical Constraints

-   **File Processing:** Use `PyMuPDF` or `Unstructured` for PDF parsing.
    
-   **Background Workers:** Use **TaskIQ** (Windows-friendly) to handle heavy embedding tasks.
    
- **Vector DB:**  **Qdrant** for storing policy embeddings.
    
-   **Privacy:** Automatic scrubbing of Personal Identifiable Information (PII) like Policy Numbers or Names before sending to LLM.
    
-   **Latency:** Response time should be under 5 seconds for a "fast response" experience.