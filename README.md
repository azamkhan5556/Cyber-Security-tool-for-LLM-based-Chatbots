# Jailbreak Attacks Detection tool for LLM based Applications

Jailbreak Detector is a Python based tool designed to identify potentially dangerous or sensitive keywords in the input query to LLMs, including those obfuscated using ASCII art. This tool can be particularly useful for content moderation in chat applications, forums, or any text-based communication platform.

## Features

- Detects specified keywords in normal text
- Identifies keywords obfuscated in ASCII art
- Case-insensitive matching (configurable)
- Logging of detected keywords and original messages
- Flexible and extendable for custom use cases

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/jailbreak-detector.git
   cd jailbreak-detector
   ```

2. Install the required dependencies:
   ```
   pip install unidecode
   ```

## Usage

1. Import the `KeywordDetector` class and create an instance with your list of keywords:

   ```python
   from jailbreak_detector import KeywordDetector

   dangerous_words = ["explosive", "weapon", "bomb", "attack"]
   detector = KeywordDetector(dangerous_words)
   ```

2. Use the `detect` method to check for keywords in a message:

   ```python
   message = "This is a test message with ASCII art: #### #### ### # # #"
   detected_words = detector.detect(message)

   if detected_words:
       print(f"Detected keywords: {', '.join(detected_words)}")
   else:
       print("No keywords detected.")
   ```

3. You can also use the `check_message` function for a more detailed output:

   ```python
   from jailbreak_detector import check_message

   is_safe = check_message(detector, message, review_context=True)
   print(f"Message is safe: {is_safe}")
   ```

## Customization

You can customize the `KeywordDetector` class to fit your specific needs:

- Modify the `detect_ascii_art` method to improve ASCII art detection
- Add new detection methods for other types of obfuscation
- Adjust the logging behavior in the `_setup_logger` method

## Contributing

Contributions to improve Jailbreak Detector are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for content moderation and safety purposes. Please use responsibly and in compliance with applicable laws and regulations.
