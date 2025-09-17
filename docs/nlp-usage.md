# How tref uses Natural Language Processing (NLP)

This document explains how `tref` leverages Natural Language Processing (NLP) to provide its semantic search functionality.

## Core NLP Components

The NLP capabilities of `tref` are primarily implemented in two files:

- `tref/embeddings.py`: Handles the conversion of text into numerical representations (embeddings).
- `tref/search.py`: Implements the semantic search functionality using these embeddings.

## Text Embeddings with `transformers`

`tref` uses the `transformers` library, a popular Python library for NLP, to generate vector embeddings from the text of the cheat sheets. Specifically, it uses the `BAAI/bge-small-en-v1.5` model, a pre-trained model that is effective at creating meaningful embeddings for semantic search tasks.

The process works as follows:

1.  **Loading the Model**: The `EmbeddingManager` in `tref/embeddings.py` loads the `BAAI/bge-small-en-v1.5` model and its corresponding tokenizer.
2.  **Text to Embeddings**: When the embeddings are updated (e.g., with `tref --update-embeddings`), the content of the cheat sheets is processed. Each entry (name and explanation) is fed into the model, which outputs a high-dimensional vector (a numerical representation) for that entry. These vectors are called embeddings.
3.  **Storing Embeddings**: These embeddings are stored in the `vectors.npy` file in the configuration directory.

## Semantic Search

The semantic search functionality allows `tref` to find cheat sheet entries that are conceptually related to your query, even if they don't share the exact keywords. This is a significant improvement over traditional keyword-based search.

Here's how it works:

1.  **Query Embedding**: When you perform a search (e.g., `tref --search git "how to go back to a previous commit"`), your query is also converted into an embedding using the same `BAAI/bge-small-en-v1.5` model.
2.  **Cosine Similarity**: The `SearchManager` in `tref/search.py` then calculates the [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) between your query's embedding and the embeddings of all the cheat sheet entries for the specified tool.
3.  **Ranking Results**: The entries with the highest cosine similarity scores are the most semantically related to your query, and they are presented as the search results.

## Benefits of this Approach

- **Conceptual Matching**: Instead of just matching keywords, semantic search understands the meaning behind the query and the cheat sheet entries.
- **Improved Accuracy**: This leads to more relevant and accurate search results.
- **Natural Language Queries**: You can phrase your queries in natural language, as if you were asking a question.
