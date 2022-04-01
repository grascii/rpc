from typing import Optional

from flask_jsonrpc import JSONRPC
from grascii.parser import GrasciiParser, Interpretation
from lark import UnexpectedInput

grascii_api = JSONRPC(service_url="/api", enable_web_browsable_api=True)

parser = GrasciiParser()

@grascii_api.method("grascii.interpret")
def interpret(grascii: str) -> Optional[Interpretation]:
    try:
        interpretations = parser.interpret(grascii.upper())
    except UnexpectedInput:
        return

    return interpretations[0]
