<div align="center">

# ✨ SPARQL API code generator 🐍

</div>

A CLI tool to automatically generate a python package from a SPARQL endpoint VoID description.

It will generate a folder with all requirements for publishing a modern python package containing the classes to automatically work with the data in the endpoint.

Features:

* Each class in the endpoint will be defined as a python class, with fields for each predicates available on a class.
* It will use the classes and predicates labels from their ontology when possible to generate the python classes and their fields
* Type annotations are used for better autocompletion
* Fields of a class are retrieved when the field is called (lazy 🦥)

## 🪄 Usage

> Requirements: Python >=3.9

1. Install the package with `pip` or `pipx`:

   ```sh
   pipx install sparql-api-codegen
   ```

2. Generate the code for a SPARQL endpoint which contains a SPARQL Service Description:

   ```sh
   sparql-api-codegen <sparql-endpoint-url> <folder-for-generated-python-pkg> -i <iri-of-class-to-ignore>
   ```

3. Once the folders have been generated you can get into the folder, check and improve the instructions to run in the `README.md`, improve the metadata in the `pyproject.toml`

Optionally you can ignore some classes. For some endpoints this will be required if the label generated for 2 classes are identical, e.g. for Bgee:

```sh
sparql-api-codegen "https://www.bgee.org/sparql/" "bgee-api" \
	-i http://purl.obolibrary.org/obo/CARO_0000000 \
	-i http://purl.obolibrary.org/obo/SO_0000704 \
	-i http://purl.obolibrary.org/obo/NCIT_C14250
```

Example python API for Bgee:

```python
from bgee_api import AnatomicalEntity, Gene, GeneExpressionExperimentCondition


if __name__ == "__main__":
    all_anats = AnatomicalEntity.get()
    print(len(all_anats), all_anats[0])

    anat = AnatomicalEntity("http://purl.obolibrary.org/obo/AEO_0000013")
    print(anat)
    print(anat.label)
    print(anat.expresses)

    gene= Gene("http://omabrowser.org/ontology/oma#GENE_ENSMUSG00000053483")
    print(gene.label)

    cond = GeneExpressionExperimentCondition("http://bgee.org/#EXPRESSION_CONDITION_101909")
    print(cond.has_a_developmental_stage)
    print(cond.has_anatomical_entity)
```

For UniProt:

```sh
sparql-api-codegen "https://sparql.uniprot.org/sparql/" "uniprot-api" \
	-i http://biohackathon.org/resource/faldo#Region
```

## 🧑‍💻 Development setup

The final section of the README is for if you want to run the package in development, and get involved by making a code contribution.


### 📥️ Clone

Clone the repository:

```bash
git clone https://github.com/TRIPLE-CHIST-ERA/sparql-api-codegen
cd sparql-api-codegen
```

### 🐣 Install dependencies

Install [Hatch](https://hatch.pypa.io), a modern build system, as well as project and virtual env management tool recommended by the Python Packaging Authority. This will automatically handle virtual environments and make sure all dependencies are installed when you run a script in the project:

```bash
pipx install hatch
```

Or you could install in your favorite virtual env:

```bash
pip install -e ".[test]"
```

### 🛠️ Develop

Test with the Bgee endpoint:

```bash
hatch run sparql-api-codegen "https://www.bgee.org/sparql/" "bgee-api" \
    -i http://purl.obolibrary.org/obo/CARO_0000000 \
    -i http://purl.obolibrary.org/obo/SO_0000704 \
    -i http://purl.obolibrary.org/obo/NCIT_C14250
```

### ☑️ Run tests

Make sure the existing tests still work by running the test suite and linting checks. Note that any pull requests to the fairworkflows repository on github will automatically trigger running of the test suite;

```bash
hatch run test
```

To display all logs when debugging:

```bash
hatch run test -s
```

### ♻️ Reset the environment

In case you are facing issues with dependencies not updating properly you can easily reset the virtual environment with:

```bash
hatch env prune
```

Manually trigger installing the dependencies in a local virtual environment:

```bash
hatch -v env create
```

### 🏷️ New release process

The deployment of new releases is done automatically by a GitHub Action workflow when a new release is created on GitHub. To release a new version:

1. Make sure the `PYPI_TOKEN` secret has been defined in the GitHub repository (in Settings > Secrets > Actions). You can get an API token from PyPI at [pypi.org/manage/account](https://pypi.org/manage/account).
2. Increment the `version` number in the `pyproject.toml` file in the root folder of the repository.

    ```bash
    hatch version fix
    ```

3. Create a new release on GitHub, which will automatically trigger the publish workflow, and publish the new release to PyPI.

You can also build and publish from your computer:

```bash
hatch build
hatch publish
```

### TODO

- Bulk load with preloaded fields

  ```python
  all_anats_preloaded: list[AnatomicalEntity] = bulk_load(AnatomicalEntity, ["label", "expresses"])
  # Or
  all_anats_preloaded: list[AnatomicalEntity] = AnatomicalEntity.get(["label", "expresses"])
  ```

  > Allow also to pass a list of IRI (optional, if not we get all?)

- Returns pandas matrix with filters?

  ```python
  pandas_matrix = BiologicalEntity.get_matrix(
      filter_has_a_developmental_stage="http://some_dev_stage",
      filter_has_anatomical_entity="some anatomical entity",
  )
  ```

  > Also enable to filter on labels instead of IRI?
