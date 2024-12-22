#----------------------------------------- 1st

# chef1 = []
# chef2 = []
# chef1score = 0
# chef2score = 0
# print("=============================================")
# print("Enter Rating for two chef's ")
# print("1 is for Presentation")
# print("2 is for taste")
# print("3 is for hygiene")
# print("=============================================\n\n")
    
# for i in range(3):
#     chef1.append(int(input(f"Enter Chef 1's rating for {i+1}:")))
# print("\n=============================================\n\n")
# for i in range(3):
#     chef2.append(int(input(f"Enter Chef 2's rating for {i+1}:")))
# print("\n=============================================\n\n")
    
# for i in range(3):
#     if chef1[i] > chef2[i]:
#         chef1score += 1
#     elif chef1[i] < chef2[i]:
#         chef2score += 1

# print(f"Chef 1's score is {chef1score}")
# print(f"Chef 1's score is {chef2score}")


# ------------------------------------------ 2nd
array = list(map(int,input().split()))
min = abs(array[0]+array[1])
for i in range(0,len(array)):
    for j in range(i+1,len(array)):
        temp = array[i] + array[j]
        if abs(temp) < min:
            min = abs(temp)
for i in range(0,len(array)):
    for j in range(i+1,len(array)):
        temp = array[i] + array[j]
        if abs(temp) == min:
            print(array[i],array[j])