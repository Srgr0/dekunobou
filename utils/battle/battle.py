#指定した回数だけ対戦し, 対戦結果等を表示する
import subprocess
import tqdm
import yaml

from board import *
from legalmovelist import *

with open("config.yaml") as f:
    config=yaml.safe_load(f)

def go(board,engine_path):
    #エンジンに実行権限を与える
    subprocess.run(["chmod","u+x",engine_path])
    cp=subprocess.run([engine_path,str(board),str(int(board.turn))],encoding="utf-8",stdout=subprocess.PIPE)
    return int(cp.stdout)

def match(engine_black,engine_white):
    board=Board()
    pass_count=0
    while True:
        if pass_count>1:
            break
        moves=LegalMoveList(board)

        if len(moves)==0:
            board.push(64)
            pass_count+=1
            continue
        
        pass_count=0

        #後手番
        if board.turn:
            move=go(board,engine_white)
        else:
            move=go(board,engine_black)
        
        #着手
        board.push(move)
    
    if board.point[0]>board.point[1]:
        return 0
    elif board.point[0]<board.point[1]:
        return 1
    else:
        return 2

if __name__=="__main__":
    result=[0,0,0] #[engine1の勝ち数,engine2の勝ち数,引き分け回数]
    for i in tqdm.tqdm(range(config["match_times"]//2)):
        r1=match(config["engine1"],config["engine2"])
        r2=match(config["engine1"],config["engine2"])

        result[r1]+=1
        if r2==2:
            result[r2]+=1
        else:
            result[(r1+1)%2]+=1