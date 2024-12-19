import os

from sparql_api_codegen.settings import BOLD, CYAN, END, YELLOW
from sparql_api_codegen.utils import query_sparql

TripleDict = dict[str, dict[str, list[str]]]

GET_VOID_DESC = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX void-ext: <http://ldf.fi/void-ext#>
SELECT DISTINCT ?subjectClassLabel ?subjectClass ?prop ?propLabel ?objectClass ?objectClassLabel ?objectDatatype
WHERE {
  {
    ?cp void:class ?subjectClass ;
        void:propertyPartition ?pp .
    OPTIONAL { ?subjectClass rdfs:label ?subjectClassLabel }
    ?pp void:property ?prop .
    OPTIONAL { ?prop rdfs:label ?propLabel }
    OPTIONAL {
        {
            ?pp  void:classPartition [ void:class ?objectClass ] .
            OPTIONAL { ?objectClass rdfs:label ?objectClassLabel }
        } UNION {
            ?pp void-ext:datatypePartition [ void-ext:datatype ?objectDatatype ] .
        }
    }
  } UNION {
    ?linkset void:subjectsTarget [ void:class ?subjectClass ] ;
      void:linkPredicate ?prop ;
      void:objectsTarget [ void:class ?objectClass ] .
  }
}"""


def format_class_label(label: str) -> str:
    if "#" in label:
        return label.split("#")[-1].capitalize().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if "/" in label:
        return label.split("/")[-1].capitalize().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    label = "".join(word.capitalize() for word in label.split()) if " " in label else label
    # print(label)
    return label.replace(" ", "").replace("-", "").replace("_", "").replace("(", "").replace(")", "")


def format_property_label(label: str) -> str:
    if "#" in label:
        return label.split("#")[-1].lower().replace(" ", "_").replace("-", "").replace("(", "").replace(")", "")
    if "/" in label:
        return label.split("/")[-1].lower().replace(" ", "_").replace("-", "").replace("(", "").replace(")", "")
    return label.lower().replace(" ", "_").replace("-", "").replace("(", "").replace(")", "")


# TODO: handle when no label, and we get the URI

ignore_namespaces = [
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/ns/sparql-service-description#",
    "http://purl.org/query/voidext#",
    "http://rdfs.org/ns/void#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/ns/shacl#",
]


def should_be_ignored(uri: str) -> bool:
    return any(uri.startswith(namespace) for namespace in ignore_namespaces)


def get_void_dict(endpoint_url: str, ignore_cls: list[str]):
    """Get a dict of VoID description of an endpoint: dict[subject_cls][predicate] = list[object_cls/datatype]"""
    void_dict: TripleDict = {}
    label_dict = {}
    check_duplicate_label_dict = {}
    # print(query_sparql(GET_VOID_DESC, endpoint_url))
    for void_triple in query_sparql(GET_VOID_DESC, endpoint_url)["results"]["bindings"]:
        subj_cls_iri = void_triple["subjectClass"]["value"]
        # Filter out OWL classes
        if should_be_ignored(subj_cls_iri):
            continue
        if subj_cls_iri in ignore_cls:
            continue

        subj_cls_label = (
            format_class_label(void_triple["subjectClassLabel"]["value"])
            if "subjectClassLabel" in void_triple
            else format_class_label(subj_cls_iri)
        )
        label_dict[subj_cls_iri] = subj_cls_label
        if subj_cls_label in check_duplicate_label_dict:
            if check_duplicate_label_dict[subj_cls_label] != subj_cls_iri:
                raise ValueError(
                    f"Same label for class {subj_cls_iri} and {check_duplicate_label_dict[subj_cls_label]}. Please ignore one of these 2 classes using the -i argument"
                )
        else:
            check_duplicate_label_dict[subj_cls_label] = subj_cls_iri

        if "propLabel" in void_triple:
            label_dict[void_triple["prop"]["value"]] = format_property_label(void_triple["propLabel"]["value"])
        else:
            label_dict[void_triple["prop"]["value"]] = format_property_label(void_triple["prop"]["value"])

        if subj_cls_iri not in void_dict:
            void_dict[subj_cls_iri] = {}
        if void_triple["prop"]["value"] not in void_dict[subj_cls_iri]:
            void_dict[subj_cls_iri][void_triple["prop"]["value"]] = []
        if (
            "objectClass" in void_triple
            and void_triple["objectClass"]["value"] not in void_dict[subj_cls_iri][void_triple["prop"]["value"]]
        ):
            void_dict[subj_cls_iri][void_triple["prop"]["value"]].append(void_triple["objectClass"]["value"])
            if "objectClassLabel" in void_triple:
                label_dict[void_triple["objectClass"]["value"]] = format_class_label(
                    void_triple["objectClassLabel"]["value"]
                )
            else:
                label_dict[void_triple["objectClass"]["value"]] = format_class_label(
                    void_triple["objectClass"]["value"]
                )

        if "objectDatatype" in void_triple:
            void_dict[subj_cls_iri][void_triple["prop"]["value"]].append(void_triple["objectDatatype"]["value"])
    if len(void_dict) == 0:
        raise Exception("No VoID description found in the endpoint")
    return void_dict, label_dict


def generate_code_for_endpoint(endpoint_url: str, folder_path: str, ignore_cls: list[str]) -> None:
    print(
        f"🪄 Generating python API for {BOLD}{CYAN}{endpoint_url}{END} in the {BOLD}{YELLOW}{folder_path}{END} folder"
    )
    package_name = folder_path.split("/")[-1]
    module_name = package_name.replace("-", "_")
    already_exists_files: list[str] = []
    code = f"from dataclasses import dataclass\nfrom typing import Union\n\nfrom {module_name}.utils import query_sparql, SparqlEntity\n\n"
    code += "# This code was automatically generated by the sparql-api-codegen package (https://github.com/TRIPLE-CHIST-ERA/sparql-api-codegen)\n\n"

    void_dict, label_dict = get_void_dict(endpoint_url, ignore_cls)
    example_code_for_readme = ""
    for subject_cls, prop_dict in void_dict.items():
        if subject_cls in ignore_cls:
            continue
        code += "\n@dataclass\n"
        code += f"class {label_dict[subject_cls]}(SparqlEntity):\n"
        code += f'    type: str = "{subject_cls}"\n\n'

        # TODO: handle list of IRIs to load and preloading of fields
        # all_anats: list[AnatomicalEntity] = AnatomicalEntity.get(["label", "expresses"])
        code += "    @classmethod\n"
        code += f'    def get(cls) -> list["{label_dict[subject_cls]}"]:\n'
        code += '        res = query_sparql(f"SELECT ?iri WHERE {{ ?iri a <{cls.type}> }}", cls.sparql_endpoint)\n'
        code += (
            '        return [cls(binding["iri"]["value"], check=False) for binding in res["results"]["bindings"]]\n\n'
        )

        code += "    def __post_init__(self):\n"
        code += "        super().__post_init__()\n"
        for prop, _values in prop_dict.items():
            code += f"        self._{label_dict[prop]} = None\n"
            if len(example_code_for_readme) == 0:
                example_var = label_dict[subject_cls].lower()
                # Add the first in the README as example
                example_code_for_readme += "# Get all instances of a class\n"
                example_code_for_readme += f"    all_{example_var} = {label_dict[subject_cls]}.get()\n"
                example_code_for_readme += f"    print(len(all_{example_var}))\n"
                example_code_for_readme += f"    for {example_var} in all_{example_var}:\n"
                example_code_for_readme += f"        print({example_var}.iri, {example_var}.{label_dict[prop]})\n\n"
                example_code_for_readme += "    # Get a specific instance\n"
                example_code_for_readme += (
                    f'    {example_var} = {label_dict[subject_cls]}("https://iri-of-your-entity.org/YYY")\n'
                )
                example_code_for_readme += f"    print({example_var}.{label_dict[prop]})"
                example_cls_for_readme = label_dict[subject_cls]
        code += "\n"
        for prop, values in prop_dict.items():
            code += "    @property\n"
            retrieve_as_str = False
            if len(values) == 0 or values[0].startswith("http://www.w3.org/2001/XMLSchema#"):
                retrieve_as_str = True
            else:
                if len(values) == 1 and values[0] in void_dict:
                    code += f'    def {label_dict[prop]}(self) -> list["{label_dict[values[0]]}"]:\n'
                    code += f"        if self._{label_dict[prop]} is None:\n"
                    code += f"            self._{label_dict[prop]} = []\n"
                    code += f'            for entity_iri in self.get_predicate_value("{prop}"):\n'
                    code += f"                self._{label_dict[prop]}.append({label_dict[values[0]]}(entity_iri))\n"
                    code += f"        return self._{label_dict[prop]}\n\n"
                else:
                    obj_classes = [label_dict[obj_cls] for obj_cls in values if obj_cls in void_dict]
                    if len(obj_classes) == 0:
                        retrieve_as_str = True
                    else:
                        obj_classes_types = '", "'.join(obj_classes)
                        code += f'    def {label_dict[prop]}(self) -> list[Union["{obj_classes_types}"]]:\n'
                        code += f"        if self._{label_dict[prop]} is None:\n"
                        code += f"            self._{label_dict[prop]} = []\n"
                        code += f'            for entity_iri in self.get_predicate_value("{prop}"):\n'
                        # print(values)
                        for obj_cls_label in obj_classes:
                            code += "                try:\n"
                            code += (
                                f"                    self._{label_dict[prop]}.append({obj_cls_label}(entity_iri))\n"
                            )
                            code += "                    continue\n"
                            code += "                except ValueError:\n"
                            code += f"                    self._{label_dict[prop]}.append(entity_iri)\n"
                        code += f"        return self._{label_dict[prop]}\n\n"
            if retrieve_as_str:
                # TODO: handle datatypes str, int, float, datetime...
                code += f"    def {label_dict[prop]}(self) -> list[str]:\n"
                code += f"        if self._{label_dict[prop]} is None:\n"
                code += f'            self._{label_dict[prop]} = self.get_predicate_value("{prop}")\n'
                code += f"        return self._{label_dict[prop]}\n\n"
        code += "\n"

    # Create the target directory
    src_dir = os.path.join(folder_path, "src", module_name)
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "__init__.py"), "w") as f:
        f.write(code)

    pyproject_toml = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
requires-python = ">=3.9"
name = "{package_name}"
description = "Python API and classes to access data of the SPARQL endpoint {endpoint_url}"
readme = "README.md"
license = {{ file = "LICENSE" }}
authors = [
    {{ name = "Your Name", email = "your.name@sib.swiss" }},
]
maintainers = [
    {{ name = "Your Name", email = "your.name@sib.swiss" }},
]
keywords = [
    "Python",
    "SPARQL",
]
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
version = "0.1.0"

dependencies = [
    "requests",
]

[tool.hatch.build.targets.wheel]
packages = ["src/{module_name}"]
"""
    if not os.path.exists(os.path.join(folder_path, "pyproject.toml")):
        with open(os.path.join(folder_path, "pyproject.toml"), "w") as f:
            f.write(pyproject_toml)
    else:
        already_exists_files.append("pyproject.toml")

    readme = f"""# {package_name.capitalize()}

Python package to access data from the SPARQL endpoint available at {endpoint_url}.

## 🪄 Usage

1. Install:

    ```sh
    pip install {package_name}
    ```

2. Use the classes from python:

    ```python
    from {module_name} import {example_cls_for_readme}

    {example_code_for_readme}
    ```

## 🛠️ Development

### 📥️ Installation

Install [`hatch`](https://hatch.pypa.io), a modern build system, as well as a project and virtual env management tool recommended by the Python Packaging Authority. This will automatically handle virtual environments and make sure all dependencies are installed when you run a script something with `hatch run`.

### 🏷️ Publish a new release

1. Increment the `version` number in the `pyproject.toml` file in the root folder of the repository.

    ```bash
    hatch version fix
    ```

    > Or `minor` or `major` depending on the type of release.

2. Build and publish from your computer:

    ```bash
    hatch build
    hatch publish
    ```
"""
    if not os.path.exists(os.path.join(folder_path, "README.md")):
        with open(os.path.join(folder_path, "README.md"), "w") as f:
            f.write(readme)
    else:
        already_exists_files.append("README.md")

    license_txt = """MIT License

Copyright (c) 2024-present SIB Swiss Institute of Bioinformatics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    if not os.path.exists(os.path.join(folder_path, "LICENSE")):
        with open(os.path.join(folder_path, "LICENSE"), "w") as f:
            f.write(license_txt)
    else:
        already_exists_files.append("LICENSE")

    utils_py = """from dataclasses import dataclass
from typing import Any, Optional, Union

import requests

# This code was automatically generated by the sparql-api-codegen package (https://github.com/TRIPLE-CHIST-ERA/sparql-api-codegen)

def query_sparql(query: str, endpoint_url: str, post: bool = False, timeout: Optional[int] = None) -> Any:
    \"\"\"Execute a SPARQL query on a SPARQL endpoint using requests\"\"\"
    if post:
        resp = requests.post(
            endpoint_url,
            headers={
                "Accept": "application/sparql-results+json",
            },
            data={"query": query},
            timeout=timeout,
        )
    else:
        resp = requests.get(
            endpoint_url,
            headers={
                "Accept": "application/sparql-results+json",
            },
            params={"query": query},
            timeout=timeout,
        )
    resp.raise_for_status()
    return resp.json()


@dataclass
class SparqlEntity:
    iri: str
    type: str = "http://www.w3.org/2000/01/rdf-schema#Resource"
    sparql_endpoint: str = "!!SPARQL_ENDPOINT!!"
    check: bool = True

    def __post_init__(self):
        if self.check:
            exists = query_sparql(f"ASK WHERE {{ <{self.iri}> a <{self.type}> . }}", self.sparql_endpoint)
            if not exists.get("boolean"):
                raise ValueError(f"No resource found with IRI {self.iri} and type {self.type} in endpoint {self.sparql_endpoint}")


    def get_predicate_value(self, predicate: str) -> list[str]:
        try:
            res = query_sparql(f"SELECT ?value WHERE {{ <{self.iri}> <{predicate}> ?value }}", self.sparql_endpoint)
            return [binding["value"]["value"] for binding in res["results"]["bindings"]]
        except Exception as err:
            raise ValueError(f"No value found for predicate {predicate} for entity IRI {self.iri} in endpoint {self.sparql_endpoint}") from err
"""
    with open(os.path.join(src_dir, "utils.py"), "w") as f:
        f.write(utils_py.replace("!!SPARQL_ENDPOINT!!", endpoint_url))

    if not os.path.exists(os.path.join(src_dir, "py.typed")):
        with open(os.path.join(src_dir, "py.typed"), "w") as f:
            f.write("")

    if len(already_exists_files) > 0:
        print(
            f"⏩️ Skipping creation of the following files as they already exist in the {YELLOW}{folder_path}{END} folder: {BOLD}{f'{END}, {BOLD}'.join(already_exists_files)}{END}"
        )

    print(f"🎉 Generated code for {BOLD}{len(void_dict)}{END} classes")
