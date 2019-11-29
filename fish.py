import math
from statistics import mean


class Coordinate():
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset(self):
        self.x = 0
        self.y = 0


class Bird():
    """
    Bird Class
    """
    def __init__(self, x, y, vx, vy, identifier, field_info, others, view):
        """Bird Class Constructor

        BOID用のエージェントです
        :param x: x coordinate
        :param y: y coordinate
        :param vx: x方向の移動量
        :param vy:　y方向の移動量
        :param id: 識別用id
        :param field_info: (field_width, field_height, fish_radius, fish_speed)
        :param others: other fish
        :param view: 視野の広さ(半径)
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.identifier = identifier
        self.others = others
        self.view = view
        self.field_info = field_info
        self.inverse_x = self.field_info[0] - self.x
        self.inverse_y = self.field_info[1] - self.y
        self.r1 = 1.0
        self.r2 = 0.8
        self.r3 = 0.3
        self.neighbors = []  # 近くにいるエージェント

        self.v1 = Coordinate()
        self.v2 = Coordinate()
        self.v3 = Coordinate()

    def set_others(self, others):
        self.others = others
        self.find_neighbors()

    # 結合
    def cohesion(self):
        center_pull_coeff = 10
        if len(self.neighbors) == 0:
            return
        self.v1.x = mean([agent.x for agent in self.neighbors if not agent.identifier == self.identifier])
        self.v1.y = mean([agent.y for agent in self.neighbors if not agent.identifier == self.identifier])
        self.v1.x = (self.v1.x - self.x) / center_pull_coeff
        self.v1.y = (self.v1.y - self.y) / center_pull_coeff

    # 離脱
    def separation(self):
        personal_space = 30
        for agent in self.neighbors:
            if self.identifier == agent.identifier:
                continue

            dist = self.calc_distance(agent, self)
            if dist <= personal_space:
                self.v2.x -= (agent.x - self.x) / dist
                self.v2.y -= (agent.y - self.y) / dist

    def _separation(self):
        if len(self.neighbors) == 0:
            return
        self.v2.x = mean([agent.x for agent in self.neighbors if not agent.identifier == self.identifier]) - self.x
        self.v2.y = mean([agent.y for agent in self.neighbors if not agent.identifier == self.identifier]) - self.y

    # 距離の計算
    def calc_distance(self, a, b):
        return min(math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2),
                   math.sqrt((a.inverse_x - b.x) ** 2 + (a.inverse_y - b.y) ** 2)+10)

    # 整列
    def alignment(self):
        if len(self.neighbors) == 0:
            return
        self.v3.x = mean([agent.x for agent in self.neighbors if not self.identifier == agent.identifier])
        self.v3.y = mean([agent.y for agent in self.neighbors if not self.identifier == agent.identifier])
        self.v3.x = (self.v3.x - self.vx) / 2
        self.v3.y = (self.v3.y - self.vy) / 2

    def collision_detection(self):
        if self.x - self.field_info[2] <= 0:
            self.x = (self.x + self.vx + self.field_info[0]) % self.field_info[0]
        if self.x + self.field_info[2] >= self.field_info[0]:
            self.x = (self.x + self.vx) % self.field_info[0]

        if self.y - self.field_info[2] <= 0:
            self.y = (self.y + self.vy + self.field_info[1]) % self.field_info[1]
        if self.y + self.field_info[2] >= self.field_info[1]:
            self.y = (self.y + self.vy) % self.field_info[1]

    def step(self):
        self.cohesion()
        self.separation()
        self.alignment()

    def find_neighbors(self):
        self.neighbors = [neighbor for neighbor in self.others
                          if self.calc_distance(self, neighbor) <= self.view and
                          not self.identifier == neighbor.identifier]

    def update(self):
        self.vx += self.r1 * self.v1.x + self.r2 * self.v2.x + self.r3 * self.v3.x
        self.vy += self.r1 * self.v1.y + self.r2 * self.v2.y + self.r3 * self.v3.y

        distance = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if distance > self.field_info[3]:
            self.vx = (self.vx / distance) * self.field_info[3]
            self.vy = (self.vy / distance) * self.field_info[3]

        self.x += self.vx
        self.y += self.vy

        self.collision_detection()

        self.inverse_x = self.field_info[0] - self.x
        self.inverse_y = self.field_info[1] - self.y

    def clear_movement(self):
        self.v1.reset()
        self.v2.reset()
        self.v3.reset()

    def draw(self):
        self.clear_movement()
        self.step()
        self.update()
        return self.x, self.y, self.vx, self.vy

