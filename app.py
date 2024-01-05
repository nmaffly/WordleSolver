from flask import Flask, render_template, request, redirect, session, flash
from utils.solve import filter_words, words_with_unused_letters, generate_elim_guesses2, scored_words, count_common_words
from utils.score import all_words

app = Flask(__name__)
app.secret_key = 'xib2089fvbh28dv'

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'algo_guess' not in session:
        session['algo_guess'] = 'soare'
    if 'guess_record' not in session:
        session['guess_record'] = []
    if 'color_record' not in session:
        session['color_record'] = []
    if 'used_letters' not in session:
        session['used_letters'] = []
    if 'correct_letters' not in session:
        session['correct_letters'] = []
    if 'unused_letter_words' not in session:
        session['unused_letter_words'] = list(scored_words)[:10]
    if 'elim_words' not in session:
        session['elim_words'] = []
    if 'guess_count' not in session:
        session['guess_count'] = 0

    previous_guesses = list(zip(session['guess_record'], session['color_record']))

    unused_words = {}

    # Reconstruct word_dict from scratch on every request
    word_dict = scored_words.copy()
    for guess, color_code in zip(session['guess_record'], session['color_record']):
        word_dict = filter_words(guess, color_code, word_dict)

    possible_answers = list(word_dict.keys())[:10]

    if request.method == 'POST':
        try:
            input_letters = [request.form.get(f'letter{i}', '') for i in range(1, 6)]
            current_guess = ''.join(input_letters)
            if(current_guess not in all_words):
                flash("Please input a valid word")
                return redirect('/')
            elif len(current_guess) < 5:
                flash("Please input a five letter word")
                return redirect('/')
        except:
            return 'There was an error getting your word'
        
        try:
            input_colors = [request.form.get(f'color{i}', '') for i in range(1,6)]
            color_code = ''.join(input_colors)
            print(list(color_code))
            if set(color_code) - {'x', 'g', 'y'}:
                flash("Please input a valid color code")
                return redirect('/')
            elif len(color_code) < 5:
                flash("Please enter a valid color code")
                return redirect('/')
        except:
            return 'There was an error getting your color code'
        
        previous_guesses = list(zip(session['guess_record'], session['color_record']))

        for char in current_guess:
            if char not in session['used_letters']:
                session['used_letters'].append(char)
        
        for i, char in enumerate(color_code):
            if char != 'x' and current_guess[i] not in session['correct_letters']:
                session['correct_letters'].append(current_guess[i])

        word_dict = filter_words(current_guess, color_code, word_dict)
        if len(word_dict) != 0:
            # Append the new guess and color code
            session['guess_record'].append(current_guess)
            session['color_record'].append(color_code)
            session['guess_count'] += 1
            session.modified = True
        else:
            flash("No more possible answers. Make sure your color code was entered correctly")
            return redirect('/')

        # Apply the filter with the latest guess and color code
        unused_words = words_with_unused_letters(session['used_letters'])
        session["unused_letter_words"] = list(unused_words.keys())[:10]

        if session['guess_count'] < 2:
            if len(word_dict) < 15:
                session['algo_guess'] = list(word_dict)[0]
            elif len(word_dict) < 45:
                common_words_left = count_common_words(list(word_dict))
                session['elim_words'] = generate_elim_guesses2(common_words_left, color_code, session['correct_letters'])[:10]
                session['algo_guess'] = session['elim_words'][0]
            else:
                session['algo_guess'] = list(unused_words)[0]
        elif color_code.count('g') >= 3 and session['guess_count'] < 5:
            common_words_left = count_common_words(list(word_dict))
            if len(common_words_left) > 3:
                session['elim_words'] = (generate_elim_guesses2(word_dict, color_code, session['correct_letters']))[:10]
                session['algo_guess'] = session['elim_words'][0]
            else:
                session['algo_guess'] = list(word_dict)[0]
        else:
            if word_dict:
                session['algo_guess'] = list(word_dict)[0]
            

        return redirect('/')

    else:
        return render_template('index.html', guess_count=session['guess_count'], possible_answers=possible_answers, unused_letter_words=session['unused_letter_words'] ,elim_words=session['elim_words'], guess_record=session['guess_record'], color_record=session["color_record"], previous_guesses=previous_guesses, remaining_words=len(word_dict), algo_guess=session['algo_guess'])


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
