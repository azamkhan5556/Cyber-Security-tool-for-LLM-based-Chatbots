#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:15:32 2024

@author: asus
"""

import re
import logging
from unidecode import unidecode

class KeywordDetector:
    def __init__(self, keywords, case_sensitive=False):
        self.case_sensitive = case_sensitive
        self.keywords = set(keywords if case_sensitive else [k.lower() for k in keywords])
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger('KeywordDetector')
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('keyword_detector.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def ascii_to_text(self, text):
        ascii_pattern = r'&#(\d+);'
        return re.sub(ascii_pattern, lambda m: chr(int(m.group(1))), text)

    def normalize_text(self, text):
        text = self.ascii_to_text(text)
        return unidecode(text)

    def detect_ascii_art(self, ascii_art):
        # Convert ASCII art to a simplified pattern
        pattern = re.sub(r'[^#\s]', '.', ascii_art)
        pattern = re.sub(r'\s+', ' ', pattern)
        lines = pattern.split('\n')
        
        # Check for word-like patterns
        word_patterns = [
            r'#.+#.+#.+#.+#.+#',  # Pattern for "explosive"
            r'#.+#.+#.+#',        # Pattern for "bomb"
            r'#.+#.+#.+#.+#',     # Pattern for "weapon"
            r'#.+#.+#.+#.+#'      # Pattern for "attack"
        ]
        
        detected_words = []
        for line in lines:
            for i, pattern in enumerate(word_patterns):
                if re.search(pattern, line):
                    detected_words.append(list(self.keywords)[i])
        
        return detected_words

    def detect(self, text):
        original_text = text
        normalized_text = self.normalize_text(text)
        
        detected_words = []
        
        # Check for normal text
        for word in self.keywords:
            if re.search(r'\b' + re.escape(word) + r'\b', normalized_text, re.IGNORECASE if not self.case_sensitive else 0):
                detected_words.append(word)
        
        # Check for ASCII art
        if '#' in text:
            ascii_detected = self.detect_ascii_art(text)
            detected_words.extend(ascii_detected)

        if detected_words:
            self.logger.warning(f"Detected keywords: {', '.join(detected_words)}")
            self.logger.info(f"Original message: {original_text}")

        return detected_words

def check_message(detector, message, review_context=False):
    detected = detector.detect(message)
    if detected:
        print(f"Warning: Detected potentially concerning words: {', '.join(detected)}")
        if review_context:
            print("Please review the full context of this message:")
            print(f"Message: {message}")
        return False
    return True

# Example usage with ASCII art
dangerous_words = ["explosive", "weapon", "bomb", "attack"]
detector = KeywordDetector(dangerous_words)

ascii_art_messages = [
    "Normal message with no keywords.",
    "###### # #     ##### #     #### ####     # #     #     ###### # #     # #     # #     # #     # #     ##### ## #     # #     # #### #     # #     ##### # ## ##### #     # #     # #     # #     # #     # #     # #     # #     # #     ###### # #     # ###### #### ####     # ## ######",
    "Mixed content: Normal text and ASCII art:\n#### #### ### # # # ### # # # # # # # # ###",
    "This message has no dangerous words in ASCII art:\n### # # ### # # # # # ###",
    """
    ###### # #     ##### #     #### ####     # #     #     ###### # #     # #     # #     # #     # #     ##### ## #     # #     # #### #     # #     ##### # ## ##### #     # #     # #     # #     # #     # #     # #     # #     # #     ###### # #     # ###### #### ####     # ## ######
    """
]

print("Testing with ASCII art messages:")
for msg in ascii_art_messages:
    print(f"\nChecking message: {msg}")
    is_safe = check_message(detector, msg, review_context=True)
    print(f"Message is safe: {is_safe}")
