import pygame
import os
from sys import exit

#################################################################
##### 이페이지는 게임 개발할때 필요한 요소들을 나타낸것이다 #########
#################################################################


#################################################################
# 기본 초기화 (반드시 해야 하는 것들)

pygame.init()  # 초기화 (반드시 필요)


def gameQuit_withM(game_result):
    msg = game_font.render(game_result, True, (255, 255, 0))
    msg_rect = msg.get_rect(
        center=(int(screen_width/2), int(screen_height/2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # 2초 대기 후 꺼짐
    pygame.quit()
    exit()


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
# current_path = os.path.dirname(__file__)  # 현재파일의 위치 반환(연습과는 다른방법!!)
# image_path = os.path.join(current_path, "images")  # images 폴더위치 반환

# 배경 만들기 #실행 파일을 위해서는 절대경로로 해줘야한다!!
background = pygame.image.load(
    "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\background.png")

# 스테이지 만들기
stage = pygame.image.load(
    "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\stage.png")
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(
    "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동방향
# character_to_x = 0
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

# 캐릭터 이동속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(
    "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\weapon.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 각각 따로 처리)
ball_images = [
    pygame.image.load(
        "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\ball_XL.png"),
    pygame.image.load(
        "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\ball_L.png"),
    pygame.image.load(
        "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\ball_M.png"),
    pygame.image.load(
        "C:\\Users\\818396\\Desktop\\my_project\\Python_basic\\python_p_game\\pygame_project\\images\\ball_S.png"),
]

#  공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]  # [0]->xl 볼, [1] -> L볼 등등..

# 공들
balls = []

# 최초 발생하는 큰공 정의!(추가)
balls.append({
    "pos_x": 50,  # 공의 x 좌표
    "pos_y": 50,  # 공의 y 좌표
    "img_idx": 0,  # 공의 이미지 인덱스
    "to_x": 3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y": -6,  # y축 이동방향, 살짝 위로 올라갔다가 내려오게끔
    "init_spe_y": ball_speed_y[0]  # y 최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 30
start_ticks = pygame.time.get_ticks()  # 시작시간 정의

# 게임 종료 메시지
# timeout (시간 초과 실패)
# mission complete (성공)
# Game over (캐릭터 공에 맞음)
game_result = "Game Over"


while True:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # while 돌지않고 게임종료됨!

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                character_to_x_LEFT -= character_speed  # 키 겹칠때 멈추는거 방지
            elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:  # 무기 발사
                weapon_x_pos = character_x_pos + \
                    (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])  # 무기가 여러발
                # 될수있기때문에 리스트로 해보자!

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    # 3. 게임 캐릭터 위치 정의 (경계값 포함)
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # weapons 위치를 가져와서 w 리스트에 각각의 변화를 알려준다
    # weapons 위치가 제정의 되면 밑에서 다시 그려줄거임!
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [[w[0], w[1]-weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기 if 일때만 해당 문을 저장한다! 0보다 커야지만 저장한다!
    # 0 보다 작아짐.. 즉 Y축 의 화면 맨위로 뚫는순간 리스트에서 사라져서 blit에서 없어짐
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):  # ball리스트를 들고와서
        # ball idx의 ball value 를 출력해줌!
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 경계 처리 및 부딪혔을때 공 이동위치 반대로 변경(튕겨나옴)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1

        # 세로 위치 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"]  # 땅에닿았을때 속도 초기화
        else:
            ball_val["to_y"] += 0.5  # 올라가면서 점점 속도가 감소 내려오면서 증가!!

        # 볼위치에 이동위치를 더해준다!(자리가바뀜)
        # 이부분에의해 볼의xy 값이 to_x,y값에 의해 위치가 계속 바뀜!
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        # ball리스트를 들고와서 변수를 통해 앞으로 나올 모든 공들의 값을 정의해준다!
        # ball idx의 ball value 를 출력해줌!
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            gameQuit_withM(game_result)

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx  # 해당 무기 없애기
                ball_to_remove = ball_idx  # 해당 공 없애기

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보 index+1해서 다음공이온다!
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x 좌표
                        # 공이터지면 그 중앙에서 나타나게 할려는게 목적!
                        "pos_x": ball_pos_x + (ball_width/2) - (small_ball_width/2),
                        # 공의 y 좌표
                        "pos_y": ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx": ball_img_idx+1,  # 공의 이미지 인덱스
                        "to_x": -3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6,  # y축 이동방향, 살짝 위로 올라갔다가 내려오게끔
                        "init_spe_y": ball_speed_y[ball_img_idx+1]  # y 최초 속도
                    })

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x 좌표
                        # 공이터지면 그 중앙에서 나타나게 할려는게 목적!
                        "pos_x": ball_pos_x + (ball_width/2) - (small_ball_width/2),
                        # 공의 y 좌표
                        "pos_y": ball_pos_y + (ball_height/2) - (small_ball_height/2),
                        "img_idx": ball_img_idx+1,  # 공의 이미지 인덱스
                        "to_x": 3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6,  # y축 이동방향, 살짝 위로 올라갔다가 내려오게끔
                        "init_spe_y": ball_speed_y[ball_img_idx+1]  # y 최초 속도
                    })

                break
        else:  # 계속 게임을 진행
            continue    # 안쪽 for문의 조건이 맞지않으면 continue 하겠음
        break  # 안쪽 for문에서 break를 만나면 여기로 진입 가능. 2중 for문을 탈출방법
        # 즉 else가 없으면 for문 끝나는 순간 바로 맨밑 break로 가서 종료 되버리지만
        #  else를 통해 for문 끝나도 continue로 인해 맨밑 break는 실행이 안된다
        # 그러나 for안의 break를 만나면 for/else 문장을 빠져나와 바로 break를 만나게되
        #  break가 실행이됨으로써 2중 for문을 탈출할수있다

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료(성공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        gameQuit_withM(game_result)

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
        # 이미지 4개중 인덱스로 볼을 정한다!

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # ms -> s
    timer = game_font.render("Time : {}".format(
        int(total_time - elapsed_time)), True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    # 시간 초과 했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        gameQuit_withM(game_result)

    pygame.display.update()  # ***while을 돌면서 계속 게임화면을 그려준다! 반드시 호출되야함!!
