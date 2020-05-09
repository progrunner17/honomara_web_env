
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
  `visible`     BOOL         NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS training (
  `id`      INT           PRIMARY KEY AUTO_INCREMENT,
  `date`    DATE          NOT NULL,
  `place`   VARCHAR(30)   NOT NULL,
  `weather` VARCHAR(30),
  `title`   VARCHAR(100)  NOT NULL,
  `comment` TEXT,
  INDEX USING BTREE (date),
  FULLTEXT (title) WITH PARSER ngram,
  FULLTEXT (comment) WITH PARSER ngram
);

CREATE TABLE IF NOT EXISTS restaurant (
  id               INT PRIMARY KEY AUTO_INCREMENT,
  name  VARCHAR(30) NOT NULL, -- TODO: change column name to `name`
  place            VARCHAR(30),
  score FLOAT NOT NULL DEFAULT 0,
  comment TEXT
);

CREATE TABLE IF NOT EXISTS after (
  `id`            INT PRIMARY KEY AUTO_INCREMENT,
  `date`          DATE NOT NULL,
  `after_stage`   INT NOT NULL DEFAULT 1,
  `restaurant_id` INT NOT NULL, -- FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`id`),
  `title`         VARCHAR(100) NOT NULL,
  `comment`       TEXT,
  INDEX USING BTREE(`date`),
  FULLTEXT (title) WITH PARSER ngram,
  FULLTEXT (comment) WITH PARSER ngram
);

CREATE TABLE IF NOT EXISTS  after_participant (
  member_id   INT NOT NULL, -- FOREIGN KEY REFERENCES member(id)
  after_id    INT NOT NULL  -- FOREIGN KEY REFERENCES after(id)
);


CREATE TABLE IF NOT EXISTS  training_participant (
  member_id   INT NOT NULL, -- FOREIGN KEY REFERENCES member(id)
  training_id INT NOT NULL  -- FOREIGN KEY REFERENCES training(id)
);

CREATE TABLE IF NOT EXISTS competition (
  `id`        INT         PRIMARY KEY AUTO_INCREMENT,
  `name`      VARCHAR(60) NOT NULL,
  `name_kana` VARCHAR(60), -- sort用
  `show_name` VARCHAR(60),
  `location`  VARCHAR(30),
  `url`       TEXT,
  `comment`   TEXT
);


CREATE TABLE IF NOT EXISTS course_base (
  `id`        INT                 PRIMARY KEY AUTO_INCREMENT,
  `type`      VARCHAR(30)         NOT NULL, -- ロード、トレイル、トラック、時間走
  `distance`  INT,  -- m
  `duration`  INT,  -- s
  `comment`   TEXT
);

CREATE TABLE IF NOT EXISTS course (
  `id`                      INT           PRIMARY KEY AUTO_INCREMENT,
  `competition_id`          INT           NOT NULL, -- FOREIGN KEY REFERENCES competition(id)
  `course_base_id`          INT           NOT NULL, -- FOREIGN KEY REFERENCES cource(id)
  `name`                    VARCHAR(60),
  `cumulative_elevation`    INT,  -- m
  `comment`                 TEXT
);

CREATE TABLE IF NOT EXISTS race (
  `id`                      INT         PRIMARY KEY AUTO_INCREMENT,
  `course_id`               INT         NOT NULL,    -- FOREIGN KEY REFERENCES cource(id)
  `date`                    DATE        NOT NULL,
  `comment`                 INT
);



CREATE TABLE IF NOT EXISTS result (
  `member_id`             INT         NOT NULL,  -- FOREIGN KEY REFERENCES member(id)
  `race_id`               INT         NOT NULL,  -- FOREIGN KEY REFERENCES race(id)
  `time`                  INT,  -- ms
  `distance`              INT,  -- m
  `comment`               TEXT
);
