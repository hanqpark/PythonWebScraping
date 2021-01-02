class Car():
    # wheels = 4
    # doors = 4
    # windows = 4
    # seats = 4

    def __init_(self, **kwargs):
        self.wheels = 4
        self.doors = 4
        self.windows = 4
        self.seats = 4
        self.color = kwargs.get("color", "black")
        self.price = kwargs.get("price", "$700")

    def __str__(self):
        return f"Car with {self.wheels} wheels"

# Inheritance => 상속
class Convertable(Car):
    # extending methods
    def __init__(self, **kwargs):
        super().__init__(**kwargs)     # 부모 클래스를 호출하는 함수
        self.time = kwargs.get("time", 10)

    def take_off(self):
        return "taking off"

    def __str__(self):
        return f"Car with with no roof"

tsla = Car(color="green", price="$40")
print(tsla.color, tsla.price)

mini = Car()
print(mini.color, mini.price)