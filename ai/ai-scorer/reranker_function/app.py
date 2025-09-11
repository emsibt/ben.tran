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
        jina_indexes_and_scores = []
        if jina_results:
            jina_indexes_and_scores = jina_extract_indexes_and_scores(
                jina_results, JINA_THRESHOLD
            )

        if jina_results:
            _update_scores(docs_data, "jina", jina_results)
        if cohere_results:
            _update_scores(docs_data, "cohere", cohere_results)

        relevant_indexes, formatted_scores = extract_relevant_content_and_scores(
            cohere_indexes_and_scores, jina_indexes_and_scores
        )

        relevant_content = [docs_data[i] for i in relevant_indexes]

        if preferred_contents:
            relevant_content = preferred_contents + relevant_content
        return {
            "statusCode": 200,
            "aiReranker": {
                "relevantContent": relevant_content,
                "rerankerScore": formatted_scores,
            }
        }

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
        logger.info(
            "All documents are empty strings. Skipping the call to the reranker"
        )
        output = None

    return output


def cohere_extract_indexes_and_scores(
    reranker_results: List[Dict[str, Any]], threshold: float
) -> List[Dict[str, Any]]:
    """Extracts index and relevance_score from reranker results, filtering by a minimum score threshold."""
    return [
        {"index": i["index"], "relevance_score": i.get("relevance_score")}
        for i in reranker_results
        if i.get("relevance_score") and i.get("relevance_score") > threshold
    ]


def jina_rerank(query: str, docs: List[str]) -> List[Dict[str, Any]]:
    """
    Send a query and a list of documents to the Jina AI reranker API and return reranked results.

    Args:
        query (str): The query string to be used for reranking.
        docs (List[str]): A list of document strings to be reranked.

    Returns:
        List[Dict[str, Any]]: The reranked results from the Jina API, parsed from the response JSON.

    Raises:
        requests.RequestException: If the HTTP request fails.
        KeyError: If 'results' key is missing in the response.
    """
    url: str = "https://api.jina.ai/v1/rerank"

    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jina_api_key}",
    }

    data: Dict[str, Any] = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": docs,
        "top_n": 5,
    }

    reranker = requests.post(url, headers=headers, json=data, timeout=30)
    res: Dict[str, Any] = reranker.json()
    return res["results"]


def jina_extract_indexes_and_scores(
    reranker_results: List[Dict[str, Any]], threshold: float
) -> List[Dict[str, Any]]:
    """Extract indexes and relevance scores from Jina reranker results above a given threshold."""
    return [
        {"index": i["index"], "relevance_score": i["relevance_score"]}
        for i in reranker_results
        if i["relevance_score"] > threshold
    ]


def _update_scores(destination_doc: Dict, score_key: str, results: Dict):
    """A helper to update a dictinary with cohere and jina scores, based on liat index."""
    for r in results:
        element = destination_doc[r["index"]]
        scores = element.get("scores", ())
        if score := r.get("relevance_score"):
            scores[score_key] = score
        element.update({"scores": scores})


def extract_relevant_content_and_scores(
    cohere_results: List[Dict[str, Any]], jina_results: List[Dict[str, Any]]
) -> Tuple[List[str], Dict[str, str]]:
    relevant_indexes = {i["index"] for i in cohere_results} | {
        i["index"] for i in jina_results
    }

    scores = [
        i["relevance_score"] for i in cohere_results if i["index"] in relevant_indexes
    ] + [i["relevance_score"] for i in jina_api_key if i["index"] in relevant_indexes]

    if scores:
        min_score: float = min(scores)
        max_score: float = max(scores)
        avg_score: float = sum(scores) / len(scores)
    else:
        min_score = max_score = avg_score = 0.0
    
    logger.info(
        f"Stats - Min: {min_score}, Max: {max_score}, Avg: {avg_score}"
    )

    formatted_scores = {
        "minScore": f"{min_score:.2f}",
        "maxScore": f"{max_score:.2f}",
        "avgScore": f"{avg_score:.2f}",
    }
    return relevant_indexes, formatted_scores
