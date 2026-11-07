#!/usr/bin/env python3

from elem import Text
from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                      Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)


class Page:
    def __init__(self, element):
        self.element = element

    def is_valid(self):
        if type(self.element) is Text:
            return False
        try:
            return self._validate(self.element, set())
        except (RecursionError, AttributeError, TypeError):
            return False

    def _validate(self, node, ancestors):
        allowed = (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                   Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text)
        kind = type(node)
        if kind not in allowed:
            return False
        if kind is Text:
            return True
        if id(node) in ancestors or type(node.content) is not list:
            return False
        children = node.content
        kinds = [type(child) for child in children]
        if kind is Html and kinds != [Head, Body]:
            return False
        if kind is Head and kinds != [Title]:
            return False
        if kind in (Body, Div) and any(child not in (
                H1, H2, Div, Table, Ul, Ol, Span, Text) for child in kinds):
            return False
        if kind in (Title, H1, H2, Li, Th, Td) and kinds != [Text]:
            return False
        if kind is P and any(child is not Text for child in kinds):
            return False
        if kind is Span and any(child not in (Text, P) for child in kinds):
            return False
        if kind in (Ul, Ol) and (not kinds or any(child is not Li for child in kinds)):
            return False
        if kind is Tr and (not kinds or not (
                all(child is Th for child in kinds) or
                all(child is Td for child in kinds))):
            return False
        if kind is Table and any(child is not Tr for child in kinds):
            return False
        ancestors.add(id(node))
        valid = all(self._validate(child, ancestors) for child in children)
        ancestors.remove(id(node))
        return valid

    def __str__(self):
        prefix = '<!DOCTYPE html>\n' if type(self.element) is Html else ''
        return prefix + str(self.element)

    def write_to_file(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as output:
                output.write(str(self))
        except (OSError, TypeError, ValueError, UnicodeError) as error:
            print('Error: {}'.format(error))
            return False
        return True


def test_page():
    for element in (Title, H1, H2, Li, Th, Td):
        assert Page(element(Text('text'))).is_valid()
        assert not Page(element()).is_valid()
        assert not Page(element([Text('one'), Text('two')])).is_valid()
    for element in (Ul, Ol):
        assert Page(element(Li(Text('item')))).is_valid()
        assert not Page(element()).is_valid()
        assert not Page(element(Text('item'))).is_valid()
    assert Page(P([Text('one'), Text('two')])).is_valid()
    assert not Page(P(Span())).is_valid()
    assert Page(Span([Text('text'), P(Text('paragraph'))])).is_valid()
    assert not Page(Span(H1(Text('heading')))).is_valid()
    assert Page(Table([Tr(Th(Text('heading'))), Tr(Td(Text('cell')))])).is_valid()
    assert not Page(Tr([Th(Text('heading')), Td(Text('cell'))])).is_valid()
    assert not Page(Tr()).is_valid()
    assert not Page(Table(Td(Text('cell')))).is_valid()
    for element in (Body, Div):
        assert Page(element([H1(Text('heading')), H2(Text('subheading')),
                             Div(), Table(), Ul(Li(Text('item'))),
                             Ol(Li(Text('item'))), Span(), Text('text')])).is_valid()
        assert not Page(element(P(Text('paragraph')))).is_valid()
    assert Page(Html([Head(Title(Text('title'))), Body()])).is_valid()
    assert not Page(Html([Body(), Head(Title(Text('title')))])).is_valid()
    assert not Page(Head([Title(Text('title')), Meta()])).is_valid()
    assert not Page(Head()).is_valid()
    for element in (Meta, Img, Hr, Br):
        assert Page(element()).is_valid()
    assert not Page(Text('text')).is_valid()
    assert not str(Page(Div())).startswith('<!DOCTYPE')
    assert str(Page(Html())).startswith('<!DOCTYPE html>\n')
    cyclic = Div()
    cyclic.add_content(cyclic)
    assert not Page(cyclic).is_valid()


def main():
    try:
        test_page()
        page = Page(Html([
            Head(Title(Text('A valid page'))),
            Body([H1(Text('Hello ground!')), Span(Text('Welcome.')),
                  Ul([Li(Text('Python')), Li(Text('Django'))]),
                  Table([Tr([Th(Text('Language'))]),
                         Tr([Td(Text('Python'))])])])], attr={'lang': 'en'}))
        assert page.is_valid()
        print(page)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
