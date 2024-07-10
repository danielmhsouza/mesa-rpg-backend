const UserService = require('../services/userService');

exports.getAllUsers = function (req, res) {
    const id = req.query.id
    const users = UserService.getAllUsers(id);
    res.json(users);
}

exports.createUser = (req, res) => {
    const newUser = req.body;

    const createdUser = UserService.createUser(newUser);
    res.json(createdUser);
}

exports.deleteUser = (req, res) => { 
    const id = req.params.id;

    const noDeletedUsers = UserService.deleteUser(id);
    res.json(noDeletedUsers);
}

exports.updateUser = (req, res) => {
    const updateUser = req.body;
    const id = req.params.id;

    const updatedUser = UserService.updateUser(id, updateUser);
    res.json(updatedUser);
}