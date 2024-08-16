CREATE TABLE "match" (
    match_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    rival_id INT NOT NULL,
    match_result VARCHAR(10) NULL,  -- ENUM 타입 대신 VARCHAR 또는 TEXT로 대체
    match_start_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    match_end_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    match_user_grade INT NULL,
    match_rival_grade INT NULL,
    match_type VARCHAR(10) NULL  -- ENUM 타입 대신 VARCHAR 또는 TEXT로 대체
);

CREATE TABLE "friend" (
    user_id INT NOT NULL,
    friend_id INT NOT NULL,
    friend_relation VARCHAR(10) NOT NULL CHECK (friend_relation IN ('pending', 'accepted')),  -- ENUM 대체
    PRIMARY KEY (user_id, friend_id)
);

CREATE TABLE "tournament" (
    tournament_id SERIAL PRIMARY KEY,
    semifinal_id1 INT NULL,
    semifinal_id2 INT NULL,
    bonus_match_id INT NULL,
    final_id INT NULL
);

CREATE TABLE "Image" (
    image_id SERIAL PRIMARY KEY,
    image BYTEA NOT NULL
);

CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    profile_image_id INT NULL,
    user_login_id VARCHAR(10) NOT NULL CHECK (user_login_id != ''),
    user_login_password VARCHAR(20) NOT NULL CHECK (user_login_password != ''),
    user_profile_nickname VARCHAR(10) NOT NULL,
    user_macrotext1 VARCHAR(20) NULL DEFAULT 'good game',
    user_macrotext2 VARCHAR(20) NULL DEFAULT 'thanks',
    user_macrotext3 VARCHAR(20) NULL DEFAULT 'bye bye',
    user_macrotext4 VARCHAR(20) NULL DEFAULT 'gooooood!',
    user_macrotext5 VARCHAR(20) NULL DEFAULT 'hello',
    CONSTRAINT fk_profile_image FOREIGN KEY (profile_image_id) REFERENCES "Image" (image_id)
);

-- FK constraints are already applied above in user table
