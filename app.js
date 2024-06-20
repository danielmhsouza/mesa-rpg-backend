const express = require('express');

const PORT = 3333;

const app = express();

app.use(express.json());

app.get("/teste", (req, res)=>{
    return res.json({message: "it is running."});
})

app.listen(PORT, ()=>{console.log(`running: http://localhost:${PORT}`)});