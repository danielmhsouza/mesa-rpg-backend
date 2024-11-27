import unittest

from controllers.Controller import SpellBoundTable


class TestSpellBoundTable(unittest.TestCase):

    def setUp(self):
        SpellBoundTable.users = []
        SpellBoundTable.campaigns = []
        SpellBoundTable.artifacts = ["Espada", "Escudo"]
        SpellBoundTable.players = ["John"]

    # Login tests
    def test_login_success(self):
        SpellBoundTable.register("John Doe", "john@example.com", "password123", "password123")
        result = SpellBoundTable.login("john@example.com", "password123")
        self.assertEqual(result, "Entrar na Plataforma")

    def test_login_invalid_email_or_password(self):
        SpellBoundTable.register("John Doe", "john@example.com", "password123", "password123")
        result = SpellBoundTable.login("john@example.com", "wrongpassword")
        self.assertEqual(result, "Email ou senha inválido")

    def test_login_user_not_registered(self):
        result = SpellBoundTable.login("nonexistent@example.com", "password123")
        self.assertEqual(result, "Usuário não cadastrado")

    # Registration tests
    def test_register_success(self):
        result = SpellBoundTable.register("John Doe", "john@example.com", "password123", "password123")
        self.assertEqual(result, "Cadastro realizado")

    def test_register_missing_fields(self):
        result = SpellBoundTable.register("", "john@example.com", "password123", "password123")
        self.assertEqual(result, "Campos obrigatórios")

    def test_register_password_mismatch(self):
        result = SpellBoundTable.register("John Doe", "john@example.com", "password123", "password321")
        self.assertEqual(result, "Confirme a senha corretamente")

    def test_register_password_too_short(self):
        result = SpellBoundTable.register("John Doe", "john@example.com", "pass", "pass")
        self.assertEqual(result, "Digite uma senha válida (pelo menos 6 caract...)")

    def test_register_email_already_registered(self):
        SpellBoundTable.register("John Doe", "john@example.com", "password123", "password123")
        result = SpellBoundTable.register("Jane Doe", "john@example.com", "password123", "password123")
        self.assertEqual(result, "Email já cadastrado")

    # Campaign tests
    def test_create_campaign_success(self):
        result = SpellBoundTable.create_campaign("Aventura Épica", "Uma jornada épica", "http://image.com/img.jpg", "Semanal")
        self.assertEqual(result, "Campanha Criada")

    def test_create_campaign_missing_fields(self):
        result = SpellBoundTable.create_campaign("", "Uma jornada épica", "http://image.com/img.jpg", "Semanal")
        self.assertEqual(result, "Preencher campos obrigatórios")

    def test_create_campaign_invalid_link(self):
        result = SpellBoundTable.create_campaign("Aventura Épica", "Uma jornada épica", "invalidlink", "Semanal")
        self.assertEqual(result, "Link inválido ou ignorar link")

    # Character tests
    def test_join_campaign_success(self):
        result = SpellBoundTable.join_campaign("Aventura Épica", character_created=True)
        self.assertEqual(result, "Campanha aparece na página inicial")

    def test_join_campaign_without_character(self):
        result = SpellBoundTable.join_campaign("Aventura Épica", character_created=False)
        self.assertEqual(result, "Não entrará na campanha")

    # Artifact tests
    def test_add_artifact_success(self):
        result = SpellBoundTable.add_artifact("John", "Espada")
        self.assertEqual(result, "John tem acesso ao artefato")

    def test_add_artifact_nonexistent(self):
        result = SpellBoundTable.add_artifact("John", "Amuleto")
        self.assertEqual(result, "Artefato inexistente")

    def test_add_artifact_player_not_in_campaign(self):
        result = SpellBoundTable.add_artifact("Jane", "Espada")
        self.assertEqual(result, "Jogador fora da campanha")

    def test_remove_artifact_success(self):
        result = SpellBoundTable.remove_artifact("John", "Espada")
        self.assertEqual(result, "Espada removido do inventário do John")

    def test_remove_artifact_nonexistent(self):
        result = SpellBoundTable.remove_artifact("John", "Amuleto")
        self.assertEqual(result, "Artefato inexistente")
