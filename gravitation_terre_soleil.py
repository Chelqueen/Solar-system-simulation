import pygame
import numpy as np
import time

# initialize pygame
pygame.init()

# define width of screen
width = 1400
# define height of screen
height = 800
screen_res = (width, height)

pygame.display.set_caption("Gravitation terre soleil")
screen = pygame.display.set_mode(screen_res)

# define colors
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

pos_sol = np.array([0., 0.]) # m
pos_ter = np.array([1.5e11, 0.]) # m
vel_ter = np.array([0., 30000]) # m/s
vel_sol = np.array([0., 0.]) # m/s
# caméra
pos_cam = np.array([0., 0.]) # m
ech_cam = 2.5e-9

# temps
ech_tmp = 1e6
# plus c'est gros plus la simulation est en accéléré, 1 = temps réel
# la terre met normalement 365 jrs pour faire une révolution soit 31536000 s ~= 3e7 s
# donc si on met 3e7 ici la terre mettra une seconde

# constantes
G = 6.664e-11 # m³/kg/s²
Ms = 2e30 # kg
Mt = 6e24 # kg

debut = time.time()

def transfo_camera(pt):

	## Prend un point du monde (en mètres) et donne la position sur l'écran (en pixels)

	pt_rel = pt - pos_cam # on prend le point relatif à la position de la caméra
	pt_ech = pt_rel * ech_cam # on met à l'échelle
	pt_int = pt_ech.astype(np.int32) # on arrondit
	pt_cen = pt_int + [width // 2, height // 2] # on met au centre de l'écran
	return pt_cen

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        # check if a user wants to exit the game or not
        if event.type == pygame.QUIT:
            exit()

    # fill black color on screen
    screen.fill(black)

    dTS_vec = pos_sol - pos_ter # m
    dTS_val = np.linalg.norm(dTS_vec) # m

    dST_vec = pos_ter - pos_sol  # m
    dST_val = np.linalg.norm(dST_vec)  # m
    
    mtn = time.time()
    dt = (mtn - debut) * ech_tmp # s
    debut = mtn
    
    a_ter_val = G * Ms / (dTS_val ** 2) # m/s²
    a_ter_vec = a_ter_val * (dTS_vec / dTS_val) # m/s²
    
    vel_ter += a_ter_vec * dt # m/s
    pos_ter += vel_ter * dt # m

    a_sol_val = G * Mt / (dST_val ** 2)  # m/s²
    a_sol_vec = a_sol_val * (dST_vec / dST_val)  # m/s²

    vel_sol += a_sol_vec * dt  # m/s
    pos_sol += vel_sol * dt  # m
    
    ec_ter = 0.5 * Mt * (np.linalg.norm(vel_ter) ** 2) # J
    ep_ter = Mt * a_ter_val * dTS_val # J
    print(f"{ec_ter:.8} {ep_ter:.8} {ec_ter + ep_ter:.8}")

    pygame.draw.circle(
        surface=screen, color=yellow, center=transfo_camera(pos_sol), radius=5)

    pygame.draw.circle(
        surface=screen, color=blue, center=transfo_camera(pos_ter), radius=1)

    # update screen
    pygame.display.flip()