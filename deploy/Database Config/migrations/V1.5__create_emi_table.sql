CREATE TABLE emis
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID    NOT NULL,
    name             VARCHAR NOT NULL,
    bank_name        VARCHAR NOT NULL,
    disabled         TIMESTAMPTZ DEFAULT NULL,
    pending          NUMERIC     DEFAULT 0,
    monthly          NUMERIC     DEFAULT 0,
    total_time       INTEGER     DEFAULT 0,
    remarks          TEXT,
    FOREIGN KEY (user_id) REFERENCES user_accounts (id)
);

CREATE INDEX emi_id ON emis (id);
CREATE INDEX emi_user_id ON emis (user_id);
