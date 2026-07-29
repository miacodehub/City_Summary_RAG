# City_Summary_RAG
A RAG pipeline that generates a summary of a city based on user query

## Problem Statement

When choosing where to travel, people are confused by which location to visit first


## Solution

The solution is to have RAG create a short summary of the city user selected. This summary contains two elements:
1. The query: Users, in this case travelers, prefer to look for places with a certain vibe. The query here asks the user's input for the vibe they're looking for and uses that to create summaries of the cities.
2. City Summary : Cities can be summarized in a variety of ways. Once the user enters a vibe, the summary can be modified to show how well it fits the vibe the user entered.

A Retrieval Augmented Generation system works well in this use case because it can provide summaries more accurate to what the user needs by creating embeddings of both the user query and the summary of a prticular city.


## Entities

The core entities for this project are simple. 
A city name, a user query, and a RAG model

## Implementation

  - Data Ingestion:
  - Chunking:
  - Embedding:
  - FAISS Index
  - Retrieval
  - Summary:

## Other details

While the base product is 

### Indexing










