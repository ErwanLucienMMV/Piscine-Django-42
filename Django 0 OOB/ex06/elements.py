#!/usr/bin/env python3

from elem import Elem, Text


class _Element(Elem):
    tag_type = 'double'

    def __init__(self, content=None, attr=None):
        super().__init__(self.tag, attr, content, self.tag_type)


class Html(_Element):
    tag = 'html'


class Head(_Element):
    tag = 'head'


class Body(_Element):
    tag = 'body'


class Title(_Element):
    tag = 'title'


class Meta(_Element):
    tag = 'meta'
    tag_type = 'simple'


class Img(_Element):
    tag = 'img'
    tag_type = 'simple'


class Table(_Element):
    tag = 'table'


class Th(_Element):
    tag = 'th'


class Tr(_Element):
    tag = 'tr'


class Td(_Element):
    tag = 'td'


class Ul(_Element):
    tag = 'ul'


class Ol(_Element):
    tag = 'ol'


class Li(_Element):
    tag = 'li'


class H1(_Element):
    tag = 'h1'


class H2(_Element):
    tag = 'h2'


class P(_Element):
    tag = 'p'


class Div(_Element):
    tag = 'div'


class Span(_Element):
    tag = 'span'


class Hr(_Element):
    tag = 'hr'
    tag_type = 'simple'


class Br(_Element):
    tag = 'br'
    tag_type = 'simple'


def test_elements():
    for element in (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                    Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br):
        instance = element(attr={'id': 'example'})
        assert isinstance(instance, Elem)
        if element in (Meta, Img, Hr, Br):
            assert str(instance) == '<{} id="example" />'.format(instance.tag)
        else:
            assert str(instance) == '<{0} id="example"></{0}>'.format(instance.tag)
            instance.add_content(Text('<content>'))
            assert '&lt;content&gt;' in str(instance)
    assert str(Html([Head(), Body()])) == (
        '<html>\n  <head></head>\n  <body></body>\n</html>')
    assert str(P(Text('one\ntwo'))) == '<p>\n  one\n  <br />\n  two\n</p>'


def main():
    try:
        test_elements()
        print(Html([
            Head(Title(Text('"Hello ground!"'))),
            Body([H1(Text('"Oh no, not again!"')),
                  Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})])]))
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
