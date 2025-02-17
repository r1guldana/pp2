import json

with open("C:\pp2\lab4\sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("="*77)
print("DN", " "*48, "Description", " "*8, "speed", " "*2 , "MTU", " "*3)
print("-------------------------------------------------- --------------------  ------  ------")

for imdata in data["imdata"]:
    for i in imdata:
        for j in imdata[i]:
            print(imdata[i][j]["dn"], " "*28, imdata[i][j]["speed"], " "*2, imdata[i][j]["mtu"])