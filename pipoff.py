from libs.jckwheellib import WheelPackageInfo
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="pipoff",
    description="Create and manage your whl packages into single ALL dependencies contained (jck) package.",
    epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument("path", "-i", "--info")

args = parser.parse_args()

target_dir = Path(args.path)

if not target_dir.exists():
    print("The target directory doesn't exist")
    raise SystemExit(1)

for entry in target_dir.iterdir():
    print(entry.name)

p = WheelPackageInfo("pylint-2.6.0-py3-none-any.whl")

print(p.get_requires_dist())
print(p.has_dependencies())
print(p.is_installed())
print(p.get_version())
