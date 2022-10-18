import json
from typing import Iterable, Any, Dict, List


class CustomJSONEncoder(json.JSONEncoder):
    """
    JSON encoder class.
        Description:
            Transform description dictionary into a json file
    """

    indentation_level: int

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """
        Custom JSON encoder with readable indentation.

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    @property
    def indent_str(self) -> str:
        """Generate an indentation string"""
        return " " * self.indentation_level * self.indent

    def iterencode(self, o: Iterable, **kwargs: Dict[str, Any]) -> str:
        """
        Encode JSON object *o* in a file. Called with json.dump().

        :param o: Serializable object.
        :return: Return the object "o" encoded with JSON style
        """
        return self.encode(o)[1:]

    def encode(self, o: Iterable) -> str:
        """
        Encode JSON object *o*. Called with json.dumps().

        :param o: Serializable object.
        :return: Return the object "o" encoded with JSON style
        """

        # How to encode lists and tuples
        if isinstance(o, (list, tuple)):

            # If list / tuple does not contain strings, encode inline
            if not any(isinstance(elt, (list, tuple, str)) for elt in o):
                output = [json.dumps(elt) for elt in o]
                join_output = ", ".join(output)
                return f"[{join_output}]"

            # Otherwise, insert new line between strings
            else:
                self.indentation_level += 1
                output = [f"{self.indent_str}{self.encode(elt)}" for elt in o]
                join_output = ",\n".join(output)
                self.indentation_level -= 1
                return f"\n{self.indent_str}[\n{join_output}\n{self.indent_str}]"

        # How to encode dicts
        elif isinstance(o, dict):
            self.indentation_level += 1
            output = [f"{self.indent_str}{json.dumps(key)}: {self.encode(value)}" for key, value in o.items()]
            join_output = ",\n".join(output) if self.indentation_level != 1 else ",\n\n".join(output)
            self.indentation_level -= 1
            return f"\n{self.indent_str}{'{'}\n{join_output}\n{self.indent_str}{'}'}"

        else:
            return json.dumps(o)


if __name__ == '__main__':

    z = {"data_shape": {"input": (2, 1),
                        "output": (2, 3)},
         "nb_samples": {"total": 70,
                        "Training": [30, 30, 10],
                        "Validation": [],
                        "Running": []},
         "partitions": {"Training": {"input": ["generation_training_IN_0.npy",
                                               "generation_training_IN_1.npy"],
                                     "output": ["generation_training_OUT_0.npy",
                                                "generation_training_OUT_1.npy"]},
                        "Validation": {"input": [],
                                       "output": []},
                        "Running": {"input": [],
                                    "output": []}}}
    print(json.dumps(z, indent=3, cls=CustomJSONEncoder))
