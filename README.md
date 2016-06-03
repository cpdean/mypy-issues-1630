This demonstrates a bug where the fast-parser of mypy will crash when someone incorrectly
documents a function that is closed over by a function that is used in a monkey patch

The expected behavior would be an error informing the user of what they've done wrong, or at least that a given function
is not documented right, rather than a hard crash of mypy

Running the test case:

```
mkvirtualenv testcase -p `which python3`
pip install -r requirements.txt
mypy --fast-parser --silent-imports --py2 --check-untyped-defs --disallow-untyped-defs testcase.py
```

This produces a traceback:

```

Traceback (most recent call last):
  File "/Users/cdean/.virtualenvs/testcase/bin/mypy", line 6, in <module>
    main(__file__)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/main.py", line 54, in main
    res = type_check_only(sources, bin_dir, options)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/main.py", line 102, in type_check_only
    python_path=options.python_path)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/build.py", line 209, in build
    dispatch(sources, manager)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/build.py", line 1255, in dispatch
    process_graph(graph, manager)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/build.py", line 1386, in process_graph
    process_stale_scc(graph, scc)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/build.py", line 1416, in process_stale_scc
    graph[id].type_check()
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/build.py", line 1235, in type_check
    manager.type_checker.visit_file(self.tree, self.xpath)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 419, in visit_file
    self.accept(d)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 460, in accept
    typ = node.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 531, in accept
    return visitor.visit_decorator(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 1922, in visit_decorator
    e.func.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 462, in accept
    return visitor.visit_func_def(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 573, in visit_func_def
    self.check_func_item(defn, name=defn.name())
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 631, in check_func_item
    self.check_func_def(defn, typ, name)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 739, in check_func_def
    self.accept_in_frame(item.body)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 475, in accept_in_frame
    answer = self.accept(node, type_context)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 460, in accept
    typ = node.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 715, in accept
    return visitor.visit_block(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 1132, in visit_block
    self.accept(s)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 460, in accept
    typ = node.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 462, in accept
    return visitor.visit_func_def(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 573, in visit_func_def
    self.check_func_item(defn, name=defn.name())
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 631, in check_func_item
    self.check_func_def(defn, typ, name)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 739, in check_func_def
    self.accept_in_frame(item.body)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 475, in accept_in_frame
    answer = self.accept(node, type_context)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 460, in accept
    typ = node.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 715, in accept
    return visitor.visit_block(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 1132, in visit_block
    self.accept(s)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 460, in accept
    typ = node.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 812, in accept
    return visitor.visit_return_stmt(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 1566, in visit_return_stmt
    typ = self.accept(s.expr, return_type)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 462, in accept
    report_internal_error(err, self.errors.file, node.line)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 460, in accept
    typ = node.accept(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/nodes.py", line 1174, in accept
    return visitor.visit_call_expr(self)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checker.py", line 1980, in visit_call_expr
    return self.expr_checker.visit_call_expr(e)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checkexpr.py", line 141, in visit_call_expr
    return self.check_call_expr_with_callee_type(callee_type, e)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checkexpr.py", line 192, in check_call_expr_with_callee_type
    e.arg_names, callable_node=e.callee)[0]
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checkexpr.py", line 235, in check_call
    callee, args, arg_kinds, formal_to_actual)
  File "/Users/cdean/.virtualenvs/testcase/lib/python3.5/site-packages/mypy/checkexpr.py", line 330, in infer_arg_types_in_context2
    res[ai] = self.accept(args[ai], callee.arg_types[i])
IndexError: list index out of range

*** INTERNAL ERROR ***

testcase.py:48: error: Internal error -- please report a bug at https://github.com/python/mypy/issues

NOTE: you can use "mypy --pdb ..." to drop into the debugger when this happens.
```

to demonstrate this is related to the fast-parser, omit that flag:

```
mypy --silent-imports --py2 --check-untyped-defs --disallow-untyped-defs testcase.py
# testcase.py: note: In function "wrapper_execute":
# testcase.py:31: error: Type signature has too few arguments
```

The slow parser's message is helpful and tells me what I've done wrong.

Additionally, the `--check-untyped-defs` flag seems to contribute to the error, as omitting it will not reproduce my bug:

```
mypy --fast-parser --silent-imports --py2 --disallow-untyped-defs testcase.py
# testcase.py: note: In function "wrapper_execute":
# testcase.py:31: error: Type signature has too few arguments
# testcase.py:35: error: "str" not callable
# testcase.py:40: error: Callable[[Any, Any], Any] has no attribute "mogrify"
# testcase.py: note: In function "queries_captured":
# testcase.py:45: error: "TimeTrackingCursor" has no attribute "executemany"
```

You can replace the incorrect annotation with the correct one and the bug doesn't happen:

```
    def wrapper_execute(self, action, sql, params=()):
        # type: (TimeTrackingCursor, Callable, str, Iterable[Any]) -> None
```

Or even with an incorrect annotation with the right number of arguments, and the bug doesn't happen:

```
    def wrapper_execute(self, action, sql, params=()):
        # type: (Foo, Callable, str, Iterable[Any]) -> None
```


