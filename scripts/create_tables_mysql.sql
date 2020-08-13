
CREATE TABLE IF NOT EXISTS member (
  `id`          INT          PRIMARY KEY AUTO_INCREMENT,
  `family_name` VARCHAR(30)  NOT NULL,
  `family_kana` VARCHAR(30),
  `first_name`  VARCHAR(30)  NOT NULL,
  `first_kana`  VARCHAR(30),
  `show_name`   VARCHAR(30)  NOT NULL,
  `kana`        VARCHAR(60)  , -- for index
  `year`        INT          NOT NULL,
  `sex`         VARCHAR(30)  ,         -- フォームで選択式&自由記述にする, NULLABLE
  `visible`     BOOL         NOT NULL DEFAULT true,
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX (year, family_kana, first_kana)
  -- `comment`    TEXT,           -- 管理者のみが見れるコメント e.g. 学年が怪しい、とか...　-- いずれ実装したい
);

CREATE TABLE IF NOT EXISTS training (
  `id`          INT           PRIMARY KEY AUTO_INCREMENT,
  `date`        DATE          NOT NULL,
  `type`       VARCHAR(30)   NOT NULL,
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
  `id`            INT PRIMARY KEY AUTO_INCREMENT,
  `name`          VARCHAR(30) NOT NULL,  -- 記入ミスの際の変更を可能にするため、サロゲートキー利用
  `place`         VARCHAR(30),
  `score`         FLOAT NOT NULL DEFAULT 0,
  `comment`       TEXT,
  `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS after (
  `id`            INT PRIMARY KEY AUTO_INCREMENT,
  `date`          DATE NOT NULL,
  `after_stage`   INT NOT NULL DEFAULT 1,
  `restaurant_id` INT NOT NULL, -- FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`id`),
  `title`         VARCHAR(200) NOT NULL,
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

CREATE TABLE IF NOT EXISTS competition (
  `id`           INT PRIMARY KEY AUTO_INCREMENT,  -- 記入ミスの際の変更を可能にするため、サロゲートキー利用
  `name`         VARCHAR(60) NOT NULL,
  `kana`         VARCHAR(60),
  `show_name`    VARCHAR(30),
  `place`        VARCHAR(30),
  `comment`      TEXT,
  `created_at`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS course (
  `id`           INT PRIMARY KEY AUTO_INCREMENT,
  `type`  VARCHAR(30) NOT NULL DEFAULT 'road', -- ['road', 'trail', 'time', 'relay']
  `competition_id`   INT NOT NULL, -- FOREIGN KEY REFERENCES competition(id)
  `show_name`    VARCHAR(30),
  `time`         INT,   -- running time in seconds for type 'time' or 'relay'
  `distance`     DOUBLE, -- running distance in kilo meter
  `elevation`    INT, -- cumulative elevation in meter
  `comment`      TEXT,
  `created_at`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- コース変更があった場合は新たに作成する
-- いずれ地図データ等もつけたい

CREATE TABLE IF NOT EXISTS race (
  `id`          INT PRIMARY KEY AUTO_INCREMENT,
  `course_id`   INT NOT NULL, -- FOREIGN KEY REFERENCES course(id)
  `date`        DATE NOT NULL,
  `comment`     TEXT,
  `created_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- 年度ごとに分ける

CREATE TABLE IF NOT EXISTS result (
  `id`            INT PRIMARY KEY AUTO_INCREMENT,
  `race_id`       INT NOT NULL,      -- FOREIGN KEY REFERENCES race(id)
  `time`          INT,               -- net time in milliseconds
  `distance`      DOUBLE,            -- running distance in kilo meter -- 完走時はレース距離を入れる
  `comment`       TEXT,              -- 記録には距離を入れる。　リレマラの周回数とか？
  `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX (distance),
  INDEX (time)
);
-- リレーマラソンに対応するため、 resultに１人以上のデータを紐付けるようにする
-- フォームでは隠蔽

CREATE TABLE IF NOT EXISTS race_participant (
  `result_id`     INT NOT NULL, -- FOREIGN KEY REFERENCES result(id)
  `member_id`     INT NOT NULL, -- FOREIGN KEY REFERENCES member(id)
  `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE ekiden_competition (
  `id`           INT PRIMARY KEY AUTO_INCREMENT,  -- start at 10000 for avoiding collision with normal competition
  `name`         VARCHAR(100),                    -- 記入ミスの際の変更を可能にするため、サロゲートキー利用
  `kana`         VARCHAR(100),
  `show_name`    VARCHAR(30),
  `place`        VARCHAR(30), -- '代々木公園', '駒沢公園', '沖縄県', 'ホノルル' 等
  `comment`      TEXT,
  `created_at`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE ekiden_race (
  `id`                    INT PRIMARY KEY AUTO_INCREMENT,
  `ekiden_competition_id` INT NOT NULL, -- FOREIGN KEY REFERENCES ekiden_competition(id)
  `date`                  DATE NOT NULL,
  `comment`               TEXT,
  `created_at`            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX (date)
);


CREATE TABLE ekiden_team (
  `id`              INT PRIMARY KEY AUTO_INCREMENT,
  `ekiden_race_id`  INT NOT NULL, -- FOREIGN KEY REFERENCES ekiden_race(id)
  `team_name`       VARCHAR(30),
  `comment`         TEXT,
  `created_at`      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE ekiden_result (
  `ekiden_team_id`  INT NOT NULL,
  `kukan`           INT NOT NULL,
  `member_id`       INT NOT NULL,
  `time_individual` INT,
  `time_gross`      INT,
  `comment`         TEXT,
  `created_at`      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

