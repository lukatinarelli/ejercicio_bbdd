-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: fdb1031.007sites.com
-- Tiempo de generación: 15-10-2024 a las 16:41:52
-- Versión del servidor: 8.0.32
-- Versión de PHP: 8.1.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `4411658_enterprise`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Autor`
--

CREATE TABLE `Autor` (
  `Código` int NOT NULL,
  `Nombre` text NOT NULL,
  `DNI` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Autor`
--

INSERT INTO `Autor` (`Código`, `Nombre`, `DNI`) VALUES
(1, 'J. K. Rowling', ''),
(2, 'Oliver Bowden', ''),
(3, 'Oscar Wilde', ''),
(4, 'VICTOR HUGO', '47132938A');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Ejemplar`
--

CREATE TABLE `Ejemplar` (
  `Código` int NOT NULL,
  `Localización` text NOT NULL,
  `CódigoLibro` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Ejemplar`
--

INSERT INTO `Ejemplar` (`Código`, `Localización`, `CódigoLibro`) VALUES
(13, 'Biblioteca Municipal Coll D´En Rabassa - Carrer de Son Rossinyol, 1, Platja de Palma, 07007 Palma, Illes Balears', 1),
(14, 'Biblioteca Municipal Molinar - Carrer de Francesc Femenias, 1, Platja de Palma, 07006 Palma, Illes Balears', 1),
(15, 'Biblioteca Municipal Coll D´En Rabassa - Carrer de Son Rossinyol, 1, Platja de Palma, 07007 Palma, Illes Balears', 2),
(16, 'Biblioteca Municipal Molinar - Carrer de Francesc Femenias, 1, Platja de Palma, 07006 Palma, Illes Balears', 2),
(17, 'Biblioteca Municipal Coll D´En Rabassa - Carrer de Son Rossinyol, 1, Platja de Palma, 07007 Palma, Illes Balears', 3),
(18, 'Biblioteca Municipal Molinar - Carrer de Francesc Femenias, 1, Platja de Palma, 07006 Palma, Illes Balears', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Escribe`
--

CREATE TABLE `Escribe` (
  `CódigoAutor` int NOT NULL,
  `CódigoLibro` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Libros`
--

CREATE TABLE `Libros` (
  `Código` int NOT NULL,
  `Título` text NOT NULL,
  `ISBN` bigint NOT NULL,
  `Editorial` text NOT NULL,
  `Páginas` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Libros`
--

INSERT INTO `Libros` (`Código`, `Título`, `ISBN`, `Editorial`, `Páginas`) VALUES
(1, 'Harry Potter y la piedra filosofal', 9788478884452, 'Salamandra', 254),
(2, 'Assassin´s Creed: Renaissance', 9788445010617, 'Minotauro', 400),
(3, 'El retrato de Dorian Gray', 9788467033939, 'Austral', 288),
(4, 'LOS MISERABLES', 9788408015796, 'Austral', 1312),
(5, 'IT', 0, '', 1504);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Saca`
--

CREATE TABLE `Saca` (
  `CódigoUsuario` int NOT NULL,
  `CódigoEjemplar` int NOT NULL,
  `FechaPres` date NOT NULL,
  `FechaDevol` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Saca`
--

INSERT INTO `Saca` (`CódigoUsuario`, `CódigoEjemplar`, `FechaPres`, `FechaDevol`) VALUES
(1, 13, '2023-12-13', '0000-00-00'),
(2, 15, '2024-01-03', '0000-00-00'),
(1, 15, '2024-02-13', '0000-00-00'),
(2, 17, '2024-03-01', '2023-03-13'),
(3, 18, '2024-03-01', '2023-03-13');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuario`
--

CREATE TABLE `Usuario` (
  `Código` int NOT NULL,
  `Nombre` text NOT NULL,
  `Teléfono` int NOT NULL,
  `Dirección` text NOT NULL,
  `PROVINCIA` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Usuario`
--

INSERT INTO `Usuario` (`Código`, `Nombre`, `Teléfono`, `Dirección`, `PROVINCIA`) VALUES
(1, 'Luka Ramon Tinarelli', 666999666, 'Carrer Jacob Sureda 17 2D, 07007, Palma de Mallorca, Islas Baleares', 'Illes Balears'),
(2, 'Pedro Acosta', 638373581, 'Avenida Juan Gris 47,28691, Villanueva de la Cañada, Madrid', 'Illes Balears'),
(3, 'Miguel Torres', 633308900, 'Calle Pere Quintana, 17, 07007, Palma de Mallorca, Islas Baleares', 'Illes Balears'),
(4, 'José Antonio Fernandez', 0, '', 'Illes Balears');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Autor`
--
ALTER TABLE `Autor`
  ADD PRIMARY KEY (`Código`);

--
-- Indices de la tabla `Ejemplar`
--
ALTER TABLE `Ejemplar`
  ADD PRIMARY KEY (`Código`),
  ADD KEY `CódigoLibro` (`CódigoLibro`);

--
-- Indices de la tabla `Escribe`
--
ALTER TABLE `Escribe`
  ADD KEY `CódigoAutor` (`CódigoAutor`),
  ADD KEY `CódigoLibro` (`CódigoLibro`);

--
-- Indices de la tabla `Libros`
--
ALTER TABLE `Libros`
  ADD PRIMARY KEY (`Código`);

--
-- Indices de la tabla `Saca`
--
ALTER TABLE `Saca`
  ADD KEY `CódigoUsuario` (`CódigoUsuario`),
  ADD KEY `CódigoEjemplar` (`CódigoEjemplar`);

--
-- Indices de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`Código`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Autor`
--
ALTER TABLE `Autor`
  MODIFY `Código` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `Ejemplar`
--
ALTER TABLE `Ejemplar`
  MODIFY `Código` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `Libros`
--
ALTER TABLE `Libros`
  MODIFY `Código` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `Código` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Ejemplar`
--
ALTER TABLE `Ejemplar`
  ADD CONSTRAINT `Ejemplar_ibfk_1` FOREIGN KEY (`CódigoLibro`) REFERENCES `Libros` (`Código`);

--
-- Filtros para la tabla `Escribe`
--
ALTER TABLE `Escribe`
  ADD CONSTRAINT `Escribe_ibfk_1` FOREIGN KEY (`CódigoLibro`) REFERENCES `Libros` (`Código`),
  ADD CONSTRAINT `Escribe_ibfk_2` FOREIGN KEY (`CódigoAutor`) REFERENCES `Autor` (`Código`);

--
-- Filtros para la tabla `Saca`
--
ALTER TABLE `Saca`
  ADD CONSTRAINT `Saca_ibfk_1` FOREIGN KEY (`CódigoEjemplar`) REFERENCES `Ejemplar` (`Código`),
  ADD CONSTRAINT `Saca_ibfk_2` FOREIGN KEY (`CódigoUsuario`) REFERENCES `Usuario` (`Código`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
