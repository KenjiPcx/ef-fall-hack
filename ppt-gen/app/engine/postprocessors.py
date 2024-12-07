import logging
from typing import List, Optional

from llama_index.core import QueryBundle
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore

logger = logging.getLogger("uvicorn")

class FakeProcessor(BaseNodePostprocessor):
    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        logger.info(f"FakeProcessor: {nodes}")
        return nodes

class NodeCitationProcessor(BaseNodePostprocessor):
    """
    Append node_id into metadata for citation purpose.
    Config SYSTEM_CITATION_PROMPT in your runtime environment variable to enable this feature.
    """

    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        for node_score in nodes:
            node_score.node.metadata["node_id"] = node_score.node.node_id
        return nodes

class NodeMetadataRemover(BaseNodePostprocessor):
    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        """
        At this point, a node should have a metadata with the following keys:
        - description
        - image_url (keep)
        - source (keep)
        - file_type
        - questions that can be answered
        - keywords
        - topics
        - entities
        - visualized_data
        
        We remove the non useful keys from the metadata.
        """
        
        non_useful_keys = [
            "description", 
            "questions_that_can_be_answered", 
            "keywords", 
            "topics", 
            "entities", 
            "visualized_data",
            "file_type"
        ]
        
        for node in nodes:
            for key in non_useful_keys:
                if key in node.node.metadata:
                    del node.node.metadata[key]
        return nodes

# class NodeContentProcessor(BaseNodePostprocessor):
#     def _postprocess_nodes(
#         self,
#         nodes: List[NodeWithScore],
#         query_bundle: Optional[QueryBundle] = None,
#     ) -> List[NodeWithScore]:
#         """Format node content into readable markdown sections"""
        
#         search_res = []
        
#         for i, node_with_score in enumerate(nodes):
#             node = node_with_score.node
#             metadata = node.metadata
            
#             formatted_content = [
#                 f"### Result {i+1}",
#                 f"**Score**: {node_with_score.score:.3f}",
#                 "#### Content",
#                 f"{node.text}",
#                 "#### Metadata",
#                 f"**Source**: {metadata.get('source', 'N/A')}",
#             ]
            
#             # Add optional metadata if present
#             if "page_num" in metadata:
#                 formatted_content.append(f"**Page**: {metadata['page_num']}")
#             if "image_url" in metadata:
#                 formatted_content.append(f"**Image**: {metadata['image_url']}")
                
#             # Update the node text with formatted content
#             search_res.append("\n".join(formatted_content))
        
#         return search_res

# class NodeStaticFilesUrlProcessor(BaseNodePostprocessor):
#     """
#     Convert a relative path into the deployed static files url.
#     """

#     def _postprocess_nodes(
#         self,
#         nodes: List[NodeWithScore],
#         query_bundle: Optional[QueryBundle] = None,
#     ) -> List[NodeWithScore]:
#         import os
#         from urllib.parse import quote

#         logger.info(f"Postprocessing nodes with NodeStaticFilesUrlProcessor")
        
#         url_prefix = os.getenv("FILESERVER_URL_PREFIX")
#         for node_score in nodes:
#             image_url = node_score.node.metadata.get("image_url")
#             if image_url:
#                 encoded_path = quote(image_url)
#                 node_score.node.metadata["image_url_2"] = f"{url_prefix}/{encoded_path}"
#                 logger.info(f"Converted image_url: {image_url} to {node_score.node.metadata['image_url_2']}")
#         return nodes
