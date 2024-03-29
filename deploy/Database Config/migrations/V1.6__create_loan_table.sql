CREATE TABLE loans
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    name             VARCHAR NOT NULL,
    bank_name        VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    pending          NUMERIC     DEFAULT 0,
    total_amount     INTEGER     DEFAULT 0,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX loan_id ON loans (id);
CREATE INDEX loan_user_id ON loans (user_id);
