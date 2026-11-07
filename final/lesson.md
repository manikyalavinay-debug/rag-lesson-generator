# Introduction to RAG

## Start with a familiar problem

Imagine you need to find the closing time of the college library. You could search the library website or ask a librarian, right?

## What is RAG?

RAG stands for Retrieval-Augmented Generation. Let’s break it down: ‘Retrieval’ means finding relevant information – like searching for something online. ‘Augmented’ means enhanced or improved. ‘Generation’ means creating something new, like an answer to a question. So, RAG combines finding information and then using that information to create an answer.

## Why it helps

RAG helps because sometimes, a regular computer program (a ‘model’) doesn’t have all the information it needs to answer a question. RAG gives the model extra facts to work with, making its answers more accurate and complete.

## Prepare the documents

To use RAG, we first need to prepare the information. This means organizing documents – like the college timetable – into smaller pieces called ‘chunks’. We then create ‘embeddings’ for each chunk. Think of embeddings as lists of numbers that represent the meaning of each chunk. These embeddings are stored in a ‘vector store’ which allows us to quickly find chunks similar to a question.

## How it works

The process works like this: 1. **Ask:** You give the system a question. 2. **Find:** The system uses the embeddings to find the most relevant chunks in the vector store. 3. **Read:** The system takes those chunks as context. 4. **Answer:** The system uses the context to generate an answer. This is why it’s called ‘Retrieval-Augmented Generation’.

Importantly, RAG doesn’t usually change the model’s internal settings (weights). It just provides extra information.

## Words explained

- **Model:** A computer program designed to understand and generate text. It’s like a student learning from examples.

- **Chunk:** A small piece of a document that’s been split into smaller parts.

- **Embeddings:** Lists of numbers that represent the meaning of text. They allow computers to compare the similarity of words and phrases.

- **Vector Store:** A database specifically designed to store and quickly search through embeddings.

- **Keyword Retrieval:** Finding information based on specific words or phrases.

- **Weights:** Settings within a model that determine how it processes information.

## A fictional worked example

**Made-up source [Note A]:** The college library closes at 1 pm on Saturday. It is closed on Sunday.

**Question:** When does the college library close on Saturday?

**Retrieved text [Note A]:** The college library closes at 1 pm on Saturday. It is closed on Sunday.

**Answer:** The college library closes at 1 pm on Saturday. [Note A] [Note A]

**A question the note cannot answer:** What time does the library open on a public holiday?

**Response when evidence is missing:** The note does not contain this information.

## What can go wrong?

- Retrieval can miss relevant information.

- The information provided might be outdated.

## Try it yourself

Based on the provided information, what is the library’s closing time on Sunday?

**Answer:** The library is closed on Sunday.

## Quick check

1. What does RAG stand for?

**Answer:** Retrieval-Augmented Generation

2. What is a ‘chunk’ in the context of RAG?

**Answer:** A small piece of a document.

## Remember

Today, we learned about RAG. It’s a way to improve answers by finding relevant information and giving it to the model. Remember, RAG doesn’t guarantee correct answers and relies on the quality of the information it retrieves. Always check the source of information!
