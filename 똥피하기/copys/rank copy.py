import pandas as pd
from datetime import datetime
import os

class Rank:

    def __init__(self, username, level, score):
        self.username = username
        self.level = level
        self.score = score
        self.created_at = datetime.now()

    def to_csv(self):
        temp_df = pd.DataFrame([{ # 한 줄로 들어감
            'username': self.username,
            'level': self.level,
            'score': self.score,
            'time': self.created_at
        }])

        file_exists = os.path.isfile('rank_log.csv') # 파일 존재 여부

        temp_df.to_csv('rank_log.csv', mode='a', index=False, header=not file_exists)
        # append 모드, 파일 존재시 헤더 없이, 파일 미존재시 헤더 포함

class Top3:
    def __init__(self, path):
        self.path = path

    def result(self):
        if os.path.isfile(self.path) == True: # 파일 존재 여부
            self.sorted_df = pd.read_csv(self.path).sort_values(by='score', ascending=False, ignore_index=True)

            if len(self.sorted_df) >= 3:
                counts = 'Rank\n1등\n2등\n3등'
                users =  f'User\n{self.sorted_df['username'][0]}\n{self.sorted_df['username'][1]}\n{self.sorted_df['username'][2]}'
                scores = f'Score\n{self.sorted_df['score'][0]}\n{self.sorted_df['score'][1]}\n{self.sorted_df['score'][2]}'
                levels =  f'Level\n{self.sorted_df['level'][0]}\n{self.sorted_df['level'][1]}\n{self.sorted_df['level'][2]}'
                return counts, users, scores, levels
            
            elif len(self.sorted_df) == 2:
                counts = 'Rank\n1등\n2등\n3등'
                users =  f'User\n{self.sorted_df['username'][0]}\n{self.sorted_df['username'][1]}'
                scores = f'score\n{self.sorted_df['score'][0]}\n{self.sorted_df['score'][1]}'
                levels =  f'level\n{self.sorted_df['level'][0]}\n{self.sorted_df['level'][1]}'
                return counts, users, scores, levels
            
            elif len(self.sorted_df) == 1:
                counts = 'Rank\n1등\n2등\n3등'
                users =  f'User\n{self.sorted_df['username'][0]}'
                scores = f'score\n{self.sorted_df['score'][0]}'
                levels =  f'level\n{self.sorted_df['level'][0]}'
                return counts, users, scores, levels

        else: 
            counts = 'Rank\n1등\n2등\n3등'
            users = 'User'
            scores = 'score'
            levels = 'level'
            return counts, users, scores, levels


'''ldf = Rank('User1', 7, 170)
print(ldf.created_at)
ldf.to_csv()'''