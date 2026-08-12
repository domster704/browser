class HTML:
    def __init__(self, content: str):
        self.content = content

    def show(self):
        in_tag = False
        for char in self.content:
            if char == "<":
                in_tag = True
            elif char == ">":
                in_tag = False
            elif not in_tag:
                print(char, end="")
