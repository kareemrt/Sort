import filecmp
from pathlib import Path

folder1 = Path(input("Enter the path for folder1: "))
folder2 = Path(input("Enter the path for folder2: "))

comparison = filecmp.dircmp(folder1, folder2)

print("Only in folder1:", comparison.left_only)
print()
print("Only in folder2:", comparison.right_only)
print()
print("Different files:", comparison.diff_files)
print()
print("Identical files:", comparison.same_files)
