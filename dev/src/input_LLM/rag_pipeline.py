# # rag_pipeline.py
# from web_scraping import DisasterNewsScraper  # Your scraper class
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# from huggingface_hub import InferenceClient
# from reliable_sources import reliable_news_sources  # Your sources dict

# class RAGPipeline:
#     def __init__(self, hf_token, embedder_model='all-mpnet-base-v2'):
#         self.scraper = DisasterNewsScraper(reliable_news_sources)
#         self.embedder = SentenceTransformer(embedder_model)  # Multilingual embeddings
#         self.index = None
#         self.texts = []
#         self.client = InferenceClient(token=hf_token)

#     # def build_index(self, category=None, max_items_per_site=5):
#     #     """Scrape and index text chunks for RAG."""
#     #     news_data = self.scraper.scrape_all(category)
#     #     all_texts = []
#     #     for cat, sites in news_data.items():
#     #         for source, articles in sites.items():
#     #             if isinstance(articles, list):
#     #                 for article in articles[:max_items_per_site]:  # Limit per site
#     #                     # Chunk title + summary into smaller pieces if needed
#     #                     combined = f"{article['title']}\n{article['summary']}"
#     #                     chunks = [combined[i:i+500] for i in range(0, len(combined), 500)]  # Chunk to ~500 chars
#     #                     all_texts.extend(chunks)
#     #     self.texts = all_texts
#     #     if not all_texts:
#     #         raise ValueError("No text scraped to index.")
#     #     embeddings = self.embedder.encode(all_texts, convert_to_numpy=True)
#     #     dimension = embeddings.shape[1]
#     #     self.index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
#     #     self.index.add(embeddings)
#     def build_index(self, category=None, max_items_per_site=5):
#         """Scrape and index text chunks for RAG."""
#         news_data = self.scraper.scrape_all(category)
#         all_texts = []
#         for cat, sites in news_data.items():
#             for source, articles in sites.items():
#                 if isinstance(articles, list):
#                     for article in articles[:max_items_per_site]:  # Limit per site
#                         title = article.get('title', '')
#                         summary = article.get('summary', '')
#                         if not summary:  # Fallback if summary missing
#                             status = article.get('status', 'N/A')
#                             country = article.get('country', 'N/A')
#                             summary = f"Status: {status}\nCountry: {country}"
#                         combined = f"{title}\n{summary}".strip()
#                         if combined:  # Skip if still empty
#                             chunks = [combined[i:i+500] for i in range(0, len(combined), 500)]  # Chunk to ~500 chars
#                             all_texts.extend(chunks)
#         self.texts = all_texts
#         if not all_texts:
#             raise ValueError("No text scraped to index.")
#         embeddings = self.embedder.encode(all_texts, convert_to_numpy=True)
#         dimension = embeddings.shape[1]
#         self.index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
#         self.index.add(embeddings)

#     def retrieve(self, query, top_k=5):
#         """Retrieve top-k relevant text chunks."""
#         if self.index is None:
#             raise ValueError("Index not built. Call build_index first.")
#         q_emb = self.embedder.encode([query], convert_to_numpy=True)
#         distances, indices = self.index.search(q_emb, top_k)
#         return [self.texts[i] for i in indices[0] if i < len(self.texts)], distances[0]

#     def generate_summary(self, query, locality="Global", max_new_tokens=300):
#         """Generate summary and actions using retrieved context via HF API."""
#         self.build_index(category=locality)  # Rebuild index for locality
#         retrieved_texts, scores = self.retrieve(query, top_k=5)
#         context = "\n\n".join([f"Snippet {i+1} (score: {scores[i]:.2f}): {text}" for i, text in enumerate(retrieved_texts)])
#         prompt = (
#             f"You are an expert in disaster management. Using the following multilingual news context, "
#             f"summarize key problems in {locality} related to: {query}. "
#             f"Provide actionable recommendations for governments and NGOs in bullet points. "
#             f"Be concise, factual, and suggest mitigation strategies. If context is limited, note it. "
#             f"Context:\n{context}"
#         )
#         try:
#             response = self.client.text_generation(
#                 model="swiss-ai/Apertus-8B-Instruct-2509",
#                 inputs=prompt,
#                 max_new_tokens=max_new_tokens
#             )
#             return response['generated_text']
#         except Exception as e:
#             return f"Error generating summary: {e}"

# # # Test block for rag_pipeline.py
# # if __name__ == "__main__":
# #     HF_TOKEN = "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"  # Your token
# #     rag_pipeline = RAGPipeline(HF_TOKEN)
# #     query = "flooding issues"  # Example query
# #     locality = "Asia"  # Example locality (maps to your sources category)
# #     result = rag_pipeline.generate_summary(query, locality)
# #     print("Summary and Actions:\n", result)

# # Add this to rag_pipeline.py (e.g., after the class definition)

# # def test_scraper_and_retrieval(rag_pipeline, locality='Asia', query='flooding'):
# #     # Step 1: Test scraping
# #     news_data = rag_pipeline.scraper.scrape_all(category=locality)
# #     print(f"Scraped news sources in {locality}:")
# #     for cat, sites in news_data.items():
# #         for source, articles in sites.items():
# #             if isinstance(articles, list):
# #                 print(f"- Source: {source}, # Articles: {len(articles)}")
# #                 for i, article in enumerate(articles[:2]):  # Print first 2 articles for brevity
# #                     print(f"  {i+1}. Title: {article['title']}")
# #                     print(f"     Summary: {article['summary'][:100]}...")  # Truncate long summaries

# #     # Step 2: Test building index
# #     rag_pipeline.build_index(category=locality)
# #     print(f"\nBuilt index with {len(rag_pipeline.texts)} text chunks.")

# #     # Step 3: Test retrieval
# #     retrieved_texts, scores = rag_pipeline.retrieve(query, top_k=3)
# #     print(f"\nTop 3 retrieved chunks for query '{query}':")
# #     for i, (text, score) in enumerate(zip(retrieved_texts, scores)):
# #         print(f"{i+1}. (Score: {score:.3f}) {text[:150]}...")  # Truncate for readability

# # # To run the test, add or modify your main block like this:
# # if __name__ == "__main__":
# #     HF_TOKEN = "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"  # Your token
# #     rag_pipeline = RAGPipeline(HF_TOKEN)
# #     test_scraper_and_retrieval(rag_pipeline, locality='Asia', query='flooding')  # Run the test
# #     # Optionally uncomment to test full summary:
# #     # result = rag_pipeline.generate_summary("flooding issues", locality="Asia")
# #     # print("Summary and Actions:\n", result)



# if __name__ == "__main__":
#     HF_TOKEN = "YOUR_HF_TOKEN"          # only needed later for LLM
#     rag = RAGPipeline(HF_TOKEN)

#     # 1️⃣ Scrape just one working URL first
#     test_url = "https://reliefweb.int/disasters"
#     print("Testing single URL:", test_url)
#     print(rag.scraper.scrape_site(test_url, max_items=3), "\n")

#     # 2️⃣ Full scrape for the chosen locality
#     locality = "Asia"
#     news = rag.scraper.scrape_all(category=locality)
#     print(f"Articles scraped for {locality}:")
#     for src, arts in news[locality].items():
#         print(f"  {src}: {len(arts)}")

#     # 3️⃣ Build index only if some text exists
#     rag.build_index(category=locality)
#     print("Chunks indexed:", len(rag.texts))

#     # 4️⃣ Retrieve for a sample query
#     docs, scores = rag.retrieve("flood", top_k=3)
#     for d, s in zip(docs, scores):
#         print(f"{s:.3f} -> {d[:120]}…")


# rag_pipeline.py
from web_scraping import DisasterNewsScraper
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from huggingface_hub import InferenceClient
from reliable_sources import reliable_news_sources  # Corrected import name if needed

class RAGPipeline:
    def __init__(self, hf_token, embedder_model='all-mpnet-base-v2'):
        self.scraper = DisasterNewsScraper(reliable_news_sources)
        self.embedder = SentenceTransformer(embedder_model)
        self.index = None
        self.texts = []
        self.client = InferenceClient(token=hf_token)

    def build_index(self, category=None, max_items_per_site=5):
        """Scrape and index text chunks for RAG."""
        news_data = self.scraper.scrape_all(category)
        all_texts = []
        for cat, sites in news_data.items():
            for source, articles in sites.items():
                if isinstance(articles, list):
                    for article in articles[:max_items_per_site]:
                        title = article.get('title', '')
                        summary = article.get('summary', '')
                        if not summary:  # Fallback for sites like ReliefWeb
                            status = article.get('status', 'N/A')
                            country = article.get('country', 'N/A')
                            summary = f"Status: {status}\nCountry: {country}"
                        combined = f"{title}\n{summary}".strip()
                        if combined:
                            chunks = [combined[i:i+500] for i in range(0, len(combined), 500)]
                            all_texts.extend(chunks)
        self.texts = all_texts
        if not all_texts:
            raise ValueError("No text scraped to index.")
        embeddings = self.embedder.encode(all_texts, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def retrieve(self, query, top_k=5):
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(q_emb, top_k)
        return [self.texts[i] for i in indices[0] if i < len(self.texts)], distances[0]

    def generate_summary(self, query, locality="Global", max_new_tokens=300):
        self.build_index(category=locality)
        retrieved_texts, scores = self.retrieve(query, top_k=5)
        context = "\n\n".join([f"Snippet {i+1} (score: {scores[i]:.2f}): {text}" for i, text in enumerate(retrieved_texts)])
        prompt = (
            f"You are an expert in disaster management. Using the following multilingual news context, "
            f"summarize key problems in {locality} related to: {query}. "
            f"Provide actionable recommendations for governments and NGOs in bullet points. "
            f"Be concise, factual, and suggest mitigation strategies. If context is limited, note it. "
            f"Context:\n{context}"
        )
        try:
            response = self.client.text_generation(
                model="swiss-ai/Apertus-8B-Instruct-2509",
                inputs=prompt,
                max_new_tokens=max_new_tokens
            )
            return response['generated_text']
        except Exception as e:
            return f"Error generating summary: {e}"

# Test block
if __name__ == "__main__":
    HF_TOKEN = "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"  # Your token
    rag = RAGPipeline(HF_TOKEN)

    # 1. Scrape just one working URL first
    test_url = "https://reliefweb.int/disasters"
    print("Testing single URL:", test_url)
    print(rag.scraper.scrape_site(test_url, max_items=3), "\n")

    # 2. Full scrape for the chosen locality
    locality = "Asia"
    news = rag.scraper.scrape_all(category=locality)
    print(f"Articles scraped for {locality}:")
    for src, arts in news[locality].items():
        print(f"  {src}: {len(arts)}")
        for art in arts[:2]:  # Print sample articles
            print(f"    - {art['title']} (Status: {art.get('status', 'N/A')}, Country: {art.get('country', 'N/A')})")

    # 3. Build index only if some text exists
    rag.build_index(category=locality)
    print("Chunks indexed:", len(rag.texts))

    # 4. Retrieve for a sample query
    docs, scores = rag.retrieve("flood", top_k=3)
    for d, s in zip(docs, scores):
        print(f"{s:.3f} -> {d[:120]}…")

    # Uncomment to test full summary
    # result = rag.generate_summary("flooding issues", locality="Asia")
    # print("Summary and Actions:\n", result)
