-- migrate:up
CREATE TABLE messages (
    id SERIAL NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO messages (text) VALUES
    ('Hello from the database'),
    ('These rows come from the first migration');

-- migrate:down
DROP TABLE messages;
