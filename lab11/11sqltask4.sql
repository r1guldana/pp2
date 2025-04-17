SELECT * FROM paginated_data('phonebook', 5, 0)
AS t(id INT, name VARCHAR(100), phone VARCHAR(20));
