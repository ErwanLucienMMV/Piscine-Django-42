def demonstrate_path():
    from path import Path

    directory = Path("example")
    directory.makedirs_p()
    output = directory / "hello.txt"
    output.write_text("Hello from path.py!\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    try:
        demonstrate_path()
    except (ImportError, OSError) as error:
        print("Error:", error)
        raise SystemExit(1)
