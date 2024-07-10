const express = require('express');
const userRoutes = require('./routes/user');

const PORT = 3333;

const app = express();

app.use(express.json());

app.use('/user/', userRoutes);

app.listen(PORT, ()=>{console.log(`running: http://localhost:${PORT}`)});