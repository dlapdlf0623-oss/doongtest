import time, cv2, numpy, pygame

class Photo:
    WEIGHT = 50
    HEIGHT = 50

    @staticmethod
    def take_picture(picture_key=' ', kind='img'):
        try:
            cap = cv2.VideoCapture(0) #0번 카메라 지정
            if not cap.isOpened():
                print("카메라오류")
                exit()
            while True:
                ret, frame = cap.read()
                if not ret:
                    raise Exception('프레임 존재안함')

                cv2.imshow('Camera', frame)
                key = cv2.waitKey(1)
                if key == 27 or cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1: #esc와 x누르면 사진창 닫힘
                    cap.release() #카메라 끄고 정리
                    cv2.destroyAllWindows()
                    break
                if key & 0xFF == ord(picture_key):
                    cap.release() #카메라 끄고 정리
                    cv2.destroyAllWindows()
                    return Photo.crop_face(frame, kind)
        except:
            pass # 기본 이미지 사용

    @staticmethod
    def img_resize(img, w, h, kind):
        height, width, channel = img.shape #사진 크기 불러오기
        x1 = (width - height) // 2 
        x2 = width - ((width - height) // 2) #1:1 크롭위한 정중앙 계산공식 (보통 높이가 더 작으므로 높이기준으로 1:1 크롭함)
        crop_image = img[0:height,x1:x2]
        resized_image = cv2.resize(crop_image, (w,h)) #원하는 크기로 이미지 리사이즈
        ts = time.time()
        f_name = f'image/original/{ts}.png' #이미지 상대경로 지정 (이미지 이름을 타임스탬프로 지정/덮어쓰기 방지)
        cv2.imwrite(f_name, resized_image) #이미지 저장
        return Photo.make_body(resized_image, ts, kind) #이미지 경로 리턴

    @staticmethod
    def crop_face(img, kind): #얼굴 이미지 자르는 함수
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        ) #opencv내에 얼굴정면 학습된 파일을 불러온다
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #인식 용이하게 하기위해 흑백으로 변경
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5) #얼굴 위치찾기, 두 인수는 정확도 관련

        if len(faces) == 0: #얼굴이 하나도 감지 안될시
            return Photo.img_resize(img, Photo.WEIGHT, Photo.HEIGHT, kind) #이미지 크롭하기
        
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3]) #인식된 얼굴이미지들중 제일 큰걸 선택하고, 좌표계산
        face_crop = img[y:y+h, x:x+w] #크롭하기
        resized_image = cv2.resize(face_crop, (Photo.WEIGHT, Photo.HEIGHT)) #크롭된 이미지를 일정한 사이즈로 가공
        ts = time.time() #파일명을 위해 타임스탬프
        cv2.imwrite(f'image/original/{ts}.png', resized_image) #파일 저장
        return Photo.make_body(resized_image, ts, kind) #얼굴에 팔다리 달기
    
    @staticmethod    
    def make_body(img, ts, kind): #몸이랑 붙이기
        body_img = cv2.imread('assets/body.png')
        full_img = numpy.vstack((img, body_img)) #사진 위 아래 붙여주는 함수
        path = f'image/full/{ts}.png'
        cv2.imwrite(path, full_img)

        if kind == 'ts':
            return f'{ts}'
        elif kind == 'original_img':
            return pygame.image.load(f'image/original/{ts}.png')
        
class Profile: #이름, 캐릭터이미지, 난이도, 점수 저장하는 클래스, game.py에 Difficulty에 전달됨. (점수 기본 : 0)
    def __init__(self, name, char_img, level, score=0):
        self.name = name
        self.char_img = char_img
        self.score = score
        self.level = level

    def set_score(self, score): #점수설정 (안쓰임)
        self.score = score
    
    @classmethod
    def make_profile(cls, name, char_img, level, score=0):
        return cls(name, char_img, level, score)