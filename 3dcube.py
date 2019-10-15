import sys
import math

import pygame

class Vertex:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def rotate_x(self, angle):
        """Rotate X by an angle"""
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)

        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa

        return Vertex(self.x, y, z)

    def rotate_y(self, angle):
        """Rotate Y by an angle"""
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)

        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa

        return Vertex(x, self.y, z)

    def rotate_z(self, angle):
        """Rotate Z by an angle"""
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa

        return Vertex(x, y, self.z)
    
    def project(self, window_width, window_height, fov, view_dist):
        """Makes the 3D point 2D"""
        try:
            factor = fov / (view_dist + self.z)
        except ZeroDivisionError:
            return self

        x = self.x * factor + window_width / 2
        y = -self.y * factor + window_height / 2

        return Vertex(x, y, 1)

class Renderer:
    def __init__(self, window_width = 640, window_height = 480):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((window_width, window_height))
        self.font = pygame.font.SysFont("Sans Serif", 30)

        self.fov = 256
        self.view_dist = 4

        self.speed = 1
        
        self.clock = pygame.time.Clock()

        self.vertecies = [
            Vertex(-1,1,-1),
            Vertex(1,1,-1),
            Vertex(1,-1,-1),
            Vertex(-1,-1,-1),
            Vertex(-1,1,1),
            Vertex(1,1,1),
            Vertex(1,-1,1),
            Vertex(-1,-1,1)
        ]

        self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
    
    def run(self):
        """Main Window Loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 5:
                        self.fov -= 10
                    
                    elif event.button == 4:
                        self.fov += 10
                
                if event.type == pygame.KEYDOWN:
                    if event.key == 275:
                        self.view_dist -= 1
                    
                    elif event.key == 276:
                        self.view_dist += 1

                    elif event.key == 270:
                        self.speed += 1
                    
                    elif event.key == 269:
                        self.speed -= 1

            self.clock.tick(50)
            self.screen.fill((0,0,0))

            transformed = []

            try:
                for vertex in self.vertecies:
                    rotation = vertex.rotate_x(self.angle_x).rotate_y(self.angle_y).rotate_z(self.angle_z)

                    projected = rotation.project(self.screen.get_width(), self.screen.get_height(), self.fov, self.view_dist)

                    transformed.append(projected)
                
                for face in self.faces:
                    pygame.draw.line(self.screen, (255,255,255), (transformed[face[0]].x, transformed[face[0]].y), (transformed[face[1]].x, transformed[face[1]].y))
                    pygame.draw.line(self.screen, (255,255,255), (transformed[face[1]].x, transformed[face[1]].y), (transformed[face[2]].x, transformed[face[2]].y))
                    pygame.draw.line(self.screen, (255,255,255), (transformed[face[2]].x, transformed[face[2]].y), (transformed[face[3]].x, transformed[face[3]].y))
                    pygame.draw.line(self.screen, (255,255,255), (transformed[face[3]].x, transformed[face[3]].y), (transformed[face[0]].x, transformed[face[0]].y))
                
                self.angle_x += self.speed
                self.angle_y += self.speed
                self.angle_z += self.speed
            except TypeError:
                pass

            x = self.font.render(f"X Total: {self.angle_x}", False, (255,255,255))
            y = self.font.render(f"Y Total: {self.angle_y}", False, (255,255,255))
            z = self.font.render(f"Z Total: {self.angle_z}", False, (255,255,255))

            speed = self.font.render(f"Rotation Speed: {self.speed} (Use + or - to control)", False, (255,255,255))
            transformations = self.font.render(f"View Distance: {self.view_dist} (Use left and right arrows to control)", False, (255,255,255))
            fov = self.font.render(f"FOV: {self.fov} (Use scroll to control)", False, (255,255,255))

            self.screen.blit(x, (10, 410))
            self.screen.blit(y, (10, 435))
            self.screen.blit(z, (10, 460))

            self.screen.blit(speed, (10, 10))
            self.screen.blit(transformations, (10, 30))
            self.screen.blit(fov, (10, 50))

            pygame.display.flip()

if __name__ == "__main__":
    Renderer().run()