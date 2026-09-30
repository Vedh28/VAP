from pathlib import Path

ROOT = Path(r"C:\Users\vedhp\VAD").resolve()
ROOT.mkdir(parents=True, exist_ok=True)


def safe_path(path: str) -> Path:
    """Resolve a path and prevent access outside the workspace."""
    target = (ROOT / path).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("Access outside the workspace is prohibited.")
    return target


def echo(message: str) -> str:
    """Return the user's text unchanged, without adding a prefix."""
    return message


def run_agent() -> None:
    """Echo each entered line until the user types exit."""
    while True:
        prompt = input("\nJARVIS: ")
        if prompt.strip().lower() == "exit":
            break
        if not prompt:
            continue
        print(echo(prompt))


if __name__ == "__main__":
    run_agent()
