from pycparser import c_ast, parse_file



def ast_to_string(node, indent=0):
    if isinstance(node, c_ast.FileAST):
        string_representation = ""
        for child in node.ext:
            string_representation += ast_to_string(child, indent)
        return string_representation

    elif isinstance(node, c_ast.FuncDef):
        string_representation = f"{'  ' * indent}Function: {node.decl.name}\n"
        string_representation += ast_to_string(node.body, indent + 1)
        return string_representation

    elif isinstance(node, (c_ast.Compound, c_ast.DoWhile)):
        string_representation = f"{'  ' * indent}Statement: {node.__class__.__name__}\n"
        for child in node.block_items:
            string_representation += ast_to_string(child, indent + 1)
        return string_representation

    elif isinstance(node, c_ast.If):
        string_representation = f"{'  ' * indent}Statement: {node.__class__.__name__}\n"
        string_representation += f"{'  ' * (indent + 1)}Condition:\n"
        string_representation += ast_to_string(node.cond, indent + 2)
        string_representation += f"{'  ' * (indent + 1)}If True:\n"
        string_representation += ast_to_string(node.iftrue, indent + 2)
        if node.iffalse:
            string_representation += f"{'  ' * (indent + 1)}If False:\n"
            string_representation += ast_to_string(node.iffalse, indent + 2)
        return string_representation

    elif isinstance(node, c_ast.While):
        string_representation = f"{'  ' * indent}Statement: {node.__class__.__name__}\n"
        string_representation += f"{'  ' * (indent + 1)}Condition:\n"
        string_representation += ast_to_string(node.cond, indent + 2)
        string_representation += f"{'  ' * (indent + 1)}Body:\n"
        string_representation += ast_to_string(node.stmt, indent + 2)
        return string_representation

    elif isinstance(node, (c_ast.For, c_ast.ID, c_ast.Constant)):
        return f"{'  ' * indent}Expression: {node.__class__.__name__} - {getattr(node, 'name', '')}\n"

    else:
        return f"{'  ' * indent}{str(node)}\n"  # Handle other node types



FileName = "sampleShort.c"

ast = parse_file(FileName, use_cpp=True, cpp_path='mcpp.exe')

ast_as_text = ast_to_string(ast)

with open("ASTtxt.txt", "w") as file:
    file.write(ast_as_text)
