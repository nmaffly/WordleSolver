from score import common_words, all_words, calc_score, answers
from solve import filter_words, generate_elim_guesses1


def evaluate_algorithm(positional_weight, overall_weight, elim_threshold):
    scored_words = {}
    for word in all_words:
        scored_words[word] = calc_score(word, positional_weight, overall_weight)

    scored_words = dict(sorted(scored_words.items(), key=lambda item: item[1], reverse=True))

    total_guesses = 0
    unsolved = {}
    for i, word in enumerate(answers):
        #print(f"{round(100 * i/len(common_words))}%: {word}")
        num_guesses = run_wordle(word, scored_words, elim_threshold)
        if num_guesses > 6:
            unsolved[word] = num_guesses
        else:
            total_guesses += num_guesses

    avg_num_guesses = total_guesses / len(answers)

    #print_stats(avg_num_guesses, positional_weight, overall_weight, unsolved, elim_threshold)

    return avg_num_guesses, unsolved

def print_stats(avg_guesses, positional_weight, overall_weight, unsolved_words, elim_threshold):
    print()
    print("Algorithm: ")
    print(f"Weight of positional letter frequencies: {positional_weight}")
    print(f"Weight of overall letter frequencies: {overall_weight}")
    print(f"Elimination guess threshold: {elim_threshold}")
    print()
    print(f"It took the algorithm an average of {round(avg_guesses, 4)} guesses to solve a given wordle, excluding unsolved wordles")
    print(f"There were {len(unsolved_words)} out of {len(answers)} unsolved wordles (over 6 guesses)")
    percent_unsolved = round((100 * len(unsolved_words) / len(answers)), 2)
    print()
    print(f"Your algorithm was able to solve {100 - percent_unsolved}% of wordles")
    print(f"Your algorithm was unable to solve {percent_unsolved}% of wordles")

def run_wordle(answer, scored_words, elim_threshold):
    num_guesses = 0
    color_code = 'xxxxx'
    word_dict = scored_words.copy()
    used_letters = []
    correct_letters = []
    elim_dict = {}

    current_guess = list(word_dict)[0]

    while(color_code != 'ggggg'):
        for char in current_guess:
            if char not in used_letters:
                used_letters.append(char)

        color_code = compare_answer(current_guess, answer)
        for i, char in enumerate(color_code):
            if char != 'x' and current_guess[i] not in correct_letters:
                correct_letters.append(current_guess[i])

        num_guesses += 1

        word_dict = filter_words(current_guess, color_code, word_dict)

        if len(word_dict) > elim_threshold: 
            elim_dict = generate_elim_guesses1(used_letters, correct_letters)
            current_guess = list(elim_dict)[0]
        else:
            current_guess = list(word_dict)[0]
        
    
    return num_guesses

def compare_answer(guess, answer):
    color_code = [None] * 5
    temp_answer = list(answer)
    already_assigned = []
    for i, char in enumerate(guess):
        if char == temp_answer[i]:
            color_code[i] = 'g'
            temp_answer[i] = '_'
            already_assigned.append(i)
    for i, char in enumerate(guess):
        if char in temp_answer and char != temp_answer[i] and i not in already_assigned:
            color_code[i] = 'y'
            temp_answer[temp_answer.index(char)] = '_'
    for i, char in enumerate(guess):
        if color_code[i] == None:
            color_code[i] = 'x'

    return ''.join(color_code)

def main():
    '''
    #Test cases for compare_answer()
    print(compare_answer('soare', 'bagel'))
    print(compare_answer('linty', 'bagel'))
    print(compare_answer('paled', 'bagel'))
    print(compare_answer('elect', 'elect'))
    '''
    positional_weight = 0.2
    overall_weight = 2
    
    elim_threshold_evaluation = {}

    
    print("Elimination threshold: avg number of guesses to solve")
    for elim_threshold in range(325, 376):
        avg_guesses, _ = evaluate_algorithm(positional_weight, overall_weight, elim_threshold)
        elim_threshold_evaluation[elim_threshold] = avg_guesses
        print(f"{elim_threshold}: {avg_guesses}")
    
    most_efficient = min(elim_threshold_evaluation, key=lambda k: elim_threshold_evaluation[k])
    print()
    print(f"The most efficient elimination threshold was {most_efficient} with an average number of guesses of {elim_threshold_evaluation[most_efficient]}")
    
    

    #for word, guesses in unsolved_words.items():
        #print(f"{word}: {guesses}")
    

if __name__ == "__main__":
    main()