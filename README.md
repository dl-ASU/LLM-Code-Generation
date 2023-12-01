## C Code Parsing (Local Setup on Windows)

###  Install the Library

To get started, install the `pycparser` library using the following pip command:

```bash
pip install pycparser
```

 If your C file contains tokens that is needed to preproced ie: `#define`, `#typedef`, you must make `use_cpp=True` and `cpp_path='mcpp.exe'` (mcpp is a portable c preprocessor) otherwise you dont have to set the paramater `use_cpp` or `cpp_path`

### unfortunatily the script is not ready yet to parse C files that imports from another libraries (even with "stdio.h")

## C Code Parsing (Setup on google colab)
all the steps are the same except you dont need to specify the path `cpp_path='mcpp.exe'`, just put `use_cpp=True` and it will work just fine

