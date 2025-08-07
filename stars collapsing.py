import pygame
import numpy as np
import matplotlib.pyplot as plt

pygame.init()

dist0 = 300

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
width = 1000
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stars")
dt = 1
G = 10
c = 50
code = 0

class Particle():
    def __init__(self, x, y, density, radius, color, omega):
        self.x = x
        self.y = y
        self.density = density
        self.radius = radius
        self.mass = density * (4/3) * np.pi * radius ** 3
        self.color = color
        self.omega = omega

        self.x_vel = 0
        self.y_vel = 0
    
    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def gravity(particles, G, dt):
    if len(my_particles) == 2:
        p1 = particles[0]
        p2 = particles[1]

        dx = p1.x - p2.x
        dy = p1.y - p2.y

        dist2 = dx**2 + dy**2
        dist = np.sqrt(dist2)
        if dist < p1.radius + p2.radius:
            return True
        F = (G * p1.mass * p2.mass) / dist2
        Fx = F * dx / dist
        Fy = F * dy / dist

        p1.x_vel -= Fx / p1.mass * dt
        p1.y_vel -= Fy / p1.mass * dt

        p2.x_vel += Fx / p2.mass * dt
        p2.y_vel += Fy / p2.mass * dt

        LGW = (32 * G ** 4 * (p1.mass + p2.mass) ** 3 * ((p1.mass * p2.mass)/(p1.mass + p2.mass))** 2)/(5 * c ** 5 * (dist/2) ** 5)

        Eloss = LGW * dt
        Ecurr = -G * p1.mass * p2.mass / (dist)
        ENew = Ecurr - Eloss

        rnew = -G * p1.mass * p2.mass / (2 * ENew)
        scale = rnew /(dist/2)
        print(scale)
        p1.x = masscentrx + (p1.x - masscentrx) * scale
        p1.y = masscentry + (p1.y - masscentry) * scale

        p2.x = masscentrx + (p2.x - masscentrx) * scale
        p2.y = masscentry + (p2.y - masscentry) * scale

        scalev = 1 / np.sqrt(scale)
        p1.x_vel *= scalev
        p1.y_vel *= scalev
        p2.x_vel *= scalev
        p2.y_vel *= scalev

        p1.omega = np.sqrt(G * (p1.mass + p2.mass) / (dist/2)**3)
        p2.omega = p1.omega

    return False

star1 = Particle(width/2 - dist0/2, height/2, 0.05, 15, (255, 255, 255), 0)
star2 = Particle(width/2 + dist0/2, height/2, 0.05, 15, (255, 255, 255), 0)
star1.y_vel = np.sqrt((G * star1.mass) / (4 * (star2.x - star1.x)/2))
star2.y_vel = -star1.y_vel

masscentrx = (star1.x * star1.mass + star2.x * star2.mass) / (star1.mass + star2.mass)
masscentry = (star1.y * star1.mass + star2.y * star2.mass) / (star1.mass + star2.mass)

def GW(omega, t, R, r, m):
    Amp = (8 * m * omega ** 2 * R ** 2)/r 
    hplusz = -Amp * np.cos(2 * omega * t)
    hplusx = hplusz/2
    hxz = Amp * np.sin(2 * omega * t)
    hxx = hxz/2
    return hplusz, hxz, hplusx, hxx

my_particles = [star1, star2]
clock = pygame.time.Clock()
t = 0.0
data1 = []
data2 = []
data3 = []
data4 = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if code == 0:
        t += dt
        hpz, hxz, hpx, hxx = GW(star1.omega, t, (star1.x - masscentrx), 1, star1.mass)
        data1.append(hpz)
        data2.append(hxz)
        data3.append(hpx)
        data4.append(hxx)

    screen.fill((0, 0, 0))

    if gravity(my_particles, G, dt):
        code = 1
        mass_new = my_particles[0].mass + my_particles[1].mass
        r_new = (2 * G * mass_new)/(c ** 2)
        my_particles.append(Particle(masscentrx, masscentry, mass_new/((4/3) * np.pi * (r_new ** 3)) ,r_new , (255, 255, 255), 1))
        my_particles.pop(0)
        my_particles.pop(0)
        screen.fill((0, 0, 0))
        my_particles[0].display()
        running = False
    
    for p in my_particles:
        p.x += p.x_vel * dt
        p.y += p.y_vel * dt

        p.display()

    pygame.display.update() 
    clock.tick(1000)

time = np.linspace(0, t, len(data1))

ax.plot(time, data3, data1, label='h_plus_combined')
ax.plot(time, data4, data2, label='h_x_combined')
ax.plot(time, 0, data1, alpha = 0.4, label='h_plus_z-axis')
ax.plot(time, 0, data2, alpha = 0.4, label='h_x_z-axis')
ax.plot(time, data3, 0, alpha = 0.4, label='h_plus_x-axis')
ax.plot(time, data4, 0, alpha = 0.4, label='h_x_x-axis')
ax.set_xlabel('t[adapted]')
ax.set_ylabel('X')
ax.set_zlabel('Z')
ax.view_init(elev=20., azim=-35, roll=0)
ax.legend()
plt.grid(True)
plt.show()

pygame.quit()
