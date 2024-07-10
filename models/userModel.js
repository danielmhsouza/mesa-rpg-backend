var users = [
    {
        id: 1,
        name: 'Daniel',
        email: 'daniel@email.com',
        data_nascimento: "03/07/2000"
    },
    {
        id: 2,
        name: 'Sara',
        email: 'sara@email.com',
        data_nascimento: "05/06/2002"
    },
    {
        id: 3,
        name: 'Felipe',
        email: 'felipe@email.com',
        data_nascimento: "24/11/2005"
    },
];

exports.find = (userID) => {
    if (userID > 0) {
        const u = users.filter(value => (value.id == userID));
        return u;
    }
    return users;
}

exports.create = (user) => {
    let newID = users.length + 1;
    let isUserValid = user.hasOwnProperty('name');
    isUserValid &= user.hasOwnProperty('email');
    isUserValid &= user.hasOwnProperty('data_nascimento');

    if (!isUserValid) {
        return "Invalid User"
    }

    user.id = newID;

    users.push(user);
    return user
}

exports.delete = (userID) => {
    users = users.filter(value => (value.id != userID));

    return users;
}

exports.update = (userID, obj) => {
    let u = users.filter(user => user.id == userID);
    console.log(u);

    for (v of Object.keys(obj)) {
        console.log(v)
        if (v in u[0]) {
            u[0][v] = obj[v];
        }
    }
    return u;
}