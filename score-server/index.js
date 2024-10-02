const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.set('view engine', 'ejs');

app.use(express.json());
app.use(express.static('public'));  // Serve static files (e.g., CSS, JS)

let gameStarted = false;
let startTime = null;
let elapsedTime = 0;

const playerScores = {
  1: { name: 'Player 1', score: 0 },
  2: { name: 'Player 2', score: 0 },
  3: { name: 'Player 3', score: 0 },
  4: { name: 'Player 4', score: 0 },
  5: { name: 'Player 5', score: 0 },
  6: { name: 'Player 6', score: 0 },
  7: { name: 'Player 7', score: 0 },
};

// Add score to the specified player
app.post('/score', (req, res) => {
  const { player_id, score } = req.body;
  if (playerScores[player_id]) {
    playerScores[player_id].score += score;
    console.log(`Score updated for Player ${player_id}: ${playerScores[player_id].score}`);
    res.json({ status: 'success' });
  } else {
    res.status(404).json({ status: 'Player not found' });
  }
});

// Start game by sending POST request to http://red:5555/game-start
app.post('/start-game', async (req, res) => {
  try {
    const response = await axios.post('http://red:5555/game-start');
    if (response.data.status === 'Game started') {
      gameStarted = true;
      startTime = Date.now();
      return res.json({ status: 'Game started' });
    } else {
      return res.status(500).json({ status: 'Failed to start game' });
    }
  } catch (error) {
    console.error('Error starting game:', error.message);
    return res.status(500).json({ status: 'Failed to start game' });
  }
});

// Endpoint to return elapsed time
app.get('/elapsed-time', (req, res) => {
  if (!gameStarted) {
    return res.json({ elapsedTime: 0 });
  }

  elapsedTime = Math.floor((Date.now() - startTime) / 1000);  // Elapsed time in seconds
  res.json({ elapsedTime });
});

// Serve the main page
app.get('/', async (req, res) => {
  const players = Object.keys(playerScores).map(player_id => ({
    name: playerScores[player_id].name,
    score: playerScores[player_id].score
  }));

  // Sort players by score in descending order
  players.sort((a, b) => b.score - a.score);

  // Calculate elapsed time for initial rendering
  if (gameStarted) {
    elapsedTime = Math.floor((Date.now() - startTime) / 1000);  // In seconds
  }

  res.render('index', { players, gameStarted, elapsedTime });
});

// Start the server
app.listen(port, () => {
  console.log(`Score server listening at http://localhost:${port}`);
});
