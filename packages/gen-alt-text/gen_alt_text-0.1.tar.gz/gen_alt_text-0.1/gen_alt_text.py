#!/usr/bin/env python3

"""gen-alt-text

Usage:
    gen-alt-text [-m MODEL] <path_to_image>
    gen-alt-text -h

Options:
    -h          show this help message and exit
    -m MODEL    Use MODEL as the model. If MODEL is not provided, it defaults
                to llama3.2-vision:11b.

Examples:
    gen-alt-text -m llama3.2-vision:90b ~/pictures/rubber_duck.jpg
    gen-alt-text ~/pictures/coffee.jpg
"""

import os

from docopt import docopt
from ollama import Client, ResponseError
from rich.console import Console
from rich.markdown import Markdown


def main():
    args = docopt(__doc__)
    if args["-m"]:
        model = args["-m"]
    else:
        model = "llama3.2-vision:11b"

    if os.getenv("OLLAMA_HOST"):
        client = Client(host=os.getenv("OLLAMA_HOST"))
    else:
        client = Client(host="http://localhost:11434")

    print()
    console = Console()
    try:
        with console.status(
            f"[bold magenta] {model}[/bold magenta] is generating alt-text for "
            + args["<path_to_image>"]
            + "...",
            spinner="aesthetic",
        ):
            response = client.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": "Describe this image concisely",
                        "images": [args["<path_to_image>"]],
                    }
                ],
                stream=False,
            )
    except ResponseError as e:
        if e.status_code == 404:
            with console.status(
                f"[bold magenta] {model}[/bold magenta] was not found on the ollama server. Pulling it now...",
                spinner="aesthetic",
            ):
                client.pull(model=model)
            console.print(
                f"Successfully pulled [bold magenta]{model}[/bold magenta]. You may try running the command again."
            )
            exit(0)
        else:
            print("Error: ", e.error)
            exit(1)

    md_content = Markdown(response["message"]["content"])
    console.print(md_content)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit("Keyboard interrupt detected. Exiting.")
