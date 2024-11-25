query_users = {
    "register": "INSERT INTO user (user_name, email, password) VALUES (%s, %s, %s)",
    "select": "SELECT * FROM user WHERE email = %s AND password = %s",
    "update": "UPDATE user SET user_name = %s, email = %s, password = %s WHERE user_id = %s",
    "delete": "DELETE FROM user WHERE user_id = %s",
}

query_campaigns = {
    "register": "INSERT INTO campaign (user_id, name, description, freq, img_link) VALUES (%s, %s, %s, %s, %s)",
    "select": "SELECT * FROM campaign WHERE campaign_id = %s",
    "update": "UPDATE campaign SET name = %s, description = %s, freq = %s, img_link = %s WHERE campaign_id = %s",
    "delete": "DELETE FROM campaign WHERE campaign_id = %s",
}

query_characters = {
    "register": "INSERT INTO character (user_id, campaign_id, name, class, img_link, race, money, force, dest, consti, intel, wisdom, charisma, armor, init, desloc, hp, bProef, inspiration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "select": "SELECT * FROM character WHERE character_id = %s",
    "update": "UPDATE character SET name = %s, class = %s, img_link = %s, race = %s, money = %s, force = %s, dest = %s, consti = %s, intel = %s, wisdom = %s, charisma = %s, armor = %s, init = %s, desloc = %s, hp = %s, bProef = %s, inspiration = %s WHERE character_id = %s",
    "delete": "DELETE FROM character WHERE character_id = %s",
}

query_artifacts = {
    "register": "INSERT INTO artifact (campaign_id, name, desc, category) VALUES (%s, %s, %s, %s)",
    "select": "SELECT * FROM artifact WHERE campaign_id = %s",
    "update": "UPDATE artifact SET name = %s, desc = %s, category = %s WHERE artifact_id = %s",
    "delete": "DELETE FROM artifact WHERE artifact_id = %s",
}

query_inventory = {
    "register": "INSERT INTO inventory (character_id, artifact_id) VALUES (%s, %s)",
    "select": "SELECT * FROM inventory WHERE character_id = %s",
    "delete": "DELETE FROM inventory WHERE character_id = %s AND artifact_id = %s",
}

query_entry_campaign = {
    "register": "INSERT INTO entry_campaign (user_id, campaign_id) VALUES (%s, %s)",
    "select": "SELECT * FROM entry_campaign WHERE user_id = %s AND campaign_id = %s",
    "delete": "DELETE FROM entry_campaign WHERE user_id = %s AND campaign_id = %s",
}

query_created_campaign = {
    "register": "INSERT INTO created_campaign (user_id, campaign_id) VALUES (%s, %s)",
    "select": "SELECT * FROM created_campaign WHERE user_id = %s AND campaign_id = %s",
    "delete": "DELETE FROM created_campaign WHERE user_id = %s AND campaign_id = %s",
}
