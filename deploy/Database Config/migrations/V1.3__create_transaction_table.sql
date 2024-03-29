CREATE TYPE holder_type AS ENUM (
    'bank', 'credit_card', 'emi', 'loan', 'expense', 'income', 'stock', 'fd', 'asset'
    );

CREATE TABLE transactions
(
    id                UUID PRIMARY KEY,
    created_at        TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at  TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    from_account_id   UUID        DEFAULT NULL,
    from_account_type holder_type DEFAULT NULL,
    to_account_id     UUID        DEFAULT NULL,
    to_account_type   holder_type DEFAULT NULL,
    amount            NUMERIC NOT NULL,
    user_id           UUID    NOT NULL,
    CHECK (from_account_id IS NOT NULL OR to_account_id IS NOT NULL),
    CHECK (from_account_type IS NOT NULL OR to_account_type IS NOT NULL),
    remarks           TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX transaction_id ON transactions (id);
CREATE INDEX transaction_user_id ON transactions (user_id);
