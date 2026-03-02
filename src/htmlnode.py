class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = []
        if self.props is None or self.props is {}:
            return ""
        else:
            for key, value in self.props.items():
                result.append(f' {key}="{value}"')
            return "".join(result)

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.props}"

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have children")
        result = f"<{self.tag}{self.props_to_html()}>"
        while len(self.children) > 0:
            result += self.children.pop(0).to_html()
        return result + f"</{self.tag}>"
