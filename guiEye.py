import pygame
import cv2


def put_vid_on_screen(sample_surface, frame_max, frame_min, x, y):
    if frame_max.size != 0 and frame_min.size != 0:
        frame_max = cv2.cvtColor(frame_max, cv2.COLOR_BGR2RGB)
        frame_min = cv2.cvtColor(frame_min, cv2.COLOR_BGR2RGB)

        frame_max = cv2.rotate(frame_max, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_min = cv2.rotate(frame_min, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_max = pygame.surfarray.make_surface(frame_max)
        frame_min = pygame.surfarray.make_surface(frame_min)


        sample_surface.blit(frame_max, (0, 0))
        sample_surface.blit(frame_min, (x, y))
        pygame.display.flip()
