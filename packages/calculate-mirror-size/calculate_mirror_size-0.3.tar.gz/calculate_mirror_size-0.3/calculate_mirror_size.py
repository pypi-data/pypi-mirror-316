#!/usr/bin/env python3

"""calculate-mirror-size

Usage:
    calculate-mirror-size -H <http_url> -R <rsync_url>
    calculate-mirror-size -h

Examples:
    calculate-mirror-size -H "https://mirrors.servercentral.com/voidlinux/" -R "rsync://repo-sync.voidlinux.org/voidlinux/"

Options:
    -H <http_url>   HTTP URL of the mirror
    -R <rsync_url>  rsync URL of the mirror
    -h, --help      show this help message and exit
"""

import subprocess
from tempfile import TemporaryDirectory

import requests
from bs4 import BeautifulSoup
from docopt import docopt
from rich.console import Console
from rich.text import Text


def human_bytes(bites: int) -> str:
    B = float(bites)
    KiB = float(1024)
    MiB = float(KiB**2)
    GiB = float(KiB**3)
    TiB = float(KiB**4)

    match B:
        case B if B < KiB:
            return "{0} {1}".format(B, "bytes" if 0 == B > 1 else "byte")
        case B if KiB <= B < MiB:
            return "{0:.2f} KiB".format(B / KiB)
        case B if MiB <= B < GiB:
            return "{0:.2f} MiB".format(B / MiB)
        case B if GiB <= B < TiB:
            return "{0:.2f} GiB".format(B / GiB)
        case B if TiB <= B:
            return "{0:.2f} TiB".format(B / TiB)
        case _:
            return ""


def main():
    args = docopt(__doc__)

    repo_shorthand = Text(args["-R"].split("//")[1])

    print()
    console = Console()

    with console.status(
        "[bold magenta]Calculating mirror size...[/bold magenta]", spinner="aesthetic"
    ):
        response = requests.get(args["-H"], timeout=60)
        soup = BeautifulSoup(response.text, "html.parser")
        mirror_dirs = []
        for node in soup.find_all("a"):
            if not node.get("href").startswith(".") and node.get("href").endswith("/"):
                mirror_dirs.append(node.get("href"))

        console.log(
            f"Summing up the sizes of each directory in [bold blue]{repo_shorthand}[/bold blue]."
        )
        with TemporaryDirectory():
            dir_sizes = []
            max_dir_len = len(max(mirror_dirs, key=len))
            for dir in mirror_dirs:
                rsync_cmd = f"rsync -a -n --stats {args['-R']}/{dir}/ | grep '^Total file size' | tr -d ','"
                output = subprocess.run(rsync_cmd, shell=True, capture_output=True)
                logstr = (
                    dir.rjust(max_dir_len)
                    + " "
                    + human_bytes(int(output.stdout.split()[3]))
                )
                console.log(logstr)
                dir_sizes.append(int(output.stdout.split()[3]))

    console.print(
        f"\n[bold blue]{repo_shorthand}[/bold blue]: " + human_bytes(sum(dir_sizes))
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit("Keyboard interrupt detected. Exiting.")
