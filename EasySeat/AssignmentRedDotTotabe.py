import json

# 读取现有的 D5data.json 文件
json_file = "reddot.json"
try:
    with open(json_file, "r") as f:
        red_dot_centers = json.load(f)
except FileNotFoundError:
    red_dot_centers = []

red_dot_centers[89-1][2] = 1  
red_dot_centers[89-1][3] = 7 

red_dot_centers[88-1][2] = 1  
red_dot_centers[88-1][3] = 4 

red_dot_centers[87-1][2] = 1  
red_dot_centers[87-1][3] = 1 

red_dot_centers[81-1][2] = 1  
red_dot_centers[81-1][3] = 11 

red_dot_centers[80-1][2] = 1  
red_dot_centers[80-1][3] = 8 

red_dot_centers[79-1][2] = 1  
red_dot_centers[79-1][3] = 5 

red_dot_centers[78-1][2] = 1  
red_dot_centers[78-1][3] = 2 

red_dot_centers[68-1][2] = 1  
red_dot_centers[68-1][3] = 13 

red_dot_centers[67-1][2] = 1  
red_dot_centers[67-1][3] = 12 

red_dot_centers[66-1][2] = 1  
red_dot_centers[66-1][3] = 9 

red_dot_centers[65-1][2] = 1  
red_dot_centers[65-1][3] = 6 

red_dot_centers[64-1][2] = 1  
red_dot_centers[64-1][3] = 3 

red_dot_centers[54-1][2] = 1  
red_dot_centers[54-1][3] = 15 

red_dot_centers[53-1][2] = 1  
red_dot_centers[53-1][3] = 14 

red_dot_centers[52-1][2] = 1  
red_dot_centers[52-1][3] = 10 

red_dot_centers[41-1][2] = 1  
red_dot_centers[41-1][3] = 16 


red_dot_centers[115-1][2] = 5 
red_dot_centers[115-1][3] = 8 

red_dot_centers[127-1][2] = 5 
red_dot_centers[127-1][3] = 5 

red_dot_centers[140-1][2] = 5 
red_dot_centers[140-1][3] = 3 

red_dot_centers[153-1][2] = 5 
red_dot_centers[153-1][3] = 2 

red_dot_centers[165-1][2] = 5 
red_dot_centers[165-1][3] = 1 

red_dot_centers[114-1][2] = 5 
red_dot_centers[114-1][3] = 13 

red_dot_centers[126-1][2] = 5 
red_dot_centers[126-1][3] = 9 

red_dot_centers[139-1][2] = 5 
red_dot_centers[139-1][3] = 6 

red_dot_centers[152-1][2] = 5 
red_dot_centers[152-1][3] = 4 

red_dot_centers[113-1][2] = 5 
red_dot_centers[113-1][3] = 11 

red_dot_centers[125-1][2] = 5 
red_dot_centers[125-1][3] = 10 

red_dot_centers[138-1][2] = 5 
red_dot_centers[138-1][3] = 7 

red_dot_centers[112-1][2] = 5 
red_dot_centers[112-1][3] = 12 


red_dot_centers[38-1][2] = 15 
red_dot_centers[38-1][3] = 3 

red_dot_centers[106-1][2] = 15  
red_dot_centers[106-1][3] = 1 

red_dot_centers[107-1][2] = 15  
red_dot_centers[107-1][3] = 4 

red_dot_centers[108-1][2] = 15  
red_dot_centers[108-1][3] = 6 

red_dot_centers[118-1][2] = 15  
red_dot_centers[118-1][3] = 2 

red_dot_centers[119-1][2] = 15  
red_dot_centers[119-1][3] = 5 

red_dot_centers[120-1][2] = 15  
red_dot_centers[120-1][3] = 7 

red_dot_centers[121-1][2] = 15  
red_dot_centers[121-1][3] = 9 

red_dot_centers[122-1][2] = 15  
red_dot_centers[122-1][3] = 10 

red_dot_centers[132-1][2] = 15  
red_dot_centers[132-1][3] = 8 

red_dot_centers[133-1][2] = 15  
red_dot_centers[133-1][3] = 11 

red_dot_centers[134-1][2] = 15  
red_dot_centers[134-1][3] = 12 

red_dot_centers[135-1][2] = 15  
red_dot_centers[135-1][3] = 13 

red_dot_centers[141-1][2] = 15  
red_dot_centers[141-1][3] = 15

red_dot_centers[147-1][2] = 15  
red_dot_centers[147-1][3] = 14 

red_dot_centers[148-1][2] = 15  
red_dot_centers[148-1][3] = 16 


red_dot_centers[154-1][2] = 18  
red_dot_centers[154-1][3] = 13 

red_dot_centers[155-1][2] = 18  
red_dot_centers[155-1][3] = 12 

red_dot_centers[168-1][2] = 18  
red_dot_centers[168-1][3] = 11 

red_dot_centers[169-1][2] = 18  
red_dot_centers[169-1][3] = 8 

red_dot_centers[180-1][2] = 18  
red_dot_centers[180-1][3] = 10 

red_dot_centers[181-1][2] = 18  
red_dot_centers[181-1][3] = 9 

red_dot_centers[182-1][2] = 18  
red_dot_centers[182-1][3] = 7 

red_dot_centers[183-1][2] = 18  
red_dot_centers[183-1][3] = 6 

red_dot_centers[184-1][2] = 18  
red_dot_centers[184-1][3] = 1 

red_dot_centers[196-1][2] = 18  
red_dot_centers[196-1][3] = 2 

red_dot_centers[195-1][2] = 18  
red_dot_centers[195-1][3] = 4 

red_dot_centers[207-1][2] = 18  
red_dot_centers[207-1][3] = 5 

red_dot_centers[208-1][2] = 18  
red_dot_centers[208-1][3] = 3 

json_file = 'reddot.json' 

with open(json_file, "w") as f:
    json.dump(red_dot_centers, f, indent=2)

#for i, reddot in enumerate(red_dot_centers):
#    print(f"Red Dot {i}: x={reddot[0]}, y={reddot[1]}, d_id={reddot[2]}, id={reddot[3]}")

numbers = [1, 5, 15, 18]
# 初始化一个 4x16 的二维列表
rows = 4
cols = 17
tables = [[None for _ in range(cols)] for _ in range(rows)]

for i, reddot in enumerate(red_dot_centers):
    #if i == 121 :print(f"到底是怎么了？Red Dot {i}: x={reddot[0]}, y={reddot[1]}, d_id={reddot[2]}, id={reddot[3]}")
    
    if reddot[2] == 0 and reddot[3] == 0 :
        continue
    print(f"Red Dot {i}: x={reddot[0]}, y={reddot[1]}, d_id={reddot[2]}, id={reddot[3]}")

    if reddot[2] == 1 : tables[0][reddot[3]] = [reddot[0],reddot[1]]
    if reddot[2] == 5 : tables[1][reddot[3]] = [reddot[0],reddot[1]]
    if reddot[2] == 15 : tables[2][reddot[3]] = [reddot[0],reddot[1]]
    if reddot[2] == 18 : tables[3][reddot[3]] = [reddot[0],reddot[1]]
    
# 打印 tables
for i in range(rows):
    for j in range(cols):
        if tables[i][j] is not None:
            print(f"tables[{i}][{j}] = {tables[i][j]}")
        else: print(f"tables[{i}][{j}] = null")

json_file = 'table_reddot.json' 

with open(json_file, "w") as f:
    json.dump(tables, f, indent=2)