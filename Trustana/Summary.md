# What is trustana?
I’m currently a developer on the AI team at Trustana, a platform that helps businesses manage and enrich their product data for global trade. My work specifically focuses on leveraging Generative AI to automate the creation of high-quality product content. By implementing new AI technologies, I help ensure that the data we generate is not only scalable but also highly accurate and market-ready for our international clients.

for example, you are a retailer:

You might upload a 'messy' spreadsheet with thousands of products that only have basic name and brand (e.g., Iphone 17 - Apple).

AI-Driven Enrichment: Our AI identifies the product category and automatically generates a compelling, SEO-optimized description and structured attributes (like material, weight, chip and usage) based on the brand's specific tone and rules.

Accuracy & Attribution: This is where my team’s focus on accuracy comes in. We’ve built a Source Attribution layer where the AI tracks exactly where it found each piece of info, allowing the user to verify the data against trusted supplier feeds instead of just 'hallucinating' details.

Channel Syndication: Once validated, this accurate data is instantly formatted and pushed to multiple marketplaces like Amazon, Shopify, Shopee, or Lazada, reducing a process that used to take weeks down to just minutes.


## Task 1: Multi-modal Category Classification
*The Pitch*: "I built a *zero-shot classification* system that categorizes products by analyzing both visual and textual data at the same time, ensuring high accuracy even for products the system hasn't seen before."

*The Tech Stack*: "Inspired by *OpenAI’s CLIP* architecture, I developed a service that converts product names, brands, and images into unified multi-modal *embeddings*. We store these in a *Milvus vector database* to perform semantic searches, allowing for high-speed, zero-shot classification."

*Challenge*
1. *Solving for Accuracy*: "To minimize errors, I implemented a pre-processing layer where the AI performs real-time internet research to gather missing technical specs and extra images. This enriched context is 'fused' before embedding, significantly reducing misclassification."

2. *Solving for Scalability*: "To handle concurrency for hundreds of thousands of SKUs, I optimized the service architecture to process batches asynchronously, ensuring the system remains performant under heavy enterprise loads."

## Task 2: Automated Evaluation Framework (LLM-as-a-Judge)
*The Pitch*: "I established a automated benchmarking system to ensure that our AI enrichment remains accurate and compliant as we migrate across different LLM versions (from GPT-4o to GPT-5 variants)."

*The 'Judge' Architecture*: "I implemented an 'LLM-as-a-Judge' pattern, using a high-reasoning model to audit the output of our production models. This is integrated into an End-to-End (E2E) test suite, allowing us to quantify improvements or regressions instantly when we upgrade our core AI engines."
