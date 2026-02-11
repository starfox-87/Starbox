# Pawn AI System

class Pawn:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)
        self.health = 100

    def move(self, x, y):
        self.position = (x, y)
        print(f"{self.name} moved to {self.position}")

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} took {amount} damage, health is now {self.health}")

    def is_alive(self):
        return self.health > 0

class AdaptiveAISystem:
    def __init__(self):
        self.pawns = []

    def add_pawn(self, pawn):
        self.pawns.append(pawn)

    def simulate_turn(self):
        for pawn in self.pawns:
            if pawn.is_alive():
                pawn.move(random.randint(-1, 1), random.randint(-1, 1))

# Example usage
if __name__ == '__main__':
    ai_system = AdaptiveAISystem()
    pawn1 = Pawn("Pawn 1")
    pawn2 = Pawn("Pawn 2")
    ai_system.add_pawn(pawn1)
    ai_system.add_pawn(pawn2)
    ai_system.simulate_turn()