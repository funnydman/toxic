-- name: get-all-users
-- Get all user records
SELECT * from users;

-- name: find-user-by-username
select * from users where username=:username;
