#!/usr/bin/python3


class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        Do you really need a comment to understand this method?..
        """
        return self.escape(super().__str__()).replace('\n', '\n<br />\n')

    @staticmethod
    def escape(value):
        return (str(value).replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """
    class ValidationError(Exception):
        def __init__(self):
            super().__init__('Invalid HTML element or content.')

    def __init__(self, tag='div', attr=None, content=None, tag_type='double'):
        """
        __init__() method.

        Obviously.
        """
        if (not isinstance(tag, str) or not tag or
                tag_type not in ('simple', 'double') or
                (attr is not None and (not isinstance(attr, dict) or
                                       not all(isinstance(key, str)
                                               for key in attr)))):
            raise self.ValidationError()
        self.tag = tag
        self.attr = {} if attr is None else dict(attr)
        self.tag_type = tag_type
        self.content = []
        if content is not None:
            self.add_content(content)

    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...).
        """
        if self.tag_type == 'double':
            result = '<' + self.tag + self.__make_attr() + '>'
            result += self.__make_content()
            if self.content:
                result += '\n'
            result += '</' + self.tag + '>'
        elif self.tag_type == 'simple':
            result = '<' + self.tag + self.__make_attr() + ' />'
        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + pair[0] + '="' + Text.escape(pair[1]) + '"'
        return result

    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """

        if len(self.content) == 0:
            return ''
        result = '\n'
        result += '\n'.join('  ' + str(elem).replace('\n', '\n  ')
                            for elem in self.content)
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))


if __name__ == '__main__':
    try:
        print(Elem('html', content=[
            Elem('head', content=Elem('title', content=Text('"Hello ground!"'))),
            Elem('body', content=[
                Elem('h1', content=Text('"Oh no, not again!"')),
                Elem('img', attr={'src': 'http://i.imgur.com/pfp3T.jpg'},
                     tag_type='simple')])]))
    except Exception as error:
        print(error)
