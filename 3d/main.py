import cv2
import mediapipe as mp
import pygame
import numpy as np
import math
from pygame.locals import *

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.8
)

pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🚀 Space Hand Control - 3D Object Loader")
clock = pygame.time.Clock()

def create_spaceship_mesh():
    vertices = np.array([
        [0,   0, 120],
        [15,  8, 80],
        [-15, 8, 80],
        [15,-8, 80],
        [-15,-8, 80],

        [20,  10, 80],
        [-20, 10, 80],
        [20,-10, 80],
        [-20,-10, 80],

        [25,  12,-40],
        [-25, 12,-40],
        [25,-12,-40],
        [-25,-12,-40],

        [0,   0,-80],

        [40,  0, 40],
        [80,-10,10],
        [70,-20,-20],

        [-40,  0, 40],
        [-80,-10,10],
        [-70,-20,-20],

        [0, 25,-20],
        [0, 18,-50],

        [15, -8,-40],
        [15,  2,-40],
        [15, -8,-60],
        [15,  2,-60],

        [-15,-8,-40],
        [-15, 2,-40],
        [-15,-8,-60],
        [-15, 2,-60],
    ], dtype=float)

    faces = [
        [0, 1, 2],
        [0, 3, 1],
        [0, 4, 3],
        [0, 2, 4],

        [1, 5, 6], [1, 6, 2],
        [3, 4, 8], [3, 8, 7],
        [1, 3, 7], [1, 7, 5],
        [2, 6, 8], [2, 8, 4],

        [5, 9,10], [5,10, 6],
        [7, 8,12], [7,12,11],
        [5, 7,11], [5,11, 9],
        [6,10,12], [6,12, 8],

        [9,11,13],
        [10,13,12],
        [9,13,10],
        [11,12,13],

        [5,14,1],
        [5,7,14],
        [7,16,14],
        [7,11,16],
        [14,15,1],
        [14,16,15],

        [6,2,17],
        [6,17,8],
        [8,17,19],
        [8,19,12],
        [17,2,18],
        [17,18,19],

        [10,20,21],
        [10,21,13],
        [9,13,21],
        [9,21,20],

        [22,23,25], [22,25,24],
        [23,9,25],  [9,11,25],
        [22,24,11], [22,11,7],

        [26,29,27], [26,28,29],
        [27,29,10], [29,12,10],
        [26,8,28],  [26,7,8],
    ]

    face_colors = []
    for idx in range(len(faces)):
        if idx <= 3:
            face_colors.append((220, 220, 255))
        elif 4 <= idx <= 11:
            face_colors.append((80, 160, 255))
        elif 12 <= idx <= 23:
            face_colors.append((40, 120, 240))
        elif 24 <= idx <= 35:
            face_colors.append((255, 120, 80))
        elif 36 <= idx <= 39:
            face_colors.append((200, 200, 80))
        else:
            face_colors.append((255, 180, 80))

    return vertices, faces, face_colors

def load_obj(filename):
    return create_spaceship_mesh()

class Star:
    def __init__(self):
        self.x = np.random.randint(-1000, 1000)
        self.y = np.random.randint(-1000, 1000)
        self.z = np.random.randint(1, 1500)
        self.pz = self.z
        
    def update(self, speed):
        self.z -= speed
        if self.z < 1:
            self.z = 1500
            self.x = np.random.randint(-1000, 1000)
            self.y = np.random.randint(-1000, 1000)
            self.pz = self.z
    
    def show(self, surface, center_x, center_y):
        sx = int((self.x / self.z) * 400 + center_x)
        sy = int((self.y / self.z) * 400 + center_y)
        px = int((self.x / self.pz) * 400 + center_x)
        py = int((self.y / self.pz) * 400 + center_y)
        
        self.pz = self.z
        
        if 0 <= sx < width and 0 <= sy < height:
            brightness = int(255 * (1 - self.z / 1500))
            size = max(1, int(8 * (1 - self.z / 1500)))
            color = (brightness, brightness, min(255, brightness + 50))
            pygame.draw.circle(surface, color, (sx, sy), size)
            
            if abs(sx - px) < 100 and abs(sy - py) < 100:
                trail_color = (brightness//2, brightness//2, brightness//3)
                pygame.draw.line(surface, trail_color, (px, py), (sx, sy), 1)

stars = [Star() for _ in range(300)]

class Object3D:
    def __init__(self, vertices, faces, face_colors):
        self.vertices = vertices
        self.faces = faces
        self.face_colors = face_colors
        self.rotation = [0, 0, 0]
        self.position = [width//2, height//2, 0]
        self.scale = 1.0
        if len(vertices) > 0:
            max_coord = np.max(np.abs(vertices))
            if max_coord > 0:
                self.scale = 220.0 / max_coord
        
    def rotate_vertices(self):
        if len(self.vertices) == 0:
            return self.vertices
        
        rx, ry, rz = self.rotation
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz),  np.cos(rz), 0],
            [0, 0, 1]
        ])
        
        rotated = self.vertices.copy()
        rotated = np.dot(rotated, Rx.T)
        rotated = np.dot(rotated, Ry.T)
        rotated = np.dot(rotated, Rz.T)
        
        return rotated * self.scale
    
    def project(self, vertices):
        projected = []
        fov = 500
        viewer_distance = 500
        
        for vertex in vertices:
            x, y, z = vertex
            z = z + viewer_distance
            
            if z > 0:
                factor = fov / z
                x_proj = x * factor + self.position[0]
                y_proj = y * factor + self.position[1]
                projected.append([x_proj, y_proj, z])
            else:
                projected.append([self.position[0], self.position[1], 1])
        
        return projected
    
    def draw(self, surface):
        if len(self.vertices) == 0:
            return
        
        rotated = self.rotate_vertices()
        projected = self.project(rotated)
        
        face_depths = []
        for face_idx, face in enumerate(self.faces):
            if all(i < len(projected) for i in face):
                z_avg = np.mean([projected[i][2] for i in face])
                face_depths.append((z_avg, face_idx))
        
        face_depths.sort(reverse=True)
        
        for z_depth, face_idx in face_depths:
            face = self.faces[face_idx]
            try:
                points = []
                for i in face:
                    if i < len(projected):
                        x, y = int(projected[i][0]), int(projected[i][1])
                        if 0 <= x < width*2 and 0 <= y < height*2:
                            points.append((x, y))
                if len(points) >= 3:
                    base_color = self.face_colors[face_idx]
                    depth_factor = max(0.5, min(1.2, 700.0 / (z_depth + 1)))
                    color = (
                        int(base_color[0] * depth_factor),
                        int(base_color[1] * depth_factor),
                        int(base_color[2] * depth_factor),
                    )
                    color = (
                        max(0, min(255, color[0])),
                        max(0, min(255, color[1])),
                        max(0, min(255, color[2])),
                    )
                    pygame.draw.polygon(surface, color, points)
            except:
                pass
        
        drawn_edges = set()
        for face in self.faces:
            for i in range(len(face)):
                v1 = face[i]
                v2 = face[(i + 1) % len(face)]
                edge = tuple(sorted([v1, v2]))
                
                if edge not in drawn_edges and v1 < len(projected) and v2 < len(projected):
                    drawn_edges.add(edge)
                    
                    p1 = projected[v1]
                    p2 = projected[v2]
                    
                    x1, y1 = int(p1[0]), int(p1[1])
                    x2, y2 = int(p2[0]), int(p2[1])
                    
                    if (0 <= x1 < width and 0 <= y1 < height and 
                        0 <= x2 < width and 0 <= y2 < height):
                        for thickness in range(2, 0, -1):
                            color = (0, 140 + thickness*25, 255)
                            pygame.draw.line(surface, color, (x1, y1), (x2, y2), thickness)
        
        for point in projected:
            x, y = int(point[0]), int(point[1])
            if 0 <= x < width and 0 <= y < height:
                pygame.draw.circle(surface, (200, 255, 255), (x, y), 2)

OBJ_FILENAME = "spaceship.obj"
vertices, faces, face_colors = load_obj(OBJ_FILENAME)
space_obj = Object3D(vertices, faces, face_colors)

cap = cv2.VideoCapture(0)

class Smoother:
    def __init__(self, smoothing=0.7):
        self.value = None
        self.smoothing = smoothing
    
    def update(self, new_value):
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.smoothing * self.value + (1 - self.smoothing) * new_value
        return self.value

def clamp_delta(prev, new, max_delta):
    if prev is None:
        return new
    delta = new - prev
    if delta > max_delta:
        new = prev + max_delta
    elif delta < -max_delta:
        new = prev - max_delta
    return new

smooth_hand_x = Smoother(smoothing=0.85)
smooth_hand_y = Smoother(smoothing=0.85)
smooth_hand_distance = Smoother(smoothing=0.9)

smooth_rotation_x = Smoother(smoothing=0.8)
smooth_rotation_y = Smoother(smoothing=0.8)
smooth_scale = Smoother(smoothing=0.85)

hand_x, hand_y = 0.5, 0.5
hand_distance = 0.1
auto_rotate = True
warp_speed = 5

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

running = True
print("\n🎮 Controls:")
print("   ✋ Move hand to rotate")
print("   👌 Pinch (thumb+index) to zoom")
print("   SPACE: Toggle auto-rotate")
print("   ↑↓: Warp speed")
print("   R: Reset smoothing")
print("   ESC: Quit\n")

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                auto_rotate = not auto_rotate
            elif event.key == K_UP:
                warp_speed = min(20, warp_speed + 2)
            elif event.key == K_DOWN:
                warp_speed = max(1, warp_speed - 2)
            elif event.key == K_r:
                smooth_rotation_x.value = None
                smooth_rotation_y.value = None
                smooth_scale.value = None
                smooth_hand_x.value = None
                smooth_hand_y.value = None
                smooth_hand_distance.value = None
                print("🔄 Smoothing reset")
    
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            
            index_tip = hand.landmark[8]
            thumb_tip = hand.landmark[4]

            raw_x = index_tip.x
            raw_y = index_tip.y
            raw_distance = math.sqrt(
                (thumb_tip.x - index_tip.x) ** 2 +
                (thumb_tip.y - index_tip.y) ** 2
            )

            hand_x = smooth_hand_x.update(raw_x)
            hand_y = smooth_hand_y.update(raw_y)
            hand_distance = smooth_hand_distance.update(raw_distance)
            
            target_rot_y = (hand_x - 0.5) * 3.0
            target_rot_x = (hand_y - 0.5) * 3.0

            base_scale = 200.0 / max(1, np.max(np.abs(vertices)))
            target_scale = (0.5 + hand_distance * 6.0) * base_scale
            
            rot_x_new = smooth_rotation_x.update(target_rot_x)
            rot_y_new = smooth_rotation_y.update(target_rot_y)
            scale_new = smooth_scale.update(target_scale)

            space_obj.rotation[0] = clamp_delta(space_obj.rotation[0], rot_x_new, max_delta=0.08)
            space_obj.rotation[1] = clamp_delta(space_obj.rotation[1], rot_y_new, max_delta=0.08)
            space_obj.scale = clamp_delta(space_obj.scale, scale_new, max_delta=0.05)
            
            auto_rotate = False
    
    if auto_rotate:
        space_obj.rotation[1] += 0.01
        space_obj.rotation[2] += 0.005
    
    screen.fill((5, 5, 15))
    
    for star in stars:
        star.update(warp_speed)
        star.show(screen, width//2, height//2)
    
    space_obj.draw(screen)
    
    title = font.render("🚀 SPACE NAVIGATOR", True, (0, 255, 255))
    screen.blit(title, (20, 20))
    
    controls = [
        "✋ Move hand to rotate",
        "👌 Pinch to zoom",
        "SPACE: Auto-rotate",
        "↑↓: Warp speed",
        "R: Reset smoothing",
        "ESC: Quit"
    ]
    
    y = 70
    for control in controls:
        text = small_font.render(control, True, (150, 200, 255))
        screen.blit(text, (20, y))
        y += 25
    
    status_y = height - 100
    mode = "AUTO" if auto_rotate else "MANUAL"
    mode_color = (100, 255, 100) if auto_rotate else (255, 255, 100)
    mode_text = small_font.render(f"Mode: {mode}", True, mode_color)
    screen.blit(mode_text, (20, status_y))
    
    warp_text = small_font.render(f"Warp: {warp_speed}x", True, (255, 150, 50))
    screen.blit(warp_text, (20, status_y + 25))
    
    info_text = small_font.render(f"Vertices: {len(vertices)} | Faces: {len(faces)}", True, (150, 255, 150))
    screen.blit(info_text, (20, status_y + 50))
    
    fps = int(clock.get_fps())
    fps_color = (100, 255, 100) if fps > 25 else (255, 100, 100)
    fps_text = small_font.render(f"FPS: {fps}", True, fps_color)
    screen.blit(fps_text, (width - 100, 20))
    
    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
