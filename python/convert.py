with open("python/part1.txt", "r") as file:
    content = file.read()

spaced_content = " ".join(content)

with open("python/gengar_spaced.txt", "w") as file:
    file.write(spaced_content)

print("Spacing added successfully! You can download the modified file.")