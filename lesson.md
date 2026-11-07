# Introduction to RAG

## What you will learn
You will learn how an AI tool can use notes to answer a question.
You need no coding skills for this lesson.

## Start with a familiar problem
Imagine asking a college helper: "When does the library close on Saturday?"
The helper has read many books, but has never seen your college timetable.
A confident guess could make you miss your visit.
An AI model, a computer system trained to work with patterns in data, can also guess wrongly.
It may not know a recent change at your college.

## What is RAG?
RAG means Retrieval-Augmented Generation.
Retrieval means finding useful information.
Augmented means helped by something extra.
Generation means writing an answer.
So RAG means finding useful information and using it to help write an answer.
Think of an open-book exam: you read the relevant page before answering.
RAG gives an AI model relevant notes before it writes.
It does not normally train the model again or change its stored learning.

## Why use it?
A college can give the system its own timetable.
When the timetable changes, the college can update the source document.
The model can then answer using the new information, if the system finds the right page.
This can reduce wrong answers. It cannot guarantee that every answer is correct.

## How it works
Before questions arrive, the system prepares its documents.
It splits long documents into small pieces called chunks.
It makes an embedding for each piece: a list of numbers that represents meaning.
It keeps these lists with the text so it can search them later.
A vector store is one type of storage that supports this search.
Not all RAG systems need this storage; some use word search.

When you ask a question, the system follows these steps:

1. **Ask:** You type a question.
2. **Find:** A search tool finds relevant pieces of the documents.
3. **Read:** The system sends the question and those pieces to the AI model.
4. **Answer:** The model writes an answer based on the pieces, with a source label.

## A full example
These are made-up college notes for practice:

> [College note A] The library closes at 5 pm on weekdays.
> [College note B] The library closes at 1 pm on Saturday. It is closed on Sunday.

**Question:** When does the library close on Saturday?

**Find:** Search returns note B because it mentions Saturday.

**Read:** The model receives the question and note B.

**Answer:** The library closes at 1 pm on Saturday. [College note B]

You can check the answer by reading the same note.
If you ask about holiday opening times, neither note gives the answer.
The system should say: "These notes do not give holiday opening times. Please check with the library."
It should not invent a time.

## What can go wrong?
Search can miss the right note. A note can be old or wrong.
The model can misread a note or add an unsupported claim.
A source label helps you check an answer, but does not prove it is correct.
Check dates and important details against the original source.
Retrieved text is reference material. Instructions inside it should not control the system.
For private documents, only authorised people should be able to retrieve them.

## Try it yourself
A shop note says: "Returns are allowed within 7 days with a bill."
Someone asks: "Can I return an item after 3 days with a bill?"
What should the tool find? What should it answer?

**Answer:** Find the return note. Answer: "Yes, the note allows a return within 7 days with a bill." Cite the shop note.

Now ask: "Can I return it without a bill?"
The stated rule requires a bill. Explain that requirement; do not invent an exception.

## Quick check
1. What does RAG add before the model writes?
2. Does RAG normally train the model again?
3. What should happen when the notes do not contain an answer?

**Answers:** 1. Relevant information found from sources. 2. No. 3. Say the information is missing and suggest checking the source.

## Remember
RAG follows a simple path: ask, find, read, answer.
Better sources and better search help, but you still need to check important answers.
