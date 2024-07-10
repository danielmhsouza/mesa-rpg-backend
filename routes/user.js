const express = require('express');
const router = express.Router();
const UserController = require('../controllers/userController');

router.get('/', UserController.getAllUsers);
router.post('/', UserController.createUser);
router.delete('/:id', UserController.deleteUser);
router.patch('/:id', UserController.updateUser);

module.exports = router;