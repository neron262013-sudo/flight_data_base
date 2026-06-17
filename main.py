from src.api_adapter import APIAdapter


def main():
    adapter = APIAdapter()

    data = adapter.get_aeroplanes("Germany")

    print(f"Количество самолетов: {len(data.get('states', []))}")

    if data.get("states"):
        print(data["states"][0])

    print(data.keys())

    data = adapter.get_aeroplanes("France")
    print(len(data.get("states", [])))


if __name__ == "__main__":
    main()