CREATE TABLE cards
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    name             VARCHAR NOT NULL,
    card_name        VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    pending          NUMERIC     DEFAULT 0,
    credit_limit     NUMERIC     DEFAULT 0,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX card_id ON cards (id);
CREATE INDEX card_user_id ON cards (user_id);
