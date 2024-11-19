CREATE DATABASE spellboundtable;

USE spellboundtable;

CREATE TABLE user (
    user_id int NOT NULL AUTO_INCREMENT,
    user_name varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(255) NOT NULL,

    CONSTRAINT pk_user PRIMARY KEY(user_id)
);

CREATE TABLE campaign (
    campaign_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    name varchar(50) NOT NULL,
    description text NOT NULL,
    freq varchar(10) NOT NULL,
    img_link text NOT NULL,
    
    CONSTRAINT pk_campaign PRIMARY KEY(campaign_id),
    CONSTRAINT fk_campaign_user FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE `character` (
    character_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    campaign_id int NOT NULL,
    name varchar(50) NOT NULL,
    class varchar(50) NOT NULL,
    img_link text NOT NULL,
    race varchar(20) NOT NULL,
    money float NOT NULL,
    `force` int NOT NULL,
    dest int NOT NULL,
    consti int NOT NULL,
    intel int NOT NULL,
    wisdom int NOT NULL,
    charisma int NOT NULL,
    armor int NOT NULL,
    initi int NOT NULL,
    desloc int NOT NULL,
    hp int NOT NULL,
    b_proef int NOT NULL,
    inspiration int NOT NULL,

    CONSTRAINT `pk_character` PRIMARY KEY(character_id),
    CONSTRAINT `fk_user_id` FOREIGN KEY (user_id) REFERENCES user(user_id),
    CONSTRAINT `fk_campaign_id` FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id)

);

CREATE TABLE artifact (
    artifact_id INT NOT NULL PRIMARY KEY,
    campaign_id INT NOT NULL,
    name varchar(50) NOT NULL,
    `desc` TEXT NOT NULL,
    category CHAR(50) NOT NULL,
    CONSTRAINT `fk_artifact_campaign_id` FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id)
);

CREATE TABLE inventory (
    character_id INT NOT NULL,
    artifact_id INT NOT NULL,
    CONSTRAINT `fk_character_id` FOREIGN KEY (character_id) REFERENCES `character`(character_id),
    FOREIGN KEY `fk_artifact_id` (artifact_id) REFERENCES artifact(artifact_id)
);

CREATE TABLE entry_campaign (
    user_id INT NOT NULL,
    campaign_id INT NOT NULL,
    CONSTRAINT `fk_entry_camp_user_id` FOREIGN KEY (user_id) REFERENCES user(user_id),
    CONSTRAINT `fk_entry_camp_campaign_id` FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id)
);

CREATE TABLE created_campaign (
    user_id INT NOT NULL,
    campaign_id INT NOT NULL,
    CONSTRAINT `fk_created_camp_user_id` FOREIGN KEY (user_id) REFERENCES user(user_id),
    CONSTRAINT `fk_created_camp_campaign_id` FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id)
);