class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = []
        for prop in self.props:
            result.append(f'{prop}="{self.props[prop]}"')
        return ' '.join(result)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def init(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"