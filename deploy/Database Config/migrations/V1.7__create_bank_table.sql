CREATE TABLE banks
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    name             VARCHAR NOT NULL,
    bank_name        VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    balance          NUMERIC     DEFAULT 0,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX bank_id ON banks (id);
CREATE INDEX bank_user_id ON banks (user_id);
