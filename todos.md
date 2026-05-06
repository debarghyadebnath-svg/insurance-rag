# Insurance RAG Assistant Development Plan (Next.js + FastAPI)

Each step below adds one complete, testable feature. After each step, verify the functionality as a user would before proceeding.

## Step 1: Initialize Workspace (Monorepo Style)

-   Set up a `/backend` folder with **FastAPI** and **TaskIQ**.
    
-   Set up a `/frontend` folder with **Next.js** (App Router) and javascript and **Tailwind CSS**.
    

## Step 2: Set up SQLite Database

-   Create `insurance_rag.db` within the backend.
    
-   Define `policy_manuals` table: `id`, `file_hash`, `insurer`, `category`, `vector_collection_id`.
    
-   Define `query_logs` table: `id`, `query_text`, `response_text`, `sources_used` (JSON).
    
-   **Verification**: Use a GET endpoint to return an empty list of manuals to the Next.js frontend.
    

## Step 3: Implement PyMuPDF Parsing Engine

-   In the backend, create a utility to extract text and page numbers using **PyMuPDF**.
    
-   Ensure strict **Type Hinting** for the extraction output (e.g., `List[Dict[str, Any]]`).
    
-   **Verification**: Run a backend test script to ensure a PDF's text is extracted with correct page metadata.
    

## Step 4: Configure TaskIQ Worker

-   Setup the TaskIQ broker (e.g., Redis) to handle asynchronous jobs.
    
-   Create a `process_policy_task` that accepts a file and updates the SQLite status.
    
-   **Verification**: Trigger a dummy task and see "Processing" log in the worker terminal.
    

## Step 5: Integrate LangChain & Qdrant

-   Implement LangChain’s `RecursiveCharacterTextSplitter` within the worker.
    
-   Connect to **Qdrant** and upsert vectors using an embedding model of Qdrant which is FastEmbed refer the documentation of the Qdrant or Source code
    
-   **Verification**: Use the Qdrant dashboard to confirm points are stored after a task completes.
    

## Step 6: Build Three-Column Next.js Layout

-   Create a main dashboard page using **Tailwind CSS** Grid.
    
-   **Left Column**: Source Vault (Document management).
    
-   **Center Column**: Query Console (Chat interface).
    
-   **Right Column**: Insight & Verification (Source viewer).
    
-   **Verification**: Confirm columns are fixed-width/responsive on your local browser.
    

## Step 7: Upload & Indexing Workflow

-   Build a file upload component in the Left Column using 
    
-   On upload, FastAPI should trigger the TaskIQ worker.
    
-   Use **SWR** or **React Query** to poll the status until "Indexing" changes to "Active."
    
-   **Verification**: Upload a PDF and see the status update in real-time on the UI.
    

## Step 8: Retrieval & Answer Logic

-   Create a POST endpoint in FastAPI for queries.
    
-   Use LangChain to retrieve relevant chunks from Qdrant and send them to **Groq/**.
    
-   Implement a **Hallucination Guard**: "If not in manual, say I don't know."
    
-   **Verification**: Ask "What is the room rent limit?" and see the raw response in the Center Column.
    

## Step 9: Delete Custom Manuals

-   Add a delete icon to manuals in the Source Vault.
    
-   Implement a backend route to purge the physical file, SQLite record, and Qdrant points.
    
-   **Verification**: Delete a manual and confirm it no longer influences the AI's answers.
    

## Step 10: Citation System & Page Links

-   Format the AI response to include clickable citations (e.g., `[Source 1, Page 5]`).
    
-   Map these citations to the unique IDs in your `policy_manuals` table.
    
-   **Verification**: Click a citation and verify the frontend captures the event.
    

## Step 11: Insight & Verification (Right Column)

-   Create a "Snippet Viewer" in the Right Column.
    
-   When a citation is clicked, fetch and display the exact text chunk and page number.
    
-   **Verification**: Ensure the right panel updates instantly when a chat citation is clicked.
    


    


## Step 14: Final Polish & Refinement

-   Add loading skeletons in Next.js for the chat and source list.
    
-   Ensure all backend functions use pure functional patterns where possible.
    
-   Final end-to-end test: Upload -> Index -> Query -> Verify Source.