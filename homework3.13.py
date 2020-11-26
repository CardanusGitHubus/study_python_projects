class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", " ")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(f'{attribute}="{value}"')
        attrs = " ".join(attrs)

        if self.children:
            opening = f"<{self.tag} {attrs}>"
            internal = f"{self.text}"
            for child in self.children:
                internal += "\n" + str(child)
            ending = f"</{self.tag}>\n"
            return opening + internal + ending
        else:
            if self.is_single:
                return f"<{self.tag} {attrs}/>"
            else:
                return f"<{self.tag} {attrs}>{self.text}</{self.tag}>\n"


class TopLevelTag(Tag):
    def __init__(self, tag, klass=None, is_single=False, toplevel=True, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.toplevel = toplevel


class HTML(TopLevelTag):
    def __init__(self, tag="html", klass=None, is_single=False, toplevel=True, output=None):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.toplevel = toplevel
        self.output = output

    def __exit__(self, type, value, traceback):
        if self.toplevel:
            if self.output is not None:
                file_object = open(f"{self.output}", "w", encoding="utf-8")
                file_object.write(f"<{self.tag}>")
                file_object.close()
            print(f"<{self.tag}>")
            for child in self.children:
                if self.output is not None:
                    file_object = open(f"{self.output}", "a", encoding="utf-8")
                    file_object.write(f"{child}")
                    file_object.close()
                print(child)

            if self.output is not None:
                file_object = open(f"{self.output}", "a", encoding="utf-8")
                file_object.write(f"</{self.tag}>")
                file_object.close()
            print(f"</{self.tag}>")


# if __name__ == "__main__":

# проверка обычным вводом атрибутов

with HTML(output="name_of_file.html") as html:
    with TopLevelTag("body") as body:
        with Tag("div") as div:
            div.attributes["class"] = "container"
            div.text = "Текст Div"
            with Tag("p") as paragraph:
                paragraph.text = "Какой-то текст"
                div.children.append(paragraph)

            body.children.append(div)

        html.children.append(body)

# проверка вводом кортежем класса, остальные атрибуты **kwargs

with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head.children.append(title)
        doc.children.append(head)

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body.children.append(h1)

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div.children.append(paragraph)

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div.children.append(img)

            body.children.append(div)

        doc.children.append(body)
