import sys
from typing import Optional, List
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from flask_jsonrpc import JSONRPC
from grascii.parser import GrasciiParser, Interpretation
from grascii.searchers import GrasciiSearcher
from lark import UnexpectedInput

grascii_api = JSONRPC(service_url="/api", enable_web_browsable_api=True)

parser = GrasciiParser()
searcher = GrasciiSearcher()

@grascii_api.method("grascii.interpret")
def interpret(grascii: str) -> Optional[Interpretation]:
    try:
        interpretations = parser.interpret(grascii.upper())
    except UnexpectedInput:
        return

    return interpretations[0]

Strictness = Literal["discard", "retain", "strict"]
@grascii_api.method("grascii.search")
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
