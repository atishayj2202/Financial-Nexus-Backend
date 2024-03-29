CREATE TABLE stocks
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    symbol           VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    amount           NUMERIC     DEFAULT 0,
    buy_price        NUMERIC     DEFAULT 0,
    avg_sell_price   NUMERIC     DEFAULT 0,
    already_sold     NUMERIC     DEFAULT 0,
    remarks          TEXT,
    buy_transaction  UUID NOT NULL UNIQUE,
    sell_transactions UUID[] DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX stock_id ON stocks (id);
CREATE INDEX stock_user_id ON stocks (user_id);
