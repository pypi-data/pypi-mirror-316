class Operator:
    def __init__(self, operator_type, params=None):
        self.operator_type = operator_type
        self.params = params or {}
        self.id = f"{operator_type}-{hash(frozenset(self.params.items()))}"
        print(f"Created operator '{self.operator_type}' with params: {self.params}")
