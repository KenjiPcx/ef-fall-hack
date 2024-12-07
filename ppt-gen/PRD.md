# Product Requirements Document

## Overview

The product is a chatbot where the user can answer questions about a company's private documents, the AI can:
- generate a report based on the conversation, a report can have a combination of the following slides:
    - front page
    - executive summary
    - size and history forecast
    - growth drivers
    - risks
    - m&a consolidation
    - dynamics
    - profiles
- answer follow up questions
- include visual references from private documents
- include citations and further readings

## Workflow

1. User inputs question, could be a bundle of questions.
2. QueryBreakDownAgent will break down the question into smaller specific questions, also responsible for query expansion, figuring out what the user truly wants to know etc.
3. Based on the questions, decide which slides to have
4. Outline agent writes an outline for the report
5. Chosen slide agents will create content for the slides and go through 1 review process, it will save the source nodes for each slide
6. Slides are passed to a combiner agent to put the content together and generate the report

## Tech Implementation

### Tech Stack
- Next.js for the frontend
- LlamaIndex to ingest and query the documents
- Supabase for the backend
- FastAPI for the backend
- e2b for the code interpreter
- Use gpt-4o for the LLM

### Private Documents Search Tool
- Use LlamaIndex to ingest the documents


### Todos
- [ ] Modify the financial report workflow to fit one slide agent
    - [ ] Research and get the nodes -> Store in the context
    - [ ] Analyze agent -> Loads the context and does something with the interpreter tool -> Store the result in the context
    - [ ] Report agent -> Loads the context and put it into a report format in text
- [ ] Do the same for all the other slides
- [ ] Summarize into a frontslide and an executive summary