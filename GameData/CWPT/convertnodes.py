import re
import sys

nodere = re.compile(r"RDNode\s*\{\s*id = (\w*).*?title = (.*?)\n.*?Unlocks\s*\{([^}]+)\s*\}", re.DOTALL)
partre = re.compile(r"part = (\w+)")
unlocks = re.compile(r"Unlocks\s*\{([^}]+)\s*\}\n")

tree = sys.argv[1].split(".")[0]

with open(sys.argv[1], "r") as inp:
	inpr = inp.read()

with open(tree + "_patches.cfg", "w") as patches:
	for i, n in enumerate(nodere.finditer(inpr)):
		print(f"Converted {i} nodes\r", end="")
		node, name, parts = n.groups()
		patches.write(f"// {name}\n")
		for p in partre.finditer(parts):
			part = p.group(1)
			patches.write(f"""\
@PART[{part}]
{{
  @TechRequired = {node}
}}\n""")
with open(tree + "_tree.cfg", "w") as tree:
	tree.write(unlocks.sub("", inpr))
	