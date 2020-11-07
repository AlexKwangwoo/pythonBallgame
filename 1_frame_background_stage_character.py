import pygame
import os
from sys import exit

#################################################################
##### 이페이지는 게임 개발할때 필요한 요소들을 나타낸것이다 #########
#################################################################


#################################################################
# 기본 초기화 (반드시 해야 하는 것들)

pygame.init()  # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640  # 가로 크기
screen_height = 480  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Kwangwoo Pang")  # 게임 이름

# FPS
clock = pygame.time.Clock()
#################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임이미지, 좌표, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재파일의 위치 반환(연습과는 다른방법!!)
image_path = os.path.join(current_path, "images")  # images 폴더위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

while True:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # while 돌지않고 게임종료됨!

    # 3. 게임 캐릭터 위치 정의 (경계값 포함)

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()  # ***while을 돌면서 계속 게임화면을 그려준다! 반드시 호출되야함!!
