#----------------------------------------------------------------------

    # Libraries
from dataclasses import dataclass
#----------------------------------------------------------------------

    # Class
@dataclass
class Category:
    keyword: str
    icon: str

    def __hash__(self) -> int:
        return hash(self.keyword)
#----------------------------------------------------------------------
