const UserModel = require('../models/userModel');

exports.createUser = (user) => {
    return UserModel.create(user);
}

exports.getAllUsers = (user) => {
    return UserModel.find(user);
}

exports.deleteUser = (user) => {
    return UserModel.delete(user);
}

exports.updateUser = (id, obj) => {
    return UserModel.update(id, obj);
}