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

// Fetch attack progress and calculate player scores
async function updateScores() {
  try {
    const response = await axios.get('http://red:5555/attack-progress');
    const progress = response.data;

    const playerScores = {
      1: { name: 'Player 1', score: 0 },
      2: { name: 'Player 2', score: 0 },
      3: { name: 'Player 3', score: 0 },
      4: { name: 'Player 4', score: 0 },
      5: { name: 'Player 5', score: 0 },
      6: { name: 'Player 6', score: 0 },
      7: { name: 'Player 7', score: 0 },
    };

    // Calculate scores based on attack progress
    for (let step in progress) {
      for (let container in progress[step]) {
        const result = progress[step][container];
        const player_id = container.replace('container', '');  // e.g., 'container1' -> '1'
        
        if (result === 'failed') {
          playerScores[player_id].score += 50;
        }
      }
    }
    console.log(playerScores);
    return playerScores;
  } catch (error) {
    console.error('Error fetching attack progress:', error.message);
  }
}

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

// Serve the main page
app.get('/', async (req, res) => {
  try {
    const playerScores = await updateScores();

    // Convert playerScores object into an array for easier iteration
    const players = Object.keys(playerScores).map(player_id => ({
      name: playerScores[player_id].name,
      score: playerScores[player_id].score
    }));

    // Sort players by score in descending order
    players.sort((a, b) => b.score - a.score);

    // Calculate elapsed time
    if (gameStarted) {
      elapsedTime = Math.floor((Date.now() - startTime) / 1000);  // In seconds
    }

    res.render('index', { players, gameStarted, elapsedTime });
  } catch (error) {
    console.error('Error fetching attack progress:', error.message);
    res.status(500).send('Error fetching attack progress');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Score server listening at http://localhost:${port}`);
});
