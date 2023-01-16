-- 스키마 제작
CREATE SCHEMA `project7smartstore`;
-- 회원 가입을 통해 받는 유저 정보 테이블
CREATE TABLE `project7smartstore`.`user_info` (`idx` INT NOT NULL, `user_id` VARCHAR(16) NOT NULL, `user_pw` VARCHAR(16) NOT NULL, `user_name` VARCHAR(16) NOT NULL, `user_tel` INT NOT NULL, `temp` VARCHAR(16) NOT NULL, `user_type` INT NOT NULL);
