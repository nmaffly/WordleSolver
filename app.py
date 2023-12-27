from flask import Flask, render_template, request, redirect, session
from solve import filter_words, generate_elim_guesses1, scored_words

app = Flask(__name__)
app.secret_key = 'xib2089fvbh28dv'

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'guess_record' not in session:
        session['guess_record'] = []
    if 'color_record' not in session:
        session['color_record'] = []
    if 'used_letters' not in session:
        session['used_letters'] = []
    if 'correct_letters' not in session:
        session['correct_letters'] = []
    if 'elim_words' not in session:
        session['elim_words'] = []
    if 'guess_count' not in session:
        session['guess_count'] = 0



    # Reconstruct word_dict from scratch on every request
    word_dict = scored_words.copy()
    for guess, color_code in zip(session['guess_record'], session['color_record']):
        word_dict = filter_words(guess, color_code, word_dict)

    possible_answers = [list(word_dict.keys())[:10]]

    if request.method == 'POST':
        current_guess = request.form['word']
        for char in current_guess:
            if char not in session['used_letters']:
                session['used_letters'].append(char)
        
        color_code = request.form['colors']
        for i, char in enumerate(color_code):
            if char != 'x' and current_guess[i] not in session['correct_letters']:
                session['correct_letters'].append(current_guess[i])

        # Append the new guess and color code
        session['guess_record'].append(current_guess)
        session['color_record'].append(color_code)
        session['guess_count'] += 1
        session.modified = True

        # Apply the filter with the latest guess and color code
        word_dict = filter_words(current_guess, color_code, word_dict)
        session["elim_words"] = list((generate_elim_guesses1(session['used_letters'], session['correct_letters'])).keys())[:10]

        return redirect('/')

    else:
        return render_template('index.html', guess_count=session['guess_count'], possible_answers=possible_answers, elim_words=session['elim_words'], guess_record=session['guess_record'], remaining_words=len(word_dict))


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
