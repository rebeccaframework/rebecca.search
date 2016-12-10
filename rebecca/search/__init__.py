import colander as c
import deform


class AbstractExpression:
    base_type = c.String

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def __call__(self):
        if self.value == c.null:
            return True
        return self.sql(self.column, self.value)


class Expression(AbstractExpression):
    def sql(self, column, value):
        return column == value


class InExpression(AbstractExpression):
    def sql(self, column, value):
        if not value:
            return True
        return column.in_(value)


class ContainsExpression(AbstractExpression):
    def sql(self, column, value):
        return column.contains(value)


class ExpressionType(c.SchemaType):
    def __init__(self,
                 column,
                 base_type_cls=c.String,
                 expression_cls=Expression):
        super(ExpressionType, self).__init__()
        self.column = column
        self.base_type = base_type_cls()
        self.expression_cls = expression_cls

    def serialize(self, node, appstruct):
        if isinstance(appstruct, AbstractExpression):
            appstruct = appstruct.value
        return self.base_type.serialize(node, appstruct)

    def deserialize(self, node, cstruct):
        value = self.base_type.deserialize(node, cstruct)
        return self.expression_cls(self.column, value)

    def contains(self):
        return self.__class__(self.column, self.base_type, ContainsExpression)

    def in_(self):
        return self.__class__(self.column, c.Set, InExpression)


def sa_col(column):
    return ExpressionType(column)


class SearchForm(deform.Form):
    def search(self, request, query):
        controls = request.params.items()
        params = self.validate(controls)
        expressions = [e() for e in params.values()]
        return query.filter(*expressions)
