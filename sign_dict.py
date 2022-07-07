class ChangeSigns:

    @staticmethod
    def change_signs(text):
        for i in ",/?;:\|=+`@#$%^& ":
            text = text.replace(i, str(hex(ord(i)))[1:].title())
        return text
