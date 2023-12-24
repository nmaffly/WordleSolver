from score import scored_words

#alphabet as a global variable
all_letters = [chr(ord('a') + i) for i in range(26)] 

def filter_words(guess, color_code, word_dict): 
    guess = guess.lower()
    color_code = color_code.lower()
    
    g_pos = []
    y_pos = []
    x_pos = []
    for pos, letter in enumerate(color_code):
        if letter == 'x':
            x_pos.append(pos)
        elif letter == 'y':
            y_pos.append(pos)
        elif letter == 'g':
            g_pos.append(pos)

    words_to_remove = []  # Create a list to store words to be removed

    for word, _ in word_dict.items():
        continue_flag = True
        temp = list(word)

        for pos in g_pos:
            if temp[pos] != guess[pos]:
                words_to_remove.append(word)
                continue_flag = False
                break
            else:
                temp[pos] = '_'
        if continue_flag:
            for pos in y_pos:
                if (temp.count(guess[pos]) < 1) or (temp[pos] == guess[pos]):
                    words_to_remove.append(word)
                    continue_flag = False
                    break
                else:
                    for i, val in enumerate(temp):
                        if val == guess[pos]:
                            temp[i] = '_'
                            break
        if continue_flag:
            for pos in x_pos:
                if guess[pos] in temp:
                    words_to_remove.append(word)
                    break

    # Remove the words outside the loop
    for word in words_to_remove:
        del word_dict[word]

#generates a list of elimination words based on unused letters
def generate_elim_guesses1(used_letters, correct_letters):
    copy_dict = scored_words.copy()
    filtered_dict = {}
    letters = used_letters[:]
    add_index = 0
    if correct_letters:
        max_iterations = len(correct_letters)
    else:
        max_iterations = 1
            

    while not filtered_dict and add_index < max_iterations:
        for word, value in copy_dict.items():
            add = True
            for letter in letters:
                if letter in word:
                    add = False
                    break
        
            if add:
                filtered_dict[word] = value
        if correct_letters:
            letters.remove(correct_letters[add_index])
        add_index += 1

    return filtered_dict

#generates a list of words based on unused letters
def generate_elim_guesses2(unused_letters, word_dict):
    copy_dict = scored_words.copy()
    filtered_dict = {}
    letters = unused_letters[:]

    if(len(word_dict) < 15):
        letters = remove_letters(letters, list(word_dict.keys()))
    
    while not filtered_dict and len(letters) > 1:
        for word, value in copy_dict.items():
            if word == 'ponty':
                print()
            add = True
            for letter in word:
                if letter not in letters:
                    add = False
                    break
        
            if add:
                filtered_dict[word] = value
    
        letters.pop()

    return filtered_dict

#removes any letters from list 'letters' that aren't in any of the words in list 'words'
def remove_letters(letters, words):
    new_letters = []

    for letter in letters:
        remove_letter = True
        for word in words:
            if letter in word:
                new_letters.append(letter)
                break
    
    return new_letters
   
    
#driver code for solving
def solve():
    word_dict = scored_words.copy()
    elim_dict = {}
    color_code = 'xxxxx'
    guess = ''
    
    unused_letters = all_letters[:]
    used_letters = []
    correct_letters = []

    print("Hi, I'm your virtual wordle assistant!")
    print("Here are some my recommended words to use: ")
    print(list(word_dict.keys())[:10])
    print(f"Possible words left: {len(word_dict)}\n")

    guess = input("Enter your guess: ")
    for char in guess:
            if char not in used_letters:
                used_letters.append(char)
        
    color_code = input("What was the corresponding color code (e.g. xxgyx): ")
    #add correct letters to list
    for i, char in enumerate(color_code):
        if char != 'x' and guess[i] not in correct_letters:
            correct_letters.append(guess[i])
        elif char == 'x' and guess[i] in unused_letters:
            unused_letters.remove(guess[i])
    
    filter_words(guess, color_code, word_dict)

    while(color_code != 'ggggg'):
        print(f"Possible words left: {len(word_dict)}")  
        print(f"Used letters: {[letter for letter in all_letters if letter not in used_letters]}")
        
        print("Here are some my elimination words to use: ")
        elim_dict = generate_elim_guesses1(used_letters, correct_letters)
        #elim_dict = generate_elim_guesses2(unused_letters, word_dict)
        if elim_dict:
            print(list(elim_dict.keys())[:10])
            print("Here are some possible answers: ")
            print(list(word_dict.keys())[:10])
        else:
            print("There are no possible elimantion words left. Here are possible answers:")
            print(list(word_dict.keys())[:10])

        guess = input("Enter your guess: ")
        #add each letter from your guess to list of used letters
        for char in guess:
            if char not in used_letters:
                used_letters.append(char)

        color_code = input("What was the corresponding color code (e.g. xxgyx): ")
        #add correct letters to list
        for i, char in enumerate(color_code):
            if char != 'x' and guess[i] not in correct_letters:
                correct_letters.append(guess[i])
        
        filter_words(guess, color_code, word_dict)
    
    print("Congrats on solving the wordle!")


def main():
    solve()

if __name__ == "__main__":
    main()
