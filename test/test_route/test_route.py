from unittest import TestCase
from routes.Route import Route

class UserTest(TestCase):

    def setUp(self):
        print("\n **INICIANDO TESTES** \n")

    def test_register(self):
        self.route:Route = Route()
        user_data: dict = {
            "user_name": "newUser",
            "email": "newemail@email.com",
            "password": "senha123",
            "confPass": "senha123"
        }

        valid_response: dict = {
            "statusCode": 200,
            "data": "Usuário Cadastrado com Sucesso!"
        }

        self.assertEqual(self.route.register(
            user_data["user_name"], user_data["email"], user_data["password"], user_data["confPass"]), 
            valid_response
        )

        user_data["email"] = ""
        self.assertEqual(self.route.register(
            user_data["user_name"], user_data["email"], user_data["password"], user_data["confPass"]), 
            {"statusCode": 403, "data": "Preencha todos os campos."}
        )


        user_data["email"] = "email@email.com"
        self.assertEqual(self.route.register(
            user_data["user_name"], user_data["email"], user_data["password"], user_data["confPass"]), 
            {"statusCode": 403, "data": "Email já cadastrado!"}
        )

        user_data["confPass"] = '321senha'
        self.assertEqual(self.route.register(
            user_data["user_name"], user_data["email"], user_data["password"], user_data["confPass"]), 
            {"statusCode": 403, "data": "Confirme a senha corretamente!"}
        )

        user_data["confPass"] = "senh"
        user_data["password"] = "senh"
        self.assertEqual(self.route.register(user_data["email"], user_data["password"]), {
          "statusCode": 403,
          "data": "A senha deve conter pelo menos 6 caracteres."  
        })

        user_data["confPass"] = "senha123"
        user_data["password"] = "senha123"
        user_data["email"] = "invalid_email"
        self.assertEqual(self.route.register(user_data["email"], user_data["password"]), {
          "statusCode": 403,
          "data": "Email inválido."  
        })

    def test_login(self):
        self.route: Route = Route()
        user_data: dict = {
            "email": "email@email.com",
            "password": "senha123"
        }

        valid_response: dict = {
            "statusCode": 200,
            "data": {
                "user_id": 0,
                "username": "Teste",
                "email": "email@email.com"
            }
        }

        self.assertEqual(self.route.login(user_data["email"], user_data["password"]), valid_response)

        user_data["email"] = "invalid_email"
        self.assertEqual(self.route.login(user_data["email"], user_data["password"]), {
          "statusCode": 403,
          "data": "Dados inválidos"  
        })

        user_data["email"] = "emailnotfound@email.com"
        self.assertEqual(self.route.login(user_data["email"], user_data["password"]), {
            "statusCode": 403,
            "data": "Email não cadastrado"
        })

        user_data["email"] = ''
        self.assertEqual(self.route.login(user_data["email"], user_data["password"]), {
          "statusCode": 403,
          "data": "Campos obrigatórios!"  
        })

        user_data["email"] = "email@email.com"
        user_data["password"] = ''
        self.assertEqual(self.route.login(user_data["email"], user_data["password"]), {
          "statusCode": 403,
          "data": "Campos obrigatórios!"  
        })

        user_data["password"] = "321senha"
        self.assertEqual(self.route.login(user_data["email"], user_data["password"]), {
          "statusCode": 403,
          "data": "Email ou Senha inválida."  
        })
    
    def test_create_campaing(self):
        self.route: Route = Route()

        data: dict = {
            "name": "Teste",
            "desc": "Uma campanha de teste",
            "freq": "mensal",
            "imgLink": ""
        }

        self.assertEqual(self.route.create_campaign(
                data["name"], data["desc"], data["freq"], data["imgLink"]
            ),
            {
                "statusCode": 200,
                "data": "Campanha criada com sucesso!"
            }
        )
        
        self.assertEqual(self.route.create_campaign(
                "", data["desc"], data["freq"], data["imgLink"]   
            ),
            {
                "statusCode": 403,
                "data": "Preencha todos os campos!"
            }
        )
        
        self.assertEqual(self.route.create_campaign(
                data["name"], data["desc"], data["freq"], "https://youtube.com"   
            ),
            {
                "statusCode": 403,
                "data": "O link da imagem é inválido."
            }
        )

    def test_enter_campaing(self):
        self.route: Route = Route()

        campaign_code: int = 0
        character_code: int = 0
        user_id = 0

        self.assertEqual(self.route.enter_campaign(campaign_code, character_code),
                         {
                             "statusCode": 200,
                             "data": "Nova campanha adicionada."
                         })
        
        num_campaign:int = self.route.controller.count_user_entry_campaing()
        self.assertEqual(num_campaign+1, self.route.controller.count_user_entry_campaing())

        self.assertEqual(self.route.enter_campaign_as_master(campaign_code, user_id),
                         {
                             "statusCode": 200,
                             "data": {}

                         })
        # TODO: verificar quais dados retornar quando entrar na campanha como mestre
        
        self.assertEqual(self.route.enter_campaign_as_player(campaign_code, user_id),
                         {
                             "statusCode": 200,
                             "data": {}

                         })
        # TODO: verificar quais dados retornar quando entrar na campanha como player

    def test_create_character(self):
        pass
    
    
        
        




