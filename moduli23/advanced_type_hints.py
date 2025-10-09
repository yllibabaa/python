from typing import Optional
from typing import Union
from typing import Any



def get_name(name: Optional[str]= None) -> str:
    if name:
        return name
    return "Anonymous"


print(get_name())


def process_value(value: Union[int, str]) -> str:
    if isinstance(value, int):
      return f"Number: {value}"
    return f"String: {value}"


print(process_value("Digital School"))


def process_anything(value: Any) -> str:
    return f"Processed {value}"


print(process_anything("Any string"))

def sum_list (numbers:List[int]) -> int:
    return sum(numbers)

numbers: List[int] =[1,2,3]
result: int = sum_list(numbers)