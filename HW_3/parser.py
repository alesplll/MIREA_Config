import toml
import sys
import re


def parse_toml(file_path):
    try:
        with open(file_path, 'r') as file:
            return toml.load(file)
    except Exception as e:
        print(f"Error reading TOML file: {e}")
        sys.exit(1)


def convert_to_config(toml_data):
    config = ""
    for key, value in toml_data.items():
        config += convert_item(key, value)
    return config


def convert_item(key, value):
    if isinstance(value, dict):
        result = f"[{key} => \n"
        for k, v in value.items():
            result += f"{k} => {v},\n"
        return result + "]\n"
    elif isinstance(value, list):
        return f"array({', '.join(map(str, value))})\n"
    elif isinstance(value, (int, float)):
        return f"{key} = {value}\n"
    elif isinstance(value, str):
        return f'{key} = "{value}"\n'
    else:
        raise ValueError(f"Unsupported type for {key}: {type(value)}")


def validate_syntax(config_text):
    # Пример базовой проверки синтаксиса
    if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*", config_text):
        print("Syntax error detected")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python parser.py <path_to_toml_file>")
        sys.exit(1)

    toml_file = sys.argv[1]
    toml_data = parse_toml(toml_file)
    config_text = convert_to_config(toml_data)
    validate_syntax(config_text)
    print(config_text)


if __name__ == "__main__":
    main()
