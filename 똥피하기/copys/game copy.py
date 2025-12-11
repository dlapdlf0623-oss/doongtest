'''
TODO
- 게임 종료화면 만들기
- 랭킹 연동
- 추가적인 기능 있으면 추가
- 디자인 개선
'''

'''
- 파일 경로 수정
- surface, char 변수 main.py에서 받아오게 변경
- Profile 클래스 main.py로 이동
- Difficulty 클래스 super삭제, Profile클래스를 인자로 받아오게 변경
- run함수 update로 이름변경
- run함수내에 while문 제거 (main.py에서 반복문 실행)
- 반복문 제거로 인해 게임오버시 break하는 부분 제거 (대신 main.py에서 self.game_over 변수 감지해서 스크린 바꾸는걸로 변경)
'''

import pygame, sys, random
from pygame.locals import QUIT, K_LEFT, K_RIGHT

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('똥 피하기') 
#surface = pygame.display.set_mode((900, 700)) //메인화면과 통일된 surface사용을 위해, 인자 받아오는걸로 변경 #24, 32
ground = pygame.image.load('assets/main_background.png')
#char = pygame.image.load('assets/default_char.png') //캐릭터사진 인자받아오는걸로 변경 #19
poo = pygame.image.load('assets/default_poo.png')

font = pygame.font.Font('assets/font.ttf', 50)

'''민수 난이도'''
class Difficulty:
    def __init__(self, Profile): #Profile 클래스를 받아와 이름, 캐릭터모양, 난이도 변수 설정
        self.user_name = Profile.name
        self.char = Profile.char_img
        self.level = Profile.level

class Drop:
    def __init__(self, screen):
        self.x = random.randint(0, 1000)
        self.y = -3
        self.surface = screen

    def move(self):
        self.y += 7

    def draw(self):
        self.surface.blit(poo, (self.x, self.y))


class Game(Difficulty):
    def handle_event(self, screen, mouse_pos): #다른 화면에서 버튼클릭 감지때문에 실행하는 함수 (여기선 역할없음, 지우면 오류)
        pass

    def __init__(self, profile, screen, images):
        super().__init__(profile)

        self.surface = screen
        self.images = images
        self.char_img = self.char

        self.game_over = False
        self.pos_x, self.pos_y = 425, 570
        self.score = 0
        self.drop_poos = []

    def update(self, screen, mouse_pos): #run => update 이름변경, main.py에 update함수에 반복문 돌아가게 되있음
        '''
        if self.game_over: #게임오버 main.py에서 처리해서 삭제
            break
        clock.tick(60) #main.py에 존재
        '''

        if self.level == 1: A = 30
        elif self.level == 2: A = 25
        elif self.level == 3: A = 20
        elif self.level == 4: A = 15
        elif self.level == 5: A = 10
        elif self.level == 6: A = 5
        elif self.level == 7: A = 3

        if self.score % A == 0: self.drop_poos.append(Drop(self.surface))

        self.surface.blit(ground, (0, 0))
        self.surface.blit(self.char, (self.pos_x, self.pos_y))

        for poo_obj in self.drop_poos:
            poo_obj.move()
            poo_obj.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key_press = pygame.key.get_pressed()
        if key_press[K_LEFT]:
            if self.pos_x > 0: self.pos_x -= 7

        if key_press[K_RIGHT]:
            if self.pos_x < 850: self.pos_x += 7

        self.score += 1

        if (self.score % 100 == 0) and self.level < 7: self.level += 1

        text_score = font.render(f'score: {self.score}', True, (255, 255, 0))
        self.surface.blit(text_score, (20, 10))

        for poo_obj in self.drop_poos:
            if self.pos_x - 45 < poo_obj.x < self.pos_x + 45:
                if self.pos_y - 30 < poo_obj.y + 10 < self.pos_y + 10:
                    text_gameover = font.render("Game Over!", True, (255, 0, 0))
                    self.surface.blit(text_gameover, (20, 100))
                    self.game_over = True
        '''
        pygame.display.update() #main.py에 존재
        
        return {
            "user_name": self.user_name,
            "level": self.level,
            "score": self.score
            } 
            '''
    
    def get_result(self): #break사라져서 return이 안되서 따로 함수생성
        return {
            "user_name": self.user_name,
            "level": self.level,
            "score": self.score
            } 

        


'''
# 실행 예시
if __name__ == '__main__':
    game = Game(user_name="Player1", level=1)
    result = game.run()
    print(result)
    '''