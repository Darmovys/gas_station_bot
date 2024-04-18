-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Ноя 05 2023 г., 14:49
-- Версия сервера: 10.4.27-MariaDB
-- Версия PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `автозаправка`
--

-- --------------------------------------------------------

--
-- Структура таблицы `керування_пальним`
--

CREATE TABLE `керування_пальним` (
  `id_дії` int(11) NOT NULL,
  `дата_і_час_дії` datetime DEFAULT current_timestamp(),
  `купив` int(11) DEFAULT NULL,
  `додав` int(11) DEFAULT NULL,
  `id_пального` int(11) NOT NULL,
  `кількість_л` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `керування_пальним`
--

INSERT INTO `керування_пальним` (`id_дії`, `дата_і_час_дії`, `купив`, `додав`, `id_пального`, `кількість_л`) VALUES
(1, '2023-10-01 17:20:46', 7, NULL, 3, 100),
(2, '2023-10-01 17:22:07', NULL, 4, 8, 200),
(3, '2023-10-01 17:23:19', NULL, 1, 6, 300),
(4, '2023-10-01 17:23:58', 2, NULL, 1, 400),
(5, '2023-10-01 17:24:31', 5, NULL, 9, 500),
(6, '2023-10-01 18:52:42', NULL, 1, 1, 6000),
(7, '2023-10-01 18:57:22', 4, NULL, 1, 6000),
(8, '2023-10-15 18:56:02', 11, NULL, 1, 500),
(9, '2023-10-15 18:56:02', 11, NULL, 7, 700),
(10, '2023-10-29 14:15:55', 12, NULL, 6, 300),
(11, '2023-10-29 14:15:55', 12, NULL, 10, 400);

--
-- Триггеры `керування_пальним`
--
DELIMITER $$
CREATE TRIGGER `Перевірка_наявного_пального` BEFORE INSERT ON `керування_пальним` FOR EACH ROW BEGIN
    DECLARE доступна_кількість DOUBLE;
    SELECT залишок_л INTO доступна_кількість
    FROM типи_пального
    WHERE id_пального = NEW.id_пального;
    
    IF NEW.додав IS NULL AND NEW.кількість_л > доступна_кількість THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Недостатньо пального на складі для цієї операції';
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `зняття_залишку_пального` AFTER INSERT ON `керування_пальним` FOR EACH ROW BEGIN
	IF NEW.додав IS NULL THEN
    	UPDATE типи_пального
    	SET Залишок_л = Залишок_л - NEW.кількість_л
    	WHERE id_пального = NEW.id_пального;
    ELSE
    	UPDATE типи_пального
    	SET Залишок_л = Залишок_л + NEW.кількість_л
        WHERE id_пального = NEW.id_пального;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `керування_товарами`
--

CREATE TABLE `керування_товарами` (
  `id_дії` int(11) NOT NULL,
  `дата_і_час_дії` datetime DEFAULT current_timestamp(),
  `купив` int(11) DEFAULT NULL,
  `додав` int(11) DEFAULT NULL,
  `id_товару` int(11) NOT NULL,
  `кількість` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `керування_товарами`
--

INSERT INTO `керування_товарами` (`id_дії`, `дата_і_час_дії`, `купив`, `додав`, `id_товару`, `кількість`) VALUES
(1, '2023-10-01 17:26:10', NULL, 2, 8, 1),
(2, '2023-10-01 17:26:57', 4, NULL, 1, 1),
(3, '2023-10-01 17:27:28', 9, NULL, 6, 1),
(4, '2023-10-01 17:27:52', NULL, 3, 4, 2),
(5, '2023-10-01 17:28:21', 8, NULL, 5, 5),
(6, '2023-10-01 19:10:53', NULL, 2, 1, 60),
(7, '2023-10-01 19:11:57', 8, NULL, 1, 60),
(8, '2023-10-21 16:34:44', 11, NULL, 7, 1),
(9, '2023-10-21 16:34:44', 11, NULL, 6, 1),
(10, '2023-10-29 15:30:35', NULL, 5, 3, 0),
(11, '2023-10-29 15:36:40', NULL, 5, 9, 6);

--
-- Триггеры `керування_товарами`
--
DELIMITER $$
CREATE TRIGGER `доступна_кількість_т` BEFORE INSERT ON `керування_товарами` FOR EACH ROW BEGIN
    DECLARE доступна_кількість INT;
    SELECT кількість INTO доступна_кількість
    FROM товари
    WHERE id_товару = NEW.id_товару;
    IF NEW.додав IS NULL AND NEW.кількість > доступна_кількість THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Недостатньо товару на складі для цієї операції';
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `зняття_залишку_товарів` AFTER INSERT ON `керування_товарами` FOR EACH ROW BEGIN
	IF NEW.додав IS NULL THEN
    	UPDATE товари
    	SET Кількість = Кількість - NEW.кількість
    	WHERE id_товару = NEW.id_товару;
    ELSE
    	UPDATE товари
    	SET Кількість = Кількість + NEW.кількість
        WHERE id_товару = NEW.id_товару;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `клієнти`
--

CREATE TABLE `клієнти` (
  `id_клієнта` int(11) NOT NULL,
  `ім’я_користувача` varchar(15) NOT NULL,
  `ПІБ` varchar(35) NOT NULL,
  `номер_телефону` varchar(15) DEFAULT NULL,
  `електронна_пошта` varchar(25) DEFAULT NULL,
  `пароль` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `клієнти`
--

INSERT INTO `клієнти` (`id_клієнта`, `ім’я_користувача`, `ПІБ`, `номер_телефону`, `електронна_пошта`, `пароль`) VALUES
(1, 'kasch', 'Кащук Наталія Андріївна', '0991111111', 'kashchnat@gmail.com', 'Djzjawzgz5'),
(2, 'galavar', 'Галацан Варвара Андріївна', '0991111112', 'galavar@gmail.com', 'XnxPvaybk9'),
(3, 'vieana', 'Вієцька Анастасія Валентинівна', '0991111113', 'vieana@gmail.com', 'J7ONs77Hav'),
(4, 'mil', 'Мілян Денис Ігорович', '0991111114', 'mildenig@gmail.com', 'aV7bC2Ma4D'),
(5, 'zaha', 'Захарко Даніїл Юрійович', '0991111115', 'dazaha@gmail.com', 'jKhki7tX0n'),
(6, 'dernaz', 'Деркач Назар Тарасович', '0991111116', 'dernaz@gmail.com', 'fnB1wP7emq'),
(7, 'sawUw', 'Савка Діана Сергіївна', '0991111117', 'Savian@gmail.com', 'XWP7NRAGjc'),
(8, 'roropo', 'Потюк Роман Романович', '0991111118', 'potroom@outlook.com', '3zkTSYdLcy'),
(9, 'Rokyry', 'Кириченко Артем Романович', '0991111119', 'rokyry.art@gmail.com', 'olg1vCyk2H'),
(10, 'malaj', 'Малай Солома Володимирівна', '0991111120', 'malajsoloma@gmail.com', 'mvkfWOwUCd'),
(11, 'Taras', 'Тарасюк Тарас Вікторович', NULL, NULL, 'qwerty123'),
(12, 'Anton', 'Тарасюк Антон Вікторович', NULL, 'Anton@gmail.com', '123456789');

-- --------------------------------------------------------

--
-- Структура таблицы `працівники`
--

CREATE TABLE `працівники` (
  `id_працівника` int(11) NOT NULL,
  `ідентифікатор` varchar(10) NOT NULL,
  `ПІБ` varchar(35) NOT NULL,
  `телефон` varchar(15) NOT NULL,
  `електронна_пошта` varchar(25) NOT NULL,
  `посада` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `працівники`
--

INSERT INTO `працівники` (`id_працівника`, `ідентифікатор`, `ПІБ`, `телефон`, `електронна_пошта`, `посада`) VALUES
(1, 'QAIRyphk1T', 'Кабуша Богдан Іванович', '0981111111', 'kaboogi@gmail.com', 'Продавець пального'),
(2, 'AA3fO9hjD6', 'Буйна Ілона Миколаївна', '0981111112', 'byjna.ilmy@outlook.com', 'Касир'),
(3, 'S9w5CpfYXe', 'Гадяк Вадим Богданович', '098111113', 'gadvad@gmail.com', 'Касир'),
(4, 'o0N5pESQs3', 'Федор Федор Федорович', '0977777777', 'inferno.king@yahoo.com', 'Продавець пального'),
(5, 'U5F203sgWB', 'Соболь Олена Антонівна', '0981111115', 'Sobolena@gmail.com', 'Касир');

-- --------------------------------------------------------

--
-- Структура таблицы `типи_пального`
--

CREATE TABLE `типи_пального` (
  `id_пального` int(11) NOT NULL,
  `Назва` varchar(20) NOT NULL,
  `Залишок_л` int(11) DEFAULT NULL,
  `Ціна_за_1_л` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `типи_пального`
--

INSERT INTO `типи_пального` (`id_пального`, `Назва`, `Залишок_л`, `Ціна_за_1_л`) VALUES
(1, 'Дизель', 4600, '30.00'),
(2, 'Преміум-дизель', 3500, '32.00'),
(3, 'Бензин А-95', 6000, '34.00'),
(4, 'Бензин А-92', 4500, '32.00'),
(5, 'Бензин А-98', 2800, '36.00'),
(6, 'Дизель Euro-5', 3900, '31.50'),
(7, 'Дизель Euro-6', 3000, '32.50'),
(8, 'Бензин А-80', 3000, '30.00'),
(9, 'Бензин А-91', 3200, '31.00'),
(10, 'Бензин А-100', 2000, '38.00');

-- --------------------------------------------------------

--
-- Структура таблицы `товари`
--

CREATE TABLE `товари` (
  `id_товару` int(11) NOT NULL,
  `Назва_товару` varchar(30) NOT NULL,
  `Ціна` decimal(10,2) NOT NULL,
  `Кількість` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `товари`
--

INSERT INTO `товари` (`id_товару`, `Назва_товару`, `Ціна`, `Кількість`) VALUES
(1, 'Вода мінеральна (0,5 літра)', '10.00', 60),
(2, 'Очисники', '15.00', 30),
(3, 'Омивачі скла', '350.00', 40),
(4, 'Ароматизатори', '100.00', 60),
(5, 'Кава (розчинна)', '18.00', 25),
(6, 'Чай (чайні пакетики)', '8.00', 43),
(7, 'Хот-дог', '22.50', 18),
(8, 'Гамбургер', '30.00', 25),
(9, 'Газети і журнали', '12.00', 20),
(10, 'Автомобільні оливи та масла', '50.00', 11);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `керування_пальним`
--
ALTER TABLE `керування_пальним`
  ADD PRIMARY KEY (`id_дії`),
  ADD KEY `купив` (`купив`),
  ADD KEY `додав` (`додав`),
  ADD KEY `id_пального` (`id_пального`);

--
-- Индексы таблицы `керування_товарами`
--
ALTER TABLE `керування_товарами`
  ADD PRIMARY KEY (`id_дії`),
  ADD KEY `купив` (`купив`),
  ADD KEY `додав` (`додав`),
  ADD KEY `id_товару` (`id_товару`);

--
-- Индексы таблицы `клієнти`
--
ALTER TABLE `клієнти`
  ADD PRIMARY KEY (`id_клієнта`);

--
-- Индексы таблицы `працівники`
--
ALTER TABLE `працівники`
  ADD PRIMARY KEY (`id_працівника`);

--
-- Индексы таблицы `типи_пального`
--
ALTER TABLE `типи_пального`
  ADD PRIMARY KEY (`id_пального`);

--
-- Индексы таблицы `товари`
--
ALTER TABLE `товари`
  ADD PRIMARY KEY (`id_товару`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `керування_пальним`
--
ALTER TABLE `керування_пальним`
  MODIFY `id_дії` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `керування_товарами`
--
ALTER TABLE `керування_товарами`
  MODIFY `id_дії` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `клієнти`
--
ALTER TABLE `клієнти`
  MODIFY `id_клієнта` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `працівники`
--
ALTER TABLE `працівники`
  MODIFY `id_працівника` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `типи_пального`
--
ALTER TABLE `типи_пального`
  MODIFY `id_пального` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `товари`
--
ALTER TABLE `товари`
  MODIFY `id_товару` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `керування_пальним`
--
ALTER TABLE `керування_пальним`
  ADD CONSTRAINT `керування_пальним_ibfk_1` FOREIGN KEY (`купив`) REFERENCES `клієнти` (`id_клієнта`),
  ADD CONSTRAINT `керування_пальним_ibfk_2` FOREIGN KEY (`додав`) REFERENCES `працівники` (`id_працівника`),
  ADD CONSTRAINT `керування_пальним_ibfk_3` FOREIGN KEY (`id_пального`) REFERENCES `типи_пального` (`id_пального`);

--
-- Ограничения внешнего ключа таблицы `керування_товарами`
--
ALTER TABLE `керування_товарами`
  ADD CONSTRAINT `керування_товарами_ibfk_1` FOREIGN KEY (`купив`) REFERENCES `клієнти` (`id_клієнта`),
  ADD CONSTRAINT `керування_товарами_ibfk_2` FOREIGN KEY (`додав`) REFERENCES `працівники` (`id_працівника`),
  ADD CONSTRAINT `керування_товарами_ibfk_3` FOREIGN KEY (`id_товару`) REFERENCES `товари` (`id_товару`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
