PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE post
    RENAME COLUMN image_file to post_image;

COMMIT;

PRAGMA foreign_keys=on;