-- name: get-all-users
-- Get all user records
SELECT * from users;

-- name: find-user-by-username
SELECT id, username, email, password
FROM users
WHERE username = :username
LIMIT 1;

--name: find-user-by-username
SELECT id, username, email, password FROM users WHERE email=:email LIMIT 1;


