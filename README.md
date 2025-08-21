# ♟️ Chess Minimax AI

A Python-based chess game that includes a playable interface and an AI opponent using the Minimax algorithm. The AI logic is hosted via a Flask server (designed to run on Google Colab), and the frontend runs locally using main\_v3.py. This setup allows the user to play against a computer with basic move prediction capabilities powered by Minimax.

#
📌 Features

* 👨‍💻 Local playable chess board with graphical assets
* 🧠 AI opponent using the Minimax algorithm (Flask API)
* 🔁 Server-client architecture (backend in Google Colab via ngrok)
* 🖼️ PNG chess piece images for intuitive gameplay
* ✅ Simple, portable structure with no external GUI library required


#
🗂 Project Structure

```
chess\_minimax/
├── main\_v3.py                  # Frontend GUI chess board (client)
├── chess\_server.ipynb          # Backend Flask server (run in Colab)
├── assets\_v3/                  # PNG images for chess pieces
│   ├── bK.png, wK.png, ...     # Black/white pieces (King, Queen, etc.)
```

#
🚀 How It Works

1. The chess\_server.ipynb runs a Flask API that receives a FEN string and responds with the best move using Minimax.
2. The main\_v3.py file renders a local chess board GUI and sends board states to the server for move calculation.
3. The user plays white; the server plays black.


#
🔌 Setting Up the Server (Google Colab)

1. Open chess\_server.ipynb in Google Colab.

2. Run all cells. It will:

   * Install Flask & pyngrok
   * Start a Flask server with Minimax logic
   * Expose it via an ngrok public URL like:

     [https://abc123.ngrok.io](https://abc123.ngrok.io)

3. Copy the ngrok URL.


#
📝 Set the Server URL in main\_v3.py

At the top of main\_v3.py, update this line with your ngrok URL:

python
COLAB_URL = "url123/best_move"

Replace url123 with your actual session’s ngrok subdomain.


#
▶️ Running the Game

After pasting your ngrok URL:

1. Ensure the server is running in Colab.
2. Run the local GUI:

python
python main\_v3.py

3. A window will appear. Click on white pieces to make a move.
4. The AI will respond after each move based on the server-side Minimax prediction.


#
📦 Requirements

* Python 3.x
* Required libraries:

  For server (in Colab):

  * flask
  * flask\_cors
  * chess
  * pyngrok

  For client (local):

  * pygame
  * requests
  * chess

Install with:

bash
pip install flask flask\_cors chess pygame requests pyngrok


#
🧠 Minimax Logic

* The server evaluates moves using the Minimax algorithm with depth-limited search.
* Board states are encoded using FEN and evaluated for material advantage.
