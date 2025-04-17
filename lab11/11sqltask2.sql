CREATE OR REPLACE PROCEDURE insert_users(
user_name varchar(100)[],
user_phone varchar(100)[]
)
LANGUAGE plpgsql
AS $$
DECLARE --объявление переменной  
    i INTEGER;
BEGIN
	for i in 1..array_length(user_name, 1) loop

		IF user_phone[i] ~ '^[0-9]{9,15}$' THEN
                   		--start[numbers]{количество}end
		
        INSERT INTO phonebook (name, phone)
        VALUES (user_name[i], user_phone[i])
        ON CONFLICT (name) DO UPDATE 
        SET phone = EXCLUDED.phone;
END IF;
	
end loop ;
end; 
$$ ;

--select * from phonebook 
--CALL insert_users(
--ARRAY['notuser', 'noting'],
--ARRAY['877712345649949937', '8771200003333213242']);
