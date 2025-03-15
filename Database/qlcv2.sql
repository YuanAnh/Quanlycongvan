-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th3 15, 2025 lúc 03:14 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `qlcv2`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `baocaothongke`
--

CREATE TABLE `baocaothongke` (
  `baocaoid` varchar(50) NOT NULL,
  `loaibaocao` enum('Công văn đi','Công văn đến','Theo phòng ban','Theo người ký') NOT NULL,
  `thoigian` date NOT NULL,
  `soluong` int(11) NOT NULL,
  `filebaocao` varchar(255) DEFAULT NULL,
  `createdat` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `congvanden`
--

CREATE TABLE `congvanden` (
  `congvandenid` varchar(50) NOT NULL,
  `socongvan` varchar(50) NOT NULL,
  `ngaynhan` date NOT NULL,
  `noigui` varchar(255) NOT NULL,
  `noidung` text NOT NULL,
  `trangthai` enum('Đã xử lý','Đang xử lý','Chưa xử lý') DEFAULT 'Chưa xử lý',
  `phongbanphutrach` varchar(100) NOT NULL,
  `linkdinhkem` varchar(5000) DEFAULT NULL,
  `createdat` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `congvanden`
--

INSERT INTO `congvanden` (`congvandenid`, `socongvan`, `ngaynhan`, `noigui`, `noidung`, `trangthai`, `phongbanphutrach`, `linkdinhkem`, `createdat`) VALUES
('CVD04', '123/1234', '2000-01-01', 'Sở Giáo Dục', 'Không', 'Đã xử lý', 'Phòng Kinh Doanh', 'file.pdf', '2025-03-15 13:58:18');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `congvandi`
--

CREATE TABLE `congvandi` (
  `congvandiid` varchar(50) NOT NULL,
  `socongvan` varchar(50) NOT NULL,
  `noidung` text NOT NULL,
  `nguoiky` varchar(100) NOT NULL,
  `ngayphathanh` date NOT NULL,
  `noinhan` varchar(255) NOT NULL,
  `phongbanphutrach` varchar(5000) NOT NULL,
  `loaicongvan` enum('Nội bộ','Gửi đối tác','Gửi cơ quan nhà nước','Khẩn cấp') NOT NULL,
  `trangthai` enum('Đã gửi','Chưa gửi','Đang chờ duyệt') DEFAULT 'Chưa gửi',
  `linkdinhkem` varchar(5000) DEFAULT NULL,
  `createdby` varchar(50) DEFAULT NULL,
  `createdat` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `congvandi`
--

INSERT INTO `congvandi` (`congvandiid`, `socongvan`, `noidung`, `nguoiky`, `ngayphathanh`, `noinhan`, `phongbanphutrach`, `loaicongvan`, `trangthai`, `linkdinhkem`, `createdby`, `createdat`) VALUES
('CV01', '123', 'Không', 'Lê Anh Phong', '2000-01-01', 'Bộ Giao Thông Vận Tải', 'Phòng Hành Chính', 'Gửi cơ quan nhà nước', 'Đang chờ duyệt', 'E:/Tài liệu ôn thi/Bộ câu hỏi ôn tập -TACN-ok 2025.docx', 'Lãnh đạo', '2025-03-15 13:52:02');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `congvanngoai`
--

CREATE TABLE `congvanngoai` (
  `id` varchar(50) NOT NULL,
  `congvandiid` varchar(50) NOT NULL,
  `phongbanid` varchar(50) NOT NULL,
  `trangthai` enum('Đã gửi','Chờ gửi','Đang chờ duyệt') DEFAULT 'Chờ gửi',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `congvannoibo`
--

CREATE TABLE `congvannoibo` (
  `id` varchar(50) NOT NULL,
  `congvandenid` varchar(50) NOT NULL,
  `phongbanid` varchar(50) NOT NULL,
  `trangthai` enum('Chờ xử lý','Đang xử lý','Hoàn thành') DEFAULT 'Chờ xử lý',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lichsutruycap`
--

CREATE TABLE `lichsutruycap` (
  `lichsuid` varchar(50) NOT NULL,
  `userid` varchar(50) NOT NULL,
  `hanhdong` enum('Xem','Sửa','Xóa') NOT NULL,
  `congvanid` varchar(50) NOT NULL,
  `loaicongvan` enum('Công văn đi','Công văn đến') NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `luutrucongvan`
--

CREATE TABLE `luutrucongvan` (
  `luutruid` varchar(50) NOT NULL,
  `socongvan` varchar(50) NOT NULL,
  `tieude` varchar(255) NOT NULL,
  `noidung` text NOT NULL,
  `linkdinhkem` varchar(255) DEFAULT NULL,
  `phongbanphutrach` varchar(5000) NOT NULL,
  `createdat` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `luutrucongvan`
--

INSERT INTO `luutrucongvan` (`luutruid`, `socongvan`, `tieude`, `noidung`, `linkdinhkem`, `phongbanphutrach`, `createdat`) VALUES
('LT01', 'S1004', 'Công Văn Đến', 'Công văn về kế hoạch tổ chức sự kiện văn hóa.', 'N/A', 'Phòng Văn Hóa', '2025-03-11 19:18:50'),
('LT02', '123', 'Công Văn Đến', 'Không có', 'file.pdf', 'Phòng Hành Chính', '2025-03-15 14:01:45');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `pheduyetcongvan`
--

CREATE TABLE `pheduyetcongvan` (
  `pheduyetid` varchar(50) NOT NULL,
  `congvanid` varchar(50) NOT NULL,
  `loaicongvan` enum('Công văn đi','Công văn đến') NOT NULL,
  `nguoipheduyet` varchar(50) NOT NULL,
  `trangthai` enum('Đã duyệt','Yêu cầu chỉnh sửa','Từ chối') DEFAULT 'Yêu cầu chỉnh sửa',
  `ghichu` text DEFAULT NULL,
  `approvedat` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `pheduyetcongvan`
--

INSERT INTO `pheduyetcongvan` (`pheduyetid`, `congvanid`, `loaicongvan`, `nguoipheduyet`, `trangthai`, `ghichu`, `approvedat`) VALUES
('PD01', 'CV01', 'Công văn đi', 'Lãnh đạo', 'Yêu cầu chỉnh sửa', 'Có lỗi', '2025-03-07 17:00:00');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `phongbanngoai`
--

CREATE TABLE `phongbanngoai` (
  `id` varchar(50) NOT NULL,
  `tenphongban` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `phongbanngoai`
--

INSERT INTO `phongbanngoai` (`id`, `tenphongban`) VALUES
('PBN04', 'Bộ Công An'),
('PBN05', 'Bộ Công Thương'),
('PBN03', 'Bộ Giao Thông Vận Tải'),
('PBN06', 'Chính Phủ'),
('PBN01', 'Sở Giáo Dục'),
('PBN02', 'Sở Y Tế');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `phongbannoi`
--

CREATE TABLE `phongbannoi` (
  `id` varchar(50) NOT NULL,
  `tenphongban` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `phongbannoi`
--

INSERT INTO `phongbannoi` (`id`, `tenphongban`) VALUES
('PB01', 'Phòng Hành Chính'),
('PB02', 'Phòng Kế Toán'),
('PB05', 'Phòng Kinh Doanh'),
('PB04', 'Phòng Kỹ Thuật'),
('PB03', 'Phòng Nhân Sự'),
('PB06', 'Phòng Tài Chính');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `user`
--

CREATE TABLE `user` (
  `userid` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `passwordhash` varchar(255) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `ngaysinh` date NOT NULL,
  `gioitinh` enum('Nam','Nữ') NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `role` enum('Admin','Nhân viên văn thư','Lãnh đạo') NOT NULL,
  `createdat` timestamp NOT NULL DEFAULT current_timestamp(),
  `cauhoi1` varchar(5000) NOT NULL,
  `cauhoi2` varchar(5000) NOT NULL,
  `cauhoi3` varchar(5000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `user`
--

INSERT INTO `user` (`userid`, `username`, `passwordhash`, `fullname`, `ngaysinh`, `gioitinh`, `email`, `phone`, `role`, `createdat`, `cauhoi1`, `cauhoi2`, `cauhoi3`) VALUES
('ID01', 'anhphong', '1', 'Lê Anh Phong', '2004-09-08', 'Nam', 'anhphong@gmail.com', '0932410983', 'Lãnh đạo', '2025-03-15 13:47:07', 'MU', 'XC', 'Chó');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `baocaothongke`
--
ALTER TABLE `baocaothongke`
  ADD PRIMARY KEY (`baocaoid`);

--
-- Chỉ mục cho bảng `congvanden`
--
ALTER TABLE `congvanden`
  ADD PRIMARY KEY (`congvandenid`),
  ADD UNIQUE KEY `socongvan` (`socongvan`);

--
-- Chỉ mục cho bảng `congvandi`
--
ALTER TABLE `congvandi`
  ADD PRIMARY KEY (`congvandiid`),
  ADD UNIQUE KEY `socongvan` (`socongvan`),
  ADD KEY `createdby` (`createdby`);

--
-- Chỉ mục cho bảng `congvanngoai`
--
ALTER TABLE `congvanngoai`
  ADD PRIMARY KEY (`id`),
  ADD KEY `congvandiid` (`congvandiid`),
  ADD KEY `congvanngoai_ibfk_2` (`phongbanid`);

--
-- Chỉ mục cho bảng `congvannoibo`
--
ALTER TABLE `congvannoibo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `congvandenid` (`congvandenid`),
  ADD KEY `congvannoibo_ibfk_2` (`phongbanid`);

--
-- Chỉ mục cho bảng `lichsutruycap`
--
ALTER TABLE `lichsutruycap`
  ADD PRIMARY KEY (`lichsuid`),
  ADD KEY `userid` (`userid`);

--
-- Chỉ mục cho bảng `luutrucongvan`
--
ALTER TABLE `luutrucongvan`
  ADD PRIMARY KEY (`luutruid`),
  ADD UNIQUE KEY `socongvan` (`socongvan`);

--
-- Chỉ mục cho bảng `pheduyetcongvan`
--
ALTER TABLE `pheduyetcongvan`
  ADD PRIMARY KEY (`pheduyetid`),
  ADD KEY `nguoipheduyet` (`nguoipheduyet`);

--
-- Chỉ mục cho bảng `phongbanngoai`
--
ALTER TABLE `phongbanngoai`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tenphongban` (`tenphongban`);

--
-- Chỉ mục cho bảng `phongbannoi`
--
ALTER TABLE `phongbannoi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tenphongban` (`tenphongban`);

--
-- Chỉ mục cho bảng `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userid`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `congvanngoai`
--
ALTER TABLE `congvanngoai`
  ADD CONSTRAINT `congvanngoai_ibfk_1` FOREIGN KEY (`congvandiid`) REFERENCES `congvandi` (`congvandiid`),
  ADD CONSTRAINT `congvanngoai_ibfk_2` FOREIGN KEY (`phongbanid`) REFERENCES `phongbanngoai` (`id`);

--
-- Các ràng buộc cho bảng `congvannoibo`
--
ALTER TABLE `congvannoibo`
  ADD CONSTRAINT `congvannoibo_ibfk_1` FOREIGN KEY (`congvandenid`) REFERENCES `congvanden` (`congvandenid`),
  ADD CONSTRAINT `congvannoibo_ibfk_2` FOREIGN KEY (`phongbanid`) REFERENCES `phongbannoi` (`id`);

--
-- Các ràng buộc cho bảng `lichsutruycap`
--
ALTER TABLE `lichsutruycap`
  ADD CONSTRAINT `lichsutruycap_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
