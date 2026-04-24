-- Posts
CREATE TABLE posts (
    id                      BIGINT PRIMARY KEY,
    post_type_id            SMALLINT,
    accepted_answer_id      BIGINT,
    creation_date           TIMESTAMP,
    score                   INT,
    view_count              INT,
    body                    TEXT,
    owner_user_id           BIGINT,
    owner_display_name      TEXT,
    last_editor_user_id     BIGINT,
    last_editor_display_name TEXT,
    last_edit_date          TIMESTAMP,
    last_activity_date      TIMESTAMP,
    title                   TEXT,
    tags                    TEXT,
    answer_count            INT,
    comment_count           INT,
    favorite_count          INT,
    parent_id               BIGINT,
    closed_date             TIMESTAMP,
    community_owned_date    TIMESTAMP
);

-- Users
CREATE TABLE users (
    id                  BIGINT PRIMARY KEY,
    display_name        TEXT,
    creation_date       TIMESTAMP,
    last_access_date    TIMESTAMP,
    reputation          INT,
    views               INT,
    up_votes            INT,
    down_votes          INT,
    website_url         TEXT,
    location            TEXT,
    about_me            TEXT,
    account_id          BIGINT,
    age                 INT,
    profile_image_url   TEXT
);

-- Votes
CREATE TABLE votes (
    id              BIGINT PRIMARY KEY,
    post_id         BIGINT,
    vote_type_id    SMALLINT,
    creation_date   TIMESTAMP,
    user_id         BIGINT,
    bounty_amount   INT
);

-- Comments
CREATE TABLE comments (
    id                BIGINT PRIMARY KEY,
    post_id           BIGINT,
    score             INT,
    text              TEXT,
    creation_date     TIMESTAMP,
    user_id           BIGINT,
    user_display_name TEXT
);

-- Tags
CREATE TABLE tags (
    id               BIGINT PRIMARY KEY,
    tag_name         TEXT,
    count            INT,
    excerpt_post_id  BIGINT,
    wiki_post_id     BIGINT
);

-- Badges
CREATE TABLE badges (
    id       BIGINT PRIMARY KEY,
    user_id  BIGINT,
    name     TEXT,
    date     TIMESTAMP,
    class    SMALLINT
);

-- PostHistory
CREATE TABLE post_history (
    id                    BIGINT PRIMARY KEY,
    post_history_type_id  SMALLINT,
    post_id               BIGINT,
    revision_guid         TEXT,
    creation_date         TIMESTAMP,
    user_id               BIGINT,
    text                  TEXT,
    comment               TEXT,
    user_display_name     TEXT
);

-- PostLinks
CREATE TABLE post_links (
    id               BIGINT PRIMARY KEY,
    creation_date    TIMESTAMP,
    post_id          BIGINT,
    related_post_id  BIGINT,
    link_type_id     SMALLINT
);
