CREATE TYPE message_by AS ENUM ('user', 'ai');

CREATE TABLE messages
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    message          VARCHAR NOT NULL,
    message_by       message_by NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX message_id ON messages (id);
CREATE INDEX message_user_id ON messages (user_id);
