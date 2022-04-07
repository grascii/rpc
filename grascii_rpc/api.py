import sys
from typing import Optional, List, Set
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from flask_jsonrpc import JSONRPC
from grascii.outline import Outline
from grascii.parser import GrasciiParser, Interpretation
from grascii.searchers import GrasciiSearcher
from lark import UnexpectedInput

Strictness = Literal["discard", "retain", "strict"]

AVAILABLE_APIS = {"grascii.interpret", "grascii.search"}

def create_api(service_url: str="/api",
               enable_web_browsable_api: bool=False,
               enabled_apis: Set[str]=AVAILABLE_APIS):

    api = JSONRPC(service_url=service_url, enable_web_browsable_api=enable_web_browsable_api)

    parser = GrasciiParser()
    searcher = GrasciiSearcher()

    if "grascii.interpret" in enabled_apis:
        @api.method("grascii.interpret")
        def interpret(grascii: str, infer_directions: bool=False) -> Optional[Interpretation]:
            try:
                interpretations = parser.interpret(grascii.upper(), preserve_boundaries=infer_directions)
            except UnexpectedInput:
                return

            interpretation = interpretations[0]
            if infer_directions:
                outline = Outline(interpretation)
                return outline.to_interpretation()
            return interpretation

    if "grascii.search" in enabled_apis:
        @api.method("grascii.search")
        def search(grascii: str,
                   uncertainty: Literal[0, 1, 2]=0,
                   search_mode: Literal["match", "start", "contain"]="match",
                   annotation_mode: Strictness="discard",
                   aspirate_mode: Strictness="discard",
                   disjoiner_mode: Strictness="strict",
                   fix_first: bool=False,
                   interpretation: Literal["best", "all"]="best") -> List[str]:
            return searcher.search(grascii=grascii,
                                   uncertainty=uncertainty,
                                   search_mode=search_mode,
                                   annotation_mode=annotation_mode,
                                   aspirate_mode=aspirate_mode,
                                   disjoiner_mode=disjoiner_mode,
                                   fix_first=fix_first,
                                   interpretation=interpretation)

    return api
