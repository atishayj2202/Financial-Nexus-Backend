CREATE TABLE fds
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    bank_name        VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    amount           NUMERIC     DEFAULT 0,
    interest_rate    NUMERIC     DEFAULT 0,
    duration         NUMERIC     DEFAULT 0,
    sell_amount      NUMERIC     DEFAULT 0,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX fd_id ON fds (id);
CREATE INDEX fd_user_id ON fds (user_id);
