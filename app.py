from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

responses = []
app.config['SECRET_KEY'] = "SurveysRCool"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

@app.route('/')
def home_page():
    """renders template that includes details of the survey and start button"""
    return render_template('start_survey.html', survey=survey)

@app.route('/begin-survey', methods=['POST'])
def begin_survey():
    """User is redirected to first question of the survey"""
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question_and_answer():
    """Choices append to the length to redirect user onto the next question.
    IF the responses meets the length of the survey, then user is redirected to the completion page.
    """
    choice = request.form['answer']
    responses.append(choice)
    if (len(responses) == len(survey.questions)):
        return redirect('/survey-complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:id>')
def survey_questions(id):
    """ If loops """
    if (responses == None):
        """ If there are no responses, then user is redirected to the main page"""
        return redirect('/')
    elif (len(responses) == len(survey.questions)):
        """If responses meet the length of questions, then user is redirected to completion page"""
        return redirect('/survey-complete')
    elif(len(responses) != id):
        """If response length does not meet the id number of questions then a flash msg will pop up invalidating that url request"""
        flash(f'Invalid Accces to Question {id}')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[id]
    return render_template('questions.html', question_num =id, question=question)

# @app.route('/answer', methods=['POST'])
# def handle_given_questions():


@app.route('/survey-complete')
def completed_survey():
    "Completion of the survey renders the 'Thank you' template."
    return render_template('survey_completion.html')