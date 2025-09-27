# rag_pipeline.py
from web_scraping import DisasterNewsScraper  # Your scraper class
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import openai
import os
from reliable_sources import reliable_news_sources  # Your sources dict


class RAGPipeline:
    def __init__(self, embedder_model='all-mpnet-base-v2'):
        self.scraper = DisasterNewsScraper(reliable_news_sources)
        self.embedder = SentenceTransformer(embedder_model)  # Multilingual embeddings
        self.index = None
        self.texts = []
        self.client = openai.OpenAI(
            api_key=os.getenv("SWISSCOM_API"),
            base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
        )


    # def build_index(self, category=None, max_items_per_site=5):
    #     """Scrape and index text chunks for RAG."""
    #     news_data = self.scraper.scrape_all(category)
    #     all_texts = []
    #     for cat, sites in news_data.items():
    #         for source, articles in sites.items():
    #             if isinstance(articles, list):
    #                 for article in articles[:max_items_per_site]:  # Limit per site
    #                     title = article.get('title', '')
    #                     summary = article.get('summary', '')
    #                     if not summary:  # Fallback if summary missing
    #                         status = article.get('status', 'N/A')
    #                         country = article.get('country', 'N/A')
    #                         summary = f"Status: {status}\nCountry: {country}"
    #                     combined = f"{title}\n{summary}".strip()
    #                     if combined:  # Skip if still empty
    #                         chunks = [combined[i:i+500] for i in range(0, len(combined), 500)]  # Chunk to ~500 chars
    #                         all_texts.extend(chunks)
    #     self.texts = all_texts
    #     if not all_texts:
    #         raise ValueError("No text scraped to index.")
    #     embeddings = self.embedder.encode(all_texts, convert_to_numpy=True)
    #     dimension = embeddings.shape[1]
    #     self.index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
    #     self.index.add(embeddings)

    def build_index(self, category=None, max_items_per_site=5):
        """Scrape and index text chunks for RAG. Handles no category by flattening all data."""
        news_data = self.scraper.scrape_all(category)  # Pass category if provided
        all_texts = []
        if category:
            # Use specific category if provided (existing behavior)
            data_source = news_data.get(category, {})
        else:
            # Flatten all data when no category (aggregate across all)
            data_source = {}
            for cat, sites in news_data.items():
                for source, articles in sites.items():
                    if isinstance(articles, list):
                        if source not in data_source:
                            data_source[source] = []
                        data_source[source].extend(articles)
        
        for source, articles in data_source.items():
            if isinstance(articles, list):
                for article in articles[:max_items_per_site]:  # Limit per site
                    title = article.get('title', '')
                    summary = article.get('summary', '')
                    if not summary:  # Fallback if summary missing
                        status = article.get('status', 'N/A')
                        country = article.get('country', 'N/A')
                        summary = f"Status: {status}\nCountry: {country}"
                    combined = f"{title}\n{summary}".strip()
                    if combined:  # Skip if still empty
                        chunks = [combined[i:i+500] for i in range(0, len(combined), 500)]  # Chunk to ~500 chars
                        all_texts.extend(chunks)
        self.texts = all_texts
        if not all_texts:
            raise ValueError("No text scraped to index.")
        embeddings = self.embedder.encode(all_texts, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
        self.index.add(embeddings)

    def retrieve(self, query, top_k=5):
        """Retrieve top-k relevant text chunks."""
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(q_emb, top_k)
        return [self.texts[i] for i in indices[0] if i < len(self.texts)], distances[0]


    def generate_summary(self, query, locality="Global", max_new_tokens=300):
        """Generate summary and actions using retrieved context via Swisscom API."""
        self.build_index(category=locality)  # Rebuild index for locality
        retrieved_texts, scores = self.retrieve(query, top_k=5)
        context = "\n\n".join([f"Snippet {i+1} (score: {scores[i]:.2f}): {text}" for i, text in enumerate(retrieved_texts)])
        sys_msg = (
            "You are an expert in disaster management. Be concise, factual, and suggest mitigation strategies. "
            "If context is limited, note it."
        )
        user_msg = (
            f"Using the following multilingual news context, "
            f"summarize key problems in {locality} related to: {query}. "
            f"Provide actionable recommendations for governments and NGOs in bullet points. "
            f"Context:\n{context}"
        )
        try:
            resp = self.client.chat.completions.create(
                model="swiss-ai/Apertus-70B",
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=max_new_tokens
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {e}"


# Test block
if __name__ == "__main__":
    rag = RAGPipeline()

    # 1. Scrape just one working URL first
    test_url = "https://reliefweb.int/disaster/wf-2025-000163-bol"
    print("Testing single URL:", test_url)
    print(rag.scraper.scrape_site(test_url, max_items=3), "\n")

    # 2. Full scrape for the chosen locality
    locality = "Asia"
    news = rag.scraper .scrape_all(category=locality)
    print(f"Articles scraped for {locality}:")
    for src, arts in news.get(locality, {}).items():
        count = len(arts) if isinstance(arts, list) else 0
        print(f"  {src}: {count}")
        if isinstance(arts, list):
            for art in arts[:2]:
                title = art.get('title') or art.get('section_title') or '(No Title)'
                status = art.get('status') or art.get('description') or art.get('section_content') or 'N/A'
                country = art.get('country') or 'N/A'
                print(f"    {title} (Status: {status}, Country: {country})")

    # 3. Build index only if some text exists
    rag.build_index(category=locality)
    print("Chunks indexed:", len(rag.texts))

    # 4. Retrieve for a sample query
    docs, scores = rag.retrieve("flood", top_k=3)
    for d, s in zip(docs, scores):
        print(f"{s:.3f} -> {d[:120]}…")

    # Test full summary
    # result = rag.generate_summary("flooding issues", locality="Asia")
    # print("Summary and Actions:\n", result)
