# Records API plugin for Pinecone python SDK

## Installation

The plugin is distributed separately from the core python SDK.

```
# Install the base python SDK, version 5.4.0 or higher
pip install pinecone

# And also the plugin functionality
pip install pinecone-plugin-records
```

## Usage

This plugin extends the functionality of the `pinecone` SDK to allow creating indexes for specific embedding models, and upserting and searching records in these indexes. These operations are added to the existing `Pinecone` and `Index` classes.

Models currently supported:

- [multilingual-e5-large](https://arxiv.org/pdf/2402.05672)

## Create an index for an embedding model, upsert records, and search

The following example highlights how to use the `Pinecone` class to create a new index for an embedding model, and then uses `Index` to upsert and search some records.

```python
from pinecone import Pinecone

pc = Pinecone(api_key="<<PINECONE_API_KEY>>")

# Create an index for your embedding model
index_model = pc.create_index_for_model(
    name="my-model-index",
    cloud="aws",
    region="us-east-1",
    embed={
        "model":"multilingual-e5-large",
        "field_map": {"text": "my_text_field"}
    }
)

# establish an index connection
index = pc.Index(host=index_model.host)

# upsert records
index.upsert_records(
    "my-namespace",
    [
        {
            "_id": "test1",
            "my_text_field": "Apple is a popular fruit known for its sweetness and crisp texture.",
        },
        {
            "_id": "test2",
            "my_text_field": "The tech company Apple is known for its innovative products like the iPhone.",
        },
        {
            "_id": "test3",
            "my_text_field": "Many people enjoy eating apples as a healthy snack.",
        },
        {
            "_id": "test4",
            "my_text_field": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces.",
        },
        {
            "_id": "test5",
            "my_text_field": "An apple a day keeps the doctor away, as the saying goes.",
        },
        {
            "_id": "test6",
            "my_text_field": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership.",
        },
    ],
)

# search for similar records
response = index.search_records(
    namespace="test-namespace",
    query={
        "inputs":{
            "text": "Apple corporation",
        },
        "top_k":3,
    },
    rerank={
        "model": "bge-reranker-v2-m3",
        "rank_fields": ["my_text_field"],
        "top_n": 3,
    },
)
```
