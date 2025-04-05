UPDATE users
SET name = %(name)s, updated_at = NOW()
WHERE id = %(id)s;