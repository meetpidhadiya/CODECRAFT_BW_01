const express = require('express');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = 3000;
app.use(express.json());

const users = {}; // In-memory storage

// Create User
app.post('/users', (req, res) => {
    const { name, email, age } = req.body;
    if (!name || !email || !age || typeof age !== 'number' || !email.includes('@')) {
        return res.status(400).json({ error: 'Invalid input' });
    }
    const id = uuidv4();
    users[id] = { id, name, email, age };
    res.status(201).json(users[id]);
});

// Read All Users
app.get('/users', (req, res) => {
    res.json(Object.values(users));
});

// Read Single User
app.get('/users/:id', (req, res) => {
    const user = users[req.params.id];
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

// Update User
app.put('/users/:id', (req, res) => {
    const { name, email, age } = req.body;
    if (!name || !email || !age || typeof age !== 'number' || !email.includes('@')) {
        return res.status(400).json({ error: 'Invalid input' });
    }
    const user = users[req.params.id];
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    users[req.params.id] = { id: req.params.id, name, email, age };
    res.json(users[req.params.id]);
});

// Delete User
app.delete('/users/:id', (req, res) => {
    if (!users[req.params.id]) {
        return res.status(404).json({ error: 'User not found' });
    }
    delete users[req.params.id];
    res.status(204).send();
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
