CREATE TABLE expenses
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    name             VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    amount           NUMERIC NOT NULL,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX expense_id ON expenses (id);
CREATE INDEX expense_user_id ON expenses (user_id);
