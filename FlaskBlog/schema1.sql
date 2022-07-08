PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE post
    ADD COLUMN post_image1 VARCHAR(250) NULL;
    INSERT INTO post_image1 SELECT * FROM post_image

COMMIT;

PRAGMA foreign_keys=on;