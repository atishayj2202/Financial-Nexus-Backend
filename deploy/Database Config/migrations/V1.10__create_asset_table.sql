CREATE TABLE assets
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    name             VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    amount           NUMERIC     DEFAULT 0,
    sell_price       NUMERIC     DEFAULT 0,
    buy_transaction  UUID NOT NULL UNIQUE,
    sell_transaction UUID DEFAULT NULL,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX asset_id ON assets (id);
CREATE INDEX asset_user_id ON assets (user_id);
