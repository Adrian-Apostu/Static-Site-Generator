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
