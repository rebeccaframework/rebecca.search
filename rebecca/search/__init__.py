import colander as c
from sqlalchemy import and_


class AbstractExpression:
    base_type = c.String

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def __call__(self):
        if self.value == c.null:
            return True
        return self.sql(self.column, self.value)


class EqualExpression(AbstractExpression):
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


class RangeExpression(AbstractExpression):
    def sql(self, column, value):
        return and_(column <= value, column >= value)


class ExpressionType(c.SchemaType):
    def __init__(self,
                 column,
                 base_type=c.String,
                 expression_cls=EqualExpression):
        super(ExpressionType, self).__init__()
        self.column = column
        self.base_type = base_type
        self.expression_cls = expression_cls

    def serialize(self, node, appstruct):
        if isinstance(appstruct, AbstractExpression):
            appstruct = appstruct.value
        return self.base_type.serialize(node, appstruct)

    def deserialize(self, node, cstruct):
        value = self.base_type.deserialize(node, cstruct)
        return self.expression_cls(self.column, value)

    def contains(self, typ=c.String()):
        return self.__class__(self.column, typ, ContainsExpression)

    def in_(self, typ=c.Set()):
        return self.__class__(self.column, typ, InExpression)

    def eq(self, typ=c.String()):
        return self.__class__(self.column, typ, EqualExpression)


def sa_col(column):
    return ExpressionType(column)
