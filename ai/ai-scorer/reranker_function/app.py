import os
import logging
import cohere
import requests

from typing import List, Dict, Any, Tuple
from cohere_untils import filtered_to_original_map, remap_indices

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

cohere_api_key: str = os.environ["COHERE_API_KEY"]
jina_api_key: str = os.environ["JINA_API_KEY"]

COHERE_THRESHOLD: float = 0.60
JINA_THRESHOLD: float = 0.60

co: cohere.Client = cohere.Client(cohere_api_key)


def lambda_handler(event: List[Any], context: Any = None) -> Dict[str, Any]:
    try:
        docs_data, product_data = event
        # Initialize a list to store extracted content from the preferred Urls
        preferred_contents = []
        for doc in docs_data:
            doc_type = doc.get("type")
            if doc_type and doc_type == "user-preferred_web":
                preferred_contents.append(doc)
                docs_data.remove(doc)

        query: str = build_query(product_data)
        docs: List[str] = get_docs(docs_data)

        try:
            cohere_results = cohere_rerank(query, docs)
        except Exception as e:
            logger.warning(f"Cohere Reranker failure {e}", RuntimeWarning)
            cohere_results = None
        cohere_indexes_and_scores = []
        if cohere_results:
            cohere_indexes_and_scores = cohere_extract_indexes_and_scores(
                cohere_results, COHERE_THRESHOLD
            )

        try:
            jina_results = jina_rerank(query, docs)
        except Exception as e:
            logger.warning(f"Jina Reranker failure {e}", RuntimeWarning)
            jina_results = None

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {"statusCode": 500, "error": str(e)}


def build_query(product_data: Dict[str, Any]) -> str:
    """
    Build a descriptive query string for a product based on the provided data.

    Args:
        product_data (Dict[str, Any]): A dictionary containing product information.
            Required keys:
                - 'name': The name of the product.
                - 'brand': The brand of the product.
            Optional keys:
                - 'variantable_attributes': Variant attributes of the product (default: empty string).
                - 'product_model': The model of the product (default: empty string).

    Returns:
        str: A formatted query string describing the product.
    """
    product: str = product_data["name"]
    brand: str = product_data["brand"]
    variantable_attributes: str = product_data.get("variantable_attributes", "")
    product_model: str = product_data.get("product_model", "")

    q = f"Description, attributes, characteristics, features for product: {product} by brand: {brand}"
    if variantable_attributes:
        q += f", product model: {product_model}"
    q += "."
    logger.info(f"Reranker query: \n{q}")
    return q


def get_docs(data: List[Dict[str, Any]]) -> List[str]:
    """Extracts the 'contents' string from each dictionary in a list."""
    return [
        i["contents"] if "contents" in i and isinstance(i["contents"], str) else ""
        for i in data
    ]


def cohere_rerank(query: str, docs: List[str]) -> List[Dict[str, Any]]:
    """
    Because cohere does not accept empty strings, before invoking the API, empty strings are removed. By keeping track
    of the indices of there removed documents, the output of the reranker is postprocessed to include result for
    the empty strings and preserving the original order
    """

    # Before filtering out empty strings, preserving the original indices of the non-empty strings
    mapping, length = filtered_to_original_map(docs)
    _docs = [d for d in docs if d]

    if _docs:
        reranker = co.rerank(query=query, documents=_docs, top_n=5, model="rerank-v3.5")
        output = [
            {"index": i.index, "relevance_score": i.relevance_score}
            for i in reranker.results
        ]
        output = remap_indices(output, mapping, length)
    else:
        logger.info("All documents are empty strings. Skipping the call to the reranker")
        output = None
    
    return output

def cohere_extract_indexes_and_scores(reranker_results: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    """Extracts index and relevance_score from reranker results, filtering by a minimum score threshold."""
    return [
        {"index": i["index"], "relevance_score": i.get("relevance_score")}
        for i in reranker_results
        if i.get("relevance_score") and i.get("relevance_score") > threshold
    ]

def jina_rerank(query: str, docs: List[str]) -> List[Dict[str, Any]]:
    url: str = "https://api.jina.ai/v1/rerank"