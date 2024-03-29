CREATE TABLE user_accounts
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    email            VARCHAR NOT NULL,
    name             VARCHAR NOT NULL,
    firebase_user_id VARCHAR NOT NULL,
    UNIQUE (firebase_user_id),
    UNIQUE (email)
);

CREATE INDEX idx_firebase_user_id ON user_accounts (firebase_user_id);
CREATE INDEX idx_phone_no ON user_accounts (email);