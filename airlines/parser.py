import os


prefix = '                                                <p class="mb-0 text-small">'
files = os.listdir('data')
content = {}
for file in files:
    path = os.path.join("data", file)
    with open(path, "r") as f:
        content[path] = f.read()
for p, c in content.items():
    lines = c.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            assert i > 0
            prev = lines[i - 1]

            full = prev[len(prefix)+1:].split("<")[0]
            shorts = reversed(line[len(prefix):].split("<")[0].split()[0::2])
            print(f"{' '.join(shorts)}  ---  {full}")

