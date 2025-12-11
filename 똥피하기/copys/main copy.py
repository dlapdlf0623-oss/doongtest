import pygame, sys
from objects import Button, TextInput
from photo import Photo
from game import Game

username = ''
gamelevel = 1

def Yeongdo_Bold(size): #중복된 구문 줄여 코드작성 편하게 해주는 함수
    return pygame.font.Font("assets/font.ttf", size)

def get_screen(): #game.py에 surface 주기위한 함수
    return screen

class Profile: #이름, 캐릭터이미지, 난이도, 점수 저장하는 클래스, game.py에 Difficulty에 전달됨. (점수 기본 : 0)
    def __init__(self, name, char_img, level, score=0):
        self.name = name
        self.char_img = char_img
        self.score = score
        self.level = level

    def set_score(self, score): #점수설정 (안쓰임)
        self.score = score

class ScreenTemplate: #스크린 템플릿 (아래에서 자동으로 실행되기 편한 형식)
    def __init__(self):
        pass #한번만 설정하면 되는부분 삽입. ex) self.변수설정, 버튼, 텍스트, rect등 
    def update(self, screen, mouse_pos):
        pass #계속 반복되면서 수정되야 하는 부분 삽입 ex) 충돌감지, 마우스 위치 감지 등
    def handle_event(self, event, mouse_pos):
        pass #pygame.event 쓰이는것 삽입 ex) 키 감지, 마우스 클릭감지

class Main_Screen: #접속시 보이는 가장 기본 메인화면
    def __init__(self, char_img=None, poo_img=None):
        if char_img == None: #(캐릭터,난이도 설정화면) => (메인화면) 시에 캐릭터 이미지 유지위한 함수
            self.head_img = pygame.image.load("assets/default_char.png")
        else:
            self.head_img = char_img
        if poo_img == None: #위의 똥버전 (혹시 똥 바꿀수있게 남겨둠)
            self.poo_img = pygame.image.load("assets/default_poo.png")
        else:
            self.poo_img = poo_img

        btn1_img = pygame.image.load("assets/300x100.png") #버튼 이미지(그냥 300x100 흰화면)
        btn2_img = pygame.image.load("assets/300x100.png")
        self.main_bg = pygame.image.load("assets/main_background.png") #배경 이미지 로드
        self.button1 = Button(btn1_img, (250,500), '게임방법', Yeongdo_Bold(60), "#000000", "#585858") #버튼생성 
        self.button2 = Button(btn2_img, (650,500), '게임시작', Yeongdo_Bold(60), "#000000", "#585858") #(자세한건 objects.py주석 참고)

        self.text_logo = Yeongdo_Bold(167).render("똥 피하기", True, "#644608") #메인화면의 로고
        self.text_logo_rect = self.text_logo.get_rect(center=(450,230)) #위치 표현 용이하게 하기위해 rect설정

        self.btn_list = [self.button1, self.button2] #버튼 여러개일때 같은 함수 반복해서 쓰는걸 방지하기 위한 리스트

    def update(self, screen, mouse_pos):
        screen.blit(self.main_bg, (0,0)) #배경화면 보이게 설정
        screen.blit(self.text_logo, self.text_logo_rect) #로고 보이게 설정
        for btn in self.btn_list: #버튼 반복문
            btn.check_hover_button(mouse_pos) #마우스가 버튼위에 있을때 버튼의 글자 색 바뀌게 설정
            btn.update(screen) #버튼 blit 해주는 역할

    def handle_event(self, event, mouse_pos):
        global current_screen #현재 화면을 알려주고, 바꾸는 전역변수

        if event.type == pygame.MOUSEBUTTONDOWN: #마우스 버튼 눌렸을때 (좌클릭, 우클릭)
            if self.button1.check_button_click(mouse_pos): #마우스가 버튼위에 있는지 감지 (버튼 클릭 감지)
                current_screen = Game_Guide() #게임방법으로 이동
            elif self.button2.check_button_click(mouse_pos): #마우스가 버튼위에 있는지 감지 (버튼 클릭 감지)
                current_screen = Set_Profile_Screen(self.head_img, self.poo_img) #스크린을 프로필 설정으로 이동 (몸이미지와 똥이미지 줌)


class Set_Profile_Screen: #프로필 난이도 설정 화면
    def __init__(self, char_img, poo_img):
        self.char_img = char_img #위에서 받아온 인자들을
        self.poo_img = poo_img   #인스턴스 변수로 변경

        self.main_bg = pygame.image.load("assets/main_background.png") #배경이미지 로드
        self.char_pic_btn_img = pygame.image.load("assets/200x100.png") #사진찍는 버튼 이미지 로드(현재 200x100흰화면)

        self.easy_btn_img = pygame.image.load("assets/200x100.png") #각각 쉬움, 보통, 어려움 난이도 설정 버튼 사진지정
        self.normal_btn_img = pygame.image.load("assets/200x100.png")
        self.hard_btn_img = pygame.image.load("assets/200x100.png")

        self.text_logo = Yeongdo_Bold(167).render("똥 피하기", True, "#644608") #로고

        self.easy_btn = Button(self.easy_btn_img, (225, 600), 'easy', Yeongdo_Bold(60), "#000000", '#585858') #위 난이도 버튼들 생성
        self.normal_btn = Button(self.normal_btn_img, (450, 600), 'normal', Yeongdo_Bold(60), '#000000', '#585858')
        self.hard_btn = Button(self.hard_btn_img, (675, 600), 'hard', Yeongdo_Bold(60), '#000000', '#585858')
        self.char_pic_btn = Button(self.char_pic_btn_img, (225, 450), '사진 촬영', Yeongdo_Bold(50), '#000000', '#585858')#사진찍는 버튼
        
        self.text_input = TextInput(575, 425, 200, 50, Yeongdo_Bold(30), placeholder='닉네임 입력', max_length=11) 
        #닉네임쓰는거생성(object.py)참고
    
        self.char_img_rect = self.char_img.get_rect(center=(450, 450)) #캐릭터사진(뭔지 보여주는거) rect지정
        self.text_logo_rect = self.text_logo.get_rect(center=(450,230)) #로고 클릭가능하게 하기위해 rect지정

        self.btn_list = [self.char_pic_btn, self.easy_btn, self.normal_btn, self.hard_btn] #버튼 여러개일때 같은 함수 반복해서 쓰는걸 방지하기 위한 리스트
        
    def update(self, screen, mouse_pos):
        screen.blit(self.main_bg, (0,0))
        screen.blit(self.char_img, self.char_img_rect)
        screen.blit(self.text_logo, self.text_logo_rect) #표시하기
        
        self.text_input.draw(screen) #text_input blit하는거

        for btn in self.btn_list:
            btn.check_hover_button(mouse_pos)
            btn.update(screen)

    def handle_event(self, event, mouse_pos):
        global username, gamelevel
        global current_screen

        self.text_input.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.char_pic_btn.check_button_click(mouse_pos):
                self.char_img_ts = Photo.take_picture(' ', 'ts') #사진을 찍는클래스 호출(photo.py), 그 결과를 타임스탬프(파일이름)으로 받아옴 
                if self.char_img_ts == None: #사진안찍히면 뒷코드 실행방지
                    return
                
                #self.sized_head_img = pygame.transform.scale(pygame.image.load(f"image/original/{self.char_img_ts}.png"), (100, 100))
                #머리이미지 크기조정해주는 역할 (혹시 랭킹클래스에서 쓸수도 있을거같아 그냥 주석처리)

                self.char_img = pygame.image.load(f"image/full/{self.char_img_ts}.png") #본게임에 넘길 캐릭터전신

            elif self.text_logo_rect.collidepoint(mouse_pos):
                current_screen = Main_Screen(self.char_img, self.poo_img) #로고 클릭하면 메인화면으로

            elif self.easy_btn.check_button_click(mouse_pos): #난이도 설정버튼 클릭하면
                gamelevel = 1                                 #게임레벨을 해당난이도로 변경하고
                username = self.text_input.get_value()        #유저네임을 유저가 입력한 텍스트로 변경
                if len(username) < 1:                         #근데 만약 유저네임길이가 0이라면
                    self.text_input.add_placeholder('!')      #placeholder에 !을 추가함(닉네임을 입력하세요!!! 이런식으로바뀜) // 임시 
                    return                                    #뒷 코드 실행방지
                user_profile = Profile(username, self.char_img, gamelevel)  #game.py에 Difficult클래스에 프로필 넘겨주기위해 프로필 설정
                current_screen = Game(user_profile, get_screen(), self.char_img) #Game클래스에 프로필, surface, 캐릭터 이미지 넘겨주고
                                                                                 #스크린 변경
            elif self.normal_btn.check_button_click(mouse_pos): #위랑 게임레벨빼고 동일
                gamelevel = 2
                username = self.text_input.get_value()
                if len(username) < 1:
                    self.text_input.add_placeholder('!')
                    return
                user_profile = Profile(username, self.char_img, gamelevel)
                current_screen = Game(user_profile, get_screen(), self.char_img)

            elif self.hard_btn.check_button_click(mouse_pos): #위랑 게임레벨빼고 동일
                gamelevel = 3
                username = self.text_input.get_value()
                if len(username) < 1:
                    self.text_input.add_placeholder('!')
                    return
                user_profile = Profile(username, self.char_img, gamelevel)
                current_screen = Game(user_profile, get_screen(), self.char_img)


class Game_Guide: #게임 방법설명 화면
    def __init__(self):
        self.back_btn_img = pygame.image.load("assets/300x100.png") #돌아가기 버튼 이미지 로드
        self.img = pygame.image.load("assets/game_guide.jpg") #게임 설명화면은 그냥 전체가 하나의 이미지임

        self.img_rect = self.img.get_rect(center=(450,350))
        self.back_btn = Button(self.back_btn_img, (450,600), '돌아가기', Yeongdo_Bold(40), "#000000", "#585858")

        self.btn_list = [self.back_btn] #그냥 새로쓰기 귀찮아서 있던코드 재활용

    def update(self, screen, mouse_pos):
        screen.blit(self.img, self.img_rect) #blit
        for btn in self.btn_list:
            btn.check_hover_button(mouse_pos)
            btn.update(screen)

    def handle_event(self, event, mouse_pos):
        global current_screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.check_button_click(mouse_pos):
                current_screen = Main_Screen() #돌아가기 버튼 누르면 메인화면으로 이동

class Score_screen:
    def __init__(self, result, char_img):
        self.char_img = char_img              # ← 딱 이것만 추가

        self.score = result['score']
        self.username = result['user_name']
        self.level = result['level']

        self.text = Yeongdo_Bold(50).render(f'name : {self.username}, level : {self.level}, score : {self.score}', True, '#000000')
        #여러 정보들 표시 / 임시로 값 확인용도

        btn1_img = pygame.image.load("assets/300x100.png") #버튼 이미지(그냥 300x100 흰화면)
        btn2_img = pygame.image.load("assets/300x100.png")
        self.main_bg = pygame.image.load("assets/main_background.png") #배경 이미지 로드
        self.button1 = Button(btn1_img, (250,500), '게임 재시작', Yeongdo_Bold(60), "#000000", "#585858") #버튼생성 
        self.button2 = Button(btn2_img, (650,500), '게임 종료', Yeongdo_Bold(60), "#000000", "#585858") #(자세한건 objects.py주석 참고)

        self.btn_list = [self.button1, self.button2] #버튼 여러개일때 같은 함수 반복해서 쓰는걸 방지하기 위한 리스트

    def update(self, screen, mouse_pos):
        screen.blit(self.text, (100,300))

        for btn in self.btn_list: #버튼 반복문
            btn.check_hover_button(mouse_pos) #마우스가 버튼위에 있을때 버튼의 글자 색 바뀌게 설정
            btn.update(screen) #버튼 blit 해주는 역할

    def handle_event(self, event, mouse_pos):
        global current_screen #현재 화면을 알려주고, 바꾸는 전역변수

        if event.type == pygame.MOUSEBUTTONDOWN: #마우스 버튼 눌렸을때 (좌클릭, 우클릭)
            if self.button1.check_button_click(mouse_pos): #마우스가 버튼위에 있는지 감지 (버튼 클릭 감지)
                user_profile = Profile(self.username, self.char_img, gamelevel)
                current_screen = Game(user_profile, screen, self.char_img)
            elif self.button2.check_button_click(mouse_pos): #마우스가 버튼위에 있는지 감지 (버튼 클릭 감지)
                pygame.quit()
                sys.exit()


if __name__ == '__main__': #import시 실행방지
    pygame.init()
    pygame.display.set_caption('똥 피하기') #창 이름 지정
    screen = pygame.display.set_mode((900, 700)) #창 사이즈 지정
    clock = pygame.time.Clock() #60프레임 제한 걸기위함

    current_screen = Main_Screen() #맨처음은 메인화면 진입


    while True:
        mouse_pos = pygame.mouse.get_pos() #마우스 현재 위치
        for event in pygame.event.get():   #파이게임 이벤트 받아오기
            if event.type == pygame.QUIT:   #창에 x버튼 누르면 창꺼지게 하는 코드
                pygame.quit()
                exit()

            current_screen.handle_event(event, mouse_pos) #위의 Screen_Template클래스 참고

        current_screen.update(screen, mouse_pos) #얘도 Screen_Template참고
        pygame.display.update() #화면 업데이트
        clock.tick(60) #프레임제한

        if isinstance(current_screen, Game) and current_screen.game_over: #현재 스크린이 Game(게임화면) 스크린인지와 게임오버 감지
            result = current_screen.get_result() #게임오버시 결과 불러오기
            current_screen = Score_screen(result, current_screen.char_img) #결과 표시화면