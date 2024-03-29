CREATE TABLE feedbacks
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    rating           INT  NOT NULL CHECK (rating > 0),
    feedback         VARCHAR     DEFAULT NULL,
    from_user_id     UUID NOT NULL,
    FOREIGN KEY (from_user_id) REFERENCES user_accounts (id)
);

CREATE INDEX feedbacks_from_user_id_idx ON feedbacks (from_user_id);
