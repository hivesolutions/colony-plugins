# COP-003: Template Compiler

## Document Information

| Field               | Value                                                     |
| ------------------- | --------------------------------------------------------- |
| **Document Number** | COP-003                                                   |
| **Date**            | 2026-09-11                                                |
| **Author**          | João Magalhães <joamag@hive.pt>                           |
| **Subject**         | Translation of Template Trees into Python Bytecode        |
| **Status**          | Implemented                                               |
| **Version**         | 1.0                                                       |

## Description

### Problem

The template engine renders by walking the abstract syntax tree and dispatching a visitor method for every node of every render. Once the repeated parsing was removed, the dispatch itself became the dominant cost of the render path: every node pays a method resolution, a `before_visit`, an `after_visit` and a recursive `accept`, and every literal chunk of text costs a full visit just to be written to the buffer.

This is a structural ceiling rather than a set of remaining inefficiencies, as the profile of the render path is almost entirely made of interpreter bookkeeping instead of the actual production of contents.

### Solution

Translate the already parsed tree into python source once, compile it with the built-in `compile()` and keep the resulting function next to the parsed tree in the templates cache. The control flow of the template becomes the control flow of the generated function, the literal parts become constants, and the per node dispatch disappears.

The visitor is **not** replaced. It remains both the reference implementation and the fallback for everything the compiler does not cover, which keeps the extension points intact and bounds the risk of the change.

## Design

### Generated code

The generated function receives the visitor and the sequence of constants, and starts by aliasing the values it uses repeatedly:

```python
def render(visitor, constants):
    write = visitor.write
    resolve = visitor.resolve
    global_map = visitor.global_map
    write(constants[0])
    for _element_8 in _iterable_1:
        write_out(visitor, resolve(_value_11, constants[5]), constants[6])
```

No value that originates from a template is ever part of the generated source. Every literal, name and comparison function is placed in the constants tuple and referred to by position, so a template can never influence the shape of the emitted program.

### Coverage and fallback

The compiler is deliberately conservative and refuses a whole tree whenever it contains a construct it does not fully understand, in which case the visitor renders the template exactly as before. The following is translated:

- the literal contents, joined so that a run of them costs a single write
- the output nodes that define only a value and the auto escaping mode
- the conditionals, including the `elif` and `else` branches
- the iterations, both the `{% for %}` and the `${foreach}` forms
- the assignments

The following falls back to the visitor:

- the filtering of values
- the tag family, apart from the iteration one
- the inclusion and the extension of templates
- the output nodes that define extra attributes (prefix, format, quoting, among others)

The rendering also falls back whenever the context is not the default one, meaning a non default visitor or a process method attached to it, as both change the meaning of the nodes at runtime.

### Optimizations

- **Literal joining**, a run of contiguous literal nodes results in a single constant and a single write.
- **Pre encoded literals**, the literal constants are encoded at compile time so that the write operation does not encode them on every single render.
- **Local binding of the iteration value**, the value of an iteration is bound to a local of the generated function so that the contents read it directly instead of going through the global map. The binding is skipped whenever the contents re-assign the very same name.
- **Conditional loop bookkeeping**, the loop related values are only maintained when the contents of the iteration actually read them.

### Equivalence

For any template the compiler accepts, the compiled output must be byte identical to the interpreted one. This is enforced by the test suite rather than by a handful of cases: every rendering assertion renders the template through both paths and compares the results, so the equivalence is a property of the whole suite.

## Trade-offs

| Aspect          | Benefit                                          | Cost                                                     |
| --------------- | ------------------------------------------------ | -------------------------------------------------------- |
| Render speed    | Around twice as fast for the accepted templates  | None at render time                                       |
| Compilation     | Paid once per file, kept in the templates cache  | A small amount of work on the first parse of each file    |
| Coverage        | The common content templates are accepted        | The templates using filters or inclusion keep the visitor |
| Maintainability | The visitor stays the single reference           | Two rendering paths have to be kept equivalent            |

## Future work

- Translate the filtering of values, which is what keeps most of the real templates out of the compiled path.
- Translate the inclusion and the extension of templates, which requires the expansion of the tree to happen before the compilation.
- Emit a narrower resolver for the cases where it is provably equivalent, measured as being worth a further factor of two.
