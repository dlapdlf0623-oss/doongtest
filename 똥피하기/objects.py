import pygame

class Button:
    def __init__(self, image, pos: tuple[int,int], text, font, base_color, hovering_color):
            self.image = image
            self.pos_x = pos[0]
            self.pos_y = pos[1]
            self.font = font
            self.base_color = base_color
            self.hovering_color = hovering_color
            self.text_data = text
            self.text = self.font.render(text, True, self.base_color) #렌더링 시킨 텍스트를 변수저장

            self.button_rect = self.image.get_rect(center=(self.pos_x, self.pos_y)) #버튼의 범위값을 이미지의 크기로 지정
            self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y)) #텍스트의 범위값을 텍스트 크기로 지정
    
    def update(self, screen):
        screen.blit(self.image, self.button_rect) #버튼의 이미지 띄우기
        screen.blit(self.text, self.text_rect) #버튼의 텍스트 띄우기

    def check_button_click(self, mouse_pos):
        return self.button_rect.collidepoint(mouse_pos)
    
    def check_hover_button(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos): #마우스 커서가 버튼위에 있으면
            self.text = self.font.render(self.text_data, True, self.hovering_color) #버튼의 텍스트를 hovering_color 색으로 교체
        else: #그 반대
            self.text = self.font.render(self.text_data, True, self.base_color)
    

class TextInput:
    def __init__(self, x, y, w, h, font, text_color=pygame.Color("white"), color_inactive=pygame.Color("lightskyblue3", ),color_active=pygame.Color("dodgerblue2"), cursor_interval=500, max_length=None, placeholder="", bg_color=pygame.Color("black")):

        self.rect = pygame.Rect(x, y, w, h) #사각형 rect(범위) 하나 생성
        self.bg_color = bg_color

        self.font = font
        self.text_color = text_color
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = color_inactive

        self.active = False #textinput이 선택되있는지 감지
        self.text = ""
        self.placeholder = placeholder #그 입력하기 전에 보이는 회색 글자 (placeholder라고 검색하면 설명나옴)
        self.max_length = max_length #글자 최대길이

        self.cursor_visible = True #커서 깜빡이게 할건지 여부
        self.cursor_last_switch = 0 #커서 깜빡이게 하기위한 시간감지용
        self.cursor_interval = cursor_interval #커서 깜빡이는 속도, 기본 0.5초

    def get_value(self): #textinput 안에있는 값 가져오기
        return self.text
    
    def add_placeholder(self, text): #placeholder에 더하기 (닉네임 비었을때 사용하는 함수 / main.py #142)
        self.placeholder += text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos): #textinput클릭시 활성화 되게함
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive #활성화여부에 따라 컬러 다르게 설정

            if not self.active:
                self.cursor_visible = False #액티브 안되있으면 커서 안보이게
            else:
                self.cursor_visible = True #액티브시 커서 보이게
                self.cursor_last_switch = pygame.time.get_ticks() #커버 깜빡이는 시간

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: #백스페이스시 하나 지우기
                self.text = self.text[:-1]
            elif event.key == pygame.K_DELETE: #Delete키와 Tab키누르면
                self.text += ""
            elif event.key == pygame.K_TAB:    #문자가 깨져보여서 입력방지
                self.text += ""
            else:
                if (self.max_length is None) or (len(self.text) < self.max_length):
                    if event.unicode in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ': #이모티콘, 특수문자 등 막는용도
                        self.text += event.unicode #알파벳이여야만 추가됨

            self.cursor_visible = True
            self.cursor_last_switch = pygame.time.get_ticks() #커서깜빡임 시간감지

    def update(self):
        now = pygame.time.get_ticks()
        if self.active and now - self.cursor_last_switch >= self.cursor_interval: #커서 깜빡이게 하는 부분
            self.cursor_visible = not self.cursor_visible 
            self.cursor_last_switch = now

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect) #rect에 색을 채워넣는 역할
        if self.text == "" and not self.active and self.placeholder: #placeholder만드는 역할
            display_text = self.placeholder
            display_color = (150, 150, 150) #회색
        else:
            display_text = self.text
            display_color = self.text_color

        txt_surface = self.font.render(display_text, True, display_color)

        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5)) #텍스트 blit
        pygame.draw.rect(surface, self.color, self.rect, 2)

        if self.active and self.cursor_visible: #글자 위치에 맞게 커서 그리기
            text_width = self.font.render(self.text, True, self.text_color).get_width()
            cursor_x = self.rect.x + 5 + text_width + 1
            cursor_y = self.rect.y + 5
            cursor_h = self.font.get_height()
            pygame.draw.rect(surface, self.text_color,
                             (cursor_x, cursor_y, 2, cursor_h))