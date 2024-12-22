
class MimicQuerySet:
    def __init__(self, objects=[]):
        self.objects = objects
        self.filer_pk = None

    def all(self):
        return self

    def filter(self, **kwargs):
        if "pk" in kwargs:
            self.filer_pk = kwargs["pk"]
        elif "id" in kwargs:
            self.filer_pk = kwargs["id"]
        return self

    def get(self, **kwargs):
        if kwargs and "pk" in kwargs:
            return self.objects[kwargs["pk"]]
         
        elif self.filer_pk is not None:
            return self.objects[self.filer_pk]
        return None

    def order_by(self, *args):
        return self
    
    def first(self):
        return self.objects[0]

    def last(self):
        return self.objects[-1]

    def count(self):
        return len(self.objects)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, index):
        return self.objects[index]

    def __iter__(self):
        return iter(self.objects)
