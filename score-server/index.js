const express = require('express');
const app = express();
const port = 3000;

app.set('view engine', 'ejs');

app.use(express.json());

// In-memory storage for player scores (player_id: score)
let playerScores = {
  1: { name: 'Player 1', score: 0 },
  2: { name: 'Player 2', score: 0 },
  3: { name: 'Player 3', score: 0 },
  4: { name: 'Player 4', score: 0 },
  5: { name: 'Player 5', score: 0 },
  6: { name: 'Player 6', score: 0 },
  7: { name: 'Player 7', score: 0 },
};

app.get('/', (req, res) => {
  // Convert playerScores object into an array for easier iteration
  const players = Object.keys(playerScores).map(player_id => ({
    name: playerScores[player_id].name,
    score: playerScores[player_id].score
  }));

  // Sort players by score in descending order
  players.sort((a, b) => b.score - a.score);

  // Render the template with the sorted players
  res.render('index', { players: players });
});

app.post('/score', (req, res) => {
  const { player_id, score } = req.body;

  if (!player_id || !score) {
    res.status(400).json({ error: 'player_id and score are required' });
  }

  // Convert score to integer
  const scoreInt = parseInt(score, 10);

  // Check if player exists
  if (playerScores[player_id]) {
    // Increase player's score
    playerScores[player_id].score += scoreInt;
    res.json({ player_id, score: playerScores[player_id].score });
  } else {
    res.status(404).json({ error: 'Player not found' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Score server listening at http://localhost:${port}`);
});
