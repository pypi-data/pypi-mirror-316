"""Formatter for SELECT statements."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.SubLink, override=True)
def sub_link(node: ast.SubLink, output: stream.RawStream) -> None:
    """Printer for SubLink."""
    slt = enums.SubLinkType

    if node.subLinkType == slt.EXISTS_SUBLINK:
        output.write("EXISTS")
        output.space()
    elif node.subLinkType == slt.ALL_SUBLINK:
        output.print_node(node.testexpr)
        output.space()
        output.write(printers.dml.get_string_value(node.operName))
        output.space()
        output.write("ALL")
        output.space()
    elif node.subLinkType == slt.ANY_SUBLINK:
        output.print_node(node.testexpr)
        if node.operName:
            output.space()
            output.write(printers.dml.get_string_value(node.operName))
            output.space()
            output.write("ANY")
            output.space()
        else:
            output.space()
            output.write("IN")
            output.space()
    elif node.subLinkType == slt.EXPR_SUBLINK:
        pass
    elif node.subLinkType == slt.ARRAY_SUBLINK:
        output.write("ARRAY")
    elif node.subLinkType in (
        slt.MULTIEXPR_SUBLINK,
        slt.ROWCOMPARE_SUBLINK,
    ):
        msg = f"SubLink of type {node.subLinkType} not supported yet"
        raise NotImplementedError(msg)

    with output.expression(need_parens=False):
        bool_in_ancestors = ast.BoolExpr in node.ancestors
        indent = 7 if bool_in_ancestors else 10
        dedent = -3 if bool_in_ancestors else -3
        with output.push_indent(indent, relative=False):
            output.write("(")
            output.newline()
            output.print_node(node.subselect)
            output.newline()
            output.indent(dedent, relative=False)
            output.write(")")
            output.dedent()


@printers.node_printer(ast.SelectStmt, override=True)
def select_stmt(node: ast.SelectStmt, output: stream.RawStream) -> None:
    """Printer for SelectStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
            output.indent()

        so = enums.SetOperation

        if node.valuesLists:
            # Is this a SELECT ... FROM (VALUES (...))?
            with output.expression(isinstance(node.ancestors[0], ast.RangeSubselect)):
                output.write("VALUES")
                output.space()
                output.print_lists(node.valuesLists, standalone_items=False)
        elif node.op != so.SETOP_NONE and (node.larg or node.rarg):
            with output.push_indent():
                if node.larg:
                    with output.expression(
                        printers.dml._select_needs_to_be_wrapped_in_parens(  # noqa: SLF001
                            node.larg,
                        ),
                    ):
                        output.print_node(node.larg)
                output.newline()
                if node.op == so.SETOP_UNION:
                    output.space()
                    output.write("UNION")
                elif node.op == so.SETOP_INTERSECT:
                    output.write("INTERSECT")
                elif node.op == so.SETOP_EXCEPT:
                    output.write("EXCEPT")
                if node.all:
                    output.space()
                    output.write("ALL")
                output.newline()
                if node.rarg:
                    with output.expression(
                        printers.dml._select_needs_to_be_wrapped_in_parens(  # noqa: SLF001
                            node.rarg,
                        ),
                    ):
                        output.print_node(node.rarg)
        else:
            output.write("SELECT")
            if node.distinctClause:
                output.space()
                output.write("DISTINCT")
                if node.distinctClause[0]:
                    output.space()
                    output.write("ON")
                    output.space()
                    with output.expression(need_parens=True):
                        output.print_list(node.distinctClause)
                output.newline()
                output.space(6)
            if node.targetList:
                output.space()
                output.print_list(node.targetList)
            if node.intoClause:
                output.newline()
                output.space(2)
                output.write("INTO")
                output.space()
                if node.intoClause.rel.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
                    output.write("UNLOGGED")
                    output.space()
                elif node.intoClause.rel.relpersistence == enums.RELPERSISTENCE_TEMP:
                    output.write("TEMPORARY")
                    output.space()
                output.print_node(node.intoClause)
            if node.fromClause:
                output.newline()
                output.space(2)
                output.write("FROM")
                output.space()
                output.print_list(node.fromClause)
            if node.whereClause:
                output.newline()
                output.space()
                output.write("WHERE")
                output.space()
                output.print_node(node.whereClause)
            if node.groupClause:
                output.newline()
                output.space()
                output.write("GROUP BY")
                output.space()
                if node.groupDistinct:
                    output.write("DISTINCT")
                    output.space()
                output.print_list(node.groupClause)
            if node.havingClause:
                output.newline()
                output.write("HAVING")
                output.space()
                output.print_node(node.havingClause)
            if node.windowClause:
                output.newline()
                output.write("WINDOW")
                output.space()
                output.print_list(node.windowClause)
        if node.sortClause:
            output.newline()
            output.space()
            output.write("ORDER BY")
            output.space()
            output.print_list(node.sortClause)
        if node.limitCount:
            output.newline()
            if node.limitOption == enums.LimitOption.LIMIT_OPTION_COUNT:
                output.space()
                output.write("LIMIT")
            elif node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.space()
                output.write("FETCH FIRST")
            output.space()
            if isinstance(node.limitCount, ast.A_Const) and node.limitCount.isnull:
                output.write("ALL")
            else:
                with output.expression(
                    isinstance(node.limitCount, ast.A_Expr)
                    and node.limitCount.kind == enums.A_Expr_Kind.AEXPR_OP,
                ):
                    output.print_node(node.limitCount)
            if node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.space()
                output.write("ROWS WITH TIES")
        if node.limitOffset:
            output.newline()
            output.write("OFFSET")
            output.space()
            output.print_node(node.limitOffset)
        if node.lockingClause:
            output.newline()
            output.write("FOR")
            output.space()
            output.print_list(node.lockingClause)

        if node.withClause:
            output.dedent()


@printers.node_printer(ast.IntoClause, override=True)
def into_clause(node: ast.IntoClause, output: stream.RawStream) -> None:
    """Printer for IntoClause."""
    output.print_node(node.rel)
    if node.colNames:
        output.space()
        with output.expression(need_parens=True):
            output.print_name(node.colNames, ",")
    with output.push_indent(2):
        if node.accessMethod:
            output.write("USING")
            output.space()
            output.print_name(node.accessMethod)
            output.newline()
        if node.options:
            output.write("WITH")
            output.space()
            with output.expression(need_parens=True):
                output.print_list(node.options)
            output.newline()
        if node.onCommit != enums.OnCommitAction.ONCOMMIT_NOOP:
            output.space(2)
            output.write("ON COMMIT")
            output.space()
            if node.onCommit == enums.OnCommitAction.ONCOMMIT_PRESERVE_ROWS:
                output.write("PRESERVE ROWS")
            elif node.onCommit == enums.OnCommitAction.ONCOMMIT_DELETE_ROWS:
                output.write("DELETE ROWS")
            elif node.onCommit == enums.OnCommitAction.ONCOMMIT_DROP:
                output.write("DROP")
            output.newline()
        if node.tableSpaceName:
            output.write("TABLESPACE")
            output.space()
            output.print_name(node.tableSpaceName)
            output.newline()
