import ast
import inspect
import textwrap


IS_ASYNC_MODE = 'is_async_mode'
is_async_mode = True


class NotEnclosedAwait(Exception):
    def __init__(self, expr_lineno):
        super().__init__()
        self.expr_lineno = expr_lineno

class Transformer(ast.NodeTransformer):
    def __init__(self, func_name):
        self.main_async_func_encountered = False
        self.func_name = func_name
        self.async_mode_test_on = False

    def visit_AsyncFunctionDef(self, asyncfunc_ast):
        main_async_func_encountered = self.main_async_func_encountered
        self.main_async_func_encountered = True
        asyncfunc_ast = self.generic_visit(asyncfunc_ast)

        if main_async_func_encountered:
            return asyncfunc_ast

        decorator_list = []
        for decorator in asyncfunc_ast.decorator_list:
            if not (isinstance(decorator, ast.Name)
                    and decorator.id == 'syncit'):
                decorator_list.append(decorator)

        return ast.copy_location(
            ast.FunctionDef(
                name=self.func_name,
                args=asyncfunc_ast.args,
                body=asyncfunc_ast.body,
                decorator_list=decorator_list,
                returns=asyncfunc_ast.returns
            ),
            asyncfunc_ast
        )

    def visit_statements(self, statements):
        new_statements = []
        for stmt in statements:
            if isinstance(stmt, ast.AST):
                value = self.visit(stmt)
                if value is None:
                    continue
                elif not isinstance(value, ast.AST):
                    new_statements.extend(value)
                    continue
            new_statements.append(value)
        return new_statements

    def visit_If(self, if_ast):
        async_mode_test = (
            isinstance(if_ast.test, ast.Name) and
            if_ast.test.id == IS_ASYNC_MODE
        )

        if async_mode_test:
            self.async_mode_test_on = True

        if_ast.body = self.visit_statements(if_ast.body)

        if async_mode_test:
            self.async_mode_test_on = False

        if_ast.orelse = self.visit_statements(if_ast.orelse)

        if async_mode_test:
            return if_ast.orelse
        return if_ast

    def visit_Await(self, node):
        if not self.async_mode_test_on:
            raise NotEnclosedAwait(node.lineno)
        return node


def syncit(async_func):
    # Get source of async function as string
    source = inspect.getsource(async_func)
    # Remove indentation if it's defined as a method
    source = textwrap.dedent(source)
    # Get lineno where function is defined
    lineno = inspect.getsourcelines(async_func)[1]
    lineno_increment = lineno - 1

    func_name = async_func.__name__ + '__sync'
    transformer = Transformer(func_name)

    tree = ast.parse(source)
    # transform the tree
    try:
        tree = transformer.visit(tree)
    except NotEnclosedAwait as e:
        raise AssertionError(
            "Encountered await expression not enclosed in `if %s:` block in "
            "`%s` at lineno %s" % (
                IS_ASYNC_MODE,
                async_func.__name__,
                e.expr_lineno + lineno_increment)
        )

    ast.fix_missing_locations(tree)
    ast.increment_lineno(tree, lineno_increment)

    filename = inspect.getfile(async_func)
    module_globals = inspect.getmodule(async_func).__dict__
    exec(compile(tree, filename=filename, mode='exec'), module_globals)
    sync_func = eval(func_name, module_globals)
    sync_func.async_call = async_func
    del module_globals[func_name]
    return sync_func
