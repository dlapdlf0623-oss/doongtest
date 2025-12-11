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
                rank1 = f'1등: {self.sorted_df['username'][0]}, 점수: {self.sorted_df['score'][0]}, 최고 레벨:{self.sorted_df['level'][0]}'
                rank2 = f'2등: {self.sorted_df['username'][1]}, 점수: {self.sorted_df['score'][1]}, 최고 레벨:{self.sorted_df['level'][1]}'
                rank3 = f'3등: {self.sorted_df['username'][2]}, 점수: {self.sorted_df['score'][2]}, 최고 레벨:{self.sorted_df['level'][2]}'
                return rank1, rank2, rank3
            
            elif len(self.sorted_df) == 2:
                rank1 = f'1등: {self.sorted_df['username'][0]}, 점수: {self.sorted_df['score'][0]}, 최고 레벨:{self.sorted_df['level'][0]}'
                rank2 = f'2등: {self.sorted_df['username'][1]}, 점수: {self.sorted_df['score'][1]}, 최고 레벨:{self.sorted_df['level'][1]}'
                rank3 = '3등:'
                return rank1, rank2, rank3
            
            elif len(self.sorted_df) == 1:
                rank1 = f'1등: {self.sorted_df['username'][0]}, 점수: {self.sorted_df['score'][0]}, 최고 레벨:{self.sorted_df['level'][0]}'
                rank2 = '2등:'
                rank3 = '3등:'
                return rank1, rank2, rank3

            elif len(self.sorted_df) == 0:
                rank1 = '1등:'
                rank2 = '2등:'
                rank3 = '3등:'
                return rank1, rank2, rank3

        else: 
            rank1 = '1등'
            rank2 = '2등'
            rank3 = '3등'
            return rank1, rank2, rank3


'''ldf = Rank('User1', 7, 170)
print(ldf.created_at)
ldf.to_csv()'''