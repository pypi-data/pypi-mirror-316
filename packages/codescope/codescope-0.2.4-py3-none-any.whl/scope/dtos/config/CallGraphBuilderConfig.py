# Standard library
from dataclasses import dataclass
from scope.enums import AllowedSymbols

@dataclass
class CallGraphBuilderConfig:
    """
    Config options for the CallGraphBuilder.
    timeit: bool = False
    log_level: LogLevelLSP = LogLevelLSP.NONE
    log_file: str = None
    language: str = None
    allowed_symbols: str = AllowedSymbols.STRICT
    allow_libraries: bool = False
    """

    timeit: bool = False
    log_file: str = None
    language: str = None
    log_level: str = None
    allowed_symbols: str = AllowedSymbols.STRICT
    allow_libraries: bool = False