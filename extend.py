

class Extend():
    def __init__(self,target):
        self.target=target

    def my_input(self,name,text):
        self.target.find_element_by_id(name).send_keys(text)
