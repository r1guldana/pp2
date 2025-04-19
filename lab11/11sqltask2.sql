CALL insert_users(
    ARRAY['Altyn', 'Dian'],
    ARRAY['87771234567', '87771234568']
);
select * from phonebook;
'''CREATE OR REPLACE PROCEDURE insert_users(
    user_name varchar(100)[],
    user_phone varchar(100)[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(user_name, 1) LOOP
        IF user_phone[i] ~ '^[0-9]{9,15}$' THEN
        
            UPDATE phonebook
            SET phone = user_phone[i]
            WHERE name = user_name[i];
        
            IF NOT FOUND THEN
                INSERT INTO phonebook (name, phone)
                VALUES (user_name[i], user_phone[i]);
            END IF;
        
        END IF;
    END LOOP;
END;
$$;
'''