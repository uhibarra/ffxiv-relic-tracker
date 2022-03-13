SELECT *
FROM arr_paladin;

DELETE FROM arr_paladin;

--

SELECT *
FROM arr_weapon;

DELETE FROM arr_weapon;

--

SELECT *
FROM character;

DELETE FROM character;

--
SELECT *
FROM public.user;

DELETE FROM public.user;

DELETE FROM public.user
WHERE email <> 'test@test.com';