import os
import random
from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")  # fallback for local testing


@app.route("/")
def home():
    """Home page - starts the game if not already started"""
    if "number" not in session:  # start new game if not active
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0
        session["game_over"] = False
        session["message"] = "🎯 I'm thinking of a number between 1 and 100!"

    return render_template(
        "index.html",
        message=session["message"],
        attempts=session["attempts"],
        game_over=session["game_over"]
    )


@app.route("/guess", methods=["POST"])
def guess():
    """Handles the user's guess"""
    if "number" not in session:  # if no active game, restart
        return redirect(url_for("home"))

    try:
        user_guess = int(request.form["guess"])
    except ValueError:
        session["message"] = "⚠️ Please enter a valid number!"
        return redirect(url_for("home"))

    session["attempts"] += 1
    number = session["number"]

    if user_guess < number:
        session["message"] = "⬆️ Too low! Try again."
    elif user_guess > number:
        session["message"] = "⬇️ Too high! Try again."
    else:
        session["message"] = (
            f"🎉 Correct! The number was {number}. "
            f"You guessed it in {session['attempts']} tries."
        )
        session["game_over"] = True  # mark game as finished

    return redirect(url_for("home"))


@app.route("/reset")
def reset():
    """Resets the game for a new round"""
    session.clear()  # clears all session data at once
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)



# Guess the Number Game
# A simple web application where users guess a randomly generated number.
# The app provides feedback on whether the guess is too high, too low, or correct.
# It tracks the number of attempts and allows for a new game after a correct guess.