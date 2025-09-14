"""
In this problem, there is a class named Quiz_item that models multiple choice questions. The class should have attributes 
for the question, choices, correct answer. Also, the class has methods for changing the question, 
each choice, and the correct answer. 
"""

class Quiz_item:
    def __init__(self, question, choice, correct_answer):
        """
        Purpose: Initialize a Quiz_item object 
        Inputs: question(str): The quiz question 
                choice(list[str]): List of choices
                correct_answer(str): The correct answer
                
        Output: ValueError: If inputs are invalid 
        """
        # Validate that question is a non-empty string
        if not isinstance (question, str) or not question.strip():
            raise ValueError("question must be a non-empty string")
        # Validate that choice is a list of non-empty strings
        if not isinstance(choice, list):
            raise ValueError("choice must be a list of strings")
        if len(choice) < 2:
            raise ValueError("There must be at least two choices")
        if not all(isinstance(c, str) and c.strip() for c in choice):
            raise ValueError("each choice must be a non-empty string")
        # Validate correct_answer
        if not isinstance(correct_answer, str) or not correct_answer.strip():
            raise ValueError("correct answer must be a non-empty string")
        if correct_answer not in choice:
            raise ValueError("Correct answer must be one of the choices")
        
        # Assign attributes
        self.question = question
        self.choices = choice 
        self.correct_answer = correct_answer
    
    def set_question(self, question):
        """
        Update the quiz question
        Inputs: question(str): New question text
        Output: ValueError: If question is invalid
        """
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must be a non-empty string")
        self.question = question 
    
    def set_choices(self, index, choice):
        """
        Update a specific choice at a given index
        Inputs: index(int): Index of the choice to update
                choice(str): New choice text
        Outputs: ValueError: If the choice is invalid
                 IndexError: If the index is out of range
        """
        if not isinstance(choice, str) or not choice.strip():
            raise ValueError("choice must be a non-empty string")
        if 0 <= index < len(self.choices):
            self.choices[index] = choice
        else:
            raise IndexError("Choice index is out of range")
    
    def set_correct_answer(self, correct_answer):
        """
        Update the correct answer
        Inputs: correct_answer (str): The new correct answer.
        Outputs: ValueError: If invalid 
        """
        if not isinstance(correct_answer, str) or not correct_answer.strip():
            raise ValueError("correct answer must be a non-empty string")
        if correct_answer not in self.choices:
            raise ValueError("Correct answer must be one of the choices")
        self.correct_answer = correct_answer
    
    def get_question(self):
        """
        Get the quiz question
        Returns: str: The question text 
        """
        return self.question
    
    def get_choice(self, index):
        """
        Get a specific choice by index.
        Inputs: index(int): The index of the choice 
        Returns: str: The choice 
        Raises: IndexError: if index is out of range
        """
        if 0 <= index < len(self.choices):
            return self.choices[index]
        else:
            raise IndexError("Choice index is out of range")
    
    def get_correct_answer(self):
        """
        Get the correct answer 
        Returns: str: Correct answer 
        """
        return self.correct_answer

"""
In this program there is a class named Quiz, that will use Quiz_item
to model a quiz. Then develop a terminal-based system that allows a user 
to add a new quiz item to the quiz, view all the quiz items in the quiz, 
modify individual quiz items, and take the quiz by seeing and answering 
quiz questions one by one.
"""

class Quiz:
    def __init__(self):
        """
        Initialize an empty quiz.
        Inputs:  None
        Outputs: None
        """
        self.questions = []

    def add_question(self, my_quiz):
        """
        Add a `Quiz_item` to the quiz.
        Purpose:
            Ensures only valid Quiz_item objects are added to the internal list.
        Inputs:
            my_quiz (Quiz_item): The question to add.
        Outputs:
            None
        Raises:
            TypeError: If `my_quiz` is not a Quiz_item instance.
        """
        if not isinstance (my_quiz, Quiz_item):
            raise TypeError("my_quiz must be a Quiz_item object")
        self.questions.append(my_quiz)
    
    def display_questions(self):
        """
        Print all questions with choices and correct answer
        Purpose:
            Provides a quick, non-interactive preview of the quiz content.
        Inputs:
            None
        Outputs:
            None 
        """
        if not self.questions:
            print("No quiz available")
            return 
        for i in range(len(self.questions)):
            q = self.questions[i]
            print(f"{i+1}: {q.get_question()}")
            for j in range(len(q.choices)):
                print(f"{j+1}. {q.choices[j]}")
            print(f"Correct Answer: {q.get_correct_answer()}")
    
    def execute_quiz(self):
        """
        Purpose:
            Prompts the user to answer each question by entering the index 
        Inputs:
            None 
        Outputs:
            int: The number of correct answers for this run.
        """
        if not self.questions:
            print("No quiz available")
            return 
        score = 0
        wrong_answers = []

        for i in range(len(self.questions)):
            q = self.questions[i]
            print(f"{i+1}: {q.get_question()}")
            for j in range(len(q.choices)):
                print(f"{j+1}. {q.choices[j]}")
            # Keep asking until a valid index is provided
            while True:
                try:
                    user_answer = int(input("Your answer: "))
                    # Validate 1-based choice index
                    if 1 <= user_answer <= len(q.choices):
                        selected_choice = q.choices[user_answer - 1]
                        if selected_choice == q.get_correct_answer():
                            score = score + 1
                            print("Correct!")
                        else:
                            wrong_answers.append((i+1, q.get_question(), selected_choice, q.get_correct_answer()))
                            print("Incorrect!")
                        break
                    else: 
                        print(f"Please enter a number between 1 and {len(q.choices)}")
                except ValueError:
                    # Handles non-integer input 
                    print("Please enter a valid number")
        
        percentage = (score/ len(self.questions)) * 100
        print(f"Final Percentage: {percentage} %")

        if wrong_answers:
            print("Incorrect answers: ")
            for q_num, question, your_answer, correct_answer in wrong_answers:
                print(f"Q{q_num}: {question}")
                print(f"Your answer: {your_answer}")
                print(f"Correct answer: {correct_answer}")
        
        return score 
    
"""
This program lets you create named quizzes, add multiple-choice questions (exactly 4 choices, pick the correct one).
Preview a quiz’s questions and correct answers. Take a quiz with a global countdown timer (30s per question), see your score,
and review which questions you missed.
"""

from tkinter import *
from tkinter import messagebox

quizzes = {}    # Create an empty quiz 

def create_quiz():
    """
    Purpose:
        - Open a dialog to create a new, named Quiz and store it in the global 'quizzes' dict.
    Inputs:
        - Reads the quiz name from an Entry in a Toplevel window.
    Outputs:
        - On success: inserts quizzes[name] = Quiz(), shows a success dialog, and closes the window.
        - On failure: shows an error dialog (duplicate or empty name).
        - Creates/destroys a Toplevel window.
    """
    win = Toplevel()
    win.title("Create Quiz")
    win.geometry("300x150")

    Label(win, text="Enter Quiz Name: ").pack(pady=10)
    ent = Entry(win)
    ent.pack(pady=5)

    def save_quiz():
        """
        Validate the name and create the Quiz object if the name is new and non-empty
        """
        name = ent.get()
        if name and name not in quizzes:
            quizzes[name] = Quiz()
            messagebox.showinfo("Success", "Quiz created!")
            win.destroy()
        else:
            # Either empty name or a name that already exists.
            messagebox.showerror("Error", "Invalid name")
    
    Button(win, text="Create", command=save_quiz).pack(pady=20)

def add_question():
    """
    Purpose:
        - Open a dialog to add a new multiple-choice question to one of the existing quizzes.

    Inputs:
        - User selects a quiz name
        - User provides the question text and 4 choice strings.
        - User inputs the index (1–4) of the correct choice.

    Outputs:
        - On success: constructs a Quiz_item and calls quiz.add_question(item),
          shows success dialog, and closes the window.
        - On failure: shows an error dialog and keeps the window open.
        - Creates/destroys a Toplevel window.
    """
    if not quizzes:
        messagebox.showerror("Error", "No quizzes available")
        return
    
    win = Toplevel()
    win.title("Add Question")
    win.geometry("420x470")

    # Quiz selector
    Label(win, text="Select Quiz:").pack(pady=20)
    quiz_var = StringVar()
    first_name = next(iter(quizzes.keys())) # pick any existing quiz name as default
    quiz_var.set(first_name)
    for name in quizzes.keys():
        Radiobutton(win, text=name, variable=quiz_var, value=name).pack(fill='x', padx=12)
    
    # Question prompt and choices 
    Label(win, text="Question: ").pack(padx=12, pady=(10,2))
    ent_q = Entry(win, width=50)
    ent_q.pack(padx=12, pady=(0,8))

    Label(win, text="Choices:").pack(anchor="w", padx=12)
    Label(win, text="(fill all 4, then pick the correct number 1–4)").pack(anchor="w", padx=12, pady=(0,6))

    # Each row holds the label for the index and the Entry
    row = Frame(win)
    row.pack(fill="x", padx=12, pady=2)
    Label(row, text="1").pack(side="left")
    ent_c1 = Entry(row, width=40)
    ent_c1.pack(side="left")

    row = Frame(win)
    row.pack(fill="x", padx=12, pady=2)
    Label(row, text="2").pack(side="left")
    ent_c2 = Entry(row, width=40)
    ent_c2.pack(side="left")

    row = Frame(win)
    row.pack(fill="x", padx=12, pady=2)
    Label(row, text="3").pack(side="left")
    ent_c3 = Entry(row, width=40)
    ent_c3.pack(side="left")

    row = Frame(win)
    row.pack(fill="x", padx=12, pady=2)
    Label(row, text="4").pack(side="left")
    ent_c4 = Entry(row, width=40)
    ent_c4.pack(side="left")

    Label(win, text="Correct Answer (enter 1–4):").pack(anchor="w", padx=12, pady=(10,2))
    ent_correct = Entry(win, width=6)
    ent_correct.pack(anchor="w", padx=12)

    def save():
        """
        Validate inputs, build a Quiz_item, and append it to the selected Quiz.
        Raises:
            - Shows message boxes for any validation errors rather than raising Python exceptions.
        """
        quiz_name = quiz_var.get()
        question = ent_q.get()
        choices = [ent_c1.get(), ent_c2.get(), ent_c3.get(), ent_c4.get()]

        # validations
        if not quiz_name:
            messagebox.showerror("Error", "Please select a quiz.")
            return
        if not question:
            messagebox.showerror("Error", "Please enter a question.")
            return
        if not all(choices):
            messagebox.showerror("Error", "Please fill all four choices.")
            return

        try:
            idx = int(ent_correct.get())
        except:
            messagebox.showerror("Error", "Correct answer must be between 1 and 4.")
            return

        if not (1 <= idx <= 4):
            messagebox.showerror("Error", "Correct answer must be between 1 and 4.")
            return

        correct_answer = choices[idx - 1]

        try:
            # Create the item and add it to the selected quiz
            item = Quiz_item(question, choices, correct_answer)
            quizzes[quiz_name].add_question(item)
        except Exception as e:
            # raise any error that could be caused 
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Success", "Question added!")
        win.destroy()

    Button(win, text="Add Question", command=save).pack(pady=16)

def preview_quiz():
    """
    Purpose:
        Allow the user to select a quiz and preview all questions and the correct answers.
    Inputs:
        - Quiz name
    Outputs:
        - Updates a label within the Toplevel to display the quiz contents.
        - Shows an error dialog if there are no quizzes.
        - Creates/destroys a Toplevel window.
    """
    if not quizzes:
        messagebox.showerror("Error", "No quizzes available")
        return
    
    win = Toplevel()
    win.title("Preview Quiz")
    win.geometry("500x400")

    Label(win, text="Select Quiz: ").pack(pady=(10,4))
    quiz_var = StringVar()
    quiz_var.set(next(iter(quizzes)))   #default pick 

    for name in quizzes.keys():
        Radiobutton(win, text=name, variable=quiz_var, value=name).pack(fill="x", padx=12)

    lbl = Label(win, text="Quiz will be shown here")
    lbl.pack(fill="both", expand=True, padx=12, pady=10)

    def show():
        """
        Update the currently selected quiz's questions and correct answers into the label.
        """
        name = quiz_var.get()
        qz = quizzes[name]
        if not qz.questions:
            lbl.config(text="No questions in this quiz yet")
            return
        # Build a human-readable preview
        lines = []
        i = 1
        for q in qz.questions:
            lines.append(f"{i}. {q.get_question()}")
            j = 1
            for c in q.choices:
                lines.append(f"{j}) {c}")
                j = j + 1
            lines.append(f"Correct: {q.get_correct_answer()}")
            i = i + 1
        
        lbl.config(text="\n".join(lines))
        
    Button(win, text="Show Quiz", command=show).pack(pady=5)

def choose_quiz():
    """
    Purpose:
        Let the user pick which quiz to take, then launch the quiz.
    Inputs:
        - Quiz name 
    Outputs:
        - Opens the quiz window on success.
        - Shows an error if the chosen quiz has no questions.
        - Creates/destroys a Toplevel window.
    """
    if not quizzes:
        messagebox.showerror("Error", "No quizzes available")
        return
    
    choose = Toplevel()
    choose.title("Select Quiz")
    choose.geometry("300x200")

    Label(choose, text="Choose Quiz: ").pack(pady=(10,6))
    quiz_var = StringVar()
    quiz_var.set(next(iter(quizzes)))   # Default pick

    for name in quizzes.keys():
        Radiobutton(choose, text=name, variable=quiz_var, value=name).pack(padx=12)
    
    def start():
        """
        Start the selected quiz, otherwise show an error
        """
        name = quiz_var.get()
        qz = quizzes[name]
        if not qz.questions:
            messagebox.showerror("Error", "That quiz has no questions")
            return
        choose.destroy()
        run_quiz(qz, name)

    Button(choose, text="Start Quiz", command=start).pack(pady=12)

def run_quiz(qz, name):
    """
    Runs the quiz for the selected quiz name.

    Purpose:
        - Shows each question one by one with multiple-choice answers.
        - Starts a countdown timer (30 seconds per question in total).
        - Keeps track of correct and wrong answers.
        - At the end, shows your score and a summary of mistakes.

    Inputs:
        - qz: the Quiz object (contains the list of questions).
        - name: the quiz name (used as the window title).
    Outputs:
        - Creates a new Toplevel window for the quiz run.
        - Displays timer, question, multiple-choice options, and a Next/Finish button.
        - At the end, shows a results with score and missed questions.
        - Destroys the quiz window when time is up.
    """
    index = {"value": 0}    # default value 0 (assuming 0 current questions)
    score= {"value": 0}     # number of correct answers 
    missed = []             # empty list for (q_number, question_text, your_answer, correct_answer)

    # Total time = 30 seconds per question
    total_time = len(qz.questions) * 30 
    remaining_time = {"value": total_time}
    timer_running = {"value": True}

    win = Toplevel()
    win.title("Choosing: " + name)
    win.geometry("500x300")
    
    # Question text label
    q_label = Label(win, text="")
    q_label.pack(padx=12, pady=(12,8))

    # Timer and progress 
    timer_frame = Frame(win)
    timer_frame.pack(fill="x", padx=12, pady=5)
    
    timer_label = Label(timer_frame, text="")
    timer_label.pack()
    
    progress_label = Label(timer_frame, text="")
    progress_label.pack()

    # Navigation button(next/finish)
    next_btn = Button(win, text="Next")
    next_btn.pack(pady=12)

    # Answer options 
    answer_var = StringVar()
    opts_frame = Frame(win)
    opts_frame.pack(fill="x", padx=12)

    def clear_options():
        """
        Remove any existing Radiobuttons so we can update the next question's choices.
        """
        for widget in opts_frame.winfo_children():
            widget.destroy()

    def update_timer():
        """
        Decrease the timer once per second, update the readout, and
        trigger finish() if time runs out.
        """
        if not timer_running["value"]:
            return
        
        current_q = index["value"] + 1
        total_q = len(qz.questions)
        remaining_q = total_q - index["value"]
        # Integer division
        if remaining_q > 0:
            time_per_remaining = remaining_time["value"] // remaining_q
        else:
            time_per_remaining = 0
        
        mins, secs = divmod(remaining_time["value"], 60)
        
        timer_label.config(text=f"Time Remaining: {mins}:{secs}")
        progress_label.config(text=f"Question {current_q}/{total_q} | Questions Remaining: {remaining_q} | Time per remaining question: {time_per_remaining}s")
        
        if remaining_time["value"] <= 0:
            # Time is up, stop the timer and exit the quiz
            timer_running["value"] = False
            messagebox.showwarning("Time Up!", "You ran out of time.")
            finish()
            return
        
        # Schedule the timer for 1000ms=1s
        remaining_time["value"] -= 1
        win.after(1000, update_timer)  

    def update_quiz():
        """
        Update the current question and its choices. If we are past the last question,
        end the quiz by calling finish().
        """
        i = index["value"]
        if i >= len(qz.questions):
            finish()
            return
        
        q = qz.questions[i]
        q_label.config(text="Q" + str(i+1) + ": " + q.get_question())
        answer_var.set("")  # clear previous selection
        clear_options()

        # Rebuild the options as Radiobuttons for the current question
        j = 1
        for choice in q.choices:
            Radiobutton(opts_frame, text=str(j) + ". " + choice, value=choice, variable=answer_var,).pack(fill="x", pady=2)
            j = j + 1
        
        if i == len(qz.questions) - 1:
            next_btn.config(text="Finish")
        else:
            next_btn.config(text="Next")
    
    def submit():
        """
        Record the chosen answer (if any), update score/missed, advance to next question,
        and re update. If user hasn't picked an option, warn and stay on the current question.
        """
        i = index["value"]
        if i >= len(qz.questions):
            finish()
            return

        q = qz.questions[i]
        chosen = answer_var.get()
        if not chosen:
            messagebox.showwarning("Choose one", "Please select an answer.")
            return

        if chosen == q.get_correct_answer():
            score["value"] = score["value"] + 1
        else:
            missed.append((i+1, q.get_question(), chosen, q.get_correct_answer()))

        index["value"] = index["value"] + 1
        update_quiz()

    def finish():
        """
        Stop the timer, compute and show final results (score and percent),
        and list incorrect answers with your choice vs. the correct one.
        Then close the quiz window.
        """
        timer_running["value"] = False  
        total = len(qz.questions)
        final_score = score["value"]
        total = len(qz.questions)
        final_score = score["value"]
        pct = (final_score / total) * 100
        # Build result summary
        result_lines = [f"Quiz Completed!\nScore: {final_score}/{total} ({pct}%)"]
        
        if missed:
            result_lines.append("Incorrect answers:")
            for n, ques, your, corr in missed:
                result_lines.append(f"Q{n}: {ques}")
                result_lines.append(f"Your answer: {your}")
                result_lines.append(f"Correct answer: {corr}")
        
        messagebox.showinfo("Quiz Results", "\n".join(result_lines))
        win.destroy()

    # Call the functions
    next_btn.config(command=submit)
    update_quiz()
    update_timer()

# Main window screen
root = Tk()
root.title("Quiz Management System")
root.geometry("400x300")

Label(root, text="Quiz Management System").pack(pady=20)
Button(root, text="Create New Quiz", command=create_quiz, width=20).pack(pady=5)
Button(root, text="Add Question to Quiz", command=add_question, width=20).pack(pady=5)
Button(root, text="Preview Quiz", command=preview_quiz, width=20).pack(pady=5)
Button(root, text="Take Quiz", command=choose_quiz, width=20).pack(pady=5)
Button(root, text="Exit", command=root.quit, width=20).pack(pady=20)

# Enter the Tkinter loop
root.mainloop()
