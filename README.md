# Ansys Zemax Programming Library

The Ansys Zemax Programming Library centralizes programming solutions provided by the Ansys Zemax team. Zemax OpticStudio offers several programming approaches:

- **ZOS-API**: Zemax OpticStudio Application Programming Interface (API)
- **ZPL**: Zemax programming language
- **User-defined DLLs**: Custom surfaces, objects, and other DLL types

This repository maintains boilerplate code, sample code shipped with OpticStudio, and knowledgebase examples for the five ZOS-API-supported languages.

The ZOS-API is backward compatible so most examples should work on any version of OpticStudio, as long as the leveraged features are available in that version.


## Dependencies

- An installed and licensed copy of Zemax OpticStudio (any version)
- A programming language with .NET or COM capabilities (required by the ZOS-API)
- Language-specific development tools (such as compilers and IDEs)

## Documentation

- [Getting started with ZOS-API](https://optics.ansys.com/hc/en-us/articles/42661816179731--Tutorial-Series-Getting-Started-with-ZOS-API)
- [ZPL programming](https://optics.ansys.com/hc/en-us/articles/42661790851603--Tutorial-Series-ZPL-Programming)
- [Custom DLLs in OpticStudio](https://optics.ansys.com/hc/en-us/articles/42661741799699-Custom-DLLs-in-OpticStudio-An-overview-of-user-defined-surfaces-objects-and-other-DLL-types)

## Examples

The [`examples`](examples/) directory contains ready-to-run examples, organized by programming language:

| Language | Directory | Count |
|---|---|---|
| C# | [`examples/c_sharp`](examples/c_sharp/) | 28 |
| C++ | [`examples/c_plus_plus`](examples/c_plus_plus/) | 27 |
| Mathematica | [`examples/mathematica`](examples/mathematica/) | 6 |
| MATLAB | [`examples/matlab`](examples/matlab/) | 25 |
| Python | [`examples/python`](examples/python/) | 25 |
| VB.NET | [`examples/vb_net`](examples/vb_net/) | 1 |

Run a Python example with the following steps:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e .[examples]
python examples/python/<example_name>.py
```

## Tests

Automated tests (Python only) verify the ZOS-API examples using **pytest**.

1. Install the project with test dependencies:

    ```bash
    pip install .[tests]
    ```

2. Run pytest from the project root:

    ```bash
    pytest
    ```

## Contributing

To contribute to the library or suggest modifications, please open an Issue. For guidelines, see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project uses the [MIT License](LICENSE).
