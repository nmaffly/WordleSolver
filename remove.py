# Read file B and store its words in a set for faster lookups
with open('words/allowed_words.txt', 'r') as file:
    words_in_B = set(file.read().splitlines())

# Read file A
with open('words/common_five_letter_words.txt', 'r') as file:
    words_in_A = file.read().splitlines()

# Keep only the words in A that are also in B
words_in_A_filtered = [word for word in words_in_A if word in words_in_B]

# Write the filtered words back to file A
with open('words/common_five_letter_words1.txt', 'w') as file:
    for word in words_in_A_filtered:
        file.write(word + '\n')
