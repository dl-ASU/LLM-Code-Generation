import clang.cindex


# Set to track visited functions during traversal
visited_functions = set()

def find_calling_functions(cursor, method_name):
    calling_functions = []

    def visit(node):
        if node.kind == clang.cindex.CursorKind.CALL_EXPR :
                calling_function_info = {
                    'name': node.displayname,
                    'return_type': node.result_type.spelling,
                    'arguments': [arg.type.spelling for arg in node.get_arguments()]
                }
                calling_functions.append(calling_function_info)

        for child in node.get_children():
            visit(child)

    for cursor_child in cursor.get_children():
        visit(cursor_child)

    return calling_functions


def get_parent_method(cursor):
    while cursor and cursor.kind not in [clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.FUNCTION_DECL]:
        cursor = cursor.semantic_parent

    if cursor and cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        return cursor

    # Handle special case for global functions
    if cursor and cursor.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
        return cursor

    return None

def extract_global_variables(cursor):
    global_vars = []
    for child in cursor.get_children():
        if child.kind == clang.cindex.CursorKind.VAR_DECL:
            global_vars.append({
                'name': child.displayname,
                'type': child.type.spelling
            })
    return global_vars

def extract_class_info(cursor):
    classes = []
    for child in cursor.get_children():
        if child.kind == clang.cindex.CursorKind.CLASS_DECL:
            class_info = {
                'name': child.displayname,
                'attributes': [],
                'methods': []
            }

            for class_child in child.get_children():
                if class_child.kind == clang.cindex.CursorKind.FIELD_DECL:
                    class_info['attributes'].append({
                        'name': class_child.displayname,
                        'type': class_child.type.spelling
                    })

                elif class_child.kind == clang.cindex.CursorKind.CXX_METHOD:
                    method_info = {
                        'name': class_child.displayname,
                        'return_type': class_child.result_type.spelling,
                        'parameters': [],
                        'calling_functions': []  # New field for calling functions
                    }

                    for param in class_child.get_children():
                        if param.kind == clang.cindex.CursorKind.PARM_DECL:
                            method_info['parameters'].append({
                                'name': param.displayname,
                                'type': param.type.spelling
                            })

                    class_info['methods'].append(method_info)

            classes.append(class_info)

    return classes

def extract_standalone_functions(cursor):
    functions = []
    for child in cursor.get_children():
        if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            function_info = {
                'name': child.displayname,
                'return_type': child.result_type.spelling,
                'parameters': [],
                'calling_functions': []  # New field for calling functions
            }

            for param in child.get_children():
                if param.kind == clang.cindex.CursorKind.PARM_DECL:
                    function_info['parameters'].append({
                        'name': param.displayname,
                        'type': param.type.spelling
                    })

            functions.append(function_info)

    return functions

def parse_cpp_code(code):
    index = clang.cindex.Index.create()
    translation_unit = index.parse('tmp.cpp', args=['-std=c++14'], unsaved_files=[('tmp.cpp', code)])
    return translation_unit.cursor

cpp_code = """
int global_var = 42;

class MyClass {
public:
    int attribute1;
    double attribute2;

    void method1(int param1, double param2);
    void method2();
};

class AnotherClass {
private:
    float attribute3;

public:
    void method3(char param);
};
void me3(){
//function body
}
void standaloneFunction() {
    // function body
     me3();
}
"""

cursor = parse_cpp_code(cpp_code)

global_variables = extract_global_variables(cursor)
classes_info = extract_class_info(cursor)
standalone_functions = extract_standalone_functions(cursor)

# Find calling functions for each method
for class_info in classes_info:
    for method_info in class_info['methods']:
        calling_functions = find_calling_functions(cursor, method_info['name'])
        method_info['calling_functions'] = calling_functions

# Find calling functions for standalone functions
for function_info in standalone_functions:
    calling_functions = find_calling_functions(cursor, function_info['name'])
    function_info['calling_functions'] = calling_functions

# Print the extracted information
print("Global Variables:")
for var in global_variables:
    print(f"  {var['type']} {var['name']}")

print("\nClasses and Their Attributes/Methods:")
for class_info in classes_info:
    print(f"\nClass: {class_info['name']}")
    
    print("  Attributes:")
    for attr in class_info['attributes']:
        print(f"    {attr['type']} {attr['name']}")

    print("  Methods:")
    for method_info in class_info['methods']:
        print(f"    Method: {method_info['name']}")
        print(f"      Return Type: {method_info['return_type']}")
        print("      Parameters:")
        for param in method_info['parameters']:
            print(f"        {param['type']} {param['name']}")

        print("      Calling Functions:")
        for calling_function_info in method_info['calling_functions']:
            print(f"        Calling Function: {calling_function_info['name']}")
            print(f"          Return Type: {calling_function_info['return_type']}")
            print("          Arguments:")
            for arg in calling_function_info['arguments']:
                print(f"            {arg}")

# Output for standalone functions without a class
print("\nStandalone Functions:")
for function_info in standalone_functions:
    print(f"  Function: {function_info['name']}")
    print(f"    Return Type: {function_info['return_type']}")
    print("    Parameters:")
    for param in function_info['parameters']:
        print(f"      {param['type']} {param['name']}")
    
    print("    Calling Functions:")
    for calling_function_info in function_info['calling_functions']:
        print(f"      Calling Function: {calling_function_info['name']}")
        print(f"        Return Type: {calling_function_info['return_type']}")
        print("        Arguments:")
        for arg in calling_function_info['arguments']:
            print(f"          {arg}")
