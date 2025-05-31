# Arsène DoS Attack Tool

<p>
    <img src="https://files.catbox.moe/lp2t10.jpg" />
</p>


Arsène DoS Attack Tool is a powerful and stylish command-line DoS attack tool themed after Arsène from Persona. This tool allows you to perform various types of DoS attacks with ease, complete with a dramatic countdown timer and stylish output.

## Features

- **Multiple Attack Methods**: Choose from different attack methods including CFB, HTTP/2, and SOC attacks.
- **Dramatic Countdown**: A countdown timer adds flair and anticipation before the attack begins.
- **Command-Line Interface**: Easy to use with command-line arguments for method, target, threads, and duration.
- **Stylish Output**: Colorful and informative output makes the tool visually appealing and easy to understand.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/arsene-dos.git
   ```

2. Navigate to the project directory:
   ```sh
   cd arsene-dos
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line with the following arguments:

- `method`: The type of attack method (cfb, http2, soc).
- `target`: The target URL or IP address.
- `threads`: The number of threads to use for the attack.
- `time`: The duration of the attack in seconds.

Example:
```sh
python arsene_dos.py http2 https://example.com 100 60
```

## Attack Methods

### CFB Attack
Bypasses Cloudflare protection and performs a bypass CF attack.

### HTTP/2 Attack
Exploits HTTP/2 protocol to overwhelm the target server.

### SOC Attack
Performs a socket-based attack to flood the target with requests.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the creators of Persona for inspiring this tool.
- Thanks to the open-source community for providing the libraries and tools used in this project.

## Contact

For any questions or suggestions, please open an issue or contact me directly.

---
