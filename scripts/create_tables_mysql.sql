
CREATE TABLE IF NOT EXISTS member (
  `id`          INT          PRIMARY KEY AUTO_INCREMENT,
  `family_name` VARCHAR(30)  NOT NULL,
  `family_kana` VARCHAR(30),
  `first_name`  VARCHAR(30)  NOT NULL,
  `first_kana`  VARCHAR(30),
  `show_name`   VARCHAR(30)  NOT NULL,
  `kana`        VARCHAR(60)  , -- for index
  `year`        INT          NOT NULL,
  `sex`         INT          NOT NULL DEFAULT 0, -- 0=man, 1=woman
  `visible`     BOOL         NOT NULL DEFAULT true,
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training (
  `id`          INT           PRIMARY KEY AUTO_INCREMENT,
  `date`        DATE          NOT NULL,
  `place`       VARCHAR(30)   NOT NULL,
  `weather`     VARCHAR(30),
  `title`       VARCHAR(100)  NOT NULL,
  `comment`     TEXT,
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX USING BTREE (date),
  FULLTEXT (title) WITH PARSER ngram,
  FULLTEXT (comment) WITH PARSER ngram
);

CREATE TABLE IF NOT EXISTS restaurant (
  id              INT PRIMARY KEY AUTO_INCREMENT,
  name            VARCHAR(30) NOT NULL, -- TODO: change column name to `name`
  place           VARCHAR(30),
  score           FLOAT NOT NULL DEFAULT 0,
  comment         TEXT,
  `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS after (
  `id`            INT PRIMARY KEY AUTO_INCREMENT,
  `date`          DATE NOT NULL,
  `after_stage`   INT NOT NULL DEFAULT 1,
  `restaurant_id` INT NOT NULL, -- FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`id`),
  `title`         VARCHAR(100) NOT NULL,
  `comment`       TEXT,
  `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX USING BTREE(`date`),
  FULLTEXT (title) WITH PARSER ngram,
  FULLTEXT (comment) WITH PARSER ngram
);

CREATE TABLE IF NOT EXISTS  after_participant (
  `member_id`   INT NOT NULL, -- FOREIGN KEY REFERENCES member(id)
  `after_id`    INT NOT NULL, -- FOREIGN KEY REFERENCES after(id)
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS  training_participant (
  `member_id`   INT NOT NULL, -- FOREIGN KEY REFERENCES member(id)
  `training_id` INT NOT NULL, -- FOREIGN KEY REFERENCES training(id)
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS race_base (
  `race_name`      VARCHAR(60) PRIMARY KEY,
  `race_name_kana` VARCHAR(60),
  `prefecture`     VARCHAR(30),
  `comment`        TEXT,
  `created_at`     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS race (
  `id`          INT PRIMARY KEY AUTO_INCREMENT,
  `race_name`   VARCHAR(60) NOT NULL,
  `date`        DATE NOT NULL,
  `comment`     TEXT,
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS race_type (
  `id`         INT PRIMARY KEY AUTO_INCREMENT,
  `race_type`  VARCHAR(30) NOT NULL DEFAULT 'road',
  `show_name`  VARCHAR(30),
  `ranking`    INT NOT NULL DEFAULT 100,
  `duration`   FLOAT,
  `distance`   FLOAT,
  `comment`    TEXT,
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS result (
  `member_id`     INT NOT NULL, -- FOREIGN KEY REFERENCES member(id)
  `race_type_id`  INT NOT NULL, -- FOREIGN KEY REFERENCES race_type(id)
  `race_id`       INT NOT NULL, -- FOREIGN KEY REFERENCES race(id)
  `result`        INT NOT NULL,
  `comment`       TEXT,
  `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
);

