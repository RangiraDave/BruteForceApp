import nltk
import string  # Add this import to handle string operations
from nltk.corpus import words
from django.shortcuts import render


# Download the words corpus from nltk (This needs to be done once)
nltk.download('words')

# Define the caesar_bruteforce function here
def caesar_bruteforce(encrypted_message):
    try:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        word_list = set(words.words())  # Use set for faster lookups
        encrypted_message = encrypted_message.upper()
        all_results = []  # To store all decrypted shifts

        # print(f"Brute-forcing message: {encrypted_message}")  # Debugging

        # Try every possible key (shift from 0 to 25)
        for shift in range(26):
            decrypted_message = ''
            for char in encrypted_message:
                if char in alphabet:
                    index = alphabet.index(char)
                    new_index = (index - shift) % 26
                    decrypted_message += alphabet[new_index]
                else:
                    decrypted_message += char

            # Add each result to the list
            all_results.append((shift, decrypted_message))
            print(f"Shift {shift}: {decrypted_message}")  # Debugging: Check each decryption

            # Clean the decrypted message: remove punctuation and convert to lowercase
            cleaned_message = decrypted_message.translate(str.maketrans('', '', string.punctuation)).lower()
            words_in_message = cleaned_message.split()
            print(f"Cleaned words: {words_in_message}")  # Debugging

            # Check if all words are in the word list
            if all(word in word_list for word in words_in_message):
                print(f"Found a meaningful word at shift {shift}: {decrypted_message}")  # Debugging
                return 'meaningful', shift, decrypted_message

        # If no meaningful word is found, return all 25 results
        return 'all', all_results

    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        return 'error', []

def home(request):
    """
    View function for the home page.
    """

    decrypted_message = None
    shift_used = None
    all_decrypted = None  # Correct the variable name typo from 'all_decripted'
    original_message = None

    if request.method == 'POST':
        try:
            message = request.POST.get('message', '')  # Ensure message is fetched, use '' if empty
            technique = request.POST.get('technique', '')

            if message and technique == 'caesar':
                original_message = message  # Store the original message for display later

                # Call the brute force function for Caesar Cipher
                result_type, *result = caesar_bruteforce(message)
                # print(f"Bruteforce result: {result_type}, {result}")

                if result_type == 'meaningful':
                    # If a meaningful word is found, display only that result
                    shift_used, decrypted_message = result
                elif result_type == 'all':
                    # If no meaningful word is found, display all results
                    all_decrypted = result[0]  # Get the list of all decrypted messages

        except Exception as e:
            print(f"An error occurred in the view: {e}")

    return render(
        request,
        'crypto/home.html',
        {
            'original_message': original_message,
            'decrypted_message': decrypted_message,
            'shift_used': shift_used,
            'all_decrypted': all_decrypted
        })
