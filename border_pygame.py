from __future__ import annotations
import pygame
from pygame import Vector2

pygame.init()
point_size = 10
image = pygame.image.load("border_dotless.png")
width, height = image.get_size()

window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


class Point():
    points:list[Point] = []
    point_selected:Point = None

    [staticmethod]
    def get_nearest_points(position:Vector2, amount:int) -> list[Point]:
        if amount <= 0:
            return []
        
        # points and distances from farthest to closest
        points_near = []
        distances = []
        
        for i, point in enumerate(Point.points):
            dist = (point.position-position).length()
            # if the first point add it and continue
            if i == 0:
                points_near.append(point)
                distances.append(dist)
                continue
            
            index = 0
            for point_dist in distances:
                if dist < point_dist:
                    index += 1
                else:
                    break

            points_near.insert(index, point)
            distances.insert(index, dist)
            if len(distances) > amount:
                points_near.pop(0)
                distances.pop(0)

        return points_near


    def __init__(self, position:Vector2):
        self.position:Vector2 = position
        Point.points.append(self)
    
    def update(self):
        # color should be green if mouse is over, blue if touching point_selected, and red otherwise.
        if Point.point_selected is self:
            color = (0, 255, 0) 
        elif self.touching_point():
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)
        pygame.draw.circle(window, color, self.position, point_size)

    def touching_point(self) -> bool:
        if Point.point_selected == None:
            return False
        
        if self in Point.get_nearest_points((Point.point_selected.position+self.position)/2, 2):
            return True
        else:
            return False



points = [
    Point(Vector2(270.78063344719027, 658.7651155582982)),
    Point(Vector2(37.89591803586478, 689.0072017464784)),
    Point(Vector2(124.81130887031148, 180.89270296010227)),
    Point(Vector2(748.938943892807, 140.6900446245136)),
    Point(Vector2(10.93392332355765, 357.0940294018386)),
    Point(Vector2(36.31938010703945, 196.45065312430515)),
    Point(Vector2(474.0281109811982, 63.60971851353932)),
    Point(Vector2(686.0984206424878, 316.30692972708835)),
    Point(Vector2(291.6728060073435, 140.55789706677717)),
    Point(Vector2(570.5553405532719, 657.8043269221783)),
    Point(Vector2(189.6174002634755, 507.98217698521603)),
    Point(Vector2(707.4404673170274, 167.0819591563597)),
    Point(Vector2(303.6970619596356, 414.670015327001)),
    Point(Vector2(48.042312111267506, 639.5115721280457)),
    Point(Vector2(442.50956707879664, 731.502015563621)),
    Point(Vector2(105.10415782400483, 312.04259476823347)),
    Point(Vector2(509.85180721516826, 406.1278695882836)),
    Point(Vector2(221.89651305412693, 164.45427510942596)),
    Point(Vector2(642.8568021648784, 14.782129341315397)),
    Point(Vector2(158.96327716239387, 591.3864653381297)),
    Point(Vector2(762.891732541894, 275.05658390528174)),
    Point(Vector2(560.3687566649254, 236.0449684244887)),
    Point(Vector2(232.24123119931443, 233.96619642187045)),
    Point(Vector2(348.1004302456613, 692.2182667315024)),
    Point(Vector2(320.9411493787119, 614.5722058081868)),
    Point(Vector2(716.0057770074247, 615.7070769162254)),
    Point(Vector2(627.0249278939309, 139.21623938899225)),
    Point(Vector2(8.72548253616364, 297.2832597325638)),
    Point(Vector2(266.2871279543885, 455.1482801740641)),
    Point(Vector2(547.2413516978048, 362.4444999907706)),
    Point(Vector2(422.95898145843785, 360.0062170670582)),
    Point(Vector2(294.84423246743637, 750.2218940051487)),
]

near_points = Point.get_nearest_points(Vector2(100, 150), 2)
for point in near_points:
    print((point.position-Vector2(100, 150)).length())

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pygame Renderer")
    
    running = True
    while running:
        window.fill((255, 0, 255))
        window.blit(image, (0, 0))
        mouse_pos = Vector2(pygame.mouse.get_pos())
        
        # set `Point` hover_point
        for point in points:
            Point.point_selected = None
            if (point.position-mouse_pos).length()<point_size:
                Point.point_selected = point
                break

        for point in points:
            point.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
