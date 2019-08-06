/*
 Navicat Premium Data Transfer

 Source Server         : Tencent
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : 123.207.27.93:3306
 Source Schema         : maoyan

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 25/07/2019 22:42:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for top_100
-- ----------------------------
DROP TABLE IF EXISTS `top_100`;
CREATE TABLE `top_100`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ranking` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stars` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `release_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `score` float(3, 1) NOT NULL,
  `img_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
