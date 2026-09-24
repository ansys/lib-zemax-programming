# Examples

This directory contains programming examples for the Zemax OpticStudio ZOS-API in multiple languages.

## Supported languages

- **C++**: See the [c_plus_plus](c_plus_plus/) directory for C++ examples.
- **C#**: See the [c_sharp](c_sharp/) directory for C# examples.
- **Mathematica**: See the [mathematica](mathematica/) directory for Mathematica examples.
- **MATLAB**: See the [matlab](matlab/) directory for MATLAB examples.
- **Python**: See the [python](python/) directory for Python examples.
- **VB.NET**: See the [vb_net](vb_net/) directory for Visual Basic .NET (VB.NET) examples.

## Run Python examples

1. Install the required dependencies:

   ```bash
   pip install -r requirements/requirements_example.txt
   ```

2. Verify that Zemax OpticStudio is installed and licensed on your machine.

3. Run a Python example:

   ```bash
   python examples/python/<example_name>.py
   ```

## Run examples in other languages

Each language folder contains examples with instructions specific to that language. For compilation and execution instructions, see the individual example files.

## Requirements

All examples require:
- An installed and licensed copy of Zemax OpticStudio
- Appropriate development tools for your chosen language (such as compilers and IDEs)

## Using templates

In the template directory, each language will have a base template with which you can start developing your code. These templates handle the general connection to Zemax, key functions, and basic error handling. In each template there will be a clear comment where you can start writing your specific ZOS-API code.

- **C++ & C#** : these will require Visual Studio or similar IDE for compiling and editing the code. They both come in four flavors:
   - **Standalone** - this mode will run Zemax headlessly and return results or information about your model without the Zemax GUI.
   - **User Extension** - this mode will run inside of Zemax (found in Programming...Extensions) where your code can interact with the Zemax GUI.
   - **User Analysis** - will open an analysis window, much like the built-in windows in Zemax, where you can define your own settings and data visualization.
   - **User Operand** - will create a user defined operand for the Zemax Merit Function to customize optimization.

- **Python** : will require a Python-specific IDE like Visual Code or similar, as well as the other requirements listed for running Python examples. There are two types:
   - **Standalone** - this is similar to the C-templates and will run Zemax headlessly without the Zemax GUI.
   - **Interactive Extension** - this mode will connect to a listening Zemax instance and allow your Python script to take control of the GUI.
   
- **MATLAB & Mathematica** : these templates will require MATLAB or Mathematica to run, and have the same types as Python.