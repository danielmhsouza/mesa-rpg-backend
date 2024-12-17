from .Database import Database
class User:

    def __init__(self):
        self.database = Database()
        self.query = {
            "register": "INSERT INTO user (user_name, email, password) VALUES (%s, %s, %s)",
            "select": "SELECT * FROM user WHERE email = %s AND password = %s",
            "update": "UPDATE user SET user_name = %s, email = %s, password = %s WHERE user_id = %s",
            "delete": "DELETE FROM user WHERE user_id = %s"
        }

    def insert_user(self, user_data: dict) -> int:

        values = (user_data['user_name'], user_data['email'], user_data['password'])
        if self.database.execute_query(self.query["register"], values):
                return self.database.return_last_insert()
        return 0

    def select_user(self, email: str, password: str) -> dict:

        values = (email, password)
        result = self.database.execute_select_query(self.query["select"], values)
        
        if result:
            return {
                "user_id": result[0][0],
                "user_name": result[0][1],
                "email": result[0][2],
                "password": result[0][3],

            }
        return {}

    def update_user(self, user_data: dict) -> bool:

        values = (user_data['user_name'], user_data['email'], user_data['password'], user_data['user_id'])
        return self.database.execute_query(self.query["update"], values)
