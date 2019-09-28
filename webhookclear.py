print("Starting")
open("hooks.txt", "w").close()
print("Finished, checking")
file = open("hooks.txt", "r")
for i in file.readlines():
    print("".join(i.split()))
print("Exiting")
